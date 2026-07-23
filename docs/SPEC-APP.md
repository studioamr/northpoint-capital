# SPEC — app.html (NORTHPOINT TERMINAL — plataforma del trader)

Archivo único autocontenido: `/Users/andremacouzet/claude/northpoint/app.html`.
Vanilla HTML+CSS+JS, sin frameworks, persistencia en localStorage (clave raíz `np_terminal_v1`).
Sigue `docs/DESIGN.md`. Fuente de lógica: `docs/handbook.txt` — sobre todo el CAPÍTULO 03
(Reglas & Protocolos): la plataforma ES ese capítulo convertido en software. Es una HERRAMIENTA:
densa, precisa, sin scroll-reveal, sin marketing. El trader abre esto cada mañana a las 7:00am.

`<title>NORTHPOINT TERMINAL</title>`

## Estado (localStorage, JSON bajo `np_terminal_v1`)
```js
{
  trader: { nombre, cuenta: 25000, creado },   // cuenta = tamaño de cuenta USD, editable
  trades: [ { id, fecha:'YYYY-MM-DD', hora:'HH:MM', instrumento, direccion:'LONG|SHORT',
              resultado:  numero USD (+/-), r: numero (múltiplo R),
              setup: {targets:bool, liquidez:bool, estructura:bool, entrada:bool},
              emocion:'CALMA|FOMO|REVENGE|ANSIEDAD|DUDA', nota, screenshot(url opcional) } ],
  checklists: { 'YYYY-MM-DD': [bool x6] },     // pre-market del día
  reportes: { 'YYYY-MM-DD': true },            // días con reporte enviado/copiado
  estudio: { lecciones: {id:true}, quizzes: {moduloId: score} }
}
```
Si no hay trader → pantalla de alta centrada (glass card): logo, "NORTHPOINT TERMINAL",
inputs nombre + tamaño de cuenta (default $25,000), botón "Iniciar operación". Sin backend, todo local.

## Shell
- Sidebar izquierda fija 220px (glass, borde derecho --line-soft): logo arriba; nav vertical:
  DASHBOARD · SESIÓN · JOURNAL · PROGRAMA · REGLAS; abajo: nombre del trader, cuenta en mono,
  y micro "CONFIDENCIAL · v1.0". En <900px la sidebar se vuelve barra inferior fija con iconos+labels 10px.
- Header fino: título de la vista + fecha de hoy en mono + RELOJ EN VIVO (HH:MM:SS, mono) con
  badge de estado de la VENTANA DE OPERACIÓN según hora local:
  - antes de 7:00 → "PRE-MARKET" (--dim)
  - 7:00–8:30 → "VENTANA ABIERTA" (--up)
  - después de 8:30 → "FUERA DE VENTANA — no se opera" (--warn)
