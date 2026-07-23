#!/usr/bin/env python3
"""
Avisa por correo a los socios. Dos trabajos en un solo archivo:

  python3 scripts/avisos.py                  vigila la mesa y avisa de lo que cambió
  python3 scripts/avisos.py --recordatorio X  manda el aviso de reloj X

El navegador no puede mandar correo desde un sitio estático, así que esto corre en
GitHub Actions (.github/workflows/avisos.yml y recordatorios.yml).

Qué avisa cuando algo cambia en la mesa:
  · una tesis nueva esperando firmas
  · cada firma que se agrega, y a quién le toca la siguiente
  · una tesis que ya juntó las cuatro y está lista para ejecutarse
  · una tesis rechazada
  · cada trade registrado, con el acumulado del día
  · un trade con violación de disciplina
  · una cuenta cuyo colchón se acercó al corte
  · una cuenta que cambió de fase o llegó a su objetivo

Qué avisa por reloj (lunes a viernes, hora de Morelia):
  · 6:50  la ventana abre a las 7:00
  · 7:20  el rango de apertura es a las 7:30
  · 8:35  cerró la ventana, hay que documentar
  · 9:00  los días 1 y 16, corte de quincena

Los avisos de cambio se comparan contra data/avisos-visto.json y los de reloj contra
data/avisos-reloj.json; los dos archivos los actualiza y commitea el propio trabajo,
así que nada se manda dos veces.

Secretos que necesita (en GitHub → Settings → Secrets and variables → Actions):
  SUPABASE_URL           https://xxxx.supabase.co
  SUPABASE_SERVICE_KEY   la llave sb_secret_… (NUNCA va en el repositorio)
  GMAIL_USER             la cuenta desde la que sale el correo
  GMAIL_APP_PASSWORD     contraseña de aplicación de Google, no la del correo
"""
import argparse
import json
import os
import smtplib
import ssl
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CFG = RAIZ / 'data' / 'avisos.json'
VISTO = RAIZ / 'data' / 'avisos-visto.json'
RELOJ = RAIZ / 'data' / 'avisos-reloj.json'
BITACORA = RAIZ / 'data' / 'bitacora.json'
BITACORA_TOPE = 400        # se conserva lo reciente; el archivo no puede crecer sin fin
TERMINAL = 'https://studioamr.github.io/northpoint-capital/app.html'

GATES = [('research', 'Research'), ('riesgo', 'Riesgo'),
         ('quant', 'Quant'), ('cio', 'CIO')]
FASES = {'eval': 'Evaluación', 'buffer': 'Colchón', 'payout': 'Retiros'}
DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']


# ─────────────────────────── utilidades ───────────────────────────

