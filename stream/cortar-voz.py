#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte la grabación de André en las 19 tomas del guion.

Nadie graba 19 archivos: se graba de corrido con 3 segundos de silencio entre
toma y toma, y aquí se detectan esos silencios. Si hay MÁS trozos que tomas es
porque repitió alguna — se queda con las últimas, que son las buenas.

    python3 cortar-voz.py ~/Movies/voz-andre.m4a
"""
import sys, os, subprocess, wave, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
INTRO = os.path.join(AQUI, '..', '.respaldos', 'intro')
DEST = os.path.join(INTRO, 'voz-real')
SR = 44100
SILENCIO_MIN = 1.6      # un corte de verdad; una pausa de respiración no llega
UMBRAL_REL = 0.030      # del pico: lo que está debajo cuenta como silencio


def a_wav(src):
    """cualquier formato → wav mono 44.1k, con el afconvert que ya trae el Mac"""
    tmp = '/tmp/np-voz.wav'
    subprocess.run(['/usr/bin/afconvert', '-f', 'WAVE', '-d', 'LEI16@44100',
                    '-c', '1', src, tmp], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmp


def lee(ruta):
    with wave.open(ruta) as w:
        n, ancho, canales = w.getnframes(), w.getsampwidth(), w.getnchannels()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
        if canales > 1:
            x = x.reshape(-1, canales).mean(axis=1)
        return x, w.getframerate()


def trozos(x, sr):
    """envolvente por ventanas de 20 ms → tramos con voz"""
    v = int(sr * 0.02)
    env = np.abs(x[:len(x)//v*v].reshape(-1, v)).max(axis=1)
    umbral = env.max() * UMBRAL_REL
    hay = env > umbral
    huecoMin = int(SILENCIO_MIN / 0.02)

    out, ini = [], None
    quieto = 0
    for i, h in enumerate(hay):
        if h:
            if ini is None: ini = i
            quieto = 0
        elif ini is not None:
            quieto += 1
            if quieto >= huecoMin:
                out.append((ini*v, (i-quieto)*v)); ini = None
    if ini is not None: out.append((ini*v, len(hay)*v))
    # fuera los suspiros sueltos: menos de un segundo no es una toma
    return [(a, b) for a, b in out if (b-a)/sr > 1.0]


def guarda(x, sr, ruta):
    d = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(ruta, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(d.tobytes())


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Movies/voz-andre.m4a')
    if not os.path.exists(src):
        sys.exit('  ✗ no encuentro ' + src)
    plan = json.load(open(os.path.join(INTRO, 'plan.json')))
    x, sr = lee(a_wav(src) if not src.lower().endswith('.wav') else src)
    tr = trozos(x, sr)
    print('  · %d trozos con voz · %d tomas esperadas' % (len(tr), len(plan)))
    if len(tr) < len(plan):
        print('  ⚠ faltan tomas: revisa que los silencios sean de 3 s completos')
    tr = tr[-len(plan):]        # si repitió, las últimas son las buenas

    os.makedirs(DEST, exist_ok=True)
    for (a, b), bl in zip(tr, plan):
        # 120 ms de aire a cada lado para que no corte la última sílaba
        aire = int(sr * 0.12)
        trozo = x[max(0, a-aire): min(len(x), b+aire)]
        ruta = os.path.join(DEST, bl['nombre'] + '.wav')
        guarda(trozo, sr, ruta)
        print('    ✓ %-16s %5.1fs' % (bl['nombre'], len(trozo)/sr))
    print('  ── listo en %s' % DEST)
