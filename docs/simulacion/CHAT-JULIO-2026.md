# Chat de la mesa · julio 2026

Un mes completo de operación de NORTHPOINT, con los cuatro socios coordinándose día a día.

**Los números de los trades son reales**: salieron de simular 65% de aciertos a 1:1 y
pasarlos por el motor de cálculo del propio terminal — las mismas funciones que la app usa
para detectar violaciones, calcular el drawdown y el Northpoint Score. La conversación es
la reconstrucción de cómo se coordinaron para llegar a esos números.

| Quién | Cargo | Qué firma |
|---|---|---|
| **PABLO** | Chief Investment Officer · Portfolio Manager | La cuarta puerta (CIO). Es el único que ejecuta |
| **MATEO** | Chief Risk Officer · Research Analyst | Dos puertas: Research y Riesgo. Puede detener la mesa él solo |
| **ANDRÉ** | Quant · Chief Operating Officer | La puerta Quant: que los números cuadren |
| **GOYO** | Chief Strategy Officer | **Ninguna.** Aporta el marco macro, no vota trades |

Cinco cuentas Tradeify de 50k replicadas por un copiador: **una orden entra en las cinco a
la vez**. Por eso cada cifra aparece dos veces — «por cuenta» y «la mesa», que es ×5.

---


## 1 de julio · miércoles

> **−$5,020 la mesa · 2 trades · VIOLACIÓN de riesgo diario** — acumulado por cuenta: -1,004

`06:41`  **GOYO** · Buenos días. Antes de que abran, dejo el marco de julio para que sepan en qué agua estamos nadando. Venimos de dos lecturas de inflación seguidas debajo de lo esperado y el mercado ya trae descontado el recorte de septiembre casi al 90%. El dólar lleva tres semanas bajando y las tasas a 10 años se aplanaron. Eso históricamente es viento a favor para el Nasdaq, pero también sube el ruido intradía porque hay mucho posicionamiento apretado del mismo lado.

`06:44`  **GOYO** · Eventos que condicionan el mes: nóminas el viernes 3, CPI el jueves 9, y desde el 14 arranca la temporada de reportes con los bancos. La semana del 28 traemos Fed. Mi sesgo estructural para el mes es largo, pero con la advertencia de que las primeras dos semanas son de rango, no de tendencia. Todo lo que aporto es contexto, ustedes tienen la ventana.

`07:08`  **PABLO** · Buenos días. Primer día del mes, arrancamos las 5 cuentas en 50k limpias. Ojo con el proceso, no con el resultado.

`07:12`  **MATEO** · Buenos días. Research: NQ viene de dos días de rango, no hay barrido limpio de nada. Ando tibio con esto.

`07:20`  **ANDRÉ** · Firma Quant lista: 25 puntos de stop × $20 = $500 por cuenta, × 5 = $2,500 mesa. Riesgo del día limpio, 1,000 disponibles por cuenta.

`07:22`  **PABLO** · Leí el plan de Mateo. Sesgo largo por el gap y por el nivel de ayer. Firmo CIO.

`07:29`  **MATEO** · Pablo quiere el largo arriba del ORB. Ok, firmo Research por continuación del alza de ayer. Riesgo: 1 contrato x 5, stop 25 pts abajo del ORB = $500/cuenta. Firmado.

`07:35`  **PABLO** · Ejecutado. NQ largo en el rompimiento del ORB, 1 contrato por cuenta, stop 25 puntos. 07:33.

`07:35`  **ANDRÉ** · Primera entró 07:33 LONG. Stop cargado en el copiador, las 5 cuentas espejeadas sin desfase.

`07:41`  **MATEO** · Nos sacaron. -511/cuenta. El deslizamiento nos pegó 11 dólares extra. Anótenlo, eso importa.

`07:45`  **PABLO** · Stop. -511 por cuenta. Nos queda un intento.

`07:48`  **ANDRÉ** · Salió el stop: -511 por cuenta, no -500. Se deslizó medio punto y medio. Quedan 489 de riesgo del día, no 500. Anótalo antes del segundo.

`07:51`  **MATEO** · Segundo y último intento. Mismo esquema largo, stop 25 pts. Riesgo firmado pero ya vamos con 511 encima: si esto pega el stop nos pasamos del tope diario. Que quede escrito.

`07:55`  **PABLO** · Segundo ejecutado 07:53, largo otra vez, mismo stop. Y también pegó. -493.