def leer_json(p, default=None):
    if not p.exists():
        return default if default is not None else {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return default if default is not None else {}


def leer_mesa(obligatoria=True):
    """Baja el estado compartido. Si obligatoria=False, un fallo no tumba el aviso."""
    try:
        url = os.environ['SUPABASE_URL'].rstrip('/')
        key = os.environ['SUPABASE_SERVICE_KEY']
        req = urllib.request.Request(
            f'{url}/rest/v1/northpoint_estado?id=eq.1&select=data,rev',
            headers={'apikey': key, 'Authorization': f'Bearer {key}'})
        with urllib.request.urlopen(req, timeout=25) as r:
            filas = json.loads(r.read().decode())
        if not filas:
            raise RuntimeError('la mesa está vacía en la nube')
        return filas[0].get('data') or {}, filas[0].get('rev', 0)
    except Exception as e:
        if obligatoria:
            raise SystemExit(f'No se pudo leer la mesa: {e}')
        print(f'  ! sin datos de la mesa ({e}); el recordatorio va sin contexto',
              file=sys.stderr)
        return {}, None


def ahora_local(cfg):
    return datetime.now(timezone.utc) + timedelta(hours=cfg.get('utc_offset', -6))


def nombre_de(cfg, usuario):
    for s in cfg['socios']:
        if s['usuario'] == usuario:
            return s['nombre']
    return usuario or 'alguien'


def faltantes(t):
    firmas = t.get('firmas') or {}
    return [etiqueta for clave, etiqueta in GATES if clave not in firmas]


def dinero(n):
    if n is None:
        return '—'
    return ('-$' if n < 0 else '$') + f'{abs(n):,.0f}'


def resumen_del_dia(mesa, fecha):
    """Cuántos trades y cuánto P&L lleva la mesa en esa fecha."""
    trades = [t for t in ((mesa.get('resumen') or {}).get('trades_recientes') or [])
              if t.get('date') == fecha]
    return trades, sum(t.get('pnl') or 0 for t in trades)


# ─────────────────── avisos por cambio en la mesa ───────────────────

def novedades(cfg, mesa, visto):
    """Compara la mesa contra lo ya avisado.

    Devuelve ([(asunto, cuerpo)], memoria) donde 'memoria' es lo que hay que
    recordar para la próxima corrida y no se puede derivar del estado actual.
    """
    av = cfg.get('avisar', {})
    res = mesa.get('resumen') or {}
    salida = []
    memoria = {'colchon_avisado': visto.get('colchon_avisado') or {}}
    # Los avisos de trade y de cuenta se agregaron después. Si el archivo de control
    # viene de la versión anterior no trae su historial, y avisar de todo lo que ya
    # existía sería un correo por cada trade viejo. Esta corrida sólo los fotografía.
    estrena = visto.get('v', 1) < 2

    tesis = {t['id']: t for t in (mesa.get('tickets') or []) if t.get('id')}
    antes = visto.get('tickets', {})

    for tid, t in tesis.items():
        prev = antes.get(tid)
        sym = t.get('sym', '?')
        lado = 'LONG' if t.get('dir') == 'L' else 'SHORT'
        quien = nombre_de(cfg, t.get('por'))
        falta = faltantes(t)

        if prev is None and av.get('tesis_nueva'):
            salida.append((
                f'Tesis nueva · {sym} {lado}',
                f'{quien} propuso {sym} {lado}.\n\n'
                f'Tesis: {t.get("tesis") or "(sin texto)"}\n\n'
                f'Faltan {len(falta)} firmas: {", ".join(falta) or "ninguna"}.'))
            continue
        if prev is None:
            continue

        nuevas = set((t.get('firmas') or {})) - set(prev.get('firmas') or {})
        if nuevas and av.get('firma_nueva'):
            det = []
            for k in nuevas:
                f = (t.get('firmas') or {}).get(k) or {}
                det.append(f'{dict(GATES).get(k, k)} — {nombre_de(cfg, f.get("u"))}')
            salida.append((
                f'Firma en {sym} {lado}',
                'Se firmó:\n  ' + '\n  '.join(det) +
                (f'\n\nFaltan: {", ".join(falta)}.' if falta else
                 '\n\nYa están las cuatro firmas.')))

        if not falta and faltantes(prev) and av.get('tesis_lista'):
            salida.append((
                f'LISTA PARA EJECUTAR · {sym} {lado}',
                f'{sym} {lado} juntó las cuatro firmas. Le toca al PM ejecutarla y '
                f'registrarla en el journal.'))

        if t.get('estado') == 'rechazada' and prev.get('estado') != 'rechazada' \
                and av.get('tesis_rechazada'):
            salida.append((
                f'Tesis rechazada · {sym} {lado}',
                f'Motivo: {t.get("motivo") or "(sin motivo escrito)"}'))

    # ── trades registrados ──
    recientes = res.get('trades_recientes') or []
    ya = set(visto.get('trades_vistos') or [])
    if av.get('trade_nuevo') and recientes and not estrena:
        # se agrupan por día para poder decir el acumulado con el trade ya incluido
        por_dia = {}
        for tr in recientes:
            por_dia.setdefault(tr.get('date'), []).append(tr)
        for tr in recientes:
            if tr.get('id') in ya:
                continue
            lado = 'LONG' if tr.get('dir') == 'L' else 'SHORT'
            n = tr.get('nAcc') or 1
            dia = por_dia.get(tr.get('date')) or []
            acum = sum(x.get('pnl') or 0 for x in dia)
            meta = (res.get('dia') or {}).get('meta')
            linea = [f'{nombre_de(cfg, tr.get("por"))} registró un trade.', '']
            linea.append(f'  {tr.get("sym")} {lado} · {tr.get("qty")} contratos '
                         f'· {tr.get("time")}')
            if tr.get('entry') is not None or tr.get('exit') is not None:
                linea.append(f'  entrada {tr.get("entry")} → salida {tr.get("exit")}')
            linea.append(f'  {dinero(tr.get("pnl1"))} por cuenta × {n} '
                         f'= {dinero(tr.get("pnl"))}')
            linea.append(f'  setup válido: {"sí" if tr.get("setupOk") else "NO"}')
            if tr.get('notas'):
                linea.append(f'  notas: {tr["notas"]}')
            linea += ['', f'Van {len(dia)} trade(s) el {tr.get("date")}, '
                          f'acumulado {dinero(acum)}.']
            if meta:
                falta_meta = meta - acum
                linea.append(f'Meta del día {dinero(meta)} · '
                             + (f'faltan {dinero(falta_meta)}.' if falta_meta > 0
                                else 'ya se cumplió.'))
            if tr.get('violaciones'):
                linea += ['', f'⚠ Este trade rompió: {", ".join(tr["violaciones"])}.']
            if len(dia) >= 2:
                linea.append('Son dos trades: la sesión se cierra aquí.')
            salida.append((f'Trade · {tr.get("sym")} {lado} {dinero(tr.get("pnl"))}',
                           '\n'.join(linea)))

    # ── trades con violación (aviso aparte, para que no se pierda entre los normales) ──
    if av.get('trade_con_violacion'):
        vistos = set(visto.get('trades_avisados') or [])
        for tr in (res.get('trades_violados') or []):
            vs = tr.get('violaciones') or []
            if vs and tr.get('id') not in vistos:
                salida.append((
                    f'Violación · {tr.get("sym")} {tr.get("date")}',
                    f'El trade de {tr.get("date")} {tr.get("time")} en '
                    f'{tr.get("sym")} quedó marcado: {", ".join(vs)}.'))

    # ── cuentas ──
    salud = res.get('cuentas_salud') or []
    prev_cuentas = visto.get('cuentas', {})

    if av.get('colchon_bajo'):
        limite = cfg.get('colchon_minimo', 700)
        paso = cfg.get('colchon_paso', 150)
        # Avisar una sola vez y callar no sirve: un colchón que va de 600 a 200 es
        # justo cuando hay que enterarse. Se guarda con cuánto se avisó la última vez
        # y se vuelve a avisar cada vez que baja otro 'paso'. Si se recupera por
        # encima del límite, el registro se borra y queda armado de nuevo.
        antes_col = visto.get('colchon_avisado') or {}
        memoria['colchon_avisado'] = nuevo_col = dict(antes_col)
        for c in salud:
            alias, col = c.get('alias'), c.get('colchon')
            if col is None or col > limite:
                nuevo_col.pop(alias, None)      # se recuperó: queda armado de nuevo
                continue
            previo = antes_col.get(alias)
            if previo is not None and col > previo - paso:
                continue                        # bajó poco: se conserva el aviso previo
            nuevo_col[alias] = col
            salida.append((
                f'Colchón bajo · {alias}',
                (f'La cuenta {alias} quedó a {dinero(col)} del corte'
                 + (f' (antes iban {dinero(previo)})' if previo is not None else '')
                 + '.\n\n'
                 f'Balance {dinero(c.get("balance"))}. '
                 f'El CRO tiene autoridad para detener la mesa.')))

    for c in (salud if not estrena else []):
        alias = c.get('alias')
        p = prev_cuentas.get(alias)
        if not p:
            continue
        if av.get('cuenta_cambio_fase') and c.get('fase') != p.get('fase'):
            salida.append((
                f'Cambio de fase · {alias}',
                f'{alias} pasó de {FASES.get(p.get("fase"), p.get("fase"))} a '
                f'{FASES.get(c.get("fase"), c.get("fase"))}.\n\n'
                f'Balance {dinero(c.get("balance"))}. '
                f'Riesgo diario nuevo {dinero(c.get("rDia"))}, '
                f'objetivo {dinero(c.get("oDia"))}.'))
        if av.get('objetivo_alcanzado') and c.get('hito') is not None \
                and c.get('balance') is not None \
                and c['balance'] >= c['hito'] > (p.get('balance') or 0):
            salida.append((
                f'Objetivo alcanzado · {alias}',
                f'{alias} llegó a {dinero(c["balance"])}, arriba del objetivo de '
                f'{dinero(c["hito"])}. Toca revisar días mínimos y consistencia '
                f'antes de pedir nada.'))

    return salida, memoria


def foto(cfg, mesa, rev, memoria):
    res = mesa.get('resumen') or {}
    return {
        'v': 2,
        'rev': rev,
        'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'tickets': {t['id']: {'firmas': t.get('firmas') or {}, 'estado': t.get('estado')}
                    for t in (mesa.get('tickets') or []) if t.get('id')},
        'trades_vistos': [t['id'] for t in (res.get('trades_recientes') or [])
                          if t.get('id')],
        'trades_avisados': [t['id'] for t in (res.get('trades_violados') or [])
                            if t.get('id')],
        'cuentas': {c.get('alias'): {'fase': c.get('fase'), 'balance': c.get('balance')}
                    for c in (res.get('cuentas_salud') or []) if c.get('alias')},
        # con cuánto colchón se avisó cada cuenta, para no repetir ni quedarse callado
        'colchon_avisado': memoria.get('colchon_avisado') or {},
    }


