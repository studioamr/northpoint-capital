#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""El feed de Instagram de NORTHPOINT · seis piezas de 1080×1350.

Una por cada FRENTE del programa —los mismos seis que manda el sitio— y cada una
montada sobre una FOTOGRAFÍA real generada en Gemini, no sobre dibujo. Ésa fue la
corrección de André: los conceptos se diseñan con fotografía, y los temas salen de
los seis frentes, no de ocurrencias sueltas.

Las fotos viven en `fondos/`. El código sólo pone encima la capa de tipografía: un
rótulo mono arriba, el titular abajo y la firma. Nada más — la foto ya trae toda la
atmósfera, y meterle gráficos flotando la convertiría en el mismo cartel de trading
que hace ruido en Instagram.

Regla que manda sobre el copy: NO hay una sola cifra inventada. Lo que se promete
aquí es lo mismo que el sitio ya promete, palabra por palabra.

    /usr/local/bin/python3 generar.py
"""
import io, os, subprocess

RAIZ   = '/Users/andremacouzet/claude/northpoint/marca/instagram'
FONDOS = os.path.join(RAIZ, 'fondos')
TMP    = '/private/tmp/claude-501/-Users-andremacouzet-claude/0988e467-1d40-43c4-a642-7f65ccea31c3/scratchpad/ig'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
os.makedirs(TMP, exist_ok=True)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;position:relative;background:#080808;
  font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}

/* LA FOTO. `cover` con el foco un poco arriba del centro: en las seis fotos el
   sujeto vive en el tercio superior y el aire de abajo es donde entra el texto.
   El filtro las empareja — vienen de seis prompts distintos y sin esto se nota
   que unas salieron más cálidas que otras. */
.foto{position:absolute;inset:0;background-size:cover;background-position:center 34%;
  filter:saturate(.6) contrast(1.05) brightness(.98)}

/* El velo. Dos gradientes en vez de uno plano: si se oscurece pareja la foto se
   apaga entera; así la imagen respira arriba y el texto de abajo cae sobre negro
   casi sólido, que es lo único que garantiza que se lea en un teléfono. */
.velo{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(8,8,8,.72) 0%,rgba(8,8,8,.22) 24%,
    rgba(8,8,8,.40) 46%,rgba(8,8,8,.93) 78%,#080808 100%)}
/* El suelo del titular. Sin esto, en la foto del cuaderno el texto blanco cae
   justo sobre la página iluminada y se lava: el degradado de arriba es parejo y
   no sabe dónde está el texto. Éste sí — entra por la esquina de abajo a la
   izquierda, que es exactamente donde vive el bloque. */
.suelo{position:absolute;inset:0;
  background:radial-gradient(120% 62% at 6% 92%,rgba(8,8,8,.92) 0%,
    rgba(8,8,8,.55) 42%,rgba(8,8,8,0) 74%)}
.grano{position:absolute;inset:0;opacity:.16;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'>\
<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/></filter>\
<rect width='140' height='140' filter='url(%23n)' opacity='.5'/></svg>")}

.cap{position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:space-between;padding:92px 84px 84px;color:#F4F4F4}

.eyebrow{display:flex;align-items:center;gap:18px;
  font-family:ui-monospace,Menlo,monospace;font-size:18px;letter-spacing:.32em;
  text-transform:uppercase;color:#C8A24A}
.eyebrow i{display:block;width:44px;height:1px;background:#C8A24A;opacity:.7}
.eyebrow b{font-weight:400;color:rgba(244,244,244,.55);margin-left:auto;
  letter-spacing:.28em}

h1{font-size:96px;line-height:.98;letter-spacing:-.042em;font-weight:600;
  text-wrap:balance;text-shadow:0 2px 40px rgba(0,0,0,.55)}
h1.chico{font-size:74px;line-height:1.03}
h1 em{font-style:normal;color:#C8A24A}
.sub{font-size:29px;line-height:1.44;font-weight:300;color:rgba(244,244,244,.72);
  margin-top:34px;max-width:23ch;text-shadow:0 2px 30px rgba(0,0,0,.6)}

.firma{display:flex;justify-content:space-between;align-items:flex-end;
  margin-top:56px;padding-top:30px;border-top:1px solid rgba(244,244,244,.16)}
.firma b{display:block;font-size:25px;letter-spacing:.26em;font-weight:600}
.firma b span{display:block;font-family:ui-monospace,Menlo,monospace;font-size:13px;
  letter-spacing:.3em;font-weight:400;color:rgba(244,244,244,.5);margin-top:11px}
.firma u{text-decoration:none;font-family:ui-monospace,Menlo,monospace;font-size:15px;
  letter-spacing:.2em;color:rgba(244,244,244,.6)}
"""

