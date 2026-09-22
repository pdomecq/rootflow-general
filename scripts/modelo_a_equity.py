#!/usr/bin/env python3
"""Convierte el Modelo Financiero V14 (tramo inversor = prestamo participativo)
en V15: el inversor entra en CAPITAL con un % del equity y una salida pactada.

Cambios, todos reversibles (la estructura 5 es nueva; las 1-4 siguen igual):
  Hipotesis
    D94  = 5            nueva estructura "Capital (equity)"
    D119 = 10%          equity cedido al inversor (antes kicker 2,5%)
    D124 = 48           mes de salida del inversor (derecho desde el ano 4)
    D125 = 1            sumar caja neta al valor de salida
    D126 = 3            mes previsto de formalizacion de ENISA (chequeo FFPP)
  Hojas mensuales (x4)
    f89   saldo vivo FFF = 0 con estructura 5 (no es deuda -> desbloquea dividendos)
    f92   servicio FFF = 0 con estructura 5
    f94   pasa a acumular lo COBRADO por el inversor (para que el payback sea real)
    f121  anade el cobro de la salida en el mes pactado
    f122  idem en el flujo del stack
    f133  valor de salida = EQUITY (EV + caja - deuda) con estructura 5
    f152+ bloque nuevo: calculo del valor de salida
    f160+ bloque nuevo: chequeo del requisito de fondos propios de ENISA
  Resumen
    C53   CHOOSE ampliado con la 5a estructura
"""
import openpyxl, sys
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

ORIGEN = "/root/.claude/uploads/6f26b853-9262-5df8-baaf-05a855956a32/9c6a69ab-Rootflow_Modelo_Financiero_v14-20-07-26_1.xlsx"
RUTA = "modelo/Rootflow_Modelo_Financiero_V15_equity.xlsx"
MENSUALES = ["Modelo_Mensual","Esc_Conservador","Esc_Base","Esc_Optimista"]
COL0, COLN = 3, 86          # C..CH = meses 1..84

