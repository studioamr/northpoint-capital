# INFORME FINAL — AUDITORÍA DEL TERMINAL NORTHPOINT
**Archivo:** `/Users/andremacouzet/claude/northpoint/app.html` (~256KB, vanilla, esquema 4)
**Fecha:** 22-jul-2026 · **Base:** 78 aserciones de humo (78 PASA / 0 FALLA), 16 hallazgos confirmados contra refutador, 21 hallazgos refutados, un mes completo operado por los tres socios.

---

## 1 · VEREDICTO

El **motor de cálculo es correcto y está bien probado**: reglas del catálogo, piso congelado, colchón, proyección de la copiadora, violaciones y score pasan 78 de 78 aserciones. **El terminal no lo está.** La ruta principal de la app —registrar un trade— está rota: `#tSave` guarda el trade sin `t.accts` y el trade desaparece del journal, del calendario, del P&L, del score y de los balances; hoy la mesa no puede capturar una sola operación desde la UI. Encima de eso hay tres defectos que producen **números falsos sobre dinero real**: el plan y la fase de la cuenta son campos independientes (hito $52,000 en vez de $52,100, piso que nunca se congela), `reglasFondeadas()` lee el plan equivocado del catálogo, y el tope de consistencia se calcula sobre el objetivo fijo en vez del acumulado (95.8% real reportado como verde → payout rebotado por Tradeify).

La lógica está bien; **la captura, la validación de estado y la traducción a pantalla, no**. Y el mes cerró declarando 93.5% de la meta con **$0 al banco**.

---

## 2 · LO QUE ESTÁ BIEN (verificado ejecutando)

**Catálogo y reglas — `reglasDe()` [EJECUTADO, 13 aserciones]**
Select Evaluation 50k: target 3,000 · dailyLoss 0 · maxDD 2,000 · consistency 40% · minDays 3 · `lockAtProfit` null. Select Daily 50k: dailyLoss 1,000 · maxDD 2,000 · lockAtProfit 100 · target 0. Un plan fuera del catálogo devuelve `null`, nunca un número inventado. Las fases propias de André salen exactas: eval 1,000/1,000 · colchón 200/400 · retiros 100/200.

**Piso congelado y colchón — `saludDe()` [EJECUTADO, 7 aserciones]**
Con balance 52,100 el piso se congela en 50,100 y el colchón vale 2,000 (un drawdown completo por encima del piso). El hito de la fase colchón sale 52,100. Con balance 50,050 el piso todavía flota (pico − maxDD) y **no se descongela al perder**. En evaluación el piso nunca se congela. Esta es la parte más delicada del modelo y está bien.

**Copiadora — 1 decisión, N cuentas [EJECUTADO, 11 aserciones]**
Una orden replicada a 5 cuentas produce **una sola fila**, con P&L proyectado ×5 = 1,000 y `pnl1` = 200 conservado intacto. Con 2 cuentas seleccionadas, ×2 = 400. Con 1 cuenta, sin multiplicar. Una cuenta que no participó no ve el trade. `idsSel()` no cuela `__none` en modo custom. `capitalVista()` = 5 × 50k = 250,000.

**Motor de violaciones — `violations()` [EJECUTADO, 20 aserciones]**
MINIS dispara con MNQ/MES/MYM/M2K y no con NQ. FUERA DE VENTANA dispara a 06:59 y 08:31, **no** a 07:00 ni a 08:30 exactos (los bordes están bien). 3ER TRADE sólo en el tercero. OPERÓ TRAS GANAR sólo tras un trade 1 ganador. REVENGE excluye SIN SETUP (no se cuenta doble) y no dispara tras perder si el setup fue válido. Dos decisiones en 5 cuentas → 2 filas, ningún 3ER TRADE falso.

**Migración 3 → 4 [EJECUTADO, 7 aserciones]** — Sube el esquema, marca `["__none"]` a los trades sin cuentas, borra `profile.cuenta`, crea `accounts[]` y `ui.acctSel`, es idempotente y no pisa `accts` ya asignadas. Un guardado v3 real de localStorage migra limpio.

**Metas, sesión y score [EJECUTADO, 11 aserciones]** — `metas()` deriva de las cuentas y no de la meta declarada (5 en colchón → 2,000/día, 10,000/semana, 40,000/mes); una cuenta quemada no suma. `sessionState()` da pre/live/orb/off correctamente y cierra el fin de semana. `calMatrix` alinea el 1-jul-2026 (miércoles) en la 3ª casilla. `computeScore` da 1000 en día limpio y `null` sin trades, y castiga Risk/Decision/Consistency dejando Emotion limpia cuando no hay trade previo.

---

## 3 · DEFECTOS CONFIRMADOS (por severidad real)

### D1 · CRÍTICO — Todo trade registrado desde el modal nace sin `t.accts` y desaparece de la app para siempre [EJECUTADO]
**Dónde:** `app.html:3462-3483`, push en la 3478 (`S.trades.push({ id: uid(), ...data })`). El objeto `data` (3465-3476) no lleva `accts`. Candado de `migrar()` en 1997 (`if((s.schema||0) >= SCHEMA) return s;`).
**Qué falla:** el modal `#ovTrade` (1494) no tiene selector de cuentas y nadie más escribe `accts` (los únicos escritores son `migrar()` con schema<4, `borrarCuenta()` 2861 y `asignarHuerfanos()` 2870). Con `t.accts === undefined`, `nSel()` devuelve 0 y **todo el aparato lo descarta**: `tradesByDay()`, `pnlRanges()`, `computeScore()`, `saludDe()`, el calendario, el contador x/2, `gestionState()` y el CSV.
**Reproducción:** `S.trades.push({ id:uid(), date:hoy, time:'07:35', sym:'NQ', dir:'L', qty:1, pnl:1000, setupOk:true })` (copia literal del handler) → `t.accts = undefined` · balance T1 = 50000 (esperado 51000) · `pnlRanges` = `{dia:0,semana:0,quincena:0,mes:0,anio:0}` · `nSel` = 0 · `computeStats.pnl` = 1000 · `gestionState` = "Sin trades hoy" · `computeScore` = null. Tras `save()` + `load()`: `accts` sigue `undefined`, schema 4.
**Qué se ve mal:** el toast dice "Trade documentado", el journal sigue vacío, el calendario no pinta el día, el P&L no se mueve, el balance de las 5 cuentas sigue en $50,000 — **pero** "Trades registrados · win rate" del dashboard de firma sí lo cuenta (usa `S.trades` crudo), así que la misma pantalla muestra dos verdades opuestas. El rescate de huérfanos no lo ve: busca `accts.includes(SIN_CUENTA)`, que es `false` para `undefined`. El botón DEMO (4458) empuja trades igual de mancos.
**Arreglo:** (a) selector múltiple de cuentas en el modal y `S.trades.push({ id:uid(), accts: enVista.length ? enVista : [SIN_CUENTA], ...data })`; (b) red de seguridad fuera del early-return: mover `(s.trades||[]).forEach(t=>{ if(!Array.isArray(t.accts)||!t.accts.length) t.accts=[SIN_CUENTA]; })` ANTES de la línea 1997; (c) cambiar el filtro de huérfanos a `!Array.isArray(t.accts) || t.accts.includes(SIN_CUENTA)`; (d) arreglar el seed DEMO de la 4458.

