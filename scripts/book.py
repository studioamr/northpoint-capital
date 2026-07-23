#!/usr/bin/env python3
"""
Genera el Kit de Bienvenida de Northpoint en PDF, uno por socio.

Es un libro, no un informe: portada, carta, índice y capítulos con aire. No vende
la estrategia ni justifica cifras — eso vive en docs/AUDITORIA-OPERATIVA.md. Aquí
va lo que se le entrega a alguien el primer día: quiénes somos, cuál es su lugar,
cómo se opera, qué no se negocia y cómo entrar.

Se arma en HTML y se imprime con Chrome sin ventana, así que el texto es vectorial.

    python3 scripts/book.py     → docs/book/NORTHPOINT-<Socio>.pdf
"""
import html
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'docs' / 'book'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
TERMINAL = 'https://studioamr.github.io/northpoint-capital/app.html'

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
         'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

ROLES = {
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
    {'usuario': 'pablo.np', 'nombre': 'Pablo', 'correo': 'pablo@northpoint.mx',
     'roles': ['NP-001', 'NP-010'], 'firma': 'CIO',
     'sintesis': 'Decides qué se opera y firmas al final. Nada se ejecuta sin ti.'},
    {'usuario': 'mateo.np', 'nombre': 'Mateo', 'correo': 'mateo@northpoint.mx',
     'roles': ['NP-020', 'NP-030'], 'firma': 'riesgo',
     'sintesis': 'Eres el freno. Puedes detener la mesa sin pedirle permiso a nadie.'},
    {'usuario': 'andre.np', 'nombre': 'André', 'correo': 'andre@northpoint.mx',
     'roles': ['NP-040', 'NP-050'], 'firma': 'quant',
     'sintesis': 'Mides. Si un número no cierra, lo dices aunque incomode.'},
]

CAPS = [
    ('I', 'La casa'), ('II', 'Tu lugar en la mesa'), ('III', 'El día'),
    ('IV', 'Lo que no se negocia'), ('V', 'Cómo entra un trade'),
    ('VI', 'Tu acceso'), ('VII', 'Tu formación'), ('VIII', 'Lo que esperamos'),
]

NO_NEGOCIABLES = [
    ('Nunca micros', 'Operar MNQ, MES, MYM o M2K está prohibido. Sin excepciones.'),
    ('Sólo la ventana de 7:00 a 8:30',
     'Hora de Nueva York, de lunes a viernes. Fuera de ahí no se opera. Punto.'),
    ('Nada abierto después de 8:30',
     'El día termina cuando termina la ventana, no cuando te sientas listo.'),
    ('Sin setup, no se opera',
     'Si el checklist no da setup válido, el mejor trade del día es no operar.'),
    ('Dos operaciones como máximo',
     'Y si ganas la primera, se cierra la plataforma. No hay nada más que demostrar.'),
]

FIRMAS = [
    ('Se propone la tesis',
     'Cualquiera la abre en la mesa de aprobaciones: instrumento, dirección y el '
     'argumento por escrito.'),
    ('Firma research', 'Se revisa que el argumento se sostenga con evidencia, no con opinión.'),
    ('Firma riesgo', 'Se confirma que el tamaño y el stop caben en el riesgo del día.'),
    ('Firma quant', 'Se verifica que los números cuadren y que no se rompa ningún límite.'),
    ('Firma el CIO', 'Se aprueba o se rechaza. Sin esa firma no se ejecuta.'),
    ('Se ejecuta y se documenta',
     'La tesis queda cerrada cuando el trade existe en el journal, con su screenshot.'),
]

ESPERAMOS = [
    ('Que registres todo',
     'Cada operación con su hora, su precio, su tamaño y qué viste. Un trade sin '
     'documentar no ocurrió.'),
    ('Que respetes la ventana',
     'Noventa minutos al día. Lo que no cabe ahí, no se opera.'),
    ('Que digas cuando algo no cuadra',
     'Aquí se prefiere una discusión incómoda a un número maquillado. Nadie se enoja '
     'por una objeción bien puesta.'),
    ('Que sostengas tu firma',
     'Si firmaste una tesis, respondes por ella. Y si no la firmaste, no se ejecuta.'),
]


