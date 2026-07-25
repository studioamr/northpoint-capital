#!/bin/bash
# Puente del gabinete · usa tu Claude Code, sin costo extra.
# Doble clic para prenderlo. Deja esta ventana abierta.

cd "$(dirname "$0")" || exit 1
clear
echo "──────────────────────────────────────────────"
echo "  NORTHPOINT · puente del gabinete"
echo "──────────────────────────────────────────────"
echo

# python3 puede no estar en el PATH que usa Finder al abrir un .command
PY=""
for cand in /opt/anaconda3/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3 /usr/bin/python3; do
  [ -x "$cand" ] && PY="$cand" && break
done
[ -z "$PY" ] && PY="$(command -v python3)"

if [ -z "$PY" ]; then
  echo "  No encuentro python3 en este equipo."
  echo "  Instálalo o dime y lo resolvemos de otra forma."
  echo
  echo "Presiona Enter para cerrar."
  read -r
  exit 1
fi

echo "  Usando: $PY"
echo

"$PY" scripts/puente.py
CODIGO=$?

echo
echo "──────────────────────────────────────────────"
if [ $CODIGO -ne 0 ]; then
  echo "  El puente se cerró con un error (código $CODIGO)."
  echo "  Copia lo de arriba y pásamelo."
else
  echo "  Puente cerrado."
fi
echo "  Presiona Enter para cerrar esta ventana."
read -r
