#!/usr/bin/env python3
"""V17 = V16 + modelo de negocio MIXTO: línea DISTRIBUCIÓN + línea RESTAURANTES.

Qué cambia (todo con fórmulas, nada pegado como valor):
  · Producto: tarifas reales por canal (mayorista, tienda, restaurante) de
    COSTES_ROOTFLOW.xlsx; costes unitarios bottom-up (semilla × dosis, sustrato,
    envase según formato); cilantro a 10 días de luz.
  · Restaurantes (hoja nueva): la palanca (% de la nave para restaurantes),
    ticket, frecuencia, riders, microhub, lanzadera, preparación, captación,
    estacionalidad de agosto y techo de mercado con datos del censo municipal.
  · Hipótesis: índices de precio y coste prudentes (base = tarifa y coste reales),
    ingreso y COGS por bandeja de cada línea.
  · CAPEX: microhub, kit de riders y fianzas de alquiler.
  · Motor mensual (×4 hojas): bloque nuevo de líneas de negocio (filas 170-217)
    y la cuenta de resultados reenlazada a él. La mecánica de escenarios
    (selector Hipótesis!C4 y hojas Esc_*) y la hoja Mano_de_obra no se tocan.

Se puede construir en "modo puente" con parámetros para aislar cada efecto.
"""
import openpyxl, shutil, sys, json
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL

ORIGEN  = "modelo/Rootflow_Modelo_Financiero_V16.xlsx"
DESTINO = "modelo/Rootflow_Modelo_Financiero_V17.xlsx"

INPUT = PatternFill("solid", fgColor="FFF2CC")       # convención del modelo
CALC  = PatternFill("solid", fgColor="E2EFDA")
HEAD  = PatternFill("solid", fgColor="1F4D2B")
BLUE  = Font(color="0000FF")
BOLD  = Font(bold=True)
WHITE = Font(bold=True, color="FFFFFF")
THIN  = Side(style="thin", color="BFC9C2")
BOX   = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
EUR   = '#,##0" €";\\(#,##0") €";\\-'
EUR2  = '#,##0.00" €";\\(#,##0.00") €";\\-'
NUM   = '#,##0;\\(#,##0\\);\\-'
NUM1  = '#,##0.0;\\(#,##0.0\\);\\-'
NUM2  = '0.00'
PCT   = '0.0%'

MENSUALES = {"Modelo_Mensual": ("F", "C"), "Esc_Conservador": ("C", "E"),
             "Esc_Base": ("D", "F"), "Esc_Optimista": ("E", "G")}
#            hoja: (columna de escenario en Hipótesis/Restaurantes, columna de CAPEX)
C0, CN = 3, 86          # C..CH = meses 1..84

DEFAULT = dict(
    tarifas_nuevas=True, costes_nuevos=True, cilantro_luz=10,
    idx_precio_distro=(0.90, 1.00, 1.10), idx_coste=(1.05, 1.00, 0.90),
    idx_precio_rest=(0.90, 1.00, 1.10), pct_retail=0.05,
    s=0.05, lanzamiento=1, rampa=(36, 24, 18), microhub=True, fianzas=True,
    limitar_mercado=1, penetracion=0.30,
)

# ---------- tarifas (COSTES_ROOTFLOW.xlsx, hoja 4) ----------------------------
# fila Producto -> (formato_rest, precio_rest, formato_tienda, precio_tienda, precio_mayorista)
TARIFAS = {
    16: (50, 5.50, 50, 3.00, 3.00),   # Micromezclum (mayorista 100 g)
    17: (30, 7.85, 15, 1.75, 2.50),   # Cilantro
    18: (30, 9.30, 15, 1.65, 2.50),   # Albahaca genovesa
    19: (30, 5.95, 15, 1.85, 1.50),   # Rábano daikon
    20: (30, 6.80, 15, 1.60, 1.50),   # Rúcula
    21: (30, 6.20, 15, 1.85, 1.50),   # Rábano rose
    22: (30, 6.90, 15, 1.55, 1.50),   # Mostaza Red Giant
    23: (15, 4.00, 15, 1.85, 1.50),   # Brócoli (restaurante en 15 g)
    24: (30, 10.80, 15, 1.65, 3.00),  # Amaranto
}
# inactivas: solo tarifa restaurante de las "tarifas facilitadas" (30 g); tienda = mayorista
TARIFAS_INACT = {25: (30, 6.20), 26: (30, 6.00), 27: (30, 8.05), 28: (30, 8.05),
                 29: (30, 9.30), 30: (30, 9.30), 31: (30, 10.15)}
# semilla €/bandeja = precio €/kg × dosis g (COSTES hoja 3)
SEMILLA = {16: 0.3144, 17: 0.225, 18: 0.333, 19: 0.34, 20: 0.165,
           21: 0.3366, 22: 0.44, 23: 0.484, 24: 0.45}

ZONAS = [("Justicia", "Centro", 140), ("Recoletos", "Salamanca", 92),
         ("Castellana", "Salamanca", 69), ("Goya", "Salamanca", 64),
         ("Trafalgar", "Chamberí", 62), ("Almagro", "Chamberí", 57),
         ("Ríos Rosas", "Chamberí", 54), ("Lista", "Salamanca", 47)]


def put(ws, ref, val, fmt=None, fill=None, font=None, bold=False):
    c = ws[ref]; c.value = val
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if font: c.font = font
    elif bold: c.font = BOLD
    return c


