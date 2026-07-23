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
PUBLICO = RAIZ / 'docs'          # el del candidato SÍ va al repositorio: no lleva claves
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

LANDING = 'https://studioamr.github.io/northpoint-capital/'
TERMINAL = 'https://studioamr.github.io/northpoint-capital/app.html'

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
         'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

# Los mismos deberes que muestra el terminal en Ajustes (ROLES en app.html).
# Si allá cambian, aquí también: es el mismo contrato dicho dos veces.
DEBERES = {
 'NP-001': ('Chief Investment Officer', [
   'Responsable final de todas las decisiones de inversión del fondo.',
   'Define la estrategia macroeconómica y los mandatos de cada estrategia.',
   'Aprueba o rechaza toda tesis de inversión antes de ejecución.',
   'Responde ante el comité de inversiones y los limited partners.']),
 'NP-010': ('Portfolio Manager', [
   'Gestión activa de portafolios dentro de los mandatos aprobados.',
   'Construcción y monitoreo de posiciones largas y cortas.',
   'Comunicación periódica con el CIO sobre exposiciones y riesgo.',
   'Documenta cada decisión de posición con tesis escrita.']),
 'NP-020': ('Chief Risk Officer', [
   'Monitoreo en tiempo real del drawdown máximo permitido por estrategia.',
   'Emite alertas de riesgo con autoridad para detener operaciones.',
   'Reporte diario al CIO sobre posiciones y exposición de mercado.',
   'Define y actualiza el Risk Management Framework.']),
 'NP-030': ('Research Analyst', [
   'Investigación fundamental y cuantitativa de activos y sectores.',
   'Produce memos de inversión con evidencia documentada.',
   'Monitorea earnings, macro data y eventos catalizadores.',
   'Da seguimiento a posiciones existentes y alerta cambios de tesis.']),
 'NP-040': ('Quantitative Analyst', [
   'Desarrollo y backtesting de modelos cuantitativos de inversión.',
   'Análisis estadístico de patrones conductuales en datos de mercado.',
   'Construye el Northpoint Score y métricas de behavioral intelligence.',
   'Mantiene los sistemas de datos y pipelines de información.']),
 'NP-050': ('Chief Operating Officer', [
   'Gestión de operaciones diarias, compliance y relación con brokers.',
   'Coordina prime brokerage, custodios y administradores del fondo.',
   'Supervisa client relations e investor relations.',
   'Implementa protocolos operativos y auditorías internas.']),
}

