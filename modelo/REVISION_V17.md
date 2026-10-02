# Revisión V17 — modelo de negocio mixto: distribución + restaurantes

> 02/10/2026 · Modelo **V17** (`modelo/Rootflow_Modelo_Financiero_V17.xlsx`), recalculado y verificado.
> Base: V16 (se conserva intacto). Generador reproducible: `scripts/modelo_v17.py`.
> **Sin tocar:** estructura de capital V15 (10 % por 100.000 €, suelo 1,5×, salida desde el año 4, nota convertible), ronda de 200.000 €, selector de escenarios (Hipótesis!C4) y hoja Mano_de_obra.

---

## 1. Qué cambia en una frase

La nave sigue produciendo lo mismo, pero ahora vende por **dos líneas de negocio**:

| | **Línea 1 · Distribución** | **Línea 2 · Restaurantes** |
|---|---|---|
| Clientes | Distribuidores, retail, Mercamadrid (pipeline actual + nuevas cuentas) | Restaurantes de 8 zonas calientes de Madrid |
| Precio | Tarifa mayorista (y tienda en el 5 % retail) | Tarifa restaurante (formato de 30 g, el de menor €/g) |
| Entrega | Furgo propia en Madrid + Athos fuera | 2 pedidos/semana con riders desde un microhub refrigerado |
| Papel | Volumen | Margen por kilo y marca |

**La palanca** está en `Restaurantes!D7`: % de la capacidad de la nave que se vende a restaurantes. **Sale de la distribución, no se suma**: la ocupación total de la nave es la misma que en el V16 (con 0 % el modelo reproduce exactamente los volúmenes del V16). El caso base usa **5 %**, el mismo reparto que la hoja de costes (`5. FACTURACIÓN Y VENTAS`: 5 % restaurante, 5 % tienda, 90 % mayorista).

Orden de servicio cada mes: clientes identificados de distribución → restaurantes (con rampa y techo de mercado) → nuevas cuentas de distribución.

---

## 2. Qué se ha incorporado y de dónde sale

| Bloque | Dónde | Dato | Fuente |
|---|---|---|---|
| Tarifas por canal | Producto, cols. F, W-AJ | Mayorista, tienda y restaurante por variedad | COSTES_ROOTFLOW.xlsx · hoja 4 |
| Coste unitario | Producto, cols. N-P, D12-D14 | Semilla (€/kg × dosis), sustrato 0,37 €/band., envase 0,17 € (30-100 g) / 0,10 € (5-15 g) | COSTES_ROOTFLOW.xlsx · hojas 1 y 3 |
| Cilantro | Producto!H17 | 10 días de luz (antes 11) | Decisión de producción |
| Ticket y frecuencia | Restaurantes 16-25 | Mix 55/30/15 % (18,50 / 30 / 65 €) → **ticket medio 28,93 €**, 2 pedidos/semana | MICROHUB_COSTES.xlsx · Facturación |
| Riders | Restaurantes 35-41 | 16 €/h coste empresa, 7 entregas/h (5 cons. · 8 opt.), ventana 5 h/día → 1 rider al principio, 2 en régimen; mínimo 2 h/día pagadas | Producción + MICROHUB_COSTES |
| Microhub | Restaurantes 44-48 | Alquiler 500 €/mes + 100 €/mes suministros; acondicionamiento 3.500 € (CAPEX); fianza 2 meses | MICROHUB_COSTES + supuestos |
| Lanzadera nave → microhub | Restaurantes 51-55 | 25 viajes/mes, 30 km, 0,19 €/km, 1 h de conductor a 16 €/h | MICROHUB_COSTES · Furgoneta |
| Preparación | Restaurantes 56-58 | 3 min/pedido a 16 €/h + 0,15 € de embalaje | Añadido (MICROHUB no lo incluía) |
| Captación y cartera | Restaurantes 61-63 | 40 €/restaurante captado, rotación 1,5 %/mes | Supuestos |
| Estacionalidad | Restaurantes 31-32 | Agosto −85 % (solo restaurantes) | MICROHUB_COSTES |
| Techo de mercado | Restaurantes 11-13, 72-84 | **585 restaurantes abiertos** en las 8 zonas × 30 % = **175** | Censo de Locales del Ayto. de Madrid (datos.madrid.es, epígrafe 561001) |
| Fianzas | CAPEX 46-50 | 2 meses de la nave + 2 del microhub | Supuesto |
| Kit riders | CAPEX 43 | 2 × 150 € | Supuesto |