`08:02`  **ANDRÉ** · Segundo stop -493. 511 + 493 = 1,004. Nos pasamos 4 dólares del tope diario. El motor ya marcó VIOLACIÓN: DAY_RISK.

`08:05`  **MATEO** · -493. Cerramos -1,004 por cuenta. -5,020 la mesa. Y sí: el motor marcó VIOLACIÓN de riesgo diario. Nos pasamos por 4 dólares.

`08:20`  **MATEO** · Como CRO no lo dejo pasar. El problema no es que perdimos, es que el sistema permitió pasarnos del tope. Dos stops de $500 con deslizamiento SIEMPRE van a rebasar $1,000. Aritmética, no mala suerte.

`08:24`  **MATEO** · Corrección efectiva desde mañana: riesgo por trade baja de $500 a $475 por cuenta. Dos stops completos con deslizamiento = ~$990. Cabemos abajo del tope. No lo estoy proponiendo, lo estoy poniendo.

`08:31`  **MATEO** · André, ajusta el sizing en el copiador. Pablo, ya sé que odias bajar riesgo después de un rojo, pero es lo contrario: bajamos riesgo porque el tope existe, no porque perdimos.

`08:40`  **PABLO** · Cierre: -1,004 por cuenta, -5,020 la mesa. Peor arranque posible.

`08:44`  **PABLO** · Y hay algo más grave que el dinero. El motor marcó VIOLACIÓN de riesgo diario: 1,004 contra tope de 1,000. Nos pasamos.

`08:47`  **PABLO** · Que quede claro: eso no fue mala suerte, fue mal diseño. Dos stops de 500 nominales no caben en un tope de 1,000 porque el slippage se come el margen. La regla estaba escrita para no cumplirse.

`08:50`  **ANDRÉ** · La cuenta no daba desde el principio: 2 × 500 = 1,000 exacto, sin margen para deslizamiento. Diseñamos una regla que solo se cumple si el mercado nos llena perfecto las dos veces.

`08:52`  **PABLO** · Ajuste desde mañana, decisión de CIO: el segundo trade va con riesgo recortado. Si el primero pierde más de $520, se acabó el día. No hay segundo. André, quiero eso duro en el motor, no en la memoria de nadie.

`08:52`  **GOYO** · Vi el cierre. -1,004 por cuenta y arriba del tope diario. No voy a opinar de la ejecución porque no es mi puerta, pero sí de por qué el día estaba trampa: primer día del trimestre, rebalanceo de fondos de pensiones y un ORB que se formó con volumen de reposicionamiento, no de convicción. Ese rango se rompe hacia los dos lados y no significa nada.

`08:55`  **GOYO** · Y la parte incómoda: el exceso de $4 sobre el tope no es un error de dedo, es un síntoma. El primer día del mes es cuando más ganas hay de arrancar con algo. Eso no es macro, eso es calendario mental.

`08:58`  **ANDRÉ** · Le pongo número para no andar cambiándolo: riesgo objetivo $475 por trade, 23 puntos de stop ($460 nominal). Dos stops con 6% de deslizamiento = 975. Cabe con margen.

`09:04`  **ANDRÉ** · Va, Pablo. No queda en la memoria de nadie: lo pongo como bloqueo duro en el motor. Si el segundo trade no cabe en lo que resta del día, el terminal no deja firmar. Cero criterio humano.


## 2 de julio · jueves

> **+$2,540 · 1 trade** — acumulado por cuenta: -496

`06:38`  **GOYO** · Ojo con hoy y mañana. Nóminas el viernes con el mercado medio cerrado por el 4 de julio significa liquidez delgada en la sesión previa. Rango contenido y falsos rompimientos. Si el marco del mes es largo pero el régimen de esta semana es de rango, la única lectura consistente es paciencia. Ustedes deciden, yo solo pongo el clima.

`07:14`  **MATEO** · Barrido del mínimo de Asia en 21,430 y FVG de 4H arriba. Estructura limpia. Research firmado.

`07:22`  **ANDRÉ** · Bloqueo ya vive en el terminal. Validado: 23 puntos × $20 = $460, × 5 cuentas = $2,300 mesa. Riesgo del día intacto.

`07:26`  **PABLO** · Cuatro firmas listas. Firmo CIO: mismo sesgo pero con el tope nuevo puesto.

