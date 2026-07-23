# CHAT DE MESA · NORTHPOINT CAPITAL MANAGEMENT
### Julio 2026 — Pablo (CIO+PM) · Mateo (CRO+Research) · André (Quant+COO)

---

## SEMANA 1 · 1 al 3 de julio

**[MIÉ 1 JUL · 06:41] André:** Ya quedaron las 5 Tradeify de 50k en el gestor. `capitalVista()` = $250,000. Las cinco en EVALUACIÓN desde hoy.

**[MIÉ 1 JUL · 06:42] André:** Catálogo verificado de Select Evaluation 50k: objetivo $3,000, drawdown $2,000, consistencia 40%, mínimo 3 días. Hito de evaluación: $53,000.

**[MIÉ 1 JUL · 06:44] Mateo:** Y el tope de consistencia entonces son $1,200 por día. 40% de $3,000. Nadie hace los tres mil en un día o se cae la evaluación aunque el balance llegue.

**[MIÉ 1 JUL · 06:45] Pablo:** Anotado. Ventana 07:30 a 08:30, dos balas, si gana la primera se cierra la plataforma.

**[MIÉ 1 JUL · 06:52] André:** Pablo, antes de abrir. La app tiene dos metas y no se hablan. La que tú escribiste en el perfil son $30,000. La que `metas()` deriva de las cuentas dice día $5,000, semana $25,000, **mes $100,000**.

**[MIÉ 1 JUL · 06:53] Pablo:** ¿Cien mil?

**[MIÉ 1 JUL · 06:53] André:** Cien mil. Cinco cuentas por $1,000/día por 20 días. Y el KPI del dashboard usa esa, no la tuya.

**[MIÉ 1 JUL · 06:54] Mateo:** Es peor de lo que suena. El techo matemático de la fase es 5 × $3,000 = $15,000, y al tocarlo la cuenta REINICIA. La app te está pidiendo 6.7 veces lo máximo que la fase permite ganar.

**[MIÉ 1 JUL · 06:55] Pablo:** Ok. La barra del mes no la miramos. La meta es $30,000, la que acordamos.

**[MIÉ 1 JUL · 07:38] Pablo:** ORB alcista. Largo NQ, 2 contratos. Ejecutado.

**[MIÉ 1 JUL · 08:04] Pablo:** Cerrado. +$780 por cuenta. Registrado en el journal.

**[MIÉ 1 JUL · 08:05] André:** +$3,900 proyectado. `gestionState()` dice lo correcto: "Trade 1 ganado → día terminado".

**[MIÉ 1 JUL · 08:05] Pablo:** Plataforma cerrada. Nos vemos mañana.

**[MIÉ 1 JUL · 08:11] André:** Una regla de captura y no la vuelvo a repetir: **`t.pnl` es el P&L de UNA cuenta, siempre.** El que pegue un agregado en el journal me rompe todos los balances del mes y no hay forma de auditarlo hacia atrás.

**[JUE 2 JUL · 07:33] Pablo:** Primer intento fuera. −$620.

**[JUE 2 JUL · 07:51] Pablo:** BOS de 5m, setup nuevo y válido. Segundo. +$900.

**[JUE 2 JUL · 08:02] Mateo:** Ese es el patrón bueno. Stop limpio y setup nuevo, no reentrada dolida. Día +$280 por cuenta.

**[JUE 2 JUL · 08:03] André:** +$1,400 proyectado. Acumulado +$5,300. T1 en $51,060, las cinco iguales.

**[JUE 2 JUL · 18:20] André:** Ojo con mañana. `esHabil('2026-07-03')` devuelve **true**. El 4 de julio cae sábado, el feriado se observa el viernes y el CME está cerrado.

**[JUE 2 JUL · 18:21] Mateo:** O sea que el terminal cuenta 23 días hábiles en julio y en la realidad son 22.

**[JUE 2 JUL · 18:22] André:** Y el 3 va a aparecer para siempre en el calendario como día hábil sin operar. Como día que fallamos.

**[VIE 3 JUL · 09:10] Pablo:** Mercado cerrado. Nada que hacer.

**[VIE 3 JUL · 19:02] André:** Cierre de semana: +$5,300. Northpoint Score: **1000/1000 · INSTITUCIONAL**.

**[VIE 3 JUL · 19:04] André:** Y ese mil es basura, lo digo yo que construí el Score. Lo probé aislado: **un solo trade limpio y `computeScore()` da 1000**. No hay mínimo de muestra. La semana 1 no demostró nada y el terminal nos puso corona.

