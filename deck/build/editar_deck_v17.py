#!/usr/bin/env python3
"""Deck V17: parte del deck V15_1 del equipo y aplica las cifras del modelo V17.

- Actualiza las diapositivas con cifras (operación, nave, ronda, proyección,
  escenarios, palancas, estructura, visión y portada).
- Añade dos diapositivas tras «El salto»: las dos líneas de negocio y el mapa de
  zonas calientes de reparto a restaurantes.

Uso: python3 editar_deck_v17.py <es|en> <deck_origen.pptx> <mapa.png> <salida.pptx> <ruta_skill_pptx>
El deck inglés (V15_EN) tiene la misma estructura; solo cambian los textos.
"""
import re, sys, shutil, subprocess, zipfile, os, tempfile

LANG, SRC, MAPA, OUT, SKILL = sys.argv[1:6]
ES = LANG == "es"
IDIOMA = "es-ES" if ES else "en-US"
EMU = 914400
VERDE, VERDE2, NARANJA, TEXTO, GRIS = "1D4F37", "2C5F47", "ED7E1F", "3A453F", "8A827B"
CREMA, LINEA, VERDE_CLARO, VERDE_MEDIO, BLANCO = "FCF1ED", "E3D9D1", "D8ECDF", "9BC9AE", "FFFFFF"


# ---------------------------------------------------------------- utilidades XML
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def run(t, sz, color, b=False, i=False, spc=None):
    s = f' spc="{spc}"' if spc else ""
    return (f'<a:r><a:rPr lang="{IDIOMA}" sz="{int(sz * 100)}" b="{int(b)}" i="{int(i)}"{s} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="Arial"/></a:rPr>'
            f'<a:t xml:space="preserve">{esc(t)}</a:t></a:r>')


def para(runs, algn="l", ln=None, aft=None, bullet=None):
    ppr = f'<a:pPr algn="{algn}"'
    if bullet:
        ppr += ' marL="171450" indent="-171450"'
    ppr += ">"
    if ln: ppr += f'<a:lnSpc><a:spcPct val="{ln * 1000}"/></a:lnSpc>'
    if aft: ppr += f'<a:spcAft><a:spcPts val="{aft * 100}"/></a:spcAft>'
    if bullet:
        ppr += f'<a:buClr><a:srgbClr val="{bullet}"/></a:buClr><a:buFont typeface="Arial"/><a:buChar char="•"/>'
    ppr += "</a:pPr>"
    return f"<a:p>{ppr}{''.join(runs)}</a:p>"


def xfrm(x, y, w, h):
    return (f'<a:xfrm><a:off x="{round(x * EMU)}" y="{round(y * EMU)}"/>'
            f'<a:ext cx="{round(w * EMU)}" cy="{round(h * EMU)}"/></a:xfrm>')


def caja(i, name, x, y, w, h, paras, anchor="t", ins=(0, 0, 0, 0)):
    l, t, r, b = (round(v * EMU) for v in ins)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" anchor="{anchor}"/>'
            f'<a:lstStyle/>{"".join(paras) or "<a:p/>"}</p:txBody></p:sp>')


def forma(i, name, x, y, w, h, fill, line=None, adj=7000, paras=(), anchor="ctr", ins=(0, 0, 0, 0), prst="roundRect"):
    l, t, r, b = (round(v * EMU) for v in ins)
    relleno = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    ln = (f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line
          else "<a:ln><a:noFill/></a:ln>")
    geom = (f'<a:prstGeom prst="{prst}"><a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst></a:prstGeom>'
            if prst == "roundRect" else f'<a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}{geom}{relleno}{ln}</p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" anchor="{anchor}"/>'
            f'<a:lstStyle/>{"".join(paras) or "<a:p/>"}</p:txBody></p:sp>')


def imagen(i, name, rid, x, y, w, h, descr):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{name}" descr="{esc(descr)}"/>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


def span(xml, name):
    m = re.search(r'<p:(sp|pic|cxnSp)><p:nv\w+><p:cNvPr id="\d+" name="%s"[ />].*?</p:\1>' % re.escape(name), xml, re.S)
    assert m, f"no encuentro la forma {name}"
    return m.start(), m.end()


def en_forma(xml, name, fn):
    a, b = span(xml, name)
    return xml[:a] + fn(xml[a:b]) + xml[b:]


