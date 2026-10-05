#!/usr/bin/env python3
"""Cierre de septiembre 2026 a partir de los datos del ERP (Supabase, proyecto «rootflow erp v3»).

Datos extraídos el 05/10/2026 de las tablas facturas, albaranes, pedidos, recibos_tpv, gastos y lotes,
y de los PDF de las facturas de gasto (periodos de luz, agua, alquiler y software).
Todo sin IVA. Uso: python3 scripts/cierre_septiembre.py finanzas/Cierre_Septiembre_2026.xlsx
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as CL

OUT = sys.argv[1] if len(sys.argv) > 1 else "finanzas/Cierre_Septiembre_2026.xlsx"
F = "Arial"
BASE = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
BLUE = Font(name=F, size=10, color="0000FF")
GREEN = Font(name=F, size=10, color="008000")
GREEN_B = Font(name=F, size=10, color="008000", bold=True)
WHITE = Font(name=F, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=F, size=14, bold=True, color="1D4F37")
SUB = Font(name=F, size=10, italic=True, color="666666")
SEC = Font(name=F, size=11, bold=True, color="1D4F37")
HEAD = PatternFill("solid", fgColor="1D4F37")
YELLOW = PatternFill("solid", fgColor="FFFF00")
TOTAL = PatternFill("solid", fgColor="E6F2EA")
LINE = Border(top=Side(style="thin", color="1D4F37"))
EUR = '#,##0.00" €";(#,##0.00" €");"-"'
PCT = '0.0%;(0.0%);"-"'
DATE = "dd/mm/yyyy"

wb = Workbook()


def hoja(nombre, titulo, sub, anchos):
    ws = wb.create_sheet(nombre)
    ws["A1"] = titulo; ws["A1"].font = TITLE
    ws["A2"] = sub; ws["A2"].font = SUB
    for i, w in enumerate(anchos, 1):
        ws.column_dimensions[CL(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws


def cabecera(ws, fila, textos):
    for i, t in enumerate(textos, 1):
        c = ws.cell(row=fila, column=i, value=t)
        c.font = WHITE; c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[fila].height = 30


def fila(ws, r, valores, fmts, fonts=None):
    for i, (v, f) in enumerate(zip(valores, fmts), 1):
        c = ws.cell(row=r, column=i, value=v)
        if f: c.number_format = f
        c.font = (fonts[i - 1] if fonts else BASE) or BASE
        c.alignment = Alignment(vertical="top", wrap_text=isinstance(v, str) and len(v) > 40)


from datetime import date as D

# ============================================================== INGRESOS
wi = hoja("Ingresos", "Ingresos de septiembre 2026 — por fecha de entrega",
          "Base imponible sin IVA. Una venta cuenta en septiembre si se entregó en septiembre, aunque la factura sea de otro mes. "
          "Fuente: albaranes, facturas y recibos TPV del ERP.",
          [12, 30, 15, 13, 12, 12, 10, 12, 16, 70])
cabecera(wi, 4, ["Entrega", "Cliente", "Albarán / ticket", "Factura", "Fecha factura", "Base (€)", "IVA (€)",
                 "Total (€)", "¿Ingreso de septiembre?", "Nota"])
ING = [
    (D(2026, 9, 1), "La Huerta Hermanos Nieto", "A-2026-0009", "F-2026-0010", D(2026, 9, 28), 116.80, 4.67, "Sí", "40 cilantro + 20 albahaca 30 g, 20 % dto."),
    (D(2026, 9, 8), "La Huerta Hermanos Nieto", "A-2026-0013", "F-2026-0010", D(2026, 9, 28), 116.80, 4.67, "Sí", "Igual, 20 % dto."),
    (D(2026, 9, 15), "La Huerta Hermanos Nieto", "A-2026-0016", "F-2026-0010", D(2026, 9, 28), 138.60, 5.54, "Sí",
     "SIN el 20 % dto. que llevan los demás. El pedido 28 decía 114,00 €. Revisar precio pactado."),
    (D(2026, 9, 21), "La Huerta Hermanos Nieto", "A-2026-0018", "F-2026-0010", D(2026, 9, 28), 147.50, 5.90, "Sí", "SIN el 20 % dto."),
    (D(2026, 9, 28), "La Huerta Hermanos Nieto", "A-2026-0021", "F-2026-0010", D(2026, 9, 28), 120.00, 4.80, "Sí", "20 % dto."),
    (D(2026, 9, 3), "Albahaca Ecotienda", "A-2026-0010", "F-2026-0003", D(2026, 8, 21), 48.45, 1.94, "Sí",
     "La factura figura con fecha 21/08, pero el pedido y la entrega son del 3/09. Cobrada el 21/09."),
    (D(2026, 9, 5), "Frutas Félix Vázquez", "A-2026-0015", "F-2026-0009", D(2026, 9, 14), 33.00, 1.32, "Sí", "Primer pedido."),
    (D(2026, 9, 10), "Frutas Félix Vázquez", "A-2026-0014", "F-2026-0009", D(2026, 9, 14), 41.25, 1.65, "Sí", ""),
    (D(2026, 9, 16), "Frutas Félix Vázquez", "A-2026-0017", "F-2026-0014", D(2026, 10, 1), 65.80, 2.63, "Sí",
     "Entregado en septiembre, facturado el 1/10."),
    (D(2026, 9, 24), "Frutas Félix Vázquez", "A-2026-0020", "F-2026-0014", D(2026, 10, 1), 49.45, 1.98, "Sí",
     "Entregado en septiembre, facturado el 1/10."),
    (D(2026, 9, 15), "Venta directa (TPV)", "Ticket 5", "—", None, 4.81, 0.19, "Sí", ""),
    (D(2026, 9, 16), "Venta directa (TPV)", "Ticket 4", "—", None, 8.65, 0.35, "Sí", ""),
    (D(2026, 9, 24), "Venta directa (TPV)", "Ticket 3", "—", None, 8.65, 0.35, "Sí", ""),
    (D(2026, 9, 7), "El abuelo Pedro", "A-2026-0011", "SIN FACTURA", None, 124.20, 4.97, "Pendiente",
     "Entregado y sin facturar. Se emitieron F-0006 y F-0007 (67,55 € cada una) y luego se borraron del ERP."),
    (D(2026, 10, 6), "Tequendama", "Pedido 34", "F-2026-0011", D(2026, 9, 29), 31.40, 1.26, "No (octubre)",
     "Facturada el 29/09 para un evento que se entrega el 6/10: ingreso de octubre."),
    (D(2026, 9, 21), "Tequendama", "A-2026-0019", "—", None, 22.05, 0.88, "No (cancelado)",
     "El pedido 30 está cancelado, pero el albarán sigue como «entregado»."),
    (D(2026, 10, 1), "Café El Padrino", "A-2026-0022", "F-2026-0015", D(2026, 10, 2), 10.10, 0.40, "No (octubre)", ""),
    (D(2026, 10, 1), "Venta directa (TPV)", "Ticket 2", "—", None, 8.65, 0.35, "No (octubre)", ""),
]
r0 = 5
for k, (fe, cli, alb, fac, ff, base, iva, inc, nota) in enumerate(ING):
    r = r0 + k
    fila(wi, r, [fe, cli, alb, fac, ff, base, iva, f"=F{r}+G{r}", inc, nota],
         [DATE, None, None, None, DATE, EUR, EUR, EUR, None, None],
         [BLUE, BASE, BASE, BASE, BLUE, BLUE, BLUE, BASE, BLUE, BASE])
rN = r0 + len(ING) - 1
rt = rN + 2
wi[f"A{rt}"] = "INGRESOS DE SEPTIEMBRE (entregados en septiembre)"; wi[f"A{rt}"].font = BOLD
for col in "FGH":
    c = wi[f"{col}{rt}"]; c.value = f'=SUMIFS({col}{r0}:{col}{rN},$I${r0}:$I${rN},"Sí")'
    c.number_format = EUR; c.font = BOLD; c.fill = TOTAL; c.border = LINE
wi[f"A{rt+1}"] = "Pendiente de facturar (El abuelo Pedro)"; wi[f"A{rt+1}"].font = BASE
c = wi[f"F{rt+1}"]; c.value = f'=SUMIFS(F{r0}:F{rN},$I${r0}:$I${rN},"Pendiente")'; c.number_format = EUR
ING_TOTAL, ING_PEND = f"Ingresos!$F${rt}", f"Ingresos!$F${rt+1}"

# facturas por fecha de factura (informativo)
rf = rt + 4
wi[f"A{rf}"] = "FACTURAS DEL ERP POR FECHA DE FACTURA (informativo)"; wi[f"A{rf}"].font = SEC
cabecera(wi, rf + 1, ["Fecha factura", "Cliente", "Factura", "Estado cobro", "", "Base (€)", "IVA (€)", "Total (€)",
                      "¿Fecha en septiembre?", "Nota"])
FAC = [
    (D(2026, 8, 21), "Albahaca Ecotienda", "F-2026-0003", "Cobrada 21/09", 48.45, 1.94, "No", "Fecha probablemente errónea (pedido del 3/09)."),
    (D(2026, 9, 14), "Frutas Félix Vázquez", "F-2026-0009", "Cobrada 21/09", 74.25, 2.97, "Sí", "En el ERP: estado «pagada» pero cobro «pendiente»."),
    (D(2026, 9, 28), "La Huerta Hermanos Nieto", "F-2026-0010", "Cobrada 02/10", 639.70, 25.59, "Sí", ""),
    (D(2026, 9, 29), "Tequendama", "F-2026-0011", "Pendiente", 31.40, 1.26, "Sí", "Entrega el 6/10."),
    (D(2026, 10, 1), "Frutas Félix Vázquez", "F-2026-0014", "Pendiente", 115.25, 4.61, "No", "Entregas del 16 y 24/09."),
    (D(2026, 10, 2), "Café El Padrino", "F-2026-0015", "Pendiente", 10.10, 0.40, "No", ""),
]
for k, (ff, cli, fac, cob, base, iva, sep, nota) in enumerate(FAC):
    r = rf + 2 + k
    fila(wi, r, [ff, cli, fac, cob, None, base, iva, f"=F{r}+G{r}", sep, nota],
         [DATE, None, None, None, None, EUR, EUR, EUR, None, None],
         [BLUE, BASE, BASE, BASE, BASE, BLUE, BLUE, BASE, BLUE, BASE])
rfa, rfb = rf + 2, rf + 1 + len(FAC)
rft = rfb + 1
wi[f"A{rft}"] = "Facturado con fecha de septiembre"; wi[f"A{rft}"].font = BOLD
for col in "FGH":
    c = wi[f"{col}{rft}"]; c.value = f'=SUMIFS({col}{rfa}:{col}{rfb},$I${rfa}:$I${rfb},"Sí")'
    c.number_format = EUR; c.font = BOLD; c.border = LINE
FACT_SEP = f"Ingresos!$F${rft}"
wi.freeze_panes = "A5"

# ============================================================== GASTOS
wg = hoja("Gastos", "Gastos imputados a septiembre 2026 — prorrateo por periodo",
          "Base sin IVA (el IVA soportado se recupera). Si una factura cubre varios meses, solo se imputa la parte de septiembre: "
          "Imputado = Base × Parte de septiembre ÷ Periodo. Fuente: tabla gastos del ERP y PDF de cada factura.",
          [8, 12, 22, 40, 12, 12, 11, 11, 10, 13, 15, 62])
cabecera(wg, 4, ["Nº ERP", "Fecha", "Proveedor", "Concepto (periodo de la factura)", "Total pagado (€)", "Base sin IVA (€)",
                 "Periodo (días o meses)", "Parte de septiembre", "% imputado", "Imputado a sept. (€)", "Tipo", "Nota"])
GAS = [
    (157, D(2026, 8, 27), "Anthropic", "Claude Pro (27/08–27/09)", 18.00, 18.00, 31, 26, "Estructura", "26 de sus 31 días caen en septiembre."),
    (144, D(2026, 8, 31), "Bellbro Renting", "Alquiler del local, septiembre (fra. 000020)", 535.50, 525.00, 1, 1, "Estructura",
     "525 € + 110,25 € IVA − 99,75 € retención IRPF = 535,50 €. La retención se ingresa en Hacienda (modelo 115): el coste es 525 €."),
    (140, D(2026, 9, 3), "Leroy Merlin", "Bomba y tubos", 93.29, 77.10, 1, 1, "Inversión", "Equipo puntual, no gasto recurrente."),
    (136, D(2026, 9, 4), "Seguridad Social", "Cuota de autónomos (Nico)", 2.95, 2.95, 1, 1, "Estructura",
     "De mayo a agosto la cuota fue de 88,56 €. Confirmar si la de septiembre es realmente 2,95 €."),
    (141, D(2026, 9, 14), "Leroy Merlin", "Estantería", 64.99, 53.71, 1, 1, "Inversión", "Equipo puntual."),
    (158, D(2026, 9, 16), "Anthropic", "Claude, uso extra prepago", 20.00, 20.00, 1, 1, "Estructura", ""),
    (146, D(2026, 9, 21), "Finetwork", "Recargo por impago de una factura anterior", 5.00, 4.13, 1, 1, "Estructura",
     "No es la cuota mensual: es un recargo por una factura devuelta. La cuota de septiembre no está en el ERP."),
    (151, D(2026, 9, 23), "Organik Green Zone", "Sustrato: 4 sacos de coco de 100 L", 74.00, 61.16, 1, 1, "Material",
     "Compra del mes. En la hoja Material se compara con lo realmente consumido."),
    (156, D(2026, 9, 27), "Anthropic", "Claude Pro (27/09–27/10)", 18.00, 18.00, 30, 4, "Estructura", "4 de sus 30 días caen en septiembre."),
    (159, D(2026, 9, 27), "Anthropic", "Claude Pro (27/09–27/10) — DUPLICADO", 18.00, 18.00, 30, 0, "Duplicado",
     "Es el mismo PDF que el gasto 156 (factura 8OGMHWLR-0031). Borrar uno de los dos en el ERP."),
    (153, D(2026, 9, 30), "Bellbro Renting", "Alquiler del local, octubre", 535.50, 525.00, 1, 0, "Otro mes", "Es de octubre."),
    (154, D(2026, 9, 30), "Bellbro Renting", "Agua (10/07–08/09)", 30.71, 27.92, 60, 30, "Estructura",
     "Tarifa diaria de la última factura × 30 días (8 días ya facturados + 22 estimados hasta la próxima)."),
    (155, D(2026, 9, 30), "Bellbro Renting", "Luz repercutida (15/07–15/09)", 137.51, 134.82, 62, 30, "Estructura",
     "Tarifa diaria × 30 días (15 días facturados + 15 estimados). 134,82 € + 28,31 € IVA − 25,62 € IRPF."),
    (124, D(2026, 6, 26), "Bellbro Renting", "Tasa de basura 2026, parte proporcional («6 de 12»)", 101.10, 101.10, 6, 1, "Estructura",
     "Cubre 6 meses: se imputa 1/6 a septiembre. Exenta de IVA."),
    (152, D(2026, 10, 1), "Proveedor (Polonia)", "Semillas", 354.52, 292.99, 1, 0, "Otro mes",
     "Compra de octubre para stock. En septiembre se sembró con semilla de junio: ver hoja Material."),
]
g0 = 5
for k, (n, fe, prov, conc, tot, base, per, parte, tipo, nota) in enumerate(GAS):
    r = g0 + k
    fila(wg, r, [n, fe, prov, conc, tot, base, per, parte, f"=IF(G{r}>0,H{r}/G{r},0)", f"=F{r}*I{r}", tipo, nota],
         [None, DATE, None, None, EUR, EUR, "0", "0", PCT, EUR, None, None],
         [BASE, BLUE, BASE, BASE, BLUE, BLUE, BLUE, BLUE, BASE, BASE, BLUE, BASE])
gN = g0 + len(GAS) - 1
gt = gN + 2
labels = [("Estructura", "Gastos de estructura"), ("Material", "Material comprado en septiembre"),
          ("Inversión", "Inversión puntual (equipo)")]
for k, (tipo, et) in enumerate(labels):
    r = gt + k
    wg[f"D{r}"] = et; wg[f"D{r}"].font = BASE
    c = wg[f"J{r}"]; c.value = f'=SUMIFS($J${g0}:$J${gN},$K${g0}:$K${gN},"{tipo}")'; c.number_format = EUR
rtot = gt + len(labels)
wg[f"D{rtot}"] = "TOTAL GASTOS REGISTRADOS IMPUTADOS A SEPTIEMBRE"; wg[f"D{rtot}"].font = BOLD
c = wg[f"J{rtot}"]; c.value = f"=SUM(J{gt}:J{rtot-1})"; c.number_format = EUR; c.font = BOLD; c.fill = TOTAL; c.border = LINE
G_EST, G_MAT, G_INV, G_TOT = (f"Gastos!$J${gt}", f"Gastos!$J${gt+1}", f"Gastos!$J${gt+2}", f"Gastos!$J${rtot}")
wg.freeze_panes = "A5"

# ============================================================== MATERIAL
wm = hoja("Material", "Material consumido en septiembre (estimado)",
          "En septiembre no se compró semilla (la última compra es de junio y la siguiente del 1/10) y los envases se compraron en agosto. "
          "Para medir el mes de verdad, se estima lo consumido a partir de las bandejas sembradas y las tarrinas entregadas.",
          [30, 18, 18, 14, 14, 14, 14, 52])
wm["A4"] = "1 · SEMILLA — bandejas sembradas para septiembre (tabla lotes del ERP)"; wm["A4"].font = SEC
cabecera(wm, 5, ["Variedad", "Bandejas con fecha de AGOSTO en el ERP", "Bandejas con fecha de SEPTIEMBRE",
                 "Total bandejas", "g de semilla por bandeja", "€/kg de semilla (sin IVA)", "Coste (€)", "Fuente"])
for col, w in (("B", 18), ("C", 18), ("D", 14), ("E", 14), ("F", 14), ("G", 14), ("H", 52)):
    wm.column_dimensions[col].width = w
SEM = [("Cilantro", 45, 53, 34, 7.5, "g/bandeja: ERP · €/kg: COSTES_ROOTFLOW"),
       ("Albahaca", 30, 49, 14, 37, "g/bandeja: ERP · €/kg: COSTES_ROOTFLOW"),
       ("Mostaza", 1, 5, 25, 22, "g/bandeja: ERP · €/kg: COSTES_ROOTFLOW"),
       ("Amaranto", 1, 4, 9, 50, "COSTES_ROOTFLOW (el ERP no tiene la dosis)"),
       ("Rúcula", 1, 3, 15, 11, "COSTES_ROOTFLOW (el ERP no tiene la dosis)"),
       ("Rábano verde / daikon", 1, 3, 34, 10, "COSTES_ROOTFLOW (el ERP no tiene la dosis)"),
       ("Rábano red", 1, 3, 34, 9.9, "COSTES_ROOTFLOW (rábano rose)"),
       ("Remolacha roja", 1, 0, None, None, "Sin dosis en el ERP ni en COSTES: 0,60 € por bandeja del modelo V16 (provisional)")]
for k, (v, ago, sep, g, e, fu) in enumerate(SEM):
    r = 6 + k
    coste = f"=D{r}*E{r}/1000*F{r}" if g is not None else f"=D{r}*0.6"
    fila(wm, r, [v, ago, sep, f"=B{r}+C{r}", g, e, coste, fu],
         [None, "0", "0", "0", "0", '#,##0.00', EUR, None], [BASE, BLUE, BLUE, BASE, BLUE, BLUE, BASE, BASE])
s1, s2 = 6, 5 + len(SEM)
rs = s2 + 1
wm[f"A{rs}"] = "Total semilla"; wm[f"A{rs}"].font = BOLD
for col in "BCD":
    wm[f"{col}{rs}"] = f"=SUM({col}{s1}:{col}{s2})"; wm[f"{col}{rs}"].number_format = "0"; wm[f"{col}{rs}"].font = BOLD
c = wm[f"G{rs}"]; c.value = f"=SUM(G{s1}:G{s2})"; c.number_format = EUR; c.font = BOLD; c.border = LINE
wm[f"A{rs+1}"] = ("En agosto no se sembró (producción parada): los 12 lotes con fecha 17-28/08 tienen la fecha mal y son los que se "
                  "cosecharon y vendieron en septiembre, así que su semilla y sustrato son consumo de septiembre. Cuadra con las ventas: "
                  "lo entregado en septiembre (~14 kg) pide unas 110 bandejas.")
wm[f"A{rs+1}"].font = SUB
r = rs + 3
wm[f"A{r}"] = "2 · SUSTRATO"; wm[f"A{r}"].font = SEC
cabecera(wm, r + 1, ["Concepto", "", "", "Bandejas", "Litros por bandeja", "€/litro (sin IVA)", "Coste (€)", "Fuente"])
rr = r + 2
fila(wm, rr, ["Sustrato de coco", None, None, f"=D{rs}", 2.5, "=18/1.21/100", f"=D{rr}*E{rr}*F{rr}",
              "COSTES_ROOTFLOW: saco de 100 L a 18 € con IVA, 2,5 L por bandeja"],
     [None, None, None, "0", "0.0", '#,##0.0000', EUR, None], [BASE, BASE, BASE, BASE, BLUE, BLUE, BASE, BASE])
R_SUS = rr

r = rr + 2
wm[f"A{r}"] = "3 · ENVASES — tarrinas entregadas en septiembre (albaranes)"; wm[f"A{r}"].font = SEC
cabecera(wm, r + 1, ["Formato", "", "", "Tarrinas", "", "€ por tarrina (sin IVA)", "Coste (€)", "Fuente"])
e1 = r + 2
fila(wm, e1, ["Tarrina grande (28-100 g)", None, None, 385, None, 0.17, f"=D{e1}*F{e1}", "COSTES_ROOTFLOW · incluye las 55 de El abuelo Pedro"],
     [None, None, None, "0", None, '#,##0.00', EUR, None], [BASE, BASE, BASE, BLUE, BASE, BLUE, BASE, BASE])
fila(wm, e1 + 1, ["Tarrina pequeña (5-15 g)", None, None, 100, None, 0.10, f"=D{e1+1}*F{e1+1}", "COSTES_ROOTFLOW"],
     [None, None, None, "0", None, '#,##0.00', EUR, None], [BASE, BASE, BASE, BLUE, BASE, BLUE, BASE, BASE])
re_ = e1 + 2
wm[f"A{re_}"] = "Total envases"; wm[f"A{re_}"].font = BOLD
c = wm[f"G{re_}"]; c.value = f"=SUM(G{e1}:G{e1+1})"; c.number_format = EUR; c.font = BOLD; c.border = LINE

rtm = re_ + 2
wm[f"A{rtm}"] = "MATERIAL CONSUMIDO EN SEPTIEMBRE (semilla + sustrato + envases)"; wm[f"A{rtm}"].font = BOLD
c = wm[f"G{rtm}"]; c.value = f"=G{rs}+G{R_SUS}+G{re_}"; c.number_format = EUR; c.font = BOLD; c.fill = TOTAL; c.border = LINE
M_CONS = f"Material!$G${rtm}"
wm[f"A{rtm+1}"] = "Compra de sustrato registrada en septiembre (hoja Gastos), para comparar"
c = wm[f"G{rtm+1}"]; c.value = f"={G_MAT}"; c.number_format = EUR; c.font = GREEN

# ============================================================== RESUMEN
ws = wb.active; ws.title = "Resumen"
ws.sheet_view.showGridLines = False
for i, w in enumerate([66, 16, 70], 1):
    ws.column_dimensions[CL(i)].width = w
ws["A1"] = "Rootflow — Cierre de septiembre 2026"; ws["A1"].font = TITLE
ws["A2"] = ("Todo sin IVA. Ingresos por fecha de entrega; gastos prorrateados por el periodo de cada factura. "
            "Sin sueldos de socios ni amortización del equipo. Datos del ERP a 05/10/2026."); ws["A2"].font = SUB


def linea(r, et, f, fmt=EUR, font=None, nota="", fill=None):
    ws[f"A{r}"] = et; ws[f"A{r}"].font = font or BASE
    c = ws[f"B{r}"]; c.value = f; c.number_format = fmt; c.font = font or GREEN
    if fill: c.fill = fill; ws[f"A{r}"].fill = fill
    if nota: ws[f"C{r}"] = nota; ws[f"C{r}"].font = SUB


ws["A4"] = "1 · LO QUE DICE EL ERP"; ws["A4"].font = SEC
linea(5, "Ingresos de septiembre (entregas de septiembre)", f"={ING_TOTAL}", nota="Hoja Ingresos")
linea(6, "(–) Gastos de estructura", f"=-{G_EST}", nota="Alquiler, luz, agua, basura, software, teléfono, autónomos")
linea(7, "(–) Material comprado (sustrato)", f"=-{G_MAT}")
linea(8, "(–) Inversión puntual (bomba y estantería)", f"=-{G_INV}")
linea(9, "RESULTADO CON LO REGISTRADO", "=SUM(B5:B8)", font=BOLD, fill=TOTAL)

ws["A11"] = "2 · RESULTADO OPERATIVO REAL DEL MES (para ver el break-even)"; ws["A11"].font = SEC
linea(12, "Ingresos de septiembre", "=B5")
linea(13, "(–) Gastos de estructura", "=B6")
linea(14, "(–) Material realmente consumido (estimado)", f"=-{M_CONS}",
      nota="Semilla y sustrato de las 201 bandejas sembradas para septiembre + envases de lo entregado (hoja Material)")
linea(15, "RESULTADO OPERATIVO", "=SUM(B12:B14)", font=BOLD, fill=TOTAL,
      nota="Sin la bomba ni la estantería (son inversión, no gasto del mes)")

ws["A17"] = "3 · GASTOS QUE PROBABLEMENTE FALTAN EN EL ERP (confirmar; celdas amarillas)"; ws["A17"].font = SEC
falta = [("Gestoría: no hay ninguna cuota registrada desde junio", 99.00,
          "Último importe registrado: 119,79 € con IVA (junio). Si ya no hay gestoría, poner 0."),
         ("Finetwork: cuota de septiembre (solo consta un recargo por impago)", 21.48,
          "25,99 € con IVA, como en julio y agosto. El asiento contable sí recogía 30,99 €."),
         ("Autónomos Nico: diferencia hasta la cuota habitual (88,56 − 2,95)", 85.61,
          "Si la cuota de septiembre fue realmente 2,95 €, poner 0.")]
for k, (et, v, nota) in enumerate(falta):
    r = 18 + k
    ws[f"A{r}"] = et; ws[f"A{r}"].font = BASE
    c = ws[f"B{r}"]; c.value = -v; c.number_format = EUR; c.font = BLUE; c.fill = YELLOW
    ws[f"C{r}"] = nota; ws[f"C{r}"].font = SUB
linea(21, "RESULTADO OPERATIVO con estos gastos", "=B15+SUM(B18:B20)", font=BOLD, fill=TOTAL)
linea(22, "… y además facturando a El abuelo Pedro (entregado el 7/09)", f"=B21+{ING_PEND}", font=BOLD,
      nota="Albarán A-2026-0011: 124,20 € sin IVA, entregado y sin factura")

ws["A24"] = "4 · ¿CUÁNTO HAY QUE VENDER AL MES PARA CUBRIR GASTOS?"; ws["A24"].font = SEC
linea(25, "Material consumido sobre ventas", f"=IFERROR({M_CONS}/B5,0)", fmt=PCT, font=BASE)
linea(26, "Ventas de equilibrio — con los gastos registrados", "=IFERROR(-B6/(1-B25),0)",
      nota="Gastos de estructura ÷ (1 − % de material)")
linea(27, "Ventas de equilibrio — si se confirman los gastos que faltan", "=IFERROR(-(B6+SUM(B18:B20))/(1-B25),0)")
linea(28, "Ventas de septiembre", "=B5")

ws["A30"] = "5 · OTRAS FORMAS DE CONTARLO (informativo)"; ws["A30"].font = SEC
linea(31, "Facturado con fecha de septiembre (por fecha de factura, sin TPV)", f"={FACT_SEP}",
      nota="Incluye la factura de Tequendama del 29/09 (entrega en octubre) y no incluye la F-0014 de Frutas Félix (1/10)")
linea(32, "Total gastos registrados imputados a septiembre", f"={G_TOT}")
ws.freeze_panes = "A4"

# ============================================================== INCIDENCIAS
wn = hoja("Incidencias ERP", "Incidencias del ERP encontradas al hacer el cierre",
          "No se ha modificado nada en el ERP: solo se ha leído. Conviene revisarlas con la gestoría.",
          [5, 34, 80, 50])
cabecera(wn, 4, ["#", "Dónde", "Qué pasa", "Qué hacer"])
INC = [
    ("Contabilidad (asientos)",
     "El diario conserva asientos de 7 facturas que ya no existen (F-0004 a F-0008, F-0012 y F-0013). "
     "La F-0010 aparece dos veces: una de Tequendama (26,50 €) y otra de La Huerta por 788,10 € (la factura real es de 639,70 €). "
     "El alquiler de septiembre está contabilizado dos veces (GAS-144 y GAS-145).",
     "Regenerar o depurar los asientos. Hoy la contabilidad del ERP infla las ventas y los gastos de septiembre."),
    ("Numeración de facturas",
     "Faltan los números F-0004 a F-0008, F-0012 y F-0013 porque se borraron.",
     "La numeración debe ser correlativa: una factura emitida se anula con una rectificativa, no se borra. Consultar a la gestoría."),
    ("Cobros", "Hay un cobro de 87,36 € (14/09) asignado a la F-0005, que ya no existe. Frutas Félix pagó además la F-0009 (77,22 €) el 21/09.",
     "Comprobar en el banco si Frutas Félix pagó dos veces o si el cobro está mal asignado."),
    ("Alquiler y luz (IVA e IRPF)",
     "El ERP contabiliza 535,50 € como 442,56 € + 21 % IVA. La factura real es de 525 € + 110,25 € IVA − 99,75 € de retención IRPF (y la luz repercutida igual).",
     "Contabilizar base, IVA y retención por separado y presentar el modelo 115 trimestral."),
    ("El abuelo Pedro", "Albarán A-2026-0011 (7/09, 124,20 € sin IVA) entregado y sin factura.", "Emitir la factura (o marcarlo como muestra si lo era)."),
    ("Tequendama", "Pedido 30 cancelado, pero su albarán A-2026-0019 figura como «entregado». La F-0011 (29/09) es de un pedido que se entrega el 6/10.",
     "Anular el albarán. Revisar si la factura del evento debía emitirse antes de la entrega."),
    ("La Huerta", "Los albaranes A-0016 y A-0018 van sin el 20 % de descuento que llevan los demás; el pedido 28 decía 114,00 € y el albarán 138,60 €. La factura ya está cobrada.",
     "Confirmar el precio pactado con el cliente."),
    ("Albahaca Ecotienda", "La F-2026-0003 tiene fecha 21/08, pero el pedido y la entrega son del 3/09.", "Revisar la fecha de la factura."),
    ("Gastos duplicados", "Los gastos 156 y 159 son la misma factura de Anthropic (18 €, 27/09).", "Borrar uno."),
    ("Lotes de producción",
     "Hay 12 lotes (81 bandejas) con fecha de siembra 17-28/08, cuando en agosto no se sembró. Y varios lotes de septiembre siguen como «sembrado» pasado su ciclo (p. ej. el lote 71, cilantro del 1/09).",
     "Corregir las fechas y cerrar los lotes cosechados: el coste de producción por lote depende de ello."),
    ("Gastos que faltan", "No hay gestoría desde junio, falta la cuota de septiembre de Finetwork (solo hay un recargo por impago) y la cuota de autónomos de septiembre figura en 2,95 € (antes 88,56 €).",
     "Subir las facturas que falten para que el cierre sea completo."),
]
for k, (donde, que, hacer) in enumerate(INC):
    r = 5 + k
    fila(wn, r, [k + 1, donde, que, hacer], [None] * 4)
    for col in "BCD":
        wn[f"{col}{r}"].alignment = Alignment(wrap_text=True, vertical="top")

for w in wb.worksheets:
    for row in w.iter_rows():
        for c in row:
            if c.font and c.font.name != F:
                c.font = Font(name=F, size=c.font.size, bold=c.font.bold, italic=c.font.italic, color=c.font.color)
wb.save(OUT)
print("escrito", OUT)