**[VIE 3 JUL · 19:09] Pablo:** Lo tomo como que no significa nada hasta que tengamos 20 decisiones.

---

## SEMANA 2 · 6 al 10 de julio

**[LUN 6 JUL · 07:02] Mateo:** Subí la tesis a la mesa: NQ largo, ORB, mientras el VIX siga bajo 16 y no haya CPI dentro de la ventana. Firmo research (NP-030) y riesgo (NP-020).

**[LUN 6 JUL · 07:11] André:** Firmada validación cuantitativa (NP-040). Van 3 de 4.

**[LUN 6 JUL · 07:14] Pablo:** Firmo CIO (NP-001). 4/4. Le doy a "Ejecutada — registrar en Journal".

**[LUN 6 JUL · 08:22] Pablo:** Salió mal. −$540 por cuenta.

**[LUN 6 JUL · 08:23] André:** −$2,700 proyectado. Las cinco en $50,520.

**[MAR 7 JUL · 07:44] Pablo:** Ese sí. +$1,150 por cuenta. Se para.

**[MAR 7 JUL · 08:10] André:** Ahí hay algo. El terminal me registró `accts` con 3 ids, no 5. Proyectado +$3,450, no +$5,750.

**[MAR 7 JUL · 08:11] Pablo:** ¿Y no avisó nada?

**[MAR 7 JUL · 08:12] André:** Nada. Ni badge, ni nota, ni advertencia. La app sabe cuántas cuentas hay vivas y en cuántas cayó el trade, y no las compara.

**[MIÉ 8 JUL · 07:41] Pablo:** +$410. Primera ganada.

**[MIÉ 8 JUL · 07:58] Pablo:** Le metí otra. +$290.

**[MIÉ 8 JUL · 08:20] Pablo:** Y una tercera en ES. −$680.

**[MIÉ 8 JUL · 08:21] Mateo:** Pablo. Ganaste la primera. Ahí se acababa el día.

**[MIÉ 8 JUL · 08:34] André:** El terminal marcó lo correcto:
```
#2 NQ 07:58 → OPERÓ TRAS GANAR
#3 ES 08:20 → 3ER TRADE + OPERÓ TRAS GANAR + SIN SETUP
```

**[MIÉ 8 JUL · 08:36] André:** Y esto es lo peligroso: el día cerró en **+$20 por cuenta**. En dinero fue positivo. Tres violaciones y el journal se ve verde.

**[MIÉ 8 JUL · 08:40] André:** Lo registré con el checklist incompleto tal cual estaba. Si lo rellenamos a posteriori, la dimensión Consistency del Score se vuelve decoración.

**[MIÉ 8 JUL · 09:02] Mateo:** Congelo el tamaño en 2 contratos hasta que termine la evaluación. Y André, necesito que la copiadora rechace órdenes con timestamp después de las 08:30. La app no lo puede impedir, nada más lo etiqueta después.

**[MIÉ 8 JUL · 09:05] Mateo:** Eso me molesta del terminal, por cierto. `violations()` corre sobre trades YA registrados. Es forense, no preventivo. Y no hay una vista de "violaciones del mes" en ningún lado — el día 8 aparece con un puntito en el calendario y ya. Tuve que recorrer `tradesByDay()` a mano.

**[MIÉ 8 JUL · 19:40] André:** Score al cierre: **847 · PROFESIONAL**. Bajó 153 puntos por un solo día.

**[JUE 9 JUL · 07:26] Mateo:** Checklist no da setup en ninguna de las tres condiciones. No se opera.

**[JUE 9 JUL · 07:27] Pablo:** De acuerdo. Mesa cerrada.

**[JUE 9 JUL · 07:31] Pablo:** Y esto me da coraje: el 9 simplemente no va a existir. No hay forma de registrar "hoy decidimos no operar". La mitad de mi chamba como CIO es decir que no, y el terminal no guarda esa decisión en ningún lado.

**[JUE 9 JUL · 07:33] André:** Es el mejor día del mes y no aparece en ninguna métrica. Correcto.

**[VIE 10 JUL · 07:52] Pablo:** +$880 por cuenta, se para.

**[VIE 10 JUL · 08:40] André:** Me puse a leer los balances cuenta por cuenta en el gestor. Tenemos un problema serio.

**[VIE 10 JUL · 08:41] André:**
```
T1 $52,570   T2 $52,570   T3 $52,570
T4 $50,540   T5 $50,540
```

**[VIE 10 JUL · 08:42] André:** La copiadora se cayó el 7 y hoy. Las dos órdenes entraron en T1-T3 y no en T4-T5. +$1,150 y +$880 por cuenta. **$2,030 que T4 y T5 nunca vieron.**