# ────────────────────────── avisos por reloj ──────────────────────────

def recordatorio(cfg, clave, forzar):
    """Devuelve [(asunto, cuerpo)] o [] si hoy no toca."""
    r = (cfg.get('recordatorios') or {}).get(clave)
    if not r:
        raise SystemExit(f'No existe el recordatorio "{clave}" en data/avisos.json')
    if not r.get('activo', True):
        print(f'recordatorio "{clave}" apagado en la configuración')
        return []

    hoy = ahora_local(cfg)
    fecha = hoy.strftime('%Y-%m-%d')

    if not forzar:
        if hoy.weekday() > 4:
            print(f'hoy es {DIAS[hoy.weekday()]}: la mesa está cerrada')
            return []
        dias_mes = r.get('dias_del_mes')
        if dias_mes and hoy.day not in dias_mes:
            print(f'"{clave}" sólo va los días {dias_mes} del mes; hoy es {hoy.day}')
            return []
        # GitHub a veces dispara un cron dos veces: una llave por día lo corta
        ya = leer_json(RELOJ)
        if ya.get(clave) == fecha:
            print(f'"{clave}" ya se mandó hoy ({fecha})')
            return []

    cuerpo = list(r.get('cuerpo') or [])

    # contexto en vivo: sólo si la mesa se pudo leer
    mesa, _ = leer_mesa(obligatoria=False)
    res = mesa.get('resumen') or {}

    if clave == 'pre':
        pendientes = [t for t in (mesa.get('tickets') or [])
                      if t.get('estado') not in ('rechazada', 'ejecutada')]
        sin_firmar = [t for t in pendientes if faltantes(t)]
        listas = [t for t in pendientes if not faltantes(t)]
        if listas:
            cuerpo += ['', 'Firmadas y sin ejecutar:']
            cuerpo += [f'  · {t.get("sym")} '
                       f'{"LONG" if t.get("dir") == "L" else "SHORT"}' for t in listas]
        if sin_firmar:
            cuerpo += ['', 'Esperando firmas:']
            cuerpo += [f'  · {t.get("sym")} '
                       f'{"LONG" if t.get("dir") == "L" else "SHORT"} '
                       f'— faltan {", ".join(faltantes(t))}' for t in sin_firmar]
        d = res.get('dia') or {}
        if d.get('cuentas'):
            cuerpo += ['', f'Hoy operan {d["cuentas"]} cuentas · '
                           f'meta {dinero(d.get("meta"))} · '
                           f'riesgo máximo {dinero(d.get("riesgo"))}.']

    if clave == 'cierre':
        trades, pnl = resumen_del_dia(mesa, fecha)
        d = res.get('dia') or {}
        if trades:
            cuerpo += ['', f'Hoy: {len(trades)} trade(s), {dinero(pnl)}.']
            for t in trades:
                lado = 'LONG' if t.get('dir') == 'L' else 'SHORT'
                marca = '  ⚠' if t.get('violaciones') else '  ·'
                cuerpo.append(f'{marca} {t.get("time")} {t.get("sym")} {lado} '
                              f'{dinero(t.get("pnl"))}')
            if d.get('meta'):
                cuerpo.append('')
                cuerpo.append(f'Meta {dinero(d["meta"])} · '
                              + ('cumplida.' if pnl >= d['meta']
                                 else f'faltaron {dinero(d["meta"] - pnl)}.'))
        else:
            cuerpo += ['', 'No hay trades registrados hoy. Si se operó, hay que '
                           'meterlos al journal; si no se operó, un día sin setup '
                           'también es un día bien trabajado.']

    if clave == 'quincena':
        salud = res.get('cuentas_salud') or []
        if salud:
            cuerpo += ['', 'Estado de las cuentas:']
            for c in salud:
                cuerpo.append(f'  · {c.get("alias")} — {dinero(c.get("balance"))} '
                              f'· fase {FASES.get(c.get("fase"), c.get("fase"))} '
                              f'· a {dinero(c.get("colchon"))} del corte')

    hora = r.get('hora', '')
    pie = f'{DIAS[hoy.weekday()].capitalize()} {fecha} · {hora} hora de la mesa'
    return [(r.get('asunto', clave), '\n'.join(cuerpo) + f'\n\n{pie}')]


