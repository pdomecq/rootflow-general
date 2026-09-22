# Opciones de estructura que cumplen con ENISA

> ⚠️ **DOCUMENTO SUPERADO — 22/09/2026.** Partía de que ENISA desembolsaba meses después de la
> ampliación, lo que abría una pinza que en realidad no existe: **ENISA desembolsa a la semana de
> tener el capital**. Con eso, la estructura de 100.000 € al 10 % cumple sin necesidad de levantar más.
> **La estructura cerrada está en `ESTRUCTURA_FINAL.md`.** Esto se conserva solo como registro del
> análisis de sensibilidad sobre el importe de la ronda.

> Todas verificadas **recalculando el modelo V15**, no estimadas. 21/09/2026.
> Requisito que manda sobre todo lo demás: **fondos propios ≥ importe solicitado a ENISA.**
> Análisis de estructuración, no asesoramiento legal ni fiscal.

---

## 1. El problema, en una tabla

Los 100.000 € entran como capital, pero **las pérdidas del Año 1 se los comen deprisa**. Fondos propios en el momento de formalizar ENISA:

| Mes | Resultado acumulado | Fondos propios | ¿Cubre 100 k€ de ENISA? |
|---|---|---|---|
| **0** (antes de arrancar el gasto) | 0 € | **100.000 €** | **Sí, justo** |
| 1 | −16.199 € | 83.801 € | No |
| 2 | −31.369 € | 68.631 € | No |
| 3 | −44.457 € | 55.543 € | No |
| 6 | −76.619 € | 23.381 € | No |
| **9** (peor momento) | −86.102 € | **13.898 €** | No |
| 12 | −73.116 € | 26.884 € | No |

**La ventana es estrechísima.** Si ENISA formaliza incluso un mes después de que arranque el gasto de la nave, el expediente deja de cumplir. Esto no es un detalle: es el riesgo principal de toda la operación.

---

## 2. Las tres estructuras que SÍ cumplen

| | **A · La elegida** | **D · Colchón** | **E · ENISA reducido** |
|---|---|---|---|
| Capital del inversor | 100.000 € | 150.000 € | 100.000 € |
| **% del inversor** | **10,0 %** | 14,3 % | **10,0 %** |
| Importe ENISA | 100.000 € | 100.000 € | **80.000 €** |
| Total levantado | 200.000 € | 250.000 € | 180.000 € |
| Cobertura sobre 161.278 € | 1,24× | 1,55× | 1,12× |
| Fondos propios al formalizar | **100.000 €** | 105.543 € | 83.868 € |
| **¿Cumple ENISA?** | **Sí, sin margen** | **Sí, con margen** | **Sí, con margen** |
| TIR del inversor (base) | **35,1 %** | 33,9 % | **35,1 %** |
| MOIC (base) | **3,33×** | 3,22× | **3,33×** |
| DSCR mínimo | 6,78× | 6,78× | **8,20×** |
| Fundadores conservan | **90 %** | 85,7 % | **90 %** |

### A · La que has elegido — 10 % por 100.000 €
Funciona, **pero solo si ENISA formaliza antes de que arranque el gasto de la nave.** Fondos propios exactamente 100.000 € contra 100.000 € exigidos: cero margen. Cualquier retraso, cualquier gasto adelantado, y deja de cumplir.
**Condición operativa:** inscribir la ampliación en el Registro y formalizar ENISA **antes** de firmar la nave o pedir el CAPEX.

### D · Colchón — 150.000 € de capital
La más segura. Sobran 5.543 € incluso formalizando en el mes 3, así que absorbe retrasos. **Cuesta 4,3 puntos más de dilución** (14,3 % en vez de 10 %) y obliga a convencer a un inversor de poner 150.000 € o a sindicar dos tickets.

### E · ENISA reducido — pedir 80.000 € en vez de 100.000 €
**Mi recomendación como plan B, y casi como plan A.** Mantiene intacto lo que has decidido (10 % por 100.000 €), cumple con margen aunque formalices en el mes 1, y **mejora el DSCR a 8,20×**. El precio: 20.000 € menos de financiación total, con cobertura que baja a 1,12× sobre la necesidad — sigue cubriendo el plan, pero con menos colchón de caja.

---

## 3. Las que NO cumplen — para que no se propongan por error