**[VIE 10 JUL · 08:44] Pablo:** ¿Y nos enteramos hasta hoy?

**[VIE 10 JUL · 08:44] André:** Hasta hoy, y porque me puse a leer. Nada me avisó. Si no me siento a revisar, el 14 me sorprenden por atrás.

**[VIE 10 JUL · 08:46] Mateo:** El 6 de julio las cinco estaban en $50,520 exactos. Hoy hay una brecha de dos mil dólares abierta por infraestructura, no por trading.

**[VIE 10 JUL · 08:51] Pablo:** André, mapeo y perfiles de la copiadora se revisan **todos los lunes a las 6:50** y lo reportas aquí antes de la campana. No lo negocio.

---

## SEMANA 3 · 13 al 17 de julio

**[LUN 13 JUL · 06:52] André:** Copiadora revisada, cinco cuentas enganchadas.

**[LUN 13 JUL · 07:05] Mateo:** Subí tesis ES corto a la mesa por si acaso.

**[LUN 13 JUL · 07:19] André:** Firmo quant. 1/4.

**[LUN 13 JUL · 08:41] Pablo:** No firmo el ES. La ventana ya cerró. Con las cuatro firmas fuera de tiempo no hay orden, aunque el ticket se vea bonito en verde.

**[LUN 13 JUL · 08:42] Mateo:** De acuerdo. Se queda EN MESA.

**[LUN 13 JUL · 08:45] André:** Día −$60 por cuenta con la tesis vieja. −$300 proyectado.

**[MAR 14 JUL · 07:35] Pablo:** +$1,200 por cuenta. Se para ahí.

**[MAR 14 JUL · 07:50] André:** +$6,000 proyectado. **T1, T2 y T3 en $53,710 contra el hito de $53,000. Pasaron evaluación.**

**[MAR 14 JUL · 07:51] Pablo:** Eso.

**[MAR 14 JUL · 07:58] André:** Antes de festejar: ocho días operados, ganancia $3,710 por cuenta, mejor día $1,200. Eso es **32.3%** del total contra un tope de 40%. Pasamos con espacio.

**[MAR 14 JUL · 07:59] Mateo:** ¿De dónde sacaste el 32.3%?

**[MAR 14 JUL · 08:00] André:** De mi script. **El terminal no calcula consistencia en ningún lado.** El catálogo tiene el campo (`consistency: 0.40`), `FASES.eval.tope` sabe que son $1,200, y no existe una pantalla que te diga "tu mejor día es el X% de tu ganancia".

**[MAR 14 JUL · 08:03] Mateo:** Es la regla que más gente truena en fondeadoras y la app la guarda como dato muerto. Eso debería ser mi pantalla de CRO y no está.

**[MAR 14 JUL · 08:07] Pablo:** Y hay algo peor en cómo está planteado el tope. `FASES.eval.tope()` calcula 40% del **objetivo** = $1,200 fijo. La regla de Tradeify es 40% del **acumulado**. Mientras vas abajo del objetivo, ese $1,200 no te protege de nada.

**[MIÉ 15 JUL · 06:58] André:** Metí T1-T3 a fase colchón en el gestor. Reinician a $50,000.

**[MIÉ 15 JUL · 07:12] André:** Algo no cuadra. El panel me dice hito del colchón **$52,000** y piso $48,000 sin congelar. Y a quince centímetros, el panel "Proceso" dice "Retiros desde **$52,100**".

**[MIÉ 15 JUL · 07:14] Mateo:** ¿Dos números para el mismo hito en la misma pantalla?

**[MIÉ 15 JUL · 07:15] André:** Dame un rato.

**[MIÉ 15 JUL · 07:52] André:** Ya. Cambiar de fase son **dos desplegables, no uno**. `Fase` y `Plan`. Yo cambié Fase a "Colchón" y dejé Plan en "Select Evaluation". Y `saludDe()` lee las reglas del **plan**, no de la fase.

**[MIÉ 15 JUL · 07:53] André:**
```
plan sin corregir              plan corregido a Select Daily
hito colchón   $52,000         $52,100
piso T1        $50,525 flota   $50,100 CONGELADO
colchón T1     $2,000          $2,425
```

**[MIÉ 15 JUL · 07:55] André:** Select Evaluation tiene `lockAtProfit: null`. Sin piso congelado, el colchón es `balance − (pico − 2,000)`, o sea **exactamente $2,000 siempre** mientras vayas ganando. La columna que más miramos era una constante disfrazada de métrica.