`07:28`  **MATEO** · Riesgo: 1 contrato, stop 24 pts abajo del barrido = $480/cuenta. Dentro del nuevo límite. Firmado. Pablo tienes luz verde cuando el ORB confirme.

`07:33`  **PABLO** · Ejecutado 07:31, NQ largo, 1 contrato por cuenta. Salió +508. Se para. Regla es regla, no le buscamos el segundo.

`07:45`  **MATEO** · +508. Primer trade ganador, se para. No hay segundo. Esa es la regla y hoy sí la respetamos.

`08:05`  **ANDRÉ** · +508 en la primera y paramos. Segundo trade bloqueado por regla, no por ganas. Así se ve cuando el sistema manda.


## 3 de julio · viernes

> **−$15 · 2 trades** — acumulado por cuenta: -499

`07:12`  **GOYO** · Oigan, el NQ acaba de barrer el mínimo de ayer y regresó adentro. Eso normalmente es entrada larga. ¿Alcanzan a meter el segundo?

`07:19`  **GOYO** · Tienen toda la razón, perdón. Me metí a una puerta que no es mía. Yo no firmo Research ni Riesgo y menos ejecuto — ver una figura bonita en el gráfico no me da voto. Queda anotado y no se repite. Mi trabajo empieza a las 8:35, no a las 7:12.

`07:20`  **MATEO** · Viernes previo a feriado gringo, liquidez chafa. Research firmado pero con nota: hoy espero más ruido del normal. Short desde el máximo de ayer, stop 24 pts.

`07:25`  **ANDRÉ** · Validado SHORT, 23 puntos, $460 nominal. Si pierde quedan ~528 del tope diario, alcanza para el segundo. Firmo.

`07:48`  **MATEO** · -527. Nos barrieron y se regresó. Clásico de viernes flojo. Queda un intento y ya.

`08:05`  **MATEO** · +524 el segundo. Día cerrado en -3 por cuenta, prácticamente plano. Lo tomo. Ojo: con el riesgo viejo este día habría sido peor.

`08:10`  **ANDRÉ** · -527 y +524, día en -3 por cuenta. Lo importante: nunca nos acercamos al tope. El bloqueo hizo su trabajo.

`08:40`  **PABLO** · -3 por cuenta. Día plano. El segundo trade recuperó casi todo el primero y el riesgo se quedó dentro del tope. Eso es lo que quería ver.


## 6 de julio · lunes

> **−$135 · 2 trades** — acumulado por cuenta: -526

`06:47`  **GOYO** · Semana corta y arrancamos post-feriado. El posicionamiento de fondos apalancados en NQ subió a máximos de tres meses según el reporte del viernes, o sea que hay mucha gente del mismo lado del barco. Eso no cambia mi sesgo largo del trimestre, pero sí sube la probabilidad de sacudidas rápidas sin dirección. Mi lectura de la semana: cuidado el jueves, CPI.

`07:18`  **MATEO** · Short otra vez, tomamos el máximo del viernes. Research y Riesgo firmados, stop 24 pts, $480.

`07:26`  **ANDRÉ** · Firma Quant: 23 puntos, $460, cabe completo. Segundo intento disponible con 540 de holgura.

`08:08`  **MATEO** · -529 y luego +502. -27 el día. Dos sesiones seguidas planas. No es glamoroso pero no estamos sangrando, y eso ahorita vale.

`08:12`  **ANDRÉ** · -529 y +502, día -27. Dos días seguidos de casi-plano. Aburrido es exactamente lo que queremos.

`08:38`  **PABLO** · Otro plano, -27. Dos días seguidos casi en cero. Aburrido está bien.


## 7 de julio · martes

> **sin operar · Mateo detuvo la mesa** — acumulado por cuenta: -526

`07:22`  **MATEO** · No veo setup. El precio está a la mitad del rango de ayer, sin barrido de nada, sin desbalance arriba ni abajo. Research NO firmado.

`07:31`  **MATEO** · Pablo, "se ve que quiere subir" no es una tesis. Dime el nivel, dime qué liquidez tomó y dime dónde va tu stop. Si no me lo dices, no hay firma.

`07:36`  **MATEO** · No. Riesgo tampoco firma. Un stop de 25 pts a media zona de balance es regalar dinero, es la peor colocación posible.

`07:40`  **MATEO** · Y para que no quede duda: como CRO estoy deteniendo la mesa hoy. No necesito las otras firmas para eso. Hoy no se opera.

