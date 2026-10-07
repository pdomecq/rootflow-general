#!/usr/bin/env python3
"""Excel para la asesoría de ENISA: proveedores, clientes y facturación real, y pipeline.

Datos del ERP de Rootflow (Supabase) a 07/10/2026 y del modelo financiero V17 (hoja Pipeline).
Las notas comerciales del CRM se resumen en texto neutro: sin nombres de personas, teléfonos ni correos.
Uso: python3 scripts/enisa_eric.py finanzas/Rootflow_ENISA_Proveedores_Clientes_Pipeline.xlsx
"""
import sys
from datetime import date as D
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.worksheet.table import Table, TableStyleInfo

OUT = sys.argv[1] if len(sys.argv) > 1 else "finanzas/Rootflow_ENISA_Proveedores_Clientes_Pipeline.xlsx"
CORTE = "07/10/2026"
A = "Arial"
BASE = Font(name=A, size=10)
BOLD = Font(name=A, size=10, bold=True)
BLUE = Font(name=A, size=10, color="0000FF")
GREEN = Font(name=A, size=10, color="008000")
GREEN_B = Font(name=A, size=10, color="008000", bold=True)
WHITE = Font(name=A, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=A, size=14, bold=True, color="1D4F37")
SUB = Font(name=A, size=9, italic=True, color="666666")
SEC = Font(name=A, size=11, bold=True, color="1D4F37")
HEAD = PatternFill("solid", fgColor="1D4F37")
SECF = PatternFill("solid", fgColor="E6F2EA")
TOT = PatternFill("solid", fgColor="E6F2EA")
LINE = Border(top=Side(style="thin", color="1D4F37"))
EUR = '#,##0.00" €";(#,##0.00" €");"-"'
EUR0 = '#,##0" €";(#,##0" €");"-"'
PCT = '0%;(0%);"-"'
DATE = "dd/mm/yyyy"
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()


def hoja(ws, titulo, sub, anchos):
    ws["A1"] = titulo; ws["A1"].font = TITLE
    ws["A2"] = sub; ws["A2"].font = SUB
    for i, w in enumerate(anchos, 1):
        ws.column_dimensions[CL(i)].width = w
    ws.sheet_view.showGridLines = False


def cabecera(ws, r, textos):
    for i, t in enumerate(textos, 1):
        c = ws.cell(row=r, column=i, value=t)
        c.font = WHITE; c.fill = HEAD; c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[r].height = 32


def celda(ws, r, col, v, fmt=None, font=BASE, wrap=False):
    c = ws.cell(row=r, column=col, value=v)
    if fmt: c.number_format = fmt
    c.font = font
    c.alignment = WRAP if wrap else Alignment(vertical="top")
    return c


