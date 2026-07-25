# Auditoría del Gabinete IA · julio 2026

Tres auditores independientes revisaron la idea antes de conectarle una llave de IA:
uno cuantitativo, uno de cumplimiento y riesgo, uno de producto. Convergieron en la
misma conclusión, así que vale la pena escribirla sin adornos.

---

## El veredicto

> **Siete agentes de IA no van a predecir la dirección del NQ. Y fingir que sí es el
> modo de falla más caro, porque fabrica un trade convincente todos los días.**

La buena noticia es que el sistema sí sirve — con la dirección invertida. El gabinete
no debe tener permiso de decir COMPRA. Sólo de decir NO.

---

## Lo que no iba a funcionar

**La predicción.** No hay evidencia de LLMs prediciendo dirección intradía de índices
líquidos. Peor: el modelo fue entrenado con datos que ya contienen el futuro del NQ,
así que cualquier «backtest conversacional» está contaminado. La apertura del NQ es
donde compiten los actores mejor capitalizados del mundo; no es el mercado donde un
panel de chat encuentra ventaja.

**El 65% de aciertos es una suposición, no una medición.** Con comisiones y
deslizamiento, el punto de equilibrio real está en **~54%**, no en 50%. La distancia
entre 54% y 65% es toda la tesis del plan — y para distinguirlas estadísticamente
hacen falta **100+ trades**. La evaluación da unos 30. No se puede validar el sistema
con el sistema.

**El copiador ×5 no diversifica: apalanca.** No son cinco intentos, es un intento con
cinco veces el costo. Cinco pérdidas seguidas se comen el drawdown, y a 55% de
aciertos la probabilidad de una racha así en 40 trades pasa del 70%. Las cinco cuentas
mueren el mismo día, por la misma decisión.

**La deliberación era una opinión con siete voces.** Siete prompts sobre el mismo
modelo base tienen errores correlacionados: si el modelo base se equivoca, los siete se
equivocan igual. El debate multiagente mejora tareas con verdad verificable
—matemáticas, código—; aquí no hay verdad verificable al momento de decidir.

**Los sliders eran placebo.** Escribían un número que nadie leía. Un usuario listo lo
detecta en dos minutos y entonces desconfía de todo lo demás — incluido lo que sí es
real. Ésa era la pérdida grande.

---

## Dónde sí estaba el valor

Y esto ya estaba medido en la simulación de julio, sólo que no lo habíamos usado:

| Día | Qué pasó | Causa real |
|---|---|---|
| 1 jul | −$1,004 y **violación de riesgo** | Aritmética: dos stops de $500 no caben en un tope de $1,000 |
| 13 jul | −$992, sin violación | El ajuste de tamaño lo salvó por $8 |
| 7 jul | **No se operó** — el día más rentable del mes | Disciplina |
| Todo el mes | 16 días en vez de 3-5 | Expectativa mal calculada |

**Ninguno fue un error de predicción.** Todos fueron dimensionamiento, disciplina o
expectativas. Ahí es donde un gabinete sí puede ganar dinero — evitando que se pierda.

---

## Lo que se construyó

El gabinete dejó de proponer entradas. Ahora **calcula si puedes operar, con qué
tamaño, y cuándo tienes que parar**. Todo es aritmética determinista sobre las reglas
verificadas y tus propios trades: cero opinión, cero modelo.

### PRE-VUELO

Lo primero que ves cada mañana. Cuatro números y un veredicto:

- **Tope del día** — la regla de la casa, apretada por la severidad de DIQUE.
- **Te resta** — lo que queda después de lo ya perdido hoy.
- **Riesgo por trade** — calculado para que **dos stops quepan en el tope**, con 6% de
  margen de deslizamiento. La falla del 1 de julio quedó estructuralmente imposible.
- **Trades de hoy** — sobre el máximo de 2.

Y el veredicto: **PUEDES OPERAR · MEDIO TAMAÑO · MESA CERRADA**, con todos los motivos
listados, no sólo el primero.

Vetos que calcula (no opina):

| Quién | Veta cuando |
|---|---|
| YUNQUE | Fin de semana · fuera de la ventana 7:00–8:30 · ya van 2 trades · el primero ganó |
| DIQUE | Riesgo del día agotado · no cabe un trade completo · una cuenta está más cerca del corte que el riesgo de un trade |
| DIQUE | La ganancia del día rompe el tope de consistencia del 40% |

### Los sliders ahora son reales

Ésta era la prueba que exigió la auditoría: *si mueves una perilla y el número no se
mueve, la perilla se borra.* Medido:

| Severidad | Tope del día | Riesgo/trade | Dos stops | ¿Caben? |
|---|---|---|---|---|
| 0 | $1,000 | $357 | $714 | sí |
| 50 | $750 | $268 | $536 | sí |
| 75 | $625 | $223 | $446 | sí |
| 100 | $500 | $179 | $358 | sí |

| Apetito (sev. 75) | Riesgo/trade |
|---|---|
| 0 | $176 |
| 40 | $223 |
| 100 | $294 |

Monótono, verificable a mano, y **en todos los casos dos stops caben en el tope**.

### ÁBACO dice la verdad sobre tu muestra

Corre estadística sobre **tus** trades, no sobre un backtest genérico: aciertos reales,
esperanza por trade, y el punto de equilibrio calculado con tu propia relación
ganancia/pérdida. Y si tienes menos de 30 trades, lo dice: *«muestra insuficiente para
concluir nada»*. No inventa confianza que no existe.

---

## Lo que falta, en orden

1. **Registro de avisos con motivo de rechazo.** Cada veto se guarda con si lo acataste
   y por qué no. Sin eso no se puede medir nada.
2. **El marcador «costo de ignorar al gabinete»**, en dólares. Si sale negativo, el
   gabinete se apaga — eso también es información honesta.
3. **La oficina como estado, no como adorno.** Que DIQUE se pare y se ponga rojo cuando
   quedan menos de $200 de tope; que las sillas estén vacías fuera de la ventana. Si el
   canvas se ve igual con las cuentas sanas que a un trade del corte, es fondo de
   pantalla.
4. **La llave de IA, sólo al final, y sólo para redactar.** El modelo narra en prosa lo
   que los cálculos ya decidieron. Escribe; nunca decide.

---

## Lo que hay que verificar afuera (no lo puede resolver el software)

- **Preguntar a Tradeify por escrito** si una señal generada por IA que tú ejecutas a
  mano es aceptable, si el copiador entre tus cuentas está permitido, y qué evidencia
  piden en el payout. Guardar el correo con fecha. La zona gris es donde niegan pagos.
- **Sacar del panel de Tradeify los números reales de tu plan** (objetivo, tipo de
  drawdown, piso congelado, días mínimos, tope de contratos). El catálogo del terminal
  se leyó una vez en julio de 2026; el contrato manda sobre cualquier catálogo.
- **Conseguir datos en vivo.** El terminal usa precios de Yahoo con retraso, refrescados
  cada 20 minutos. Sirven para contexto, **no para decidir un stop intradía**.

---

## La línea roja

**Ningún agente toca el botón de ejecutar. Nunca.** Sin API de broker, sin webhooks. Los
agentes calculan y escriben; tú operas. Y nunca: subir tamaño para recuperar tiempo
perdido, saltarse el modo papel, ni pedirle al gabinete que interprete las reglas de la
fondeadora — ésas se leen del contrato o se preguntan a soporte.
