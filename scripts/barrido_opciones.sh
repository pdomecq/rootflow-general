#!/bin/bash
# Prueba varias estructuras contra el modelo real y recalcula cada una.
set -e
export HOME=/tmp/lohome
cd /home/user/rootflow-general
mkdir -p /tmp/opts /tmp/opts_recalc
# nombre        ronda   pre-money  enisa   mes_salida  mes_formalizacion
cat > /tmp/opts/lista.txt <<'L'
A 100000 900000 100000 48 0
B 100000 900000 100000 48 3
C 130000 900000 100000 48 3
D 150000 900000 100000 48 3
E 100000 900000  80000 48 1
F 130000 900000 100000 60 3
L
while read -r n ronda pre enisa salida form; do
  [ -z "$n" ] && continue
  python3 scripts/modelo_a_equity.py "$ronda" "$pre" "$enisa" "$salida" "$form" "/tmp/opts/opt_$n.xlsx" >/dev/null
  timeout 420 libreoffice --headless --norestore --convert-to xlsx --outdir /tmp/opts_recalc "/tmp/opts/opt_$n.xlsx" >/dev/null 2>&1
  echo "  opcion $n lista"
done < /tmp/opts/lista.txt
