#!/usr/bin/env python3
"""Consolida los CSV de los agentes de búsqueda de inversores de Rootflow.

- Deduplica por nombre normalizado + dominio web.
- Fusiona informacion entre duplicados (gana el valor mas informativo).
- Cruza con el pipeline actual (seccion 7 del contexto) -> columna `estado`.
- Recalcula `tier` a partir de `score`.
- Genera CSV + XLSX multi-pestana.
"""
import csv, glob, os, re, sys, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "output")

COLS = ["id","entidad","tipo","subtipo","pais","ciudad","web","tesis_resumen",
        "evidencia_agro_food","ticket_min_eur","ticket_max_eur","instrumentos",
        "acepta_minoritario_sin_control","ultima_operacion_fecha","persona_contacto",
        "cargo","linkedin_url","email_publico","via_entrada","angulo_pitch","red_flags",
        "conflicto","score","tier","confianza","fuente_url_1","fuente_url_2",
        "fecha_verificacion","estado"]

# --- Pipeline actual (seccion 7 del contexto) --------------------------------
EN_CONVERSACION = ["primaflor","frutas eloy","garret","juan urquijo",
                   "las rozas innova","madrid food innovation hub"]
YA_IDENTIFICADOS = ["enisa","first drop vc","first drop","cdti","zubi capital","zubi",
    "lanzadera","covap","ship2b ventures","ship2b","bewater funds","bewater",
    "keiretsu forum","foro capital pymes","kaudal","caixabank","agrobank",
    "sego venture","sego finance","encomenda capital partners","encomenda",
    "growersgo","k fund","kfund","eoniq fund","eoniq","nazari ventures","nazari",
    "fundalogy","unicaja","wayra","ayming","cooperativa la palma","la palma",
    "bstartup","banco sabadell","treemond","asagra safefood","asagra","invertidos",
    "aaban","sherry ventures"]

LEGAL = r"\b(s\.?l\.?u?\.?|s\.?a\.?u?\.?|sociedad limitada|sociedad anonima|scr|sgeic|sicc|sl|sa|srl|ltd|llc|gmbh|bv|inc|corp|s\.?c\.?a\.?|sccl|coop|s\.?coop\.?)\b"

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