# ============================================================ PROVEEDORES
# Compras registradas en el ERP (tabla gastos), importe pagado con IVA: id -> (fecha, importe)
G = {
    92: (D(2026, 5, 20), 147.77), 116: (D(2026, 6, 17), 147.77), 117: (D(2026, 6, 25), 343.17), 152: (D(2026, 10, 1), 354.52),
    87: (D(2026, 5, 19), 72.00), 120: (D(2026, 6, 29), 72.00), 151: (D(2026, 9, 22), 74.00),
    83: (D(2026, 5, 15), 5.99), 113: (D(2026, 6, 17), 117.13), 133: (D(2026, 8, 19), 253.00),
    44: (D(2026, 4, 10), 142.46),
    69: (D(2026, 5, 4), 7.41), 77: (D(2026, 5, 7), 4.26), 78: (D(2026, 5, 7), 10.50), 112: (D(2026, 6, 14), 32.10),
    94: (D(2026, 5, 20), 28.85),
    100: (D(2026, 5, 26), 203.44), 108: (D(2026, 6, 1), 78.10),
    41: (D(2026, 4, 9), 60.38), 42: (D(2026, 4, 9), 27.79), 60: (D(2026, 4, 25), 113.19), 79: (D(2026, 5, 7), 127.36),
    99: (D(2026, 5, 22), 116.00),
    50: (D(2026, 3, 14), 21.99), 17: (D(2026, 3, 15), 34.86), 33: (D(2026, 4, 9), 103.88), 54: (D(2026, 4, 24), 213.95),
    55: (D(2026, 4, 24), 8.68), 56: (D(2026, 4, 24), 82.74), 57: (D(2026, 4, 24), 37.39), 88: (D(2026, 5, 19), 274.00),
    89: (D(2026, 5, 19), 12.59), 95: (D(2026, 5, 21), 10.84), 97: (D(2026, 5, 21), 219.84), 102: (D(2026, 5, 28), 34.65),
    103: (D(2026, 5, 28), 12.95), 140: (D(2026, 9, 3), 93.29), 141: (D(2026, 9, 14), 64.99),
    110: (D(2026, 6, 9), 38.43), 31: (D(2026, 4, 9), 144.95), 61: (D(2026, 4, 25), 99.95),
    27: (D(2026, 3, 6), 535.50), 62: (D(2026, 5, 4), 547.61), 106: (D(2026, 5, 28), 557.05), 123: (D(2026, 6, 26), 535.00),
    124: (D(2026, 6, 26), 101.10), 125: (D(2026, 6, 30), 66.91), 131: (D(2026, 7, 15), 29.00), 142: (D(2026, 7, 28), 535.50),
    143: (D(2026, 7, 28), 27.43), 144: (D(2026, 8, 31), 535.50), 153: (D(2026, 9, 30), 535.50), 154: (D(2026, 9, 30), 30.71),
    155: (D(2026, 9, 30), 137.51),
    16: (D(2026, 5, 5), 635.25),
    70: (D(2026, 4, 30), 163.35), 107: (D(2026, 5, 7), 163.35), 126: (D(2026, 6, 5), 119.79),
    72: (D(2026, 3, 19), 181.50), 73: (D(2026, 3, 19), 504.40), 74: (D(2026, 3, 19), 98.75), 75: (D(2026, 3, 19), 60.83),
    76: (D(2026, 3, 19), 65.34), 104: (D(2026, 5, 27), 15.98), 105: (D(2026, 5, 13), 34.18),
    24: (D(2026, 4, 7), 18), 26: (D(2026, 4, 8), 5), 28: (D(2026, 4, 9), 5), 45: (D(2026, 4, 14), 5), 46: (D(2026, 4, 14), 5),
    63: (D(2026, 4, 21), 5), 64: (D(2026, 4, 27), 18), 65: (D(2026, 4, 30), 5), 66: (D(2026, 5, 4), 5), 67: (D(2026, 5, 5), 5),
    68: (D(2026, 5, 5), 5), 71: (D(2026, 5, 6), 5), 85: (D(2026, 5, 13), 5), 98: (D(2026, 5, 21), 5), 101: (D(2026, 5, 27), 18),
    111: (D(2026, 6, 10), 5), 114: (D(2026, 6, 22), 5), 121: (D(2026, 6, 26), 5), 122: (D(2026, 6, 29), 18), 128: (D(2026, 7, 6), 5),
    129: (D(2026, 7, 10), 5), 130: (D(2026, 7, 10), 5), 132: (D(2026, 7, 20), 5), 157: (D(2026, 8, 27), 18),
    158: (D(2026, 9, 16), 20), 156: (D(2026, 9, 27), 18),
    147: (D(2026, 5, 1), 15.72), 148: (D(2026, 6, 1), 27.76), 149: (D(2026, 7, 1), 25.99), 150: (D(2026, 8, 1), 25.99),
    146: (D(2026, 9, 21), 5.00),
    18: (D(2025, 12, 30), 1.21), 19: (D(2026, 1, 30), 1.21), 20: (D(2026, 3, 1), 1.21),
    25: (D(2026, 4, 7), 104.96), 119: (D(2026, 6, 27), 104.83), 32: (D(2026, 4, 9), 18.93),
    160: (D(2026, 10, 4), 221.00),
    49: (D(2026, 3, 27), 16.30), 48: (D(2026, 3, 30), 15.60), 34: (D(2026, 4, 9), 30.48), 35: (D(2026, 4, 9), 42.48),
    36: (D(2026, 4, 9), 20.75), 37: (D(2026, 4, 9), 16.06), 38: (D(2026, 4, 9), 20.60), 39: (D(2026, 4, 9), 10.00),
    40: (D(2026, 4, 9), 16.58), 43: (D(2026, 4, 9), 20.79), 47: (D(2026, 4, 19), 40.00), 51: (D(2026, 4, 20), 14.89),
    52: (D(2026, 4, 20), 4.40), 53: (D(2026, 4, 21), 4.90), 59: (D(2026, 4, 25), 14.99), 81: (D(2026, 5, 13), 126.28),
    82: (D(2026, 5, 14), 124.48), 84: (D(2026, 5, 14), 25.22), 86: (D(2026, 5, 18), 25.00), 91: (D(2026, 5, 20), 50.00),
    93: (D(2026, 5, 20), 40.31), 109: (D(2026, 6, 1), 29.60),
}
# (categoría, proveedor, razón social / ubicación, qué suministra, relación, ids de compra)
PROV = [
    ("Semillas", "MP Seeds", "HYDRO Mateusz Przybiński · Łódź (Polonia)",
     "Semilla para microbrotes: cilantro, albahaca, rábano daikon y rojo, amaranto, brócoli, rúcula", "Recurrente · principal",
     [92, 116, 117, 152]),
    ("Sustrato", "Organic Growshop", "Organik Green Zone, S.L. · Madrid",
     "Sustrato de fibra de coco (Atami, sacos de 100 L)", "Recurrente · principal", [87, 120, 151]),
    ("Envases y etiquetado", "Envases del Mediterráneo", "San Ginés (Murcia)",
     "Tarrinas de PET con bisagra para los formatos de 30 g", "Recurrente · principal", [83, 113, 133]),
    ("Envases y etiquetado", "Envanature", "Tecnopacking, S.L.U. · Onda (Castellón)", "Tarrinas de 150 y 250 cc", "Puntual", [44]),
    ("Envases y etiquetado", "Amazon Business", "—", "Etiquetas térmicas, pegatinas y consumibles de impresora", "Recurrente", [69, 77, 78, 112]),
    ("Envases y etiquetado", "360imprimir", "—", "Etiquetas frontales impresas", "Puntual", [94]),
    ("Sistema de cultivo", "Green Ice", "Green Ice, S.L. · Toledo", "Luminarias LED T5 de cultivo", "Puntual (equipamiento)", [100]),
    ("Sistema de cultivo", "LEDBOX", "Salamanca", "Conectores y material de iluminación LED", "Puntual (equipamiento)", [108]),
    ("Sistema de cultivo", "AliExpress", "—", "Luces LED y conectores", "Puntual (equipamiento)", [41, 42, 60, 79]),
    ("Sistema de cultivo", "Plases Grow Shop", "Plases Internacional 2020, S.L.U. · Yuncos (Toledo)",
     "Mesas de cultivo de 100 × 110 cm (bandejas de inundación)", "Puntual (equipamiento)", [99]),
    ("Sistema de cultivo", "Leroy Merlin", "—", "Estanterías, tubería, bomba y material de riego, sensores de temperatura y humedad",
     "Recurrente (equipamiento)", [50, 17, 33, 54, 55, 56, 57, 88, 89, 95, 97, 102, 103, 140, 141]),
    ("Sistema de cultivo", "FYMALSA", "Las Rozas (Madrid)", "Material eléctrico y de riego", "Puntual (equipamiento)", [110]),
    ("Sistema de cultivo", "IKEA", "—", "Mobiliario de trabajo", "Puntual (equipamiento)", [31]),
    ("Sistema de cultivo", "Cash Converters", "—", "Impresora de etiquetas (segunda mano)", "Puntual (equipamiento)", [61]),
    ("Sistema de gestión", "ERP propio", "Desarrollo interno",
     "Pedidos, producción y trazabilidad por lote, albaranes y facturación (React + Supabase)", "Propio · sin coste de licencia", []),
    ("Sistema de gestión", "Anthropic (Claude)", "—", "Herramienta de IA para el desarrollo del ERP propio", "Mensual",
     [24, 26, 28, 45, 46, 63, 64, 65, 66, 67, 68, 71, 85, 98, 101, 111, 114, 121, 122, 128, 129, 130, 132, 157, 158, 156]),
    ("Local", "Bellbro Renting and Development", "Bellbro Renting and Development, S.L. · Las Rozas (Madrid)",
     "Arrendador del local de producción (alquiler, luz y agua repercutidas, tasa de basura)", "Mensual",
     [27, 62, 106, 123, 124, 125, 131, 142, 143, 144, 153, 154, 155]),
    ("Local", "Inmobiliaria MBlanco", "—", "Honorarios de intermediación del alquiler", "Puntual", [16]),
    ("Servicios profesionales", "Ayuda-T Soluciones Profesionales", "Ayuda-T Soluciones Profesionales, S.L.", "Asesoría y gestoría",
     "Mensual", [70, 107, 126]),
    ("Servicios profesionales", "Ortega y del Río Notarios", "Ortega y del Río Notarios, C.B.", "Notaría (constitución de la sociedad)",
     "Puntual", [72, 73, 74, 75, 76]),
    ("Servicios profesionales", "FNMT-RCM", "—", "Certificado digital de la sociedad", "Puntual", [104]),
    ("Servicios profesionales", "Registro de la Propiedad", "—", "Certificado registral", "Puntual", [105]),
    ("Comunicaciones", "Finetwork", "WEWI Mobile, S.L.", "Fibra y telefonía móvil", "Mensual", [147, 148, 149, 150, 146]),
    ("Comunicaciones", "IONOS", "—", "Dominio y web", "Mensual", [18, 19, 20]),
    ("Marketing", "Vistaprint", "Vistaprint B.V.", "Tarjetas de visita", "Puntual", [25]),
    ("Otros", "Fronda", "Fronda Centros de Jardinería, S.L. · Majadahonda (Madrid)",
     "Brotes de cilantro (compra puntual de producto, junio 2026)", "Puntual", [119]),
    ("Otros", "DIA", "—", "Productos de limpieza", "Puntual", [32]),
    ("Otros", "Reparto propio", "—", "Combustible del reparto con vehículo propio", "Recurrente", [160]),
    ("Otros", "Compras menores sin proveedor identificado", "—",
     "Material de segunda mano (cubetas, nevera, cortadora), ferretería, utensilios y teléfono de empresa", "Puntual",
     [49, 48, 34, 35, 36, 37, 38, 39, 40, 43, 47, 51, 52, 53, 59, 81, 82, 84, 86, 91, 93, 109]),
]
assert len({i for p in PROV for i in p[5]}) == sum(len(p[5]) for p in PROV), "compra asignada a dos proveedores"

