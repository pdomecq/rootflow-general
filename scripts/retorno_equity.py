#!/usr/bin/env python3
"""Recalcula el retorno del inversor si entra en CAPITAL en vez de en
prestamo participativo. Parte de las cifras del Modelo V14 escenario Base.

El V14 calcula TIR 33% / MOIC 2,39x / payback 33 meses sobre el tramo
PARTICIPATIVO: el inversor cobraba intereses desde el ano 1. Con equity y
dividendos bloqueados hasta amortizar ENISA, el inversor NO cobra nada hasta
la salida, asi que el retorno depende solo del valor de salida y del momento.
"""
INVERSION = 100_000

# --- Modelo V14, escenario Base (extraido del xlsx) -------------------------
EBITDA = {1:-51_620, 2:191_397, 3:350_220, 4:468_143, 5:460_201, 6:430_665, 7:400_955}
CAJA   = {1:30_000, 2:102_587, 3:318_816, 4:453_076, 5:638_336, 6:760_983, 7:871_428}
# "Caja + fondo Hito 4 en la empresa (ano 7)" del propio V14
CAJA_MAS_FONDO_A7 = 1_362_674
# El V14 valora el 30% de un socio en 828.362 EUR a su multiplo de salida
VALOR_30_PCT_V14 = 828_362
VALOR_SALIDA_V14 = VALOR_30_PCT_V14 / 0.30      # ~2,76 M EUR de valor total

def moic_necesario(tir, anos):
    return (1 + tir) ** anos

def tir_de(moic, anos):
    return moic ** (1/anos) - 1

def valor_salida(ano, multiplo, incluir_caja=True):
    ev = EBITDA[ano] * multiplo
    caja = CAJA_MAS_FONDO_A7 if ano == 7 else CAJA[ano]
    return ev + (caja if incluir_caja else 0)

print("="*78)
print("RETORNO DEL INVERSOR CON ENTRADA EN CAPITAL — 100.000 EUR, sin dividendos")
print("="*78)

print("\n1. VALOR DE SALIDA SEGUN HIPOTESIS (EBITDA x multiplo + caja)\n")
print(f"{'Salida':<10}{'EBITDA':>12}{'5x':>14}{'6x':>14}{'7x':>14}{'8x':>14}")
for ano in (5,6,7):
    fila=f"Ano {ano:<6}{EBITDA[ano]:>12,.0f}"
    for m in (5,6,7,8): fila+=f"{valor_salida(ano,m):>14,.0f}"
    print(fila.replace(",","."))
print(f"\nReferencia del propio V14 (valor del 30% de un socio x3): {VALOR_SALIDA_V14:>12,.0f} EUR".replace(",","."))
print("  -> El V14 es MAS CONSERVADOR que un 5x sobre EBITDA mas caja. Hay que")
print("     reconciliar las dos cifras antes de ensenar ninguna a un inversor.")

print("\n\n2. QUE PORCENTAJE HAY QUE DAR PARA CADA TIR OBJETIVO")
print("   (salida en ano 7, sin dividendos intermedios)\n")
print(f"{'TIR objetivo':<14}{'MOIC necesario':>16}{'% con valor V14':>18}{'% con 6x+caja':>16}")
v6 = valor_salida(7,6)
for tir in (0.12,0.15,0.20,0.25,0.30,0.33):
    m = moic_necesario(tir,7)
    p_v14 = INVERSION*m/VALOR_SALIDA_V14*100
    p_6x  = INVERSION*m/v6*100
    print(f"{tir*100:>5.0f} %{'':<8}{m:>14.2f}x{p_v14:>17.1f}%{p_6x:>15.1f}%")

print("\n\n3. EL EFECTO DEL PLAZO — misma participacion, distinta TIR")
print("   Ejemplo: inversor con el 10% del capital\n")
print(f"{'Salida en':<12}{'Valor total (6x+caja)':>24}{'Vale su 10%':>16}{'MOIC':>8}{'TIR':>9}")
for ano in (4,5,6,7):
    v = valor_salida(ano,6); vale=v*0.10; m=vale/INVERSION
    print(f"Ano {ano:<8}{v:>24,.0f}{vale:>16,.0f}{m:>7.2f}x{tir_de(m,ano)*100:>8.1f}%".replace(",","."))

print("\n\n4. LA CONCLUSION QUE IMPORTA\n")
m_old = 2.39
p_necesario = INVERSION*m_old/VALOR_SALIDA_V14*100
print(f"   El participativo prometia MOIC {m_old}x con payback a 33 meses.")
print(f"   Replicar solo el MOIC {m_old}x con equity exige darle el {p_necesario:.1f}% del capital...")
print(f"   ...pero cobrado en el ano 7 en vez de en el mes 33, la TIR baja a {tir_de(m_old,7)*100:.1f}%.")
print(f"   Y replicar la TIR del 33% a 7 anos exige un MOIC de {moic_necesario(0.33,7):.2f}x,")
print(f"   es decir el {INVERSION*moic_necesario(0.33,7)/VALOR_SALIDA_V14*100:.1f}% del capital. Incompatible con dilucion minima.")
print("\n   => Con equity puro NO puedes prometer 33% de TIR sin regalar la empresa.")
print("      La palanca no es el porcentaje: es ADELANTAR LA LIQUIDEZ.")