# ──────────────────────────── envío ────────────────────────────

PIE = ('— — —\nAbrir la mesa: {t}#aprobaciones\n'
       'Este aviso lo manda el terminal solo. No hace falta contestarlo.')


def registrar(entradas):
    """Deja constancia de lo que se mandó, para que el terminal lo pueda mostrar.

    Es un archivo en el repositorio y no la nube a propósito: el aviso sale desde
    GitHub Actions, que no tiene sesión de socio y por tanto no puede escribir en
    Supabase sin la llave secreta viajando de más. Aquí basta con que quede escrito.
    """
    if not entradas:
        return
    libro = leer_json(BITACORA, [])
    if not isinstance(libro, list):
        libro = []
    libro = entradas + libro                    # lo nuevo primero
    BITACORA.write_text(json.dumps(libro[:BITACORA_TOPE],
                                   ensure_ascii=False, indent=1) + '\n')


def anotacion(tipo, asunto, destinos, detalle=''):
    return {'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'tipo': tipo, 'asunto': asunto,
            'para': [d.split('@')[0] for d in destinos],   # sin la dirección completa
            'detalle': (detalle or '')[:300]}


def _smtp():
    ctx = ssl.create_default_context()
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ctx)
    s.login(os.environ['GMAIL_USER'], os.environ['GMAIL_APP_PASSWORD'])
    return s