### D2 · CRÍTICO — `Fase` y `Plan` son campos independientes: el piso nunca se congela y el terminal declara colchones completos que no existen [confirmado operando el mes; el refutador lo redujo a "falta validación", la operación demuestra el daño]
**Dónde:** gestor de cuentas, desplegables `Plan` (2802-2804) y `Fase` (2810-2812); consumido por `reglasDe()` 2053-2061 y `saludDe()` 2064-2083. El propio código tiene un comentario advirtiendo del riesgo (3252-3253) y aun así permite el estado.
**Qué falla:** pasar la cuenta a fase Colchón sin cambiar el plan a "Select Daily (fondeada)" deja `lockAtProfit` en `null`. El piso de drawdown **no se congela** ($50,430 flotante en vez de $50,100 fijo), el colchón se lee $2,000 en vez de $2,330 y el hito baja a $52,000 en vez de $52,100. La app tiene el dato (`p.phase`) para detectar la incoherencia y no lo usa.
**Qué se ve mal:** el terminal reportó que **T5 (balance $52,010) ya había completado su colchón**. Con el plan correcto le faltaban **$90**. Con ese dato en verde se pide un payout que Tradeify rebota. Además la columna "colchón" queda pegada en $2,000 en las cinco cuentas todo el mes —una constante disfrazada de métrica— y el reporte automático la imprimió cinco veces.
**Arreglo:** validar en el gestor: si `FASES[a.fase]` implica fondeada y `reglasDe(a).lockAtProfit == null`, pintar "PLAN Y FASE NO COINCIDEN" y bloquear el guardado; mejor aún, que cambiar Fase a buffer/payout proponga automáticamente el plan fondeado de la misma familia. Añadir "aplicar a todas las cuentas en vista".

### D3 · CRÍTICO — `violations()` no conoce el dinero: un día que mata la cuenta sale limpio y con 750/1000 PROFESIONAL [confirmado por CRO]
**Dónde:** `violations()` 2142-2158. `rDia` (riesgo de fase) y `dailyLoss` (límite de la firma) sólo se pintan como texto; nunca se comparan contra el P&L del día.
**Qué falla:** un día construido con **−$5,000** en una cuenta fondeada de 50k —25× el riesgo de fase de $200, 5× el `dailyLoss` de $1,000, balance $45,000 contra piso $48,000, colchón **−$3,000**, cuenta muerta— devuelve `[]` en ambos trades, `gestionState()` dice "2 trades — sesión completa" y `computeScore()` da **750/1000 PROFESIONAL**. Confirmado también en operación: el 23-jul se perdieron $210 en fase colchón (rDia $200) y no se marcó nada.
**Arreglo:** dos violaciones nuevas — `RIESGO DIARIO EXCEDIDO` (Σ pnl del día por cuenta < −rDia) y `LÍMITE DE LA FIRMA` (< −dailyLoss cuando dailyLoss > 0) — más una alerta dura, no una etiqueta, cuando `saludDe(a).colchon <= 0`.

### D4 · CRÍTICO — `violations()` cuenta filas, no decisiones: 8 de 15 violaciones de julio son falsas, 67 puntos de score [confirmado operando]
**Dónde:** `violations()` deriva 3ER TRADE / OPERÓ TRAS GANAR / REVENGE del **índice dentro del arreglo del día** que produce `tradesByDay()` (2162-2170), ya filtrado por el picker de cuentas.
**Qué falla:** al partir una decisión en dos órdenes (cuentas en fases distintas), el 17-jul salieron **4 filas de 2 decisiones** y el terminal marcó dos 3ER TRADE y un OPERÓ TRAS GANAR falsos. Filtrando a T1-T3 las mismas operaciones salen limpias: **la violación depende del selector de cuentas**. El Score cerró en 808 cuando agrupando por decisión da 875.
**Nota:** el refutador declaró este mecanismo "inalcanzable" porque hoy ningún camino de la UI produce `accts` heterogéneos — es cierto, y sólo porque D1 impide crear cualquier `accts`. En cuanto D1 se arregle (selector de cuentas por operación), esto es real el mismo día. La operación real del mes ya lo produjo.
**Arreglo:** `violations()` y los contadores x/2 deben calcularse **siempre** sobre `tradesByDay()` con TODAS las cuentas, agrupando por decisión (mismo `date`+`time`+`sym`+`dir`), y el picker debe afectar sólo la proyección de P&L.

### D5 · CRÍTICO — Tope de consistencia mal planteado y sin medidor en pantalla [confirmado por CIO y CRO]
**Dónde:** `FASES.eval.tope()` calcula 40% del **OBJETIVO** ($1,200 fijo). La regla de Tradeify es 40% del **ACUMULADO**.
**Qué falla:** el 7-jul iban en **56.1%** (mejor día $1,150 / acumulado $2,050) y la app no dijo nada porque $1,150 < $1,200. El 8-jul llegaron a **95.8%**. Con ese dato en verde se pide un payout que la firma rebota. Además **no existe medidor de consistencia en ninguna pantalla**: el terminal conoce la regla (consistency 0.40, minDays 3) y nunca compara el mejor día real contra el tope. T4/T5 cerraron evaluación en 37.4%, a 2.6 puntos de tronar, y se supo corriendo un script aparte.
**Arreglo:** `tope = 0.40 × Σpnl acumulado de la fase` (recalculado cada día), y una barra de consistencia permanente en el panel de la cuenta con el ratio actual y el color cambiando a partir de 35%.

