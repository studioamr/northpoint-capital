#!/usr/bin/env python3
"""
Puente local: le da razonamiento al gabinete usando TU Claude Code.

Por qué existe: la API de Anthropic se cobra por uso, y tú ya pagas Claude Code.
Este puente corre en tu máquina, escucha en localhost y le pasa las preguntas al
comando `claude` que ya tienes instalado. No hay llave que pegar y no se paga
nada extra — es exactamente lo que hace SPOTTER.

Cómo se usa:

    python3 scripts/puente.py

Déjalo corriendo en una terminal. El terminal web lo detecta solo y el chat pasa
a razonar. Se cierra con Ctrl-C.

Nada sale de tu equipo: el navegador habla con localhost, y localhost habla con
el `claude` de tu Mac.
"""
import json
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PUERTO = 4319
CLAUDE = shutil.which('claude')
TIMEOUT = 90

# Sólo el terminal de Northpoint puede hablarle a este puente.
ORIGENES = {
    'https://studioamr.github.io',
    'http://localhost:4304',
    'http://127.0.0.1:4304',
}


def pregunta_a_claude(sistema, mensaje):
    """Una pregunta suelta, sin sesión: cada llamada es independiente."""
    prompt = f'{sistema}\n\n---\n\n{mensaje}'
    r = subprocess.run(
        [CLAUDE, '-p', prompt],
        capture_output=True, text=True, timeout=TIMEOUT,
        stdin=subprocess.DEVNULL,      # sin esto claude se queda esperando entrada
    )
    salida = (r.stdout or '').strip()
    err = (r.stderr or '').strip()
    # claude devuelve 0 aunque falle la sesión, así que el fallo se detecta en el texto
    mezcla = (salida + ' ' + err).lower()
    if 'oauth' in mezcla or 'authenticate' in mezcla or 'session expired' in mezcla:
        raise RuntimeError('Tu sesión de Claude Code expiró. Abre una terminal, '
                           'corre  claude  y vuelve a entrar. Luego reinicia este puente.')
    if r.returncode != 0 or not salida:
        raise RuntimeError(err[:300] or 'claude no devolvió texto')
    return salida


class Puente(BaseHTTPRequestHandler):
    def _cors(self):
        origen = self.headers.get('Origin', '')
        if origen in ORIGENES:
            self.send_header('Access-Control-Allow-Origin', origen)
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        """El terminal pregunta si el puente está vivo antes de usarlo."""
        self.send_response(200)
        self._cors()
        self.send_header('content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'ok': True, 'claude': bool(CLAUDE)}).encode())

    def do_POST(self):
        try:
            n = int(self.headers.get('content-length') or 0)
            cuerpo = json.loads(self.rfile.read(n) or b'{}')
            texto = pregunta_a_claude(cuerpo.get('sistema', ''), cuerpo.get('mensaje', ''))
            salida, codigo = {'texto': texto}, 200
        except subprocess.TimeoutExpired:
            salida, codigo = {'error': f'claude tardó más de {TIMEOUT}s'}, 504
        except Exception as e:
            salida, codigo = {'error': str(e)[:300]}, 500
        self.send_response(codigo)
        self._cors()
        self.send_header('content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(salida, ensure_ascii=False).encode())

    def log_message(self, *a):
        pass            # sin ruido en la terminal


def main():
    if not CLAUDE:
        print('No encuentro el comando `claude` en este equipo.', file=sys.stderr)
        print('Instálalo o revisa que esté en el PATH, y vuelve a correr esto.', file=sys.stderr)
        return 1
    print(f'Puente del gabinete escuchando en http://localhost:{PUERTO}')
    print(f'Usando: {CLAUDE}')
    print('Deja esta ventana abierta. El terminal lo detecta solo.')
    print('Ctrl-C para cerrar.\n')
    try:
        HTTPServer(('127.0.0.1', PUERTO), Puente).serve_forever()
    except KeyboardInterrupt:
        print('\nPuente cerrado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
