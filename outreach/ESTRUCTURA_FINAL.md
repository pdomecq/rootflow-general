# Estructura final de la ronda — cerrada y verificada

> 22/09/2026 · Modelo **V15**, recalculado. Sustituye a `OPCIONES_ESTRUCTURA_ENISA.md`.
> Análisis de estructuración, no asesoramiento legal ni fiscal.

---

## 1. La estructura

| Concepto | Condición |
|---|---|
| Inversor privado | **100.000 € en capital** (ampliación con prima) |
| Participación | **10 %** · los fundadores conservan el **90 %** |
| Derecho de salida | A partir del **año 4** |
| Suelo de protección | **1,5×** sobre lo aportado |
| ENISA | 100.000 € · 84 meses · **carencia de 24 meses** |
| Instrumentación | Nota convertible en octubre → capitalizada antes de que ENISA formalice |

### Retorno del inversor (verificado recalculando el modelo)

| Escenario | TIR | MOIC | Valor del equity a la salida | Cobra |
|---|---|---|---|---|
| Conservador | **10,7 %** | 1,50× | 787.920 € | 150.000 € *(por el suelo)* |
| **Base** | **35,1 %** | **3,33×** | **3.329.273 €** | **332.927 €** |
| Optimista | **53,2 %** | 5,51× | 5.512.227 € | 551.223 € |

### Solidez del plan

| | Conservador | Base | Optimista |
|---|---|---|---|
| **DSCR mínimo (años 2-7)** | **2,42** | **11,43** | 16,46 |
| Caja mínima | 30.000 € | 30.000 € | 30.000 € |
| ¿Cumple el requisito de fondos propios de ENISA? | **Sí** | **Sí** | **Sí** |

---

## 2. Los cinco problemas y cómo quedaron

### 1. Desfase de caja hasta que llegue ENISA → **NO ERA UN PROBLEMA**
El análisis anterior asumía que ENISA desembolsaba meses después de la ampliación, lo que abría una pinza mortal. **Corregido: ENISA desembolsa a la semana de tener el capital.** Los fondos propios en el momento de formalizar son los 100.000 € íntegros, sin que las pérdidas hayan empezado a comérselos. **Cumple exactamente el requisito.**

> ⚠️ **La única condición que hay que respetar:** el margen es cero — 100.000 € aportados contra 100.000 € exigidos. Si por lo que sea pasa un mes entre la ampliación y la formalización, los fondos propios bajan a **83.801 €** y deja de cumplir. Mientras la semana se respete, no hay problema; si se alarga, hay que subir la aportación.

### 2. El derecho de salida del año 4 → **RESUELTO POR REDACCIÓN**
En el mes 48 quedan **61.667 €** de ENISA vivos. Una recompra por la sociedad reduciría fondos propios con el préstamo vivo. Por eso el derecho de salida se redacta como **búsqueda de comprador o derecho de arrastre**, nunca como opción de venta contra la sociedad ni contra los fundadores. El modelo ya lo trata así: el pago no toca la caja de la empresa.

### 3. DSCR que se hundía en los años 6 y 7 → **ARREGLADO, y era un error del modelo**

El V14 asumía una **carencia de 60 meses** en ENISA, lo que metía los 100.000 € de principal en solo 24 meses (4.167 €/mes) justo cuando el EBITDA conservador cae. Resultado: DSCR de 1,53 y **1,00**.

Pero las condiciones publicadas de ENISA dan **carencia de hasta 2 años**, no de 5. Los 60 meses del modelo no existían. Corregido a **24 meses**:

| Carencia | DSCR mínimo (conservador) |
|---|---|
| 12 meses | 0,81 ❌ *(empieza a amortizar durante la rampa)* |
| **24 meses** | **2,42** ✅ **óptimo** |
| 36 meses | 1,95 |
| 48 meses | 1,48 |
| 60 meses *(V14)* | **1,00** ❌ |

**El DSCR mínimo pasa de 1,00 a 2,42 en conservador y de 6,78 a 11,43 en base.** No cuesta nada: aprovecha la holgura de los años 2-5, que tenían DSCR de entre 3,8 y 19,8. Y no afecta al retorno del inversor.

> **Confirmar con la asesora:** plazo, carencia y periodicidad de amortización que ENISA aplica realmente a la línea AgroInnpulso. Sus condiciones publicadas hablan de hasta 7 años, hasta 2 de carencia y amortización **trimestral** (el modelo la calcula mensual — diferencia menor).

### 4. Capital social descuadrado → **ARREGLADO**
`D81` decía 50.000 € con una ronda que aporta 100.000 €. Ahora es **100.030 €** (los 100.000 € de la ronda más los 30 € de capital fundacional). Es la hipótesis conservadora para la reserva legal: si estructuráis con prima de emisión alta, el nominal será menor y la reserva legal más pequeña, lo que solo ayuda.

### 5. Todo el dinero entra en el mes 1 → **CORRECTO, no se toca**
Confirmado que privado y ENISA entran a la vez. El modelo ya lo refleja.

---

## 3. Qué cambia respecto a lo que decía el V14

| | V14 (participativo) | **V15 (capital)** |
|---|---|---|
| Instrumento | Préstamo participativo + kicker 2,5 % | **Capital, 10 %** |
| TIR base | 33,0 % | **35,1 %** |
| MOIC base | 2,39× | **3,33×** |
| TIR conservador | 16,3 % | 10,7 % *(peor)* |
| Liquidez del inversor | Cupón desde el año 1 | Un cobro en el año 4 *(peor)* |
| DSCR mínimo base | 3,70 | **11,43** |
| DSCR mínimo conservador | 0,42 | **2,42** |
| Carencia ENISA | 60 meses *(no existe)* | **24 meses** |
| ¿Cumple ENISA? | **No** | **Sí** |

---

## 4. Lo que queda pendiente

1. **Confirmar con la asesora** el plazo y la carencia reales de AgroInnpulso, y que la formalización va de verdad a una semana de la ampliación.
2. **Cuadrar el cap table** pre y post: el 10 % implica una valoración post de 1 M€. Decidir el reparto nominal/prima.
3. **Redactar el derecho de salida** como búsqueda de comprador o arrastre. Que lo escriba un mercantilista.
4. **Decidir si el suelo es 1,5×** o negociable. Sin él, el inversor pierde dinero en conservador (TIR −6,0 %); con él gana 10,7 %, y en base y optimista **no cuesta nada**.
5. **Meter la facturación real 2026** en el modelo y en el deck.

---

## 5. Reproducir

```bash
# importe · pre-money · ENISA · mes salida · mes formalización · suelo · carencia ENISA · destino
python3 scripts/modelo_a_equity.py 100000 900000 100000 48 0 1.5 24 modelo/mi_version.xlsx
```

En `Hipótesis`: `D92` importe · `D104` ENISA · `D109` carencia · `D119` % inversor · `D124` mes de salida · `D126` mes de formalización · `D127` suelo. La fila **165** de cada hoja mensual dice si cumple ENISA y cuánto falta.