def textos(xml, name, cambios):
    """Sustituye el contenido exacto de <a:t> dentro de una forma (cada viejo debe aparecer una vez)."""
    def f(s):
        for viejo, nuevo in cambios:
            pat = r'(<a:t(?: [^>]*)?>)%s(</a:t>)' % re.escape(esc(viejo))
            assert len(re.findall(pat, s)) == 1, f"{name}: «{viejo}» no aparece una sola vez"
            s = re.sub(pat, lambda m: m.group(1) + esc(nuevo) + m.group(2), s)
        return s
    return en_forma(xml, name, f)


def geom(xml, name, x=None, y=None, w=None, h=None):
    def f(s):
        off = re.search(r'<a:off x="(\d+)" y="(\d+)"/>', s); ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>', s)
        nx = round(x * EMU) if x is not None else int(off.group(1)); ny = round(y * EMU) if y is not None else int(off.group(2))
        nw = round(w * EMU) if w is not None else int(ext.group(1)); nh = round(h * EMU) if h is not None else int(ext.group(2))
        s = s.replace(off.group(0), f'<a:off x="{nx}" y="{ny}"/>', 1)
        return s.replace(ext.group(0), f'<a:ext cx="{nw}" cy="{nh}"/>', 1)
    return en_forma(xml, name, f)


def quitar(xml, name):
    a, b = span(xml, name)
    return xml[:a] + xml[b:]


# ---------------------------------------------------------------- textos por idioma
def L(es, en): return es if ES else en