wp = wb.active; wp.title = "Proveedores"
hoja(wp, "Rootflow Hydroponics — Proveedores y servicios",
     f"Datos del ERP a {CORTE}. Importe acumulado = suma de las compras registradas, IVA incluido. "
     "No incluye impuestos ni cuotas de la Seguridad Social.",
     [24, 32, 40, 58, 24, 10, 16, 13, 13])
cabecera(wp, 4, ["Categoría", "Proveedor", "Razón social / ubicación", "Qué suministra", "Relación", "Nº de compras",
                 "Importe acumulado (IVA incl.)", "Primera compra", "Última compra"])
r = 5
for cat, prov, rs, que, rel, ids in PROV:
    vals = [G[i] for i in ids]
    celda(wp, r, 1, cat)
    celda(wp, r, 2, prov, font=BOLD)
    celda(wp, r, 3, rs, wrap=True)
    celda(wp, r, 4, que, wrap=True)
    celda(wp, r, 5, rel, wrap=True)
    celda(wp, r, 6, len(ids) if ids else None, "0", BLUE)
    celda(wp, r, 7, round(sum(v for _, v in vals), 2) if ids else None, EUR, BLUE)
    celda(wp, r, 8, min(f for f, _ in vals) if ids else None, DATE, BLUE)
    celda(wp, r, 9, max(f for f, _ in vals) if ids else None, DATE, BLUE)
    r += 1
p1, p2 = 5, r - 1
celda(wp, r + 1, 2, "TOTAL COMPRAS REGISTRADAS", font=BOLD)
for col, f, fmt in ((6, f"=SUM(F{p1}:F{p2})", "0"), (7, f"=SUM(G{p1}:G{p2})", EUR)):
    c = celda(wp, r + 1, col, f, fmt, BOLD); c.fill = TOT; c.border = LINE
PROV_TOTAL = f"Proveedores!$G${r+1}"
celda(wp, r + 3, 1, "Proveedores principales de la producción: MP Seeds (semilla), Organic Growshop (sustrato) y "
      "Envases del Mediterráneo (tarrinas). El sistema de cultivo (estanterías, mesas de inundación, iluminación LED y riego) "
      "se ha montado con compras de equipamiento; la gestión va sobre un ERP propio.", font=SUB)
wp.freeze_panes = "C5"
wp.auto_filter.ref = f"A4:I{p2}"

