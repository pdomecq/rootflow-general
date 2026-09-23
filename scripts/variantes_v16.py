#!/usr/bin/env python3
"""Genera variantes del V16 tocando solo celdas de input, recalcula y extrae cifras."""
import openpyxl, shutil, subprocess, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extraer_cifras import cifras

BASE = "modelo/Rootflow_Modelo_Financiero_V16.xlsx"
TMP, OUT = "/tmp/var", "/tmp/var_out"

def variante(nombre, dias_muertos=None, capex_ajuste=None, importe=None,
             enisa=None, pre_money=900000, guardar=None):
    os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    src = f"{TMP}/{nombre}.xlsx"
    shutil.copy(BASE, src)
    wb = openpyxl.load_workbook(src, data_only=False)
    if dias_muertos is not None: wb["Producto"]["D7"] = dias_muertos
    if capex_ajuste is not None: wb["CAPEX"]["C37"] = capex_ajuste
    if importe is not None:
        wb["Hipótesis"]["D92"]  = importe
        wb["Hipótesis"]["D119"] = importe / (pre_money + importe)
    if enisa is not None: wb["Hipótesis"]["D104"] = enisa
    wb.save(src)
    env = dict(os.environ, HOME="/tmp/lohome")
    subprocess.run(["libreoffice","--headless","--norestore","--convert-to","xlsx",
                    "--outdir",OUT,src], check=False, capture_output=True, timeout=420, env=env)
    dst = f"{OUT}/{nombre}.xlsx"
    if guardar: shutil.copy(dst, guardar)
    return cifras(dst)

if __name__ == "__main__":
    res = {}
    print("Generando variantes (cada una recalcula el modelo entero)...")
    res["v16"]           = cifras(BASE)
    res["dias_muertos1"] = variante("dm1", dias_muertos=1);            print("  · días muertos = 1")
    for pct, et in ((0.10,"capex10"), (0.25,"capex25"), (0.50,"capex50")):
        res[et] = variante(et, capex_ajuste=pct);                      print(f"  · CAPEX +{pct:.0%}")
    for imp, et in ((125000,"ronda250"), (150000,"ronda300")):
        res[et] = variante(et, importe=imp, enisa=imp);                print(f"  · ronda {imp*2:,} €")
    json.dump(res, open("/tmp/variantes.json","w"), ensure_ascii=False, default=str)
    print("OK")
