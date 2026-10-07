# Rootflow — Mapa de inversores para la ronda

Trabajo de identificación y priorización de inversores para la ronda de Rootflow
Hydroponics (100 k€ privados + 100 k€ ENISA). **Confidencial — uso interno.**

## Estructura

| Carpeta | Contenido |
|---|---|
| `contexto/` | Contexto de compañía, brief de investigación e instrucciones de los agentes |
| `output/` | CSV por segmento, consolidado y Excel con el Top 30 |
| `outreach/` | Proceso de roadshow, plantillas de email y guía de condiciones |
| `scripts/` | Consolidación, deduplicación y generación del Excel |

## Cómo regenerar los entregables

```bash
python3 scripts/consolidar.py      # deduplica y cruza con el pipeline
python3 scripts/generar_xlsx.py    # genera el Excel multi-pestaña
```

## Entregables principales

- `output/inversores_rootflow_consolidado.xlsx` — Portada, Top 30, Consolidado,
  una pestaña por segmento, Descartados, Seguimiento y Fuentes.
- `output/RESUMEN.md` — Top 30 comentado, jugadas destacadas y huecos detectados.
- `outreach/PROCESO_ROADSHOW.md` — embudo, gating de información y guion de visita.
- `outreach/PLANTILLAS_EMAIL.md` — plantillas por segmento y secuencia de seguimiento.
- `outreach/CONDICIONES_Y_NEGOCIACION.md` — oferta base, líneas rojas y escalera de concesiones.

## Agente de inversores (pitches y seguimiento)

- **Dónde se ve el seguimiento:** en Notion, página «Ronda Rootflow · Inversores». Contiene la base «Pipeline de inversores» con 345 entidades y las vistas Tablero, Para revisar, Agenda, En conversación y Embudo. Ahí también está el «Parte diario del agente».
- **Qué hace cada mañana laborable:**
  1. Lee Gmail y actualiza el estado de cada inversor.
  2. Prepara pitches y seguimientos para el visto bueno.
  3. Envía solo lo que está en «Aprobado».
  4. Deja el parte del día.
- **Instrucciones del agente:** `.claude/skills/ronda-inversores/`.
  - `SKILL.md`: el proceso.
  - `config.md`: IDs, límites y firma.
  - `datos.md`: las únicas cifras que puede usar, del modelo V17 y el ERP.
  - `plantillas.md`: los mensajes, que sustituyen a `outreach/PLANTILLAS_EMAIL.md` (V14).
- **Envío:** solo cuando el Gmail conectado es `p.domecq@rootflow.es` (Google Workspace) y el interruptor «Envío» de la página de Notion está en ACTIVADO.
- **Lanzarlo a mano:** pide «pasada de inversores» en una sesión de Claude Code con este repositorio.
