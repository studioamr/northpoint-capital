# Simulación de un mes · julio 2026

Se simuló la operación diaria completa con **65% de aciertos a 1:1** y se midió todo con
el motor del propio terminal — las mismas funciones que la app usa en producción para
detectar violaciones, calcular el drawdown, la salud de cada cuenta y el Score.

Ningún número de este documento está escrito a mano.

---

## Cómo se montó

- **5 cuentas** Tradeify Select Evaluation de 50k, replicadas por copiador: una orden
  entra en las cinco. Reglas reales del catálogo verificado: objetivo +$3,000, drawdown
  máximo $2,000, consistencia 40%, mínimo 3 días.
- **17 días hábiles**, del 1 al 23 de julio.
- **Riesgo $500 por cuenta por trade** — la mitad del tope diario de $1,000, para que la
  regla de «máximo 2 trades» tenga sentido.
- Regla de la casa: si el primer trade gana, se para. Si pierde, queda un intento.
- Deslizamiento aleatorio de ±6% en cada llenado, porque los stops nunca salen exactos.
- 12% de probabilidad diaria de que no haya setup válido.

---

## Lo que salió

| | |
|---|---|
| Días hábiles | 17 |
| Días operados | 16 (uno sin setup) |
| Trades | 21 — **14 ganados, 7 perdidos** |
| Aciertos reales | **66.7%** |
| Días verdes / rojos | 11 / 5 |
| Mejor día | +$529 por cuenta |
| Peor día | −$1,004 por cuenta |
| **P&L por cuenta** | **+$3,459** |
| **P&L de la mesa** (×5) | **+$17,295** |
| Balance final por cuenta | **$53,459** |
| Evaluación | **PASADA** el 23 de julio |
| Northpoint Score | 690 / 1000 · «EN DESARROLLO» |

---

## Los tres hallazgos

### 1 · El riesgo por trade estaba mal dimensionado

**El 1 de julio el motor marcó una violación real de riesgo diario.** Dos stops de $500
nominales sumaron $1,004 contra un tope de $1,000. Se pasaron por cuatro dólares.

No fue mala suerte, fue aritmética: **dos trades de medio tope no caben en el tope**
cuando el llenado se desliza. La regla estaba escrita para no poder cumplirse.

La corrección es de una línea: bajar el riesgo por trade a **$460–475 por cuenta** (23
puntos de NQ en vez de 25). Con eso, dos stops completos con deslizamiento del 6% suman
~$975 y caben debajo del tope.

Que esto importa se comprobó solo: **el 13 de julio se repitió el escenario exacto** —dos
pérdidas seguidas— y cerró en −$992. Con el tamaño viejo habría sido la segunda violación
grave del mes.

### 2 · El objetivo diario del plan no es alcanzable con esta estructura

El plan original decía **riesgo diario $1,000, objetivo diario $1,000, evaluación en 3–5
días**. La simulación tardó **16 días**.

No es que el sistema sea lento. Es que la expectativa estaba mal calculada:

```
Esperanza por día y por cuenta, con 65% a 1:1 parando tras la primera ganadora:

  gana la primera        0.65 × (+500)                    = +325
  pierde y luego gana    0.35 × 0.65 × (0)                =    0
  pierde las dos         0.35 × 0.35 × (−1,000)           = −122.5
                                                   ────────────────
                                                    ≈ +$202 por día
```

$3,000 ÷ $202 = **15 días hábiles**. La simulación tardó 16. La cuenta cuadra.

Esto **no es un problema del sistema, es un problema de la meta**. Y es el riesgo más
serio del trimestre que entra: si las cuentas fondeadas se calibran con el plan viejo, la
tentación va a ser subir tamaño para «ponerse al corriente». Ahí es donde se truenan las
cuentas.

**Recomendación:** reescribir el objetivo de payout en días reales — 16 a 20 hábiles, no
5 — para que la meta deje de mentir.

### 3 · La consistencia del 40% nunca estuvo cerca de ser problema

El mejor día del mes fue **+$529** y el tope permitido era **$1,384** (40% de $3,459).
Sobró 62% de margen. Con esta estructura —parar después de la primera ganadora— es
prácticamente imposible violar la consistencia. Una preocupación menos.

---

## Lo que se verificó del terminal

Todo esto lo calculó la app, no yo:

- **Detección de violaciones** — encontró la del 1 de julio sola, la etiquetó
  «RIESGO DIARIO EXCEDIDO» y la dejó marcada en el journal, sin posibilidad de borrarla.
- **Copiador** — cada trade se replicó correctamente en las 5 cuentas: $501 por cuenta
  aparece como $2,505 de mesa.
- **Salud de cuenta** — balance, pico, línea de drawdown y colchón calculados en cada
  una de las cinco.
- **Calendario mensual** — los 17 días hábiles con su P&L, la columna semanal, los días
  vacíos de fin de semana y el día sin operar en blanco.
- **Northpoint Score** — 690, penalizado por la falta grave del día 1.
- **Resumen del mes** — +$17,295, 57.7% de la meta mensual de $30,000, 16/23 días
  operados, 11/16 verdes.

---

## El chat

La coordinación día a día está en [CHAT-JULIO-2026.md](CHAT-JULIO-2026.md): 134 mensajes
entre los cuatro socios, con quién propuso cada tesis, quién firmó, quién se opuso y por
qué.

Los momentos donde se ve el proceso funcionando:

- **1 de julio** — el desastre y la discusión de por qué la regla estaba mal diseñada.
- **3 de julio** — Goyo sugiere un trade y le recuerdan que ésa no es su puerta.
- **7 de julio** — Mateo se niega a firmar, Pablo insiste, Mateo detiene la mesa como
  CRO. **Ese día no se operó y fue la decisión más rentable del mes.**
- **13 de julio** — segundo día de dos pérdidas; Mateo evalúa parar la mesa y decide que
  no, con la razón escrita: «detengo la mesa cuando se rompe el proceso, no cuando se
  rompe el resultado».
- **23 de julio** — el cierre, y la propuesta de Goyo para el trimestre.