def norm_name(s):
    s = strip_accents((s or "").lower().strip())
    s = re.sub(r"[.,;:()\"'’`]", " ", s)
    s = re.sub(LEGAL, " ", s)
    s = re.sub(r"\b(grupo|group|the|family office|familyoffice|capital|partners|ventures|venture|fund|fondo|holding|holdings)\b", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def norm_domain(url):
    u = (url or "").strip().lower()
    if not u or u in ("-", "n/a", "desconocido", "na"):
        return ""
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = u.split("/")[0].split("?")[0].strip()
    return u if "." in u else ""

def info_score(v):
    """Cuanto 'aporta' un valor: se usa para elegir al fusionar duplicados."""
    v = (v or "").strip()
    if v in ("", "-", "desconocido", "desconocida", "n/a", "na", "none", "None"):
        return 0
    return len(v)

CONF_RANK = {"alta": 3, "media": 2, "baja": 1, "": 0}

def merge(a, b):
    """Fusiona dos filas. Gana el valor mas informativo campo a campo."""
    out = {}
    for c in COLS:
        va, vb = a.get(c, ""), b.get(c, "")
        if c == "score":
            try: out[c] = str(max(int(float(va or 0)), int(float(vb or 0))))
            except Exception: out[c] = va or vb
        elif c == "confianza":
            out[c] = va if CONF_RANK.get(va, 0) >= CONF_RANK.get(vb, 0) else vb
        elif c == "id":
            out[c] = "+".join(sorted({x for x in (va, vb) if x and x != "-"}))
        elif c in ("fuente_url_1", "fuente_url_2"):
            out[c] = va if info_score(va) else vb
        else:
            out[c] = va if info_score(va) >= info_score(vb) else vb
    # un conflicto detectado por cualquiera de los dos se conserva
    for c in ("conflicto",):
        vals = {a.get(c, ""), b.get(c, "")} - {"", "-", "ninguno"}
        if vals:
            out[c] = sorted(vals)[0]
    return out

def cruzar_pipeline(row):
    n = norm_name(row.get("entidad", ""))
    if not n:
        return row.get("estado", "nuevo") or "nuevo"
    for p in EN_CONVERSACION:
        pn = norm_name(p)
        if pn and (pn in n or n in pn):
            return "ya_en_pipeline"
    for p in YA_IDENTIFICADOS:
        pn = norm_name(p)
        if pn and (pn == n or (len(pn) > 4 and (pn in n or n in pn))):
            return "ya_identificado"
    return "nuevo"

def tier_de(score):
    try: s = int(float(score))
    except Exception: return "C"
    return "A" if s >= 75 else ("B" if s >= 55 else "C")

def main():
    files = sorted(glob.glob(os.path.join(OUT, "agente_*.csv")))
    if not files:
        sys.exit("No hay CSV de agentes en output/")
    raw, problemas = [], []
    for f in files:
        with open(f, encoding="utf-8-sig", newline="") as fh:
            rd = csv.DictReader(fh, delimiter=";")
            missing = [c for c in COLS if c not in (rd.fieldnames or [])]
            if missing:
                problemas.append(f"{os.path.basename(f)}: faltan columnas {missing}")
            n = 0
            for r in rd:
                row = {c: (r.get(c) or "").strip() for c in COLS}
                if not row["entidad"] or row["entidad"] == "-":
                    continue
                row["_origen"] = os.path.basename(f)
                raw.append(row); n += 1
            print(f"  {os.path.basename(f):42s} {n:4d} filas")

    print(f"\nTotal filas brutas: {len(raw)}")

    # --- Deduplicacion por nombre normalizado y por dominio -------------------
    by_key, order = {}, []
    dom_index, name_index = {}, {}
    for row in raw:
        nn, dom = norm_name(row["entidad"]), norm_domain(row["web"])
        key = None
        if dom and dom in dom_index:
            key = dom_index[dom]
        elif nn and nn in name_index:
            key = name_index[nn]
        if key is None:
            key = f"k{len(order)}"
            order.append(key); by_key[key] = row
        else:
            by_key[key] = merge(by_key[key], row)
        if dom: dom_index[dom] = key
        if nn: name_index[nn] = key

    rows = [by_key[k] for k in order]
    print(f"Entidades unicas tras deduplicar: {len(rows)}  (eliminados {len(raw)-len(rows)} duplicados)")

    # --- Cruce con pipeline + recalculo de tier ------------------------------
    for r in rows:
        r["estado"] = cruzar_pipeline(r)
        r["tier"] = tier_de(r["score"])
        if not r.get("fecha_verificacion") or r["fecha_verificacion"] == "-":
            r["fecha_verificacion"] = "2026-09-21"

    def sort_key(r):
        try: s = int(float(r["score"]))
        except Exception: s = 0
        return (-s, r["entidad"].lower())
    rows.sort(key=sort_key)

    # --- Salidas -------------------------------------------------------------
    csv_path = os.path.join(OUT, "inversores_rootflow_consolidado.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow(r)
    print(f"\nEscrito {csv_path}")

    # Estadisticas
    por_tier = defaultdict(int); por_tipo = defaultdict(int); por_estado = defaultdict(int)
    for r in rows:
        por_tier[r["tier"]] += 1; por_tipo[r["tipo"] or "-"] += 1; por_estado[r["estado"]] += 1
    print("\nPor tier:  " + "  ".join(f"{k}={v}" for k, v in sorted(por_tier.items())))
    print("Por estado: " + "  ".join(f"{k}={v}" for k, v in sorted(por_estado.items())))
    print("Por tipo:")
    for k, v in sorted(por_tipo.items(), key=lambda x: -x[1]):
        print(f"   {k:24s} {v}")
    if problemas:
        print("\nAVISOS:"); [print("  - " + p) for p in problemas]
    return rows

if __name__ == "__main__":
    main()