| | Capital | ENISA | Formaliza | Fondos propios | Resultado |
|---|---|---|---|---|---|
| B | 100.000 € | 100.000 € | mes 3 | 55.543 € | **Faltan 44.457 €** |
| C | 130.000 € | 100.000 € | mes 3 | 85.543 € | **Faltan 14.457 €** |
| F | 130.000 € | 100.000 € | mes 3, salida año 5 | 85.543 € | **Faltan 14.457 €** |

La C es la trampa: parece prudente levantar 130.000 € en vez de 100.000 €, y **aun así no cumple** si ENISA formaliza en el mes 3. El problema no se arregla solo con más dinero: se arregla con **secuencia**.

---

## 4. El suelo de protección — la pieza que hace vendible el caso conservador

Sin protección, con equity puro el inversor **pierde dinero en el escenario conservador**: el valor del equity a la salida sería de 779.834 €, su 10 % son 77.983 €, sobre 100.000 € aportados. **TIR del −6,0 %.** Con el participativo ganaba un 16,3 %. Es la primera objeción que te van a poner.

Se resuelve con un **suelo de cobro de 1,5×**: el inversor cobra el mayor de su 10 % del valor o 1,5× lo aportado.

| Escenario | Sin suelo | **Con suelo 1,5×** | Coste para vosotros |
|---|---|---|---|
| Conservador | −6,0 % · 0,78× | **+10,7 % · 1,50×** | 72.017 € |
| Base | 35,1 % · 3,33× | **35,1 % · 3,33×** | **0 €** |
| Optimista | 53,2 % · 5,51× | **53,2 % · 5,51×** | **0 €** |

**En base y en optimista no cuesta absolutamente nada.** Solo paga si el plan sale mal, que es exactamente cuando el inversor necesita la protección. Es la concesión con mejor relación coste-beneficio de toda la estructura, y ya está metida en el modelo V15.

En el conservador el valor del equity (779.834 €) cubre de sobra los 150.000 €, así que el suelo es pagable en los tres escenarios.

---

## 5. Comparación honesta con lo que prometía el participativo

| | Participativo (V14) | **Capital 10 % + suelo 1,5× (V15)** |
|---|---|---|
| TIR conservador | 16,3 % | 10,7 % · *peor* |
| **TIR base** | 33,0 % | **35,1 % · mejor** |
| TIR optimista | 43,8 % | **53,2 % · mejor** |
| MOIC base | 2,39× | **3,33× · mejor** |
| Liquidez | Cupón desde el año 1 | Un solo cobro en el año 4 · *peor* |
| DSCR mínimo | 3,70× | **6,78× · mejor** |
| ¿Cumple ENISA? | **No** | **Sí** |

El capital es **mejor en base y en optimista, y peor en conservador y en liquidez**. Ese es el intercambio real, y conviene contarlo así: un inversor que detecte que se lo maquillas dejará de creerte el resto.

---

## 6. Qué preguntar a la asesora — en este orden

1. **¿Sobre qué fecha de balance mide ENISA los fondos propios?** ¿La del último cierre, la de la solicitud, o la de la formalización? **De esto depende que la opción A sea viable o no.** Es la pregunta más importante de todas.
2. ¿Cuánto tiempo pasa realmente entre resolución favorable y formalización? Determina cuánto se puede retrasar el gasto de la nave.
3. ¿Admite ENISA una **nota convertible** firmada en octubre y capitalizada antes de formalizar? ¿Qué documentación exige para acreditar la conversión?
4. Si pedimos **80.000 € en vez de 100.000 €** (opción E), ¿cambia algo del expediente aparte del importe?
5. ¿Las **cuentas en participación** computan como fondos propios, como deuda, o son indiferentes? Decide si sirven como tramo adicional por encima del capital.

---

## 7. Cómo reproducir cualquiera de estas opciones

```bash
# importe · pre-money · ENISA · mes de salida · mes de formalización · suelo · destino
python3 scripts/modelo_a_equity.py 100000 900000 100000 48 0 1.5 modelo/mi_opcion.xlsx
bash scripts/barrido_opciones.sh    # compara las seis de golpe
```

El modelo entregado (`modelo/Rootflow_Modelo_Financiero_V15_equity.xlsx`) viene configurado con la **opción A**. En la hoja `Hipótesis` puedes cambiar a mano: `D92` importe, `D104` ENISA, `D119` % del inversor, `D124` mes de salida, `D126` mes de formalización y `D127` suelo. La fila **165** de cada hoja mensual te dice si cumple o no, y cuánto falta.