EDIT = {
 "slide1.xml": [("TextBox 8", [(L("SEPTIEMBRE 2026", "SEPTEMBER 2026"), L("OCTUBRE 2026", "OCTOBER 2026"))])],
 "slide10.xml": [
  ("TextBox 14", [(L("3 + 2 días", "3 + 2 days"), L("3 + 3 días", "3 + 3 days"))]),
  ("TextBox 15", [(L("15 ciclos/mes", "15 cycles/mo"), L("10 ciclos/mes", "10 cycles/mo"))]),
  ("TextBox 19", L([("6", "5"), (" + 9 días", " + 10 días")], [("6 + 9 days", "5 + 10 days")])),
  ("TextBox 24", L([("6", "5"), ("2", "3")], [("6 + 12 days", "5 + 13 days")])),
  ("TextBox 27", [L(("Estimación sobre 96 bandejas en luz simultánea (3 torres, 14,4 m² de cultivo) · mix comercial: 40% ciclo corto, 40% medio, 20% largo.",
                     "Estimación sobre 96 bandejas en luz simultánea (3 torres, 14,4 m² de cultivo) · mix de variedades del plan · rendimientos medidos por producción."),
                    ("Estimate based on 96 trays under light simultaneously (3 towers, 14.4 m² of growing surface) · commercial mix: 40% short cycle, 40% medium, 20% long.",
                     "Estimate based on 96 trays under light simultaneously (3 towers, 14.4 m² of growing surface) · planned variety mix · yields measured in production."))]),
  ("Rounded Rectangle 28", L([("~160 kg/", "~120 kg/"), (" de ~350 kg/", " de ~240 kg/")],
                             [("~160 kg/mo with a commercial variety mix  ·  peak of ~350 kg/mo in short-cycle monoculture",
                               "~120 kg/mo with a commercial variety mix  ·  peak of ~240 kg/mo in short-cycle monoculture")])),
 ],
 "slide13.xml": [
  ("TextBox 7", [L(("La capacidad de cultivo se multiplica por 30. En régimen, el plan prevé ~2.900 kg al mes con el mix comercial previsto: volumen suficiente para servir distribución a escala manteniendo el modelo de cosecha viva bajo pedido.",
                    "La capacidad de cultivo se multiplica por 30. En régimen, el plan prevé ~3.100 kg al mes: volumen para servir distribución a escala y abastecer a los restaurantes de las zonas calientes, sin renunciar a la cosecha viva bajo pedido."),
                   ("Growing capacity multiplies by 30. At full run-rate, the plan projects ~2,900 kg per month with the planned commercial mix: enough volume to serve distribution at scale while keeping the live, made-to-order model.",
                    "Growing capacity multiplies by 30. At full run-rate, the plan projects ~3,100 kg per month: enough volume to serve distribution at scale and supply restaurants in our hot zones, while keeping the live, made-to-order model."))]),
  ("Rounded Rectangle 11", [(L("~2.900 kg", "~2,900 kg"), L("~3.100 kg", "~3,100 kg"))]),
 ],
 "slide16.xml": [
  ("X612", [(L("35 %", "35%"), L("51 %", "51%"))]),
  ("X614", [(L("3,3×", "3.3×"), L("5,2×", "5.2×"))]),
  ("X610", [L(("Cubre la necesidad de 161.278 € del plan  ·  cobertura 1,24×", "Cubre la necesidad de 173.048 € del plan  ·  cobertura 1,16×"),
              ("Covers the plan's €161,278 need  ·  1.24× coverage", "Covers the plan's €173,048 need  ·  1.16× coverage"))]),
  ("X623", [L(("EN QUÉ SE INVIERTE  ·  161.278 €", "EN QUÉ SE INVIERTE  ·  173.048 €"), ("WHERE IT GOES  ·  €161,278", "WHERE IT GOES  ·  €173,048"))]),
  ("X631", [L(("62.608 €  ", "65.008 €  "), ("€62,608  ", "€65,008  "))]),
  ("X633", [L(("23.870 €  ", "24.440 €  "), ("€23,870  ", "€24,440  "))]),
  ("X635", [L(("10.000 €  ", "18.800 €  "), ("€10,000  ", "€18,800  ")),
            L(("Automatización", "Automatización, microhub y fianzas"), ("Automation", "Automation, microhub and deposits"))]),
  ("Rounded Rectangle 12", [L(("caja mínima de 30.000 €, DSCR de 11,4× (años 2-7) y circulante con póliza de crédito, no con la ronda.",
                               "caja mínima de 30.000 €, DSCR mínimo de 15,9× (años 2-7) y circulante con póliza de crédito, no con la ronda."),
                              ("€30,000 minimum cash, 11.4× DSCR (years 2–7), and working capital on a credit line — not the round.",
                               "€30,000 minimum cash, 15.9× minimum DSCR (years 2–7), and working capital on a credit line — not the round."))]),
 ],
 "slide17.xml": [
  ("TextBox 7", [L(("El Año 1 va en pérdidas (EBITDA −52 k€): es la nave llenándose y la plantilla entrando antes que los ingresos. A partir de ahí la facturación sube cliente a cliente hasta el régimen: ~1,30 M€ y un 35 % de margen EBITDA.",
                    "El Año 1 va en pérdidas (EBITDA −30 k€): es la nave llenándose y la plantilla entrando antes que los ingresos. A partir de ahí la facturación sube cliente a cliente —distribución y restaurantes— hasta el régimen: ~1,72 M€ y un 42 % de margen EBITDA."),
                   ("Year 1 runs at a loss (−€52K EBITDA): the facility is filling and the team arrives before the revenue does. From there, revenue climbs client by client to full run-rate: ~€1.30M and a 35% EBITDA margin.",
                    "Year 1 runs at a loss (−€30K EBITDA): the facility is filling and the team arrives before the revenue does. From there, revenue climbs client by client — distribution and restaurants — to full run-rate: ~€1.72M and a 42% EBITDA margin."))]),
 ] + [(n, [(L(a, c), L(b, d))]) for n, a, b, c, d in (
      ("X706", "183 k€", "248 k€", "€183K", "€248K"), ("X711", "686 k€", "900 k€", "€686K", "€900K"),
      ("X716", "1,03 M€", "1,37 M€", "€1.03M", "€1.37M"), ("X721", "1,27 M€", "1,68 M€", "€1.27M", "€1.68M"),
      ("X726", "1,30 M€", "1,72 M€", "€1.30M", "€1.72M"),
      ("X708", "−52 k€", "−30 k€", "−€52K", "−€30K"), ("X713", "191 k€", "309 k€", "€191K", "€309K"),
      ("X718", "350 k€", "553 k€", "€350K", "€553K"), ("X723", "468 k€", "716 k€", "€468K", "€716K"),
      ("X728", "460 k€", "714 k€", "€460K", "€714K"),
      ("X709", "−28 %", "−12 %", "−28%", "−12%"), ("X714", "28 %", "34 %", "28%", "34%"), ("X719", "34 %", "40 %", "34%", "40%"),
      ("X724", "37 %", "43 %", "37%", "43%"), ("X729", "35 %", "42 %", "35%", "42%"))] + [
  ("TextBox 27", [L(("Escenario base del modelo financiero V15 · régimen pleno en el año 5: nave llena y plantilla de 9 · cifras sin IVA, sujetas al cierre de cada ejercicio.",
                     "Escenario base del modelo financiero V17 · régimen pleno en el año 5: nave llena, 123 restaurantes y plantilla de 9 · cifras sin IVA, sujetas al cierre de cada ejercicio."),
                    ("Base case from financial model V15 · full run-rate in year 5: facility full, team of 9 · figures ex-VAT, subject to year-end close.",
                     "Base case from financial model V17 · full run-rate in year 5: facility full, 123 restaurants, team of 9 · figures ex-VAT, subject to year-end close."))]),
  ("Rounded Rectangle 28", [L(("las palancas —minutos por bandeja, precio y coste— llevan el margen EBITDA en régimen del 11% (conservador) al 50% (optimista).",
                               "las palancas —minutos por bandeja, precio, coste y peso de los restaurantes— llevan el margen EBITDA en régimen del 27 % (conservador) al 53 % (optimista)."),
                              ("the levers — minutes per tray, pricing, and cost — drive run-rate EBITDA margin from 11% (conservative) to 50% (optimistic).",
                               "the levers — minutes per tray, pricing, cost and restaurant share — drive run-rate EBITDA margin from 27% (conservative) to 53% (optimistic)."))]),
 ],
 "slide20.xml": [
  ("X402", [L(("El Base es el plan de negocio. Cambiar una sola palanca —los minutos por bandeja, el precio o la automatización— recalcula plantilla, EBITDA, caja y retorno del inversor.",
               "El Base es el plan de negocio. Cambiar una sola palanca —los minutos por bandeja, el precio, la automatización o el peso de los restaurantes— recalcula plantilla, EBITDA, caja y retorno del inversor."),
              ("Base is the business plan. Changing a single lever — minutes per tray, price, or automation — recomputes headcount, EBITDA, cash, and the investor's return.",
               "Base is the business plan. Changing a single lever — minutes per tray, price, automation or restaurant share — recomputes headcount, EBITDA, cash, and the investor's return."))]),
 ] + [(n, [(L(a, c), L(b, d))]) for n, a, b, c, d in (
      ("X405", "10,7 %", "28,2 %", "10.7%", "28.2%"), ("X408", "1,50×", "2,70×", "1.50×", "2.70×"),
      ("X409", "MOIC · POR EL SUELO", "MOIC", "MOIC · FLOOR", "MOIC"), ("X410", "0,79 M€", "2,70 M€", "€0.79M", "€2.70M"),
      ("X412", "1,03 M€", "1,45 M€", "€1.03M", "€1.45M"), ("X414", "115 k€ · 11 %", "389 k€ · 27 %", "€115K · 11%", "€389K · 27%"),
      ("X419", "35,1 %", "50,7 %", "35.1%", "50.7%"), ("X422", "3,33×", "5,16×", "3.33×", "5.16×"),
      ("X424", "3,33 M€", "5,16 M€", "€3.33M", "€5.16M"), ("X426", "1,30 M€", "1,72 M€", "€1.30M", "€1.72M"),
      ("X428", "460 k€ · 35 %", "714 k€ · 42 %", "€460K · 35%", "€714K · 42%"),
      ("X432", "53,2 %", "66,6 %", "53.2%", "66.6%"), ("X435", "5,51×", "7,70×", "5.51×", "7.70×"),
      ("X437", "5,51 M€", "7,70 M€", "€5.51M", "€7.70M"), ("X439", "1,52 M€", "1,98 M€", "€1.52M", "€1.98M"),
      ("X441", "757 k€ · 50 %", "1,05 M€ · 53 %", "€757K · 50%", "€1.05M · 53%"),
      ("X451", "100 %", "90 %", "100%", "90%"), ("X452", "120 %", "100 %", "120%", "100%"), ("X453", "135 %", "110 %", "135%", "110%"),
      ("X455", "100 %", "105 %", "100%", "105%"), ("X456", "85 %", "100 %", "85%", "100%"), ("X457", "75 %", "90 %", "75%", "90%"))] + [
  ("Rounded Rectangle 28", [L(("en el caso conservador el inversor cobra 1,5× —150.000 € por sus 100.000 €— aunque el plan se quede corto. En base y optimista el suelo no cuesta nada.",
                               "garantiza al inversor un mínimo de 1,5× —150.000 € por sus 100.000 €— aunque el plan se quede corto. Con el plan actual no llega a activarse en ninguno de los tres casos."),
                              ("in the conservative case the investor still receives 1.5× — €150,000 on €100,000 invested — even if the plan falls short. In base and optimistic, the floor costs nothing.",
                               "guarantees the investor at least 1.5× — €150,000 on €100,000 invested — even if the plan falls short. Under the current plan it is not triggered in any of the three cases."))]),
 ],
 "slide21.xml": [("TextBox 15", [L(("Más peso de flores comestibles y variedades de alto valor por kilo: sube el ticket medio sin subir el coste de producción.",
                                     "Más peso de restaurantes, flores comestibles y variedades de alto valor por kilo: sube el ingreso por bandeja sin subir el coste de producción."),
                                    ("More edible flowers and high-value-per-kilo varieties: raises the average ticket without raising production cost.",
                                     "More restaurants, edible flowers and high-value-per-kilo varieties: raises revenue per tray without raising production cost."))])],
 "slide23.xml": [("X962", L([("Siguiente paso: ", "Ya en el plan: "),
                             ("hubs urbanos en Salamanca, Chamberí y centro, con riders para la última milla.",
                              "microhub en Salamanca, Chamberí y Centro, con riders para la última milla.")],
                            [("Next step: ", "Already in the plan: "),
                             ("urban hubs in Salamanca, Chamberí and the center, with riders for the last mile.",
                              "a microhub in Salamanca, Chamberí and the center, with riders for the last mile.")]))],
}
COBROS = [("X819", "X820", 270, L("150 k€  ·  1,5× por el suelo", "€150K  ·  1.5× from the floor"), L("270 k€  ·  2,7×", "€270K  ·  2.7×")),
          ("X822", "X823", 516, L("333 k€  ·  3,3×", "€333K  ·  3.3×"), L("516 k€  ·  5,2×", "€516K  ·  5.2×")),
          ("X825", "X826", 770, L("551 k€  ·  5,5×", "€551K  ·  5.5×"), L("770 k€  ·  7,7×", "€770K  ·  7.7×"))]