### D6 · CRÍTICO — Dos pestañas abiertas = pérdida total de datos [EJECUTADO]
**Dónde:** `save()` 2018 y `let S = load()` 1995. No hay ningún `addEventListener('storage')` en todo el archivo.
**Qué falla:** cada pestaña carga `S` una sola vez y `save()` serializa el documento entero. Cualquier click que dispare `save()` en la pestaña vieja —marcar un check del pre-market, abrir un módulo, firmar en la mesa— reescribe localStorage con el `S` obsoleto y borra lo hecho en la otra.
**Reproducción:** dos instancias sobre el mismo localStorage: A registra 2 trades ("en disco hay 2"), B marca UN check del pre-market y guarda → "trades en disco: 0"; al recargar A, "trades: 0".
**Arreglo:** `addEventListener('storage', e=>{ if(e.key===LS){ S = load(); renderAll(); } })` y un contador `rev` en el estado: `save()` relee el raw y si su `rev` es mayor, recarga/fusiona en vez de pisar.

### D7 · CRÍTICO — Hay botón de respaldo pero ninguna forma de restaurarlo [EJECUTADO]
**Dónde:** `#btnBackup` 4430-4435. No existe `#btnRestore`, ni `<input type="file">`, ni `FileReader`, ni `readAsText` en todo el archivo (verificado por grep sobre el HTML completo).
**Qué falla:** el único mecanismo de recuperación del terminal es un callejón sin salida. Combinado con "Terminal en cero", el borrado del sitio en el navegador o D6, el socio tiene un archivo con todos sus trades y ninguna manera de meterlo de vuelta. El toast "Respaldo descargado" implica una restauración que no existe.
**Arreglo:** `<input type="file" accept="application/json">` que lea con FileReader, valide el JSON, lo pase por `load()`/`migrar()` y pida confirmación antes de reemplazar `S`.

### D8 · IMPORTANTE — `reglasFondeadas()` y `reglasEval()` devuelven el primer plan del catálogo, no el de la familia de la cuenta [EJECUTADO]
**Dónde:** `planDeFase` / `reglasFondeadas` / `reglasEval` 3254-3274, consumido por `renderProceso` 3305-3308.
**Qué falla:** `planDeFase(a,'funded', p => p.lockAtProfit != null)` recorre `Object.keys(FIRM_CATALOG[a.firm].plans)` y devuelve **siempre "Growth Sim Funded"**, sin mirar `a.plan`. El hito de la barra, en cambio, sale de `reglasDe(a)` — el plan verdadero. Con una cuenta "Select Daily (fondeada)" el paso dice `dailyLoss` $1,250 en vez de $1,000, consistency 35% en vez de 40%, minDays 5 en vez de 3.
**Reproducción:** cuenta Tradeify 100k, plan "Select Daily (fondeada)", fase buffer → `saludDe(a).hito = 102600` pero `reglasFondeadas(a).plan = 'Growth Sim Funded'` y `maxDD = 3500` (el real es 2500). El panel imprime "Retiros desde $103,600" y la barra de abajo "hito $102,600" — **$1,000 de error en la misma pantalla**. Con 150k Select Flex: $155,100 vs $154,600. Con Lightning Funded 100k el paso dice $103,600 cuando la zona real empieza en $104,100: le dice al operador que puede retirar $500 antes de tiempo. En 50k coincide de chiripa porque los cuatro planes fondeados comparten maxDD 2,000.
**Arreglo:** que `reglasFondeadas` prefiera el plan que la cuenta ya tiene y, sólo en evaluación, busque la fondeada de la MISMA familia:
```js
const reglasFondeadas = a => {
  const R = reglasDe(a);
  if(R && R.lockAtProfit != null) return { ...R, plan:a.plan };
  const fam = String(a.plan||'').split(' ')[0];
  return planDeFase(a,'funded',(p,n)=> p.lockAtProfit!=null && n.startsWith(fam))
      || planDeFase(a,'funded', p => p.lockAtProfit!=null);
};
```
Igual para `reglasEval` con `(p,n)=> p.sizes[a.size].target>0 && n.startsWith(fam)`. Además `PASOS[2].sub` usa `a.size` mientras el hito usa `a.start`: cambiar a `a.start + Rf.maxDD + Rf.lockAtProfit`.

### D9 · IMPORTANTE — Reiniciar la cuenta el día que se pasa la evaluación cuenta el P&L de ese día dos veces [EJECUTADO]
**Dónde:** `window.reiniciarCuenta` 2851-2855 (`a.start = a.size; a.desde = todayISO();`) contra el filtro `t.date >= a.desde` de `saludDe` 2068.
**Qué falla:** el reinicio marca `desde = hoy`, pero el filtro es `>=`, así que los trades de HOY que ya estaban registrados —justo los que hicieron tocar los $53,000— se vuelven a sumar sobre el nuevo start de $50,000. Es el camino normal: la cuenta se pasa y se reinicia el mismo día.
**Reproducción:** trades +1,500 (20-jul), +500 (21-jul) y +1,000 hoy → balance 53,000 → "Reiniciar balance" → **balance 51,000** en vez de 50,000, pico 51,000, colchón inflado en $1,000. En fase colchón (riesgo $200/día) son cinco días de trabajo inventados y el hito de 52,100 se ve $1,000 más cerca. Si el día del reinicio fue perdedor, la cuenta arranca por debajo de 50,000.
**Agravante operativo:** no hay campo de fecha en el reinicio. `a.desde` siempre es `todayISO()` de la máquina, así que capturar el reinicio con un día de retraso borra un día entero de trades del cálculo del colchón sin avisar.
**Arreglo:** `const hoyPnl = S.trades.filter(t=>t.date===todayISO() && (t.accts||[]).includes(a.id)).reduce((x,t)=>x+(t.pnl||0),0); a.start = a.size - hoyPnl; a.desde = todayISO();` — y añadir un campo de fecha editable. Mejor: `a.desdeTs = Date.now()` con `t.ts` por trade y filtro `t.date > a.desde || (t.date === a.desde && t.ts >= a.desdeTs)`.