Restaurantes abiertos por zona (censo municipal): Justicia 140 · Recoletos 92 · Castellana 69 · Goya 64 · Trafalgar 62 · Almagro 57 · Ríos Rosas 54 · Lista 47. No se cuentan los 714 bar-restaurantes de esas mismas zonas: son mercado adicional.

**Hojas nuevas:** `Restaurantes` (inputs de la línea y bloque «lo que implica la palanca») y `Lineas_Negocio` (cuenta de resultados por línea, cuadrada al céntimo con el EBITDA). **Motor:** bloque nuevo en las filas 168-217 de las cuatro hojas mensuales; la cuenta de resultados lee de él.

---

## 3. Criterios de prudencia

- **Precios = tarifa real, sin subidas.** El V16 suponía +20 % de precio y −15 % de coste en el caso base; el V17 usa la tarifa y el coste reales (índice 100 %). Conservador −10 % de precio y +5 % de coste; optimista +10 % / −10 %.
- **Restaurantes en el formato de 30 g**, el más barato por gramo (criterio de la propia hoja de costes).
- **Sin volumen extra:** los restaurantes salen de la nave que ya se vendía a distribución.
- **Techo de mercado activado:** nunca más restaurantes que el 30 % de los censados en las zonas.
- **Costes de arranque desde el mes 1:** microhub, lanzadera y rider con turno mínimo pagado aunque haya pocos pedidos.
- **Agosto −85 %** en restaurantes y esa producción no se reasigna.
- Los descuentos de canal del pipeline (Mercamadrid −20 %, Makro −25 %, Primaflor −30 %) se aplican **encima** de la tarifa mayorista.

---

## 4. Resultados

### Por escenario (año 5, régimen)

| | Conservador V16 | **Conservador V17** | Base V16 | **Base V17** | Optimista V16 | **Optimista V17** |
|---|---|---|---|---|---|---|
| Ingresos | 1.106.500 | **1.452.129** | 1.403.362 | **1.720.250** | 1.642.538 | **1.980.364** |
| · de restaurantes | — | **285.621 (19,7 %)** | — | **344.953 (20,1 %)** | — | **402.215 (20,3 %)** |
| EBITDA | 176.569 | **388.643** | 543.914 | **713.969** | 858.246 | **1.051.016** |
| Margen EBITDA | 16,0 % | **26,8 %** | 38,8 % | **41,5 %** | 52,3 % | **53,1 %** |
| Restaurantes en cartera | — | **113** | — | **123** | — | **130** |
| Riders | — | **2** | — | **2** | — | **2** |
| TIR inversor | 10,7 % | **28,2 %** | 40,7 % | **50,7 %** | 58,0 % | **66,6 %** |
| MOIC | 1,50× | **2,70×** | 3,92× | **5,16×** | 6,23× | **7,70×** |
| Cobro a la salida (mes 48) | 150.000 | **270.220** | 392.115 | **515.986** | 623.349 | **769.793** |
| DSCR mínimo | 4,77 | **9,55** | 12,87 | **15,94** | 17,77 | **20,44** |
| Póliza máxima dispuesta | 23.292 | **29.594** | 3.133 | **15.581** | 6.183 | **10.050** |
| Necesidad de financiación | 148.778 | **161.048** | 161.278 | **173.048** | 185.228 | **196.598** |
| Requisito ENISA de fondos propios | Cumple | **Cumple** | Cumple | **Cumple** | Cumple | **Cumple** |

Caja mínima: 30.000 € en todos los casos (la póliza la sostiene; límite 50.000 €). Ronda de 200.000 € → cobertura base **1,16×** (antes 1,24×).

### Caso base, año a año