- SPA por vistas: mostrar/ocultar secciones con JS, hash routing (#dashboard, #sesion, #journal, #programa, #reglas).

## Vista 1 — DASHBOARD
Fila de 4 stat-cards (número grande mono):
  P&L acumulado (verde/rojo según signo) · Win rate % · Trades totales · Racha de días documentados.
**NORTHPOINT SCORE** — card protagonista: número 0–1000 grande + anillo SVG de progreso (trazo --accent 3px)
y 4 barras de dimensiones (0–250 c/u): Risk Discipline, Emotion Control, Decision Quality, Consistency.
Cálculo (determinista, desde datos; si hay <3 trades mostrar "—" y "Opera y documenta para generar tu Score"):
  - Risk Discipline (250): empieza en 250; −40 por cada día con >2 trades; −30 por trade fuera de ventana
    (hora < 07:00 o > 08:30); −60 por trade en instrumento mini (contiene 'M' inicial tipo MNQ/MES/MYM/M2K).
    Piso 0.
  - Emotion Control (250): 250 × (1 − proporción de trades con emocion FOMO o REVENGE), −30 extra por
    cada trade #2 del día registrado tras una pérdida con setup incompleto (revenge estructural).
  - Decision Quality (250): 250 × proporción de trades con setup completo (4/4 checks) ; −10 por trade sin nota.
  - Consistency (250): 100 × (días con checklist pre-market completo / días operados)
    + 100 × (días con reporte / días operados) + 50 × min(1, racha_journal/10).
  Redondear todo; clamp 0–250 por dimensión.
**OBJETIVOS (VISIÓN cap 03)** — card con 5 filas de progreso, cifras del handbook escaladas a la cuenta del trader
(el handbook asume $250k; usar los PORCENTAJES: día 0.6% · semana 3% · quincena 6% · mes 12% · año 144%):
  Diario / Semanal / Quincenal / Mensual / Anual → barra de progreso: P&L del periodo actual vs objetivo
  (monto objetivo = cuenta × pct, mostrado en mono). Barra --accent; si se excede, cap al 100% + check.
**CURVA DE EQUITY** — SVG line chart del P&L acumulado por día (últimos 30 días con datos). Línea --accent 1.5px,
  área 8%, tooltip simple al hover (title o div). Si no hay datos: estado vacío elegante.
**MÉTRICAS DE RIESGO** — fila: Max drawdown (desde el pico de la curva, USD y %), Consistencia %
  (mejor día / P&L total ×100 — si >30% marcar en --warn con nota "un solo día domina tu curva"),
  Profit factor (suma ganancias / |suma pérdidas|), R promedio.

## Vista 2 — SESIÓN (el protocolo diario en vivo — corazón de la plataforma)
Tres bloques en columna, formato del cap 03:
**PRE-MARKET (7:00)** — checklist interactivo de 6 pasos (persistente por fecha):
  1 Tradingview abierto y revisión inicial de gráficos
  2 Calendario económico y fundamental del día
  3 Análisis overnight — liquidez Asia/Londres
  4 Estado de cuenta: situación y objetivos
  5 Proyecciones daily bias (NY open)
  6 Esperar open y ORB (7:30–7:45)
  Progreso "X/6" en mono. Al completar 6/6: línea "Protocolo pre-market completo." en --up.
**SETUP VÁLIDO — se cumplen TODAS; si falta una, NO HAY TRADE** — 4 toggles grandes:
  A Targets overnight sin tomar (Asia/Londres H/L, PDH/PDL)
  B El break apunta hacia liquidez clara
  C BOS / FVG de 5m · EMA 14/50 a favor
  D Entrada tantito antes o en el break — no FOMO
  Veredicto en vivo debajo: 4/4 → "SETUP VÁLIDO — ejecuta el plan" (--up, borde verde sutil);
  <4 → "SIN SETUP. El mejor trade del día es no operar." (--dim). Estos toggles precargan el checklist
  de setup del formulario de registro.
**ESTADO DE LA SESIÓN (gestión, cap 03)** — máquina de estados según trades de HOY:
  - 0 trades → "Sin operaciones. Máximo 2 trades, estricto."
  - 1 trade ganador → banner --up: "SE GANÓ EL TRADE 1 → SE CIERRA LA PLATAFORMA. Día terminado." (y el
    botón de registrar trade se desactiva con nota)
  - 1 trade perdedor → banner --warn: "Trade 1 perdido → UN SOLO intento más, ÚNICAMENTE con setup
    válido nuevo completo. Nunca revenge."
  - 2 trades → banner: "Límite de sesión alcanzado (2/2). Plataforma cerrada hasta mañana." (registro bloqueado)
**POST-MARKET** — 3 filas: Registrar los trades (link a #journal) · Verificar dashboard (link) ·
  REPORTE AL EQUIPO: botón "Generar reporte del día" → modal/inline con texto preformateado mono:
  ```
  NORTHPOINT · REPORTE DIARIO — {fecha}
  Trader: {nombre} · Cuenta: ${cuenta}
  Trades: {n} ({W}W/{L}L) · P&L día: {+/-$X} ({pct de la cuenta}%)
  Cumplimiento: {✓/✗ ventana} · {✓/✗ máx 2 trades} · {✓/✗ setup completo}
  Progreso mensual: ${acum}/{objetivo} ({pct}%)
  ```
  Botón "Copiar" (navigator.clipboard) — al copiar marca `reportes[hoy]=true` y muestra "Reporte copiado — pégalo en el canal del equipo."

## Vista 3 — JOURNAL (trade tracker)
**Formulario de registro** (card superior): fecha (default hoy), hora (default ahora), instrumento
  (select: NQ, ES, YM, RTY, GC, CL, + "Otro" con input) — si el usuario elige/escribe un micro (MNQ, MES, MYM, M2K…):
  BLOQUEO con mensaje --down: "NUNCA MINIS. Operación en minis está prohibida. Sin excepciones." (no se guarda);
  dirección LONG/SHORT (toggle); resultado USD (+/−); múltiplo R; checklist de setup 4 checks;
  emoción (chips: CALMA / DUDA / ANSIEDAD / FOMO / REVENGE); nota; URL de screenshot (opcional).
**Validaciones de regla al guardar** (además del bloqueo de minis):
  - hora fuera de 07:00–08:30 → se guarda PERO se marca flag "FUERA DE VENTANA" (chip --warn en la fila)
    y descuenta Score. Confirmación previa: "Estás registrando un trade fuera de la ventana 7:00–8:30."
  - tercer trade del mismo día → confirmación dura: "REGLA: 2 trades máximo, estricto." — permitir solo
    tras confirmar (queda flag "VIOLACIÓN 2-MAX" --down y golpea el Score). La plataforma registra la
    verdad, no la esconde.
  - setup incompleto → aviso: "Guardando trade SIN setup válido (X/4)."
**Tabla/lista de trades** (desc por fecha): fecha·hora mono, instrumento, dirección (chip L/S),
  resultado en mono verde/rojo, R, chips de flags (fuera de ventana / 2-max / sin setup / emoción si FOMO o REVENGE),
  nota truncada con expandir, botón borrar (confirm). Filtros simples: Todos · Este mes · Ganadores · Perdedores · Con violación.
**Resumen del periodo** arriba de la tabla: P&L, win rate, PF del filtro activo, en fila mono.

## Vista 4 — PROGRAMA (programa de estudio)
Micro-etiqueta: "DESARROLLO CONTINUO — Los mercados evolucionan. Quien no evoluciona, se queda atrás."
Barra de progreso global (lecciones completadas / total) + Score de quizzes.
6 módulos (acordeón de cards glass; cada lección = título + 3–6 párrafos REALES escritos desde el handbook
y conocimiento sólido de trading — NADA de placeholder — + botón "Marcar como estudiada"):
  M01 FILOSOFÍA NORTHPOINT — 3 lecciones: Behavioral intelligence (el mercado no te derrota, tu conducta sí) ·
      Los 6 pilares aplicados al trader · Lo que Northpoint no es (y por qué te protege).
  M02 ESTRUCTURA DE LA SESIÓN — 3 lecciones: El pre-market de 7:00 paso a paso · Calendario económico y
      liquidez overnight (Asia/Londres, PDH/PDL) · Daily bias y la apertura de NY.
  M03 EL SETUP — 4 lecciones: ORB 7:30–7:45 (la apertura y el rango) · Liquidez: hacia dónde apunta el break ·
      BOS y FVG de 5 minutos · EMA 14/50 y estructura; la entrada sin FOMO.
  M04 GESTIÓN Y RIESGO — 4 lecciones: 2 trades máximo (por qué existe la regla) · Ganaste el 1: cierras ·
      Perdiste el 1: un solo intento · Los no negociables (nunca minis, ventana, nada abierto después de 8:30).
  M05 PSICOLOGÍA CONDUCTUAL — 4 lecciones: Sesgos cognitivos del trader · FOMO y revenge: anatomía ·
      Gestión del ego (ningún trade es "tuyo") · La disciplina cuando es incómoda (principio rector).
  M06 POST-MARKET Y MEJORA CONTINUA — 3 lecciones: El journal como activo (el error documentado) ·
      Leer tu dashboard: consistencia, drawdown, Score · El reporte al equipo y la revisión semanal.
Cada módulo cierra con QUIZ de 3 preguntas (opción múltiple, radio buttons; al enviar: calificación X/3,
respuestas correctas marcadas; persistir mejor score). Preguntas sobre las reglas reales
(ej. "Ganaste el trade 1. ¿Qué sigue?" → "Se cierra la plataforma").
Al 100% de lecciones + quizzes ≥2/3: card final "PROTOCOLO INTERNALIZADO" con la cita del principio rector.

## Vista 5 — REGLAS (referencia rápida)
El capítulo 03 completo, bellamente tipografiado para consulta diaria:
  VISIÓN (tabla mono: Diario $1,500/0.6% · Semanal $7,500/3% · Quincenal $15,000/6% · Mensual $30,000/12% ·
  Anual $360,000 — nota: "cifras de referencia sobre cuenta de $250k; tu dashboard las escala a tu cuenta") ·
  PRE-MARKET (6) · SETUP VÁLIDO (4, con la advertencia "si falta una no hay trade") · GESTIÓN (2-max, win→cierra,
  lose→1 intento) · POST-MARKET (3) · NO NEGOCIABLES (4, card destacada borde --warn) ·
  PRINCIPIO RECTOR como quote de cierre: "Ninguna regla de Northpoint tiene 'excepción creativa'…
  La disciplina no se aplica cuando es cómodo. Se aplica siempre."
Además card compacta "CONDUCTAS DE TERMINACIÓN INMEDIATA" (cap 04, las 8) — el trader debe tenerlas presentes.

## Detalles de implementación
- Todo el JS en un solo <script> al final; funciones puras para el Score (testeables desde consola:
  exponer `window.__np = {state, save, score}` para debug).
- Formato dinero: Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).
- Fechas: siempre local (no UTC) — cuidado con toISOString; usar helper `hoy()` con getFullYear/getMonth/getDate.
- Sin imágenes externas. Sin librerías. Sin emojis (los ✓/✗ del reporte en texto están bien).
- El archivo será largo (~2000+ líneas): está bien. Completo > corto.