def documento(s):
    hoy = date.today()
    fecha = f'{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}'
    cargos = ' · '.join(ROLES[r][0] for r in s['roles'])
    nombre = html.escape(s['nombre'])

    indice = ''.join(
        f'<div class="ix"><span class="rn">{n}</span><span class="ti">{html.escape(t)}</span></div>'
        for n, t in CAPS)

    deberes = ''.join(
        f'<div class="cargo"><div class="cargo-h">{html.escape(ROLES[r][0])}'
        f'<span>{r}</span></div><ul>'
        + ''.join(f'<li>{html.escape(d)}</li>' for d in ROLES[r][1])
        + '</ul></div>'
        for r in s['roles'])

    nn = ''.join(f'<div class="regla"><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>'
                 for t, d in NO_NEGOCIABLES)
    firmas = ''.join(f'<div class="paso"><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>'
                     for t, d in FIRMAS)
    esperamos = ''.join(f'<div class="regla"><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>'
                        for t, d in ESPERAMOS)

    def cap(num, titulo, cuerpo, primero=False):
        salto = '' if primero else ' style="page-break-before:always"'
        return (f'<section{salto}><div class="cap-h"><span class="cap-n">{num}</span>'
                f'<h2>{html.escape(titulo)}</h2></div>{cuerpo}</section>')

    c1 = cap('I', 'La casa', '''
  <p class="entrada">Somos una mesa de tres socios con dos departamentos y una sola
  forma de trabajar.</p>
  <div class="dep"><b>Mesa de futuros</b>
  <p>Operación diaria sobre futuros del Nasdaq en una sola ventana de noventa minutos,
  de 7:00 a 8:30 de la mañana, hora de Nueva York. El capital viene de cuentas fondeadas
  que operamos en paralelo con una copiadora: una misma orden cae en todas.</p></div>
  <div class="dep"><b>Snowball Investments</b>
  <p>Capital de clientes con horizonte largo. Seis puertas antes de tomar una posición
  y rebalanceo trimestral. Aquí la paciencia no es una virtud, es el método.</p></div>
  <p>Lo que distingue a la casa no es la estrategia — hay cientos parecidas. Es que todo
  queda escrito, y que ninguno de los tres puede mover dinero solo.</p>''', primero=True)

    c2 = cap('II', 'Tu lugar en la mesa', f'''
  <p class="entrada">{html.escape(s['sintesis'])}</p>
  <p>Llevas dos cargos. No son títulos decorativos: cada uno tiene deberes que los
  otros dos socios dan por hechos.</p>
  {deberes}''')

    c3 = cap('III', 'El día', '''
  <p class="entrada">Noventa minutos. Todo lo demás es preparación o registro.</p>
  <p><b>Antes de las 7:00.</b> Se abre el protocolo del día en el terminal: plataforma
  lista, calendario económico revisado, liquidez de la noche marcada, estado de cada
  cuenta y bias definido. Seis puntos, cada uno firmado por quien lo revisó.</p>
  <p><b>De 7:00 a 8:30.</b> Se espera la apertura y el rango. Si el checklist de setup
  no da las cuatro condiciones, no hay trade — y ese día se cierra igual de bien que
  uno ganador.</p>
  <p><b>Después de las 8:30.</b> Se registra cada operación con su screenshot, se
  revisa el tablero y se manda el reporte al equipo. La plataforma se cierra.</p>
  <p>Si ganas el primer trade, el día terminó. Ésa es probablemente la regla más difícil
  de sostener y la que más dinero salva.</p>''')

    c4 = cap('IV', 'Lo que no se negocia', f'''
  <p class="entrada">Cinco reglas. Cuando alguna parece inconveniente es justo cuando
  más se necesita.</p>
  {nn}
  <p style="margin-top:6mm">El terminal las vigila solo: marca la violación, la deja
  asentada en el journal y te topa el grado del Score conductual. No hay forma de
  saltárselas en silencio, y ése es el punto.</p>''')

    c5 = cap('V', 'Cómo entra un trade', f'''
  <p class="entrada">Ninguna operación se ejecuta sin cuatro firmas.</p>
  <div class="pasos">{firmas}</div>
  <p style="margin-top:6mm">Tu firma en este circuito es
  <span class="m">{html.escape(s['firma'])}</span>. Dos socios pueden firmar al mismo
  tiempo desde equipos distintos sin borrarse: el terminal las suma.</p>''')

    c6 = cap('VI', 'Tu acceso', f'''
  <p class="entrada">Todo pasa por el terminal. Es donde se firma, se registra y se
  rinde cuentas.</p>
  <div class="acceso">
    <div class="f"><span>Terminal</span><b>{TERMINAL}</b></div>
    <div class="f"><span>Tu usuario</span><b>{html.escape(s['usuario'])}</b></div>
    <div class="f"><span>Contraseña la primera vez</span><b>1234</b></div>
  </div>
  <p class="nota">Cámbiala en cuanto entres: Configuración → Cambiar contraseña.
  Mientras sigas con la de fábrica el terminal te lo recuerda con una advertencia,
  porque cualquiera que conozca tu usuario podría entrar. Y no la compartas por
  escrito con nadie, ni siquiera con los otros dos.</p>
  <p>Entrando con tu cuenta ves la misma mesa que ellos: las mismas tesis, las mismas
  firmas, el mismo journal. Si el indicador de la vista de aprobaciones dice
  <span class="m">SINCRONIZADA</span>, estás viendo lo mismo. Si dice otra cosa,
  resuélvelo antes de firmar nada.</p>''')

    c7 = cap('VII', 'Tu formación', '''
  <p class="entrada">Hablar el mismo idioma no es opcional cuando tres personas firman
  la misma operación.</p>
  <p>Dentro del terminal, en <b>Curso</b>, están treinta días en orden. Se abren uno
  por uno: el siguiente se destraba cuando marcas el anterior. No es relleno — es el
  vocabulario común de la mesa. Cuando alguien diga «barrido de liquidez» en la ventana
  de las 7:15, los tres tenemos que estar pensando en lo mismo.</p>
  <p>Debajo del curso están los documentos propios de la casa: siete módulos escritos
  por nosotros sobre cómo operamos aquí, con sus diagramas. Ésos se leen una vez y se
  vuelven a consultar toda la vida.</p>''')

    c8 = cap('VIII', 'Lo que esperamos', f'''
  <p class="entrada">Cuatro cosas. Ninguna tiene que ver con ganar dinero.</p>
  {esperamos}
  <div class="cierre">
    <p class="lema">El tamaño se administra. La precisión se construye.</p>
    <div class="pie">
      <span>Northpoint Capital Management</span>
      <span>{nombre} · {html.escape(fecha)}</span>
    </div>
  </div>''')

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Northpoint · Kit de bienvenida · {nombre}</title>
<style>
  @page {{ size: Letter; margin: 24mm 22mm; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  html {{ -webkit-print-color-adjust:exact; print-color-adjust:exact;
          color-scheme:light; background:#fff; }}
  body {{ font-family:Georgia,"Times New Roman",serif; background:#fff; color:#1a1a1a;
          font-size:11pt; line-height:1.72; }}
  .m {{ font-family:"SF Mono",Menlo,Consolas,monospace;
        font-variant-numeric:tabular-nums slashed-zero; }}

  .portada {{ height:249mm; display:flex; flex-direction:column; page-break-after:always; }}
  .marca {{ font-family:"SF Mono",Menlo,monospace; font-size:8pt; letter-spacing:.4em; }}
  .portada .centro {{ margin:auto 0; }}
  .portada .kicker {{ font-family:"SF Mono",Menlo,monospace; font-size:8pt;
                      letter-spacing:.3em; color:#999; text-transform:uppercase; }}
  .portada h1 {{ font-size:40pt; line-height:1.02; letter-spacing:-.025em;
                 font-weight:400; margin:7mm 0 0; }}
  .portada .barra {{ width:26mm; height:2px; background:#1a1a1a; margin:9mm 0; }}
  .portada .para {{ font-family:"SF Mono",Menlo,monospace; font-size:8pt;
                    letter-spacing:.24em; color:#999; text-transform:uppercase; }}
  .portada .quien {{ font-size:19pt; margin-top:2mm; }}
  .portada .cargo {{ font-size:10.5pt; color:#666; font-style:italic; margin-top:1mm; }}
  .portada .pie {{ display:flex; justify-content:space-between;
                   font-family:"SF Mono",Menlo,monospace; font-size:7pt;
                   letter-spacing:.2em; color:#aaa; text-transform:uppercase; }}

  .carta {{ page-break-after:always; padding-top:6mm; }}
  .carta .de {{ font-family:"SF Mono",Menlo,monospace; font-size:7.5pt;
                letter-spacing:.24em; color:#999; text-transform:uppercase;
                margin-bottom:8mm; }}
  .carta p {{ margin-bottom:5mm; max-width:142mm; }}
  .carta .primera::first-letter {{ float:left; font-size:30pt; line-height:.86;
                                   padding:1mm 2mm 0 0; }}
  .firma-carta {{ margin-top:10mm; }}
  .firma-carta .n {{ font-size:12pt; }}
  .firma-carta .c {{ font-family:"SF Mono",Menlo,monospace; font-size:7.5pt;
                     letter-spacing:.2em; color:#999; text-transform:uppercase; }}

  .indice {{ page-break-after:always; padding-top:6mm; }}
  .indice h3 {{ font-family:"SF Mono",Menlo,monospace; font-size:8pt; letter-spacing:.3em;
                text-transform:uppercase; color:#999; font-weight:400; margin-bottom:8mm; }}
  .ix {{ display:flex; align-items:baseline; gap:7mm; padding:3.4mm 0;
         border-bottom:1px solid #ececec; }}
  .ix .rn {{ font-family:"SF Mono",Menlo,monospace; font-size:8.5pt; color:#bbb;
             min-width:11mm; letter-spacing:.1em; }}
  .ix .ti {{ font-size:13pt; }}

  .cap-h {{ margin-bottom:8mm; }}
  .cap-n {{ font-family:"SF Mono",Menlo,monospace; font-size:8pt; letter-spacing:.3em;
            color:#bbb; display:block; }}
  h2 {{ font-size:23pt; font-weight:400; letter-spacing:-.02em; margin-top:2mm; }}
  p {{ margin-bottom:4mm; max-width:150mm; }}
  .entrada {{ font-size:12.5pt; line-height:1.62; color:#333; margin-bottom:6mm; }}
  .dep {{ margin-bottom:5mm; }}
  .dep b {{ display:block; font-size:12pt; font-weight:400; font-style:italic;
            margin-bottom:1mm; }}

  .cargo {{ margin-bottom:7mm; page-break-inside:avoid; }}
  .cargo-h {{ display:flex; justify-content:space-between; align-items:baseline;
              border-bottom:1px solid #1a1a1a; padding-bottom:2mm; margin-bottom:3mm;
              font-size:12.5pt; }}
  .cargo-h span {{ font-family:"SF Mono",Menlo,monospace; font-size:7.5pt;
                   letter-spacing:.18em; color:#aaa; }}
  .cargo ul {{ list-style:none; }}
  .cargo li {{ position:relative; padding-left:6mm; margin-bottom:2mm; }}
  .cargo li::before {{ content:'·'; position:absolute; left:1.5mm; color:#bbb; }}

  .regla, .paso {{ padding:3.6mm 0; border-bottom:1px solid #ececec;
                   page-break-inside:avoid; }}
  .regla:last-child, .paso:last-child {{ border-bottom:0; }}
  .regla b, .paso b {{ font-size:12pt; font-weight:400; font-style:italic; }}
  .regla p, .paso p {{ margin:1mm 0 0; color:#444; }}
  .pasos {{ counter-reset:p; }}
  .pasos .paso {{ padding-left:11mm; position:relative; }}
  .pasos .paso::before {{ counter-increment:p;
    content:counter(p,decimal-leading-zero); position:absolute; left:0; top:4.6mm;
    font-family:"SF Mono",Menlo,monospace; font-size:8pt; color:#bbb; letter-spacing:.1em; }}

  .acceso {{ border-top:1px solid #1a1a1a; border-bottom:1px solid #1a1a1a;
             padding:4mm 0; margin:5mm 0; }}
  .acceso .f {{ display:flex; justify-content:space-between; gap:8mm; padding:2.2mm 0; }}
  .acceso .f span {{ color:#777; }}
  .acceso .f b {{ font-family:"SF Mono",Menlo,monospace; font-weight:400;
                  text-align:right; font-size:10pt; }}
  .nota {{ font-size:10pt; color:#555; font-style:italic; }}

  .cierre {{ margin-top:12mm; padding-top:5mm; border-top:1px solid #1a1a1a; }}
  .cierre .lema {{ font-size:14pt; font-style:italic; max-width:120mm; }}
  .cierre .pie {{ margin-top:6mm; font-family:"SF Mono",Menlo,monospace; font-size:7pt;
                  letter-spacing:.2em; color:#aaa; text-transform:uppercase;
                  display:flex; justify-content:space-between; }}
</style></head><body>

<div class="portada">
  <div class="marca">NORTHPOINT CAPITAL MANAGEMENT</div>
  <div class="centro">
    <div class="kicker">Kit de bienvenida</div>
    <h1>Así se<br>trabaja aquí.</h1>
    <div class="barra"></div>
    <div class="para">Preparado para</div>
    <div class="quien">{nombre}</div>
    <div class="cargo">{html.escape(cargos)}</div>
  </div>
  <div class="pie"><span>Documento interno</span><span>{html.escape(fecha)}</span></div>
</div>

<div class="carta">
  <div class="de">Bienvenida</div>
  <p class="primera">Este libro es lo primero que se entrega en Northpoint, y es corto
  a propósito. No vas a encontrar aquí una promesa de rendimiento ni un argumento para
  convencerte de nada: eso se demuestra operando. Lo que vas a encontrar es cómo
  trabajamos, qué se espera de ti y dónde empieza y termina tu firma.</p>
  <p>Somos tres. Eso significa que no hay a quién echarle la culpa y que cada decisión
  tiene nombre. También significa que una sola persona distraída puede costarnos el mes,
  y por eso las reglas de las páginas siguientes no tienen excepción creativa.</p>
  <p>Vas a notar que casi todo aquí se trata de dejar registro: cada operación
  documentada, cada tesis firmada por cuatro manos, cada día con su checklist. No es
  burocracia. Es la única forma que conocemos de distinguir una buena decisión de un
  buen resultado, que no son lo mismo.</p>
  <p>Léelo completo hoy. Te va a tomar quince minutos y te ahorra todas las
  conversaciones incómodas de las primeras semanas.</p>
  <div class="firma-carta">
    <div class="n">André</div>
    <div class="c">Quantitative Analyst · Chief Operating Officer</div>
  </div>
</div>

<div class="indice">
  <h3>Contenido</h3>
  {indice}
</div>

{c1}{c2}{c3}{c4}{c5}{c6}{c7}{c8}

</body></html>"""


def main():
    if not Path(CHROME).exists():
        print('No encontré Google Chrome; es lo que imprime el PDF.', file=sys.stderr)
        return 1
    SALIDA.mkdir(parents=True, exist_ok=True)
    ok = 0
    for s in SOCIOS:
        # sin acentos en el nombre: algunos clientes de mensajería rompen la liga
        slug = s['nombre'].translate(str.maketrans('ÁÉÍÓÚÑáéíóúñ', 'AEIOUNaeioun'))
        htm = SALIDA / f'_{slug}.html'
        pdf = SALIDA / f'NORTHPOINT-{slug}.pdf'
        htm.write_text(documento(s), encoding='utf-8')
        r = subprocess.run(
            [CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
             f'--print-to-pdf={pdf}', htm.as_uri()],
            capture_output=True, text=True, timeout=120)
        if not pdf.exists():
            print(f"  ! {s['nombre']}: no se generó\n{r.stderr[:400]}", file=sys.stderr)
            continue
        htm.unlink()
        ok += 1
        print(f"  {s['nombre']:8s} → {pdf.name} ({pdf.stat().st_size // 1024} KB)")
    return 0 if ok == len(SOCIOS) else 1


if __name__ == '__main__':
    sys.exit(main())