# ============================================================================
def hoja_restaurantes(wb, P):
    if "Restaurantes" in wb.sheetnames:
        del wb["Restaurantes"]
    ws = wb.create_sheet("Restaurantes", wb.sheetnames.index("Tarifas") + 1)
    ws.column_dimensions["A"].width = 64
    for c, w in (("B", 11), ("C", 13), ("D", 13), ("E", 13), ("F", 13), ("G", 70)):
        ws.column_dimensions[c].width = w

    put(ws, "A1", "ROOTFLOW — Línea RESTAURANTES (reparto propio con riders desde un microhub)",
        font=Font(bold=True, size=14, color="1F4D2B"))
    ws["A2"] = ("Segunda línea de negocio. La nave produce; una parte se reserva para restaurantes de las 8 zonas "
                "calientes, que reciben dos pedidos por semana con riders desde una cámara refrigerada alquilada. "
                "Celdas amarillas = inputs. El resto se calcula. La columna F sigue al selector de escenario (Hipótesis!C4).")
    for i, t in enumerate(("Concepto", "Unidad", "Conservador", "Base", "Optimista", "Activo", "Fuente / nota"), 1):
        c = ws.cell(row=4, column=i, value=t); c.font = WHITE; c.fill = HEAD

    def fila(r, etiqueta, unidad, valor=None, fmt=None, nota="", esc=None, formula=None):
        ws.cell(row=r, column=1, value=etiqueta)
        ws.cell(row=r, column=2, value=unidad)
        if esc is not None:                                     # input por escenario
            for col, v in zip("CDE", esc):
                put(ws, f"{col}{r}", v, fmt, INPUT, BLUE)
            put(ws, f"F{r}", f"=CHOOSE(Hipótesis!$C$4,C{r},D{r},E{r})", fmt, CALC)
        elif formula is not None:
            put(ws, f"D{r}", formula, fmt, CALC)
        else:
            put(ws, f"D{r}", valor, fmt, INPUT, BLUE)
        if nota: ws.cell(row=r, column=7, value=nota)

    def sec(r, t):
        c = ws.cell(row=r, column=1, value=t); c.font = Font(bold=True, color="1F4D2B", size=11)

    sec(6, "1 · CUÁNTO DE LA NAVE VA A RESTAURANTES — la palanca del modelo")
    fila(7, "% de la capacidad de la nave que se destina a restaurantes (objetivo)", "%", P["s"], PCT,
         "LA PALANCA. Sale de la distribución: la ocupación total no sube, cambia a quién se vende. "
         "0 % = solo distribución. 5 % = reparto de COSTES_ROOTFLOW (5 % restaurante).")
    fila(8, "Mes de lanzamiento de la línea", "mes", P["lanzamiento"], NUM,
         "Mes del modelo en que arrancan microhub, riders y lanzadera.")
    fila(9, "Meses de rampa hasta alcanzar el objetivo", "meses", fmt=NUM, esc=P["rampa"],
         nota="Ritmo comercial. Base: 24 meses (~5 restaurantes netos nuevos al mes). Conservador más lento.")
    fila(10, "¿Limitar al mercado real de las zonas? (1 = sí)", "1/0", P["limitar_mercado"], NUM,
         "Con 1, nunca se vende a más restaurantes de los que el techo de abajo permite.")
    fila(11, "Restaurantes abiertos en las 8 zonas (censo municipal)", "nº", formula="=D83", fmt=NUM,
         nota="Enlazado a la tabla de zonas (sección 7).")
    fila(12, "Penetración máxima alcanzable", "%", P["penetracion"], PCT,
         "Supuesto prudente: 3 de cada 10 restaurantes de la zona. Validar con los primeros meses.")
    fila(13, "TECHO de restaurantes alcanzables", "nº", formula="=D11*D12", fmt=NUM)

    sec(15, "2 · TICKET, FRECUENCIA Y PRECIO (modelo MICROHUB_COSTES · hoja Facturación)")
    fila(16, "Cliente MÍNIMO — % de restaurantes", "%", 0.55, PCT, "MICROHUB_COSTES.xlsx")
    fila(17, "Cliente MÍNIMO — ticket por pedido", "€", 18.5, EUR2)
    fila(18, "Cliente MEDIO — % de restaurantes", "%", 0.30, PCT)
    fila(19, "Cliente MEDIO — ticket por pedido", "€", 30, EUR2)
    fila(20, "Cliente PREMIUM — % de restaurantes", "%", 0.15, PCT)
    fila(21, "Cliente PREMIUM — ticket por pedido", "€", 65, EUR2)
    fila(22, "TICKET MEDIO PONDERADO por pedido", "€", formula="=D16*D17+D18*D19+D20*D21", fmt=EUR2,
         nota="28,93 € con el mix de MICROHUB.")
    fila(23, "Comprobación del mix (debe sumar 100 %)", "", formula='=IF(ABS(D16+D18+D20-1)<0.0001,"OK","REVISAR")')
    fila(24, "Pedidos por semana y restaurante", "nº", 2, NUM1, "Dos pedidos para tenerlo siempre fresco.")
    fila(25, "Semanas por mes", "nº", formula="=Producto!$D$6/7", fmt=NUM2)
    fila(26, "Ajuste de PRECIO restaurantes (índice sobre la tarifa de 30 g)", "índice",
         fmt=PCT, esc=P["idx_precio_rest"],
         nota="La tarifa de 30 g es la de MENOR €/g. Conservador = descuento de captación; optimista = más 15 g y 5 g.")
    fila(27, "Merma + impagados restaurantes", "%", 0.10, PCT, "Igual que distribución.")
    fila(28, "Días de cobro restaurantes", "días", 30, NUM, "Prudente. Sin factoring: son facturas pequeñas.")
    fila(29, "Porte cobrado a pedidos pequeños (0 = no se cobra)", "€/pedido", 0, EUR2,
         "Palanca de upside: la tarifa de referencia cobra 12 € a pedidos <35 €. Desactivado.")
    fila(30, "% de pedidos que pagarían porte", "%", formula="=D16", fmt=PCT, nota="El segmento 'mínimo'.")
    fila(31, "Estacionalidad: demanda de restaurantes en AGOSTO (factor)", "x", 0.15, PCT,
         "-85 % en agosto (MICROHUB). Esa producción no se siembra.")
    fila(32, "Mes natural en que arranca el modelo (mes 1)", "1-12", 4, NUM,
         "Abril de 2027 (nave tras cerrar la financiación). Solo sirve para ubicar agosto.")

    sec(34, "3 · REPARTO CON RIDERS (autónomos, bici/moto, tipo Glovo)")
    fila(35, "Días de reparto al mes", "días", 25, NUM, "MICROHUB_COSTES.xlsx")
    fila(36, "Entregas por hora y rider (salida con la bolsa llena)", "entregas/h", fmt=NUM1, esc=(5, 7, 8),
         nota="7-8 por salida de una hora (dato de producción). Conservador = 5.")
    fila(37, "Coste rider (coste empresa)", "€/h", 16, EUR2, "Cobran 12-13 €/h brutos; 16 €/h coste empresa.")
    fila(38, "Ventana de reparto por rider y día", "h/día", 5, NUM1,
         "Mañana antes del servicio + tarde antes de cenas. Fija cuándo hace falta el 2º rider.")
    fila(39, "Horas mínimas pagadas por rider activo y día", "h/día", 2, NUM1,
         "Prudente: con pocos pedidos se paga igualmente un turno mínimo.")
    fila(40, "Kit por rider: mochila isotérmica + acumuladores (CAPEX)", "€/rider", 150, EUR)
    fila(41, "Riders previstos para el kit (CAPEX)", "nº", 2, NUM)

    sec(43, "4 · MICROHUB (cámara refrigerada alquilada en la zona de reparto)")
    fila(44, "Alquiler del microhub con cámaras refrigeradas", "€/mes", 500, EUR, "MICROHUB_COSTES.xlsx")
    fila(45, "Suministros del microhub (luz de cámaras, si no van incluidos)", "€/mes", 100, EUR, "Supuesto.")
    fila(46, "Acondicionamiento: estanterías, mesa inox, balanza, etiquetadora, sondas APPCC (CAPEX)",
         "€", 3500, EUR, "Supuesto. Validar con presupuesto.")
    fila(47, "Cámara o armario refrigerado propio (CAPEX; 0 si va en el alquiler)", "€", 0, EUR,
         "La cámara va alquilada: 0.")
    fila(48, "Fianza del alquiler del microhub", "meses", 2, NUM)

    sec(50, "5 · LANZADERA NAVE → MICROHUB Y PREPARACIÓN DE PEDIDOS")
    fila(51, "Viajes nave → microhub al mes", "nº", formula="=D35", fmt=NUM, nota="Uno por día de reparto.")
    fila(52, "Kilómetros ida y vuelta por viaje", "km", 30, NUM, "Nave en el sur de Madrid → Salamanca/Chamberí.")
    fila(53, "Combustible por km (9 L/100 km × 2,09 €/L)", "€/km", formula="=0.09*2.09", fmt=EUR2,
         nota="MICROHUB_COSTES · Furgoneta. El renting ya está en OPEX.")
    fila(54, "Horas de conductor por viaje (con carga y descarga)", "h", 1, NUM1)
    fila(55, "Coste hora de conductor", "€/h", 16, EUR2)
    fila(56, "Minutos de preparación por pedido (picking + etiquetado)", "min", 3, NUM1,
         "MICROHUB no lo incluía: se añade.")
    fila(57, "Coste hora de preparación", "€/h", 16, EUR2)
    fila(58, "Embalaje por pedido (bolsa, etiqueta)", "€", 0.15, EUR2, "Supuesto.")

    sec(60, "6 · CAPTACIÓN Y CARTERA")
    fila(61, "Coste de captación por restaurante (muestras, visitas)", "€", 40, EUR, "Supuesto.")
    fila(62, "Rotación mensual de restaurantes (churn)", "%", 0.015, PCT,
         "≈17 % al año. Hay que reponerlos y eso cuesta captación.")
    fila(63, "Restaurantes que puede atender un comercial", "nº", 100, NUM, "Para el chequeo de capacidad comercial.")

    sec(64, "LO QUE IMPLICA LA PALANCA — escenario activo, año 5 (se calcula solo)")
    MM = "Modelo_Mensual!"
    fila(65, "Restaurantes en cartera (mes 60)", "nº", formula=f"={MM}$BJ$196", fmt=NUM)
    fila(66, "Riders necesarios (mes 60)", "nº", formula=f"={MM}$BJ$200", fmt=NUM)
    fila(67, "Entregas al día (media del año 5)", "nº", formula=f"=SUM({MM}$AY$198:$BJ$198)/12", fmt=NUM1)
    fila(68, "% de los kilos que van a restaurantes (año 5)", "%",
         formula=f"=IFERROR(SUM({MM}$AY$181:$BJ$181)/SUM({MM}$AY$26:$BJ$26),0)", fmt=PCT)
    fila(69, "% de los ingresos que vienen de restaurantes (año 5)", "%",
         formula=f"=IFERROR(SUM({MM}$AY$35:$BJ$35)/SUM({MM}$AY$36:$BJ$36),0)", fmt=PCT)
    fila(70, "¿El techo de mercado limita la palanca?", "",
         formula=(f'=IF({MM}$BJ$176<D7*Hipótesis!$D$13*Hipótesis!$F$26-0.5,'
                  f'"SÍ: subir la palanca ya no añade restaurantes","No")'))

    sec(72, "7 · ZONAS CALIENTES — restaurantes abiertos (Censo de Locales, Ayto. de Madrid, epígrafe 561001)")
    for i, t in enumerate(("Barrio", "Distrito", "", "Restaurantes"), 1):
        c = ws.cell(row=73, column=i, value=t); c.font = WHITE; c.fill = HEAD
    for i, (b, d, n) in enumerate(ZONAS):
        r = 74 + i
        ws.cell(row=r, column=1, value=b); ws.cell(row=r, column=2, value=d)
        put(ws, f"D{r}", n, NUM, INPUT, BLUE)
    put(ws, "A83", "TOTAL 8 ZONAS", bold=True)
    put(ws, "D83", "=SUM(D74:D81)", NUM, CALC, bold=True)
    ws["A84"] = ("Fuente: datos.madrid.es · Censo de locales, sus actividades y terrazas (actualizado 01/10/2026). "
                 "Locales en situación 'Abierto' con epígrafe 561001 RESTAURANTE. No incluye 714 bar-restaurantes "
                 "de las mismas zonas: son mercado adicional no contado.")
    return ws