MARCO = dict(cab=L("HOJA DE RUTA · HITO 3", "ROADMAP · MILESTONE 3"), ante=L("HACIA DÓNDE VAMOS", "WHERE WE'RE HEADED"),
             t1=L("El salto: de 58 m² a ", "The leap: from 58 m² "), t2=L("una nave de 350 m².", "to a 350 m² facility."),
             lema=L("Crecimiento ordenado, financiado con cabeza.", "Orderly growth, financed with discipline."),
             b1=L("Concebida para automatizarse por fases:  ", "Designed to automate in phases:  "),
             b2=L("sensórica y control de clima y riego, con datos en tiempo real integrados en nuestro ERP.",
                  "climate and irrigation sensing and control, with real-time data flowing into our ERP."))
pct = lambda v: L(f"{v} %", f"{v}%")

# ---------------------------------------------------------------- preparación
tmp = tempfile.mkdtemp()
d = os.path.join(tmp, "u")
zipfile.ZipFile(SRC).extractall(d)
S = os.path.join(d, "ppt", "slides")
add = os.path.join(SKILL, "scripts", "add_slide.py")
subprocess.run([sys.executable, add, d, "slide13.xml", "--after", "slide13.xml"], check=True, capture_output=True)
subprocess.run([sys.executable, add, d, "slide13.xml", "--after", "slide24.xml"], check=True, capture_output=True)