**[MIÉ 15 JUL · 07:57] Pablo:** ¿Y nadie avisa?

**[MIÉ 15 JUL · 07:58] André:** El código tiene un comentario que advierte de esto con todas sus letras: "leer sus umbrales del plan de evaluación daría 52,000 en vez de 52,100". Alguien ya lo sabía. Y aun así te deja cambiar una cosa sin la otra sin un solo aviso. Cuarenta minutos me costó.

**[MIÉ 15 JUL · 08:05] Mateo:** Y ya que estamos auditando el catálogo, encontré otra. `reglasFondeadas()` y `reglasEval()` devuelven el **primer** plan del catálogo con esa fase, no el de la familia del plan de la cuenta.

**[MIÉ 15 JUL · 08:06] Mateo:** Con una cuenta Select Daily, `reglasDe()` da bien $1,000 / $2,000. Pero `reglasFondeadas()`, que es el que alimenta el panel de proceso, te trae **Growth Sim Funded**: dailyLoss $1,250, consistencia 35%, mínimo 5 días. Y `reglasEval()` trae Growth Evaluation: consistencia 0%, 1 día mínimo.

**[MIÉ 15 JUL · 08:08] Mateo:** En 50k nos salva de chiripa que el maxDD coincide. En 100k no: el hito real de Select Daily es $102,600 y el panel mostraría $103,600. Mil dólares de error. Si me guío por esa pantalla en vez del catálogo, reprobamos por consistencia sin verla venir.

**[MIÉ 15 JUL · 08:30] Pablo:** Mesa partida entonces. T1-T3 en colchón con riesgo $200/día, T4-T5 en evaluación con $1,000.

**[MIÉ 15 JUL · 08:31] André:** Y una orden no puede servir a las dos. El modelo guarda un solo `pnl` por trade, así que para operar dos tamaños hay que registrar **dos filas de la misma decisión**. Hoy: 1 decisión, 2 filas. +$1,820 proyectado.

**[JUE 16 JUL · 08:20] André:** +$2,360. T1 $50,640, T5 $52,810.

**[JUE 16 JUL · 16:40] Mateo:** Voy a parar la mesa mañana. Con `lockAtProfit: 100` en cuanto la fondeada gane $100 el piso salta a 50,100 y nos quedamos con cien dólares de aire. Es insostenible.

**[JUE 16 JUL · 16:52] André:** El terminal te dice colchón $1,800, no $100. Léelo otra vez.

**[JUE 16 JUL · 17:20] Mateo:** Ya fui a `saludDe()`. La app tiene razón y yo no. El piso **trailea** con el pico y sólo se **topa** en 50,100 — la condición es `pico − 2,000 ≥ 50,100`. Es un techo del piso a favor nuestro, no un salto en contra.

**[JUE 16 JUL · 17:22] Mateo:** Lo dejo escrito porque casi meto una decisión de riesgo basada en una regla que entendí al revés.

**[JUE 16 JUL · 17:24] Pablo:** Se agradece que lo escribas.

**[VIE 17 JUL · 08:12] Pablo:** Segunda decisión del día, dos filas otra vez.

**[VIE 17 JUL · 08:40] André:** Pablo, mira lo que dice el terminal con "todas las cuentas" seleccionadas:
```
#1 07:36 → limpio
#2 07:36 → limpio
#3 08:12 → 3ER TRADE
#4 08:12 → 3ER TRADE + OPERÓ TRAS GANAR
```

**[VIE 17 JUL · 08:41] Pablo:** Pero fueron dos trades.

**[VIE 17 JUL · 08:42] André:** Fueron dos. Filtré a T1-T3 solitas y las mismas operaciones salen **limpias**. `violations()` cuenta **filas del día**, no **decisiones**. La violación depende de qué cuentas tengas seleccionadas en el picker.

**[VIE 17 JUL · 08:44] Mateo:** O sea que el invariante se cae justo cuando la mesa se parte. Que es lo normal en cuanto una cuenta avanza de fase antes que otra.

**[VIE 17 JUL · 08:45] Pablo:** Día +$40 por cuenta en el grupo de colchón. +$340 proyectado.

**[VIE 17 JUL · 19:30] André:** Score al cierre: **865 · INSTITUCIONAL**.

**[VIE 17 JUL · 19:31] André:** Subió 18 puntos. En la peor semana de disciplina del mes. Porque los tres trades sucios del 8 de julio se salieron de la ventana de 30 filas.

**[VIE 17 JUL · 19:33] Pablo:** No mames.