# ============================================================================
def producto(wb, P):
    p = wb["Producto"]
    # globales de coste
    put(p, "A12", "Coste envase tarrina PEQUEÑA (5-15 g), sin IVA")
    put(p, "D12", 0.10, EUR2, INPUT, BLUE)
    put(p, "A13", "Coste envase tarrina GRANDE (30-100 g), sin IVA")
    put(p, "D13", 0.17, EUR2, INPUT, BLUE)
    put(p, "A14", "Sustrato por bandeja, sin IVA (saco 100 L a 18 € con IVA; 2,5 L por bandeja)")
    put(p, "D14", "=(18/1.21)*(2.5/100)", EUR2, CALC)
    for co, v in (("F12", "COSTES_ROOTFLOW.xlsx · hoja 1"), ("F13", "COSTES_ROOTFLOW.xlsx · hoja 1"),
                  ("F14", "COSTES_ROOTFLOW.xlsx · hoja 1")):
        p[co] = v
    p["A5"] = "(obsoleto desde V17) Ratio precio DIRECTO ÷ DISTRIBUCIÓN — los precios por canal están en las columnas de tarifas"

    # cabeceras renombradas y nuevas
    for co, t in (("E15", "Formato\nMAYORISTA (g)"), ("F15", "Precio MAYORISTA\n€/tarrina"),
                  ("G15", "€/kg\nMAYORISTA"), ("L15", "Tarrinas/band\nmayorista"),
                  ("P15", "Envase\n€/tarrina (may.)"), ("R15", "COGS €/band\n/ciclo (may.)"),
                  ("S15", "COGS MAYOR.\n€/band/mes"), ("T15", "Ingreso MAYOR.\n€/band/mes")):
        p[co] = t
    nuevas = ["Formato\nRESTAUR. (g)", "Precio RESTAUR.\n€/tarrina", "€/kg\nRESTAUR.", "Tarrinas/band\nrestaur.",
              "Envase rest.\n€/tarrina", "Ingreso RESTAUR.\n€/band/mes", "COGS RESTAUR.\n€/band/mes",
              "Formato\nTIENDA (g)", "Precio TIENDA\n€/tarrina", "€/kg\nTIENDA", "Tarrinas/band\ntienda",
              "Envase tienda\n€/tarrina", "Ingreso TIENDA\n€/band/mes", "COGS TIENDA\n€/band/mes"]
    for i, t in enumerate(nuevas):
        c = p.cell(row=15, column=23 + i, value=t)
        c.font = WHITE; c.fill = HEAD; c.alignment = Alignment(wrap_text=True, vertical="center")
        p.column_dimensions[CL(23 + i)].width = 12.5

    if P["cilantro_luz"] is not None:
        put(p, "H17", P["cilantro_luz"], NUM, INPUT, BLUE)

    for r in range(16, 32):
        # costes unitarios bottom-up
        if P["costes_nuevos"]:
            if r in SEMILLA:
                put(p, f"N{r}", SEMILLA[r], EUR2, INPUT, BLUE)
            put(p, f"O{r}", "=Producto!$D$14", EUR2, CALC)
            put(p, f"P{r}", f"=IF(E{r}<=15,Producto!$D$12,Producto!$D$13)", EUR2, CALC)
        # tarifa mayorista
        if P["tarifas_nuevas"] and r in TARIFAS:
            put(p, f"F{r}", TARIFAS[r][4], EUR2, INPUT, BLUE)
        # tarifas restaurante y tienda
        if r in TARIFAS:
            fr, pr_, ft, pt, _ = TARIFAS[r]
            put(p, f"W{r}", fr, NUM, INPUT, BLUE); put(p, f"X{r}", pr_, EUR2, INPUT, BLUE)
            put(p, f"AD{r}", ft, NUM, INPUT, BLUE); put(p, f"AE{r}", pt, EUR2, INPUT, BLUE)
        else:
            fr, pr_ = TARIFAS_INACT[r]
            put(p, f"W{r}", fr, NUM, INPUT, BLUE); put(p, f"X{r}", pr_, EUR2, INPUT, BLUE)
            put(p, f"AD{r}", f"=E{r}", NUM, CALC); put(p, f"AE{r}", f"=F{r}", EUR2, CALC)
        envase = "IF({f}{r}<=15,Producto!$D$12,Producto!$D$13)" if P["costes_nuevos"] else "P{r}"
        put(p, f"Y{r}", f"=IFERROR(X{r}/W{r}*1000,0)", EUR2, CALC)
        put(p, f"Z{r}", f"=IFERROR(K{r}/W{r},0)", NUM2, CALC)
        put(p, f"AA{r}", "=" + envase.format(f="W", r=r), EUR2, CALC)
        put(p, f"AB{r}", f"=Z{r}*X{r}*J{r}", EUR2, CALC)
        put(p, f"AC{r}", f"=(N{r}+O{r}+Z{r}*AA{r})*J{r}", EUR2, CALC)
        put(p, f"AF{r}", f"=IFERROR(AE{r}/AD{r}*1000,0)", EUR2, CALC)
        put(p, f"AG{r}", f"=IFERROR(K{r}/AD{r},0)", NUM2, CALC)
        put(p, f"AH{r}", "=" + envase.format(f="AD", r=r), EUR2, CALC)
        put(p, f"AI{r}", f"=AG{r}*AE{r}*J{r}", EUR2, CALC)
        put(p, f"AJ{r}", f"=(N{r}+O{r}+AG{r}*AH{r})*J{r}", EUR2, CALC)
    for col in ("AB", "AC", "AI", "AJ"):
        put(p, f"{col}32", f"=SUMPRODUCT(C16:C31,D16:D31,{col}16:{col}31)", EUR2, CALC, bold=True)

    put(p, "A35", "Precio medio ponderado MAYORISTA (€/kg)")
    put(p, "A43", "PRECIO MEDIO PONDERADO POR CANAL (tarifa, sin índice de escenario)", bold=True)
    for r, et, f in ((44, "Mayorista (distribución, Mercamadrid)", "=IFERROR(T32/M32,0)"),
                     (45, "Tienda / retail", "=IFERROR(AI32/M32,0)"),
                     (46, "Restaurante (formato de 30 g, el de menor €/g)", "=IFERROR(AB32/M32,0)")):
        p[f"A{r}"] = et; put(p, f"D{r}", f, '#,##0.00" €/kg"', CALC)
    put(p, "A47", "MARGEN BRUTO DE PRODUCTO POR CANAL (antes de logística y merma)", bold=True)
    for r, et, f in ((48, "Mayorista", "=IFERROR((T32-S32)/T32,0)"),
                     (49, "Tienda / retail", "=IFERROR((AI32-AJ32)/AI32,0)"),
                     (50, "Restaurante", "=IFERROR((AB32-AC32)/AB32,0)")):
        p[f"A{r}"] = et; put(p, f"D{r}", f, PCT, CALC)
    p["A52"] = ("Tarifas: COSTES_ROOTFLOW.xlsx (hoja 4). Restaurante usa el formato de 30 g, el de MENOR margen por "
                "gramo (criterio de la propia hoja). Las variedades inactivas toman la tarifa facilitada de 30 g y, en "
                "tienda, la de mayorista. El rendimiento por bandeja sigue siendo el validado por producción (V16).")


