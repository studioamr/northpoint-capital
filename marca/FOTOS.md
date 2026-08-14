# Las fotos · 10 minutos, una sola vez

El procesador (`retratos.swift`) convierte tus fotos en retratos con el lenguaje
de NORTHPOINT: blanco y negro, negros profundos, fondo apagado. Pero **no puede
inventar luz que no está**. Con una selfie de noche a contraluz el resultado es
una mancha — probado tres veces.

Esto es lo único que hace falta, y es una sola sesión de diez minutos.

## Dónde

**Junto a una ventana, de día.** No a mediodía con sol directo: mejor por la
mañana o en la tarde, o con el cielo nublado. Esa es la mejor luz de retrato que
existe y es gratis.

- Ponte **de lado a la ventana**, no de frente: la luz que entra por un costado
  es la que hace la sombra en medio rostro. De frente te aplana la cara.
- Detrás de ti, **una pared lisa y oscura** — o simplemente aléjate de la pared
  unos dos metros, así el fondo se va solo.
- **No de espaldas a la ventana.** Eso es lo que arruinó la foto del saco.

## Cómo

- **Camiseta negra lisa.** Sin logos, sin cuello blanco. El blanco cerca de la
  cara revienta y se come la foto.
- El celular **a la altura de tus ojos**, no abajo. Desde abajo sales en
  contrapicado y se ve a selfie.
- Que alguien te las tome, o apoya el celular y usa el temporizador. **Con el
  brazo estirado no sale**: deforma la cara y se nota.
- Cámara **trasera**, no la frontal: tiene el triple de calidad.

## Qué tomar — seis fotos

| | |
|---|---|
| 1 | De frente, mirando al lente, **sin sonreír**, mandíbula firme |
| 2 | De frente, **sonriendo de verdad** (ésta es la de Instagram) |
| 3 | Tres cuartos — medio girado, ojos al lente |
| 4 | Perfil completo, 90° |
| 5 | Medio cuerpo, brazos cruzados |
| 6 | De espaldas mirando por la ventana |

De cada una toma tres o cuatro. Salen 20 fotos en diez minutos y de ahí saco el
portafolio completo.

## Después

Déjalas en `marca/fotos/` y corre:

```bash
swift marca/retratos.swift
```

De cada foto salen tres: **retrato** (la página de perfil), **avatar** (IG,
TikTok, YouTube) y **portada** (banner de YouTube). La cara se localiza sola con
Vision, así que el encuadre no depende de cómo hayas apuntado.

Si prefieres el color: `swift marca/retratos.swift --color`
