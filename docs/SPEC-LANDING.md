# SPEC — index.html (Landing institucional NORTHPOINT)

Archivo único autocontenido: `/Users/andremacouzet/claude/northpoint/index.html`.
Vanilla HTML+CSS+JS, sin frameworks. Sigue `docs/DESIGN.md` al pie de la letra.
Fuente de contenido: `docs/handbook.txt` (capítulos 01, 02, 04, 05, 06 + portada + cierre).
La landing es la cara EXTERNA del fondo: filosofía, estructura, conducta, tecnología y el plan
de inversión Snowball. Lo operativo del trader (cap 03) NO va aquí — vive en `app.html` (el Terminal).

`<title>NORTHPOINT — Behavioral Intelligence</title>`

## Nav (fija, glass)
Logo (estrella polar SVG + NORTHPOINT / micro "BEHAVIORAL INTELLIGENCE").
Links ancla: Filosofía · Estructura · Conducta · Tecnología · Snowball.
Botón derecha (borde 1px --line, glass): "Trader Terminal →" → href `app.html`.
En mobile el nav colapsa a logo + botón Terminal (los anchors se ocultan; no hace falta hamburguesa).

## 1. Hero (100vh aprox)
- Micro-etiqueta: "HEDGE FUND OPERATIONS · INTERNAL DOCUMENT · v1.0 · 2025"
- Display: "NORTHPOINT" y debajo, en --accent apagado o --dim, "BEHAVIORAL INTELLIGENCE"
- Quote grande (22–26px, Inter 400, --txt): «The market doesn't defeat traders. Their behavior does.»
- Sub (15px --dim): "Inteligencia conductual aplicada a los mercados financieros. Donde otros ven ruido, nosotros vemos patrón."
- CTAs: primario glass claro "Solicitar acceso inversor" (mailto:investors@northpoint.io) · secundario texto "Entrar al Terminal →" (app.html)
- Detalle inferior: fila mono 12px con "6 CAPÍTULOS · CONFIDENCIAL · NORTHPOINT.IO" y una línea fina.
- Fondo del hero: la retícula/estrella polar en SVG gigante, trazo finísimo casi invisible (opacity .05), NO animada o con drift muy lento.

## 2. Filosofía (cap 01)
- Dos columnas MISIÓN / VISIÓN (texto literal del handbook).
- Grid 6 pilares (cards glass): P—01 Precisión sobre volumen … P—06 Mejora continua de procesos, cada uno con su texto del handbook. El código "P — 0X" en mono --accent.
- Bloque "LO QUE NORTHPOINT NO ES": 4 filas con — inicial: no HFT / no asesoría masiva / no rendimientos garantizados / no intuición, con sus subtextos.
- Quote separadora centrada: «La reputación no se declara. Se construye con datos.»

## 3. Estructura (cap 02)
- Grid de 6 cards de liderazgo: NP-001 CIO, NP-010 Portfolio Manager, NP-020 Chief Risk Officer, NP-030 Research Analyst, NP-040 Quantitative Analyst, NP-050 COO. Código NP-0XX en mono --accent, "Reports to X" como micro-etiqueta, y las responsabilidades resumidas en 2–3 líneas (del handbook).
- "PROCESO DE TOMA DE DECISIONES": timeline horizontal (vertical en mobile) de 5 pasos: 01 Generación de idea → 02 Research & validación (mín. 72h) → 03 Revisión de riesgo → 04 Aprobación CIO → 05 Ejecución documentada. Números en mono.
- "VEHÍCULOS DE INVERSIÓN": 3 cards — Alpha Fund (Long/Short Equity · Principal · Mín. $250,000), Macro (Global Macro · Secundaria · Mín. $500,000), Quant (Systematic · Emergente · Mín. $1,000,000). Cifras en mono.

## 4. Código de Conducta (cap 04)
- 4 valores no negociables (Integridad, Transparencia, Responsabilidad, Excelencia sin arrogancia) con sus textos.
- 6 estándares profesionales como lista de dos columnas (Puntualidad, Comunicación precisa, Feedback directo, Gestión del ego, Discreción absoluta, Desarrollo continuo) — título + 1 línea.
- Card de borde ámbar sutil (border-left 2px --warn): "TERMINACIÓN INMEDIATA" con las 8 conductas en lista compacta mono 13px.
- Quote: «Al unirte a Northpoint, aceptas estos estándares sin reservas. No son aspiracionales. Son el piso mínimo.»

## 5. Tecnología (cap 05)
- Intro del NORTHPOINT SCORE: card ancha destacada — "Sistema propietario de evaluación conductual 0–1000" con las 4 dimensiones (Risk Discipline, Emotion Control, Decision Quality, Consistency) como 4 mini-gauges o barras estáticas decorativas (valores fijos ej. 232/250) y una línea: "Los traders del fondo operan con su Score en vivo dentro del Terminal." + link "Ver el Terminal →".
- Grid del stack (6 categorías del handbook: Datos de Mercado, Ejecución & Brokerage, Research & Analytics, Gestión de Portafolio, Operaciones & Compliance, Comunicación & Seguridad) con sus herramientas en mono 12.5px --dim.
- Lista de 6 protocolos de seguridad digital (2FA hardware, VPN, dispositivos personales prohibidos, bloqueo 2 min, WiFi pública prohibida, backup encriptado) — filas finas con separador.

## 6. Plan Snowball (cap 06)
- Intro: principio Snowball (Reinversión total · Horizonte mínimo 3 años · Reequilibrio trimestral) — 3 columnas.
- 3 cards de niveles: Seed $50,000 (12–18% obj.) / Core $250,000 con badge "RECOMENDADO" en --accent (15–22%) / Summit $1,000,000 (18–28%), cada una con sus bullets del handbook. Core ligeramente elevada (glass-2, borde --accent-deep al 40%).
- PROYECCIÓN: gráfica SVG inline (600×260 aprox, responsive) de la curva compuesta $250k al 19% anual, 20 años, eje con marcas Año 5 ~$599k · Año 10 ~$1.43M · Año 15 ~$3.44M · Año 20 ~$8.25M. Línea --accent 1.5px, área con gradiente vertical al 8%, puntos en los 4 hitos con label mono. Dibujarla con path calculado a mano o generado por JS al cargar (250000*1.19^t).
- Onboarding: 6 pasos numerados (Calificación → Perfilamiento 60 min → Propuesta formal → Due diligence mutuo / Data Room → Suscripción y transferencia → Onboarding y primer reporte).
- AVISO LEGAL: párrafo completo del handbook en 12px --faint, borde superior fino.

## Footer
Logo pequeño, "northpoint.io · investors@northpoint.io", "© 2025 Northpoint Behavioral Intelligence. Todos los derechos reservados.", "Documento confidencial. Distribución restringida a personal autorizado." y link discreto "Terminal de traders →".

## JS
Solo: scroll-reveal (IntersectionObserver), dibujo de la curva Snowball, smooth scroll de anchors, y contador sutil opcional en hero. Nada de librerías.
