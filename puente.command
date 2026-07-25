#!/bin/bash
# Doble clic para prender el razonamiento del gabinete.
# Usa tu Claude Code local: no se paga nada extra.
cd "$(dirname "$0")"
exec python3 scripts/puente.py