**[VIE 17 JUL · 19:35] André:** A partir de hoy el Score no se reporta solo. Va siempre con el conteo crudo de violaciones reales al lado. Una métrica que sube cuando la disciplina baja no sirve para vigilar disciplina.

---

## SEMANA 4 · 20 al 24 de julio

**[LUN 20 JUL · 06:51] André:** Copiadora revisada. Cinco enganchadas.

**[LUN 20 JUL · 08:15] André:** **T4 y T5 pasaron evaluación.** $53,210 contra $53,000. Diez días operados, ganancia $3,210, mejor día $1,200.

**[LUN 20 JUL · 08:17] André:** Eso es **37.4%**. A **2.6 puntos porcentuales** de reprobar la regla del 40% y quedarnos con dos cuentas muertas después de tres semanas.

**[LUN 20 JUL · 08:18] Mateo:** ¿Y nadie se enteró de que estuvimos así de cerca?

**[LUN 20 JUL · 08:18] André:** Nadie. Porque el terminal no lo muestra. Es el número que más me sacudió del mes.

**[LUN 20 JUL · 08:24] André:** Y para que quede: la brecha que abrió la copiadora el 7 y el 10 nos costó **seis días hábiles**. T1-T3 pasaron el 14, T4-T5 hasta hoy.

**[LUN 20 JUL · 09:10] Pablo:** Paso las cinco a colchón. Fase, plan a Select Daily, reiniciar balance. Cinco veces, cuenta por cuenta.

**[LUN 20 JUL · 09:22] Pablo:** No hay "aplicar a todas". Con una copiadora que replica la misma orden a cinco cuentas idénticas, las cinco cambian de fase el mismo día siempre. Debería ser una acción sobre la selección.

**[LUN 20 JUL · 09:24] Mateo:** Y otra: `reiniciarCuenta()` hace `a.start = a.size; a.desde = todayISO()`. Siempre hoy. Si la firma nos aprueba un lunes en la tarde y nos sentamos el miércoles, no hay forma de decirle "esto reinició el 21".

**[LUN 20 JUL · 09:26] Mateo:** Y como `saludDe()` sólo cuenta trades con `t.date >= a.desde`, la fecha del reinicio define el balance completo de la cuenta. Un campo de fecha, nada más.

**[MAR 21 JUL · 07:12] Mateo:** Subí tesis MNQ largo. Volumen bajo, quiero tamaño chico.

**[MAR 21 JUL · 07:16] Pablo:** Rechazada. Micros prohibidos por handbook. No se discute.

**[MAR 21 JUL · 07:44] André:** Se ejecutó MNQ.

**[MAR 21 JUL · 07:45] Pablo:** ¿Perdón?

**[MAR 21 JUL · 07:46] André:** Plantilla vieja en el perfil de la copiadora. El terminal lo cachó bien: `#1 MNQ 07:44 → MINIS`. −$190 por cuenta, −$950 proyectado. MNQ vale $2/punto contra los $20 de NQ y sí está en la lista MICROS.

**[MAR 21 JUL · 07:52] André:** Y aquí hay algo de compliance que me incomoda como COO: el ticket de MNQ está **rechazado** en la mesa y la orden de MNQ **se ejecutó**, el mismo día. El terminal tiene los dos hechos y no los conecta.

**[MAR 21 JUL · 07:54] André:** De hecho no puedo contestar la pregunta más básica: **¿cuántos de nuestros trades pasaron por la mesa?** El botón dice "Ejecutada — registrar en Journal" pero el trade que se registra no guarda de qué ticket vino. Cruzo fechas y símbolos a mano.

**[MAR 21 JUL · 08:30] Pablo:** La bandera de MINIS se queda. Aunque no haya sido decisión de mesa.

**[MAR 21 JUL · 08:32] Pablo:** Pero necesito poder anotarla. Dentro de seis meses, cuando revise el histórico, quiero distinguir "operamos micros" de "la copiadora mandó micros". Un campo de motivo, aunque no cambie el Score.

**[MIÉ 22 JUL · 08:14] Pablo:** +$380 por cuenta. +$1,900. Se para.

**[JUE 23 JUL · 07:41] Pablo:** Stop. −$210.

**[JUE 23 JUL · 08:42] Pablo:** Entré largo. +$190.

**[JUE 23 JUL · 08:43] Mateo:** Son las 08:42, Pablo. La ventana cerró hace doce minutos.

**[JUE 23 JUL · 08:44] André:** `FUERA DE VENTANA + REVENGE`. Día −$20 por cuenta.

**[JUE 23 JUL · 08:47] André:** Ese +$190 lo reporto como pérdida operativa aunque el P&L diga positivo. Y pido que el 23 cuente como día roto en el journal.

