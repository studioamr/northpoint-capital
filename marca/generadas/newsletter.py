#!/usr/bin/env python3
"""
NORTHPOINT · la imagen del bloque NEWSLETTER (family-office.html)

Antes ahí vivía una foto de una persona frente a dos monitores. Se fue: era
André, y el newsletter no va de quién lo escribe. Esto es la EDICIÓN misma,
dibujada: la curva de la semana sobre una página de dos columnas, en el negro
y el oro de la marca.

La semilla está fija a propósito — correrlo otra vez tiene que dar EXACTAMENTE
la misma imagen, o cada despliegue cambiaría la página sin que nadie lo pida.

    python3 marca/generadas/newsletter.py     (desde la raíz del repo)
"""
import random

random.seed(11)

W = 1000
TINTA = '#EFECE7'   # la crema de la marca, aquí de tinta sobre negro
NEGRO = '#090A07'
ORO   = '#C9A84C'
M     = 96          # margen: generoso, es lo que la hace ver cara

p = []
p.append(f'''<defs>
  <radialGradient id="calor" cx=".5" cy=".28" r=".85">
    <stop offset="0" stop-color="#14160F"/><stop offset="1" stop-color="{NEGRO}"/>
  </radialGradient>
  <linearGradient id="bajo" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{TINTA}" stop-opacity=".10"/>
    <stop offset="1" stop-color="{TINTA}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{W}" fill="url(#calor)"/>''')

# ── CABECERA: filete de oro, y dos marcas mono. Nada más. ──
p.append(f'<rect x="{M}" y="{M}" width="{W-2*M}" height="3" fill="{ORO}"/>')
p.append(f'<text x="{M}" y="{M+42}" fill="{TINTA}" fill-opacity=".62" '
         'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="19" '
         'letter-spacing="4.6">SEMANAL</text>')
p.append(f'<text x="{W-M}" y="{M+42}" text-anchor="end" fill="{TINTA}" fill-opacity=".34" '
         'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="19" '
         'letter-spacing="4.6">N&#186; 47</text>')

# ── EL GRÁFICO: una sola línea. La semana, dibujada. ──
gy0, gy1 = 196, 470
for i in range(1, 4):                      # rejilla: tres hilos, casi invisibles
    y = gy0 + (gy1 - gy0) * i / 4
    p.append(f'<line x1="{M}" y1="{y:.0f}" x2="{W-M}" y2="{y:.0f}" '
             f'stroke="{TINTA}" stroke-opacity=".07" stroke-width="1"/>')

pts = [(96,430),(163,404),(230,418),(297,362),(364,378),(431,318),(498,336),
       (565,286),(632,300),(699,254),(766,268),(833,222),(900,204),(904,204)]
d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
p.append(f'<path d="{d} L904,{gy1} L96,{gy1} Z" fill="url(#bajo)"/>')
p.append(f'<path d="{d}" fill="none" stroke="{TINTA}" stroke-width="2.4" '
         'stroke-linejoin="round" stroke-linecap="round" stroke-opacity=".88"/>')
p.append(f'<circle cx="904" cy="204" r="12" fill="{ORO}" fill-opacity=".16"/>')
p.append(f'<circle cx="904" cy="204" r="5" fill="{ORO}"/>')
p.append(f'<line x1="{M}" y1="{gy1}" x2="{W-M}" y2="{gy1}" stroke="{TINTA}" '
         'stroke-opacity=".24" stroke-width="1.4"/>')

# ── EL TEXTO: dos columnas de renglones abstractos. Se lee "esto es una carta". ──
cols = [(M, 380), (W - M - 380, 380)]
y0 = 556
for ci, (cx, cw) in enumerate(cols):
    y = y0
    parr = 0
    while y < W - M - 14:
        largo = random.uniform(.62, 1.0)
        ultimo = random.random() < .26
        if ultimo:
            largo = random.uniform(.30, .55)
        op = .17 if ci == 0 else .13       # la segunda columna, un punto más apagada
        p.append(f'<rect x="{cx}" y="{y:.0f}" width="{cw*largo:.0f}" height="7" rx="3.5" '
                 f'fill="{TINTA}" fill-opacity="{op}"/>')
        y += 26
        if ultimo:
            parr += 1
            y += 22
            if parr == 1 and ci == 0:      # el único bullet de oro, en la primera columna
                p.append(f'<rect x="{cx}" y="{y+1:.0f}" width="7" height="7" fill="{ORO}" fill-opacity=".9"/>')
                p.append(f'<rect x="{cx+18}" y="{y:.0f}" width="{cw*.74:.0f}" height="7" rx="3.5" '
                         f'fill="{TINTA}" fill-opacity=".30"/>')
                y += 26

p.append(f'<rect x="{M}" y="{W-M+6}" width="{W-2*M}" height="1" fill="{TINTA}" fill-opacity=".18"/>')
p.append(f'<rect width="{W}" height="{W}" fill="none" stroke="#000" stroke-width="70" opacity=".16"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}" '
       'role="img" aria-label="La edición semanal del newsletter: la curva de la semana sobre '
       'una página de dos columnas">\n' + '\n'.join(p) + '\n</svg>\n')

with open('marca/generadas/newsletter.svg', 'w') as f:
    f.write(svg)
print('marca/generadas/newsletter.svg —', len(svg), 'bytes')
