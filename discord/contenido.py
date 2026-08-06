# -*- coding: utf-8 -*-
"""
NORTHPOINT · contenido del servidor de Discord.

Todo el texto vive aqui. build.py lo lee y lo publica.
Los {c[canal]} se reemplazan por el ID real del canal ya creado,
para que las menciones queden clicables.

REGLA: no hay testimonios, no hay resultados prometidos, no hay cifras
inventadas de rendimiento. Donde falta un dato comercial dice [PENDIENTE].
"""

# ─────────────────────────────────────────────────────────────
# ESTRUCTURA
#  (categoria, [(canal, tipo, topic)])
#  tipo: 0 texto · 2 voz · 5 anuncios · 15 foro
# ─────────────────────────────────────────────────────────────

ESTRUCTURA = [
    ("EMPIEZA AQUI", [
        ("bienvenida",         0, "Que es Northpoint y por donde empezar."),
        ("codigo-de-conducta", 0, "Las reglas de la casa. Condicion de entrada."),
        ("anuncios",           0, "Avisos de la firma. Solo lectura."),
    ]),
    ("LA FIRMA", [
        ("filosofia",        0, "Los seis pilares. Y lo que Northpoint no es."),
        ("northpoint-score", 0, "El sistema propietario 0-1000 de conducta."),
        ("la-mesa",          0, "90 minutos al dia. Un protocolo cerrado. Maximo dos operaciones."),
        ("proceso",          0, "Los cinco pasos de toda decision."),
    ]),
    ("FORMACION", [
        ("bootcamp",       0, "El curso completo: de cero a operar con protocolo."),
        ("plan-de-estudio", 0, "Los seis modulos, en orden."),
        ("biblioteca",     0, "Lecturas, papers y material de referencia."),
        ("dudas-del-curso", 0, "Preguntas sobre el material. Se responden aqui."),
    ]),
    ("EL TERMINAL", [
        ("el-journal",   0, "El registro de operaciones y de conducta."),
        ("agentes-ia",   0, "Los agentes que revisan tu sesion y tu disciplina."),
        ("aprobaciones", 0, "Mesa de aprobaciones: nada se ejecuta sin pasar por aqui."),
    ]),
    ("LA SESION", [
        ("ice-vader",         0, "Senales del indicador ICE VADER. Automatico. No se escribe aqui."),
        ("bitacora-del-dia",  0, "Lo que paso hoy en la mesa, en una linea."),
        ("sala-de-operacion", 2, ""),
    ]),
    ("ACCESO", [
        ("productos-y-acceso", 0, "Que se vende, que incluye, y como entrar."),
        ("preguntas",          0, "Lo que todos preguntan antes de entrar."),
    ]),
    ("COMUNIDAD", [
        ("general",    0, "Conversacion abierta."),
        ("presentate", 0, "Quien eres, que operas, desde cuando."),
        ("progreso",   0, "Tu Score, tu racha, tu mes. Evidencia, no opiniones."),
    ]),
]


# ─────────────────────────────────────────────────────────────
# MENSAJES
# ─────────────────────────────────────────────────────────────

