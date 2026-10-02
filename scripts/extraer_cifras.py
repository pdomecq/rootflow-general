#!/usr/bin/env python3
"""Extrae de un modelo recalculado la tabla de cifras que alimentan los decks."""
import openpyxl, sys, json

F_KG, F_ING, F_PLANT, F_OCUP, F_POS = 26, 36, 31, 25, 24
F_EBITDA_A, F_DSCR_A = 142, 144

def cifras(ruta):
    wb = openpyxl.load_workbook(ruta, data_only=True)
    h, pr, cx = wb["Hipótesis"], wb["Producto"], wb["CAPEX"]
    o = {}
    o["kg_band_mes"]     = h["F23"].value
    o["ciclos_mes"]      = h["F24"].value
    o["precio_medio_kg"] = pr["D35"].value
    o["margen_bruto_pf"] = pr["D36"].value
    o["ingreso_band_mes"]= pr["T32"].value
    o["dias_muertos"]    = pr["D7"].value
    o["bandejas_rack"]   = h["D13"].value
    o["racks"]           = h["F26"].value
    o["posiciones_nave"] = (h["D13"].value or 0) * (h["F26"].value or 0)
    o["m2_nave"]         = (h["D14"].value or 0) * (h["F26"].value or 0)
    o["m2_bandeja"]      = h["D11"].value
    o["band_rack_antiguo"] = h["D8"].value

    # rendimiento por variedad activa (para el pico en monocultivo)
    act = []
    for r in range(16, 32):
        if (pr.cell(row=r, column=3).value or 0) == 1:
            act.append(dict(var=pr.cell(row=r, column=1).value,
                            dias_luz=pr.cell(row=r, column=8).value,
                            ciclos=pr.cell(row=r, column=10).value,
                            g=pr.cell(row=r, column=11).value,
                            kg_band_mes=pr.cell(row=r, column=13).value))
    o["activas"] = act
    rab = [a for a in act if "ábano" in str(a["var"])]
    o["kg_band_mes_rabano"] = max((a["kg_band_mes"] for a in rab), default=0)

    # CAPEX (coordenadas fijas)
    o["capex"] = {
        "adaptacion_nave": cx["C5"].value, "automatizacion": cx["C10"].value,
        "racks": cx["C13"].value, "instalacion": cx["C14"].value,
        "vehiculo": cx["C15"].value, "mobiliario": cx["C16"].value,
        "licencias": cx["C17"].value, "legal": cx["C18"].value,
        "subtotal": cx["C19"].value, "contingencia": cx["C21"].value,
        "capex_total": cx["C22"].value, "colchon_circulante": cx["C25"].value,
        "bloque_obra_bottomup": cx["C35"].value if cx["C35"].value is not None else None,
        "bloque_obra_aplicado": cx["C38"].value if cx["C38"].value is not None else None,
    }
    o["necesidad"]  = cx["C26"].value
    o["ronda_total"]= (h["D93"].value or 0)+(h["D105"].value or 0)+(h["D113"].value or 0)
    o["cobertura"]  = o["ronda_total"]/o["necesidad"] if o["necesidad"] else None
    o["pct_inversor"]     = h["D119"].value
    o["importe_inversor"] = h["D92"].value
    o["importe_enisa"]    = h["D104"].value

    v17 = "Restaurantes" in wb.sheetnames
    if v17:
        r = wb["Restaurantes"]
        o["restaurantes"] = dict(palanca=r["D7"].value, techo=r["D13"].value, zonas_total=r["D11"].value,
                                 penetracion=r["D12"].value, ticket=r["D22"].value, pedidos_semana=r["D24"].value,
                                 entregas_hora=[r["C36"].value, r["D36"].value, r["E36"].value],
                                 coste_rider_h=r["D37"].value, microhub_mes=r["D44"].value,
                                 zonas={r.cell(row=k, column=1).value: r.cell(row=k, column=4).value for k in range(74, 82)})
        o["precio_kg_canal"] = dict(mayorista=pr["D44"].value, tienda=pr["D45"].value, restaurante=pr["D46"].value)
        o["capex"]["microhub"] = cx["C44"].value
        o["capex"]["fianzas"] = cx["C50"].value
    esc = {}
    for hoja, nom in (("Esc_Conservador","conservador"),("Esc_Base","base"),("Esc_Optimista","optimista")):
        b = wb[hoja]; g = lambda r: b.cell(row=r, column=3).value
        d = dict(tir=g(128), moic=g(129), equity_salida=g(157), cobro=g(158),
                 dscr_min=g(145), caja_min=g(146), cumple=g(165),
                 kg_mes_regimen=b.cell(row=F_KG, column=62).value,
                 ocupacion_regimen=b.cell(row=F_OCUP, column=62).value,
                 posiciones_regimen=b.cell(row=F_POS, column=62).value)
        d["anual"] = []
        for i, col in enumerate(range(3, 10), 1):
            c0 = 3+(i-1)*12
            ing  = sum((b.cell(row=F_ING, column=c).value or 0) for c in range(c0, c0+12))
            kg   = sum((b.cell(row=F_KG,  column=c).value or 0) for c in range(c0, c0+12))
            ebit = b.cell(row=F_EBITDA_A, column=col).value or 0
            fila = dict(ano=i, ingresos=ing, ebitda=ebit,
                        margen=(ebit/ing if ing else 0), kg=kg,
                        plantilla=b.cell(row=F_PLANT, column=c0+11).value,
                        dscr=b.cell(row=F_DSCR_A, column=col).value)
            if v17:   # líneas de negocio (V17+)
                S = lambda r: sum((b.cell(row=r, column=c).value or 0) for c in range(c0, c0+12))
                fila.update(ing_distribucion=S(34), ing_restaurantes=S(35), kg_restaurantes=S(181),
                            cm_distribucion=S(214), cm_restaurantes=S(215), pedidos=S(188),
                            ultima_milla=-S(207),
                            restaurantes_fin=b.cell(row=196, column=c0+11).value,
                            riders_fin=b.cell(row=200, column=c0+11).value)
            d["anual"].append(fila)
        esc[nom] = d
    o["escenarios"] = esc
    return o

if __name__ == "__main__":
    print(json.dumps(cifras(sys.argv[1]), ensure_ascii=False, indent=1, default=str))
