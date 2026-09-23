# Revisión operativa V16 — cifras para los decks

> 23/09/2026 · Modelo **V16** (`modelo/Rootflow_Modelo_Financiero_V16.xlsx`), recalculado y verificado.
> Base: V15. El V15 se conserva intacto para poder comparar.
> Estructura de capital, selector de escenarios, Mano_de_obra, OPEX y precios: **sin tocar**.

---

## Tabla para los decks

### Producción

| Concepto | V15 | **V16** | Cambio |
|---|---|---|---|
| Capacidad actual · 96 bandejas, mix (kg/mes) | 107,8 | **118,8** | +11,0 |
| Capacidad actual · pico monocultivo rábano (kg/mes) | 170,4 | **238,5** | +68,1 |
| Nave en régimen · base (kg/mes) | 2.938 | **3.119** | +181 |
| Nave en régimen · conservador / optimista | 2.795 / 3.044 | **2.962 / 3.236** | — |
| Rendimiento ponderado (kg/bandeja/mes) | 1,1225 | **1,2370** | +10,2 % |
| Ingreso por bandeja (€/mes) | 44,14 | **49,39** | +11,9 % |
| Precio medio ponderado (€/kg) | 39,32 | **39,92** | +1,5 % |
| Multiplicador nave vs. hoy | ×18 *(deck)* | **×26,3 en kg · ×30 en posiciones** | corregido |

### Financiación y CAPEX — sin cambios

| Partida | € |
|---|---|
| Adaptación de nave (clima, eléctrico, fontanería) | 40.000 |
| Racks de cultivo (3 × 1.600 €) | 4.800 |
| Instalación y montaje | 10.000 |
| Mobiliario, utillaje, EPIs | 10.000 |
| **Bloque obra + racks** *(input parametrizado, ver B2)* | **64.800** |
| Automatización (según escenario) | 10.000 |
| Vehículo de reparto (renting) | 0 |
| Licencias, proyecto técnico e ingeniería | 6.000 |
| Legal / estructuración | 5.000 |
| **Subtotal CAPEX** | **85.800** |
| Contingencia (15 %) | 12.870 |
| **CAPEX + contingencia** | **98.670** |
| Colchón de circulante (4 meses) | 62.608 |
| **NECESIDAD DE FINANCIACIÓN** | **161.278** |

Ronda 200.000 € → cobertura **1,24×**. Sin cambios respecto al V15.

### Cuenta de resultados — escenario base

| Año | Ingresos V15 | **Ingresos V16** | EBITDA V15 | **EBITDA V16** | **Margen V16** | **Plantilla** | **kg/mes medio** |
|---|---|---|---|---|---|---|---|
| 1 | 182.509 | **187.388** | −51.620 | **−47.311** | **−25,2 %** | 4 | 353 |
| 2 | 685.547 | **720.399** | 191.397 | **220.713** | **30,6 %** | 7 | 1.630 |
| 3 | 1.033.329 | **1.101.639** | 350.220 | **409.694** | **37,2 %** | 8 | 2.493 |
| 4 | 1.273.677 | **1.370.566** | 468.143 | **548.962** | **40,1 %** | 9 | 3.051 |
| 5 | 1.302.988 | **1.403.362** | 460.201 | **543.914** | **38,8 %** | 9 | 3.119 |

### Retorno del inversor y solidez

| Escenario | TIR V15 | **TIR V16** | MOIC V15 | **MOIC V16** | **Equity a la salida** | **Cobra** | **DSCR mín** | **Caja mín** |
|---|---|---|---|---|---|---|---|---|
| Conservador | 10,7 % | **10,7 %** | 1,50× | **1,50×** | **1.218.204 €** | **150.000 €** | **4,77** | **30.000 €** |
| **Base** | 35,1 % | **40,7 %** | 3,33× | **3,92×** | **3.921.151 €** | **392.115 €** | **12,87** | **30.000 €** |
| Optimista | 53,2 % | **58,0 %** | 5,51× | **6,23×** | **6.233.494 €** | **623.349 €** | **17,77** | **30.000 €** |

Los tres escenarios siguen cumpliendo el requisito de fondos propios de ENISA.
---

## Bloque A — aplicado

### A1 · Rendimientos por bandeja ✅

| Variedad | Estado | V15 | **V16** |
|---|---|---|---|
| Cilantro split | CONFIRMADO | 120 g | **145 g** |
| Albahaca genovesa | CONFIRMADO | 100 g | **90 g** |
| Rábano daikon | PROVISIONAL | 175 g | **245 g** |
| Rábano rose | PROVISIONAL | 175 g | **245 g** |

