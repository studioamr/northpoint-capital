#!/usr/bin/env python3
"""
Una hoja de bienvenida por socio, con sus accesos. Breve a propósito.

El recorrido guiado de la app ya explica el terminal; esto sólo es el papel que se
manda por correo antes de que entren: qué es, cómo entran, y las tres reglas que no
se negocian.

  python3 scripts/credenciales.py

OJO: las hojas llevan contraseñas, así que se escriben en `credenciales/`, que está
FUERA del control de versiones. El repositorio es público — un PDF con claves ahí
sería regalarlas. No mover esa carpeta adentro.
"""
import html
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'credenciales'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

LANDING = 'https://studioamr.github.io/northpoint-capital/'
TERMINAL = 'https://studioamr.github.io/northpoint-capital/app.html'

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
         'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

SOCIOS = [
    {'usuario': 'pablo.np', 'nombre': 'Pablo', 'clave': 'northpointpablo',
     'cargos': [('NP-001', 'Chief Investment Officer'),
                ('NP-010', 'Portfolio Manager')],
     'puerta': 'Eres la última firma de una tesis y el único que la ejecuta.'},
    {'usuario': 'mateo.np', 'nombre': 'Mateo', 'clave': 'northpointmateo',
     'cargos': [('NP-020', 'Chief Risk Officer'),
                ('NP-030', 'Research Analyst')],
     'puerta': 'Firmas research y riesgo, y puedes detener la mesa sin pedir permiso.'},
    {'usuario': 'andre.np', 'nombre': 'André', 'clave': 'northpointandre',
     'cargos': [('NP-040', 'Quant'), ('NP-050', 'Chief Operating Officer')],
     'puerta': 'Firmas que los números cuadran y sostienes la operación.'},
]

ESTILOS = """<style>
@page { size: letter; margin: 22mm 20mm; }
/* Papel blanco a fuerza: sin esto el documento hereda el esquema oscuro del visor
   y sale texto negro sobre negro. */
:root{color-scheme:light}
html,body{background:#FFFFFF}
*{box-sizing:border-box}
body{
  font-family:Georgia,'Times New Roman',serif; color:#14181E; margin:0;
  font-size:11.5pt; line-height:1.62; -webkit-font-smoothing:antialiased;
}
.mono{font-family:'IBM Plex Mono',Menlo,Consolas,monospace}
.marca{
  font-family:'IBM Plex Mono',Menlo,Consolas,monospace;
  font-size:8.5pt; letter-spacing:.30em; color:#6A7280;
  border-bottom:1px solid #D8DCE2; padding-bottom:9px; margin-bottom:34px;
}
h1{font-size:25pt; font-weight:400; letter-spacing:-.015em; margin:0 0 6px}
.sub{color:#5B6470; font-size:11pt; margin:0 0 30px}
h2{
  font-family:'IBM Plex Mono',Menlo,Consolas,monospace;
  font-size:8.5pt; letter-spacing:.20em; color:#6A7280; font-weight:400;
  margin:30px 0 12px; padding-bottom:7px; border-bottom:1px solid #E4E7EB;
}
p{margin:0 0 12px}
.caja{border:1px solid #D8DCE2; border-radius:3px; padding:17px 19px; margin:0 0 14px}
.par{display:flex; justify-content:space-between; align-items:baseline;
     padding:7px 0; border-bottom:1px dotted #E4E7EB}
.par:last-child{border-bottom:0}
.k{font-family:'IBM Plex Mono',Menlo,Consolas,monospace; font-size:8.5pt;
   letter-spacing:.14em; color:#6A7280}
.v{font-family:'IBM Plex Mono',Menlo,Consolas,monospace; font-size:12pt; color:#14181E}
.v.liga{font-size:9.5pt; word-break:break-all}
.cargo{margin-bottom:9px}
.cargo b{font-weight:600}
.cargo span{font-family:'IBM Plex Mono',Menlo,Consolas,monospace; font-size:8.5pt;
            color:#6A7280; margin-left:7px}
ol{margin:0 0 12px; padding-left:19px}
li{margin-bottom:7px}
.nota{background:#F5F6F8; border-left:2px solid #14181E; padding:13px 16px;
      font-size:10.5pt; color:#3A424E; margin:16px 0}
.pie{margin-top:34px; padding-top:13px; border-top:1px solid #D8DCE2;
     font-family:'IBM Plex Mono',Menlo,Consolas,monospace;
     font-size:8pt; letter-spacing:.14em; color:#8A9199}
</style>"""


