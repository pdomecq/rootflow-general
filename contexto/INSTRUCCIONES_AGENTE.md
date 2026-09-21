# Instrucciones comunes para todos los agentes de búsqueda

## Antes de empezar
1. Carga las herramientas web: `ToolSearch` con query `select:WebSearch,WebFetch`.
2. Lee `contexto/ROOTFLOW_CONTEXTO.md` y `contexto/BRIEF_AGENTES_INVERSORES.md` completos.

## Reglas de oro (INVIOLABLES)
1. **Nada inventado.** Cada fila lleva >=1 URL real que respalde existencia y tesis. Si no puedes verificar -> `confianza=baja` o descarta. NUNCA inventes una entidad, un ticket, una participada ni una fecha.
2. **Sin emails adivinados.** Solo emails genéricos publicados (info@, inversiones@). Nada de nombre.apellido@. RGPD.
3. **Solo personas públicas y profesionales** (socio, director de inversiones, responsable de innovación). Nada de datos personales privados.
4. **No contactes a nadie.** No rellenes formularios, no te registres en plataformas. Solo investigación.
5. **Actividad reciente:** prioriza entidades con operaciones documentadas desde septiembre 2024. Anota la fecha de la última evidencia.
6. **Honestidad de encaje:** un VC con ticket mínimo 500 k€ es encaje BAJO aunque sea famoso. Mejor 50 candidatos realistas que 200 imposibles.
7. **Busca en español Y en inglés.**
8. **No dupliques el pipeline** (sección 7 del contexto): si aparece, `estado=ya_en_pipeline` o `ya_identificado`, enriquece y sigue.
9. **Competidores:** marca `conflicto=competidor` (productores que ya venden microgreens). Pueden ser adquirentes estratégicos.

## Lo que busca Rootflow (criterios de encaje)
- **Ticket ideal 50–100 k€** (lead) / aceptable 20–50 k€ (sindicado). Descarta mínimos >250 k€ salvo industrial/CVC flexible.
- **Instrumento:** préstamo participativo + equity kicker ~2,5 %; cuentas en participación; revenue share; deuda subordinada; equity minoritario pequeño.
- **Líneas rojas:** sin cesión de control, sin avales personales, dilución mínima.
- **Sector:** agro, hortofrutícola, food, HORECA/foodservice, CEA/vertical farming, impacto, agua, agtech.
- **Fase:** seed / primeras ventas.
- **Geografía:** Madrid > España > extranjero con inversiones en España.
- **Velocidad:** CRÍTICO. Term sheet objetivo 31/10/2026 (~6 semanas). Prioriza quien decide en semanas (angels, family offices, industriales) sobre fondos con comités de 4+ meses.

## Argumentos de venta verificados (Modelo V14, escenario Base)
- Ronda 200 k€ = 100 k€ privado + 100 k€ ENISA (en curso con asesora). Necesidad 161.278 € -> cobertura 1,24x.
- TIR inversor 33,0 % · MOIC 2,39x · payback 33 meses · DSCR mínimo 3,70.
- **77,5 % de los ingresos del Año 1 ya identificados en pipeline** (141.474 € de 182.509 €).
- Ingresos: Año 1 182,5 k€ -> Año 3 1,03 M€ -> Año 5 1,30 M€ con EBITDA 460 k€ (35,3 %).
- Capacidad actual 160 kg/mes -> 2.937 kg/mes tras el salto de nave (x18).
- Precio medio directo 39,32 €/kg. Margen bruto 74-77 %.
- Escenario conservador (4 min/bandeja, EBITDA 11 %): TIR aún 16,3 %, MOIC 1,47x.
- Apalancamiento público ~1:1: los fondos propios del inversor desbloquean ENISA y SAECA.

## Esquema CSV EXACTO (UTF-8, separador `;`, una fila por entidad)
Cabecera literal, en este orden:
```
id;entidad;tipo;subtipo;pais;ciudad;web;tesis_resumen;evidencia_agro_food;ticket_min_eur;ticket_max_eur;instrumentos;acepta_minoritario_sin_control;ultima_operacion_fecha;persona_contacto;cargo;linkedin_url;email_publico;via_entrada;angulo_pitch;red_flags;conflicto;score;tier;confianza;fuente_url_1;fuente_url_2;fecha_verificacion;estado
```
- `id`: `A{tu_numero}-{nnn}` (ej. A3-017)
- `tipo`: industrial_agro | cadena_valor | family_office | angel | red_angels | crowdfunding | vc | cvc | impacto | venture_debt | deuda_alternativa | publico_coinversor | aceleradora | banca
- `ticket_min_eur`/`ticket_max_eur`: número o `desconocido`
- `instrumentos`: equity | participativo | deuda | CeP | revenue_share | desconocido (varios con `|`)
- `acepta_minoritario_sin_control`: si | no | desconocido
- `ultima_operacion_fecha`: AAAA-MM
- `via_entrada`: evento | intro_calida | formulario_web | email_generico | red_angels | desconocida
- `conflicto`: ninguno | competidor | cliente_actual
- `confianza`: alta | media | baja
- `estado`: nuevo | ya_en_pipeline | ya_identificado
- `fecha_verificacion`: 2026-09-21
- **IMPORTANTE:** ningún campo de texto puede contener `;` ni saltos de línea. Usa comas. Si un campo está vacío pon `-`.

## Scoring (0–100)
| Dimensión | Peso | Cómo puntuar |
|---|---|---|
| Encaje ticket e instrumento | 30 | 30 = hace 20–100 k€ y acepta participativo/CeP/minoritario; 0 = solo >500 k€ o exige control |
| Encaje sectorial | 25 | 25 = agro/food/HORECA/CEA con cartera o negocio demostrable; 0 = sin relación |
| Valor estratégico | 15 | 15 = aporta canal, clientes o capacidad operativa; 0 = solo dinero |
| Geografía | 10 | 10 = Madrid; 6 = resto de España; 2 = extranjero con operaciones en España |
| Actividad reciente | 10 | 10 = operación en últimos 12 meses; 5 = 12–24 meses; 0 = sin evidencia |
| Accesibilidad y velocidad | 10 | 10 = decisión rápida y vía de entrada clara; 0 = proceso largo y cerrado |

**Tiers:** A >= 75 · B 55–74 · C < 55. Sé estricto: un tier A tiene que ser alguien a quien llamarías mañana.

## Entrega
- Escribe tu CSV en `/home/user/rootflow-general/output/agente_N_<segmento>.csv`.
- Escríbelo con un heredoc de bash o con Python (csv module, delimiter=';'). Verifica al final que el nº de columnas por fila es 29 en todas las filas.
- Devuelve en tu informe final: nº de filas, desglose por tier, y tus 5 mejores hallazgos con una frase cada uno.