**Tres cosas que he dejado sin tocar y necesitan tu confirmación:**

1. **Rábano red** sigue en **200 g**. Está `INACTIVO`, así que no entra en ningún cálculo, pero si vuelve a activarse arrastrará el dato viejo. ¿Va también a 245 g?
2. **Micromezclum** (el mix de 7 variedades) sigue en **170 g**, y pesa el **40 % de la luz** — es la variedad más importante del portfolio con diferencia. Si ese mix lleva rábano, su rendimiento tiene que subir también, y el impacto sería mayor que todo lo anterior junto.
3. Las **demás variedades activas** (rúcula 170 g, mostaza 160 g, brócoli 170 g, amaranto 80 g) no las has mencionado. Siguen como estaban.

### A2 · Días de luz — DISCREPANCIA, no he cambiado nada ⚠️

| Variedad | Deck | Modelo | ¿Cuadra? |
|---|---|---|---|
| Cilantro | 6 germ. + 9 luz = **15 días** | 5 germ. + **11 luz** = 16 días | **No** |
| Albahaca | 6 germ. + 12 luz = **18 días** | 5 germ. + **13 luz** = 18 días | Total sí, reparto no |

**El que manda es el modelo, y solo la columna «días de luz».** Los ciclos se calculan como `30,42 ÷ (días de luz + días muertos)`, porque la germinación ocurre en blackout, fuera de las posiciones de luz. Los días de germinación **no entran en el cálculo**: cambiarlos no movería nada.

O sea: si el cilantro real son **9 días de luz** y no 11, los ciclos suben de 2,77 a 3,38 al mes (+22 % de producción en esa variedad). **No lo he tocado.** Dime qué número es el bueno.

Y un tercer desajuste que conviene mirar: el deck describe un **«rábano de ciclo corto: 3 + 2 días, 15 ciclos/mes, 210 g»**. Ese es el **rábano red**, que está **INACTIVO** en el modelo. Los rábanos que de verdad producís (daikon y rose) tienen **3 días de luz → 10,1 ciclos/mes**. El deck está describiendo una variedad que no cultiváis.

### A3 · Capacidad — la nave cuadra, la capacidad actual no está modelada

**Lo que cuadra perfecto:**

| | Tu socio | Modelo | |
|---|---|---|---|
| Superficie por bandeja | 0,15 m² | `Hipótesis!D11` = 0,15 | ✅ |
| Posiciones de la nave | 2.880 | 3 racks × 960 = 2.880 | ✅ |
| Superficie de cultivo | 432 m² | 3 × 144 = 432 m² | ✅ |

**Lo que no está:** el modelo **no modela la instalación actual en absoluto**. Arranca directamente con 1 rack de la nave nueva (960 posiciones) en el mes 1. La celda `Hipótesis!D8` («Rack ANTIGUO — bandejas por rack» = 32) existe pero **no la usa ninguna fórmula**: es un input muerto.

Por eso la capacidad de hoy solo vive en el deck, y ahí los números no salían:

- **96 bandejas × 1,2370 kg = 118,8 kg/mes** con el mix, no los ~160 del deck.
- **96 × 2,484 kg = 238,5 kg/mes** en monocultivo de rábano, no los ~350 del deck.
- El **×18** del deck sale de dividir 2.900 entre 160. Con la capacidad real es **×26,3 en kg** y **×30 en posiciones y superficie**.

La diferencia entre ×26,3 y ×30 no es un error: la nave no produce a tope: en régimen ocupa el 100 % de las posiciones pero el mix y el techo de utilización de la capa adicional (55 %) dejan la producción por debajo del máximo teórico.

---

## Bloque B — preparado, pendiente de datos

### B1 · Días muertos entre ciclos

Ya era un input (`Producto!D7`), ahora está marcado en azul y documentado. `Ciclos/mes = 30,42 ÷ (días de luz + días muertos)`.

| | Ciclos/mes portfolio | Ciclos rábano | kg/bandeja/mes | kg/mes régimen | EBITDA año 5 | TIR base |
|---|---|---|---|---|---|---|
| **0 días** (actual) | 6,85 | 10,14 | 1,2370 | 3.119 | 543.914 € | 40,7 % |
| **1 día** | 5,45 | 7,61 | 0,9744 | 2.703 | 428.495 € | 32,7 % |

**Un día muerto cuesta 115.000 € de EBITDA al año y 8 puntos de TIR.** Es el parámetro más sensible de todo el modelo operativo — más que los rendimientos que acabamos de subir. Conviene medirlo de verdad antes de enseñar el caso base.