### D10 · IMPORTANTE — `metas()` no tiene techo de fase: pide 6.7× lo máximo que la fase permite ganar, y la barra mide contra un blanco móvil [confirmado operando]
**Dónde:** `metas()` 2115-2129 (`dia × 5 / 10 / 20 / 240`).
**Qué falla:** 5 cuentas en evaluación → meta mes **$100,000**, cuando el techo matemático de la fase es 5 × target = **$15,000** y al tocarlo la cuenta reinicia. Y la meta se mueve sola con la fase: $100,000 el 2-jul (todas en eval), $52,000 el 15 (fases mixtas), $40,000 el 29 (todas en colchón), $24,000 el 31 (cuatro en retiros). **El dashboard cerró marcando 116.9% sobre $24,000 cuando contra los $30,000 declarados el avance real fue 93.5%.** El 1-jul mostró 3.9% de avance contra cien mil dólares que nadie prometió. Y con el filtro "Evaluaciones" y cero cuentas en evaluación, cae al fallback `declarada/20` y muestra "$0 de $30,000" cuando sí se ganó.
**Arreglo:** topar `metas()` contra `Σ (hito − balance)` de las cuentas en vista, mostrar SIEMPRE la meta declarada junto a la derivada (dos barras, no una), y anclar el % del dashboard a la declarada.

### D11 · IMPORTANTE — El KPI de MES suma P&L de evaluación que se borra al reiniciar la cuenta [confirmado operando]
**Dónde:** `pnlRanges()` 2210-2229 vs `saludDe()` 2064-2083.
**Qué falla:** el P&L del mes suma los $18,000 (Pablo) / $16,310 (André) ganados en fase de evaluación como si fueran saldo, cuando ese dinero **desapareció** al reiniciar las cuentas a 50,000. El P&L del mes y el dinero que de verdad quedó son cifras distintas y la app sólo muestra la primera. No existe registro de retiros ni de payouts: el terminal reporta +$28,865 y no hay dónde asentar que al banco entraron **$0**.
**Arreglo:** tres KPIs separados — *P&L bruto del mes* · *saldo vivo sobre el piso* (`Σ balance − Σ start`) · *retirado al banco* — más una tabla de retiros/payouts con fecha, cuenta y monto.

### D12 · IMPORTANTE — El Score halaga: sin mínimo de muestra, ventana de 30 filas y violaciones que valen 8 puntos [confirmado operando]
**Dónde:** `computeScore()`.
**Qué falla:** (a) con **UN solo trade** en el historial devuelve **1000 / INSTITUCIONAL**; (b) la ventana es "últimos 30 trades" y a dos trades diarios máximo eso es **mes y medio**: con 20 trades en julio nada envejece nunca; (c) el score subió de 847 a 865 en la semana 3, que fue la de peor disciplina, porque los tres trades sucios del 8-jul se salieron de la ventana; (d) el tercer trade fuera de ventana del 9-jul cuesta **8 puntos sobre 1000** (929 vs 937) y las 4 violaciones del mes juntas cuestan 46 (975 → 929). Al promediar sobre 30 decisiones, un evento que puede matar una cuenta pesa 1/27. Pablo cerró con **893 "INSTITUCIONAL" con cuatro banderas del mes** (MINIS, FUERA DE VENTANA, OPERÓ TRAS GANAR, REVENGE).
**Arreglo:** mínimo de muestra (n<10 → "MUESTRA INSUFICIENTE", no 1000); ventana por calendario (mes en curso), no por conteo de filas; y penalización **absoluta** por violación de riesgo (MINIS y FUERA DE VENTANA deben topar el grado, no promediarse).

### D13 · IMPORTANTE — `pnlRanges()` mezcla tres criterios de corte temporal y se ancla al reloj de la máquina [confirmado operando]
**Dónde:** `pnlRanges()` 2210-2229 (`quinStart = day<=15 ? 1 : 16`, filtro sólo `>= quinStart`).
**Qué falla:** `semana` **sí** filtra por `<= hoy`; `mes` y `quincena` **no**. Un trade con la fecha mal tecleada lo absorbe el mes en silencio: en el mes de Mateo entraron **6 trades futuros por +$6,250** de los +$22,250 reportados (mes real sin futuro: $16,000). Y todo se ancla a `Date.now()`: revisando el cierre del 31-jul, el tile "P&L HOY" marcaba −$1,050 (el resultado del 23) y "QUINCENA" +$10,050 por el corte del día 16. Los tiles día/semana/quincena son ruido al revisar un mes cerrado. Lo mismo con `buildReport()`, clavado a `todayISO()`: sólo existe el reporte de hoy, no se puede sacar el post-mortem del 8-jul.
**Arreglo:** recortar TODOS los rangos con `t.date <= iso`, cerrar la primera quincena con `día <= 15`, y añadir una **fecha de referencia** parametrizable que alimente `pnlRanges()`, `gestionState()` y `buildReport()` (por defecto hoy, editable desde el journal).

### D14 · IMPORTANTE — `gestionState()` felicita como "sesión completa" un día que violó la regla cardinal [EJECUTADO]
**Dónde:** `gestionState()` 2985, rama `dayTr.length >= 2`.
**Qué falla:** la rama final sólo mira la cantidad: con exactamente 2 trades devuelve `cls:'win'` y "2 trades — sesión completa", sin revisar el resultado del primero. Con t1(07:32, +800) y t2(08:00, −400) el banner sale verde mientras `violations(t2)` sí marca **OPERÓ TRAS GANAR** en la tabla. El operador recibe dos veredictos opuestos y el que ve primero, grande y en verde, es el equivocado.
**Arreglo:** que `gestionState()` consulte `dayTr.flatMap(t=>violations(t,dayTr))` y devuelva `cls:'stop'` siempre que haya cualquier violación. Banner y tabla no pueden contradecirse.

