#!/usr/bin/env python3
"""
NORTHPOINT · la música de los clips

Compone un loop ORIGINAL — nada de librerías de terceros, nada de samples
con dueño: se sintetiza aquí. Eso importa porque TikTok y YouTube tumban
audio con derechos, y un canal que vive de credibilidad no puede comerse
un strike por una rola de fondo.

El mood es el de la marca: melodic techno oscuro y contenido, la línea de
Anyma / Afterlife. Sub grave que sostiene, pad menor que respira, un
arpegio que aparece y se va, y percusión seca muy atrás. Nada que compita
con la voz: el filtro deja el rango de 300–3400 Hz mayormente libre.

    python3 musica.py 60 clip.wav      # 60 segundos
"""
import sys, math, wave, struct
import numpy as np

SR = 44100
BPM = 122                      # el tempo de la casa (OBSIDIANA iba aquí)
COMPAS = 60.0 / BPM * 4

# Fa menor: la tonalidad de OBSIDIANA. Grados en Hz (F2 como raíz).
F2 = 87.31
ESCALA = {'F':1.0, 'Ab':1.189207, 'C':1.498307, 'Db':1.587401, 'Eb':1.781797}


def env(n, a, d, s, r, sus=0.7):
    """envolvente ADSR en muestras"""
    a, d, r = int(a*SR), int(d*SR), int(r*SR)
    s = max(0, n - a - d - r)
    return np.concatenate([
        np.linspace(0, 1, a, endpoint=False) if a else np.array([]),
        np.linspace(1, sus, d, endpoint=False) if d else np.array([]),
        np.full(s, sus),
        np.linspace(sus, 0, r) if r else np.array([]),
    ])[:n]


def sierra(f, n, detune=0.0):
    """diente de sierra por suma de armónicos — suena analógico, no digital"""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for k in range(1, 14):
        x += np.sin(2*np.pi*f*(1+detune)*k*t) / k
    return x * 0.35


def seno(f, n, fase=0.0):
    t = np.arange(n) / SR
    return np.sin(2*np.pi*f*t + fase)


def pasabajos(x, corte, res=0.7):
    """filtro de un polo, aplicado dos veces: suave, sin resonancia chillona"""
    a = math.exp(-2*math.pi*corte/SR)
    y = np.zeros_like(x)
    z = 0.0
    for i in range(len(x)):
        z = (1-a)*x[i] + a*z
        y[i] = z
    z = 0.0
    y2 = np.zeros_like(y)
    for i in range(len(y)):
        z = (1-a)*y[i] + a*z
        y2[i] = z
    return y2 * (1 + res)


def compone(segundos):
    n = int(segundos * SR)
    mezcla = np.zeros(n)
    t = np.arange(n) / SR

    # ── SUB: la raíz que sostiene todo, con respiración lenta ──
    sub = seno(F2/2, n) * 0.42
    sub *= 0.85 + 0.15*np.sin(2*np.pi*t/(COMPAS*2))
    mezcla += sub

    # ── PAD: acorde de Fa menor, filtrado y en movimiento ──
    pad = np.zeros(n)
    for g, det in [('F', 0), ('Ab', 0.002), ('C', -0.003)]:
        pad += sierra(F2*ESCALA[g]*2, n, det)
    # el filtro se abre y se cierra cada dos compases: eso es lo que respira
    corte = 420 + 260*np.sin(2*np.pi*t/(COMPAS*2))
    trozo = SR//4
    filtrado = np.zeros(n)
    for i in range(0, n, trozo):
        j = min(i+trozo, n)
        filtrado[i:j] = pasabajos(pad[i:j], float(corte[i]))
    mezcla += filtrado * 0.30

    # ── ARPEGIO: aparece a partir del segundo cuarto y se va al final ──
    paso = COMPAS/8
    notas = ['F','Ab','C','Eb','C','Ab','Db','C']
    arp = np.zeros(n)
    k = 0
    tt = 0.0
    while tt < segundos:
        i = int(tt*SR)
        largo = int(paso*0.9*SR)
        if i+largo > n:
            break
        f = F2*ESCALA[notas[k % len(notas)]]*4
        voz = (seno(f, largo)*0.6 + sierra(f, largo, 0.004)*0.4)
        voz *= env(largo, 0.004, 0.05, 0, 0.10, 0.25)
        arp[i:i+largo] += voz
        k += 1
        tt += paso
    # entra y sale con la pieza
    ent = np.clip((t - segundos*0.22) / (segundos*0.12), 0, 1)
    sal = np.clip((segundos*0.92 - t) / (segundos*0.08), 0, 1)
    mezcla += arp * 0.13 * ent * sal

    # ── PERCUSIÓN: bombo seco muy atrás y un hat cerrado a contratiempo ──
    negra = COMPAS/4
    tt = 0.0
    while tt < segundos:
        i = int(tt*SR)
        largo = min(int(0.16*SR), n-i)
        if largo > 0:
            f = np.linspace(58, 40, largo)
            bombo = np.sin(2*np.pi*np.cumsum(f)/SR) * env(largo, 0.001, 0.03, 0, 0.12, 0.4)
            mezcla[i:i+largo] += bombo * 0.28
        # hat en el "y" del tiempo
        j = int((tt+negra/2)*SR)
        lh = min(int(0.03*SR), n-j)
        if lh > 0 and j > 0:
            hat = np.random.default_rng(int(tt*100)).normal(0, 1, lh)
            hat *= env(lh, 0.001, 0.006, 0, 0.02, 0.1)
            mezcla[j:j+lh] += hat * 0.035
        tt += negra

    # ── el hueco para la VOZ: se baja lo que compite con ella ──
    # (un notch suave alrededor de 300–3000 Hz vía resta de la banda)
    banda = mezcla - pasabajos(mezcla, 300)
    agudos = banda - pasabajos(banda, 3000) * 0
    mezcla = mezcla - agudos*0.35

    # ── entrada y salida, y normalizado con techo ──
    fade = int(1.6*SR)
    mezcla[:fade] *= np.linspace(0, 1, fade)
    mezcla[-fade:] *= np.linspace(1, 0, fade)
    pico = np.max(np.abs(mezcla))
    if pico > 0:
        mezcla = mezcla / pico * 0.72
    return mezcla


def guarda(x, ruta):
    datos = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    est = np.repeat(datos[:, None], 2, axis=1).flatten()
    with wave.open(ruta, 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(est.tobytes())


if __name__ == '__main__':
    seg = float(sys.argv[1]) if len(sys.argv) > 1 else 60
    ruta = sys.argv[2] if len(sys.argv) > 2 else 'northpoint-loop.wav'
    guarda(compone(seg), ruta)
    print(f'  ♪ {ruta} · {seg:.0f}s · {BPM} BPM · Fa menor')
