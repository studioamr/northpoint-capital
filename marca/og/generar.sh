#!/bin/sh
# Regenera /og.png (1200×630) desde marca/og/og.html.
# Correr desde la raíz del repo:  sh marca/og/generar.sh
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --virtual-time-budget=4000 --window-size=1200,630 \
  --screenshot="$PWD/og.png" "file://$PWD/marca/og/og.html" 2>/dev/null
echo "og.png regenerada · $(wc -c < og.png) bytes"