# ============================================================================
def hipotesis(wb, P):
    h = wb["Hipótesis"]
    h["A16"] = "Ajuste de PRECIO — línea DISTRIBUCIÓN (índice sobre la tarifa mayorista/tienda actual)"
    h["A18"] = "Ajuste de COSTE de producto (índice sobre el coste bottom-up)"
    for col, v in zip("CDE", P["idx_precio_distro"]): put(h, f"{col}16", v, PCT, INPUT, BLUE)
    for col, v in zip("CDE", P["idx_coste"]):         put(h, f"{col}18", v, PCT, INPUT, BLUE)
    h["A20"] = "Ingreso por bandeja — DISTRIBUCIÓN, nuevas cuentas (mezcla mayorista/tienda × índices)"
    h["A21"] = "Ingreso por bandeja — RESTAURANTES (tarifa 30 g × índice de precio restaurantes)"
    h["A22"] = "COGS por bandeja — DISTRIBUCIÓN (mezcla mayorista/tienda × índice de coste)"
    for col in "CDE":
        h[f"{col}20"] = (f"=((1-Hipótesis!${col}$30)*Producto!$T$32+Hipótesis!${col}$30*Producto!$AI$32)"
                         f"*Hipótesis!${col}$16*Hipótesis!${col}$17")
        h[f"{col}21"] = f"=Producto!$AB$32*Restaurantes!${col}$26*Hipótesis!${col}$17"
        h[f"{col}22"] = (f"=((1-Hipótesis!${col}$30)*Producto!$S$32+Hipótesis!${col}$30*Producto!$AJ$32)"
                         f"*Hipótesis!${col}$18")
    if P.get("formula_capa_v16"):          # solo para el puente: precio de nuevas cuentas como en el V16
        for col in "CDE":
            h[f"{col}20"] = (f"=Producto!$T$32*(0.3+0.7/Producto!$D$5)*Hipótesis!${col}$16*Hipótesis!${col}$17")
    h["A30"] = "Línea DISTRIBUCIÓN: % de las nuevas cuentas que son RETAIL (tienda) frente a mayorista"
    for col in "CDE": put(h, f"{col}30", P["pct_retail"], PCT, INPUT, BLUE)

    put(h, "A128", "LÍNEA RESTAURANTES — economía por bandeja (enlaza Producto y Restaurantes)", bold=True)
    h["A129"] = "COGS por bandeja — RESTAURANTES (€/band/mes × índice de coste)"
    h["A130"] = "Ingreso por bandeja — RESTAURANTES a tarifa, SIN índice (sirve para contar pedidos)"
    for r in (129, 130): h[f"B{r}"] = "€/band/mes"
    for col in "CDE":
        put(h, f"{col}129", f"=Producto!$AC$32*Hipótesis!${col}$18", EUR2)
        put(h, f"{col}130", f"=Producto!$AB$32*Hipótesis!${col}$17", EUR2)
    for r in (129, 130):
        put(h, f"F{r}", f"=CHOOSE($C$4,C{r},D{r},E{r})", EUR2, CALC)


# ============================================================================
def capex(wb, P):
    cx = wb["CAPEX"]
    put(cx, "A40", "MICROHUB Y REPARTO A RESTAURANTES", bold=True)
    on = "(Restaurantes!$D$7>0)" if P["microhub"] else "0"
    for r, et, f in ((41, "Acondicionamiento del microhub", f"=Restaurantes!$D$46*{on}"),
                     (42, "Cámara / armario refrigerado propio", f"=Restaurantes!$D$47*{on}"),
                     (43, "Kit riders (mochilas isotérmicas + acumuladores)",
                      f"=Restaurantes!$D$40*Restaurantes!$D$41*{on}")):
        cx[f"A{r}"] = et; put(cx, f"C{r}", f, EUR, CALC)
    put(cx, "A44", "SUBTOTAL MICROHUB", bold=True); put(cx, "C44", "=SUM(C41:C43)", EUR, CALC, bold=True)

    put(cx, "A46", "FIANZAS DE ALQUILER (salida de caja inicial; no se amortizan)", bold=True)
    mn = 2 if P["fianzas"] else 0
    cx["A47"] = "Meses de fianza de la nave"; put(cx, "C47", mn, NUM, INPUT, BLUE)
    cx["A48"] = "Fianza de la nave (€)"
    for col, hc in (("C", "F"), ("E", "C"), ("F", "D"), ("G", "E")):
        put(cx, f"{col}48", f"=$C$47*Hipótesis!${hc}$36", EUR, CALC)
    cx["A49"] = "Fianza del microhub (€)"
    put(cx, "C49", f"=Restaurantes!$D$48*Restaurantes!$D$44*(Restaurantes!$D$7>0)*{1 if P['fianzas'] else 0}", EUR, CALC)
    put(cx, "A50", "TOTAL FIANZAS", bold=True)
    for col in "CEFG":
        put(cx, f"{col}50", f"={col}48+$C$49", EUR, CALC, bold=True)

    # subtotal, coste fijo de arranque y necesidad
    for col in "CEFG":
        cx[f"{col}19"] = f"=$C$38+{col}10+C15+C17+C18+$C$44"
        cx[f"{col}26"] = f"={col}22+{col}25+{col}50"
    hub = "+IF(AND(Restaurantes!$D$8<=1,Restaurantes!$D$7>0),Restaurantes!$D$44+Restaurantes!$D$45,0)"
    for col, hc in (("C", "F"), ("E", "C"), ("F", "D"), ("G", "E")):
        cx[f"{col}24"] = (f"=Hipótesis!${hc}$36+Hipótesis!${hc}$37+Hipótesis!${hc}$39+Hipótesis!${hc}$40"
                          f"+Hipótesis!$E$55{hub}")
    cx["D19"] = "Incluye el microhub (fila 44)."
    cx["D26"] = "CAPEX + contingencia + colchón de arranque + fianzas."