# ── los seis frentes, en el mismo orden que el sitio ──────────────────────────
# nombre · foto · rótulo · clase del titular · titular · bajada
POSTS = [
 ('01-conocimiento', '01-conocimiento.jpeg', 'FRENTE 01 · EL CONOCIMIENTO', '',
  'Ocho módulos.<br>Más de 48 horas.<br>Las veces<br>que quieras.',
  'El bootcamp completo, las clases en vivo con preguntas y la biblioteca de '
  'sesiones grabadas.'),

 ('02-tecnologia', '02-tecnologia.jpeg', 'FRENTE 02 · LA TECNOLOGÍA', 'chico',
  'No es un curso<br>con un PDF.<br><em>Es el Terminal.</em>',
  'Cada trade escrito el mismo día, el camino a payout en vivo y las reglas de tu '
  'fondeadora vigiladas.'),

 ('03-mesa-en-vivo', '03-mesa-en-vivo.jpeg', 'FRENTE 03 · LA MESA EN VIVO', 'chico',
  'La sesión<br>de Nueva York,<br>operada<br>delante de ti.',
  'Lunes a viernes. Incluidos los días en que no hay trade — ésos son los que '
  'enseñan.'),

 ('04-comunidad', '04-comunidad.jpeg', 'FRENTE 04 · LA COMUNIDAD', '',
  'Entra gratis<br>antes de<br>pagar nada.',
  'El Discord está abierto y la mesa transmite todos los días. Míralo trabajar y '
  'luego decides.'),

 ('05-uno-a-uno', '05-uno-a-uno.jpeg', 'FRENTE 05 · UNO A UNO', 'chico',
  'Tres sesiones<br>privadas<br>con la mesa.',
  'Tu journal revisado con tus propios números, y tu plan de ataque a la '
  'evaluación. Sólo en De por vida.'),

 ('06-programas', '06-programas.jpeg', 'FRENTE 06 · LOS PROGRAMAS', 'chico',
  'Demuéstralo<br>y te pagamos<br>la evaluación.',
  'Mandas tu historial de payouts, lo revisamos y te contestamos — aceptado o no. '
  'Aplicar no cuesta nada.'),

 # ── segunda tanda: las tres REGLAS ──────────────────────────────────────────
 # Los seis frentes de arriba dicen qué se entrega. Éstas dicen cómo se opera —
 # que es lo que de verdad distingue a la mesa de cualquier curso, y lo único
 # que un competidor no puede copiar pegando una lista de módulos.
 ('07-paciencia', '07-paciencia.jpeg', 'LA REGLA · PACIENCIA', '',
  'La paciencia<br>es la ventaja.<br><em>Todo lo demás<br>es ruido.</em>',
  'El leopardo no corre detrás de todo lo que se mueve. Espera el único momento '
  'en que no puede fallar.'),

 ('08-un-trade', '08-un-trade.jpeg', 'LA REGLA · LA CADENCIA', '',
  'Un trade<br>al día.',
  'Gane o pierda, se acabó. Sin revancha y sin segundo intento. La cuenta se '
  'quema en el tercero, no en el primero.'),

 ('09-el-record', '09-el-record.jpeg', 'EL RÉCORD', 'chico',
  '13 payouts<br>cobrados.<br>Dos fondeadoras.',
  'Es el número que hay, y está en el sitio con nombre y apellido. Los resultados '
  'pasados no predicen nada.'),
]

