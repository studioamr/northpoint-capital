#!/bin/bash
# Vuelve a generar NORTHPOINT.pdf desde dossier.html.
# Doble clic y listo — no hace falta acordarse del comando de Chrome.
cd "$(dirname "$0")/.."
python3 -m http.server 4399 >/dev/null 2>&1 &
SRV=$!; sleep 1
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --virtual-time-budget=8000 --no-pdf-header-footer \
  --print-to-pdf="$PWD/NORTHPOINT.pdf" "http://localhost:4399/dossier.html" 2>/dev/null
kill $SRV 2>/dev/null
echo "listo → $PWD/NORTHPOINT.pdf"
