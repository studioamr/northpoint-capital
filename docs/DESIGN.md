# NORTHPOINT — Sistema de diseño "Dark Glass Institucional"

Aplica IDÉNTICO a `index.html` (landing) y `app.html` (terminal). Ambas páginas deben sentirse
como el mismo producto: una institución financiera de primer nivel. "Institucionalidad silenciosa":
no vendemos esperanza, documentamos evidencia. NADA de AI-slop.

## Prohibido (el usuario lo odia)
- Glow neón, sombras de colores, gradientes morado/rosa genéricos.
- Emojis como iconos. Iconos = SVG de trazo fino (stroke 1.25–1.5, currentColor) o marcadores tipográficos (`01`, `NP-001`, `·`, `—`).
- Tarjetas con border-radius gigante + sombras blandas tipo dribbble.
- Texto de relleno tipo "Lorem" o inglés innecesario. Todo en ESPAÑOL (los términos de trading en inglés se quedan: ORB, BOS, FVG, drawdown, etc.).

## Tokens (copiar tal cual en un bloque :root)
```css
:root{
  --bg:#05070C;
  --bg-2:#090D15;
  --glass:rgba(255,255,255,.045);
  --glass-2:rgba(255,255,255,.075);
  --line:rgba(255,255,255,.09);
  --line-soft:rgba(255,255,255,.05);
  --txt:#E9EDF2;
  --dim:#8A94A6;
  --faint:#59637400; /* usar #596374 — ver nota */
  --accent:#9BC0DC;        /* azul polar — ÚNICO acento */
  --accent-deep:#5E8CAD;
  --up:#57C79B;            /* verde apagado para P&L positivo */
  --down:#DE6A5F;          /* rojo apagado para P&L negativo */
  --warn:#D9A441;          /* ámbar para alertas de regla */
  --sans:'Inter',-apple-system,system-ui,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,monospace;
}
```
Nota: `--faint` debe ser `#596374` (opaco). Verde/rojo/ámbar SOLO para datos (P&L, alertas), nunca decoración.

## Fondo de página
`background:var(--bg)` + 2 radial-gradients MUY sutiles fijos (ej. `radial-gradient(900px 600px at 80% -10%, rgba(155,192,220,.07), transparent)` y otro al 20% 110% con `.04`) + capa de ruido fino (SVG feTurbulence como data-URI, opacity .025, pointer-events none, position fixed). Nada más.

## Glass
- Card: `background:var(--glass); border:1px solid var(--line); border-radius:14px; backdrop-filter:blur(22px) saturate(140%); -webkit-backdrop-filter:...`
- Hover sutil: `background:var(--glass-2)`; transición 200ms. Sin transform llamativo (máx translateY(-2px)).
- Nav: fija arriba, glass con blur fuerte, borde inferior `--line-soft`, altura ~64px.

## Tipografía
- Google Fonts: Inter (400,500,600) + IBM Plex Mono (300,400,500). `<link>` normal.
- Micro-etiquetas: 11px, uppercase, letter-spacing .18em, color `--dim`, font-weight 500. Se usan MUCHO (encabezados de sección, labels de métricas).
- Display (hero landing): Inter 600, clamp(44px, 8vw, 96px), letter-spacing -.03em, line-height .98.
- Números grandes de datos: IBM Plex Mono 300. Los números SIEMPRE en mono.
- Cuerpo: 15px/1.65 `--dim`; títulos de card 16–18px 600 `--txt`.

## Motivo de marca
Una estrella polar / retícula de precisión: SVG minimal (4 trazos finos que cruzan un círculo pequeño) usado como logo junto a "NORTHPOINT" (wordmark en Inter 600 letter-spacing .08em) con "BEHAVIORAL INTELLIGENCE" debajo en micro-etiqueta. Repetir la línea "CONFIDENCIAL · NORTHPOINT.IO" como detalle en footers.

## Layout
- Contenedor max-width 1180px, padding lateral 24px.
- Secciones landing: padding vertical 110px, separadas por `border-top:1px solid var(--line-soft)`.
- Grids: gap 14–18px. Mobile: todo colapsa a 1 columna limpia (media query 900px y 640px).

## Interacción
- Scroll-reveal sutil (IntersectionObserver, opacity+translateY(14px), 500ms) en la landing. En el terminal NO hay reveal: es una herramienta, todo instantáneo.
- Focus visible: outline 1px `--accent-deep`.