def leer(n): return open(os.path.join(S, n), encoding="utf-8").read()
def escribir(n, x): open(os.path.join(S, n), "w", encoding="utf-8").write(x)


# ---------------------------------------------------------------- textos de las diapositivas existentes
for fichero, cambios in EDIT.items():
    x = leer(fichero)
    for forma_, pares in cambios:
        x = textos(x, forma_, pares)
    escribir(fichero, x)

# ---------------------------------------------------------------- geometría (igual en los dos idiomas)
x = leer("slide16.xml")                                   # en qué se invierte: 173.048 €
partidas = [64800, 65008, 24440, 18800]
x0 = 0.85
for nombre, p in zip(("X624", "X625", "X626", "X627"), partidas):
    w = 11.42 * p / sum(partidas); x = geom(x, nombre, x=x0, w=w); x0 += w + 0.06
x = geom(x, "X635", w=2.73)
escribir("slide16.xml", x)

x = leer("slide17.xml")                                   # barras de ingresos, misma escala visual
ingresos = [248408, 899516, 1372473, 1682448, 1720250]
for (b, lab), v in zip((("X705", "X706"), ("X710", "X711"), ("X715", "X716"), ("X720", "X721"), ("X725", "X726")), ingresos):
    h = 1.05 * v / max(ingresos)
    x = geom(x, b, y=4.92 - h, h=h); x = geom(x, lab, y=4.92 - h - 0.26)
escribir("slide17.xml", x)

x = leer("slide22.xml")                                   # qué cobra el inversor
for b, lab, v, viejo, nuevo in COBROS:
    w = 6.84 * v / 770
    x = geom(x, b, w=w); x = geom(x, lab, x=2.3 + w + 0.14); x = textos(x, lab, [(viejo, nuevo)])