def main(importe=100000, pre_money=900000, importe_enisa=100000, mes_salida=48, mes_enisa=3, suelo=1.5, destino=RUTA):
    pct_equity = importe / (pre_money + importe)
    wb = openpyxl.load_workbook(ORIGEN, data_only=False)

    # ---------------- Hipotesis ----------------
    h = wb["Hipótesis"]
    h["A94"] = "Estructura (1=Préstamo·2=Participativo·3=Ctas.particip.·4=Rev-share·5=CAPITAL)"
    h["D92"] = importe
    h["D104"] = importe_enisa
    h["D94"] = 5
    h["A119"] = "Equity cedido al inversor (estructura 5: su participación real)"
    h["D119"] = pct_equity
    h["A123"] = "SALIDA DEL INVERSOR (solo estructura 5 · capital)"
    h["A123"].font = Font(bold=True)
    h["A124"] = "Mes de salida del inversor (derecho pactado desde el año 4)"
    h["B124"] = "mes"; h["D124"] = mes_salida
    h["A125"] = "¿Sumar la caja neta al valor de salida? (1=sí / 0=no)"
    h["B125"] = "1/0"; h["D125"] = 1
    h["A126"] = "Mes previsto de formalización de ENISA (para el chequeo de fondos propios)"
    h["B126"] = "mes"; h["D126"] = mes_enisa
    h["A127"] = "Suelo de cobro a la salida (múltiplo mínimo sobre lo invertido) — protege la bajada"
    h["B127"] = "x"; h["D127"] = suelo

    # ---------------- Hojas mensuales ----------------
    for name in MENSUALES:
        ws = wb[name]

        # f89 · saldo vivo FFF: con capital no hay deuda viva (desbloquea dividendos)
        ws.cell(row=89, column=COL0).value = "=IF(Hipótesis!$D$94=5,0,Hipótesis!$D$93)"

        for col in range(COL0, COLN+1):
            L = get_column_letter(col)

            # f92 · servicio FFF = 0 con estructura 5 (si no, caeria en la rama de rev-share)
            ws.cell(row=92, column=col).value = (
                f"=IF(Hipótesis!$D$94=5,0,"
                f"IF(Hipótesis!$D$94=1,{L}90+{L}91,"
                f"IF(Hipótesis!$D$94=2,{L}90+{L}91+IF({L}89>0,Hipótesis!$D$98*MAX(0,{L}56),0),"
                f"IF(Hipótesis!$D$94=3,Hipótesis!$D$99*MAX(0,{L}56),Hipótesis!$D$100*{L}36))))")

            # f121 · flujo del inversor: servicio + cobro de la salida en el mes pactado
            cobro = (f"IF(Hipótesis!$D$94=5,IF({L}$3=Hipótesis!$D$124,$C$158,0),"
                     f"IF({L}$3=84,$C$134,0))")
            ws.cell(row=121, column=col).value = f"={L}93+{cobro}"
            # f122 · flujo del stack (empresa)
            ws.cell(row=122, column=col).value = f"=-{L}106-{cobro}"

            # f94 · acumulado COBRADO por el inversor (antes: solo servicio de deuda)
            if col == COL0:
                ws.cell(row=94, column=col).value = f"={L}121"
            else:
                P = get_column_letter(col-1)
                ws.cell(row=94, column=col).value = f"={P}94+{L}121"

        ws["A94"] = "Inversor · acumulado cobrado"

        # f133 · valor de salida: equity real con estructura 5
        ws["C133"] = "=IF(Hipótesis!$D$94=5,$C$157,$C$132*Hipótesis!$D$120)"
        ws["A134"] = "Pago de equity al inversor a la salida (€)"

        # ---- Bloque nuevo: calculo del valor de salida ----
        ws["A152"] = "SALIDA DEL INVERSOR — VALOR DEL EQUITY (estructura 5)"
        ws["A152"].font = Font(bold=True)
        ws["A153"] = "EBITDA de los 12 meses previos a la salida (€)"
        ws["C153"] = ('=SUMIFS($C$56:$CH$56,$C$3:$CH$3,">="&Hipótesis!$D$124-11,'
                      '$C$3:$CH$3,"<="&Hipótesis!$D$124)')
        ws["A154"] = "Valor de empresa a la salida (EV = EBITDA × múltiplo) (€)"
        ws["C154"] = "=$C$153*Hipótesis!$D$120"
        ws["A155"] = "Caja acumulada en el mes de salida (€)"
        ws["C155"] = '=SUMIFS($C$86:$CH$86,$C$3:$CH$3,"="&Hipótesis!$D$124)'
        ws["A156"] = "Deuda viva en el mes de salida (ENISA + SAECA + FFF) (€)"
        ws["C156"] = ('=SUMIFS($C$96:$CH$96,$C$3:$CH$3,"="&Hipótesis!$D$124)'
                      '+SUMIFS($C$101:$CH$101,$C$3:$CH$3,"="&Hipótesis!$D$124)'
                      '+SUMIFS($C$89:$CH$89,$C$3:$CH$3,"="&Hipótesis!$D$124)')
        ws["A157"] = "VALOR DEL EQUITY A LA SALIDA (€)"
        ws["A157"].font = Font(bold=True)
        ws["C157"] = "=MAX(0,$C$154+Hipótesis!$D$125*($C$155-$C$156))"
        ws["A158"] = "Cobro del inversor a la salida (€) — con suelo de protección"
        ws["C158"] = ("=MIN($C$157,MAX($C$157*Hipótesis!$D$119,"
                      "Hipótesis!$D$127*Hipótesis!$D$93))")
        ws["A159"] = "   · de los cuales, por el suelo de protección (€)"
        ws["C159"] = "=MAX(0,$C$158-$C$157*Hipótesis!$D$119)"

        # ---- Bloque nuevo: chequeo del requisito de ENISA ----
        ws["A160"] = "CHEQUEO ENISA — FONDOS PROPIOS ≥ IMPORTE SOLICITADO"
        ws["A160"].font = Font(bold=True)
        ws["A161"] = "Fondos propios aportados por la ronda (€)"
        ws["C161"] = "=IF(Hipótesis!$D$94=5,Hipótesis!$D$93,0)"
        ws["A162"] = "Resultado acumulado hasta el mes de formalización (€)"
        ws["C162"] = '=SUMIFS($C$63:$CH$63,$C$3:$CH$3,"<="&Hipótesis!$D$126)'
        ws["A163"] = "FONDOS PROPIOS ESTIMADOS a la formalización (€)"
        ws["A163"].font = Font(bold=True)
        ws["C163"] = "=$C$161+$C$162"
        ws["A164"] = "Importe de ENISA solicitado (€)"
        ws["C164"] = "=Hipótesis!$D$105"
        ws["A165"] = "¿CUMPLE el requisito de fondos propios de ENISA?"
        ws["A165"].font = Font(bold=True)
        ws["C165"] = ('=IF($C$163>=$C$164,"SI CUMPLE",'
                      '"NO CUMPLE - faltan "&TEXT($C$164-$C$163,"#,##0")&" EUR")')

    # ---------------- Resumen ----------------
    r = wb["Resumen"]
    r["C53"] = ('=CHOOSE(Hipótesis!$D$94,"Préstamo simple","Préstamo participativo",'
                '"Cuentas en participación","Revenue-share","Capital (equity)")')

    wb.save(destino)
    print(f"escrito {destino}: ronda {importe:,} EUR -> {pct_equity:.1%}, ENISA {importe_enisa:,}, salida mes {mes_salida}, formalizacion mes {mes_enisa}")

if __name__ == "__main__":
    a = sys.argv[1:]
    main(importe=int(a[0]) if len(a)>0 else 100000,
         pre_money=int(a[1]) if len(a)>1 else 900000,
         importe_enisa=int(a[2]) if len(a)>2 else 100000,
         mes_salida=int(a[3]) if len(a)>3 else 48,
         mes_enisa=int(a[4]) if len(a)>4 else 3,
         suelo=float(a[5]) if len(a)>5 else 1.5,
         destino=a[6] if len(a)>6 else RUTA)
