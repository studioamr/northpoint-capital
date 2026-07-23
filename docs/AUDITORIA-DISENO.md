# NORTHPOINT · Auditoría profesional de diseño

**Fecha:** 22 jul 2026 · **Alcance:** `app.html` (terminal, ~2,950 líneas) + `index.html` (landing, ~1,601 líneas), leídos completos.
**Método:** 5 auditores especializados en paralelo (tipografía/jerarquía, color/contraste WCAG con cálculo de luminancia, consistencia de componentes, UX de flujos con pruebas en navegador real a 1280px y 375px, accesibilidad) → 58 hallazgos → verificación adversarial de los 22 más severos contra el código real → 19 confirmados, 2 refutados. Los cálculos de contraste y las mediciones móviles fueron reproducidos independientemente por el verificador.

---

## Veredicto general

La base del sistema es **sólida y se respeta**: mono para datos, micro-etiquetas uppercase, acento azul polar usado como tinta (sin glow, disciplina confirmada en ambos archivos), glass consistente, `:focus-visible` global, Escape cierra modales, empty states con acción, hash routing correcto, toasts en las escrituras. El problema no es el diseño — es la **deriva de ejecución**: tokens que se duplican, tamaños que se fragmentan, y un breakpoint móvil que existe (rail drawer a 960px) pero que nadie terminó de cablear.

**Los tres frentes que concentran el daño:** (1) móvil roto en los tres puntos que más importan, (2) el token `--faint` falla WCAG en texto funcional en toda la app, (3) semántica de color contaminada en el journal.

---

## Hallazgos confirmados

### A · Móvil (el frente más urgente)

| # | Sev | Hallazgo | Evidencia | Fix |
|---|-----|----------|-----------|-----|
| A1 | MAJOR | **Modal "Registrar trade" desborda el viewport**: `.f-row3` (3 columnas sin media query) + input date de 147px min-content → contenido a ~425px en pantalla de 375px; el select Instrumento queda 50px fuera. Es el flujo núcleo. | `.f-row3` ~l.468; medido en vivo a 375px | `@media(max-width:640px){.f-row,.f-row3{grid-template-columns:1fr 1fr}.modal{padding:20px 16px}}` + `min-width:0` en inputs/selects |
| A2 | MAJOR | **Calendario ilegible en móvil**: celdas 40×40 (`aspect-ratio:1`+`overflow:hidden`) recortan "−$400" a "−$4" y "+$1,500" a "+$1,"; barra y W·L invisibles. | `.ts-cell` l.343-349; medido: scrollWidth 30 vs clientWidth 24 | En `@media 760px`: `aspect-ratio:auto;min-height:36px`, ocultar `.ts-bar`/`.ts-wl` y columna semanal, monto compacto |
| A3 | MAJOR | **Topbar desborda 146px** justo en el estado más importante: pill "VENTANA ABIERTA · CIERRA 8:30" (261px, nowrap) + reloj min-width 78px → scrollWidth 521px a 375px, con `body{overflow:hidden}` el reloj es inalcanzable. | `.topbar` l.124-131, `.sess-pill` l.141; medido en vivo | `@media 640px`: ocultar `.top-clock`, pill a 9.5px, `min-width:0`+ellipsis en el título |
| A4 | MAJOR | **Los ~20 SVGs del Bootcamp escalan su texto a ~4.3px reales** en móvil (viewBox 640 → contenedor ~290px). Es el contenido didáctico principal. | `.doc-fig svg` l.407 | `.doc-fig{overflow-x:auto}` + `.doc-fig svg{min-width:560px}` (mismo patrón que la tabla del journal) |

### B · Contraste y semántica de color

| # | Sev | Hallazgo | Evidencia | Fix |
|---|-----|----------|-----------|-----|
| B1 | MAJOR | **`--faint #596374` falla WCAG AA en TODOS sus usos funcionales** (3.32:1 sobre bg, 3.14:1 sobre card; requerido 4.5:1 en <18px): headers de tabla, firmas de las puertas ("✓ Mateo · 07:41"), fechas del journal, estado de nube, disclaimers, empty-states, botones ✎/✕ — a 8–11px. Aplica igual en la landing (aviso legal, vehículos, copyright). | `app.html:25`, `index.html:24` + 9 selectores citados; luminancia recalculada a mano | Subir el token a `--faint:#7A8698` (5.46:1/5.16:1, conserva la jerarquía de 3 escalones) en ambos archivos; el aviso legal de la landing mejor a `--dim` |
| B2 | MAJOR | **LONG verde / SHORT rojo rompe la semántica**: un SHORT ganador muestra tag rojo junto a P&L verde, y ese mismo rojo significa "violación" dos celdas a la derecha. Tres significados de rojo en una fila — en la tabla cuyo propósito es detectar violaciones. | `app.html:1835` (el inline `border-color:var(--line)` delata que la clase estaba mal elegida) | Tag de dirección neutro: `.tag.dir{color:var(--txt)}` — verde/rojo reservados a resultado y disciplina |
| B3 | MINOR | **Dos verdes y dos rojos conviven**: tokens de app (`#5FBF9A/#D96D62`) ≠ landing y sistema (`#57C79B/#DE6A5F`), y dentro de app.html se mezclan ambas familias en componentes adyacentes (calendario/gates/SVGs vs tags/verdict/banner/canvas). ΔE pequeño — casi imperceptible, pero es drift real. | `app.html:28-29` vs `index.html:27-28` + 10 líneas rgba citadas | Unificar tokens a `#57C79B/#DE6A5F` y reemplazar las rgba de la familia vieja (l.144, 235-236, 273, 275, 553, 555, canvas 1572) |