# ============================================================================
def motor(ws, S, K):
    """Escribe el bloque de líneas de negocio y reenlaza la cuenta de resultados.
    S = columna de escenario en Hipótesis/Restaurantes; K = columna de CAPEX."""
    H = lambda r: f"Hipótesis!${S}${r}"
    R = lambda r: f"Restaurantes!$D${r}"
    RS = lambda r: f"Restaurantes!${S}${r}"
    filas = {}

    def linea(r, etiqueta, gen, fmt=EUR, bold=False):
        ws.cell(row=r, column=1, value=etiqueta)
        if bold: ws.cell(row=r, column=1).font = BOLD
        for col in range(C0, CN + 1):
            L, Pv = CL(col), CL(col - 1)
            c = ws.cell(row=r, column=col, value=gen(L, Pv, col == C0))
            c.number_format = fmt
            if bold: c.font = BOLD
        filas[etiqueta] = r

    t = ws.cell(row=168, column=1, value="LÍNEAS DE NEGOCIO — DISTRIBUCIÓN + RESTAURANTES (V17)")
    t.font = Font(bold=True, size=12, color="1F4D2B")
    ws.cell(row=169, column=1, value="Las filas de la cuenta de resultados (34, 35, 37, 39, 52, 54) leen de este bloque.")

    linea(171, "Mes natural (1-12)", lambda L, P_, f: f"=MOD({R(32)}+{L}$3-2,12)+1", NUM)
    linea(172, "Factor estacional restaurantes (agosto)", lambda L, P_, f: f"=IF({L}171=8,{R(31)},1)", PCT)
    linea(173, "Rampa de la línea restaurantes (0-100 %)",
          lambda L, P_, f: f"=IF({L}$3<{R(8)},0,MIN(1,({L}$3-{R(8)}+1)/MAX(1,{RS(9)})))", PCT)
    linea(174, "Posiciones de clientes identificados servidas (pipeline)", lambda L, P_, f: f"={L}18*{L}21", NUM)
    linea(175, "Techo de mercado expresado en posiciones",
          lambda L, P_, f: (f"=IF({R(10)}=1,{R(13)}*{R(24)}*{R(25)}*{R(22)}/MAX(0.0001,{H(130)}),9E+9)"), NUM)
    linea(176, "Restaurantes — posiciones objetivo (cartera, sin estacionalidad)",
          lambda L, P_, f: f"=MIN({R(7)}*Hipótesis!$D$13*{H(26)},{L}175)*{L}173", NUM)
    linea(177, "Restaurantes — posiciones asignadas (tras capacidad física)",
          lambda L, P_, f: f"=MIN({L}176,MAX(0,{L}8-{L}174))", NUM)
    linea(178, "Restaurantes — posiciones en producción (con estacionalidad)",
          lambda L, P_, f: f"={L}177*{L}172", NUM, bold=True)
    linea(179, "Distribución — posiciones (pipeline + nuevas cuentas)", lambda L, P_, f: f"={L}174+{L}23", NUM, bold=True)
    linea(180, "Ocupación total de la nave", lambda L, P_, f: f"=IFERROR(({L}179+{L}178)/{L}8,0)", PCT)
    linea(181, "kg/mes a RESTAURANTES", lambda L, P_, f: f"={L}178*{H(23)}", NUM)
    linea(182, "kg/mes a DISTRIBUCIÓN", lambda L, P_, f: f"={L}20*{L}21+{L}23*{H(23)}", NUM)
    linea(183, "% de la producción (kg) que va a restaurantes",
          lambda L, P_, f: f"=IFERROR({L}181/({L}181+{L}182),0)", PCT)
    # ingresos
    linea(184, "Ingresos DISTRIBUCIÓN — clientes identificados (pipeline a tarifa)",
          lambda L, P_, f: f"={L}16*{L}21*{H(16)}")
    linea(185, "Ingresos DISTRIBUCIÓN — nuevas cuentas", lambda L, P_, f: f"={L}23*{H(20)}")
    linea(186, "INGRESOS LÍNEA DISTRIBUCIÓN (bruto)", lambda L, P_, f: f"={L}184+{L}185", bold=True)
    linea(187, "Ingresos restaurantes a tarifa, sin índice (base de pedidos)",
          lambda L, P_, f: f"={L}178*{H(130)}")
    linea(188, "Pedidos al mes", lambda L, P_, f: f"=IFERROR({L}187/{R(22)},0)", NUM)
    linea(189, "Ingresos por porte de pedidos pequeños", lambda L, P_, f: f"={L}188*{R(30)}*{R(29)}")
    linea(190, "INGRESOS LÍNEA RESTAURANTES (bruto)", lambda L, P_, f: f"={L}178*{H(21)}+{L}189", bold=True)
    linea(191, "% de los ingresos que vienen de restaurantes",
          lambda L, P_, f: f"=IFERROR({L}190/({L}186+{L}190),0)", PCT)
    linea(192, "(–) Merma DISTRIBUCIÓN", lambda L, P_, f: f"=-{L}186*{H(34)}")
    linea(193, "(–) Merma RESTAURANTES", lambda L, P_, f: f"=-{L}190*{R(27)}")
    linea(194, "(–) COGS DISTRIBUCIÓN", lambda L, P_, f: f"=-({L}19*{L}21*{H(18)}+{L}23*{H(22)})")
    linea(195, "(–) COGS RESTAURANTES", lambda L, P_, f: f"=-{L}178*{H(129)}")
    # operación restaurantes
    linea(196, "Restaurantes en cartera",
          lambda L, P_, f: f"=IFERROR({L}177*{H(130)}/{R(22)}/({R(24)}*{R(25)}),0)", NUM1, bold=True)
    linea(197, "Restaurantes captados en el mes (netos + reposición por rotación)",
          lambda L, P_, f: (f"=MAX(0,{L}196)" if f else f"=MAX(0,{L}196-{P_}196)+{P_}196*{R(62)}"), NUM1)
    linea(198, "Entregas al día", lambda L, P_, f: f"=IFERROR({L}188/{R(35)},0)", NUM1)
    linea(199, "Horas de reparto al día", lambda L, P_, f: f"=IFERROR({L}198/{RS(36)},0)", NUM1)
    linea(200, "Riders necesarios", lambda L, P_, f: f"=IF({L}198>0,MAX(1,ROUNDUP({L}199/{R(38)},0)),0)", NUM, bold=True)
    linea(201, "Horas de rider pagadas al mes",
          lambda L, P_, f: f"=MAX({L}199,{L}200*{R(39)})*{R(35)}", NUM)
    linea(202, "(–) Riders", lambda L, P_, f: f"=-{L}201*{R(37)}")
    linea(203, "(–) Microhub (alquiler + suministros)",
          lambda L, P_, f: f"=-IF(AND({L}$3>={R(8)},{R(7)}>0),{R(44)}+{R(45)},0)")
    linea(204, "(–) Lanzadera nave → microhub",
          lambda L, P_, f: f"=-IF(AND({L}$3>={R(8)},{R(7)}>0),{R(51)}*({R(52)}*{R(53)}+{R(54)}*{R(55)}),0)")
    linea(205, "(–) Preparación de pedidos", lambda L, P_, f: f"=-{L}188*{R(56)}/60*{R(57)}")
    linea(206, "(–) Embalaje de pedidos", lambda L, P_, f: f"=-{L}188*{R(58)}")
    linea(207, "(–) TOTAL ÚLTIMA MILLA RESTAURANTES", lambda L, P_, f: f"=SUM({L}202:{L}206)", bold=True)
    linea(208, "Coste de última milla por pedido", lambda L, P_, f: f"=IFERROR(-{L}207/{L}188,0)", EUR2)
    linea(209, "(–) Captación de restaurantes", lambda L, P_, f: f"=-{L}197*{R(61)}")
    linea(210, "Restaurantes por comercial activo (Nico + KAM)",
          lambda L, P_, f: (f"=IFERROR({L}196/(Hipótesis!$B$49*({L}$3>=Hipótesis!$D$49)"
                            f"+Hipótesis!$B$52*({L}$3>=Hipótesis!$D$52)),0)"), NUM)
    linea(211, "(–) Logística DISTRIBUCIÓN (furgo propia en Madrid + Athos fuera)",
          lambda L, P_, f: (f"=-({L}182*(1-Logistica!$B$5)*Logistica!$B$7"
                            f"+{L}182*Logistica!$B$5*Logistica!$B$39)"))
    linea(212, "Saldo de clientes DISTRIBUCIÓN", lambda L, P_, f: f"=({L}186+{L}192)*{H(66)}/30")
    linea(213, "Saldo de clientes RESTAURANTES", lambda L, P_, f: f"=({L}190+{L}193)*{R(28)}/30")
    linea(214, "MARGEN DE CONTRIBUCIÓN — DISTRIBUCIÓN",
          lambda L, P_, f: f"={L}186+{L}192+{L}194+{L}211", bold=True)
    linea(215, "MARGEN DE CONTRIBUCIÓN — RESTAURANTES",
          lambda L, P_, f: f"={L}190+{L}193+{L}195+{L}207+{L}209", bold=True)
    linea(216, "Comprobación: posiciones ≤ capacidad (1 = OK)",
          lambda L, P_, f: f"=IF({L}179+{L}178<={L}8+0.001,1,0)", NUM)
    linea(217, "Comprobación: restaurantes ≤ techo de mercado (1 = OK)",
          lambda L, P_, f: f"=IF({L}196<={R(13)}+0.001,1,0)", NUM)

    # ---- reenlace de la cuenta de resultados ----
    for col in range(C0, CN + 1):
        L = CL(col)
        ws[f"{L}23"] = f"=MAX(0,MIN({L}8*{L}22-{L}177,{L}8-{L}18*{L}21-{L}178))"
        ws[f"{L}24"] = f"={L}18*{L}21+{L}23+{L}178"
        ws[f"{L}26"] = f"={L}20*{L}21+{L}23*{H(23)}+{L}181"
        ws[f"{L}27"] = f"={L}17*{L}21+{L}23*{H(24)}+{L}178*{H(24)}"
        ws[f"{L}34"] = f"={L}186"
        ws[f"{L}35"] = f"={L}190"
        ws[f"{L}37"] = f"={L}192+{L}193"
        ws[f"{L}39"] = f"={L}194+{L}195"
        ws[f"{L}52"] = f"={L}211+{L}207"
        ws[f"{L}54"] = f"=-{H(40)}+{L}209"
        ws[f"{L}60"] = (f"=-({L}91+{L}98+{L}103+{L}77+{L}212*Hipótesis!$D$73*Hipótesis!$D$74/12)")
        ws[f"{L}68"] = f"={L}212+{L}213"
        ws[f"{L}70"] = f"={L}212*(1-Hipótesis!$D$73)+{L}213-{L}69"
    ws["C72"] = f"=-CAPEX!${K}$22*CAPEX!$C$29-CAPEX!${K}$50"
    for r, t in ((16, "DEMANDA IDENTIFICADA — ingresos a tarifa mayorista (€/mes)"),
                 (22, "Nuevas cuentas (distribución + restaurantes) — utilización objetivo (%)"),
                 (23, "Nuevas cuentas de DISTRIBUCIÓN — posiciones (objetivo menos restaurantes)"),
                 (24, "Posiciones ocupadas TOTALES (distribución + restaurantes)"),
                 (34, "Ingresos — línea DISTRIBUCIÓN (distribuidores, retail, Mercamadrid)"),
                 (35, "Ingresos — línea RESTAURANTES (reparto propio con riders)"),
                 (37, "(–) Merma / comercial / impagados (ambas líneas)"),
                 (39, "(–) COGS (semilla + sustrato + envases, ambas líneas)"),
                 (52, "(–) OPEX · Logística: distribución + última milla restaurantes"),
                 (54, "(–) OPEX · Otros (gestoría, seguros…) + captación de restaurantes"),
                 (68, "Saldo de CLIENTES (distribución + restaurantes)"),
                 (70, "NOF — circulante NETO (factoring solo sobre distribución)")):
        ws.cell(row=r, column=1, value=t)
    return filas


