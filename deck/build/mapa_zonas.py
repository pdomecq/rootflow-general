"""Mapa de las 8 zonas calientes de reparto con los restaurantes abiertos del censo municipal.

Uso: python3 mapa_zonas.py <es|en> <salida.png>
Datos: datos/restaurantes_zonas.json (Censo de locales del Ayto. de Madrid, epígrafe 561001, abiertos)
       y la capa pública de barrios de Madrid (se descarga si no está).
"""
import json, math, os, sys, urllib.request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.patches import Polygon, FancyArrowPatch
from shapely.geometry import shape
from pyproj import Transformer

BG, LINE, TXT = "#FCF1ED", "#D8C9BE", "#3A453F"
GREEN, GREEN_L, ORANGE, MUTED = "#1D4F37", "#D8ECDF", "#ED7E1F", "#8A827B"
plt.rcParams["font.family"] = "Liberation Sans"

LANG, SALIDA = sys.argv[1], sys.argv[2]
AQUI = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(AQUI, "datos", "madrid_barrios.geojson")
if not os.path.exists(GEO):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/madrid.geojson", GEO)
geo = json.load(open(GEO))
zonas = {"Justicia", "Recoletos", "Castellana", "Goya", "Trafalgar", "Almagro", "Rios Rosas", "Lista"}
etiqueta = {"Rios Rosas": "Ríos Rosas"}
cens = json.load(open(os.path.join(AQUI, "datos", "restaurantes_zonas.json")))
tr = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)
from shapely.geometry import Point
from shapely.ops import nearest_points
_alias = {"RIOS ROSAS": "Rios Rosas"}
_polys = {f["properties"]["name"]: shape(f["geometry"]) for f in geo["features"]}
# La capa de barrios pública está desplazada ~125 m E / 130 m N respecto al censo (ETRS89);
# se corrige el desplazamiento y los puntos que siguen fuera de su barrio se encajan dentro.
_k = 111320 * math.cos(math.radians(40.43))
pts, encajados = [], 0
for x, y, b in cens["pts"]:
    lon, lat = tr.transform(x, y)
    p = Point(lon + 125 / _k, lat + 130 / 110570)
    pg = _polys[_alias.get(b, b.title())]
    if not pg.contains(p):
        interior = pg.buffer(-0.00018)
        p = nearest_points(interior, p)[0]; encajados += 1
    pts.append((p.x, p.y))
print("encajados", encajados)

LON0, LAT0 = -3.692, 40.432
KX, KY = math.cos(math.radians(LAT0)) * 111.32, 110.57
P = lambda lon, lat: ((lon - LON0) * KX, (lat - LAT0) * KY)

W_IN, H_IN = 5.6, 4.25
fig = plt.figure(figsize=(W_IN, H_IN), dpi=300)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
fig.patch.set_alpha(0); ax.patch.set_alpha(0)
# encuadre (km): ancho/alto = W_IN/H_IN
cx, cy, hh = 0.2, 0.05, 2.45
hw = hh * W_IN / H_IN
ax.set_xlim(cx - hw, cx + hw); ax.set_ylim(cy - hh, cy + hh); ax.set_aspect("equal")

def anillos(geom):
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for pg in polys:
        yield [P(*c[:2]) for c in pg.exterior.coords]

centros = {}
for f in geo["features"]:
    n = f["properties"]["name"]; g = shape(f["geometry"])
    z = n in zonas
    for ring in anillos(g):
        ax.add_patch(Polygon(ring, closed=True, facecolor=GREEN_L if z else "#F7E8E1",
                             edgecolor=GREEN if z else LINE, linewidth=1.1 if z else 0.5, zorder=2 if z else 1))
    if z:
        rp = g.representative_point(); centros[n] = P(rp.x, rp.y)

xs, ys = zip(*[P(lon, lat) for lon, lat in pts])
ax.scatter(xs, ys, s=7, color=ORANGE, edgecolors=BG, linewidths=0.35, zorder=4, alpha=0.95)

ajuste = {"Justicia": (0.0, 0.0), "Recoletos": (0.0, 0.0), "Castellana": (0.0, 0.0), "Goya": (0.0, 0.0),
          "Trafalgar": (0.07, 0.0), "Almagro": (0.0, 0.0), "Rios Rosas": (0.0, 0.0), "Lista": (0.0, 0.0)}
for n, (x, y) in centros.items():
    dx, dy = ajuste.get(n, (0, 0))
    ax.text(x + dx, y + dy, etiqueta.get(n, n).upper(), ha="center", va="center", fontsize=7.0, fontweight="bold",
            color=GREEN, zorder=6, path_effects=[pe.withStroke(linewidth=2.4, foreground=GREEN_L)])

# escala 1 km
x0, y0 = cx - hw + 0.25, cy - hh + 0.3
ax.plot([x0, x0 + 1], [y0, y0], color=TXT, lw=1.4, solid_capstyle="butt", zorder=7)
for xx in (x0, x0 + 1):
    ax.plot([xx, xx], [y0 - 0.05, y0 + 0.05], color=TXT, lw=1.0, zorder=7)
ax.text(x0 + 0.5, y0 + 0.1, "1 km", ha="center", va="bottom", fontsize=6.5, color=TXT, zorder=7)
# norte
nx, ny = cx + hw - 0.3, cy + hh - 0.55
ax.add_patch(FancyArrowPatch((nx, ny), (nx, ny + 0.35), arrowstyle="-|>", mutation_scale=8, color=TXT, lw=1, zorder=7))
ax.text(nx, ny - 0.1, "N", ha="center", va="top", fontsize=6.5, fontweight="bold", color=TXT, zorder=7)
# lanzadera desde la nave (sur)
ax.add_patch(FancyArrowPatch((0.9, cy - hh + 0.05), (0.55, -1.25), arrowstyle="-|>", mutation_scale=11,
                             color=GREEN, lw=1.6, linestyle=(0, (3, 2)), zorder=7))
ax.text(1.0, cy - hh + 0.35, ("Lanzadera diaria\ndesde la nave (sur)" if LANG == "es" else "Daily shuttle from\nthe facility (south)"), ha="left", va="center", fontsize=6.4,
        color=GREEN, fontweight="bold", zorder=7, path_effects=[pe.withStroke(linewidth=2.2, foreground=BG)])
fig.savefig(SALIDA, dpi=300, transparent=True)
print("ok", len(pts))
