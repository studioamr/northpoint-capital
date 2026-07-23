# SPEC — La Travesía del Marinero (rediseño 3D de index.html)

Concepto: la landing entera es UNA escena WebGL continua — un mar nocturno vivo — que se recorre
con el scroll. El marinero es el trader. La estrella polar es NORTHPOINT (behavioral intelligence).
Cada sección de la página es una etapa de su travesía hasta llegar al fondo. El contenido del
handbook (caps 01, 02, 04, 05, 06) vive en paneles liquid-glass superpuestos a la escena.

El sistema de diseño de `DESIGN.md` sigue vigente (tokens, tipografía, glass, español, cero AI-slop).
El mar y el cielo usan la misma paleta: azul polar --accent como única luz fría, nada neón.

## Arco narrativo (scroll top → bottom)

### E0 · LA NOCHE — Hero
Cielo estrellado dominante, mar en calma abajo, horizonte al centro-bajo. LA estrella polar brilla
distinta a las demás (más grande, pulso lento, reflejo vertical sobre el agua).
Texto: NORTHPOINT / BEHAVIORAL INTELLIGENCE + «The market doesn't defeat traders. Their behavior does.»
CTAs: "Solicitar acceso inversor" · "Entrar al Terminal →". Indicador de scroll ("Zarpar ↓" o línea animada).

### E1 · EL ZARPE — Filosofía (cap 01)
La cámara baja hacia el agua; aparece el velero (low-poly elegante, farol encendido) navegando en
mar tranquilo. Copy puente: "Todo marinero zarpa buscando retornos. Pocos entienden que el enemigo
viaja a bordo." Paneles glass: MISIÓN · VISIÓN · los 6 pilares (P—01…P—06) · "Lo que Northpoint no es".

### E2 · LA TRIPULACIÓN — Estructura (cap 02)
Mar abierto, oleaje medio; la cámara orbita levemente el bote. Copy puente: "Nadie cruza un océano
solo. Cada puesto a bordo existe por una razón." Paneles: los 6 roles NP-001…NP-050 como "la
tripulación", el proceso de decisión en 5 pasos (la carta de navegación), y los 3 vehículos
(Alpha / Macro / Quant) como rutas.

### E3 · LA TORMENTA — Código de Conducta (cap 04)
El mar se encrespa: olas grandes, cielo cerrado (las estrellas se ocultan), relámpagos tenues a lo
lejos, el bote cabecea. Copy puente: "El mar no hunde barcos. La conducta del que lo navega, sí."
Paneles: 4 valores no negociables (los mástiles), 6 estándares profesionales, y la card ámbar de
TERMINACIÓN INMEDIATA ("por la borda: sin apelación").

### E4 · LA ESTRELLA — Tecnología & Score (cap 05)
Las nubes se abren; la estrella polar reaparece enorme y su reflejo forma un camino de luz sobre el
agua que el bote sigue; el mar se va calmando. Copy puente: "En la noche más cerrada, el marinero no
sigue su instinto. Sigue la estrella." Paneles: NORTHPOINT SCORE (0–1000, 4 dimensiones — la estrella
tiene 4 puntas: Risk Discipline · Emotion Control · Decision Quality · Consistency), stack tecnológico
condensado, protocolos de seguridad.

### E5 · EL PUERTO — Plan Snowball (cap 06) + cierre
En el horizonte aparece el faro/silueta del puerto NORTHPOINT (luz cálida única en toda la página,
muy contenida); el mar queda en calma total, amanecer apenas insinuado en el horizonte. Copy puente:
"La travesía no termina al llegar. El capital, como la nieve, crece rodando." Paneles: principio
Snowball (3 columnas), niveles Seed/Core/Summit (Core recomendado), la curva de proyección a 20 años,
onboarding en 6 pasos, AVISO LEGAL completo en letra pequeña.
Footer sobre el agua en calma: northpoint.io · investors@northpoint.io · © 2025 · confidencial ·
"Terminal de traders →".

## Reglas de la experiencia
- UNA sola escena Three.js persistente (canvas fixed); el scroll NO mueve el DOM 3D: mueve la cámara,
  el estado del mar (amplitud/frecuencia de olas), el cielo (nubes/estrellas) y el bote. Contenido HTML
  en un layer superpuesto con scroll normal (los paneles glass entran con reveal sutil).
- Progreso de scroll 0–1 → timeline maestra por etapas con interpolación suave (damping/lerp);
  cada etapa define: posición/target de cámara, altura de ola, densidad de nubes, intensidad de estrella,
  visibilidad de faro. Transiciones de etapa con crossfade de estados (nunca cortes).
- Liquid glass: los paneles de contenido refractan/difuminan la escena real de atrás (backdrop-filter
  blur+saturate; borde especular; opcional filtro SVG de desplazamiento sutil en hovers). El nav es glass.
- El bote SIEMPRE flota físicamente: su Y/pitch/roll se muestrean de la MISMA función de olas del shader.
- Performance: correr fluido en laptop normal — malla de agua razonable, sin sombras dinámicas caras,
  pixel ratio cap 2, pausar render si la pestaña no es visible. prefers-reduced-motion → escena estática
  con paneles normales.
- Mobile (<900px): misma escena simplificada (menos subdivisiones, sin relámpagos), paneles a 1 columna.
- Fallback sin WebGL: fondo estático con gradiente + estrellas CSS; el contenido completo siempre accesible.
- Todo el contenido textual del handbook se CONSERVA (viene del index.html v1 ya construido — reusar su
  copy). El SEO/accesibilidad no se sacrifica: HTML semántico real, la escena es decorativa.

## Técnica (completar con hallazgos de la investigación northpoint-3d-research)
- Three.js por CDN (versión según investigación), GSAP ScrollTrigger + Lenis si la investigación lo
  respalda como estándar actual; si no, scroll nativo + damping manual.
- Océano: Gerstner/sum-of-sines en vertex shader con parámetros animables (amplitud por etapa).
- Cielo: dome con gradiente + Points para estrellas (twinkle), sprite/glow para la polar, nubes como
  planos con noise o fog denso por etapa.
- Faro: geometría simple + luz puntual cálida de baja intensidad + haz fake (cono translúcido).