escribir("slide22.xml", x)


# ---------------------------------------------------------------- marco de las nuevas
def marco(n, cabecera, antetitulo, t1, t2, lema, quitar_banda=False):
    x = leer(n)
    for nombre in ("TextBox 7", "Rounded Rectangle 8", "Rounded Rectangle 9", "Rounded Rectangle 10", "Rounded Rectangle 11"):
        x = quitar(x, nombre)
    if quitar_banda:
        x = quitar(x, "Rounded Rectangle 12")
    x = textos(x, "TextBox 3", [(MARCO["cab"], cabecera)])
    x = textos(x, "TextBox 5", [(MARCO["ante"], antetitulo)])
    x = textos(x, "TextBox 6", [(MARCO["t1"], t1), (MARCO["t2"], t2)])
    x = textos(x, "TextBox 15", [(MARCO["lema"], lema)])
    return x


def insertar(x, formas):
    return x.replace("</p:spTree>", "".join(formas) + "</p:spTree>", 1)


# ---------------------------------------------------------------- nueva A · dos líneas
x = marco("slide24.xml", L("MODELO DE NEGOCIO", "BUSINESS MODEL"), L("DOS LÍNEAS DE NEGOCIO", "TWO BUSINESS LINES"),
          L("Una nave, ", "One facility, "), L("dos formas de vender.", "two ways to sell."),
          L("Volumen y margen, desde la misma nave.", "Volume and margin, from the same facility."))
x = textos(x, "Rounded Rectangle 12", [(MARCO["b1"], L("La palanca:  ", "The lever:  ")),
    (MARCO["b2"], L("el % de la nave para restaurantes sale de la distribución. La nave no produce más: vende mejor.",
                    "the share of the facility sold to restaurants comes out of distribution. Output doesn't grow: it sells better."))])
f, i = [], 100
def card(x0, oscuro, etiqueta, palabra, cifra, pie, puntos):
    global i
    fondo, borde = (VERDE, None) if oscuro else (BLANCO, LINEA)
    c_pal, c_cif, c_pie, c_txt, c_bul = ((CREMA, CREMA, VERDE_MEDIO, VERDE_CLARO, NARANJA) if oscuro
                                         else (VERDE, VERDE, GRIS, TEXTO, NARANJA))
    out = [forma(i, f"Línea {etiqueta}", x0, 2.5, 5.66, 2.25, fondo, borde, adj=6000)]
    out.append(caja(i + 1, f"Etiqueta {etiqueta}", x0 + 0.28, 2.7, 3.4, 0.2, [para([run(etiqueta, 9.5, NARANJA, b=True, spc=200)])]))
    out.append(caja(i + 2, f"Palabra {etiqueta}", x0 + 0.28, 2.95, 3.3, 0.42, [para([run(palabra, 20, c_pal, b=True)])]))
    out.append(caja(i + 3, f"Cifra {etiqueta}", x0 + 3.6, 2.7, 1.8, 0.7,
                    [para([run(cifra, 22, c_cif, b=True)], algn="r"), para([run(pie, 8, c_pie, b=True, spc=100)], algn="r")]))
    out.append(caja(i + 4, f"Puntos {etiqueta}", x0 + 0.28, 3.55, 5.1, 1.1,
                    [para([run(p, 11.5, c_txt)], ln=110, aft=3, bullet=c_bul) for p in puntos]))
    i += 5
    return out
f += card(0.85, False, L("LÍNEA 1  ·  DISTRIBUCIÓN", "LINE 1  ·  DISTRIBUTION"), L("El volumen", "Volume"),
          L("1,38 M€", "€1.38M"), L("INGRESOS · AÑO 5", "REVENUE · YEAR 5"), L([
    "Distribuidores, retail y Mercamadrid: clientes ya identificados y nuevas cuentas.",
    "Tarifa mayorista: 44 €/kg de media.",
    "Furgoneta propia en Madrid y Athos para el resto de España."], [
    "Distributors, retail and Mercamadrid: identified clients and new accounts.",
    "Wholesale price list: €44/kg on average.",
    "Own van in Madrid; Athos for the rest of Spain."]))
