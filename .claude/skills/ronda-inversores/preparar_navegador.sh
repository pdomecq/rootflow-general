#!/usr/bin/env bash
# Deja el Chromium de Playwright listo para navegar a través del proxy de la sesión en la nube.
# El proxy re-firma el TLS con su propia CA: Chromium la necesita en su almacén NSS.
# Uso: bash .claude/skills/ronda-inversores/preparar_navegador.sh
set -e
DIR="$HOME/.pki/nssdb"; DB="sql:$DIR"; CA=/root/.ccr/agent-proxy-ca.crt
mkdir -p "$DIR"
if ! command -v certutil >/dev/null; then
  apt-get install -y -q libnss3-tools >/dev/null 2>&1 || { apt-get update -q >/dev/null 2>&1 && apt-get install -y -q libnss3-tools >/dev/null 2>&1; }
fi
[ -f "$DIR/cert9.db" ] || certutil -N -d "$DB" --empty-password
if [ -f "$CA" ] && ! certutil -L -d "$DB" -n ccr-agent-proxy >/dev/null 2>&1; then
  certutil -A -d "$DB" -t "C,," -n ccr-agent-proxy -i "$CA"
fi
NODE_PATH=$(npm root -g) node -e "require('playwright')"
echo "Navegador listo: NODE_PATH=\$(npm root -g) node .claude/skills/ronda-inversores/formularios_web.js inspeccionar|enviar ..."
