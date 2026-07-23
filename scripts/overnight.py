#!/usr/bin/env python3
"""
Resumen de overnight: el primer correo del día, uno por socio, con gráficas.

Sale antes que el recordatorio de la ventana. Trae lo que pasó mientras la mesa
dormía: cuánto se movió cada instrumento, el rango del overnight y dónde quedó el
precio dentro de él, los niveles que importan para el rompimiento, los eventos rojos
del día y los titulares de la noche.

La mesa opera 7:00–8:30 hora de Morelia, que es 9:00–10:30 en Nueva York: el rango de
apertura de 7:30–7:45 cae exactamente en la apertura del cash. Por eso "overnight"
aquí es la sesión de Globex desde las 18:00 ET del día anterior hasta la mañana.

  python3 scripts/overnight.py            manda el correo
  python3 scripts/overnight.py --prueba   arma todo y lo guarda en /tmp sin mandar nada

Necesita GMAIL_USER y GMAIL_APP_PASSWORD. No toca Supabase: esto no depende de la mesa.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))
import avisos   # noqa: E402  — reutiliza configuración y envío
import mercado  # noqa: E402  — reutiliza la bajada con reintentos

MERCADO = RAIZ / 'data' / 'mercado.json'

# Lo que se grafica y lo que sólo se tabula. NQ y ES son los que se operan.
CON_GRAFICA = [('NQ=F', 'NQ', 'Nasdaq 100'), ('ES=F', 'ES', 'S&P 500')]
SOLO_TABLA = [('YM=F', 'YM', 'Dow'), ('RTY=F', 'RTY', 'Russell 2000'),
              ('GC=F', 'GC', 'Oro'), ('CL=F', 'CL', 'Petróleo'),
              ('DX-Y.NYB', 'DXY', 'Dólar'), ('^VIX', 'VIX', 'Volatilidad')]


def yahoo(sym, rango='2d', intervalo='5m'):
    url = (f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}'
           f'?interval={intervalo}&range={rango}&includePrePost=true')
    d = json.loads(mercado.baja(url))          # trae reintentos con espera creciente
    res = (d.get('chart') or {}).get('result') or []
    if not res:
        raise RuntimeError('Yahoo no devolvió datos')
    return res[0]


def sesion_overnight(res):
    """Devuelve (barras, meta) de la sesión de Globex vigente.

    Globex abre a las 18:00 ET. Se toma desde la última apertura que haya ocurrido.
    """
    meta = res.get('meta') or {}
    off = meta.get('gmtoffset', -14400)          # segundos: hora del mercado vs UTC
    ts = res.get('timestamp') or []
    q = ((res.get('indicators') or {}).get('quote') or [{}])[0]
    cierres = q.get('close') or []

    barras = []
    for t, c in zip(ts, cierres):
        if c is None:
            continue
        local = datetime.fromtimestamp(t, timezone.utc) + timedelta(seconds=off)
        barras.append((local, float(c)))
    if not barras:
        raise RuntimeError('sin barras utilizables')

    ultima = barras[-1][0]
    # apertura de Globex: 18:00 del día anterior si ya pasamos de las 18:00, si no anteayer
    ancla = ultima.replace(hour=18, minute=0, second=0, microsecond=0)
    if ultima.hour < 18:
        ancla -= timedelta(days=1)
    on = [b for b in barras if b[0] >= ancla]
    if len(on) < 5:                               # fin de semana o feed corto
        on = barras[-78:]
    return on, meta


def instrumento(sym, corto, nombre):
    res = yahoo(sym)
    on, meta = sesion_overnight(res)
    precios = [p for _, p in on]
    previo = meta.get('chartPreviousClose') or meta.get('previousClose') or precios[0]
    ahora = meta.get('regularMarketPrice') or precios[-1]
    alto, bajo = max(precios), min(precios)
    rango = alto - bajo
    # dónde quedó el precio dentro del rango: 100% = pegado al máximo del overnight
    pos = ((ahora - bajo) / rango * 100) if rango else 50.0
    return {'sym': corto, 'nombre': nombre, 'barras': on, 'previo': previo,
            'ahora': ahora, 'alto': alto, 'bajo': bajo, 'rango': rango, 'pos': pos,
            'cambio': ahora - previo,
            'pct': ((ahora - previo) / previo * 100) if previo else 0.0}


def grafica(datos, destino):
    """Dibuja el overnight con sus extremos marcados. Devuelve True si se pudo."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        return False

    x = [b[0] for b in datos['barras']]
    y = [b[1] for b in datos['barras']]
    sube = datos['cambio'] >= 0
    color = '#57C79B' if sube else '#DE6A5F'

    fig, ax = plt.subplots(figsize=(7.6, 3.1), dpi=150)
    fig.patch.set_facecolor('#05070C')
    ax.set_facecolor('#05070C')

    ax.plot(x, y, color=color, linewidth=1.6)
    ax.fill_between(x, y, min(y), color=color, alpha=.09)

    for valor, etiqueta in ((datos['alto'], f'máx {datos["alto"]:,.2f}'),
                            (datos['bajo'], f'mín {datos["bajo"]:,.2f}')):
        ax.axhline(valor, color='#9BC0DC', linewidth=.7, linestyle=(0, (4, 4)), alpha=.55)
        ax.annotate(etiqueta, xy=(x[0], valor), xytext=(4, 3), textcoords='offset points',
                    color='#9BC0DC', fontsize=7, family='monospace')
    ax.axhline(datos['previo'], color='#7A8698', linewidth=.7, alpha=.5)
    ax.annotate(f'cierre previo {datos["previo"]:,.2f}', xy=(x[0], datos['previo']),
                xytext=(4, -10), textcoords='offset points',
                color='#7A8698', fontsize=7, family='monospace')

    ax.set_title(f'{datos["sym"]} · overnight   '
                 f'{datos["cambio"]:+,.2f} ({datos["pct"]:+.2f}%)',
                 color='#E9EDF2', fontsize=10, loc='left', pad=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlabel('hora de Nueva York', color='#7A8698', fontsize=7,
                  family='monospace', labelpad=4)
    ax.tick_params(colors='#7A8698', labelsize=7)
    for lado, s in ax.spines.items():
        s.set_visible(lado == 'bottom')
        s.set_color('#1C2431')
    ax.grid(axis='y', color='#FFFFFF', alpha=.05, linewidth=.6)
    fig.tight_layout()
    fig.savefig(destino, facecolor=fig.get_facecolor())
    plt.close(fig)
    return True


def del_mercado():
    """Calendario rojo de hoy y titulares, de lo que ya junta scripts/mercado.py."""
    d = avisos.leer_json(MERCADO)
    hoy = avisos.ahora_local(CFG).strftime('%Y-%m-%d')
    cal = [e for e in (d.get('calendario') or []) if e.get('dia') == hoy]
    return cal, (d.get('noticias') or [])[:6], d.get('ts')


def texto(instrumentos, cal, noticias, ts_mercado, nombre):
    hoy = avisos.ahora_local(CFG)
    L = [f'Buenos días, {nombre}.', '',
         f'{avisos.DIAS[hoy.weekday()].capitalize()} {hoy.strftime("%Y-%m-%d")}. '
         f'Esto se movió mientras dormíamos.', '']

    if instrumentos:
        L.append('MOVIMIENTO DE LA NOCHE')
        for d in instrumentos:
            L.append(f'  {d["sym"]:<4} {d["ahora"]:>11,.2f}   '
                     f'{d["cambio"]:>+9,.2f}  {d["pct"]:>+6.2f}%')
        L.append('')
        L.append('RANGO DEL OVERNIGHT')
        for d in instrumentos:
            if not d.get('rango'):
                continue
            donde = ('pegado al máximo' if d['pos'] >= 80 else
                     'pegado al mínimo' if d['pos'] <= 20 else 'a media tabla')
            L.append(f'  {d["sym"]:<4} {d["bajo"]:,.2f} — {d["alto"]:,.2f}   '
                     f'({d["rango"]:,.2f} pts, {donde})')
        L += ['', 'Esos máximos y mínimos son la liquidez que el rompimiento va a buscar.']

    L += ['', 'EVENTOS DE HOY  (hora de la mesa)']
    if cal:
        for e in cal:
            dentro = '  ← DENTRO DE LA VENTANA' if '07:00' <= e.get('hora', '') <= '08:30' else ''
            L.append(f'  {e.get("hora","")}  {e.get("pais","")}  {e.get("titulo","")}'
                     f'   previsto {e.get("previsto") or "—"} · '
                     f'previo {e.get("previo") or "—"}{dentro}')
        L.append('')
        L.append('Si un evento rojo cae dentro de la ventana, no se opera.')
    else:
        L.append('  Sin eventos de alto impacto hoy.')

    if noticias:
        L += ['', 'TITULARES']
        for n in noticias:
            L.append(f'  · {n.get("titulo","")}')

    L += ['', 'La ventana abre a las 7:00. El rango de apertura, 7:30–7:45.']
    if ts_mercado:
        L.append('')
        L.append(f'Datos de mercado al {ts_mercado}.')
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prueba', action='store_true',
                    help='arma el correo y lo guarda en /tmp sin mandarlo')
    args = ap.parse_args()

    global CFG
    CFG = avisos.leer_json(avisos.CFG)
    if not CFG.get('activo'):
        print('avisos desactivados en data/avisos.json')
        return 0
    if not CFG.get('overnight', {}).get('activo', True):
        print('el resumen de overnight está apagado en data/avisos.json')
        return 0

    hoy = avisos.ahora_local(CFG)
    fecha = hoy.strftime('%Y-%m-%d')
    if not args.prueba:
        if hoy.weekday() > 4:
            print(f'hoy es {avisos.DIAS[hoy.weekday()]}: la mesa está cerrada')
            return 0
        if avisos.leer_json(avisos.RELOJ).get('overnight') == fecha:
            print(f'el resumen de overnight ya salió hoy ({fecha})')
            return 0

    instrumentos, imagenes = [], []
    salida = Path('/tmp/northpoint-overnight')
    salida.mkdir(exist_ok=True)

    for sym, corto, nombre in CON_GRAFICA:
        try:
            d = instrumento(sym, corto, nombre)
            instrumentos.append(d)
            png = salida / f'{corto}.png'
            if grafica(d, png):
                imagenes.append((f'{corto}.png', png.read_bytes()))
        except Exception as e:
            print(f'  ! {corto}: {e}', file=sys.stderr)

    for sym, corto, nombre in SOLO_TABLA:
        try:
            instrumentos.append(instrumento(sym, corto, nombre))
        except Exception as e:
            print(f'  ! {corto}: {e}', file=sys.stderr)

    if not instrumentos:
        print('no se pudo leer ningún instrumento; no se manda nada', file=sys.stderr)
        return 1

    cal, noticias, ts_mercado = del_mercado()
    asunto = f'Overnight · {hoy.strftime("%d %b")}'
    n = 0
    for socio in CFG['socios']:
        correo = socio.get('correo') or ''
        if not correo or 'CAMBIAR' in correo:
            continue
        cuerpo = texto(instrumentos, cal, noticias, ts_mercado, socio.get('nombre', ''))
        if args.prueba:
            f = salida / f'correo-{socio["usuario"]}.txt'
            f.write_text(cuerpo)
            print(f'  → {f}')
        else:
            avisos.mandar_uno(CFG, correo, asunto, cuerpo, imagenes)
            print(f'  → {correo}')
        n += 1

    if args.prueba:
        print(f'\n{len(imagenes)} gráfica(s) en {salida}')
    elif n:
        reloj = avisos.leer_json(avisos.RELOJ)
        reloj['overnight'] = fecha
        avisos.RELOJ.write_text(json.dumps(reloj, ensure_ascii=False, indent=1) + '\n')
    print(f'{n} correo(s) de overnight')
    return 0


if __name__ == '__main__':
    sys.exit(main())