`07:44`  **PABLO** · Ya. No hay setup. El rango salió sucio y no cumple filtro de Mateo. Rechazo CIO: no operamos hoy.

`07:47`  **PABLO** · Sé que va la primera semana en rojo y da comezón. No se opera por comezón. Nos vemos mañana.

`08:35`  **MATEO** · Cerró el rango dentro del de ayer. Cero direccionalidad. Un día sin operar no es un día perdido, es un día en que no le regalamos $2,500 al mercado.

`08:35`  **ANDRÉ** · Cero trades hoy. En el journal va como día válido, no como día perdido: 0 riesgo consumido, 0 faltas.


## 8 de julio · miércoles

> **+$2,410 · 1 trade** — acumulado por cuenta: -44

`06:52`  **GOYO** · Nota de contexto para hoy y mañana: el CPI de mañana es el dato del mes. Consenso 2.4% general, 2.9% subyacente. Si sale en línea o abajo, confirma septiembre y el sesgo largo estructural se refuerza. Si sale caliente, el mercado tiene que repreciar y las primeras dos horas van a ser una carnicería de rango. Ayer no se operó y me pareció la decisión más profesional del mes hasta ahora — no operar también es una posición.

`07:25`  **MATEO** · Regresó la estructura: barrido del mínimo de ayer y aceptación arriba. Research firmado. Riesgo: stop 24 pts, $480. Firmado.

`07:28`  **ANDRÉ** · Validado LONG, 23 puntos = $460 por cuenta, $2,300 mesa. Firmo.

`07:39`  **PABLO** · Ejecutado 07:37, largo, 1 contrato por cuenta, stop 25. +482 y cerramos.

`07:52`  **MATEO** · +482. Se para. Buen ritmo.


## 9 de julio · jueves

> **+$2,410 · 1 trade** — acumulado por cuenta: +438

`07:19`  **MATEO** · Short desde el máximo de la sesión europea, hay desbalance abajo sin llenar. Ambas firmas mías puestas, stop 24 pts.

`07:32`  **PABLO** · Ejecutado 07:30, corto esta vez. +482. Se para.

`07:45`  **MATEO** · +482. Dos verdes seguidos. Acumulado ya en positivo por primera vez en el mes: +438/cuenta.

`08:00`  **ANDRÉ** · +482. Acumulado por cuenta: +438. Primera vez en verde en el mes, día 6 de operación.


## 10 de julio · viernes

> **+$2,645 · 1 trade** — acumulado por cuenta: +967

`07:21`  **MATEO** · Largo tras barrido del mínimo semanal. Research firmado con nota: es el mismo patrón que el 08. Riesgo firmado, 24 pts.

`07:50`  **MATEO** · +529. Semana cerrada. Acumulado +967. Tres verdes de fila y ninguno vino de forzar el segundo trade.

`08:15`  **ANDRÉ** · +529. Vamos +967 por cuenta. Les traigo la cuenta honesta el lunes, porque el plan original mentía.

`08:36`  **PABLO** · +529. Tercer verde seguido y ya andamos en +438 acumulado por cuenta. Primera vez del mes arriba de cero.

`08:47`  **GOYO** · Tres verdes seguidos y el CPI salió en línea. Quiero ser claro en algo: los tres verdes no son porque el macro salió a favor. El macro solo definió que el régimen permitiera tendencia limpia en la primera hora. La ejecución fue de ustedes. Lo digo porque cuando venga el rojo tampoco va a ser culpa del macro.


## 13 de julio · lunes

> **−$4,960 la mesa · 2 trades** — acumulado por cuenta: -25

`07:20`  **MATEO** · Largo arriba del ORB. Firmo las dos, stop 24 pts. Estructura decente aunque el volumen viene bajo.

`07:27`  **ANDRÉ** · Validado, 23 puntos, $460. Queda espacio para dos intentos completos bajo el tope. Firmo.

`07:45`  **MATEO** · -471. Segundo intento en corto porque se rompió abajo del ORB. Firmo Riesgo pero con el ojo en el tope: llevamos 471, un stop más nos deja en ~992. Cabe. Justo, pero cabe.

`08:10`  **MATEO** · -521. Cierre -992 por cuenta. Duele, pero AQUÍ está la diferencia: el 1 de julio esto habría sido violación. Hoy el ajuste nos mantuvo abajo del tope por 8 dólares. Ese cambio ya se pagó solo.