SOCIOS = [
    {'usuario': 'pablo.np', 'nombre': 'Pablo', 'clave': 'northpointpablo',
     'cargos': [('NP-001', 'Chief Investment Officer'),
                ('NP-010', 'Portfolio Manager')],
     'puerta': 'Eres la última firma de una tesis y el único que la ejecuta.',
     'firma': ['<b>CIO</b> — la cuarta y última puerta. Puedes rechazar con motivo escrito.'],
     'ejecuta': True},
    {'usuario': 'mateo.np', 'nombre': 'Mateo', 'clave': 'northpointmateo',
     'cargos': [('NP-020', 'Chief Risk Officer'),
                ('NP-030', 'Research Analyst')],
     'puerta': 'Firmas research y riesgo, y puedes detener la mesa sin pedir permiso.',
     'firma': ['<b>Research</b> — que la tesis tiene evidencia, no corazonada.',
               '<b>Riesgo</b> — que el tamaño y el stop caben en el límite del día.'],
     'ejecuta': False},
    {'usuario': 'andre.np', 'nombre': 'André', 'clave': 'northpointandre',
     'cargos': [('NP-040', 'Quant'), ('NP-050', 'Chief Operating Officer')],
     'puerta': 'Firmas que los números cuadran y sostienes la operación.',
     'firma': ['<b>Quant</b> — que los números y el setup cuadran con lo medido.'],
     'ejecuta': False},
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
.v2{font-size:10pt; text-align:right; max-width:74%}
.cargo-h{margin-bottom:3px}
.cargo ul{margin:0 0 0 0; padding-left:18px}
.cargo li{margin-bottom:3px; font-size:10.5pt; color:#3A424E}
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

    deberes = ''.join(
        f'<div class="cargo"><div class="cargo-h"><b>{html.escape(DEBERES[c][0])}</b>'
        f'<span>{c}</span></div><ul>'
        + ''.join(f'<li>{html.escape(d)}</li>' for d in DEBERES[c][1])
        + '</ul></div>'
        for c, _ in s['cargos'])

    firmas = ''.join(f'<li>{f}</li>' for f in s['firma'])
    ejecuta = ('<p>Y como PM, cuando una tesis junta las cuatro, <b>tú la ejecutas</b> '
               'y la registras en el journal. Nadie más toca el botón.</p>'
               if s.get('ejecuta') else
               '<p>Sin tu firma la tesis no avanza. Si algo no te cuadra, no firmes: '
               'ése es exactamente el punto de que seamos cuatro puertas.</p>')

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

<h2>LO QUE TE TOCA</h2>
{deberes}

<h2>TU FIRMA</h2>
<p>Ninguna posición entra al mercado por gusto. Una tesis se propone en el terminal y
recorre <b>cuatro puertas</b> —Research, Riesgo, Quant y CIO— cada una firmada por quien
responde por ella. Con las cuatro, queda aprobada. Sin una sola, no existe.</p>
<p>Las puertas que firmas tú:</p>
<ul>{firmas}</ul>
{ejecuta}
<div class="nota"><b>Se firma antes de la sesión, no durante.</b> Una tesis que llega a
medio mercado ya viene contaminada por el precio. Lo que se opera de 7:00 a 8:30 se
decidió antes de que abriera.</div>

<h2>LO QUE TE VA A LLEGAR AL CORREO</h2>
<p>El terminal avisa solo. No hay que estar entrando a ver si pasó algo:</p>
<div class="caja">
  <div class="par"><span class="k">6:20</span><span class="v2">Resumen del overnight, con gráficas y los niveles de la noche</span></div>
  <div class="par"><span class="k">6:50</span><span class="v2">La ventana abre a las 7:00 — con lo que quedó pendiente de firmar</span></div>
  <div class="par"><span class="k">7:20</span><span class="v2">El rango de apertura empieza a las 7:30</span></div>
  <div class="par"><span class="k">8:35</span><span class="v2">Cerró la ventana — los trades del día y si se cumplió la meta</span></div>
  <div class="par"><span class="k">DÍA 1 Y 16</span><span class="v2">Corte de quincena, con el estado de cada cuenta</span></div>
</div>
<p>Y además, en cuanto pasa: una <b>tesis nueva</b> esperando firmas, <b>cada firma</b>
que se agrega y a quién le toca la siguiente, una tesis <b>lista para ejecutar</b>,
<b>cada trade</b> que alguien registra con su resultado, y las alertas de riesgo cuando
una cuenta se acerca a su límite.</p>
<p>Cuando te toque firmar, te va a llegar un correo. No hay excusa de «no me enteré».</p>

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


def candidato():
    """El documento que baja quien se registra en la landing.

    Éste sí es público y va en el repositorio: no lleva ninguna credencial. Lo que
    dice tiene que ser cierto — nadie llega a una llamada creyendo otra cosa.
    """
    hoy = date.today()
    fecha = f'{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}'
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Northpoint · Posiciones</title>
{ESTILOS}</head><body>

<div class="marca">NORTHPOINT CAPITAL MANAGEMENT</div>

<h1>Antes de la llamada.</h1>
<p class="sub">Lo que hacemos y qué esperamos de ti. {fecha}.</p>

<p>Gracias por registrarte. Este documento existe para que llegues a la llamada
sabiendo dónde te estás metiendo — y para que, si no es para ti, lo descubras aquí
en veinte minutos de lectura y no en tres meses.</p>

<h2>QUÉ ES NORTHPOINT</h2>
<p>Una mesa de futuros pequeña con un protocolo cerrado. Se opera una sola ventana al
día, de 7:00 a 8:30 de la mañana, de lunes a viernes. Máximo dos operaciones por
sesión. Fuera de esa franja la mesa está cerrada.</p>
<p>No es una señal que copias ni una comunidad de Discord. Es un proceso: se propone
una tesis por escrito, la firman cuatro puertas distintas —Research, Riesgo, Quant y
CIO— y sólo con las cuatro se ejecuta. Cada operación queda registrada con su
resultado y su análisis, salga bien o mal.</p>

<h2>CÓMO SE ENTRA</h2>
<ol>
  <li><b>La llamada.</b> Veinte minutos. Nos cuentas qué haces hoy y te decimos con
      honestidad si esto encaja contigo. A veces la respuesta es no, y es mejor
      decirla de una vez.</li>
  <li><b>El bootcamp.</b> Un mes de formación: futuros, estructura de mercado,
      liquidez, el rango de apertura, gestión de riesgo y psicología. Con material
      propio y avance medido.</li>
  <li><b>Simulado.</b> Operas el protocolo completo en simulado hasta que la conducta
      sea consistente. <b>Nadie toca capital real el primer día</b>, ni el primer mes.</li>
  <li><b>Cuenta.</b> Si el proceso se sostiene, se pasa a evaluación con una cuenta de
      fondeo. Ahí empieza lo de verdad.</li>
</ol>

<h2>QUÉ ESPERAMOS DE TI</h2>
<ol>
  <li><b>Noventa minutos al día, todos los días hábiles.</b> No es un pasatiempo de
      ratos libres. Si no puedes estar a las 7:00 de la mañana de lunes a viernes,
      esto no va a funcionar.</li>
  <li><b>Que escribas lo que hiciste, sobre todo cuando sale mal.</b> El journal no es
      trámite: es la materia prima con la que se corrige. Las violaciones de
      disciplina se marcan solas y no se borran.</li>
  <li><b>Que aceptes que otro te firme o te frene.</b> El Riesgo puede detener la mesa
      sin pedirte permiso. Si eso te molesta de entrada, mejor no.</li>
  <li><b>Paciencia con el resultado.</b> Un día perdedor operado dentro del protocolo
      es un día profesional. Un día ganador que rompió las reglas es un pasivo.</li>
</ol>

<h2>QUÉ NO ES</h2>
<p>No es un empleo con sueldo fijo ni una promesa de rendimiento. No vendemos un curso
ni cobramos por entrar. No hay garantía de que llegues a operar capital: eso depende de
que el proceso se sostenga, y no todo el mundo lo sostiene.</p>
<p>Operar futuros implica riesgo real de pérdida. Cualquiera que te prometa lo
contrario te está mintiendo.</p>

<h2>QUÉ SIGUE</h2>
<p>Agenda la llamada desde la página donde bajaste este documento. Llega habiendo
leído esto: la conversación va a ser sobre lo que acabas de leer, no sobre tu
currículum.</p>

<div class="pie">NORTHPOINT CAPITAL MANAGEMENT · DOCUMENTO INFORMATIVO · NO CONSTITUYE OFERTA</div>
</body></html>"""


def a_pdf(html_txt, destino):
    tmp = destino.parent / ('_' + destino.stem + '.html')
    tmp.write_text(html_txt, encoding='utf-8')
    subprocess.run(
        [CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
         f'--print-to-pdf={destino}', tmp.as_uri()],
        check=True, capture_output=True)
    tmp.unlink()
    print(f'  → {destino}  ({destino.stat().st_size // 1024} KB)')


def main():
    if not Path(CHROME).exists():
        print(f'No encuentro Chrome en {CHROME}', file=sys.stderr)
        return 1
    SALIDA.mkdir(exist_ok=True)
    (SALIDA / '.gitignore').write_text(
        '# Estas hojas llevan contraseñas y el repositorio es publico.\n*\n')

    print('Hojas de los socios (con contraseñas, fuera del repositorio):')
    for s in SOCIOS:
        a_pdf(hoja(s), SALIDA / f'Northpoint-{s["nombre"]}.pdf')

    print('\nDocumento del candidato (público, sí va al repositorio):')
    PUBLICO.mkdir(exist_ok=True)
    a_pdf(candidato(), PUBLICO / 'Northpoint-Posiciones.pdf')

    print(f'\n{SALIDA} NO se sube: lleva contraseñas.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