f += card(6.82, True, L("LÍNEA 2  ·  RESTAURANTES", "LINE 2  ·  RESTAURANTS"), L("El margen", "Margin"),
          L("345 k€", "€345K"), L("INGRESOS · AÑO 5", "REVENUE · YEAR 5"), L([
    "123 restaurantes en 8 zonas calientes de Madrid.",
    "Dos pedidos por semana · ticket medio de 28,93 €.",
    "Reparto con 2 riders desde un microhub refrigerado.",
    "Tarifa restaurante: 173 €/kg de media."], [
    "123 restaurants across 8 hot zones in Madrid.",
    "Two orders a week · average ticket of €28.93.",
    "Delivered by 2 riders from a refrigerated microhub.",
    "Restaurant price list: €173/kg on average."]))
f.append(caja(i, "Pie barras", 0.85, 4.93, 4.5, 0.2, [para([run(L("AÑO 5  ·  ESCENARIO BASE", "YEAR 5  ·  BASE CASE"), 8.5, GRIS, b=True, spc=150)])])); i += 1
f.append(forma(i, "Leyenda distribución", 5.95, 4.97, 0.12, 0.12, VERDE, prst="rect")); i += 1
f.append(caja(i, "Texto leyenda distribución", 6.12, 4.93, 1.2, 0.2, [para([run(L("Distribución", "Distribution"), 8.5, TEXTO)])])); i += 1
f.append(forma(i, "Leyenda restaurantes", 7.35, 4.97, 0.12, 0.12, NARANJA, prst="rect")); i += 1
f.append(caja(i, "Texto leyenda restaurantes", 7.52, 4.93, 1.3, 0.2, [para([run(L("Restaurantes", "Restaurants"), 8.5, TEXTO)])])); i += 1
for k, (lab, pd_, pr_) in enumerate(((L("Kilos vendidos", "Kilos sold"), 94.7, 5.3), (L("Ingresos", "Revenue"), 79.9, 20.1))):
    y = 5.22 + k * 0.36
    f.append(caja(i, f"Etiqueta barra {k}", 0.85, y, 1.55, 0.26, [para([run(lab, 10.5, TEXTO, b=True)])], anchor="ctr")); i += 1
    total, x0 = 6.45, 2.45
    wd = total * pd_ / 100 - 0.015; wr = total * pr_ / 100 - 0.015
    f.append(forma(i, f"Barra distribución {k}", x0, y, wd, 0.26, VERDE, adj=12000,
                   paras=[para([run(pct(round(pd_)), 9.5, CREMA, b=True)])], anchor="ctr", ins=(0.1, 0, 0, 0))); i += 1
    f.append(forma(i, f"Barra restaurantes {k}", x0 + wd + 0.03, y, wr, 0.26, NARANJA, adj=12000,
                   paras=[para([run(pct(round(pr_)), 9.5, BLANCO, b=True)], algn="ctr")], anchor="ctr")); i += 1
f.append(forma(i, "Margen por kilo", 9.3, 4.93, 3.18, 0.9, VERDE_CLARO, adj=8000, ins=(0.18, 0.04, 0.12, 0.04), anchor="ctr",
               paras=[para([run(L("× 4,4", "× 4.4"), 22, NARANJA, b=True), run(L("  margen por kilo", "  margin per kilo"), 10, VERDE, b=True)]),
                      para([run(L("restaurantes 120 €/kg frente a 27 €/kg en distribución, tras reparto y captación",
                                  "restaurants €120/kg vs €27/kg in distribution, after delivery and acquisition"), 8.5, VERDE2)], ln=105)])); i += 1
escribir("slide24.xml", insertar(x, f))

# ---------------------------------------------------------------- nueva B · mapa
x = marco("slide25.xml", L("REPARTO A RESTAURANTES", "RESTAURANT DELIVERY"), L("ZONAS CALIENTES", "HOT ZONES"),
          L("Ocho barrios, ", "Eight neighborhoods, "), L("un microhub, dos riders.", "one microhub, two riders."),
          L("Producto vivo, gourmet, de cercanía.", "Living, gourmet, locally grown."), quitar_banda=True)
shutil.copy(MAPA, os.path.join(d, "ppt", "media", "mapa_zonas_v17.png"))
rels = os.path.join(S, "_rels", "slide25.xml.rels")
r = open(rels, encoding="utf-8").read()
r = r.replace("</Relationships>", '<Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
              'relationships/image" Target="../media/mapa_zonas_v17.png"/></Relationships>')
open(rels, "w", encoding="utf-8").write(r)
f, i = [], 100
f.append(imagen(i, "Mapa zonas calientes", "rId9", 0.85, 2.42, 5.6, 4.25, L(
    "Mapa del centro de Madrid con los barrios Ríos Rosas, Trafalgar, Almagro, Castellana, Lista, Justicia, Recoletos y Goya "
    "resaltados y los 585 restaurantes abiertos marcados como puntos",
    "Map of central Madrid highlighting the Ríos Rosas, Trafalgar, Almagro, Castellana, Lista, Justicia, Recoletos and Goya "
    "neighborhoods, with the 585 open restaurants shown as dots"))); i += 1