### C · Accesibilidad y robustez

| # | Sev | Hallazgo | Evidencia | Fix |
|---|-----|----------|-----------|-----|
| C1 | MAJOR | **El candado de login es solo visual**: `pointer-events:none` no bloquea Tab ni lector de pantalla. Sin sesión se puede tabular al rail borroso, abrir Perfil con Enter y llegar a «Borrar todo» (los `confirm()` se aceptan con Enter, a ciegas). | `body.locked .app` l.329; `lockUI()` ~l.2646 | `inert` en `.app` al bloquear (+`visibility:hidden` como refuerzo); quitar al desbloquear |
| C2 | MAJOR | **Ningún modal es un diálogo accesible**: sin `role="dialog"`/`aria-modal`/nombre, y `openOv()` no mueve el foco al abrir ni lo devuelve al cerrar (solo Escape funciona). | `openOv()` l.2746; markup 963-1075 | `role`+`aria-modal`+`aria-labelledby` en los 6 overlays; guardar/restaurar foco y `inert` en `.app` durante el modal |

### D · Sistema tipográfico (deriva)

| # | Sev | Hallazgo | Fix |
|---|-----|----------|-----|
| D1 | MAJOR | Micro-etiquetas en **7 tamaños y 9 trackings** sin patrón; los 8px (.ts-wl, .rail-brand) llevan datos reales bajo el piso de legibilidad | Dos tokens: micro 10px/.16em y micro-denso 9px/.14em; nada bajo 9px; tracking ≥.22em solo para el lockup de marca |
| D2 | MAJOR | El **mismo stat tile en 5 cuerpos** (22/22 inline/19 inline/19/18/17px) — el token se erosiona con styles inline en los templates JS | 22px KPI primario (borrar overrides l.1368 y 2451) + clase `.mini-v` 17px para minis |
| D3 | MINOR | Escala global de **24 tamaños** (incl. un 12.8px huérfano); `label` duplica a `.micro` | Tokens `--fs-*` con ~9 pasos y mapeo propuesto |
| D4 | MINOR | Cifras mono grandes oscilan entre **peso 300 y 500** según la vista (el 300 llegó del port de Spotter) | Regla única: numeral mono ≥19px → 300 |
| D5 | MINOR | `<b>` sin regla hereda **Inter 700** (más pesado que cualquier título del sistema); tickers "NQ · LONG" en sans donde el journal los pone en mono | `b{font-weight:600}`, quitar `;700` de la URL de fuentes, tickers de aprobaciones a mono |
| D6 | MINOR | Bug de scoping: el subtítulo del login (`class="sub"`) cae al estilo base (14px blanco) porque la regla es `.modal .sub` y `.login-card` no es `.modal` | Selector → `.modal .sub,.login-card .sub` |
| D7 | MINOR | Disclaimer legal de Posiciones forzado a **9px mono uppercase-ish** cuando la landing resuelve el mismo aviso a 12px sans | Usar el patrón `.legal` de la landing |

---

## Hallazgos adicionales del barrido (detectados, no verificados uno a uno)

Del barrido inicial de 58, estos quedaron fuera del corte de verificación pero los auditores los reportaron con evidencia; tómalos como muy probables:

**UX:** «Cargar demo» cierra la sesión silenciosamente · guardar un trade desde Sesión deja el banner de gestión (regla de 2 trades) sin refrescar (información falsa) · el KPI SEMANA pierde los lunes por mezclar `toISOString()` (UTC) con fechas locales · «Ejecutada — registrar en Journal» descarta el instrumento/dirección que la mesa acaba de firmar y marca la tesis ejecutada antes de que exista el trade · 6 flujos usan `confirm()`/`prompt()` nativos que chocan con el sistema de modales propio (incluido el motivo de rechazo del CIO).

**Accesibilidad:** cero `<label for>` asociados en los formularios · checklists de sesión sin estado ARIA · el toast (único canal de errores) sin `aria-live` · botones ✎/✕ sin nombre accesible · tap targets de 24–30px · `app.html` sin `prefers-reduced-motion` (el dot de sesión pulsa infinito) · la landing pierde toda la navegación en móvil sin menú alternativo · la celda "hoy" del calendario pierde el anillo ámbar de violación (colisión de `box-shadow`).

---

## Plan de corrección sugerido (por lotes)

1. **Lote móvil** (A1–A4): 4 media queries + `min-width:0`. Máximo impacto, riesgo cero en desktop.
2. **Lote contraste/semántica** (B1–B3): 2 cambios de token + 1 clase + reemplazos rgba. Mecánico.
3. **Lote robustez** (C1–C2): `inert` + atributos ARIA + gestión de foco (~25 líneas).
4. **Lote sistema tipográfico** (D1–D7): consolidación de tokens — el más largo, sin riesgo funcional.
5. **Lote UX fino** (adicionales): banner de gestión, semana UTC, ejecución de tesis → journal prellenado, reemplazar `confirm/prompt` por los modales propios.
