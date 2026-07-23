#!/usr/bin/env python3
"""
Genera el Libro del Socio en PDF, uno por cada integrante de la mesa.

Se arma en HTML y se imprime con Chrome sin ventana (--headless --print-to-pdf),
que da control tipográfico completo y texto vectorial de verdad — nada de imágenes.

    python3 scripts/book.py          → docs/book/NORTHPOINT-<Socio>.pdf

Los cargos, deberes y reglas salen de app.html y del catálogo verificado de la
fondeadora: este documento no inventa cifras.
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
    {'usuario': 'pablo', 'nombre': 'Pablo', 'correo': 'pablo@northpoint.mx',
     'roles': ['NP-001', 'NP-010'], 'firma': 'cio',
     'frase': 'Tú decides qué se opera y firmas al final. Nadie ejecuta sin tu firma.'},
    {'usuario': 'mateo', 'nombre': 'Mateo', 'correo': 'mateo@northpoint.mx',
     'roles': ['NP-020', 'NP-030'], 'firma': 'riesgo',
     'frase': 'Tú eres el freno. Tienes autoridad para detener la mesa sin pedir permiso.'},
    {'usuario': 'andre', 'nombre': 'André', 'correo': 'andre@northpoint.mx',
     'roles': ['NP-040', 'NP-050'], 'firma': 'quant',
     'frase': 'Tú mides. Si un número no cierra, se dice aunque incomode.'},
]

NO_NEGOCIABLES = [
    ('Nunca micros', 'Operar MNQ, MES, MYM o M2K está prohibido. Sin excepciones. '
                     'El terminal lo marca como violación y te topa el grado del Score.'),
    ('Sólo la ventana 7:00 – 8:30', 'Hora de Nueva York, de lunes a viernes. '
                                    'Fuera de esa ventana no se opera. Punto.'),
    ('Nada abierto después de 8:30', 'Toda posición cerrada antes de las 8:30. '
                                     'El día termina cuando termina la ventana, no cuando te sientas listo.'),
    ('Sin setup, no se opera', 'Si el checklist no da setup válido, el mejor trade del día es no operar. '
                               'Un día sin operar es un día bien operado.'),
    ('Máximo dos operaciones', 'Dos por sesión, estrictas. Y si ganas la primera, se cierra la plataforma: '
                               'no hay nada más que demostrar ese día.'),
]

FASES = [
    ('Fase 1 · Evaluación', '50,000 → 53,000', [
        ('Objetivo', '$3,000 · dato de la fondeadora'),
        ('Drawdown máximo', '$2,000 · dato de la fondeadora'),
        ('Límite diario de la firma', 'no hay · la fondeadora no pone freno aquí'),
        ('Riesgo propio por día', '$1,000 · regla nuestra, no de ellos'),
        ('Consistencia', '40% del acumulado · ningún día puede concentrar más'),
        ('Días mínimos', '3'),
    ]),
    ('Fase 2 · Colchón', 'reinicia a 50,000 → 52,100', [
        ('Qué pasa al pasar', 'la cuenta REINICIA a $50,000: lo ganado en evaluación no se conserva'),
        ('Límite diario de la firma', '$1,000'),
        ('Riesgo propio por día', '$200'),
        ('Objetivo por día', '$400'),
        ('Por qué 52,100', 'el piso se congela en $50,100; $2,000 arriba es un drawdown completo de colchón'),
    ]),
    ('Fase 3 · Retiros', 'desde 52,100', [
        ('Riesgo propio por día', '$100'),
        ('Objetivo por día', '$200'),
        ('Reparto cada 15 días', 'cuentas 20% · portafolio 20% · Mateo 20% · Pablo 20% · André 20%'),
        ('Lo que queda inmovilizado', '$2,000 por cuenta que nunca se retira: es el colchón'),
    ]),
]

VERDADES = [
    ('La Fase 3 no da $30,000 al mes. Da $20,000.',
     '$200 por día × 5 cuentas × 20 días hábiles = $20,000. Contra la visión de $30,000 faltan '
     '$10,000 al mes y $120,000 al año. Para llegar a los $1,500 diarios harían falta 8 cuentas, '
     'no 5 — o subir el objetivo a $300 por cuenta con la mitad del riesgo, que exige un 3:1 con '
     'casi 100% de aciertos.'),
    ('Con la copiadora, 5 cuentas no son 5 apuestas.',
     'Son una apuesta con 5× de tamaño. El mismo trade cae en las cinco: o pasan todas o no pasa '
     'ninguna, y truenan el mismo día. El tamaño de muestra real del edge es 1, no 5.'),
    ('La Fase 1 es la más peligrosa y parece la más fácil.',
     'La evaluación NO tiene límite diario de la fondeadora: nadie te va a parar. Con $1,000 de '
     'riesgo diario contra un drawdown de $2,000, dos días malos seguidos truenan las cinco cuentas '
     'y el dinero de las evaluaciones.'),
    ('El P&L del mes no es dinero en el banco.',
     'Al aprobar cada evaluación la cuenta reinicia a $50,000 y esa ganancia desaparece contablemente. '
     'Lo que sobrevive es el colchón sobre el piso, y nada de eso es retirable hasta la Fase 3. '
     'Por eso el terminal muestra "saldo vivo" al lado del P&L bruto.'),
]


def bloque_socio(s):
    cargos = ' + '.join(ROLES[r][0] for r in s['roles'])
    deberes = ''.join(
        f'<div class="rol"><h4>{html.escape(ROLES[r][0])}<span>{r}</span></h4><ul>'
        + ''.join(f'<li>{html.escape(d)}</li>' for d in ROLES[r][1])
        + '</ul></div>'
        for r in s['roles'])
    return cargos, deberes


def documento(s):
    hoy = date.today()
    fecha = f'{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}'
    cargos, deberes = bloque_socio(s)

    nn = ''.join(
        f'<div class="nn"><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>'
        for t, d in NO_NEGOCIABLES)

    fases = ''
    for titulo, rango, filas in FASES:
        cuerpo = ''.join(
            f'<div class="fr"><span>{html.escape(k)}</span><b>{html.escape(v)}</b></div>'
            for k, v in filas)
        fases += (f'<div class="fase"><div class="fase-h"><h4>{html.escape(titulo)}</h4>'
                  f'<span class="rango">{html.escape(rango)}</span></div>{cuerpo}</div>')

    verdades = ''.join(
        f'<div class="verdad"><b>{html.escape(t)}</b><p>{html.escape(d)}</p></div>'
        for t, d in VERDADES)

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>NORTHPOINT · Libro del socio · {html.escape(s['nombre'])}</title>
<style>
  @page {{ size: Letter; margin: 18mm 16mm 16mm; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  html {{ -webkit-print-color-adjust:exact; print-color-adjust:exact;
          color-scheme:light; background:#fff; }}
  /* papel blanco siempre: un documento impreso no debe seguir el tema del visor */
  body {{ font-family:"Helvetica Neue",Helvetica,Arial,sans-serif; color:#111;
          background:#fff; font-size:10.5pt; line-height:1.6; }}
  .mono {{ font-family:"SF Mono",Menlo,Consolas,monospace; font-variant-numeric:tabular-nums slashed-zero; }}
  h1,h2,h3,h4 {{ font-weight:600; letter-spacing:-.01em; }}

  /* portada */
  .cover {{ height:232mm; display:flex; flex-direction:column; page-break-after:always; }}
  .cover .marca {{ font-family:"SF Mono",Menlo,monospace; font-size:8.5pt; letter-spacing:.34em; }}
  .cover .mid {{ margin-top:auto; }}
  .cover h1 {{ font-size:33pt; line-height:1.05; letter-spacing:-.03em; margin:5mm 0 3mm; }}
  .cover .quien {{ font-size:15pt; font-weight:500; }}
  .cover .cargo {{ font-family:"SF Mono",Menlo,monospace; font-size:8.5pt; letter-spacing:.18em;
                   text-transform:uppercase; color:#666; margin-top:2mm; }}
  .cover .frase {{ margin-top:9mm; padding-left:5mm; border-left:2px solid #111;
                   font-size:12pt; line-height:1.5; max-width:118mm; }}
  .cover .pie {{ margin-top:auto; display:flex; justify-content:space-between;
                 font-family:"SF Mono",Menlo,monospace; font-size:7.5pt; letter-spacing:.16em;
                 text-transform:uppercase; color:#777; border-top:1px solid #ddd; padding-top:3mm; }}

  section {{ page-break-inside:avoid; margin-bottom:9mm; }}
  .n {{ font-family:"SF Mono",Menlo,monospace; font-size:7.5pt; letter-spacing:.22em; color:#999; }}
  h2 {{ font-size:16pt; margin:1mm 0 4mm; letter-spacing:-.02em; }}
  p {{ margin-bottom:3mm; max-width:160mm; }}
  .lead {{ font-size:11.5pt; color:#333; }}

  .rol {{ margin-bottom:5mm; }}
  .rol h4 {{ font-size:11pt; display:flex; justify-content:space-between; align-items:baseline;
             border-bottom:1px solid #e2e2e2; padding-bottom:1.5mm; margin-bottom:2.5mm; }}
  .rol h4 span {{ font-family:"SF Mono",Menlo,monospace; font-size:7.5pt; letter-spacing:.16em; color:#999; }}
  .rol ul {{ list-style:none; }}
  .rol li {{ position:relative; padding-left:5mm; margin-bottom:1.5mm; color:#333; }}
  .rol li::before {{ content:'—'; position:absolute; left:0; color:#aaa; }}

  .acceso {{ border:1px solid #ddd; padding:5mm 6mm; }}
  .acceso .fr {{ display:flex; justify-content:space-between; gap:6mm; padding:2mm 0;
                 border-bottom:1px solid #eee; }}
  .acceso .fr:last-child {{ border-bottom:0; }}
  .acceso .fr span {{ color:#666; }}
  .acceso .fr b {{ font-family:"SF Mono",Menlo,monospace; font-weight:500; text-align:right; }}
  .aviso {{ margin-top:4mm; padding:3mm 4mm; background:#f6f6f4; border-left:2px solid #111;
            font-size:9.5pt; color:#333; }}

  .nn {{ padding:3mm 0; border-bottom:1px solid #eee; page-break-inside:avoid; }}
  .nn:last-child {{ border-bottom:0; }}
  .nn b {{ font-size:11pt; }}
  .nn p {{ color:#444; margin:1mm 0 0; }}

  .fase {{ border:1px solid #ddd; padding:4mm 5mm; margin-bottom:4mm; page-break-inside:avoid; }}
  .fase-h {{ display:flex; justify-content:space-between; align-items:baseline;
             border-bottom:1px solid #e2e2e2; padding-bottom:2mm; margin-bottom:2.5mm; }}
  .fase-h h4 {{ font-size:11.5pt; }}
  .rango {{ font-family:"SF Mono",Menlo,monospace; font-size:9pt; color:#666; }}
  .fr {{ display:flex; justify-content:space-between; gap:6mm; padding:1.3mm 0; font-size:10pt; }}
  .fr span {{ color:#666; }}
  .fr b {{ font-weight:500; text-align:right; }}

  .pasos {{ counter-reset:p; }}
  .paso {{ position:relative; padding-left:9mm; margin-bottom:3mm; }}
  .paso::before {{ counter-increment:p; content:counter(p,decimal-leading-zero);
                   position:absolute; left:0; top:.5mm; font-family:"SF Mono",Menlo,monospace;
                   font-size:8pt; color:#999; letter-spacing:.1em; }}
  .paso b {{ font-weight:600; }}
  .mia {{ background:#f2f2f0; padding:.5mm 1.5mm; }}

  .verdad {{ padding:3.5mm 0; border-bottom:1px solid #eee; page-break-inside:avoid; }}
  .verdad:last-child {{ border-bottom:0; }}
  .verdad b {{ font-size:11pt; display:block; margin-bottom:1.5mm; }}
  .verdad p {{ color:#444; margin:0; }}

  .cierre {{ margin-top:8mm; padding-top:4mm; border-top:1px solid #ddd;
             font-family:"SF Mono",Menlo,monospace; font-size:7.5pt; letter-spacing:.16em;
             text-transform:uppercase; color:#888; display:flex; justify-content:space-between; }}
</style></head><body>

<div class="cover">
  <div class="marca">NORTHPOINT CAPITAL MANAGEMENT</div>
  <div class="mid">
    <div class="marca" style="color:#888">Libro del socio</div>
    <h1>Cómo se opera<br>en esta mesa.</h1>
    <div class="quien">{html.escape(s['nombre'])}</div>
    <div class="cargo">{html.escape(cargos)}</div>
    <div class="frase">{html.escape(s['frase'])}</div>
  </div>
  <div class="pie"><span>Documento interno</span><span>{html.escape(fecha)}</span></div>
</div>

<section>
  <div class="n">01</div><h2>Qué es Northpoint</h2>
  <p class="lead">Somos tres socios operando dos departamentos con la misma disciplina.</p>
  <p><b>Mesa de futuros.</b> Operación diaria sobre futuros del Nasdaq en una sola ventana:
  7:00 a 8:30 de la mañana, hora de Nueva York. Estrategia ORB a liquidez. El capital viene de
  cuentas fondeadas de 50,000 dólares, cinco en paralelo, con una copiadora que replica una misma
  orden en todas.</p>
  <p><b>Snowball Investments.</b> Capital de clientes con horizonte largo, un proceso de cinco
  puertas antes de tomar una posición y rebalanceo trimestral.</p>
  <p>Lo que distingue a la casa no es la estrategia — es que todo queda documentado. Cada trade
  con su screenshot, cada tesis con sus cuatro firmas, cada día con su checklist firmado por quien
  lo revisó.</p>
</section>

<section>
  <div class="n">02</div><h2>Tu papel</h2>
  <p class="lead">{html.escape(s['frase'])}</p>
  {deberes}
</section>

<section>
  <div class="n">03</div><h2>Cómo entrar</h2>
  <div class="acceso">
    <div class="fr"><span>Terminal</span><b>{TERMINAL}</b></div>
    <div class="fr"><span>Usuario</span><b>{html.escape(s['usuario'])}</b></div>
    <div class="fr"><span>Correo de la mesa</span><b>{html.escape(s['correo'])}</b></div>
    <div class="fr"><span>Contraseña</span><b>te la entrega André en persona</b></div>
  </div>
  <div class="aviso"><b>Tu contraseña no está impresa aquí a propósito.</b> Un documento que se
  reenvía no es lugar para una credencial. Cámbiala la primera vez que entres y no la compartas
  por escrito con nadie, ni siquiera con los otros socios.</div>
  <p style="margin-top:4mm">Entrando con tu correo ves <b>la misma mesa</b> que los otros dos:
  las mismas tesis, las mismas firmas, el mismo journal. Si el indicador de la vista Aprobaciones
  dice <span class="mono">NUBE · SINCRONIZADA</span>, estás viendo lo mismo que ellos. Si dice
  <span class="mono">SIN SESIÓN</span> o <span class="mono">ESTADO LOCAL</span>, estás trabajando
  solo en tu máquina y hay que resolverlo antes de firmar nada.</p>
</section>

<section>
  <div class="n">04</div><h2>Lo que no se negocia</h2>
  <p>Cinco reglas. No tienen excepción creativa, y cuando una parece inconveniente es
  justo cuando más se necesita.</p>
  {nn}
</section>

<section style="page-break-before:always">
  <div class="n">05</div><h2>El plan, en tres fases</h2>
  <p>Cinco cuentas de 50,000 con la copiadora. Los datos marcados como
  <i>dato de la fondeadora</i> están verificados contra su centro de ayuda; los demás son reglas
  que nos pusimos nosotros y podemos cambiar.</p>
  {fases}
</section>

<section>
  <div class="n">06</div><h2>Cómo entra un trade a la mesa</h2>
  <div class="pasos">
    <div class="paso"><b>Se propone la tesis.</b> Cualquiera abre una tesis en la vista de
    Aprobaciones: instrumento, dirección y el argumento por escrito.</div>
    <div class="paso"><b>Firma research.</b> Mateo revisa que el argumento se sostenga con
    evidencia, no con opinión.</div>
    <div class="paso"><b>Firma riesgo.</b> Mateo confirma que el tamaño y el stop caben en el
    riesgo del día y en el colchón de las cuentas.</div>
    <div class="paso"><b>Firma quant.</b> André verifica que los números cuadren y que no rompa
    consistencia ni límites.</div>
    <div class="paso"><b>Firma el CIO.</b> Pablo aprueba o rechaza. Sin su firma no se ejecuta.</div>
    <div class="paso"><b>Se ejecuta y se registra.</b> La tesis queda marcada como ejecutada
    <i>hasta que el trade existe en el journal</i>, con sus cuentas y su screenshot.</div>
  </div>
  <p style="margin-top:3mm">Tu firma en este proceso es
  <span class="mia mono">{html.escape(s['firma'])}</span>. Dos socios pueden firmar al mismo
  tiempo sin borrarse: el terminal las suma.</p>
</section>

<section>
  <div class="n">07</div><h2>El curso</h2>
  <p>Dentro del terminal, en <b>Curso</b>, están los 30 días del Boot Camp de TJR en orden.
  Se abre día por día: el siguiente se destraba cuando marcas el anterior. No es adorno — es el
  vocabulario común de la mesa. Cuando alguien dice «barrido de liquidez» o «FVG», todos tienen
  que estar hablando de lo mismo.</p>
  <p>Debajo están los documentos propios de la casa: siete módulos escritos por nosotros sobre
  cómo operamos aquí, con diagramas.</p>
</section>

<section>
  <div class="n">08</div><h2>Lo que hay que saber sin adornos</h2>
  <p>Esto sale de auditar el plan contra las reglas reales de la fondeadora y de simular un mes
  completo con el código del terminal. No está aquí para desanimar a nadie: está aquí porque una
  mesa que se miente a sí misma no dura.</p>
  {verdades}
</section>

<div class="cierre">
  <span>Northpoint Capital Management</span>
  <span>{html.escape(s['nombre'])} · {html.escape(fecha)}</span>
</div>

</body></html>"""


def main():
    if not Path(CHROME).exists():
        print('No encontré Google Chrome; es lo que imprime el PDF.', file=sys.stderr)
        return 1
    SALIDA.mkdir(parents=True, exist_ok=True)
    hechos = []
    for s in SOCIOS:
        htm = SALIDA / f"_{s['usuario']}.html"
        pdf = SALIDA / f"NORTHPOINT-{s['nombre']}.pdf"
        htm.write_text(documento(s), encoding='utf-8')
        r = subprocess.run(
            [CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
             f'--print-to-pdf={pdf}', htm.as_uri()],
            capture_output=True, text=True, timeout=120)
        if not pdf.exists():
            print(f"  ! {s['nombre']}: no se generó\n{r.stderr[:400]}", file=sys.stderr)
            continue
        htm.unlink()
        hechos.append((s['nombre'], pdf, pdf.stat().st_size))
        print(f"  {s['nombre']:8s} → {pdf.name} ({pdf.stat().st_size // 1024} KB)")
    return 0 if len(hechos) == len(SOCIOS) else 1


if __name__ == '__main__':
    sys.exit(main())