# ============================================================================
def resumenes(wb):
    ra = wb["Resumen_Anual"]
    ra["A25"] = "(–) Logística: distribución + última milla restaurantes"
    ra["A26"] = "Ingresos de clientes identificados (pipeline)"
    for i in range(7):
        a, b = CL(3 + 12 * i), CL(14 + 12 * i)
        ra.cell(row=26, column=3 + i).value = f"=SUM(Modelo_Mensual!${a}$184:${b}$184)"
    put(ra, "A38", "MIX DE CANALES (escenario activo)", font=Font(bold=True, color="1F4D2B"))
    defs = [
        (39, "Ingresos línea DISTRIBUCIÓN", "sum", 34, EUR),
        (40, "Ingresos línea RESTAURANTES", "sum", 35, EUR),
        (41, "% de los ingresos que vienen de restaurantes", "f", "=IFERROR({c}40/{c}5,0)", PCT),
        (42, "kg vendidos a restaurantes", "sum", 181, NUM),
        (43, "% de la producción (kg) a restaurantes", "f", "=IFERROR({c}42/{c}22,0)", PCT),
        (44, "Margen de contribución DISTRIBUCIÓN", "sum", 214, EUR),
        (45, "Margen de contribución RESTAURANTES", "sum", 215, EUR),
        (46, "  · sobre ingresos de distribución", "f", "=IFERROR({c}44/{c}39,0)", PCT),
        (47, "  · sobre ingresos de restaurantes", "f", "=IFERROR({c}45/{c}40,0)", PCT),
        (48, "Restaurantes en cartera (fin de año)", "fin", 196, NUM),
        (49, "Pedidos en el año", "sum", 188, NUM),
        (50, "Riders (fin de año)", "fin", 200, NUM),
        (51, "(–) Coste de última milla restaurantes", "sum", 207, EUR),
        (52, "Coste de última milla por pedido", "f", "=IFERROR(-{c}51/{c}49,0)", EUR2),
        (53, "(–) Captación de restaurantes", "sum", 209, EUR),
    ]
    for r, et, tipo, x, fmt in defs:
        ra.cell(row=r, column=1, value=et)
        for i in range(7):
            col = 3 + i; c = CL(col); a, b = CL(3 + 12 * i), CL(14 + 12 * i)
            if tipo == "sum": v = f"=SUM(Modelo_Mensual!${a}${x}:${b}${x})"
            elif tipo == "fin": v = f"=Modelo_Mensual!${b}${x}"
            else: v = x.format(c=c)
            cell = ra.cell(row=r, column=col, value=v); cell.number_format = fmt

    rs = wb["Resumen"]
    rs["A8"] = "Precio — línea distribución (índice sobre tarifa actual)"
    rs["A9"] = "Coste de producto (índice sobre el coste bottom-up)"
    rs["A47"] = "Precio medio ponderado — mayorista (€/kg)"
    rs["C50"] = "=IFERROR(SUM(Modelo_Mensual!$C$184:$N$184)/SUM(Modelo_Mensual!$C$36:$N$36),0)"
    put(rs, "A64", "LÍNEA RESTAURANTES vs DISTRIBUCIÓN — año 5 (régimen)", font=Font(bold=True, color="1F4D2B"))
    for i, t in enumerate(("CONSERVADOR", "BASE", "OPTIMISTA")):
        c = rs.cell(row=65, column=3 + i, value=t); c.font = BOLD
    esc = ("Esc_Conservador", "Esc_Base", "Esc_Optimista")
    filas = [
        (66, "Precio restaurantes (índice sobre tarifa 30 g)", lambda e, k: f"=Restaurantes!${k}$26", PCT),
        (67, "% de la nave reservado a restaurantes (objetivo)", lambda e, k: "=Restaurantes!$D$7", PCT),
        (68, "Restaurantes en cartera (mes 60)", lambda e, k: f"={e}!$BJ$196", NUM),
        (69, "Techo de restaurantes alcanzables", lambda e, k: "=Restaurantes!$D$13", NUM),
        (70, "Pedidos al mes (media año 5)", lambda e, k: f"=SUM({e}!$AY$188:$BJ$188)/12", NUM),
        (71, "Riders (mes 60)", lambda e, k: f"={e}!$BJ$200", NUM),
        (72, "% de la producción (kg) a restaurantes", lambda e, k: f"=IFERROR(SUM({e}!$AY$181:$BJ$181)/SUM({e}!$AY$26:$BJ$26),0)", PCT),
        (73, "Ingresos restaurantes (año 5)", lambda e, k: f"=SUM({e}!$AY$35:$BJ$35)", EUR),
        (74, "% de los ingresos de restaurantes", lambda e, k: f"=IFERROR(SUM({e}!$AY$35:$BJ$35)/SUM({e}!$AY$36:$BJ$36),0)", PCT),
        (75, "Margen de contribución restaurantes (año 5)", lambda e, k: f"=SUM({e}!$AY$215:$BJ$215)", EUR),
        (76, "  · sobre sus ingresos", lambda e, k: f"=IFERROR(SUM({e}!$AY$215:$BJ$215)/SUM({e}!$AY$35:$BJ$35),0)", PCT),
        (77, "Margen de contribución distribución (año 5)", lambda e, k: f"=SUM({e}!$AY$214:$BJ$214)", EUR),
        (78, "  · sobre sus ingresos", lambda e, k: f"=IFERROR(SUM({e}!$AY$214:$BJ$214)/SUM({e}!$AY$34:$BJ$34),0)", PCT),
        (79, "Coste de última milla por pedido (año 5)", lambda e, k: f"=IFERROR(-SUM({e}!$AY$207:$BJ$207)/SUM({e}!$AY$188:$BJ$188),0)", EUR2),
    ]
    for r, et, gen, fmt in filas:
        rs.cell(row=r, column=1, value=et)
        for i, (e, k) in enumerate(zip(esc, "CDE")):
            rs.cell(row=r, column=3 + i, value=gen(e, k)).number_format = fmt

    sb = wb["Sensibilidad"]
    sb["A6"] = "Ingreso medio por posición y mes (€) — mezcla de canales en régimen"
    sb["B6"] = "=IFERROR(Modelo_Mensual!$CH$36/Modelo_Mensual!$CH$24,Producto!$T$32)"
    sb["C6"] = "enlazado al modelo mensual (mes 84)"
    sb["A7"] = "COGS medio por posición y mes (€) — mezcla de canales"
    sb["B7"] = "=IFERROR(-Modelo_Mensual!$CH$39/Modelo_Mensual!$CH$24,Producto!$S$32)"
    sb["A14"] = "Costes NO-bandeja (alquiler, luz, nóminas fijas, logística y última milla, otros) €/mes"
    sb["B14"] = "=-Modelo_Mensual!$CH$55+Modelo_Mensual!$CH$50"

    lg = wb["Logistica"]
    lg["A29"] = "Producción que va a DISTRIBUCIÓN (kg/mes, régimen)"
    lg["B29"] = "=Modelo_Mensual!$CH$182"
    lg["B36"] = "=IFERROR($B$34/Modelo_Mensual!$CH$34,0)"
    lg["A36"] = "Coste logístico de distribución como % de sus ingresos"

    pl = wb["Pipeline"]
    pl["A7"] = "Precio MAYORISTA €/tarrina"