`08:20`  **ANDRÉ** · -471 y -521. Día -992 por cuenta. Este es exactamente el escenario del 1 de julio y hoy SÍ cupo: 992 contra tope de 1,000. El ajuste aguantó por 8 dólares.

`08:22`  **MATEO** · Como CRO evalué detener la mesa mañana. Decisión: NO paro. Revisé los dos trades y ambos tenían tesis válida y stop bien puesto; perdimos por mercado, no por indisciplina. Detengo la mesa cuando se rompe el proceso, no cuando se rompe el resultado.

`08:24`  **ANDRÉ** · Con la regla vieja este día habría sido otra violación. Con 25 puntos esos dos stops habrían sido ~1,078. Segunda falta grave y adiós evaluación.

`08:26`  **MATEO** · Pero pongo una condición: si mañana hay otro rojo de dos stops, paramos dos días completos. Eso sí lo estoy anunciando, no negociando.

`08:40`  **PABLO** · Feo. -992 por cuenta, -4,960 la mesa. Largo primero, corto después, los dos pegaron.

`08:43`  **PABLO** · Pero revisen bien: -992 quedó DEBAJO del tope. El ajuste del 1 de julio funcionó justo el día que tenía que funcionar. Perdimos dinero, no perdimos la cuenta.

`08:48`  **PABLO** · Nada que cambiar. El plan estaba firmado por los cuatro, la ejecución fue la correcta, el mercado no pagó. Mañana igual.

`08:58`  **GOYO** · -992. Segundo peor día. Contexto de por qué el día estaba raro: arrancó temporada de reportes esta semana y el lunes previo a los bancos suele traer rotación sectorial fuerte, o sea el índice se mueve pero por debajo se están peleando los componentes. ORB con dirección falsa, básicamente.

`09:10`  **ANDRÉ** · La cuenta honesta que les debía. 65% de aciertos a 1:1, parando después de la primera ganadora: 0.65 × 500 = 325, menos 0.35 × [0.65 × 0 + 0.35 × 1,000] = 122.5. Esperanza = +202 por cuenta por día.

`09:13`  **ANDRÉ** · O sea que el "objetivo diario de $1,000" del plan era ficción. 3,000 entre 202 = 15 días hábiles, no 3–5. El plan no estaba mal de riesgo, estaba mal de expectativas.


## 14 de julio · martes

> **+$2,615 · 1 trade** — acumulado por cuenta: +498

`07:23`  **MATEO** · Short desde el máximo de ayer, hay liquidez clara arriba ya tomada. Research firmado. Riesgo: 24 pts, $480. Firmado.

`07:30`  **ANDRÉ** · Firma Quant: 23 puntos, $460, riesgo del día completo. +523. Acumulado +498.

`07:40`  **PABLO** · Ejecutado 07:38, corto. +523.

`07:52`  **MATEO** · +523. Se para al primero. Condición levantada.


## 15 de julio · miércoles

> **+$2,625 · 1 trade** — acumulado por cuenta: +1,023

`06:35`  **GOYO** · La pregunta que traigo desde el domingo y que quiero dejar por escrito aunque no me toque firmar: ¿los dos días de -1,000 son mercado o son sistema? Porque si son mercado, la respuesta es aguantar. Si son sistema, aguantar nos cuesta la cuenta.

`06:38`  **GOYO** · Lo que veo desde mi lado: los dos días grandes fueron 1 de julio y 13 de julio. Ambos inicio de periodo, ambos con flujo de rebalanceo, ambos con el ORB formándose sobre volumen que no era direccional. Eso me huele más a un filtro que falta que a mala suerte. Y los días rojos chicos (-3, -27, -24) están perfectos: ahí el sistema sí está cortando bien. El problema no es la frecuencia de pérdidas, es la asimetría de dos de ellas.

`07:24`  **MATEO** · Mismo patrón que ayer, el precio respetó el nivel de rechazo. Ambas firmas, stop 24 pts.

`07:50`  **MATEO** · +525. Acumulado +1,023, arriba de mil por primera vez. Vamos por el tercio del objetivo.

`08:05`  **ANDRÉ** · +525. Acumulado +1,023 por cuenta. Cruzamos a verde neto por primera vez desde el 1.


## 16 de julio · jueves

> **−$120 · 2 trades** — acumulado por cuenta: +999

`07:19`  **MATEO** · Largo. Research firmado aunque la estructura está más sucia que ayer. Riesgo firmado, 24 pts.