# ============================================================ VENTAS (detalle)
wv = wb.create_sheet("Ventas detalle")
hoja(wv, "Rootflow Hydroponics — Facturación real (detalle)",
     f"Facturas emitidas, tickets de venta directa y entregas pendientes de facturar, según el ERP a {CORTE}. "
     "Mes de entrega = mes en que se entregó el producto.",
     [16, 13, 32, 26, 12, 26, 13, 12, 13, 14, 13])
cabecera(wv, 4, ["Documento", "Fecha", "Cliente", "Canal", "Mes de entrega", "Tipo", "Base imponible", "IVA",
                 "Total", "Estado de cobro", "Fecha de cobro"])
HUERTA, FELIX, ALBA = "La Huerta Hermanos Nieto, S.L.", "Frutas Félix Vázquez, S.L.", "Albahaca Ecotienda"
TEQ, PAD, ABU, TPV = "Tequendama", "Café El Padrino, S.L.", "El Abuelo Pedro", "Venta directa (particulares)"
CANAL = {HUERTA: "Mayorista / frutería (Mercamadrid)", FELIX: "Frutería", ALBA: "Tienda ecológica",
         TEQ: "Restaurante", PAD: "Restaurante / cafetería", ABU: "Mayorista (Mercamadrid)", TPV: "Venta directa"}
V = [
    ("F-2026-0001", D(2026, 6, 30), HUERTA, "2026-06", "Factura", 619.60, 24.78, "Cobrada", D(2026, 8, 3)),
    ("F-2026-0002", D(2026, 7, 21), HUERTA, "2026-07", "Factura", 350.40, 14.02, "Cobrada", D(2026, 10, 5)),
    ("F-2026-0003", D(2026, 8, 21), ALBA, "2026-09", "Factura", 48.45, 1.94, "Cobrada", D(2026, 9, 21)),
    ("F-2026-0009", D(2026, 9, 14), FELIX, "2026-09", "Factura", 74.25, 2.97, "Cobrada", D(2026, 9, 21)),
    ("F-2026-0010", D(2026, 9, 28), HUERTA, "2026-09", "Factura", 639.70, 25.59, "Cobrada", D(2026, 10, 2)),
    ("F-2026-0011", D(2026, 9, 29), TEQ, "2026-10", "Factura", 31.40, 1.26, "Pendiente", None),
    ("F-2026-0014", D(2026, 10, 1), FELIX, "2026-09", "Factura", 115.25, 4.61, "Cobrada", D(2026, 10, 7)),
    ("F-2026-0015", D(2026, 10, 2), PAD, "2026-10", "Factura", 10.10, 0.40, "Cobrada", D(2026, 10, 6)),
    ("Ticket TPV", D(2026, 5, 24), TPV, "2026-05", "Ticket", 4.81, 0.19, "Cobrada", D(2026, 5, 24)),
    ("Ticket TPV", D(2026, 9, 15), TPV, "2026-09", "Ticket", 4.81, 0.19, "Cobrada", D(2026, 9, 15)),
    ("Ticket TPV", D(2026, 9, 16), TPV, "2026-09", "Ticket", 8.65, 0.35, "Cobrada", D(2026, 9, 16)),
    ("Ticket TPV", D(2026, 9, 24), TPV, "2026-09", "Ticket", 8.65, 0.35, "Cobrada", D(2026, 9, 24)),
    ("Ticket TPV", D(2026, 10, 1), TPV, "2026-10", "Ticket", 8.65, 0.35, "Cobrada", D(2026, 10, 1)),
    ("A-2026-0011", D(2026, 9, 7), ABU, "2026-09", "Entregado, pendiente de facturar", 124.20, 4.97, "—", None),
    ("A-2026-0023", D(2026, 10, 5), HUERTA, "2026-10", "Entregado, pendiente de facturar", 155.00, 6.20, "—", None),
]
v0 = 5
for k, (doc, fe, cli, mes, tipo, base, iva, est, fc) in enumerate(V):
    r = v0 + k
    for col, val, fmt, font in ((1, doc, None, BASE), (2, fe, DATE, BLUE), (3, cli, None, BASE), (4, CANAL[cli], None, BASE),
                                (5, mes, None, BLUE), (6, tipo, None, BASE), (7, base, EUR, BLUE), (8, iva, EUR, BLUE),
                                (9, f"=G{r}+H{r}", EUR, BASE), (10, est, None, BLUE), (11, fc, DATE, BLUE)):
        celda(wv, r, col, val, fmt, font)
vN = v0 + len(V) - 1
rt = vN + 2
celda(wv, rt, 3, "TOTAL FACTURADO Y COBRADO EN CAJA (facturas + tickets)", font=BOLD)
for col in "GHI":
    c = wv[f"{col}{rt}"]
    c.value = f'=SUMIFS({col}{v0}:{col}{vN},$F${v0}:$F${vN},"Factura")+SUMIFS({col}{v0}:{col}{vN},$F${v0}:$F${vN},"Ticket")'
    c.number_format = EUR; c.font = BOLD; c.fill = TOT; c.border = LINE
celda(wv, rt + 1, 3, "Entregado pendiente de facturar", font=BASE)
for col in "GHI":
    c = wv[f"{col}{rt+1}"]
    c.value = f'=SUMIFS({col}{v0}:{col}{vN},$F${v0}:$F${vN},"Entregado, pendiente de facturar")'; c.number_format = EUR
celda(wv, rt + 2, 3, "Pendiente de cobro (facturas emitidas)", font=BASE)
c = wv[f"I{rt+2}"]; c.value = f'=SUMIFS(I{v0}:I{vN},$J${v0}:$J${vN},"Pendiente")'; c.number_format = EUR
VR = f"'Ventas detalle'!$G${v0}:$G${vN}"           # base
VT = f"'Ventas detalle'!$I${v0}:$I${vN}"           # total
VC = f"'Ventas detalle'!$C${v0}:$C${vN}"           # cliente
VF = f"'Ventas detalle'!$F${v0}:$F${vN}"           # tipo
VM = f"'Ventas detalle'!$E${v0}:$E${vN}"           # mes
VE = f"'Ventas detalle'!$J${v0}:$J${vN}"           # estado de cobro
celda(wv, rt + 4, 1, "Agosto sin ventas: parada de producción en verano.", font=SUB)
wv.freeze_panes = "A5"
wv.auto_filter.ref = f"A4:K{vN}"