### D15 · IMPORTANTE — Empate de hora: el orden lo decide un id aleatorio y con él se pierde o se reasigna OPERÓ TRAS GANAR [EJECUTADO]
**Dónde:** `tradesByDay()` 2165 (`sort((a,b)=> (a.date+a.time+a.id).localeCompare(...))`) y `violations()` 2145/2153-2156.
**Qué falla:** `violations()` no compara horas, compara el índice del arreglo, y ese índice se desempata por `t.id` = `Math.random().toString(36)`. Con dos trades en el mismo `HH:MM` —normal en una ventana de 90 minutos— el orden real es aleatorio. Ejecutado: `[{id:'zzz',07:35,+500},{id:'aaa',07:35,−300}]` → orden aaa→zzz, **nadie recibe OPERÓ TRAS GANAR**, `gestionState` dice "sesión completa". Invirtiendo `S.trades` sale el mismo orden: el criterio real es el id. Es un veredicto silenciosamente al azar y estable entre renders, así que ni parpadea.
**Arreglo:** añadir `seq` (contador monotónico o `Date.now()`) en `#tSave` y ordenar `(a.date+a.time).localeCompare(b.date+b.time) || (a.seq||0)-(b.seq||0)`. Para lo ya guardado, desempatar por el índice original en `S.trades`. Alternativa: capturar segundos.

### D16 · IMPORTANTE — Los tres pasos del proceso y las "reglas de esta fase" salen sólo de `sel[0]` [EJECUTADO]
**Dónde:** `renderProceso` 3287-3291, 3305-3308, 3339-3355.
**Qué falla:** `mixta` se calcula sólo sobre `a.fase`, pero todos los textos numéricos se generan con `R0 = reglasDe(sel[0])`. Con una 50k y una 100k en la MISMA fase no se dispara el aviso y el panel presenta como únicas las cifras de la primera cuenta **por orden**. Cambiar el orden de las cuentas en el gestor cambia el riesgo diario declarado de **$1,000 a $1,500** y el objetivo de $1,000 a $2,000 sin tocar nada del plan. Es la cifra que gobierna cuánto arriesga el operador ese día.
**Arreglo:** `const clave = a => a.fase+'|'+a.plan+'|'+a.size; const homogenea = new Set(sel.map(clave)).size === 1;` y usar `homogenea` donde hoy se usa `!mixta`, en `#prSub`, `#prPasos` y `#prNota`; cuando no lo sea, callar el bloque numérico y decir "cada barra corre contra el hito de su cuenta".

### D17 · IMPORTANTE — El dashboard de firma cuenta trades y win rate sobre `S.trades` crudo [EJECUTADO]
**Dónde:** `renderFirma` 2306-2316 (`const allTr = S.trades;`), junto a `R` que sí viene de `pnlRanges()` con `idsSel()`.
**Qué falla:** en la misma tarjeta conviven un P&L filtrado por cuentas y un conteo/win-rate sin filtrar. Con la vista en una cuenta donde no cayó nada, el panel afirma **"2 trades · 100%"** mientras el P&L del año marca $0 y el journal sale vacío. Además es lo único que hace visibles los trades rotos de D1, lo que enmascara el problema real.
**Arreglo:** `const allTr = Object.values(tradesByDay()).flat();` (o usar `computeStats`, que ya calcula n y wr).

### D18 · IMPORTANTE — El CSV exporta el P&L proyectado sin decir sobre cuántas cuentas está [EJECUTADO]
**Dónde:** `#btnExport` 3486-3496 (la 3490 escribe `t.pnl` ya proyectado).
**Qué falla:** el mismo `northpoint-journal.csv`, sobre el mismo journal, da cifras distintas según cómo esté el selector al pulsar Exportar, sin ninguna columna que lo revele. Y la fila mezcla escalas: `qty` es de UNA orden (2 contratos) mientras `pnl` es el de N cuentas. Ejecutado: `...,NQ,LONG,2,100,105,1000,SI` con todas en vista vs `...,2,100,105,200,SI` con sólo T1. Quien concilie contra el estado de cuenta de Tradeify obtiene un P&L que no corresponde ni a una cuenta ni al fondo.
**Arreglo:** columna `cuentas` = `t.nAcc||1`, columna `pnl_por_cuenta` = `t.pnl1 ?? t.pnl`, y la selección en el nombre del archivo: `northpoint-journal-<etiquetaSel()>.csv`.

### D19 · IMPORTANTE — El ticket se marca EJECUTADA antes de que exista el trade, sin vínculo ni marcha atrás [no verificado ejecutando; leído en código]
**Dónde:** handler `[data-exec]` 4580-4590.
**Qué falla:** `t.estado='ejecutada'; save();` corre de inmediato y sólo después, con dos `setTimeout` encadenados, se abre el modal. Si el PM cancela con Escape, la mesa queda EJECUTADA para siempre — no hay botón para reabrir un ticket ejecutado. Y no se guarda referencia alguna (`t.tradeId` / `trade.tixId`), así que **no se puede contestar cuántos de los 27 trades del mes pasaron por las 4 firmas** sin cruzar fechas y símbolos a mano.
**Arreglo:** `pendienteTix = t.id` al abrir el modal, y en `#tSave` escribir `trade.tixId = pendienteTix` y recién ahí `t.estado='ejecutada'`. Botón de CIO para revertir a 'abierta'.