def hoja(s):
    hoy = date.today()
    fecha = f'{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}'
    nombre = html.escape(s['nombre'])
    cargos = ''.join(
        f'<div class="cargo"><b>{html.escape(t)}</b><span>{c}</span></div>'
        for c, t in s['cargos'])

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Northpoint · {nombre}</title>
{ESTILOS}</head><body>

<div class="marca">NORTHPOINT CAPITAL MANAGEMENT</div>

<h1>Bienvenido, {nombre}.</h1>
<p class="sub">Tus accesos a la mesa. {fecha}.</p>

<p>Somos tres y cada quien firma una puerta distinta. {html.escape(s['puerta'])}
Nada entra al mercado sin las cuatro firmas — así es como una corazonada no se vuelve
una posición.</p>

<h2>TU CARGO</h2>
{cargos}

<h2>TUS ACCESOS</h2>
<div class="caja">
  <div class="par"><span class="k">USUARIO</span><span class="v">{s['usuario']}</span></div>
  <div class="par"><span class="k">CONTRASEÑA</span><span class="v">{html.escape(s['clave'])}</span></div>
  <div class="par"><span class="k">TERMINAL</span><span class="v liga">{TERMINAL}</span></div>
  <div class="par"><span class="k">LA FIRMA</span><span class="v liga">{LANDING}</span></div>
</div>
<div class="nota">Cámbiala en <b>Ajustes</b> la primera vez que entres, arriba a la
derecha. Esta hoja trae tu contraseña escrita: no la reenvíes.</div>

<h2>CÓMO EMPEZAR</h2>
<ol>
  <li>Abre el terminal en el enlace de arriba y entra con esos datos.</li>
  <li>La primera vez te va a salir un recorrido de un minuto por las pantallas. Hazlo.</li>
  <li>Cambia tu contraseña en Ajustes.</li>
  <li>Listo. A partir de mañana el correo te llega solo: el resumen del overnight a las
      6:20, un aviso antes de que abra la ventana, y uno cada vez que alguien firma una
      tesis o registra un trade.</li>
</ol>

<h2>LO QUE NO SE NEGOCIA</h2>
<ol>
  <li><b>La ventana.</b> Se opera de 7:00 a 8:30, de lunes a viernes. El rango de
      apertura se forma de 7:30 a 7:45. Fuera de ahí la mesa está cerrada — no es
      capricho, es la franja donde el sistema tiene ventaja medida.</li>
  <li><b>Dos trades.</b> Máximo dos por sesión. Si el primero gana, se para. No hay
      tercer intento ni desquite.</li>
  <li><b>Todo se registra.</b> Cada trade va al journal con sus capturas. Las
      violaciones se marcan solas y no se borran. Un día perdedor operado bien es un
      día profesional; un día ganador que rompió las reglas es un pasivo.</li>
</ol>

<div class="pie">NORTHPOINT CAPITAL MANAGEMENT · DOCUMENTO INTERNO · {nombre.upper()}</div>
</body></html>"""


def main():
    if not Path(CHROME).exists():
        print(f'No encuentro Chrome en {CHROME}', file=sys.stderr)
        return 1
    SALIDA.mkdir(exist_ok=True)
    (SALIDA / '.gitignore').write_text(
        '# Estas hojas llevan contraseñas y el repositorio es publico.\n*\n')

    for s in SOCIOS:
        htm = SALIDA / f'_{s["usuario"]}.html'
        pdf = SALIDA / f'Northpoint-{s["nombre"]}.pdf'
        htm.write_text(hoja(s), encoding='utf-8')
        subprocess.run(
            [CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
             f'--print-to-pdf={pdf}', htm.as_uri()],
            check=True, capture_output=True)
        htm.unlink()
        print(f'  → {pdf}  ({pdf.stat().st_size // 1024} KB)')

    print(f'\n{len(SOCIOS)} hojas en {SALIDA}')
    print('Esa carpeta NO se sube al repositorio: lleva contraseñas.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