# Retoque por foto. Salen de seis prompts distintos y el filtro común no las
# empareja: la de la comunidad viene con pantallas azules y rojas que pelean con
# la paleta, y la de uno a uno salió mucho más clara que las otras cinco — en la
# cuadrícula del perfil se ve como un hueco blanco. Se corrige aquí, no pidiendo
# la foto otra vez: es el mismo trabajo que haría un editor con una foto de stock.
AJUSTE = {
    '04-comunidad': 'filter:saturate(.2) contrast(1.12) brightness(.72)',
    '05-uno-a-uno': 'filter:saturate(.3) contrast(1.12) brightness(.6)',
    # El leopardo salió camuflado de verdad —que es justo lo que hace un leopardo—
    # pero en un cuadro de Instagram eso es un rectángulo negro. Se acerca la toma
    # y se sube el brillo para que la cabeza quede ARRIBA del bloque de texto: si
    # el titular le cae encima, se pierden los dos.
    '07-paciencia': 'background-size:150%;background-position:44% 74%;'
                    'filter:saturate(.72) contrast(1.02) brightness(1.55)',
}

def pieza(foto, rotulo, clase, titular, bajada, ajuste=''):
    return """<div class="foto" style="background-image:url('file://%s');%s"></div>
<div class="velo"></div><div class="suelo"></div><div class="grano"></div>
<div class="cap">
  <p class="eyebrow"><i></i>%s<b>NORTHPOINT</b></p>
  <div>
    <h1 class="%s">%s</h1>
    <p class="sub">%s</p>
    <div class="firma">
      <b>NORTHPOINT<span>RESPALDO A TRADERS</span></b>
      <u>northpointcapital.io</u>
    </div>
  </div>
</div>""" % (foto, ajuste, rotulo, clase, titular, bajada)

hechos, faltan = [], []
for nombre, archivo, rotulo, clase, titular, bajada in POSTS:
    foto = os.path.join(FONDOS, archivo)
    if not os.path.exists(foto):
        faltan.append(archivo); continue
    html = '<style>%s</style>\n%s' % (
        CSS, pieza(foto, rotulo, clase, titular, bajada, AJUSTE.get(nombre, '')))
    f = os.path.join(TMP, nombre + '.html')
    io.open(f, 'w', encoding='utf-8').write(html)
    png = os.path.join(RAIZ, nombre + '.png')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    '--allow-file-access-from-files',
                    '--window-size=1080,1350', '--screenshot=' + png, 'file://' + f],
                   capture_output=True)
    hechos.append((nombre, os.path.getsize(png) if os.path.exists(png) else 0))

for n, t in hechos:
    print('%-20s %6.0f KB' % (n, t / 1024))
if faltan:
    print('\nfaltan fotos: ' + ', '.join(faltan))

# ── la hoja de contacto: cómo se ve el perfil ─────────────────────────────────
if hechos:
    grid = ''.join('<img src="file://%s/%s.png">' % (RAIZ, n) for n, _ in hechos)
    hoja = ('<style>*{margin:0;padding:0}body{background:#0B0B0B;width:1000px;display:grid;'
            'grid-template-columns:repeat(3,1fr);gap:5px;padding:5px}'
            'img{width:100%%;display:block}</style>%s' % grid)
    hf = os.path.join(TMP, 'hoja.html')
    io.open(hf, 'w', encoding='utf-8').write(hoja)
    filas = (len(hechos) + 2) // 3
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    '--allow-file-access-from-files',
                    '--window-size=1000,%d' % (10 + filas * 419),
                    '--screenshot=' + os.path.join(RAIZ, '_hoja-de-contacto.png'),
                    'file://' + hf], capture_output=True)
    print('\nhoja de contacto: ' + os.path.join(RAIZ, '_hoja-de-contacto.png'))
