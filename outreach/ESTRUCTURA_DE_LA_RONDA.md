# Estructura de la ronda — sustituir el préstamo participativo

> Revisión del 21/09/2026, tras la objeción de la asesora de ENISA.
> Confidencial, uso interno. **Esto es análisis de estructuración, no asesoramiento legal ni fiscal.**
> Valídalo con la asesora de ENISA y con un mercantilista antes de firmar nada.

---

## 1. Por qué ENISA rechaza el participativo privado — el motivo exacto

No es una manía del analista. Son dos reglas de ENISA que chocan de frente con el diseño actual de la ronda:

**Regla 1 — Fondos propios ≥ importe solicitado.** ENISA exige, en sus propias condiciones, que el solicitante tenga **fondos propios iguales o superiores al importe del préstamo**. Para 100.000 € de ENISA hacen falta **100.000 € de fondos propios**, no 48.000 €.

**Regla 2 — Los participativos de terceros no cuentan como fondos propios.** Un préstamo participativo es deuda en el balance, aunque tenga efectos mercantiles especiales. ENISA solo admite participativos, notas convertibles o préstamos puente de terceros **si se capitalizan de forma inminente e irrevocable, y están totalmente convertidos e inscritos en el momento de formalizar el préstamo de ENISA**.

**La consecuencia para el plan actual.** Si el inversor entra con 55.000 € en participativo y solo 45.000 € en capital, ese participativo no suma a fondos propios: sales con ~48.000 € de fondos propios pidiendo 100.000 € de ENISA. **El expediente no cumple.** Y encima el participativo privado compite en servicio de deuda con el propio ENISA, lo que empeora el DSCR que ENISA analiza.

La objeción de tu asesora, traducida: *el participativo privado no te resta un poco, te rompe el requisito central del expediente.*

> **Aviso adicional sobre el calendario contable:** los fondos propios se miran en el momento de formalizar, y **las pérdidas acumuladas los reducen**. Tu Año 1 tiene un EBITDA de −52 k€. Si quemas caja antes de que ENISA formalice, los 100.000 € de capital pueden haberse convertido en 80.000 € de fondos propios y volver a incumplir. Levanta con colchón, o secuencia el gasto para llegar a la formalización con el balance intacto.

---

## 2. La estructura que propongo

**Los 100.000 € del inversor entran íntegramente como CAPITAL: ampliación de capital con prima de emisión.**

No es un parche, es lo que hace que el expediente funcione:

| Efecto | Resultado |
|---|---|
| Fondos propios | ~100.000 € → **cumple el 1:1 de ENISA exactamente** |
| Instrumento que molesta a ENISA | Desaparece |
| Servicio de deuda que compite con ENISA | Desaparece → mejora el DSCR |
| Control de los fundadores | **Intacto** (ver punto 3) |
| Dilución | **Sube. Es el precio real de esta decisión.** |

Hay que decirlo claro: **el coste de cumplir con ENISA es aceptar más dilución que el "solo kicker" del plan original.** No hay forma de tener las dos cosas. Lo que sí se puede es blindar todo lo demás.

---

## 3. Tu línea roja de control no está en peligro — y conviene entenderlo bien

El préstamo participativo se eligió, entre otras cosas, para no ceder control. Pero con estos números **el control nunca estuvo en riesgo**: sois tres fundadores y un inversor minoritario que entra con 100.000 €. Aunque la dilución sea del 8, del 12 o del 15 %, seguís teniendo **más del 85 % y los tres asientos**.

El control se protege por **aritmética**, no por ingeniería de instrumento. Lo que de verdad hay que blindar en el pacto de socios es que el minoritario no adquiera **derechos de veto** sobre la operativa. Eso es redacción, no estructura.

### Si aun así queréis blindaje formal: participaciones sin voto

La Ley de Sociedades de Capital permite a una SL crear **participaciones sociales sin derecho de voto** por un nominal no superior a la mitad del capital (art. 98). El inversor tendría economía pero **cero votos**.

**Pero tiene una trampa que encaja fatal con ENISA, y hay que saberla antes de proponerla:** el art. 99 da a esas participaciones un **dividendo mínimo** fijado en estatutos, y **si ese dividendo mínimo no se paga, las participaciones recuperan temporalmente el derecho de voto**. Como ENISA te bloquea los dividendos hasta amortizar, el dividendo mínimo no se pagaría... y el inversor recuperaría el voto justo durante los años en que menos te conviene.

Se puede redactar para evitarlo (definiendo el dividendo mínimo como variable y condicionado a que exista beneficio distribuible y a que no haya restricción contractual a la distribución), pero **eso lo tiene que escribir un mercantilista**, no una plantilla. Si no quieres esa complejidad, quédate con participaciones ordinarias y protección por aritmética.

---

## 4. Lo que le das al inversor a cambio de quitarle el participativo

El participativo le daba al inversor **protección de bajada**: cobraba intereses pasara lo que pasara. Si se lo quitas, tienes que compensarle con derechos económicos y contractuales. Esto es lo que sustituye al participativo, ordenado de más barato a más caro para ti:

| Concesión | Qué es | Coste para ti |
|---|---|---|
| **Reporting reforzado** | Informe mensual, acceso al ERP, reunión trimestral | Cero. Dáselo de entrada. |
| **Preferencia de liquidación 1x no participativa** | En una venta, recupera su dinero antes que nadie; luego reparto normal | Cero si va bien. Es la pieza que más tranquiliza y menos cuesta. |
| **Antidilución weighted average** | Si hay ronda a la baja, se ajusta su precio | Bajo. **Nunca full ratchet.** |
| **Dividendo preferente diferido** | Derecho preferente al dividendo, **activable solo tras amortizar ENISA** | Bajo, y encaja con el bloqueo de ENISA en vez de chocar con él |
| **Tag-along** | Si vendéis, él vende en las mismas condiciones | Bajo |
| **Derecho de salida pactado** | Opción de compra por los fundadores a partir del año 4-5, a múltiplo pactado | Medio. Es lo más parecido a la "devolución" del participativo. |
| **Observador sin voto en el consejo** | Asiste, no vota | Medio. Última concesión. |

**Nunca:** veto sobre operativa, mayoría, drag-along a favor del inversor, ni avales personales.

---

## 5. El truco de calendario: nota convertible para llegar al 31/10

Aquí hay una tensión práctica. Una ampliación de capital exige junta, escritura pública ante notario e inscripción en el Registro Mercantil. **Eso no se cierra en las seis semanas que te quedan hasta el term sheet, y menos con negociación de valoración de por medio.**

La salida es la que el propio ENISA admite expresamente:

1. **Octubre — firmas una nota convertible** con el inversor. Rápida, es un contrato privado, no necesita notario ni Registro, y **te permite aplazar la pelea de valoración** (se fija un descuento o un techo y listo). Con esto cumples tu hito del 31/10.
2. **Noviembre / diciembre — conversión obligatoria e irrevocable** en ampliación de capital con prima. Junta, escritura, inscripción en el Registro Mercantil.
3. **Después — ENISA formaliza**, con la ampliación ya inscrita y los fondos propios en balance.

Esto es exactamente lo que ENISA pide: admite la nota convertible **siempre que esté totalmente convertida e inscrita en el momento de formalizar**. Y ENISA no desembolsa hasta recibir la escritura inscrita, así que el orden es obligatorio de todas formas.

**La nota convertible tiene que ser de conversión obligatoria, no opcional.** Si el inversor puede elegir no convertir, sigue siendo deuda y vuelves al problema de origen.

---

## 6. Lo que hay que cambiar en el discurso

Lo que decías antes y lo que dices ahora:

| Antes | Ahora |
|---|---|
| "Préstamo participativo con interés fijo y variable + kicker del 2,5 %" | "Entrada en capital con prima de emisión, preferencia de liquidación 1x y antidilución" |
| "Tu retorno viene del participativo" | "Tu retorno viene del valor de la participación y del derecho de salida pactado" |
| "Dilución mínima, solo kicker" | "Participación minoritaria real, con los fundadores manteniendo más del 85 %" |
| "TIR del 33 %" | **Hay que recalcular.** La TIR del 33 % del modelo V14 está calculada sobre el tramo participativo. Con equity puro, el retorno depende del valor de salida, no del cupón. |

> **Esto es lo más urgente del documento.** El Modelo V14 calcula TIR, MOIC y payback asumiendo préstamo participativo. Si cambias el instrumento, **esos tres números dejan de ser válidos** y no puedes seguir enseñándolos. Hay que rehacer el cálculo del retorno del inversor en base a equity antes de la primera reunión seria. El resto del modelo (ingresos, EBITDA, DSCR, caja) no se toca: solo cambia el tramo de financiación y el retorno al inversor.

---

## 7. Preguntas a la asesora de ENISA, esta semana

Llévale estas cinco y tendrás la estructura cerrada:

1. ¿Confirmas el requisito de fondos propios ≥ importe solicitado para la línea **AgroInnpulso** en concreto, y sobre qué fecha de balance se mide?
2. Si formalizamos con 100.000 € de capital pero arrastramos pérdidas del Año 1, **¿qué cifra de fondos propios computa**: la aportada o la neta de pérdidas? ¿Cuánto colchón recomiendas?
3. ¿Admitís una **nota convertible** firmada en octubre y capitalizada en diciembre? ¿Qué documentación exigís para acreditar la conversión?
4. ¿Cómo tratáis las **cuentas en participación**? ¿Computan como fondos propios, como deuda, o son indiferentes?
5. ¿Hay algún problema con que parte del capital entre como **participaciones sin voto** (art. 98 LSC)?

La respuesta a la 4 decide si podéis usar cuentas en participación como tramo adicional de circulante **por encima** de los 100.000 € de capital — que es donde tendría sentido, no dentro.

---

## 8. Resumen en cinco líneas

- El participativo privado no es que no guste: **rompe el requisito de fondos propios de ENISA.**
- Los 100.000 € del inversor deben entrar **como capital**, con prima de emisión.
- Eso cuesta **más dilución**. No hay alternativa que cumpla y no diluya.
- El **control no corre peligro**: seguís con más del 85 % entre los tres.
- Firma en octubre una **nota convertible obligatoria** y capitalízala antes de que ENISA formalice.