*Nota:* tu estimación de «unos 10 ciclos/mes para el rábano con 1 día muerto» corresponde al rábano de **2 días de luz** (el red, inactivo). Con los rábanos activos, de 3 días de luz, un día muerto los deja en **7,6 ciclos/mes**.

### B2 · Presupuesto de obra — input creado

En la hoja `CAPEX`:

| Celda | Qué es |
|---|---|
| `C35` | Bloque nave + racks + instalación + utillaje, bottom-up = **64.800 €** |
| `C36` | **PRESUPUESTO REAL** — escribe aquí el importe cuando llegue (0 = usar el bottom-up) |
| `C37` | Ajuste % para sensibilidad rápida (0,25 = +25 %) |
| `C38` | Bloque aplicado, que es lo que consume el subtotal |

| Escenario | Bloque obra | Necesidad | Cobertura | Caja mín | DSCR mín | TIR base | MOIC |
|---|---|---|---|---|---|---|---|
| Actual | 64.800 € | 161.278 € | **1,24×** | 30.000 € | 12,87 | 40,7 % | 3,92× |
| +10 % | 71.280 € | 168.730 € | 1,19× | 30.000 € | 12,87 | 40,7 % | 3,91× |
| +25 % | 81.000 € | 179.908 € | 1,11× | 30.000 € | 12,87 | 40,6 % | 3,90× |
| **+50 %** | 97.200 € | 198.538 € | **1,01×** | 30.000 € | 12,87 | 40,4 % | 3,89× |

**Lo que se rompe es la cobertura, no la rentabilidad.** El CAPEX es un pago único: apenas mueve la TIR (−0,3 puntos con un +50 %) ni el DSCR. Pero **con un +50 % la cobertura cae a 1,01×**: la ronda cubriría la necesidad justo, sin colchón. El umbral está en torno a **+48 %**; por encima de ahí hay que levantar más.

### B3 · Tamaño de ronda

Manteniendo la regla de ENISA (fondos propios ≥ préstamo) y una pre-money de 900.000 €:

| Ronda | Privado | ENISA | % inversor | Cobertura | TIR base | MOIC | Caja mínima | ¿Cumple ENISA? |
|---|---|---|---|---|---|---|---|---|
| **200.000 €** *(actual)* | 100.000 | 100.000 | **10,0 %** | 1,24× | **40,7 %** | 3,92× | 30.000 € | Sí |
| 250.000 € | 125.000 | 125.000 | 12,2 % | 1,55× | 40,0 % | 3,85× | 76.070 € | Sí |
| 300.000 € | 150.000 | 150.000 | 14,3 % | 1,86× | 39,4 % | 3,78× | 125.262 € | Sí |

Subir la ronda **casi no penaliza al inversor** (−0,7 puntos de TIR al pasar de 200 a 250 k€) y **multiplica el colchón de caja por 2,5**. Si el presupuesto de obra se va por encima del +25 %, la ronda de 250.000 € es la que mantiene la cobertura en zona cómoda.

### B4 · Tarifas del ERP — estructura creada

Hoja nueva **`Tarifas`**, entre `Producto` y `Pipeline`:

- **Tabla de carga** (200 filas, celdas azules): cliente · variedad · canal · formato · €/tarrina · tarrinas/mes. Calcula sola €/mes, kg/mes y €/kg.
- **Resumen por variedad** (columnas K-O): agrega por variedad con `SUMIF` y da el **€/kg ponderado** y el **€/tarrina medio**.
- **Contraste**: `N25` muestra el precio que usa hoy el modelo (**39,92 €/kg**) y `N26` la diferencia contra las tarifas reales.

**Nada de esa hoja alimenta el modelo todavía**, a propósito. Cuando tengáis el export y lo hayáis revisado, el paso es copiar el `€/tarrina medio` de cada variedad a `Producto!F`. Dime cuándo y lo enlazo.

### B5 · OPEX

Sin tocar, como pediste.

---

## Bloque C — no tocado ✅

Estructura de capital V15 (10 % por 100.000 €, suelo 1,5×, salida desde el año 4, nota convertible), selector de escenarios `Hipótesis!C4` y hoja `Mano_de_obra`: intactos.

---

## Qué necesito de ti

1. **Días de luz del cilantro**: ¿9 u 11? Vale +22 % de producción en esa variedad.
2. **Micromezclum**: es el 40 % de la luz y sigue en 170 g. ¿Se queda?
3. **Rábano red**: ¿245 g también, o se queda en 200 g mientras esté inactivo?
4. **Días muertos**: el parámetro más caro del modelo. ¿Medimos?
5. **El deck describe un rábano que no cultiváis** (2 días de luz). ¿Lo cambio al daikon real?
