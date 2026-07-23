#!/usr/bin/env python3
"""
Recolector de datos de mercado para el Inicio del terminal.

Corre en GitHub Actions (ver .github/workflows/mercado.yml), no en el navegador:
desde un servidor no hay CORS, así que se puede leer directo de las fuentes.
Deja el resultado en data/mercado.json, que la página lee del mismo origen.

Fuentes:
  · calendario  nfs.faireconomy.media (espejo del calendario de ForexFactory)
  · precios     query1.finance.yahoo.com (futuros continuos, cotización diferida)
  · noticias    RSS de CNBC, MarketWatch y WSJ Markets

Si una fuente falla, se conserva lo que ya había en el archivo para no dejar
el Inicio en blanco, y se marca en 'fallas'.
"""
import json, re, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

RAIZ   = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'data' / 'mercado.json'
UA     = 'Mozilla/5.0 (compatible; NorthpointTerminal/1.0)'

FUTUROS = [
    ('NQ',  'NQ=F',  'Nasdaq 100'),
    ('ES',  'ES=F',  'S&P 500'),
    ('GC',  'GC=F',  'Oro'),
    ('CL',  'CL=F',  'Crudo WTI'),
    ('RTY', 'RTY=F', 'Russell 2000'),
    ('YM',  'YM=F',  'Dow 30'),
]