def mandar_uno(cfg, destino, asunto, cuerpo, imagenes=None, smtp=None):
    """Un correo a una sola persona, con imágenes incrustadas si las hay.

    Va como texto y como HTML: quien tenga imágenes bloqueadas sigue leyendo todo,
    porque los niveles del overnight también van escritos en el texto.
    """
    usuario = os.environ['GMAIL_USER']
    m = EmailMessage()
    m['From'] = f'Northpoint <{usuario}>'
    m['To'] = destino
    m['Subject'] = f'[Northpoint] {asunto}'
    plano = f'{cuerpo}\n\n' + PIE.format(t=TERMINAL)
    m.set_content(plano)

    if imagenes:
        from html import escape
        cids = []
        for i, (nombre, _) in enumerate(imagenes):
            cids.append(f'img{i}@northpoint')
        figs = ''.join(
            f'<img src="cid:{c}" alt="{escape(n)}" '
            f'style="width:100%;max-width:660px;display:block;margin:14px 0">'
            for c, (n, _) in zip(cids, imagenes))
        m.add_alternative(
            '<div style="background:#05070C;color:#E9EDF2;padding:22px;'
            'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px">'
            f'{figs}'
            f'<pre style="white-space:pre-wrap;margin:0;font:inherit;color:#E9EDF2">'
            f'{escape(plano)}</pre></div>', subtype='html')
        html = m.get_payload()[-1]
        html.make_related()
        for c, (nombre, datos) in zip(cids, imagenes):
            html.add_related(datos, 'image', 'png', cid=f'<{c}>', filename=nombre)

    propio = smtp is None
    s = smtp or _smtp()
    try:
        s.send_message(m)
    finally:
        if propio:
            s.quit()
    registrar([anotacion('overnight' if 'Overnight' in asunto else 'aviso',
                         asunto, [destino], cuerpo.split('\n')[0])])


