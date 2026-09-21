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