**[JUE 23 JUL · 08:49] Pablo:** No estoy de acuerdo. El día cerró casi plano.

**[JUE 23 JUL · 08:50] Mateo:** Yo sí estoy de acuerdo con André. El mercado te pagó por romper la regla, que es lo peor que puede pasar.

**[JUE 23 JUL · 08:52] Pablo:** Lo escribo yo entonces, porque fui yo el que apretó el botón. Y desde agosto la plataforma se cierra a las 8:30 en duro. Si me la hubiera cerrado, el 23 no existiría.

**[JUE 23 JUL · 09:30] André:** Quise sacar el reporte de mesa del **8 de julio** para el post-mortem y no se puede. `buildReport()` está clavado a `todayISO()`. Sólo existe el reporte de HOY.

**[JUE 23 JUL · 09:31] André:** Igual `pnlRanges()`. DÍA, SEMANA y QUINCENA anclados al reloj real de la máquina. No hay forma de pararse en el 10 de julio y ver la semana 2 como la vio la mesa ese día. Para auditar hacia atrás, esto es medio terminal nada más.

**[JUE 23 JUL · 09:40] Mateo:** Peor: los rangos no usan el mismo criterio entre sí. `semana` filtra por `<= hoy`, `mes` y `quincena` no. Si alguien teclea mal una fecha y registra un trade del mes que entra, el mes lo absorbe en silencio y la semana no. Eso es un agujero de auditoría.

**[VIE 24 JUL · 08:20] Pablo:** +$450 por cuenta. +$2,250. Acumulado +$23,230.

**[VIE 24 JUL · 19:15] André:** Score: **823 · PROFESIONAL**.

---

## SEMANA 5 · 27 al 31 de julio

**[LUN 27 JUL · 06:50] André:** Copiadora limpia. Cinco cuentas, NQ, 2 contratos.

**[LUN 27 JUL · 08:02] Pablo:** +$420 por cuenta. +$2,100. Se para.

**[MAR 28 JUL · 07:55] Pablo:** +$330. +$1,650.

**[MAR 28 JUL · 08:10] André:** **T1, T2 y T3 en $52,230.** Cruzaron el hito de $52,100. Colchón completo. Las paso a fase retiros.

**[MAR 28 JUL · 08:12] Pablo:** Primera vez en el mes que veo un número que sí es nuestro.

**[MAR 28 JUL · 08:20] André:** Y mesa partida otra vez: tres cuentas con riesgo $100/día y dos con $200. Volvemos a dos filas por decisión el resto de la semana.

**[MIÉ 29 JUL · 08:30] André:** +$1,120. 2 filas, 1 decisión.

**[JUE 30 JUL · 08:25] André:** −$625.

**[JUE 30 JUL · 18:40] Mateo:** Les quiero enseñar algo. Construí un día a propósito para ver si el terminal nos protege.

**[JUE 30 JUL · 18:41] Mateo:** Cuenta fondeada de 50k. Dos trades dentro de ventana, con setup marcado, símbolo permitido, sin tercer trade. P&L del día: **−$5,000**.

**[JUE 30 JUL · 18:42] Mateo:** Eso son 25 veces el riesgo diario de la fase colchón, 5 veces el límite de la firma, y deja el balance en $45,000 contra un piso de $48,000. **Colchón −$3,000. La cuenta está muerta.**

**[JUE 30 JUL · 18:43] Mateo:** Lo que dijo la app:
```
violations() trade 1 → []
violations() trade 2 → []
gestionState()       → "2 trades — sesión completa. Se cierra la plataforma y se documenta."
Northpoint Score     → 750/1000 · PROFESIONAL
```

**[JUE 30 JUL · 18:44] Pablo:** Setecientos cincuenta sobre una cuenta reventada.

**[JUE 30 JUL · 18:45] Mateo:** El motor de violaciones **no conoce el dinero**. Vigila horario, símbolo, número de trades y estado anímico. No vigila pérdida diaria ni drawdown, que son los dos únicos límites que pueden matar una cuenta. Busqué en el código: `rDia` y `dailyLoss` sólo se pintan como texto, nunca se comparan contra el P&L real del día.

**[JUE 30 JUL · 18:47] Mateo:** Hacen falta dos violaciones más: `RIESGO DIARIO EXCEDIDO` y `LÍMITE DE LA FIRMA`. Y una alerta dura cuando `colchon <= 0`. Mientras eso no exista yo no puedo usar esta herramienta para hacer mi trabajo.

