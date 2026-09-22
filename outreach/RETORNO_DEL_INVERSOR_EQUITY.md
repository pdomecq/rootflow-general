# Retorno del inversor con entrada en capital — recálculo

> 21/09/2026. **ACTUALIZADO: las cifras de este documento eran estimaciones; ya están verificadas
> recalculando el Modelo V15.** Los números definitivos están en `OPCIONES_ESTRUCTURA_ENISA.md` y en
> `modelo/Rootflow_Modelo_Financiero_V15_equity.xlsx`.
>
> **Resultado final (escenario Base, 10 % del capital, salida en el año 4, suelo 1,5×):**
> **TIR 35,1 % · MOIC 3,33× · valor del equity a la salida 3.330.103 € · cobro del inversor 333.010 €.**
> Conservador: 10,7 % · 1,50×. Optimista: 53,2 % · 5,51×. DSCR mínimo 6,78×.
>
> Este documento conserva el razonamiento —por qué el plazo importa más que el porcentaje— que sigue siendo válido.
> **Esto es un análisis de estructuración, no asesoramiento financiero ni legal.**

---

## 1. Por qué hay que rehacer el número

El V14 promete **TIR 33 %, MOIC 2,39x y payback a 33 meses**. Esos tres números salen del tramo **participativo**: el inversor cobraba intereses desde el primer año, y por eso el dinero volvía pronto.

Con entrada en capital y **dividendos bloqueados hasta amortizar ENISA**, el inversor **no cobra nada hasta la salida**. El retorno pasa a depender de dos cosas y solo dos: **cuánto vale la empresa al salir** y **cuándo sale**.

No es un matiz. Es otro producto.

---

## 2. Cuánto vale la empresa al salir

Valor = EBITDA × múltiplo + caja. Cifras del V14 Base:

| Salida | EBITDA | 5x | 6x | 7x | 8x |
|---|---|---|---|---|---|
| Año 5 | 460.201 € | 2.939.341 € | 3.399.542 € | 3.859.743 € | 4.319.944 € |
| Año 6 | 430.665 € | 2.914.308 € | 3.344.973 € | 3.775.638 € | 4.206.303 € |
| Año 7 | 400.955 € | 3.367.449 € | 3.768.404 € | 4.169.359 € | 4.570.314 € |

> ✅ **Las dos incoherencias, resueltas y corregidas en el V15.**
>
> **1. El valor de salida no sumaba la caja.** Confirmado en la celda: el V14 calculaba `EBITDA año 5 × 6 = 2.761.205 €`, que es un *enterprise value*, y lo trataba como valor del equity. El V15 lo corrige a **EV + caja − deuda viva**, que en el caso base da **3.330.103 €** en el mes de salida.
>
> **2. El reparto "30 % cada socio" dejaba un 10 % suelto** mientras el kicker era del 2,5 %. Al fijar la participación del inversor en el 10 %, el 30 % por fundador **pasa a ser exactamente correcto** y la incoherencia desaparece sola.
>
> **3. Corrección a lo que dije antes:** el kicker sí estaba incluido en el retorno del inversor — se pagaba en el mes 84 (celda CH121). Lo que no incluía era la caja en el valor de salida.

---

## 3. Qué porcentaje hay que dar para cada TIR

Salida en año 7, sin dividendos intermedios:

| TIR objetivo | MOIC necesario | % con el valor del V14 | % con 6x + caja |
|---|---|---|---|
| 12 % | 2,21x | 8,0 % | 5,9 % |
| 15 % | 2,66x | 9,6 % | 7,1 % |
| **20 %** | **3,58x** | **13,0 %** | **9,5 %** |
| 25 % | 4,77x | 17,3 % | 12,7 % |
| 30 % | 6,27x | 22,7 % | 16,7 % |
| 33 % | 7,36x | 26,7 % | 19,5 % |

**Léelo despacio: replicar la TIR del 33 % con equity a 7 años exigiría darle entre el 19 y el 27 % de la compañía.** Eso no es dilución mínima, es otra empresa.

---

## 4. La palanca no es el porcentaje. Es el plazo

Mismo inversor, misma participación del 10 %, solo cambia cuándo sale:

| Salida | Valor total (6x + caja) | Vale su 10 % | MOIC | **TIR** |
|---|---|---|---|---|
| **Año 4** | 3.261.934 € | 326.193 € | 3,26x | **34,4 %** |
| **Año 5** | 3.399.542 € | 339.954 € | 3,40x | **27,7 %** |
| Año 6 | 3.344.973 € | 334.497 € | 3,34x | 22,3 % |
| Año 7 | 3.768.404 € | 376.840 € | 3,77x | 20,9 % |

**Con un 10 % y salida en el año 4-5 recuperas la TIR del 30 % largo.** Con el mismo 10 % y salida en el año 7, te quedas en el 21 %.

El participativo daba liquidez temprana vía cupón. Si lo quitas, la única forma de mantener el atractivo es **darle una puerta de salida temprana**.

---

## 5. La estructura que propongo, con números

> **~10 % del capital por 100.000 €** (valoración post implícita ≈ 1 M€)
> **+ derecho de salida pactado a partir del año 4**, a múltiplo acordado.

Por qué funciona:

- **TIR del 28-34 %** si la salida se ejecuta en el año 4-5 — en el mismo rango que prometía el participativo.
- **Los fundadores conservan el 90 %.** Control intacto, y por mucho margen.
- **Valoración post de ~1 M€**, que es *mucho* más defendible que los ~1,8 M€ que implicaba el kicker del 2,5 % sobre 45.000 € en una sociedad constituida en marzo de 2026. Este cambio te quita de encima la discusión más incómoda del roadshow.
- Cumple el requisito de fondos propios 1:1 de ENISA, que era el problema de origen.

**Lo que hay que resolver con el abogado:** cómo se instrumenta esa salida. Una opción de venta que obligue a los fundadores a comprar con su dinero es una carga personal y puede tener aspecto de deuda. Alternativas a estudiar: autocartera de la sociedad (con los límites de la LSC), compromiso de búsqueda de comprador, o derecho de arrastre condicionado a partir del año 4. **No es un detalle de redacción: cambia quién asume el riesgo.**

---

## 6. Qué puedes decir y qué no, a partir de ahora

| No digas | Di |
|---|---|
| "TIR del 33 %" | "TIR del 28-34 % con salida en el año 4-5, del 21 % si se alarga a 7" |
| "Payback 33 meses" | "Sin reparto hasta amortizar ENISA; la liquidez llega por la salida pactada" |
| "MOIC 2,39x" | "Entre 3,2x y 3,8x según el año de salida y el múltiplo" |
| "Dilución mínima, solo kicker" | "En torno al 10 %, con los fundadores conservando el 90 %" |

Y lo que **no ha cambiado** y sigue siendo tu mejor argumento: ingresos de 1,3 M€ y **EBITDA de 460 k€ (35 %)** en régimen, margen bruto del 74-77 %, **DSCR mínimo de 3,70x**, y el **77,5 % de los ingresos del Año 1 ya identificados en pipeline**. El negocio no ha cambiado. Solo cambia cómo cobra el inversor.

---

## 7. Cómo reproducir estos números

```bash
python3 scripts/retorno_equity.py
```

Las hipótesis están todas arriba del script y son editables: EBITDA y caja por año del V14 Base, importe de inversión y múltiplos de salida. Si cambias el escenario del modelo, cambia ahí las dos tablas y vuelve a correrlo.