| Año | Ingresos | · distribución | · restaurantes | EBITDA | Margen | Restaurantes (fin de año) | Riders | Plantilla |
|---|---|---|---|---|---|---|---|---|
| 1 | 248.408 | 153.340 | 95.068 | −29.923 | −12,0 % | 62 | 1 | 4 |
| 2 | 899.516 | 631.971 | 267.545 | 308.816 | 34,3 % | 123 | 2 | 7 |
| 3 | 1.372.473 | 1.027.520 | 344.953 | 553.026 | 40,3 % | 123 | 2 | 9 |
| 4 | 1.682.448 | 1.337.495 | 344.953 | 716.372 | 42,6 % | 123 | 2 | 9 |
| 5 | 1.720.250 | 1.375.297 | 344.953 | 713.969 | 41,5 % | 123 | 2 | 9 |

### Economía de cada línea (base, año 5)

| | Distribución | Restaurantes |
|---|---|---|
| kg vendidos al año | 35.394 (94,7 %) | 1.996 (5,3 %) |
| Ingresos | 1.375.297 € (79,9 %) | 344.953 € (20,1 %) |
| Precio medio a tarifa | 43,67 €/kg (mayorista) | 172,84 €/kg |
| Margen de contribución | 972.655 € · 70,7 % | 239.867 € · 69,5 % |
| Margen de contribución por kg | **27,48 €** | **120,18 €** |
| Pedidos al año | — | 11.926 (≈40 entregas/día) |
| Coste de última milla | — | 4,42 €/pedido (15 % del ticket) |
| Margen por pedido | — | 20,11 € |

Lectura para el inversor: **restaurantes usa el 5 % de los kilos y aporta el 20 % del margen.** Cada kilo vale cuatro veces más que en distribución, incluso después de pagar riders, microhub, lanzadera y captación. Distribución sigue siendo el motor de volumen.

---

## 5. Puente V16 → V17 (caso base, EBITDA del año 5)

| Paso | EBITDA año 5 | Efecto | TIR | MOIC |
|---|---|---|---|---|
| V16 | 543.914 | — | 40,7 % | 3,92× |
| + cilantro a 10 días de luz | 551.520 | +7.606 | 41,2 % | 3,97× |
| + costes unitarios reales (semilla, sustrato, envase) | 531.597 | −19.923 | 39,9 % | 3,84× |
| + tarifas reales por canal (mayorista + 5 % tienda) | 851.179 | +319.582 | 57,1 % | 6,09× |
| − quitar los índices optimistas del V16 (+20 % precio, −15 % coste) | 545.587 | −305.592 | 40,0 % | 3,85× |
| + fianzas (solo caja: necesidad +4.000 €) | 545.587 | 0 | 40,0 % | 3,84× |
| + **línea de restaurantes al 5 %** | **713.969** | **+168.382** | **50,7 %** | **5,16×** |

Conclusión: con tarifas y costes reales y **sin los ajustes optimistas del V16**, la distribución sola da el mismo EBITDA que el V16 (546 k€ frente a 544 k€). **Toda la mejora del V17 sale de la línea de restaurantes.** La regresión está comprobada: con la línea apagada y los datos del V16, el generador reproduce el V16 exacto (mismos volúmenes, costes, plantilla y EBITDA).

---

## 6. Sensibilidades de la línea de restaurantes (caso base)

| Prueba | EBITDA año 5 | vs. base | Restaurantes | TIR | MOIC |
|---|---|---|---|---|---|
| **V17 base (palanca 5 %)** | **713.969** | — | 123 | 50,7 % | 5,16× |
| Palanca 0 % (solo distribución) | 545.587 | −168.382 | 0 | 40,0 % | 3,84× |
| Palanca 2,5 % (1 rider) | 622.532 | −91.437 | 62 | 45,1 % | 4,43× |
| Palanca 7,5 % o más (choca con el techo) | 791.896 | +77.927 | 176 | 55,1 % | 5,78× |
| Techo con penetración del 20 % | 704.962 | −9.007 | 117 | 50,2 % | 5,09× |
| Precio a restaurantes −20 % | 651.878 | −62.091 | 123 | 46,9 % | 4,66× |
| Rider a 5 entregas/h | 703.212 | −10.757 | 123 | 50,1 % | 5,07× |
| Ticket medio 24 € (−17 %) | 706.068 | −7.901 | 148 | 50,2 % | 5,09× |
| Microhub a 1.000 €/mes | 707.969 | −6.000 | 123 | 50,3 % | 5,10× |
| Rampa de 36 meses | 713.969 | 0 | 123 | 50,1 % | 5,08× |
| Rotación 3 %/mes y captación 100 € | 710.425 | −3.544 | 123 | 50,5 % | 5,12× |
| Agosto a cero | 710.986 | −2.983 | 123 | 50,5 % | 5,14× |
| 4 min/bandeja (dato de la hoja de costes) | 653.354 | −60.615 | 123 | 47,8 % | 4,77× |