`08:05`  **MATEO** · -499 y luego +475. Día en -24. Segundo trade rescató casi todo. Sigo prefiriendo los días de un solo trade, la estadística del mes lo dice: cuando entramos dos veces, el día promedio es negativo.

`08:18`  **ANDRÉ** · -499 y +475, día -24. Riesgo consumido 499, mitad del tope. Ni cerca de la línea.

`08:38`  **PABLO** · -24 y adentro del tope. Ya llevamos varios de estos, el segundo trade está haciendo su trabajo.


## 17 de julio · viernes

> **+$2,420 · 1 trade** — acumulado por cuenta: +1,483

`07:22`  **MATEO** · Short desde el máximo del rango semanal. Firmas puestas, 24 pts. Corto y claro.

`07:48`  **MATEO** · +484. Acumulado +1,483. Llevamos los 3 días mínimos hace rato. El cuello es el +3,000.

`08:00`  **ANDRÉ** · +484. Acumulado +1,483. Consistencia: nuestro mejor día del mes es +529 y el tope del 40% sobre 3,459 sería 1,384. No hemos estado ni a la mitad. Nunca fue el problema.

`08:37`  **PABLO** · +484. Acumulado +1,483 por cuenta. Vamos a la mitad del objetivo y tenemos días de sobra.

`08:44`  **GOYO** · Cerró la semana en +1,483 acumulado. Sobre el trimestre: la Fed es el 29-30 y ahí sí quiero que tengan el contexto encima. No espero recorte en esa junta, espero lenguaje. El movimiento no va a estar en el anuncio, va a estar en los 20 minutos de la conferencia, y eso cae fuera de nuestra ventana de todos modos. Ventaja de operar 7:00-8:30: los días de Fed nos los saltamos por diseño.


## 20 de julio · lunes

> **+$2,645 · 1 trade** — acumulado por cuenta: +2,012

`07:20`  **MATEO** · Largo tras barrido de la mínima del viernes. Research y Riesgo firmados, stop 24 pts.

`07:29`  **ANDRÉ** · Validado LONG, 23 puntos, $460. Firmo. +529, acumulado +2,012.

`07:35`  **PABLO** · Ejecutado 07:33, largo, 1 contrato por cuenta. +529 y se para.

`07:49`  **MATEO** · +529. Acumulado +2,012. Dos tercios del objetivo. Nadie se emocione, faltan mil.


## 21 de julio · martes

> **+$2,350 · 1 trade** — acumulado por cuenta: +2,482

`07:26`  **MATEO** · Largo, continuación. Firmo las dos con nota: entramos 07:35, más tarde de lo normal, esperé confirmación del ORB. Stop 24 pts.

`07:54`  **MATEO** · +470. Acumulado +2,482.

`08:05`  **ANDRÉ** · +470. Acumulado +2,482. Faltan 518 para el objetivo. Días mínimos ya cubiertos hace rato.

`08:36`  **PABLO** · +470. Ojo con la consistencia del 40%: ningún día nuestro pasa de 530, no hay riesgo por ese lado. Bien.


## 22 de julio · miércoles

> **+$2,380 · 1 trade** — acumulado por cuenta: +2,958

`07:21`  **MATEO** · Largo, mismo patrón que ayer. Firmas puestas. Recordatorio de Riesgo: estamos a ~520 del objetivo y ahí es donde la gente se pone codiciosa y sube tamaño. El tamaño NO se mueve.

`07:31`  **ANDRÉ** · Firma Quant: 23 puntos, $460. Si pega, quedamos a ~40 puntos del objetivo. +476, acumulado +2,958.

`07:35`  **PABLO** · Ejecutado 07:33, largo. +476. Quedamos a menos de 550 del objetivo.

`07:50`  **MATEO** · +476. Acumulado +2,958. Mañana, si sale un trade limpio, cruzamos.


## 23 de julio · jueves

> **+$2,505 · 1 trade · EVALUACIÓN PASADA** — acumulado por cuenta: +3,459

`07:18`  **MATEO** · Largo tras barrido del mínimo de ayer, desbalance arriba sin llenar. Research firmado. Riesgo: 1 contrato, stop 24 pts, $480. Sin cambios, hoy menos que nunca.

`07:20`  **PABLO** · Hoy puede caer. Aviso: si entra el trade y gana, se cierra el día y se cierra la evaluación. Nadie toca nada después. Firmo CIO.