**[JUE 30 JUL · 18:52] Pablo:** Es la número uno de agosto. Y de paso, "límite diario de la firma: sin límite" tiene que dejar de decirse así. Es cierto y es la frase más malinterpretable de la app. Un socio nuevo lee eso y entiende que puede perder lo que quiera. Que diga "sin límite diario · tope real: drawdown $2,000".

**[JUE 30 JUL · 18:55] Pablo:** Y otra chica: el jueves perdí $210 con riesgo de fase en $200 y la app no dijo ni pío. Si el terminal calcula el riesgo de la fase, que avise cuando lo pasas. Ahorita ese número es decorativo.

**[VIE 31 JUL · 08:11] Pablo:** +$1,390. Cierra el mes.

---

## CIERRE DE MES · viernes 31 de julio

**[VIE 31 JUL · 17:02] André:** Lo que dice el terminal:
```
P&L del mes ............... +$28,865
meta declarada ............ $30,000  → 96.2%
meta derivada ............. $28,000  → 103.1%
filas en el journal ....... 35
decisiones reales ......... 27
días operados ............. 21 de 23 hábiles (22 reales)
winrate ................... 71.4%  ·  PF 2.76
Northpoint Score .......... 808 / 1000 · PROFESIONAL
```

**[VIE 31 JUL · 17:04] Pablo:** Espérate. Yo estoy viendo $28,050 en mi pantalla.

**[VIE 31 JUL · 17:05] Mateo:** Y yo $22,250 en el mío.

**[VIE 31 JUL · 17:07] André:** Ahí está la fricción del mes, y es la que más me pesa. La cifra es **proyectada**: cada trade multiplicado por las cuentas donde cayó. Mezcla filas de 5 cuentas, de 3 y de 2. Cambia según el picker y según el criterio de corte. **El mismo terminal nos dio tres cierres distintos del mismo mes.**

**[VIE 31 JUL · 17:10] Pablo:** Y la meta contra la que se compara también se movió sola. Nadie la tocó.

**[VIE 31 JUL · 17:11] André:** Correcto, lo corrí en las tres configuraciones:
```
5 en evaluación → mes $100,000
5 en colchón    → mes  $40,000
5 en retiros    → mes  $20,000
```

**[VIE 31 JUL · 17:12] Pablo:** O sea que el 1 de julio la barra me pedía cien mil y arrancaba en rojo, y hoy, después de que **yo mismo** moví las fases, me pide veintiocho mil y me pinta la barra llena. La app termina felicitándote por no llegar.

**[VIE 31 JUL · 17:15] André:** Y ahora la parte que hay que decir completa antes de la junta. **Dinero que entró al banco en julio: $0.**

**[VIE 31 JUL · 17:16] André:** $16,310 de esos $28,865 se hicieron antes del 15 de julio. En evaluación. Ese dinero se **borró** cuando las cuentas reiniciaron a $50,000. Nunca existió, era una calificación. Compró el derecho a operar en serio, nada más.

**[VIE 31 JUL · 17:18] André:** Lo que sí queda, con el plan ya corregido a Select Daily:
```
T1 / T2 / T3 · RETIROS  · $52,525 · piso $50,100 CONGELADO · colchón $2,425
T4 / T5      · COLCHÓN  · $51,870 · piso $49,870 flotando  · colchón $2,000 · faltan $230
suma sobre $50,100 en las cinco: $10,815
retiros ejecutados: 0
```

**[VIE 31 JUL · 17:20] André:** Con el plan sin corregir el terminal decía "faltan $130". Cien dólares de mentira que a una cuenta fondeada le importan.

**[VIE 31 JUL · 17:22] Pablo:** Entonces T4 y T5 no piden payout en agosto hasta que cierren los $230. No me voy a arriesgar a un rechazo por leer mal el terminal.

**[VIE 31 JUL · 17:26] André:** Última del Score, y me la como yo porque lo construí. De las **15 violaciones** que marcó el terminal en julio, **8 son falsas**. Todas nacidas de partir una decisión en dos filas.
```
              terminal   agrupando por decisión
Risk           208/250        225
Emotion        175/250        225
Decision       233/250        233
Consistency    191/250        191
total            808          875
```

**[VIE 31 JUL · 17:27] André:** Nos costó 67 puntos. No puedo defender un número que se mueve según cómo esté el picker de cuentas.

**[VIE 31 JUL · 17:30] Pablo:** Y ya que estamos con lo que la app dice que es y no es: las "4 firmas" son 3 personas.
```
Research (NP-030)   → mateo
Riesgo   (NP-020)   → mateo
Quant    (NP-040)   → andre
CIO      (NP-001)   → pablo
Ejecutar (NP-010)   → pablo
```