### D20 · IMPORTANTE — El modo inglés deja en español el 53% de lo que pinta el JS, incluida la señal central de la mesa [EJECUTADO]
**Dónde:** `violations()` 2119-2135, `gestionState()` 2979-2986, `renderJournal()` 3411, `renderFirma()` 2276-2340, `renderProceso()` 3277-3355, `renderSesion()` 2955-3030, `renderCalc()` 4318-4360, `renderPosiciones()` 4162-4220.
**Qué falla:** con `IDIOMA='en'` se renderizan 75 bloques y **40 (53%)** siguen conteniendo español. No es cosmético: es lo que dice si el trader rompió las reglas. La columna "Discipline" muestra MINIS, FUERA DE VENTANA, OPERÓ TRAS GANAR, SIN SETUP, 3ER TRADE, REVENGE; el banner dice "Trade 1 ganado → día terminado"; la nota de fase dice "riesgo máximo $1,000 por día"; el calendario dice "Faltan $99,950 para la meta del mes".
**Arreglo:** `violations()` debe devolver **códigos** (`MICROS`, `OUT_OF_WINDOW`, `THIRD_TRADE`, `AFTER_WIN`, `REVENGE`, `NO_SETUP`) y la vista traducirlos con `tr('vio.<code>')`; `gestionState()` devolver clave + números. Red: un test que corra los render en `'en'` y falle si el HTML hace match con `/\b(meta|día|días|cuenta|colchón|riesgo|pérdida|Sin|Faltan)\b/`.

### D21 · IMPORTANTE — La nube pega a una tabla que el instructivo no crea, y el pill miente igual [EJECUTADO]
**Dónde:** `app.html:4629` y `4641` (`/rest/v1/northpoint_estado`) vs `docs/CLOUD.md:13-20` (`create table ... cenit_estado`); `cloudPaint` 4616-4623.
**Qué falla:** siguiendo el doc al pie de la letra, todas las peticiones fallan con **404 (42P01, relation does not exist)**. Los dos `catch(e){}` de `cloudPush`/`cloudPull` se tragan el error y `cloudPaint` pinta **"NUBE · SINCRONIZADA"** con la sola condición de que `url` y `anon` no estén vacías. Los tres socios creerían estar viendo la misma mesa estando cada uno en su isla. (Residuo del renombrado; `cenit` sobrevive también en `docs/app-pre-firma.html:2160`.)
**Arreglo:** unificar el nombre de la tabla y hacer que el pill refleje la realidad: guardar `cloudErr`, comprobar `r.ok`, pintar "NUBE · ERROR (404) — ESTADO LOCAL" cuando el último intento falló o `cloudTs` lleva >30 s sin refrescarse. Antes de conectar, resolver también el last-write-wins sobre el documento completo (documentado y aceptado en `docs/CLOUD.md`, pero no aguanta 4 firmas en una ventana de 90 minutos) y sacar `profile`/`ui.acctSel` del payload compartido.

### D22 · MENOR — Un mes futuro se anuncia como "Mes cerrado" [EJECUTADO]
**Dónde:** `renderCal`, bloque del ritmo 3220-3235. `mesActual = calMes === hoyISO.slice(0,7)` y todo lo demás cae en la rama else. Con `calShift(1)` → "Agosto 2026" + "Mes cerrado. Sin operaciones registradas en este mes." Es la única línea del calendario que da lectura del plan y da la contraria.
**Arreglo:** separar pasado de futuro con `calMes.localeCompare(hoyISO.slice(0,7))` y añadir la rama "Mes por venir. Meta de $X repartida en N días hábiles."

### D23 · MENOR — `nextRebalance()` con trimestres cableados
Trimestres fijos (abr/jul/oct/ene) y una variable `q` sin usar; estando en julio se salta julio y devuelve 1-oct-2026. Además cuenta los días desde el reloj real de la máquina, no desde la fecha del informe.

---

## 4 · LO QUE SE DESCARTÓ (no volver a levantar)

1. **Piso no congelado con plan de evaluación en fase fondeada** — los números salen, pero el plan ES la fuente de verdad y la app no miente sobre él; el defecto real es la falta de validación → recogido en **D2**.
2. **Cambiar el tamaño de la cuenta no mueve `a.start`** — desplazamiento constante de etiqueta; la barra marca HITO exactamente cuando el trader ganó el target real (probado a +5,999 → falso, +6,000 → verdadero). Residuo de una línea (`a.start = a.size` al cambiar tamaño).
3. **"P&L de 5 cuentas contra meta de 3"** — el 66% depende de un plan fuera del catálogo inalcanzable por la UI (18/18 combinaciones plan×talla devuelven reglas válidas). El residuo alcanzable es 25% con una cuenta pausada.
4. **Colchón negativo sin alerta** — sí hay alerta: fila en rojo, ordenada al tope de la tabla, `−$500` en gestor, reporte y `aria-live`. El estado 'quemada' es manual por diseño.
5. **"Asignar a todas" multiplica ×5 los balances** — `saludDe` suma `t.pnl` en crudo (50,000 → 50,600, no ×5); los huérfanos son anteriores a `a.desde` y ni entran.
6. **Cuenta pausada infla la barra** — el mismo desajuste lo produce cualquier cambio de fase (20%→100%); es la definición de `metas()` como run-rate, no un bug. Cubierto por **D10**.
7. **Quincena incluye todo el mes en la primera mitad** — sólo alcanzable con fecha futura, y ahí el panel entero ya es basura. Cubierto por **D13**.
8. **El picker altera violaciones y score** — inalcanzable hoy porque `accts` es siempre homogéneo (5 estados del picker → score 563 idéntico). **Latente**: se vuelve real al arreglar D1 → recogido en **D4**.
9. **La ventana usa la hora local del navegador** — `VENTANA` está en el reloj local por diseño (7:30 Morelia = 9:30 ET = apertura real); `violations()` compara una hora tecleada a mano y es invariante a TZ (md5 del estado idéntico en 3 zonas). Residuo real: el horario de verano de NY corre las constantes una hora de nov a mar.
10. **`esHabil()` sin feriados** (reportado 3 veces) — 3 consumidores, todos cosméticos en `renderCal`; el caso estrella (3-jul) es día operable en CME; residuo real: 4 días al año, ~5%, dentro de un mes nominal de 20 días que ya aproxima 15%.
11. **"DÍAS OPERADOS" puede pasar del 100%** — exige 23/23 días hábiles perfectos más un fin de semana; el demo salta findes explícitamente.
12. **`save()` sin try/catch por cuota** — la prueba sustituye `setItem` por un throw incondicional; con cuota real de 5MB el primer fallo llega en **2047** (10,934 trades). Y como `save()` va antes de `closeOv()`, el modal se queda abierto: el usuario no cree que guardó.
13. **JSON corrupto en localStorage → terminal vacío** — `setItem` es atómico por spec; la app nunca puede escribir un raw inválido; el caso `null` toma la misma ruta con el mismo resultado.
14. **La semilla `'{}'` de CLOUD.md borra el terminal** — vive en `cenit_estado`, tabla que el código nunca consulta; y `cloudOn()` es false. Lo real es el desajuste de nombre → **D21**.
15. **La nube es last-write-wins y borra firmas** / **carrera pull-vs-save** / **el pull comparte `profile` y `ui`** — las tres corren contra `app_cloud.html`, una copia del scratchpad con la línea 4613 parcheada. En el archivo real `CLOUD = {url:'',anon:''}` y las 26 versiones del historial de git también. Anotado como riesgo de diseño **para cuando se conecte** → **D21**.
16. **"Terminal en cero" borra el terminal de los tres socios** — cero peticiones a Supabase, verificado con espía en `fetch`. Residuo: `#btnWipe` no llama `lockUI()` (menor; "Cerrar sesión" está en el mismo panel).
17. **La mesa revienta con una firma de usuario fuera de USERS** — `firmas[gk]` sólo se escribe con `S.session.user`, validado contra USERS en `doLogin`; y con `session.user` adulterado el arranque llama `lockUI()`. Requiere devtools.
18. **El CSV pierde trades / `\r` parte la fila** — `accts` es homogéneo (CSV byte a byte idéntico en los 3 modos) y `<textarea>.value` normaliza CRLF a LF por spec. Lo válido → **D18**.
19. **`calMes` no se reinicia al volver al Journal** — cada cifra declara su alcance (`#calTitulo` dice "Junio 2026"); existe el botón HOY; misma convención que `jRange`.
20. **i18n: confirm() en español, botón de idioma inalcanzable en login, 33 claves huérfanas, botones de modal sin `data-i18n`, iniciales del calendario, tarjetas del bootcamp** — seis reportes distintos de la misma condición: el modo EN cubre 138 claves / 35 nodos sobre ~347 literales españoles. Consolidado en **D20**. Las claves `tit.*` sí se usan (lookup dinámico) y `c.guardar` no cubre "Guardar trade".
21. **`const tr` sombrea `tr()` en `renderCal`** — no hay ninguna llamada a `tr(` en las líneas 3163-3196; el auditor tuvo que inyectarla con python3. Renombrar a `dayTrades` es pulido, no corrección.