def tipo_de(asunto):
    """Clasifica el aviso para que el terminal lo pueda pintar distinto."""
    a = asunto.lower()
    if a.startswith('trade ·'):        return 'trade'
    if 'violación' in a:               return 'violacion'
    if 'colchón' in a:                 return 'riesgo'
    if 'lista para ejecutar' in a:     return 'aprobada'
    if 'tesis' in a or 'firma' in a:   return 'tesis'
    if 'fase' in a or 'objetivo' in a: return 'cuenta'
    return 'recordatorio'


def mandar(cfg, avisos):
    usuario = os.environ['GMAIL_USER']
    clave = os.environ['GMAIL_APP_PASSWORD']
    destinos = [s['correo'] for s in cfg['socios']
                if s.get('correo') and 'CAMBIAR' not in s['correo']]
    if not destinos:
        print('  ! los correos de data/avisos.json siguen sin configurar', file=sys.stderr)
        return 0

    libro = []
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ctx) as smtp:
        smtp.login(usuario, clave)
        for asunto, cuerpo in avisos:
            m = EmailMessage()
            m['From'] = f'Northpoint <{usuario}>'
            m['To'] = ', '.join(destinos)
            m['Subject'] = f'[Northpoint] {asunto}'
            m.set_content(
                f'{cuerpo}\n\n'
                f'— — —\nAbrir la mesa: {TERMINAL}#aprobaciones\n'
                f'Este aviso lo manda el terminal solo. No hace falta contestarlo.')
            smtp.send_message(m)
            libro.append(anotacion(tipo_de(asunto), asunto, destinos,
                                   cuerpo.split('\n')[0]))
            print(f'  → {asunto}')
    registrar(libro)
    return len(avisos)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--recordatorio', metavar='CLAVE',
                    help='manda un aviso de reloj (pre, orb, cierre, quincena)')
    ap.add_argument('--forzar', action='store_true',
                    help='con --recordatorio: manda aunque hoy no toque o ya se haya mandado')
    args = ap.parse_args()

    cfg = leer_json(CFG)
    if not cfg.get('activo'):
        print('avisos desactivados en data/avisos.json')
        return 0

    faltan = [k for k in ('SUPABASE_URL', 'SUPABASE_SERVICE_KEY',
                          'GMAIL_USER', 'GMAIL_APP_PASSWORD')
              if not os.environ.get(k)]
    if faltan:
        print('Faltan secretos: ' + ', '.join(faltan), file=sys.stderr)
        return 1

    if args.recordatorio:
        avisos = recordatorio(cfg, args.recordatorio, args.forzar)
        n = mandar(cfg, avisos) if avisos else 0
        if avisos and not args.forzar:
            reloj = leer_json(RELOJ)
            reloj[args.recordatorio] = ahora_local(cfg).strftime('%Y-%m-%d')
            RELOJ.write_text(json.dumps(reloj, ensure_ascii=False, indent=1) + '\n')
        print(f'{n} recordatorio(s)')
        return 0

    mesa, rev = leer_mesa()
    visto = leer_json(VISTO)

    primera = not visto
    avisos, memoria = ([], {}) if primera else novedades(cfg, mesa, visto)
    if primera:
        print('primera corrida: se toma foto sin avisar de lo que ya existía')

    n = mandar(cfg, avisos) if avisos else 0
    if not avisos:
        print('sin novedades')

    VISTO.write_text(json.dumps(foto(cfg, mesa, rev, memoria),
                                ensure_ascii=False, indent=1) + '\n')
    print(f'{n} aviso(s) · rev {rev}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