f.append(forma(i, "Marco mapa", 0.85, 2.42, 5.6, 4.25, None, LINEA, prst="rect")); i += 1
f.append(caja(i, "Cabecera barrios", 6.85, 2.45, 5.6, 0.2,
              [para([run(L("RESTAURANTES ABIERTOS POR BARRIO  ·  CENSO MUNICIPAL", "OPEN RESTAURANTS BY NEIGHBORHOOD  ·  CITY CENSUS"),
                         8.5, GRIS, b=True, spc=150)])])); i += 1
zonas = [("Justicia", 140), ("Recoletos", 92), ("Castellana", 69), ("Goya", 64), ("Trafalgar", 62),
         ("Almagro", 57), ("Ríos Rosas", 54), ("Lista", 47)]
for k, (z, n) in enumerate(zonas):
    y = 2.74 + k * 0.265
    w = 3.45 * n / 140
    f.append(caja(i, f"Barrio {z}", 6.85, y, 1.25, 0.22, [para([run(z, 10.5, TEXTO)])], anchor="ctr")); i += 1
    f.append(forma(i, f"Barra {z}", 8.15, y + 0.04, w, 0.14, VERDE if k == 0 else VERDE2, adj=30000)); i += 1
    f.append(caja(i, f"Cifra {z}", 8.15 + w + 0.08, y, 0.6, 0.22, [para([run(str(n), 10, VERDE, b=True)])], anchor="ctr")); i += 1
f.append(caja(i, "Total zonas", 6.85, 4.9, 5.63, 0.5, [
    para([run(L("585 restaurantes ", "585 restaurants "), 11, NARANJA, b=True),
          run(L("en las 8 zonas, y otros 714 bar-restaurantes que no contamos.", "across the 8 zones, plus 714 bar-restaurants we don't count."), 10.5, TEXTO)], ln=105),
    para([run(L("Microhub refrigerado en la zona · dos pedidos por semana a cada restaurante.",
                "Refrigerated microhub inside the zone · two orders a week to every restaurant."), 10.5, TEXTO)], ln=105)])); i += 1
tiles = [("123", L("RESTAURANTES OBJETIVO\n1 DE CADA 5 DE LA ZONA", "TARGET RESTAURANTS\n1 IN 5 IN THE ZONE"), True),
         ("~40", L("ENTREGAS AL DÍA\n2 RIDERS · 7 POR HORA", "DELIVERIES A DAY\n2 RIDERS · 7 PER HOUR"), False),
         (L("4,4 €", "€4.4"), L("ÚLTIMA MILLA POR PEDIDO\n15 % DEL TICKET", "LAST MILE PER ORDER\n15% OF THE TICKET"), False)]
for k, (cif, pie, osc) in enumerate(tiles):
    x0 = 6.85 + k * (1.75 + 0.19)
    f.append(forma(i, f"Dato {k}", x0, 5.55, 1.75, 0.82, VERDE if osc else CREMA, None if osc else VERDE, adj=7000, anchor="ctr",
                   paras=[para([run(cif, 20, CREMA if osc else NARANJA, b=True)], algn="ctr")] +
                         [para([run(l, 7, VERDE_MEDIO if osc else VERDE2, b=True, spc=60)], algn="ctr") for l in pie.split("\n")])); i += 1
f.append(caja(i, "Fuente mapa", 6.85, 6.45, 5.63, 0.3, [para([run(L(
    "Fuente: Censo de locales y actividades del Ayuntamiento de Madrid (datos.madrid.es), locales abiertos con epígrafe 561001 "
    "Restaurante, oct. 2026. Objetivo y reparto: modelo V17, escenario base, año 5.",
    "Source: Madrid City Council premises and activities census (datos.madrid.es), open premises under code 561001 Restaurant, "
    "Oct. 2026. Target and delivery: financial model V17, base case, year 5."), 7, GRIS, i=True)], ln=100)])); i += 1
escribir("slide25.xml", insertar(x, f))

# ---------------------------------------------------------------- empaquetar
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for raiz, _, archivos in os.walk(d):
        for a in archivos:
            p = os.path.join(raiz, a)
            z.write(p, os.path.relpath(p, d))
shutil.rmtree(tmp)
print("escrito", OUT)