La palanca solo llega hasta ~7 %: por encima, el techo de 175 restaurantes manda y subirla no añade nada (la hoja Restaurantes lo avisa en la fila 70). Para ir más allá habría que ampliar zonas o subir la penetración, y eso habría que justificarlo con datos de los primeros meses.

---

## 7. Puntos a validar antes de enseñarlo

1. **Tarifa a restaurantes.** Es la tarifa «facilitada» de la hoja de costes. Es lo que más mueve la línea: −20 % de precio son −62 k€ de EBITDA. Conviene confirmarla con 10-20 restaurantes reales antes del roadshow.
2. **Ritmo de captación.** El caso base llega a 62 restaurantes en el mes 12 (~5 nuevos al mes). Nico va solo hasta que entra el KAM (mes 20) y en el mes 19 tendría ~97 restaurantes, al límite de los 100 por comercial (fila 210), además de la distribución. Si la rampa se cumple, habría que adelantar el KAM o meter a una persona de restauración.
3. **Microhub a 500 €/mes** en Salamanca/Chamberí. Es el «supuesto actual» de MICROHUB_COSTES. Si cuesta 1.000 €, el EBITDA baja 6 k€.
4. **Riders autónomos.** Hay riesgo de falso autónomo (horario fijo, un solo cliente, herramientas de la empresa). El modelo ya usa 16 €/h de coste empresa, que equivale a contratarlos por cuenta ajena a tiempo parcial, así que regularizarlos no cambia las cifras. Recomendación: contrato laboral o empresa de reparto.
5. **Minutos por bandeja.** Base 3 min (con lavadora + cinta). La hoja de costes usa 4 min: −61 k€ de EBITDA.
6. **Rendimientos y días de luz.** La hoja de costes trae datos distintos a los del socio de producción (p. ej. rúcula 120 g y 3 días frente a 170 g y 4 días; mostaza 120 g/3 d frente a 160 g/4 d; brócoli 150 g/3 d frente a 170 g/4 d). El V17 mantiene los del socio (V16). Hay que unificar.
7. **Capacidad actual.** La hoja de costes dice 4 racks × 32 = 128 bandejas en el local; el V16 usa 96. Solo afecta al mensaje de «capacidad actual» del deck.
8. **Porte de 12 € a pedidos menores de 35 €.** Está desactivado (`Restaurantes!D29 = 0`). Es una palanca al alza: si lo pagara el segmento «mínimo», serían hasta ~79 k€/año, con riesgo de perder clientes.
9. **Valor de salida.** El retorno del inversor sigue dependiendo del múltiplo de 6× EBITDA a la salida del mes 48.

---

## 8. Cómo mover la palanca

- `Restaurantes!D7`: % de la nave para restaurantes (0 % = solo distribución).
- `Restaurantes!C9:E9`: meses de rampa por escenario (36 / 24 / 18).
- `Restaurantes!D12`: penetración máxima (30 %) y `D10`: activar/desactivar el techo.
- `Restaurantes!C36:E36`: entregas por hora por escenario (5 / 7 / 8).
- `Restaurantes!C26:E26`: índice de precio a restaurantes (90 / 100 / 110 %).
- Las filas 65-70 de la hoja Restaurantes enseñan al momento cuántos restaurantes, riders y qué % de kilos e ingresos implica la palanca.

Para regenerar el modelo desde el V16: `python3 scripts/modelo_v17.py modelo/Rootflow_Modelo_Financiero_V17.xlsx` y recalcular con LibreOffice.