---

## 5 · FRICCIÓN DE USO (mes operado)

**A · Transición de fase — la que más tiempo costó**
Pasar de fase requiere DOS desplegables (Fase y Plan) sin validación cruzada (D2), más "Reiniciar balance" sin campo de fecha (D9), **cinco veces, una por cuenta**. Con la copiadora replicando la misma orden a 5 cuentas idénticas, las 5 pasan el mismo día siempre. → *Acción sobre la selección ("aplicar a todas las cuentas en vista") + aviso automático cuando `saludDe().hito` se alcanza: el terminal ya sabe que la cuenta llegó a 53,000 y no avisa, no propone y no marca.*

**B · Métricas que no informan o informan mal**
"Colchón $2,000" es constante mientras el piso flota: el 22-jul con balance $50,400 dice $2,000 y el 31-jul con $51,450 dice $2,000. El dato útil —cuánto falta para el hito de $52,100— la app lo calcula y lo entierra, y el reporte diario imprimió "colchón $2,000" cinco veces sin el faltante. "Límite diario de la firma: sin límite" (dailyLoss 0 en Select Evaluation) es peligrosamente malinterpretable: el tope real es el drawdown de $2,000. → *Mostrar `falta al hito` como métrica primaria y sustituir "sin límite" por "sin límite diario de la firma — tu freno es el drawdown de $2,000".*

**C · La copiadora es ciega a sus propios fallos**
El trade del 2-jul tocó **4 de 5 cuentas** y valió $2,400 en vez de $3,000; el journal muestra una sola fila sin indicar cuántas cuentas participaron. Hubo que filtrar T5 sola para descubrirlo. Dos días con 3 de 5 cuentas costaron **$2,030 por cuenta y 6 días hábiles de retraso**, detectados leyendo balances a mano. → *Columna "N cuentas" en el journal (el dato `t.nAcc` ya existe en `proy()`) y alerta cuando `t.accts.length < cuentasVivas().length`.*

**D · Disciplina sin gobierno**
No se puede anotar ni apelar una violación: el MINIS del 22-jul fue un error de mapeo de la copiadora, no una decisión de mesa, y se queda en el Score para siempre sin contexto. Las violaciones son forenses, no preventivas, y no tienen pantalla propia: el día infractor es un puntito en el calendario y sacar el conteo del mes por tipo exigió recorrer `tradesByDay()` a mano. No existe registro de "hoy no se opera": los días 1, 3, 10, 14, 21 y 30 simplemente no aparecen, y la decisión de no operar es la mitad del trabajo del CIO. → *Campo `nota`/`apelacion` por violación con firma del CRO; vista "Violaciones del mes" agregada por tipo; entrada "día sin operar" con motivo.*

**E · Gobierno corporativo**
Las "4 firmas" son 3 personas con doble voto: Mateo cubre NP-030 (research) y NP-020 (riesgo) —dos de las cuatro puertas él solo— y Pablo firma NP-001 (CIO) y además es el único con NP-010, el rol que marca "Ejecutada". **Aprueba y ejecuta la misma persona** y la app no lo advierte. → *Bloquear que un mismo `session.user` cubra dos de las cuatro firmas del mismo ticket, y separar quien firma CIO de quien ejecuta.*

**F · Snowball desconectado**
Los dos clientes siguieron en $300,000 suscritos = $300,000 de valor todo el mes porque no hay puente con el P&L de la mesa. `nivelDe(300000)` promete CORE 15–22% sin ninguna cifra real detrás. No hay serie de tiempo ni fecha de valuación: el "retorno acumulado 3.5%" promedia una posición de 11 días con otra del mes completo — no es TWR ni está anualizado. → *Valuación fechada por posición, TWR y puente al P&L realizado del fondo antes de mostrar cualquier nivel de retorno prometido.*