**[VIE 31 JUL · 17:31] Pablo:** Mateo cubre dos de las cuatro puertas él solo. Y yo firmo la cuarta **y** soy el único que puede marcarla ejecutada. Yo apruebo y yo ejecuto, sin nadie en medio. Para una mesa de tres está bien en la práctica, pero que la app lo diga: "3 firmantes · Mateo cubre 2 puertas".

**[VIE 31 JUL · 17:38] André:** Snowball:
```
AUM ................ $434,700
suscrito ........... $420,000
retorno acumulado .. 3.5%

Familia MR   $250,000 → $261,500  +4.6%  CORE · 15–22% · bloqueo 6m
Cuenta GL     $50,000 →  $51,800  +3.6%  SEED · 12–18% · bloqueo 12m
Despacho VH  $120,000 → $121,400  +1.2%  SEED · 12–18% · bloqueo 12m
```
Alta de Despacho VH el 20 de julio. Prospecto abierto: Tío R, $80,000.

**[VIE 31 JUL · 17:40] André:** Y ese "3.5% acumulado" no significa nada, y soy yo el que se lo tiene que enseñar a un cliente. Una posición tiene `capital` y `valor` y nada más. No hay serie de tiempo, no hay fecha de valuación, no hay aportaciones. VH lleva once días y su +1.2% se promedia con el +4.6% de Familia MR que lleva el mes completo, como si fueran comparables. No hay TWR, no hay anualizado. Es una calculadora de resta.

**[VIE 31 JUL · 17:42] Mateo:** Y `nextRebalance()` tiene los trimestres cableados abr/jul/oct/ene y se salta julio estando en julio. Dice "70 días" contando desde el reloj de la máquina, no desde la fecha del reporte.

**[VIE 31 JUL · 17:50] Pablo:** Cierro yo. Julio fue un buen mes de proceso y un mes de cero de ingreso, que es exactamente lo que un mes 1 de fondeo debe ser. Pasamos las cinco cuentas, tres tienen el piso congelado y colchón completo, dos van a $230.

**[VIE 31 JUL · 17:51] Pablo:** Lo que **no** acepto es un reporte que diga 96.2% de la meta cuando el estado de cuenta del banco dice cero. La meta es la declarada, $30,000, punto. No me la voy a regalar cambiando el denominador.

**[VIE 31 JUL · 17:53] André:** Y hay que decirlo completo: el mes se retrasó **seis días hábiles** por una falla de copiadora que el terminal no detectó. Si T4 y T5 hubieran tenido el +$1,150 del 7 y el +$880 del 10, pasan evaluación el 14 con las demás, la mesa nunca se parte, no hay 8 violaciones falsas, y hoy las cinco estarían en retiros.

**[VIE 31 JUL · 17:54] André:** Toda la cadena de problemas del mes cuelga de dos órdenes que no se replicaron y de que nadie se enteró hasta tres días después.

**[VIE 31 JUL · 18:05] Pablo:** Lista de agosto, en orden. Que quede aquí:

**[VIE 31 JUL · 18:06] Pablo:**
```
1. Violaciones de dinero: RIESGO DIARIO EXCEDIDO y LÍMITE DE LA FIRMA.
   Alerta dura con colchón <= 0. No se negocia. (Mateo)
2. Alerta de copiadora: si una orden cae en menos cuentas de las vivas, que grite. (André)
3. Agrupar por decisión, no por fila. Devuelve 67 puntos de Score. (André)
4. Fase y plan en un solo movimiento, o aviso en rojo cuando no cuadran.
5. Medidor de consistencia: mejor día / ganancia total vs el 40%.
6. Topar metas() contra el hito de la fase. Que deje de pedir $100,000.
7. reglasFondeadas()/reglasEval() por familia de plan.
8. Fecha editable en el reinicio y cambio de fase por selección.
9. Registro de retiros y campo de motivo en la violación.
10. Feriados de mercado y poder pararse en una fecha pasada.
```

**[VIE 31 JUL · 18:08] Pablo:** Y una mía, operativa: un trade al día mientras el checklist no esté completo antes de las 7:30. Ventana cerrada en duro a las 8:30. Copiadora revisada los lunes a las 6:50.

**[VIE 31 JUL · 18:10] Mateo:** Cerramos julio con las cinco cuentas vivas y fondeadas, y con un sistema de vigilancia que todavía no vigila lo que importa. Las dos cosas son ciertas.

**[VIE 31 JUL · 18:11] André:** Agosto es el primer mes donde puede entrar dinero. Nos vemos el lunes 3.