NOTICIAS = [
    ('CNBC',        'https://www.cnbc.com/id/100003114/device/rss/rss.html'),
    ('MarketWatch', 'https://feeds.content.dowjones.io/public/rss/mw_topstories'),
    ('WSJ Markets', 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml'),
]


def baja(url, timeout=25, intentos=4):
    """Las fuentes gratuitas limitan por ráfaga: se reintenta con espera creciente."""
    espera = 5
    for i in range(intentos):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as err:
            if err.code not in (429, 500, 502, 503, 504) or i == intentos - 1:
                raise
        except urllib.error.URLError:
            if i == intentos - 1:
                raise
        time.sleep(espera)
        espera *= 2


def calendario():
    """Sólo eventos de impacto alto (los rojos) de la semana en curso."""
    crudo = json.loads(baja('https://nfs.faireconomy.media/ff_calendar_thisweek.json'))
    out = []
    for e in crudo:
        if e.get('impact') != 'High':
            continue
        fecha = e.get('date') or ''
        try:
            d = datetime.fromisoformat(fecha)
            dia, hora = d.strftime('%Y-%m-%d'), d.strftime('%H:%M')
        except ValueError:
            dia, hora = fecha[:10], ''
        out.append({
            'dia': dia, 'hora': hora,
            'titulo': (e.get('title') or '').strip(),
            'pais': e.get('country') or '',
            'previsto': (e.get('forecast') or '').strip(),
            'previo': (e.get('previous') or '').strip(),
        })
    out.sort(key=lambda x: (x['dia'], x['hora']))
    return out


def precios():
    out = []
    for sym, yah, nombre in FUTUROS:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{yah}?range=5d&interval=1d'
        try:
            m = json.loads(baja(url))['chart']['result'][0]['meta']
        except Exception as err:            # un símbolo caído no tumba a los demás
            print(f'  ! {sym}: {err}', file=sys.stderr)
            continue
        p = m.get('regularMarketPrice')
        prev = m.get('chartPreviousClose') or m.get('previousClose')
        if p is None or not prev:
            continue
        out.append({
            'sym': sym, 'nombre': nombre,
            'precio': round(p, 2),
            'cambio': round(p - prev, 2),
            'pct': round((p - prev) / prev * 100, 2),
        })
    return out


def _texto(bloque, etiqueta):
    m = re.search(rf'<{etiqueta}[^>]*>(.*?)</{etiqueta}>', bloque, re.S)
    if not m:
        return ''
    t = m.group(1)
    t = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', t, flags=re.S)
    return unescape(re.sub(r'<[^>]+>', '', t)).strip()


def noticias():
    """Titulares de las tres fuentes, más recientes primero y sin repetidos."""
    todo = []
    for fuente, url in NOTICIAS:
        try:
            xml = baja(url)
        except Exception as err:
            print(f'  ! {fuente}: {err}', file=sys.stderr)
            continue
        for bloque in re.findall(r'<item[^>]*>(.*?)</item>', xml, re.S)[:12]:
            titulo = _texto(bloque, 'title')
            if not titulo:
                continue
            todo.append({
                'titulo': titulo,
                'url': _texto(bloque, 'link'),
                'fuente': fuente,
                'fecha': _texto(bloque, 'pubDate'),
            })

    def cuando(n):
        try:
            return parsedate_to_datetime(n['fecha']).timestamp()
        except Exception:
            return 0.0

    todo.sort(key=cuando, reverse=True)
    limite = time.time() - 3 * 86400          # el feed de WSJ arrastra items viejos
    vistos, out = set(), []
    for n in todo:
        clave = n['titulo'].lower()
        if clave in vistos or cuando(n) < limite:
            continue
        vistos.add(clave)
        out.append(n)
    return out[:24]


def videos():
    """Video más reciente de cada canal.

    El RSS de YouTube (feeds/videos.xml) responde 404 desde servidores, así que se
    lee la pestaña /videos del canal y se saca el primer elemento de ytInitialData.
    De ahí salen id, título y antigüedad; la miniatura se arma con el id.
    """
    cfg = json.loads((RAIZ / 'data' / 'canales.json').read_text())
    out = []
    for c in cfg.get('canales', []):
        try:
            html = baja(f"https://www.youtube.com/channel/{c['id']}/videos", timeout=30)
            m = re.search(r'var ytInitialData = (\{.*?\});</script>', html, re.S)
            if not m:
                raise ValueError('sin ytInitialData')
            datos = json.loads(m.group(1))
        except Exception as err:
            print(f"  ! {c['nombre']}: {err}", file=sys.stderr)
            continue

        encontrados = []

        def recorre(o):
            if encontrados:
                return
            if isinstance(o, dict):
                lv = o.get('lockupViewModel')
                if isinstance(lv, dict) and lv.get('contentId'):
                    encontrados.append(lv)
                    return
                for v in o.values():
                    recorre(v)
            elif isinstance(o, list):
                for v in o:
                    recorre(v)

        recorre(datos)
        if not encontrados:
            print(f"  ! {c['nombre']}: sin videos en la página", file=sys.stderr)
            continue

        lv = encontrados[0]
        vid = lv['contentId']
        meta = lv.get('metadata', {}).get('lockupMetadataViewModel', {})
        titulo = (meta.get('title') or {}).get('content', '').strip()
        cuando = ''
        for fila in (meta.get('metadata', {}).get('contentMetadataViewModel', {})
                         .get('metadataRows', [])):
            for parte in fila.get('metadataParts', []):
                t = (parte.get('text') or {}).get('content', '')
                if t.startswith('hace') or 'ago' in t:
                    cuando = t
        out.append({
            'canal': c['nombre'], 'canalId': c['id'],
            'id': vid, 'titulo': titulo, 'cuando': cuando,
            'thumb': f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg',
            'url': f'https://www.youtube.com/watch?v={vid}',
        })
    return out


def main():
    previo = {}
    if SALIDA.exists():
        try:
            previo = json.loads(SALIDA.read_text())
        except Exception:
            previo = {}

    datos, fallas = {}, []
    for clave, fn in (('calendario', calendario), ('precios', precios),
                      ('noticias', noticias), ('videos', videos)):
        try:
            v = fn()
            if not v:
                raise ValueError('sin resultados')
            datos[clave] = v
            print(f'  {clave}: {len(v)}')
        except Exception as err:
            fallas.append(clave)
            datos[clave] = previo.get(clave, [])       # se conserva lo anterior
            print(f'  ! {clave} falló ({err}); se conservan {len(datos[clave])} previos', file=sys.stderr)

    cfg = json.loads((RAIZ / 'data' / 'canales.json').read_text())
    datos['directos'] = cfg.get('directos', [])
    datos['ts'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    datos['fallas'] = fallas
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False, indent=1))
    print(f'→ {SALIDA} ({SALIDA.stat().st_size} bytes)')
    return 1 if len(fallas) == 4 else 0


if __name__ == '__main__':
    sys.exit(main())
