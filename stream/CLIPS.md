# De un stream de 4 horas a los clips, solo

El pipeline corre **sin instalar nada**: usa AVFoundation, que ya viene en
tu Mac. Cero descargas, cero servicios, cero suscripciones.

```
   marcador.html          cortar.swift
  (durante el stream)   (cuando terminas)
        │                      │
   marcas-FECHA.json  +  grabación.mp4
                              │
                    ┌─────────┴─────────┐
              clips 1080×1920      resumen 1920×1080
               → TikTok/Reels        → YouTube
```

---

## Una sola vez: que OBS grabe en .mp4

AVFoundation **no lee .mkv**, que es el formato que OBS trae por defecto.

**OBS → Ajustes → Salida → Grabación → Formato de grabación: `mp4`**

Si ya grabaste en .mkv no se perdió nada: **OBS → Archivo → Remuxear
grabaciones** lo convierte a .mp4 sin recomprimir, en segundos.

---

## Durante el stream: marcar

Abre el marcador en la tercera pantalla:

```
https://studioamr.github.io/northpoint-capital/stream/marcador.html
```

1. Dale **▶ EMPEZAR** en el mismo instante que le das grabar a OBS. Ese
   botón pone el cero del cronómetro; todo lo demás se mide desde ahí.
2. Cuando pase algo que merezca clip: **barra espaciadora**. Ya.
3. Las teclas **1 2 3 4** cambian la etiqueta (TRADE / SETUP / EXPLICA /
   REACCIÓN) y **Z** deshace la última.
4. Puedes escribirle una nota a cada marca — esa nota se vuelve el
   **titular del clip** y el nombre del archivo.
5. Al final: **■ TERMINAR** y **↓ EXPORTAR JSON**.

**Lo que marca solo:** si abres el marcador desde `studioamr.github.io`
(no como archivo local), lee el journal de tu Terminal y **marca cada
trade que registras, sin que toques nada**. Tu propio journal es el
detector de momentos. La ayuda de abajo te dice si está conectado.

---

## Después del stream: cortar

Pon la grabación y el .json en la misma carpeta y corre:

```bash
cd ~/Movies    # o donde OBS guarde
swift ~/claude/northpoint/stream/cortar.swift grabacion.mp4 marcas-2026-08-13.json
```

Sale una carpeta `clips-2026-08-13/` con:

- **`clip-01-…mp4` … `clip-NN-…mp4`** — verticales 1080×1920, con la marca
  arriba, el titular abajo y el Discord al pie. Listos para subir tal cual.
- **`resumen-2026-08-13.mp4`** — horizontal, todos los momentos pegados en
  orden, para YouTube.

Banderas:

```bash
swift cortar.swift video.mp4 marcas.json --solo-clips     # nada más los verticales
swift cortar.swift video.mp4 marcas.json --solo-resumen   # nada más el resumen
```

**Cuánto agarra cada clip:** 25 s antes de la marca y 20 s después — el
contexto de *por qué* pasó cabe en el clip, que es lo que hace que un clip
de trading funcione. Se cambia en el .json (`antes` y `despues`).

En el resumen, los momentos que se traslapan se juntan solos: no salen
tramos repetidos.

---

## El flujo completo de un día

| Cuándo | Qué |
|---|---|
| −5 min | Marcador abierto · pantalla de espera al aire |
| 0:00 | **EMPEZAR** en el marcador **y** grabar en OBS, al mismo tiempo |
| durante | Barra espaciadora en cada momento · los trades se marcan solos |
| final | **TERMINAR** → **EXPORTAR JSON** |
| +2 min | `swift cortar.swift …` |
| +10 min | Subes: clips a TikTok/Reels/Shorts · resumen a YouTube |

Los títulos y las miniaturas ya están resueltos en `TITULOS-VOD.md`.

---

## Si algo falla

**"El archivo no trae pista de video que AVFoundation pueda leer"** — es un
.mkv. Remuxéalo desde OBS (Archivo → Remuxear grabaciones).

**Un clip sale "saltado (fuera del video)"** — la marca cayó fuera de la
grabación: casi siempre es que le diste EMPEZAR al marcador antes que a
grabar en OBS. Se arregla editando el `t` de esa marca en el .json.

**Los clips salen sin la marca encima** — no debería pasar, pero si pasa
avísame: el texto se rasteriza con CoreText y ya tiene sus dos trampas
resueltas (los CATextLayer no se dibujan en un script, y el centrado va con
el ancho tipográfico, nunca con `CTLineGetImageBounds`).
