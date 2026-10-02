# Deck V17 — cambios sobre tu V15_1 (ES) y V15_EN

> 02/10/2026 · Cifras del modelo **V17** (`modelo/Rootflow_Modelo_Financiero_V17.xlsx`), escenario base salvo que se diga otra cosa.
> Partimos de **tus** decks (`deck/fuentes/`) y solo se tocan las cifras y los textos que dependen del modelo. El diseño no cambia.
> Regenerar: `python3 deck/build/mapa_zonas.py es mapa.png` y luego `python3 deck/build/editar_deck_v17.py es deck/fuentes/Rootflow_Deck_Inversores_V15_1.pptx mapa.png salida.pptx <skill pptx>` (igual con `en`).

Si en el otro chat has cambiado alguna de estas diapositivas, esta es la lista exacta para cruzarlo.

## Diapositivas nuevas (16 y 17, tras «El salto»)

| # | Título | Qué cuenta |
|---|---|---|
| 16 | **Una nave, dos formas de vender.** | Línea 1 · Distribución (el volumen: 1,38 M€, 95 % de los kilos, 44 €/kg) y Línea 2 · Restaurantes (el margen: 345 k€, 123 restaurantes, 2 pedidos/semana, ticket de 28,93 €, 2 riders, microhub, 173 €/kg). Barras de kilos (95/5) e ingresos (80/20). Margen por kilo ×4,4 (120 frente a 27 €/kg). La palanca: el % de restaurantes sale de la distribución. |
| 17 | **Ocho barrios, un microhub, dos riders.** | Mapa de Madrid con Ríos Rosas, Trafalgar, Almagro, Castellana, Lista, Justicia, Recoletos y Goya, y los **585 restaurantes abiertos reales** del censo municipal como puntos. Ranking por barrio, objetivo de 123 restaurantes (1 de cada 5), ~40 entregas al día, 4,4 € de última milla por pedido (15 % del ticket). |

El mapa usa la capa pública de barrios de Madrid y el Censo de locales del Ayuntamiento (epígrafe 561001, locales abiertos). La capa de barrios venía desplazada unos 125 m respecto al censo y se ha corregido. 27 de los 585 puntos (5 %) quedaban en el borde de su barrio y se han encajado dentro para dibujarlos. Los recuentos no cambian.

## Diapositivas actualizadas

| # | Diapositiva | Antes (V15) | Ahora (V17) |
|---|---|---|---|
| 1 | Portada | Septiembre 2026 | Octubre 2026 |
| 11 | Producción y capacidad | Rábano 3 + 2 días · 15 ciclos/mes; cilantro 6 + 9; albahaca 6 + 12; capacidad actual ~160 kg/mes, pico ~350 | Rábano 3 + 3 · 10 ciclos/mes; cilantro 5 + 10; albahaca 5 + 13; **~120 kg/mes, pico ~240** (rendimientos medidos por producción) |
| 15 | El salto | ~2.900 kg/mes en régimen | **~3.100 kg/mes**; el texto ya menciona a los restaurantes de las zonas calientes |
| 18 | La ronda | TIR 35 % · MOIC 3,3× · necesidad 161.278 € · cobertura 1,24× · DSCR 11,4× | **TIR 51 % · MOIC 5,2× · necesidad 173.048 € · cobertura 1,16× · DSCR mínimo 15,9×**. Reparto: 64.800 nave · 65.008 colchón · 24.440 licencias, legal y contingencia · 18.800 automatización, microhub y fianzas |
| 19 | Proyección | 183 k€ → 1,30 M€; EBITDA −52 k€ → 460 k€; margen 35 % | **248 k€ · 900 k€ · 1,37 M€ · 1,68 M€ · 1,72 M€**; EBITDA **−30 · 309 · 553 · 716 · 714 k€**; margen **−12 · 34 · 40 · 43 · 42 %**. Rango de margen 27 % (cons.) a 53 % (opt.) |
| 20 | Escenarios | TIR 10,7 / 35,1 / 53,2 %; MOIC 1,50× (suelo) / 3,33× / 5,51×; precio 100/120/135 %; coste 100/85/75 % | **TIR 28,2 / 50,7 / 66,6 %; MOIC 2,70× / 5,16× / 7,70×**; equity a la salida 2,70 / 5,16 / 7,70 M€; ingresos 1,45 / 1,72 / 1,98 M€; EBITDA 389 k€ (27 %) / 714 k€ (42 %) / 1,05 M€ (53 %); **precio 90/100/110 %; coste 105/100/90 %**. El suelo de 1,5× ya no se activa en ningún caso |
| 21 | Palancas | «Mix premium»: flores y variedades de alto valor | Añade el peso de los restaurantes |
| 22 | Estructura | Cobra 150 k€ (suelo) / 333 k€ / 551 k€ | **270 k€ (2,7×) / 516 k€ (5,2×) / 770 k€ (7,7×)** |
| 23 | Visión | «Siguiente paso: hubs urbanos…» | «Ya en el plan: microhub en Salamanca, Chamberí y Centro, con riders» |

## Lo que conviene revisar antes de enviarlo

- **TIR del 51 % en el caso base.** Es lo que da el modelo con salida en el mes 48 a 6× EBITDA. Un inversor lo va a descontar. Sugerencia: mostrar también el conservador (28 %) en la conversación, no solo en la diapositiva 20.
- **La mejora del V17 viene de los restaurantes.** Sin la línea de restaurantes, con las tarifas reales y sin los ajustes optimistas del V16, el EBITDA del año 5 es el mismo que en el V16 (546 k€ frente a 544 k€). Ver `modelo/REVISION_V17.md` §5.
- **Tarifa a restaurantes (173 €/kg de media).** Es la tarifa «facilitada» de la hoja de costes. Conviene validarla con restaurantes reales antes del roadshow (−20 % de precio son −62 k€ de EBITDA).
- **El logo del deck en inglés** dice «Microbrotes y flores comestibles» (viene de tu imagen original; no se ha tocado).