# ============================================================ CLIENTES
wc = wb.create_sheet("Clientes", 1)
hoja(wc, "Rootflow Hydroponics — Clientes y facturación real",
     f"Datos del ERP a {CORTE}. Base imponible sin IVA; el detalle de cada factura está en la hoja «Ventas detalle».",
     [32, 30, 12, 13, 11, 15, 15, 14, 15, 15, 46])
cabecera(wc, 4, ["Cliente", "Canal", "Alta como cliente", "Primera entrega", "Nº de entregas", "Facturado (base)",
                 "Facturado (IVA incl.)", "Cobrado", "Pendiente de cobro", "Entregado pendiente de facturar", "Observaciones"])
CLI = [
    (HUERTA, D(2026, 6, 1), D(2026, 6, 14), 14, "Pedido semanal: ~60 tarrinas de 30 g (cilantro y albahaca). Facturación mensual."),
    (FELIX, D(2026, 9, 5), D(2026, 9, 5), 4, "Pedido semanal desde septiembre, surtido de variedades."),
    (ALBA, D(2026, 6, 1), D(2026, 9, 3), 1, "Surtido de 8 variedades en formato de 15 g."),
    (ABU, D(2026, 9, 5), D(2026, 9, 7), 1, "Puesto en Mercamadrid. Primera entrega pendiente de facturar."),
    (TEQ, D(2026, 9, 21), D(2026, 10, 6), 1, "Primer pedido (evento)."),
    (PAD, D(2026, 9, 7), D(2026, 10, 1), 1, "Primer pedido."),
    (TPV, None, D(2026, 5, 24), 5, "Ventas con tarjeta en el local (5 tickets)."),
]
c0 = 5
for k, (cli, alta, prim, n, obs) in enumerate(CLI):
    r = c0 + k
    celda(wc, r, 1, cli, font=BOLD); celda(wc, r, 2, CANAL[cli])
    celda(wc, r, 3, alta, DATE, BLUE); celda(wc, r, 4, prim, DATE, BLUE); celda(wc, r, 5, n, "0", BLUE)
    fac = lambda rng: (f'=SUMIFS({rng},{VC},$A{r},{VF},"Factura")+SUMIFS({rng},{VC},$A{r},{VF},"Ticket")')
    celda(wc, r, 6, fac(VR), EUR, GREEN); celda(wc, r, 7, fac(VT), EUR, GREEN)
    celda(wc, r, 8, f'=SUMIFS({VT},{VC},$A{r},{VE},"Cobrada")', EUR, GREEN)
    celda(wc, r, 9, f'=SUMIFS({VT},{VC},$A{r},{VE},"Pendiente")', EUR, GREEN)
    celda(wc, r, 10, f'=SUMIFS({VR},{VC},$A{r},{VF},"Entregado, pendiente de facturar")', EUR, GREEN)
    celda(wc, r, 11, obs, wrap=True)
cN = c0 + len(CLI) - 1
ct = cN + 1
celda(wc, ct, 1, "TOTAL", font=BOLD)
for col in "EFGHIJ":
    c = wc[f"{col}{ct}"]; c.value = f"=SUM({col}{c0}:{col}{cN})"
    c.number_format = "0" if col == "E" else EUR; c.font = BOLD; c.fill = TOT; c.border = LINE
CLI_T = {k: f"Clientes!${k}${ct}" for k in "EFGHIJ"}

r = ct + 3
celda(wc, r, 1, "CLIENTES DADOS DE ALTA, AÚN SIN PEDIDOS", font=SEC)
cabecera(wc, r + 1, ["Cliente", "Canal", "Alta como cliente", "", "", "", "", "", "", "", "Situación"])
SIN = [("Frutas Eloy Ruano, S.L.", "Mayorista (Mercamadrid)", D(2026, 3, 29), "Cliente en el plan de distribución; sin pedidos todavía."),
       ("Tatin Catering", "Catering", D(2026, 9, 7), "Alta en septiembre; sin pedidos facturados todavía."),
       ("La Fresquera del Gourmet", "Tienda gourmet / restauración", D(2026, 9, 7), "Alta en septiembre; sin pedidos todavía."),
       ("Tucosechaonline", "Tienda online", D(2026, 10, 7), "Alta el 07/10/2026.")]
for k, (cli, can, alta, sit) in enumerate(SIN):
    rr = r + 2 + k
    celda(wc, rr, 1, cli, font=BOLD); celda(wc, rr, 2, can); celda(wc, rr, 3, alta, DATE, BLUE); celda(wc, rr, 11, sit, wrap=True)
wc.freeze_panes = "B5"

# ============================================================ PIPELINE RESTAURANTES (CRM del ERP)
wl = wb.create_sheet("Pipeline restaurantes")
hoja(wl, "Rootflow Hydroponics — Pipeline comercial: restaurantes, tiendas y distribuidores",
     f"Oportunidades abiertas en el CRM del ERP a {CORTE}. Etapa y última actividad según el CRM; la situación está resumida.",
     [5, 34, 30, 26, 15, 10, 15, 14, 62])
