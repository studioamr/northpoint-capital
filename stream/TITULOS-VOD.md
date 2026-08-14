# Títulos, descripción y miniatura del VOD

Elige el bloque según **cómo salió la sesión**. La regla que manda: el
título tiene que ser verdad. Un título que promete lo que el video no
entrega mata el canal más rápido que un título aburrido.

---

## 1 · Si NO hubo trade

**Miniatura:** `miniatura-sin-trade.png` — *NO TRADE. / Y FUE UN BUEN DÍA*

Títulos, de más a menos fuerte:

1. `3 horas esperando y CERO trades — así opero una cuenta de fondeo`
2. `No operé hoy. Y por eso sigo con la cuenta viva | NORTHPOINT en vivo`
3. `El día que NO tradear es la mejor decisión | Sesión de Asia en vivo`
4. `Sesión de Asia completa sin un solo trade — la paciencia como sistema`

**Por qué funcionan:** todos los demás suben "mi trade ganador". Un título
que presume no haber operado es raro, y lo raro se abre.

---

## 2 · Si hubo un trade (ganó o perdió)

**Miniatura:** `miniatura-un-trade.png` — *UN SOLO TRADE / ASÍ SE OPERA UNA
CUENTA DE FONDEO*

Si **ganó**:

1. `Un solo trade en toda la sesión — y me fui a casa | NORTHPOINT en vivo`
2. `Esperé 3 horas por esta entrada | Futuros del Nasdaq en vivo`
3. `Así opero MNQ en la sesión de Asia — un trade al día, sin excepción`

Si **perdió** (súbelo igual, este es el que construye confianza):

1. `Perdí el trade de hoy — y respeté todas mis reglas | NORTHPOINT en vivo`
2. `Así se ve perder con disciplina | Sesión de Asia en futuros`
3. `Stop respetado, día cerrado. Sin revancha. | NORTHPOINT en vivo`

**No uses** "así gané $X" ni cifras en el título del VOD. Atrae al público
que quiere el dinero, no al que quiere el método — y ése es el que no se
queda.

---

## 3 · Si es el estreno / hubo problemas técnicos

**Miniatura:** `miniatura-estreno.png` — *EN VIVO / LA MESA DE NORTHPOINT*

1. `Primer stream: la mesa de NORTHPOINT en vivo | Sesión de Asia`
2. `Empieza NORTHPOINT — trading de futuros en vivo, de verdad`

---

## Descripción del VOD (pégala tal cual y ajusta la primera línea)

```
[Una línea con lo que pasó hoy. Ej: "Sesión de Asia completa. Cero trades:
las condiciones no aparecieron y el día se cerró en paz."]

Esto es NORTHPOINT: una mesa de futuros en vivo, de lunes a viernes.
No es un canal de señales. Aquí se ve cómo se opera de verdad —
incluyendo las horas en las que no pasa nada.

LAS REGLAS DE LA MESA
◆ Un solo trade al día
◆ Sin alerta, no hay trade
◆ El stop se respeta, siempre
◆ Cada trade se escribe
◆ La paciencia es la ventaja

NORTHPOINT respalda a traders que YA son rentables: tú demuestras tus
payouts, nosotros pagamos tus evaluaciones.

La firma → https://studioamr.github.io/northpoint-capital
La comunidad → https://discord.gg/TWeVqTTPS

AVISO: no soy asesor financiero y nada de este video es una recomendación
de inversión. Los futuros usan apalancamiento y se puede perder dinero
rápidamente. Lo que ves es mi operación con mi cuenta y mis reglas.

#futuros #trading #nasdaq #daytrading #cuentasdefondeo #NORTHPOINT
```

---

## Cómo hacer una miniatura nueva en 10 segundos

Abre `stream/miniatura.html` cambiando el texto en la URL:

```
miniatura.html?t=NO TRADE.&s=Y FUE UN BUEN DÍA&n=0&e=ASIA SESSION
```

- `t` = la línea gigante — **máximo 3 palabras**
- `s` = la línea de abajo, el giro
- `n` = el número grande de la esquina (déjalo vacío para apagarlo)
- `e` = la etiqueta de sesión

Captura la ventana a **1280×720** y listo.

**La prueba que nunca falla:** achica la miniatura hasta que mida el ancho
de tu pulgar. Si la línea grande sigue leyéndose, sirve. Si no, menos
palabras.