`07:36`  **PABLO** · Ejecutado 07:34, NQ largo, 1 contrato por cuenta, stop 25. +501.

`07:50`  **ANDRÉ** · +501. Acumulado +3,459 por cuenta, balance $53,459. Objetivo cruzado. Evaluación PASADA en las 5 cuentas.

`07:52`  **MATEO** · +501. Acumulado +3,459 por cuenta. Balance $53,459. Objetivo cruzado, evaluación PASADA en las 5 cuentas.

`08:10`  **MATEO** · Cierre del mes: 21 trades, 14-7, 66.7%. 11 verdes, 5 rojos, 1 sin operar. 16 días. Pero el número del que estoy más orgulloso es el 7 de julio: cero trades. Ese día también construyó esto.

`08:15`  **MATEO** · Y el ajuste del 1 de julio nos salvó el 13. Una violación de riesgo en un mes, y fue el primer día. Eso es lo que reporto. Ahora sí, felicidades cabrones.

`08:35`  **PABLO** · Listo. +3,459 acumulado por cuenta, balance $53,459. Evaluación PASADA en las 5 cuentas.

`08:40`  **PABLO** · Números del mes: 21 trades, 14 ganados, 7 perdidos, 66.7%. 11 verdes, 5 rojos, 1 sin operar. 16 días.

`08:46`  **PABLO** · Lo que nos pasó la evaluación no fue el 66.7%. Fue el 7 de julio que no operamos y el ajuste que salió del desastre del día 1. El proceso aguantó dos días de -1,000 sin romperse. Eso es lo que se replica. Bien hecho, señores.

`08:51`  **GOYO** · Pasada. +3,459 por cuenta, balance 53,459. Felicidades, en serio. Ahora la parte que me toca a mí, que es la fea: pasamos con 66.7% de aciertos, que es un número excelente, pero tardamos 16 días cuando el plan decía 3 a 5. Eso no es un detalle de calendario, es información sobre el sistema.

`08:56`  **GOYO** · Lo que significa: el plan de 3 a 5 días asumía que un día promedio aporta entre +600 y +1,000 netos. La realidad fue que el día promedio ganador aporta ~+500 y que dos días malos se comieron 15 días de avance. O sea, el sistema no es lento — el sistema es correcto y el plan era optimista. Si en las cuentas fondeadas seguimos calibrando expectativas con el plan viejo, vamos a tomar riesgo de más para "ponernos al corriente". Ése es el riesgo real del próximo trimestre, y no está en el mercado, está en nosotros.

`09:00`  **ANDRÉ** · Reporte del mes: 21 trades, 14 ganados / 7 perdidos, 66.7%. 11 días verdes, 5 rojos, 1 sin operar. 16 días para pasar contra los 3–5 que decía el plan; los 202 diarios de esperanza predecían 15. La cuenta cuadró.

`09:02`  **GOYO** · Mi propuesta para el trimestre que entra, tres cosas y las dejo a votación de quienes sí firman. Uno: reescribir el objetivo de payout en días reales, 16-20 hábiles, no 5. Que la meta deje de mentirnos. Dos: un filtro de calendario que marque en rojo los días de rebalanceo — primer y último día hábil del mes, vencimientos trimestrales, lunes de arranque de temporada de reportes. En esos días o no se opera o se opera a medio riesgo. Los dos días de -1,000 del mes cayeron ahí.

`09:04`  **ANDRÉ** · Consistencia final: mejor día +529 contra tope de 1,384. 38% de margen sin usar. Peor día -1,004 el 1 de julio, único día que rompió el tope en todo el mes.

`09:05`  **GOYO** · Y tres: quiero que el marco macro deje de ser un mensaje mío de las 6:40 y se vuelva un insumo formal del sesgo semanal. No para decidir entradas — ésa no es mi puerta y ya aprendí — sino para que cuando Mateo evalúe un setup sepa si estamos en régimen de tendencia o de rango. Este mes esa diferencia valió $2,000 por cuenta. Un trimestre entero valdría mucho más.

`09:08`  **ANDRÉ** · Northpoint Score al cierre: 690 de 1000, grado EN DESARROLLO. Nos pesa una falta grave, la DAY_RISK del 1 de julio. Se queda en el expediente, no se borra.

`09:12`  **ANDRÉ** · Lo que me llevo como COO: el mes no lo salvó la disciplina, lo salvó cambiar un número mal diseñado el día 1. 23 puntos en vez de 25. Eso fue todo.