cabecera(wl, 4, ["#", "Cuenta", "Tipo", "Zona", "Etapa", "Prioridad", "Valor estimado (€)", "Última actividad", "Situación / próximo paso"])
R_, GR, TI, DI = "Restaurante", "Grupo / cadena de restauración", "Tienda / frutería", "Distribuidor / mayorista"
MAD, NO = "Madrid", "Madrid noroeste (Pozuelo, Majadahonda)"
LEADS = [
    ("Club Puerta de Hierro", R_, MAD, "Negociando", "Alta", 299, D(2026, 9, 17), "Visita con muestras al equipo de cocina; pendiente de su valoración."),
    ("Restaurante De María", R_, NO, "Negociando", "Alta", None, D(2026, 8, 31), "En negociación de condiciones."),
    ("Restaurante Jesús – AIME Ostras", R_, MAD, "Negociando", "Alta", None, D(2026, 9, 9), "Pendiente de cerrar fecha con el chef para llevar muestras."),
    ("Sushita", GR, MAD, "Interesado", "Alta", 1000, D(2026, 9, 4), "Interesados; falta definir el punto de entrega para sus locales."),
    ("Chef Fruit", DI + " (Mercamadrid)", MAD, "Interesado", "Alta", None, D(2026, 8, 31), "Están creando una sección de microbrotes; propuesta de acompañarles en el lanzamiento."),
    ("Fruotero", TI + " (abastece a chefs)", MAD, "Interesado", "Media", None, D(2026, 8, 31), "El producto gustó a los chefs a los que abastece; retomar tras la apertura de su nuevo local."),
    ("Tacos La 28", R_, MAD, "Interesado", "Media", None, D(2026, 9, 7), "Interesados; están abriendo un segundo local."),
    ("Grupo Sibuya", GR, MAD, "Interesado", "Media", None, D(2026, 9, 7), "Interesados; seguimiento en curso."),
    ("Faszina Selected", DI + " gourmet", "Barcelona (clientes en Madrid)", "Interesado", "Media", None, D(2026, 8, 24), "Interés en servir a sus clientes de Madrid; pendiente de nuevo contacto."),
    ("Frutas Iberika", DI + " (Mercamadrid)", MAD, "Acuerdo sin pedido", "Media", 50, D(2026, 9, 3), "Acuerdo para comprarnos lo que hoy venden (1-2 bandejas/semana de micromezcla, cilantro y guisante); sin pedido todavía."),
    ("Bidfood Iberia", DI + " de foodservice (Mercamadrid)", MAD, "Contactado", "Alta", 2000, D(2026, 7, 7), "Propuesta enviada por email; pendiente de respuesta."),
    ("GoldGourmet", DI + " gourmet (Mercamadrid)", MAD, "Contactado", "Alta", None, D(2026, 9, 4), "Interés en el modelo de venta en Mercamadrid; presentación a sus clientes el 14/09."),
    ("Doeat", R_, MAD, "Contactado", "Alta", 300, D(2026, 9, 3), "Presentado al equipo de cocina con valoración positiva; pendiente de pedido."),
    ("Honest Greens", GR, MAD, "Contactado", "Media", 500, D(2026, 7, 8), "Propuesta enviada al canal de proveedores; pendiente de respuesta."),
    ("Grupo Oter", GR, MAD, "Contactado", "Media", None, D(2026, 8, 25), "Primer contacto; seguimiento telefónico."),
    ("El Supertomate", R_, MAD, "Contactado", "Baja", None, D(2026, 8, 25), "Primer contacto realizado."),
    ("Georgánico", TI + " ecológica", MAD, "Contactado", "Baja", None, None, "Solo compra producto con certificación ecológica."),
    ("Frutería Silvestre", TI + " ecológica", MAD, "Contactado", "Baja", None, D(2026, 8, 24), "Consumo muy reducido y solo ecológico."),
    ("Faborit", GR + " (cafeterías)", MAD, "Nuevo", "Media", 400, D(2026, 8, 28), "Sin respuesta todavía; insistir."),
    ("Cristina Oria", "Gourmet / catering", MAD, "Nuevo", "Media", 100, D(2026, 8, 31), "Propuesta enviada por email."),
    ("Grupo La Fábrica", GR, MAD, "Nuevo", "Media", None, D(2026, 9, 4), "Prefieren el contacto por email; propuesta en curso."),
    ("Grupo Quispe", GR, MAD, "Nuevo", "Media", None, D(2026, 9, 7), "Contacto con la dirección a través de una referencia; pendiente de respuesta."),
    ("GLH", GR, MAD, "Nuevo", "Media", None, None, "Pendiente de primer contacto para presentar el producto al grupo."),
    ("Grupo Mentidero", GR, MAD, "Nuevo", "Media", None, None, "Pendiente de primer contacto."),
    ("La Lonja de Pozuelo", R_, NO, "Nuevo", "Baja", None, D(2026, 8, 31), "Pendiente de contacto con el responsable de compras."),
    ("Taberna de Elia", R_, NO, "Nuevo", "Baja", None, D(2026, 8, 28), "Responsable de compras identificado; llamar."),
    ("El Cielo de Urrechu", R_, MAD, "Nuevo", "Baja", None, D(2026, 8, 28), "Responsables de compras identificados; llamar."),
    ("Vespok", R_, MAD, "Nuevo", "Baja", None, D(2026, 9, 7), "Contacto identificado; llamar."),
    ("Bistec Boutique & Bar de Carnes", R_, NO, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
    ("Paschi Cocina Peruana", R_, NO, "Nuevo", "Baja", 50, None, "Pendiente de primer contacto."),
    ("SUMO", R_, MAD, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
    ("Nectarfruit", R_, MAD, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
    ("Frutas Maricarmen", TI, MAD, "Nuevo", "Baja", None, D(2026, 9, 4), "Contacto identificado; llamar."),
    ("Vanfresh", TI, MAD, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
    ("Hnos. Delgado", TI, MAD, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
    ("Gemüsering", TI, MAD, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
    ("Madosa", TI, MAD, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
    ("Frutas Logroño", TI, MAD, "Nuevo", "Baja", None, None, "Pendiente de primer contacto."),
]
l0 = 5
for k, (cta, tipo, zona, etapa, prio, val, ult, sit) in enumerate(LEADS):
    r = l0 + k
    for col, v, fmt, font, wrap in ((1, k + 1, "0", BASE, False), (2, cta, None, BOLD, False), (3, tipo, None, BASE, True),
                                    (4, zona, None, BASE, True), (5, etapa, None, BLUE, False), (6, prio, None, BLUE, False),
                                    (7, val, EUR0, BLUE, False), (8, ult, DATE, BLUE, False), (9, sit, None, BASE, True)):
        celda(wl, r, col, v, fmt, font, wrap)
lN = l0 + len(LEADS) - 1
wl.freeze_panes = "C5"
wl.auto_filter.ref = f"A4:I{lN}"
r = lN + 2
celda(wl, r, 2, "EMBUDO COMERCIAL (CRM del ERP)", font=SEC)
cabecera(wl, r + 1, ["", "Etapa", "Nº de cuentas", "Nota"])
EMB = [("Clientes ganados", 9, "Dados de alta como clientes; 6 ya han comprado (hoja Clientes)."),
       ("Negociando", None, ""), ("Interesado", None, ""), ("Acuerdo sin pedido", None, ""), ("Contactado", None, ""), ("Nuevo", None, ""),
       ("Descartados", 6, "Sin interés, sin consumo o requieren certificación ecológica.")]
e0 = r + 2
for k, (et, n, nota) in enumerate(EMB):
    rr = e0 + k
    celda(wl, rr, 2, et)
    celda(wl, rr, 3, n if n is not None else f'=COUNTIF($E${l0}:$E${lN},B{rr})', "0", BLUE if n is not None else BASE)
    celda(wl, rr, 4, nota, wrap=False)
eN = e0 + len(EMB) - 1
celda(wl, eN + 1, 2, "Total cuentas trabajadas", font=BOLD)
c = celda(wl, eN + 1, 3, f"=SUM(C{e0}:C{eN})", "0", BOLD); c.fill = TOT; c.border = LINE
celda(wl, eN + 3, 2, "Mercado objetivo de la línea de restaurantes: 585 restaurantes abiertos en 8 barrios de Madrid "
      "(Justicia, Recoletos, Castellana, Goya, Trafalgar, Almagro, Ríos Rosas y Lista). Fuente: Censo de locales y actividades, "
      "Ayuntamiento de Madrid (datos.madrid.es), epígrafe 561001. El plan prevé 123 restaurantes en cartera en el año 2.", font=SUB)
PIPE_ABIERTAS = f"COUNTA('Pipeline restaurantes'!$B${l0}:$B${lN})"

# ============================================================ PIPELINE DISTRIBUCIÓN (modelo V17)
wd = wb.create_sheet("Pipeline distribución")
hoja(wd, "Rootflow Hydroponics — Pipeline de distribución del plan financiero",
     "Cuentas identificadas en el modelo financiero V17 (hoja Pipeline), que alimentan la demanda de la línea de distribución, "
     f"con su situación real en el ERP a {CORTE}. Volúmenes a régimen, tras la rampa de cada cuenta.",
     [30, 18, 11, 12, 11, 13, 16, 16, 60])
cabecera(wd, 4, ["Cuenta", "Estado en el plan", "Probabilidad", "Mes de inicio (mes del plan)", "Rampa (meses)",
                 "Tarrinas al mes", "Ingreso potencial (€/mes)", "Ingreso ponderado (€/mes)", "Situación real (ERP)"])
MOD = [
    ("La Huerta Hermanos Nieto (La Huerta de Aranjuez)", "Activo", 0.95, 1, 3, 1305, 3262.50,
     "Cliente activo desde junio 2026: pedido semanal de ~60 tarrinas; 1.609,70 € facturados (base) a 07/10."),
    ("Sushita", "En conversación", 0.60, 2, 3, 130.5, 391.50, "Oportunidad abierta (interesados); sin pedidos todavía."),
    ("Frutas Eloy Ruano", "En conversación", 0.85, 3, 8, 4350, 11310.00, "Dado de alta como cliente en marzo; sin pedidos todavía."),
    ("Mercamadrid (asentadores)", "Por abrir", 0.55, 6, 8, 4350, 10440.00,
     "Contactos abiertos: Chef Fruit, GoldGourmet, Frutas Iberika y Bidfood Iberia; El Abuelo Pedro ya es cliente."),
    ("Makro (cash & carry)", "En conversación", 0.25, 12, 10, 17400, 39150.00, "Sin actividad registrada en el CRM."),
    ("Primaflor", "En conversación", 0.20, 14, 10, 8700, 18270.00, "Sin actividad registrada en el CRM."),
]
d0 = 5
for k, (cta, est, pr, mes, ramp, tar, pot, real) in enumerate(MOD):
    r = d0 + k
    for col, v, fmt, font, wrap in ((1, cta, None, BOLD, True), (2, est, None, BLUE, False), (3, pr, PCT, BLUE, False),
                                    (4, mes, "0", BLUE, False), (5, ramp, "0", BLUE, False), (6, tar, "#,##0", BLUE, False),
                                    (7, pot, EUR0, BLUE, False), (8, f"=G{r}*C{r}", EUR0, BASE, False), (9, real, None, BASE, True)):
        celda(wd, r, col, v, fmt, font, wrap)
dN = d0 + len(MOD) - 1
celda(wd, dN + 1, 1, "TOTAL", font=BOLD)
for col, fmt in (("F", "#,##0"), ("G", EUR0), ("H", EUR0)):
    c = wd[f"{col}{dN+1}"]; c.value = f"=SUM({col}{d0}:{col}{dN})"; c.number_format = fmt; c.font = BOLD; c.fill = TOT; c.border = LINE
celda(wd, dN + 3, 1, "Probabilidad, mes de inicio, rampa y volúmenes: supuestos del modelo financiero V17 (escenario base). "
      "Los descuentos de canal (Mercamadrid 20 %, Makro 25 %, Primaflor 30 %) ya están aplicados en el ingreso potencial.", font=SUB)

# ============================================================ RESUMEN
ws = wb.create_sheet("Resumen", 0)
ws.sheet_view.showGridLines = False
for i, w in enumerate([58, 18, 70], 1):
    ws.column_dimensions[CL(i)].width = w
ws["A1"] = "Rootflow Hydroponics, S.L. — Información para la solicitud ENISA"; ws["A1"].font = TITLE
ws["A2"] = f"Proveedores, clientes y facturación real, y pipeline comercial. Datos del ERP de la empresa a {CORTE}."; ws["A2"].font = SUB


def lin(r, et, f, fmt=EUR, font=None, nota=""):
    ws[f"A{r}"] = et; ws[f"A{r}"].font = font or BASE
    c = ws[f"B{r}"]; c.value = f; c.number_format = fmt; c.font = font or GREEN
    if nota: ws[f"C{r}"] = nota; ws[f"C{r}"].font = SUB


ws["A4"] = "1 · FACTURACIÓN REAL (desde el inicio de la actividad hasta hoy)"; ws["A4"].font = SEC
lin(5, "Facturado y vendido (base imponible, sin IVA)", f"={CLI_T['F']}", nota="Facturas emitidas + tickets de venta directa")
lin(6, "Facturado y vendido (IVA incluido)", f"={CLI_T['G']}")
lin(7, "Cobrado", f"={CLI_T['H']}")
lin(8, "Pendiente de cobro", f"={CLI_T['I']}")
lin(9, "Entregado pendiente de facturar (base)", f"={CLI_T['J']}", nota="Se factura en octubre")
lin(10, "Clientes que ya han comprado (sin contar la venta directa)", f"=COUNTA(Clientes!$A${c0}:$A${cN})-1", fmt="0")
lin(11, "Entregas realizadas", f"={CLI_T['E']}", fmt="0", nota="Incluye 5 tickets de venta directa")

ws["A13"] = "Ventas por mes de entrega (base imponible)"; ws["A13"].font = BOLD
ws["B13"] = "Facturado"; ws["B13"].font = BOLD
ws["C13"] = "Entregado pendiente de facturar"; ws["C13"].font = BOLD
MESES = [("2026-05", "Mayo 2026"), ("2026-06", "Junio 2026"), ("2026-07", "Julio 2026"), ("2026-08", "Agosto 2026 (producción parada)"),
         ("2026-09", "Septiembre 2026"), ("2026-10", "Octubre 2026 (hasta el día 7)")]
for k, (cod, et) in enumerate(MESES):
    r = 14 + k
    ws[f"A{r}"] = et; ws[f"A{r}"].font = BASE
    c = ws[f"B{r}"]; c.value = f'=SUMIFS({VR},{VM},"{cod}",{VF},"Factura")+SUMIFS({VR},{VM},"{cod}",{VF},"Ticket")'
    c.number_format = EUR; c.font = GREEN
    c = ws[f"C{r}"]; c.value = f'=SUMIFS({VR},{VM},"{cod}",{VF},"Entregado, pendiente de facturar")'
    c.number_format = EUR; c.font = GREEN; c.alignment = Alignment(horizontal="left")
ws["A20"] = "Total"; ws["A20"].font = BOLD
for col in "BC":
    c = ws[f"{col}20"]; c.value = f"=SUM({col}14:{col}19)"; c.number_format = EUR; c.font = BOLD; c.border = LINE
ws["C20"].alignment = Alignment(horizontal="left")

ws["A22"] = "2 · PROVEEDORES"; ws["A22"].font = SEC
lin(23, "Compras registradas desde la constitución (IVA incluido)", f"={PROV_TOTAL}",
    nota="Incluye el equipamiento del local actual y la constitución de la sociedad")
ws["A24"] = "Semilla: MP Seeds (Łódź, Polonia) · Sustrato: Organic Growshop (Madrid) · Envases: Envases del Mediterráneo (Murcia)"
ws["A24"].font = BASE
ws["A25"] = "Sistema de cultivo: Leroy Merlin, Plases Grow Shop, Green Ice, LEDBOX · Gestión: ERP propio"; ws["A25"].font = BASE

ws["A27"] = "3 · PIPELINE COMERCIAL"; ws["A27"].font = SEC
lin(28, "Oportunidades abiertas en el CRM (restaurantes, tiendas y distribuidores)", f"={PIPE_ABIERTAS}", fmt="0",
    nota="Hoja «Pipeline restaurantes»")
lin(29, "  · de ellas, en negociación o con interés confirmado",
    f"=COUNTIF('Pipeline restaurantes'!$E${l0}:$E${lN},\"Negociando\")+COUNTIF('Pipeline restaurantes'!$E${l0}:$E${lN},\"Interesado\")"
    f"+COUNTIF('Pipeline restaurantes'!$E${l0}:$E${lN},\"Acuerdo sin pedido\")", fmt="0")
lin(30, "Cuentas de distribución identificadas en el plan financiero", f"=COUNTA('Pipeline distribución'!$A${d0}:$A${dN})", fmt="0",
    nota="Hoja «Pipeline distribución»")
lin(31, "Ingreso ponderado de esas cuentas a régimen (€/mes)", f"='Pipeline distribución'!$H${dN+1}", fmt=EUR0)

ws["A33"] = "Hojas: Clientes · Ventas detalle · Proveedores · Pipeline restaurantes · Pipeline distribución."; ws["A33"].font = SUB

for w in wb.worksheets:
    w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.orientation = "landscape"; w.page_setup.fitToWidth = 1; w.page_setup.fitToHeight = 0
wb.save(OUT)
print("escrito", OUT)