# ============================================================================
def hoja_lineas(wb):
    """Cuenta de resultados por línea de negocio (escenario activo, anual)."""
    if "Lineas_Negocio" in wb.sheetnames:
        del wb["Lineas_Negocio"]
    ws = wb.create_sheet("Lineas_Negocio", wb.sheetnames.index("Resumen_Anual") + 1)
    ws.column_dimensions["A"].width = 62
    for i in range(7):
        ws.column_dimensions[CL(3 + i)].width = 13
    put(ws, "A1", "ROOTFLOW — Cuenta de resultados por LÍNEA DE NEGOCIO (escenario activo)",
        font=Font(bold=True, size=14, color="1F4D2B"))
    ws["A2"] = ("Cada línea carga sus costes directos (producto, merma, logística o última milla, captación). "
                "Los costes de la nave y la estructura son comunes. La suma cuadra con el EBITDA del modelo mensual.")
    for i, t in enumerate(["Concepto", ""] + [f"Año {k}" for k in range(1, 8)], 1):
        c = ws.cell(row=4, column=i, value=t); c.font = WHITE; c.fill = HEAD
    MM = "Modelo_Mensual!"

    def suma(r):  return lambda a, b, c: f"=SUM({MM}${a}${r}:${b}${r})"
    def fin(r):   return lambda a, b, c: f"={MM}${b}${r}"
    def f(expr):  return lambda a, b, c: "=" + expr.format(c=c)
    def neg(r):   return lambda a, b, c: f"=SUM({MM}${a}${r}:${b}${r})"

    filas = [
        (5, "LÍNEA 1 · DISTRIBUCIÓN (distribuidores, retail, Mercamadrid)", None, None, "sec"),
        (6, "kg vendidos", suma(182), NUM, ""),
        (7, "Ingresos brutos", suma(186), EUR, "b"),
        (8, "  · de clientes identificados (pipeline)", suma(184), EUR, ""),
        (9, "  · de nuevas cuentas", suma(185), EUR, ""),
        (10, "(–) Merma / impagados", suma(192), EUR, ""),
        (11, "(–) Coste de producto (semilla, sustrato, envase)", suma(194), EUR, ""),
        (12, "(–) Logística (furgo propia Madrid + Athos fuera)", suma(211), EUR, ""),
        (13, "MARGEN DE CONTRIBUCIÓN — DISTRIBUCIÓN", suma(214), EUR, "b"),
        (14, "  · % sobre sus ingresos", f("IFERROR({c}13/{c}7,0)"), PCT, ""),
        (15, "  · € por kg", f("IFERROR({c}13/{c}6,0)"), EUR2, ""),
        (17, "LÍNEA 2 · RESTAURANTES (reparto propio desde el microhub)", None, None, "sec"),
        (18, "Restaurantes en cartera (fin de año)", fin(196), NUM, ""),
        (19, "Pedidos servidos", suma(188), NUM, ""),
        (20, "kg vendidos", suma(181), NUM, ""),
        (21, "Ingresos brutos", suma(190), EUR, "b"),
        (22, "(–) Merma / impagados", suma(193), EUR, ""),
        (23, "(–) Coste de producto (semilla, sustrato, envase)", suma(195), EUR, ""),
        (24, "(–) Riders", suma(202), EUR, ""),
        (25, "(–) Microhub (alquiler + suministros)", suma(203), EUR, ""),
        (26, "(–) Lanzadera nave → microhub", suma(204), EUR, ""),
        (27, "(–) Preparación y embalaje de pedidos", lambda a, b, c: f"=SUM({MM}${a}$205:${b}$206)", EUR, ""),
        (28, "(–) Captación de restaurantes", suma(209), EUR, ""),
        (29, "MARGEN DE CONTRIBUCIÓN — RESTAURANTES", suma(215), EUR, "b"),
        (30, "  · % sobre sus ingresos", f("IFERROR({c}29/{c}21,0)"), PCT, ""),
        (31, "  · € por kg", f("IFERROR({c}29/{c}20,0)"), EUR2, ""),
        (32, "  · € por pedido", f("IFERROR({c}29/{c}19,0)"), EUR2, ""),
        (34, "COSTES COMUNES (nave y estructura)", None, None, "sec"),
        (35, "(–) Alquiler de la nave", suma(42), EUR, ""),
        (36, "(–) Suministros (fijo + luz por posición)", suma(43), EUR, ""),
        (37, "(–) Nóminas (socios, encargado, operarios, KAM)", suma(51), EUR, ""),
        (38, "(–) Vehículo (renting)", suma(53), EUR, ""),
        (39, "(–) Otros (gestoría, seguros, software, marketing)",
         lambda a, b, c: f"=SUM({MM}${a}$54:${b}$54)-SUM({MM}${a}$209:${b}$209)", EUR, ""),
        (40, "TOTAL COSTES COMUNES", f("SUM({c}35:{c}39)"), EUR, "b"),
        (42, "EBITDA = margen distribución + margen restaurantes + costes comunes", f("{c}13+{c}29+{c}40"), EUR, "b"),
        (43, "Comprobación contra el modelo mensual (debe ser 0)", lambda a, b, c: f"=ROUND({c}42-SUM({MM}${a}$56:${b}$56),2)", EUR, ""),
        (45, "PESO DE CADA LÍNEA", None, None, "sec"),
        (46, "% de los kg que van a restaurantes", f("IFERROR({c}20/({c}6+{c}20),0)"), PCT, ""),
        (47, "% de los ingresos que vienen de restaurantes", f("IFERROR({c}21/({c}7+{c}21),0)"), PCT, ""),
        (48, "% del margen de contribución que viene de restaurantes", f("IFERROR({c}29/({c}13+{c}29),0)"), PCT, ""),
    ]
    for r, et, gen, fmt, st in filas:
        c = ws.cell(row=r, column=1, value=et)
        if st == "sec":
            c.font = Font(bold=True, color="1F4D2B", size=11); continue
        if st == "b": c.font = BOLD
        for i in range(7):
            a, b = CL(3 + 12 * i), CL(14 + 12 * i)
            cell = ws.cell(row=r, column=3 + i, value=gen(a, b, CL(3 + i)))
            cell.number_format = fmt
            if st == "b": cell.font = BOLD
    ws["A50"] = ("Lectura: restaurantes usa poca nave y mucho margen por kg; distribución da el volumen. "
                 "La palanca está en Restaurantes!D7.")
    ws.freeze_panes = "C5"


