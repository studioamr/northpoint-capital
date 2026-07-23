#!/usr/bin/env python3
"""
Vigila la mesa y avisa por correo a los socios cuando algo pide su atención.

Corre en GitHub Actions (.github/workflows/avisos.yml) cada 5 minutos. El navegador
no puede mandar correo desde un sitio estático, así que el aviso sale de aquí.

Qué avisa:
  · una tesis nueva esperando firmas
  · cada firma que se agrega, y a quién le toca la siguiente
  · una tesis que ya juntó las cuatro y está lista para ejecutarse
  · una tesis rechazada
  · un trade registrado con violación de disciplina
  · una cuenta cuyo colchón se acercó al corte

Compara el estado actual contra data/avisos-visto.json, que el propio trabajo
actualiza y commitea. Así nunca manda dos veces el mismo aviso.

Secretos que necesita (en GitHub → Settings → Secrets and variables → Actions):
  SUPABASE_URL           https://xxxx.supabase.co
  SUPABASE_SERVICE_KEY   la llave sb_secret_… (NUNCA va en el repositorio)
  GMAIL_USER             la cuenta desde la que sale el correo
  GMAIL_APP_PASSWORD     contraseña de aplicación de Google, no la del correo
"""
import json
import os
import smtplib
import ssl
import sys
import urllib.request
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CFG = RAIZ / 'data' / 'avisos.json'
VISTO = RAIZ / 'data' / 'avisos-visto.json'
TERMINAL = 'https://studioamr.github.io/northpoint-capital/app.html'

GATES = [('research', 'Research'), ('riesgo', 'Riesgo'),
         ('quant', 'Quant'), ('cio', 'CIO')]


def leer_mesa():
    url = os.environ['SUPABASE_URL'].rstrip('/')
    key = os.environ['SUPABASE_SERVICE_KEY']
    req = urllib.request.Request(
        f'{url}/rest/v1/northpoint_estado?id=eq.1&select=data,rev',
        headers={'apikey': key, 'Authorization': f'Bearer {key}'})
    with urllib.request.urlopen(req, timeout=25) as r:
        filas = json.loads(r.read().decode())
    if not filas:
        raise SystemExit('La mesa está vacía en la nube.')
    return filas[0].get('data') or {}, filas[0].get('rev', 0)


def nombre_de(cfg, usuario):
    for s in cfg['socios']:
        if s['usuario'] == usuario:
            return s['nombre']
    return usuario or 'alguien'


def faltantes(t):
    firmas = t.get('firmas') or {}
    return [etiqueta for clave, etiqueta in GATES if clave not in firmas]


def novedades(cfg, mesa, visto):
    """Compara y devuelve [(asunto, cuerpo)] de lo que cambió."""
    av = cfg.get('avisar', {})
    salida = []

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

    # trades con violación
    if av.get('trade_con_violacion'):
        vistos = set(visto.get('trades_avisados') or [])
        for tr in ((mesa.get('resumen') or {}).get('trades_violados') or []):
            vs = tr.get('violaciones') or []
            if vs and tr.get('id') not in vistos:
                salida.append((
                    f'Violación · {tr.get("sym")} {tr.get("date")}',
                    f'El trade de {tr.get("date")} {tr.get("time")} en '
                    f'{tr.get("sym")} quedó marcado: {", ".join(vs)}.'))

    # colchón bajo
    if av.get('colchon_bajo'):
        limite = cfg.get('colchon_minimo', 700)
        avisadas = set(visto.get('cuentas_avisadas') or [])
        for c in ((mesa.get('resumen') or {}).get('cuentas_salud') or []):
            if c.get('colchon') is not None and c['colchon'] <= limite \
                    and c.get('alias') not in avisadas:
                salida.append((
                    f'Colchón bajo · {c.get("alias")}',
                    f'La cuenta {c.get("alias")} quedó a {c["colchon"]} dólares del '
                    f'corte. El CRO tiene autoridad para detener la mesa.'))

    return salida


def mandar(cfg, avisos):
    usuario = os.environ['GMAIL_USER']
    clave = os.environ['GMAIL_APP_PASSWORD']
    destinos = [s['correo'] for s in cfg['socios']
                if s.get('correo') and 'CAMBIAR' not in s['correo']]
    if not destinos:
        print('  ! los correos de data/avisos.json siguen sin configurar', file=sys.stderr)
        return 0

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
            print(f'  → {asunto}')
    return len(avisos)


def main():
    cfg = json.loads(CFG.read_text())
    if not cfg.get('activo'):
        print('avisos desactivados en data/avisos.json')
        return 0

    faltan = [k for k in ('SUPABASE_URL', 'SUPABASE_SERVICE_KEY',
                          'GMAIL_USER', 'GMAIL_APP_PASSWORD')
              if not os.environ.get(k)]
    if faltan:
        print('Faltan secretos: ' + ', '.join(faltan), file=sys.stderr)
        return 1

    mesa, rev = leer_mesa()
    visto = {}
    if VISTO.exists():
        try:
            visto = json.loads(VISTO.read_text())
        except Exception:
            visto = {}

    primera = not visto
    avisos = [] if primera else novedades(cfg, mesa, visto)
    if primera:
        print('primera corrida: se toma foto sin avisar de lo que ya existía')

    n = mandar(cfg, avisos) if avisos else 0
    if not avisos:
        print('sin novedades')

    VISTO.write_text(json.dumps({
        'rev': rev,
        'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'tickets': {t['id']: {'firmas': t.get('firmas') or {}, 'estado': t.get('estado')}
                    for t in (mesa.get('tickets') or []) if t.get('id')},
        'trades_avisados': [t['id'] for t in ((mesa.get('resumen') or {}).get('trades_violados') or []) if t.get('id')],
        'cuentas_avisadas': [c.get('alias') for c in ((mesa.get('resumen') or {}).get('cuentas_salud') or [])
                             if c.get('colchon') is not None
                             and c['colchon'] <= cfg.get('colchon_minimo', 700)],
    }, ensure_ascii=False, indent=1))
    print(f'{n} aviso(s) · rev {rev}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