---

## 6 · EL MES SIMULADO EN NÚMEROS

**No da.** Contra el plan de **$30,000 al mes**, esto es lo que pasó:

| Concepto | Cifra |
|---|---|
| P&L bruto del mes proyectado (5 cuentas) | **$28,050 – $28,865** (93.5% – 96.2% de la meta declarada) |
| P&L de fase de evaluación borrado al reiniciar a $50,000 | **−$18,000** (Pablo) / **−$16,310** (André) |
| Saldo vivo real sobre el piso, 31-jul | **$10,050 – $11,320** (Pablo, planes corregidos) · **$10,815** (André) |
| Retiros ejecutados en julio | **0** |
| **Dinero que entró al banco** | **$0** |

**De dónde sale la diferencia.** Los ~$28,000 que el dashboard llama "P&L del mes" son P&L **bruto de plataforma**, no patrimonio. Al aprobar cada evaluación la cuenta reinicia a $50,000 y **todo lo ganado en esa fase se evapora contablemente**: $18,000 de los $28,050 de Pablo, $16,310 de los $28,865 de André. Lo que sobrevivió es el colchón sobre el piso de $50,100 — entre $10,050 y $11,320 — y **nada de eso es retirable todavía**: T1-T4 completaron colchón el 29-jul y T5 se quedó a **$90** del hito (el terminal decía que ya lo había completado, D2). Medido en dinero real, el avance contra los $30,000 fue de **~34-38%**, no 93.5%.

**El 116.9% es un espejismo triple.** (1) La meta derivada bajó sola de $100,000 (2-jul, todas en eval) a $24,000 (31-jul, cuatro en retiros): la barra midió contra un blanco móvil que se encoge a medida que la mesa progresa (D10). (2) El numerador incluye P&L de evaluación ya borrado (D11). (3) En el mes de Mateo el numerador incluía además **$6,250 de 6 trades con fecha futura** que `pnlRanges().mes` no recorta (D13): el mes real era $16,000, no $22,250.

**Contra el techo matemático de las fases** (Mateo): $25,500 posibles (eval 5×$3,000 = $15,000 + colchón $10,500), realizados $22,250 = **87.3%**. Esa es la única lectura de eficiencia que tiene sentido, y no está en ninguna pantalla.

**Disciplina.** 27 decisiones, 20-21 días operados, win rate 55.6%–71.4%, PF 1.95–4.05. Violaciones marcadas 15, **reales 7, falsas 8** (todas por contar filas en vez de decisiones, D4). Score final 808 (real 875) y 893/929 "INSTITUCIONAL" en las otras dos corridas **con cuatro banderas del mes encima**. El día de prueba catastrófico (−$5,000, cuenta muerta, colchón −$3,000) salió con **cero violaciones y 750 PROFESIONAL** (D3). El score no es una medida de disciplina hoy; es un adorno.

**Consistencia.** Peor ratio real alcanzado **95.8%** contra un tope de 40%, con la app en verde porque compara $1,150 contra $1,200 fijos (D5). Cierre final 36.4%–37.4%, a 2.6 puntos de tronar la evaluación, y ese número lo calcularon los socios fuera de la app.

---

## 7 · QUÉ ARREGLAR PRIMERO

**1 · `#tSave` debe escribir `t.accts` + selector de cuentas en el modal + saneo en `load()` fuera del candado de esquema (D1).**
Criterio: es el único defecto que hace el terminal **inutilizable**. Hoy no se puede registrar un solo trade desde la UI; todo lo demás se audita sobre datos que la app no puede producir. Nada más importa hasta que esto esté. Al arreglarlo se activa D4 (violaciones por fila), así que van juntos.

**2 · Validar `Plan` × `Fase` y arreglar `reglasFondeadas`/`reglasEval` por familia de plan (D2 + D8).**
Criterio: es el único bloque que produce **cifras falsas sobre dinero que la firma va a auditar**. Ya causó que el terminal declarara completo un colchón al que le faltaban $90, y en cuentas de 100k son $1,000 de error en el umbral de retiro. Un payout rebotado cuesta semanas.

**3 · `violations()` por decisión y con dinero: agrupar órdenes de una misma decisión + `RIESGO DIARIO EXCEDIDO` + `LÍMITE DE LA FIRMA` + alerta dura con `colchon <= 0`; `gestionState()` derivado de `violations()` (D4 + D3 + D14 + D15).**
Criterio: la disciplina es el producto. Hoy 8 de 15 banderas son falsas (67 pts de score) y un día que mata la cuenta sale limpio con 750 PROFESIONAL. Un motor de disciplina que no distingue un día perfecto de una cuenta muerta no sirve para nada, y el banner verde contradice la tabla roja en la misma pantalla.

**4 · Consistencia sobre el acumulado + medidor permanente (D5) y meta topada al techo de fase con la declarada siempre visible (D10 + D11).**
Criterio: son los dos números que el operador mira para decidir si pide un payout y si va bien. Hoy uno estuvo en 95.8% pintado de verde y el otro cerró en 116.9% sobre una meta que se encogió sola mientras el banco recibía $0. Separar *P&L bruto* / *saldo vivo sobre el piso* / *retirado* es media hora de trabajo y cambia toda la lectura del mes.

**5 · Integridad del estado: listener de `storage` + `rev` en `save()` (D6) e importar respaldo (D7).**
Criterio: va al final sólo porque no afecta la corrección de las cifras — pero es el que puede borrar el mes entero. Dos pestañas abiertas destruyen el trabajo sin aviso y el único respaldo que existe no se puede volver a cargar. Es la red bajo los cuatro puntos anteriores; en cuanto se toque `#tSave` y el gestor de cuentas, el riesgo de perder datos sube.

*Después de estos cinco, en este orden:* D9 (doble conteo del reinicio), D13 (cortes temporales y fecha de referencia para `buildReport`), D16/D17/D18 (`sel[0]`, dashboard crudo, CSV), D12 (score: mínimo de muestra y ventana por calendario), D19 (ticket↔trade), D21 (nombre de tabla y pill de la nube antes de conectarla), D20 (i18n de las etiquetas de violación), D22/D23.