def portada(wb):
    po = wb["Portada"]
    for r in range(3, 40):
        po.cell(row=r, column=2).value = None
    lineas = {
        3: "Modelo financiero V17 — Ronda: inversor privado (capital) + ENISA",
        4: "Microbrotes y flores comestibles · Madrid · DOS líneas de negocio: distribución + restaurantes",
        6: "Qué hay dentro",
        7: "· PRODUCTO: rendimiento, ciclos y coste bottom-up por variedad; TARIFAS REALES por canal (mayorista, tienda, restaurante).",
        8: "· TARIFAS: hoja para cargar el export del ERP (no alimenta todavía el modelo).",
        9: "· RESTAURANTES: la palanca (% de la nave para restaurantes), ticket, riders, microhub, lanzadera, captación, agosto y techo de mercado con el censo municipal.",
        10: "· PIPELINE: clientes de distribución identificados. Alimentan la demanda de la línea de distribución.",
        11: "· HIPÓTESIS: escenarios, nóminas, financiación y estructura del inversor (capital 10 %, suelo 1,5×, salida año 4).",
        12: "· LOGÍSTICA: distribución con furgo propia en Madrid y Athos fuera. CAPEX: nave, automatización, microhub y fianzas.",
        13: "· MODELO_MENSUAL (escenario activo) y Esc_* (los tres casos, 84 meses). Bloque de líneas de negocio en filas 168-217.",
        15: "Cómo funciona la mezcla de canales",
        14: "· LINEAS_NEGOCIO: cuenta de resultados por línea (distribución, restaurantes y costes comunes), cuadrada con el EBITDA.",
        16: "La nave produce. Restaurantes!D7 fija qué parte de su capacidad se vende a restaurantes: SALE de la distribución, no se suma.",
        17: "Orden: clientes identificados de distribución → restaurantes (con rampa y techo de mercado) → nuevas cuentas de distribución.",
        18: "Con 0 % el modelo es solo distribución (volúmenes idénticos al V16). Más % = más ingreso por kg, pero más restaurantes, riders y captación.",
        20: "Criterios de prudencia del caso BASE (V17)",
        21: "· Precios = tarifas actuales (índice 100 %); conservador −10 %, optimista +10 %. Restaurante en formato de 30 g, el de menor €/g.",
        22: "· Costes de producto = bottom-up (índice 100 %). Rendimientos validados por producción.",
        23: "· Agosto: la demanda de restaurantes cae un 85 %. Riders con turno mínimo pagado. Captación y rotación de restaurantes con coste.",
        25: "AVISO CLAVE — minutos por bandeja",
        26: "Es la palanca de coste más sensible. El caso base asume 3 min/bandeja con la automatización incluida en CAPEX (lavadora + cinta).",
        27: "La hoja de costes operativa usa 4 min/bandeja. Ver la hoja Sensibilidad antes de presentar.",
        29: "ESTRUCTURA DE FINANCIACIÓN",
        30: "Inversor privado: capital (10 % por 100.000 €), suelo de cobro 1,5×, salida pactada desde el año 4, vía nota convertible.",
        31: "ENISA: préstamo participativo, carencia 24 meses. Exige fondos propios ≥ préstamo (chequeo en la fila 165 de cada escenario).",
        32: "Factoring del 60 % solo sobre facturas de distribución. Póliza de crédito para el resto del circulante.",
        33: "Dividendos bloqueados hasta amortizar toda la deuda (condición ENISA).",
        35: "Leyenda: amarillo = input · verde = cálculo · negro = fórmula. No insertes filas: el modelo depende de ellas.",
        37: "V17 · Octubre 2026",
    }
    for r in range(3, 40):
        po.cell(row=r, column=2).font = Font(size=10, color="333333")
    for r, t in lineas.items():
        c = po.cell(row=r, column=2, value=t)
        if r in (3, 6, 15, 20, 25, 29):
            c.font = Font(bold=True, size=12 if r == 3 else 11, color="1F4D2B")
        elif r in (26, 31):
            c.font = Font(bold=True, size=10, color="9C2A00")


# ============================================================================
def construir(P=None, destino=DESTINO, origen=ORIGEN):
    P = {**DEFAULT, **(P or {})}
    shutil.copy(origen, destino)
    wb = openpyxl.load_workbook(destino, data_only=False)
    producto(wb, P)
    hoja_restaurantes(wb, P)
    hipotesis(wb, P)
    capex(wb, P)
    for nombre, (S, K) in MENSUALES.items():
        motor(wb[nombre], S, K)
    resumenes(wb)
    hoja_lineas(wb)
    portada(wb)
    wb.save(destino)
    return destino


if __name__ == "__main__":
    extra = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    out = construir(extra, sys.argv[1] if len(sys.argv) > 1 else DESTINO)
    print("escrito", out)