MENSAJES = {

"bienvenida": ["""# NORTHPOINT
### Behavioral Intelligence for Traders

No somos un canal de senales. No predecimos el precio.

La mayoria de las perdidas de un trader no ocurren por falta de conocimiento tecnico. Ocurren en los segundos que van de **ver la senal** a **presionar ejecutar**. Ahi no falla el analisis. Falla la conducta.

Northpoint existe para medir esa conducta, ponerle numero, y darte un protocolo que la contenga.
""",

"""## Lo que vive aqui

**{c[bootcamp]} — El Bootcamp**
El metodo completo. De cero a operar con un protocolo cerrado.

**{c[el-journal]} — El Journal**
Tu registro. Cada operacion, cada decision, cada desviacion. Es lo que alimenta tu Score.

**{c[agentes-ia]} — Los Agentes**
Revision automatica de tus sesiones. Te dicen lo que tu no quieres ver.

**{c[ice-vader]} — La Senal**
ICE VADER publica aqui cada evento de la sesion: Asia, Londres, Nueva York, el ORB, el break, el retest, la entrada y el resultado.
""",

"""## Por donde empezar

**1.** Lee {c[codigo-de-conducta]}. No es adorno. Es la condicion de entrada.
**2.** Lee {c[filosofia]} y {c[northpoint-score]}. Ahi esta la doctrina completa.
**3.** Presentate en {c[presentate]}: que operas y desde cuando.
**4.** Cuando quieras el acceso, {c[productos-y-acceso]}.

-# Northpoint Capital Management"""],


"codigo-de-conducta": ["""# CODIGO DE CONDUCTA

Northpoint se sostiene sobre cuatro valores. No son decorativos: son la condicion para seguir aqui.

**Integridad**
Se reporta lo que paso. La operacion perdida se publica igual que la ganada. Un journal maquillado no sirve para nada, y aqui se nota.

**Disciplina**
El protocolo se respeta cuando conviene y cuando no. Especialmente cuando no.

**Transparencia**
Nadie presume retornos sin evidencia. Si publicas un numero, publicas de donde salio.

**Responsabilidad**
Tu cuenta es tuya. Tus decisiones son tuyas. Aqui se dan metodo y medicion, no ordenes de compra.
""",

"""## Reglas del servidor

**01** Prohibido pedir o dar senales fuera de {c[ice-vader]}. Este no es un canal de senales.
**02** Prohibido publicar resultados sin captura o sin registro que los respalde.
**03** Prohibido promocionar fondeadoras, brokers, cursos, grupos o referidos ajenos.
**04** Prohibido el MD comercial a otros miembros. Se expulsa sin aviso.
**05** Prohibido pedir consejo de inversion personalizado. Nadie aqui lo va a dar.
**06** Se discute el proceso, no el pronostico. "Va a subir" no es una aportacion.
**07** Respeto en todo momento. Se puede desarmar una idea sin desarmar a la persona.

## Advertencia

Operar futuros implica **riesgo de perdida sustancial**, incluida la perdida total del capital. El desempeno pasado no garantiza resultados futuros. Nada de lo publicado en este servidor es asesoria de inversion.

Al permanecer en este servidor aceptas este codigo."""],


"anuncios": ["""# ANUNCIOS

Canal de una sola via. Aqui se publica lo que cambia en la firma:

- aperturas y cierres de acceso al {c[bootcamp]}
- cambios en el protocolo de la mesa
- nuevas versiones de ICE VADER
- nuevos agentes del {c[agentes-ia]}
- mantenimiento del Terminal

Actívalo con la campana. Es el unico canal que vas a necesitar seguir."""],


"filosofia": ["""# FILOSOFIA

Northpoint no es un fondo de inversion tradicional. Es una institucion construida sobre **inteligencia conductual aplicada a los mercados financieros**.

La tesis es simple y es incomoda: el conocimiento tecnico dejo de ser el cuello de botella hace anos. Cualquiera tiene acceso al mismo grafico, a los mismos datos y a la misma teoria. Lo que separa al operador que sobrevive del que no es **como se comporta bajo presion, con dinero adentro y con el reloj corriendo**.

Eso se puede medir. Y lo que se mide, se corrige.
""",

"""## Los seis pilares

**01 · Precision sobre volumen**
Menos operaciones, mejor seleccionadas. La actividad no es rendimiento.

**02 · Disciplina conductual**
El protocolo por encima del impulso. Siempre, no cuando conviene.

**03 · Evidencia empirica**
Ninguna regla entra al sistema sin datos que la sostengan. Si no se midio, no existe.

**04 · Control del riesgo primero**
La primera pregunta nunca es cuanto se puede ganar. Es cuanto se puede perder.

**05 · Institucionalidad silenciosa**
El trabajo se nota en los numeros, no en el ruido.

**06 · Mejora continua de procesos**
El proceso se revisa, se mide y se corrige. Permanentemente.
""",

"""## Lo que Northpoint NO es

**No es trading de alta frecuencia.** No competimos por microsegundos.
**No es asesoria masiva.** Nadie va a decirte que comprar.
**No promete retornos.** Cualquiera que te garantice un rendimiento te esta mintiendo.
**No opera por intuicion.** Si una decision no se puede explicar, no se ejecuta.

-# Si buscas alguien que te diga cuando entrar, este no es el lugar."""],


"northpoint-score": ["""# NORTHPOINT SCORE
### Sistema propietario · 0 a 1000

El Score es la medicion conductual de un operador. No mide cuanto ganaste. Mide **como te comportaste**.

Un mes verde con Score bajo es una advertencia: ganaste rompiendo tu propio protocolo, y eso no se repite.
Un mes rojo con Score alto es informacion util: hiciste lo correcto y el mercado no pago. Eso si se repite.
""",

"""## Las cuatro dimensiones

Cada una vale **250 puntos**. Suman 1000.

**RISK DISCIPLINE** · 250
Tamano de posicion respecto al plan. Stop respetado o movido. Riesgo por operacion y riesgo del dia.

**EMOTION CONTROL** · 250
Revancha despues de una perdida. Entradas fuera de ventana. Operaciones no planeadas. Tiempo entre la senal y el click.

**DECISION QUALITY** · 250
La entrada cumplia el setup completo o solo una parte. Se documento antes o se justifico despues.

**CONSISTENCY** · 250
Cuantos dias seguidos se siguio el protocolo. La varianza de tu propia conducta.
""",

"""## Como se usa

El Score vive en el Terminal y se actualiza con cada operacion que registras en {c[el-journal]}.

Los agentes de {c[agentes-ia]} leen tu registro y te devuelven **donde perdiste puntos y por que**. No en general: en la operacion, con la hora.

Publica tu Score en {c[progreso]} cuando quieras. Es la unica cifra que aqui vale la pena presumir.

-# El Score no es un juego. Es el unico numero que predice si vas a seguir aqui en seis meses."""],


"la-mesa": ["""# LA MESA DE FUTUROS

> **90 minutos al dia. Un protocolo cerrado. Maximo dos operaciones.**

Esa frase es la operacion completa. Todo lo demas es detalle.
""",

"""## La ventana

La mesa abre con Nueva York y cierra 90 minutos despues. Fuera de esa ventana no se opera. No porque el mercado no se mueva, sino porque **la disciplina de horario es la mas barata de todas** y la que mas cuentas salva.

Antes de la apertura ya estan definidos: instrumento, riesgo del dia, tamano y los dos escenarios posibles. Durante la sesion no se improvisa nada.

## El limite de dos

Maximo **dos operaciones** por dia. No es una sugerencia.

La tercera operacion de un dia casi nunca es una oportunidad: es una reaccion. El limite existe para que la revancha sea imposible por diseno, no por fuerza de voluntad.

## La regla de la senal

No se entra sin la alerta de **ICE VADER**. Sin senal publicada en {c[ice-vader]}, entrar esta prohibido.

Esto elimina de raiz la peor operacion de todas: la que se justifica sola despues de verla."""],


"proceso": ["""# EL PROCESO DE DECISION

Cinco pasos. Toda operacion pasa por los cinco, en orden. Si uno falla, no hay operacion.

**01 · Contexto**
Que dejaron Asia y Londres. Que liquidez quedo sin tomar. Donde esta el rango.

**02 · Hipotesis**
Una sola idea, escrita antes de que abra el mercado. Con su invalidacion.

**03 · Riesgo**
Cuanto se pierde si esto sale mal. El numero se define antes que el objetivo, nunca despues.

**04 · Ejecucion**
Solo con senal. Entrada, stop y objetivo definidos en el mismo momento. Sin ajustes en caliente.

**05 · Revision**
La operacion se registra en {c[el-journal]} el mismo dia. Ganada o perdida. Sin excepcion.

-# El paso 5 es el que casi todos se saltan. Es el unico que produce mejora."""],


"bootcamp": ["""# EL BOOTCAMP

El metodo completo de Northpoint, en el orden en que se debe aprender.

No es un curso de indicadores. Es la construccion de un operador con protocolo: contexto de sesiones, apertura de rango, gestion de riesgo por porcentaje, y sobre todo **la mecanica conductual que hace que el plan sobreviva al primer dia rojo**.
""",

"""## Que incluye

- Los seis modulos completos (ver {c[plan-de-estudio]})
- El indicador **ICE VADER** configurado y explicado, no solo entregado
- Acceso al **Terminal**: sesion, journal, aprobaciones y tu Northpoint Score en vivo
- Los **agentes de revision** sobre tus propias operaciones
- Las senales en vivo en {c[ice-vader]}
- Revision de tu journal dentro de la comunidad

**Duracion:** [PENDIENTE]
**Precio:** [PENDIENTE]
**Cupo:** [PENDIENTE]

Detalles de acceso en {c[productos-y-acceso]}. Dudas del material en {c[dudas-del-curso]}.
""",

"""## Lo que no incluye

No incluye una cuenta fondeada. No incluye senales fuera del protocolo. No incluye promesa de rentabilidad.

Incluye un metodo, una medicion y un lugar donde te van a decir la verdad sobre como estas operando.

-# Operar futuros implica riesgo de perdida sustancial. Nada aqui es asesoria de inversion."""],


"plan-de-estudio": ["""# PLAN DE ESTUDIO
### Seis modulos. En orden. No se saltan.

**MODULO 01 · El mercado que vas a operar**
Futuros, contratos, micros y minis. Valor del punto. Margen y horarios. Por que MNQ y no otra cosa.

**MODULO 02 · Contexto de sesiones**
Asia, Londres y Nueva York. Liquidez tomada y sin tomar. Como leer lo que dejo la noche antes de que abra tu ventana.

**MODULO 03 · El rango de apertura**
El ORB de los primeros 15 minutos. Que es un break real y que es ruido. El retest. El FVG. Donde vive el stop y por que ahi.

**MODULO 04 · Riesgo antes que objetivo**
Riesgo por operacion como porcentaje. Tamano calculado, no elegido. El riesgo del dia. Cuando la respuesta correcta es no operar.

**MODULO 05 · Conducta bajo presion**
Las cuatro dimensiones del Score. Los patrones de fuga: revancha, adelanto de entrada, mover el stop, la tercera operacion.

**MODULO 06 · El sistema completo**
Rutina de 90 minutos de principio a fin. El journal como parte de la operacion, no como tarea. Como se lee un mes.

-# Cada modulo cierra con una revision de tu propio registro. No hay examen; hay evidencia."""],


"biblioteca": ["""# BIBLIOTECA

Material de referencia. Se agrega poco y solo lo que se uso de verdad.

**Conducta y decision**
Trabajo sobre sesgos, aversion a la perdida y toma de decisiones bajo incertidumbre. Es la base teorica del Score.

**Estructura de mercado**
Sesiones, liquidez, subasta y apertura de rango.

**Riesgo y tamano**
Riesgo fijo por operacion, ruina y varianza. Por que el tamano se calcula y no se siente.

**Documentos internos**
Protocolo de la mesa · Codigo de conducta · Especificacion del Score

-# Si algo entra a esta biblioteca es porque cambio la forma de operar de alguien. No por llenar."""],


"dudas-del-curso": ["""# DUDAS DEL CURSO

Aqui se preguntan cosas del material. Una duda por mensaje.

**Como preguntar bien**
Modulo y minuto o leccion. Que intentaste. Que esperabas y que paso. Captura si aplica.

**Que no va aqui**
- "Entro largo?" → no es una duda del curso
- Opiniones sobre el mercado de hoy → {c[general]}
- Fallas del Terminal o de la senal → {c[el-journal]} o {c[ice-vader]}

-# Toda duda respondida aqui queda para el siguiente que llegue. Por eso no se responden por privado."""],


"el-journal": ["""# EL JOURNAL

El journal no es una libreta. Es el instrumento de medicion de la firma.

Sin registro no hay Score. Sin Score no hay correccion. Sin correccion, un ano de operar es el mismo mes repetido doce veces.
""",

"""## Que se registra

Por cada operacion:

```
Fecha y hora        Instrumento      Direccion
Entrada  Stop  Objetivo             Contratos
Riesgo en $         Resultado en $   R obtenida
Cumplia el setup completo?          Si / No
Se movio el stop?                   Si / No
Estaba dentro de la ventana?        Si / No
Que senti antes de entrar
Que haria distinto
```

Las tres preguntas de Si/No son las que alimentan el Score. Son tambien las tres que dan pena contestar con la verdad. Contestalas con la verdad.
""",

"""## Reglas del journal

**Se registra el mismo dia.** Un journal escrito el domingo es ficcion.
**Se registra la perdida igual que la ganancia.** El sesgo de solo anotar lo bueno destruye el dato.
**No se edita despues.** Se agrega una nota, no se corrige la historia.

Los agentes de {c[agentes-ia]} leen esto. Lo que escribas aqui es lo que te van a devolver."""],


"agentes-ia": ["""# LOS AGENTES

Revision automatica de tu operacion. No opinan del mercado: opinan de ti.
""",

"""## Que hace cada uno

**ANALISTA DE SESION**
Lee tu jornada completa y la compara contra el protocolo. Devuelve donde te saliste y en que minuto.

**AUDITOR DE RIESGO**
Revisa tamano, stop y riesgo del dia. Detecta la operacion en la que arriesgaste mas de lo que dijiste que ibas a arriesgar.

**LECTOR DE CONDUCTA**
Cruza lo que escribiste en {c[el-journal]} contra lo que hiciste. Es el que encuentra la revancha antes de que se vuelva costumbre.

**REVISOR DEL SCORE**
Explica el movimiento de tus cuatro dimensiones. Que subio, que bajo y por cual operacion.
""",

"""## Como leerlos

Un agente no aprueba ni reprueba. Senala.

Si el informe dice que moviste el stop dos veces este mes, eso no es una acusacion: es un dato. Lo unico que importa es si el mes que viene son cero.

-# Los agentes trabajan sobre lo que registras. Journal incompleto, informe inutil."""],


"aprobaciones": ["""# MESA DE APROBACIONES

Nada se ejecuta fuera del protocolo sin pasar por aqui.

Si una operacion no cumple los cinco pasos de {c[proceso]}, tiene dos caminos: no se hace, o se somete a aprobacion **antes** de ejecutarse. Nunca despues.
""",

"""## Formato de solicitud

```
INSTRUMENTO
DIRECCION
ENTRADA / STOP / OBJETIVO
RIESGO EN $ Y EN %
QUE PASO DEL PROTOCOLO NO SE CUMPLE
POR QUE DEBERIA HACERSE DE TODAS FORMAS
```

**Aprobada** — se ejecuta y se registra marcada como excepcion.
**Rechazada** — no se ejecuta. Se registra la solicitud igual.

## Por que existe

Porque el 90% de las excepciones mueren solas en el momento en que hay que escribirlas. El formato es el filtro.

-# Ejecutar primero y pedir aprobacion despues cuenta como operacion fuera de protocolo."""],


"ice-vader": ["""# ICE VADER
### Senal automatica de la mesa

Este canal lo escribe el indicador. **No se conversa aqui.**

## Que vas a ver

```
INICIO DE ASIA        apertura de la sesion asiatica
CIERRE DE ASIA        high, low y si fue alcista o bajista
INICIO DE LONDRES     apertura de la sesion europea
CIERRE DE LONDRES     high, low y sesgo
INICIO DE NUEVA YORK  abre la ventana de la mesa
INICIO DEL ORB        arranca el rango de apertura
FORMACION DEL ORB     rango cerrado: high, low y amplitud
BREAK DEL ORB         cierre confirmado fuera del rango
RETEST DEL ORB        el precio regreso al nivel de la orden
ENTRADA               precio, stop, objetivo, R, contratos y riesgo en $
RESULTADO             como cerro la operacion
```

## La regla

> Sin alerta de ICE VADER publicada en este canal, entrar al trade esta prohibido.

No es una recomendacion del servidor. Es la regla de la mesa.

-# La senal no es una orden de compra. Es la condicion minima para que una operacion sea legitima."""],


"bitacora-del-dia": ["""# BITACORA DEL DIA

Una linea por dia. Lo que hizo la mesa.

**Formato**
```
FECHA · sesgo de Asia y Londres · amplitud del ORB
operaciones tomadas · resultado en R · Score del dia
una linea de que se aprendio
```

Sin analisis largo, sin justificaciones. La bitacora es memoria, no ensayo.

-# Al final del mes esta bitacora vale mas que cualquier captura de una cuenta verde."""],


"productos-y-acceso": ["""# ACCESO A NORTHPOINT

Tres cosas se venden. Se pueden tomar por separado, pero estan disenadas para funcionar juntas.
""",

"""## 01 · EL BOOTCAMP
El metodo completo, los seis modulos, ICE VADER configurado y la comunidad.
**Precio:** [PENDIENTE] · **Duracion:** [PENDIENTE] · **Cupo:** [PENDIENTE]

## 02 · EL TERMINAL
Sesion, journal, aprobaciones y tu Northpoint Score en vivo. La herramienta con la que se opera todos los dias.
**Precio:** [PENDIENTE] al mes

## 03 · LOS AGENTES
Los cuatro agentes de revision sobre tu propio registro.
**Precio:** [PENDIENTE] al mes

**PAQUETE COMPLETO** — los tres, [PENDIENTE].
""",

"""## Como entrar

**1.** Presentate en {c[presentate]}.
**2.** Escribe en {c[preguntas]} lo que necesites resolver antes de decidir.
**3.** Cuando estes listo, [PENDIENTE: enlace de pago o formulario].

## Antes de pagar, lee esto

Northpoint **no garantiza rentabilidad**. No existe ningun producto aqui que asegure que vas a ganar dinero. Operar futuros implica riesgo de perdida sustancial, incluida la perdida total del capital depositado.

Lo que si se entrega: un metodo escrito, una herramienta de medicion y una revision honesta de como operas.

Si lo que buscas es una senal que te haga rentable sin cambiar tu conducta, no compres. No lo vendemos."""],


"preguntas": ["""# PREGUNTAS FRECUENTES

**Esto es un grupo de senales?**
No. ICE VADER publica eventos de la sesion, pero la senal sin protocolo no sirve de nada. Lo que se ensena es el protocolo.

**Necesito cuenta fondeada?**
No para el bootcamp. Se puede recorrer completo en simulado, y es lo recomendado hasta que el Score sea estable.

**Cuanto capital necesito?**
Depende del instrumento y de la fondeadora. Lo que Northpoint fija no es el capital: es el **riesgo por operacion como porcentaje**, que funciona igual en 5,000 que en 100,000.

**Cuanto tiempo al dia?**
90 minutos de mercado mas el registro. Fuera de eso no se opera.

**Puedo aplicar esto a otro instrumento?**
El protocolo si. Los parametros de ICE VADER estan medidos sobre MNQ; en otro instrumento hay que volver a medirlos, no suponerlos.

**Van a manejar mi dinero?**
No. Aqui no se administra capital de terceros ni se dan recomendaciones personalizadas.

**Me garantizan resultados?**
No. Nadie serio lo hace. Lo que se garantiza es el metodo, la medicion y la honestidad del informe.

**En que idioma?**
Espanol.

-# Falta tu pregunta? Escribela aqui abajo."""],


"presentate": ["""# PRESENTATE

Un mensaje. Cuatro lineas.

```
NOMBRE O ALIAS
QUE OPERAS         (instrumento y temporalidad)
DESDE CUANDO
QUE TE TRAE AQUI   (una frase, la verdadera)
```

No hace falta que digas cuanto ganas. Nadie lo va a preguntar y a nadie le sirve.

-# Los que escriben "que te trae aqui" con honestidad son los que terminan el bootcamp."""],


"progreso": ["""# PROGRESO

Aqui se publica evidencia, no opiniones.

**Que si va**
- Tu Northpoint Score y su movimiento del mes
- Racha de dias siguiendo el protocolo
- Resultado en **R**, no en pesos
- Una captura del journal

**Que no va**
- Capturas de cuentas sin registro que las respalde
- Cifras en dinero sin contexto de riesgo
- Resultados de un solo dia presentados como sistema

Un mes rojo con Score alto se publica igual que uno verde. **Eso es lo que aqui se aplaude.**

-# La cuenta de alguien mas no es tu referencia. Tu mes pasado si."""],


"general": ["""Bienvenido a {c[general]}.

Conversacion abierta: proceso, herramientas, rutina, lo que estas leyendo.

Antes de escribir, dos recordatorios de {c[codigo-de-conducta]}:
se discute el proceso, no el pronostico; y no se piden ni se dan senales fuera de {c[ice-vader]}.

Si es duda del curso, va en {c[dudas-del-curso]}. Si es resultado, va en {c[progreso]}."""],

}

# Canales que se dejan como solo-lectura para @everyone (el bot y los admins si escriben)
SOLO_LECTURA = [
    "bienvenida", "codigo-de-conducta", "anuncios", "filosofia", "northpoint-score",
    "la-mesa", "proceso", "bootcamp", "plan-de-estudio", "biblioteca",
    "el-journal", "agentes-ia", "ice-vader", "productos-y-acceso",
]

# Mensajes que se fijan (el primero de cada uno de estos canales)
FIJAR = ["bienvenida", "codigo-de-conducta", "northpoint-score", "la-mesa",
         "ice-vader", "productos-y-acceso", "el-journal"]
