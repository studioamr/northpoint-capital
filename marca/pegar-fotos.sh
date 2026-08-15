#!/bin/bash
# NORTHPOINT · captura las fotos del portapapeles
#
# Copias una foto (Cmd+C, o clic derecho → Copiar imagen) y esto la guarda solo.
# Copias la siguiente, la guarda. Y así hasta que le des Ctrl+C.
#
# Existe porque las fotos pegadas en el chat viven en la conversación, no en el
# disco: no hay forma de que yo las escriba desde ahí.
#
#   bash marca/pegar-fotos.sh

DEST="$(cd "$(dirname "$0")" && pwd)/fotos"
mkdir -p "$DEST"
n=$(ls "$DEST"/andre-*.png "$DEST"/andre-*.jpg 2>/dev/null | wc -l | tr -d ' ')
ultima=""

echo "  Guardando en: $DEST"
echo "  Ya hay $n fotos."
echo ""
echo "  → Copia una foto (Cmd+C). La guardo sola."
echo "  → Copia la siguiente. Y la siguiente."
echo "  → Cuando acabes: Ctrl+C"
echo ""

while true; do
  # ¿hay una imagen en el portapapeles?
  if osascript -e 'clipboard info' 2>/dev/null | grep -qi "PNGf\|TIFF\|JPEG"; then
    tmp="/tmp/np-clip.png"
    osascript <<'OSA' >/dev/null 2>&1
      set f to (open for access POSIX file "/tmp/np-clip.png" with write permission)
      try
        set eof f to 0
        write (the clipboard as «class PNGf») to f
      end try
      close access f
OSA
    if [ -s "$tmp" ]; then
      firma=$(md5 -q "$tmp" 2>/dev/null)
      if [ "$firma" != "$ultima" ]; then
        ultima="$firma"
        n=$((n+1))
        out="$DEST/$(printf 'andre-%02d.png' $n)"
        cp "$tmp" "$out"
        d=$(sips -g pixelWidth -g pixelHeight "$out" 2>/dev/null | awk '/pixel/{printf "%sx",$2}' | sed 's/x$//')
        echo "  ✓ $(basename "$out")  ($d)"
      fi
    fi
  fi
  sleep 1
done
