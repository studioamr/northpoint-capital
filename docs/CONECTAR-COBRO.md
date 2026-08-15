# Conectar el cobro · Stripe y MercadoPago

La sección de compra ya está en la landing con el precio de **$17,000 MXN**.
Los botones están **desactivados a propósito** y dicen «abre en unos días»
hasta que existan las cuentas. Cuando las tengas, esto son dos líneas.

---

## Por qué las dos

| | Stripe | MercadoPago |
|---|---|---|
| Tarjeta internacional | ✅ | limitado |
| OXXO en efectivo | ✗ | ✅ |
| SPEI / transferencia | ✗ | ✅ |
| Meses sin intereses | ✗ en MX | ✅ |
| Comisión aprox. | 3.6% + $3 | 3.5% + IVA |

En México, **cerca de la mitad de la gente paga en OXXO o por transferencia**.
Si sólo pones tarjeta, dejas fuera a esa mitad. Y si sólo pones MercadoPago,
dejas fuera al que te compra desde Estados Unidos, que es a donde apunta la
firma. Por eso van las dos.

---

## Paso 1 · Stripe

1. Crea la cuenta en [dashboard.stripe.com/register](https://dashboard.stripe.com/register)
   — necesitas RFC y una cuenta bancaria mexicana.
2. Te van a pedir la **URL del negocio**: `https://northpointcapital.io`
3. Y los **términos y la política de reembolso**. Ya están publicados:
   - `https://northpointcapital.io/legal/terminos.html`
   - `https://northpointcapital.io/legal/privacidad.html`
4. En el panel: **Payment links → New** → producto «Bootcamp NORTHPOINT»,
   precio **17000 MXN**, pago único.
5. Copia el enlace que te da (se ve como `https://buy.stripe.com/xxxx`).

## Paso 2 · MercadoPago

1. Entra a [mercadopago.com.mx](https://www.mercadopago.com.mx) con tu cuenta.
2. **Vender → Link de pago → Crear link**.
3. Producto «Bootcamp NORTHPOINT», **$17,000 MXN**, cantidad 1.
4. Activa **OXXO**, **SPEI** y **meses sin intereses** si los quieres ofrecer.
5. Copia el enlace (`https://mpago.la/xxxx`).

## Paso 3 · La página de después del pago

Antes de copiar los enlaces, en cada uno pon a dónde llega el que ya pagó:

- **Stripe** → el payment link → *After payment* → **Redirect to a page**
- **MercadoPago** → el link de pago → **URL de retorno** → *Pago aprobado*

En los dos va la misma:

```
https://northpointcapital.io/gracias.html
```

Esa página ya existe y ya está escrita: le da al que acabó de pagar los cuatro
pasos para arrancar el mismo día (correo, Terminal, Discord, la apertura de las
8:30). **Si no la configuras, el que paga se queda mirando el recibo de Stripe** y
nadie le dice qué sigue — que es justo el minuto en el que más ganas tiene de
empezar y el más caro de desperdiciar.

Lleva `noindex`, así que no aparece en Google ni se la encuentra quien no pagó.

## Paso 4 · Pegar los enlaces

En `index.html`, busca `var PAGO = {` y pon los enlaces:

```js
var PAGO = {
  stripeMensual: 'https://buy.stripe.com/...',   // SUSCRIPCIÓN mensual $1,490
  stripeAnual:   'https://buy.stripe.com/...',   // pago único $11,900
  mpAnual:       'https://mpago.la/...',         // MercadoPago $11,900
  stripeVida:    'https://buy.stripe.com/...',   // pago único $17,000
  mpVida:        'https://mpago.la/...'          // MercadoPago $17,000
};
```

Con eso los botones se activan solos. **Si dejas uno vacío, ese botón se queda
desactivado y los demás funcionan** — así puedes lanzar con el anual primero y
agregar los otros después.

> ⚠️ **El mensual es una SUSCRIPCIÓN, no un pago único.** En Stripe se crea con
> *Product → Recurring → Monthly*, no con un Payment Link normal. Si lo creas
> como pago único, cobras una sola vez y el acceso queda abierto para siempre a
> $1,490. MercadoPago también maneja suscripciones, pero su flujo es más
> engorroso: por eso el mensual va sólo por Stripe.

---

## Los tres planes y por qué esos precios

| Plan | Precio | Equivale a | Qué suma |
|---|---|---|---|
| Mensual | $1,490/mes | — | La puerta de entrada |
| **Un año** | **$11,900** | $992/mes | 4 meses de regalo · 1 sesión 1a1 |
| De por vida | $17,000 | pago único | Actualizaciones · 3 sesiones · prioridad |

El razonamiento, para que no se toque a la ligera:

- **El mensual a doce meses cuesta $17,880 — más que el de por vida.** Es a
  propósito. El mensual existe para que entren, no para que se queden ahí.
- **El anual es el ancla** y el que más se va a vender: cuatro meses de regalo
  contra el mensual. Por eso lleva la marca de «el más elegido».
- **El de por vida son sólo $5,100 más que el anual.** Ese contraste es lo que
  lo hace ver razonable. Sin el anual en medio, $17,000 sueltos parecen mucho.

Lo que sube con el plan **no es el contenido** —los tres traen los 8 módulos, el
Terminal y el Discord— sino el compromiso de André: sesiones uno a uno y
prioridad en el Programa. Retener contenido genera rencor en quien paga menos;
dar más acceso a la persona, no.

## Antes de la primera venta

- [ ] **El correo `hola@northpointcapital.io`** debe existir: está en los tres
      documentos legales y en el pie. Con un redirect a tu Gmail basta para
      empezar.
- [ ] **Prueba una compra de verdad** con tu propia tarjeta y luego reembólsala.
      Es la única forma de saber que el flujo completo funciona.
- [ ] **Decide qué pasa después del pago.** Hoy nadie recibe nada
      automáticamente: tienes que mandar el acceso al Discord y al Terminal a
      mano. Con pocas ventas se aguanta; a partir de diez al mes se vuelve un
      problema.
- [ ] **Factura.** Si vas a facturar, el CFDI se emite aparte — ni Stripe ni
      MercadoPago lo hacen solos en México.

---

## Lo que todavía no existe y hay que resolver

**La entrega es manual.** Alguien paga y no pasa nada automático: no le llega el
video, ni la invitación al Discord, ni el acceso al Terminal. Eso lo mandas tú.

Es aceptable para las primeras ventas —y hasta conviene, porque hablas con cada
comprador—, pero es lo siguiente que hay que automatizar. El camino natural es un
webhook de la pasarela que dé de alta al comprador en `mesa_socios` de Supabase,
igual que ya funciona el alta del Terminal.

---

# Estado real de Stripe (15-ago-2026)

Entré a la cuenta y dejé **los tres enlaces armados en el entorno de prueba**.
Sirven para ver el flujo completo y como plantilla exacta; **no cobran dinero
real** (llevan `test_` en la URL, y así se distinguen de un vistazo).

| Plan | Tipo | Precio | Enlace de PRUEBA |
|---|---|---|---|
| Mensual | **Suscripción mensual** | $1,490 MXN | `https://buy.stripe.com/test_eVqcN4clYc9Df4adLzcMM01` |
| Un año | Pago único | $11,900 MXN | `https://buy.stripe.com/test_8x228qeu63D73lsePDcMM00` |
| De por vida | Pago único | $17,000 MXN | `https://buy.stripe.com/test_bJedR8fyaehL9JQ0YNcMM02` |

Los tres ya llevan **Después del pago → No mostrar la página de confirmación →
`https://northpointcapital.io/gracias.html`**, que es la pieza que casi nadie
configura y sin la cual la página de gracias no sirve de nada.

## Lo que falta, y por qué no lo puedo hacer yo

**La cuenta activa no está habilitada.** Al cambiar de «Entorno de prueba» a
«cuenta activa», Stripe abre el formulario de activación y pide **nombre legal,
fecha de nacimiento, domicilio particular y cuenta bancaria**. Eso es identidad
y datos bancarios: lo teclea André, no yo. Sin ese paso no existe ningún enlace
que cobre dinero real.

Cuando esté activada, los tres se rehacen en modo activo con la tabla de arriba
—los productos de prueba **no se copian solos al modo activo**, es a mano— y los
enlaces `https://buy.stripe.com/…` (ya sin `test_`) se pegan en `var PAGO` de
index.html.

## ⚠️ El checkout dice «0 to hero», no NORTHPOINT

La cuenta de Stripe se llama **0 to hero** y ese nombre es el que aparece
**arriba de la página de pago** y en el estado de cuenta del cliente. Alguien que
paga $17,000 por NORTHPOINT y ve otro nombre en la pantalla de cobro duda — y esa
duda es exactamente de donde salen los contracargos.

Se arregla en *Configuración → Empresa → Datos públicos* (nombre público y
descriptor del extracto). **No lo cambié yo a propósito:** si esa misma cuenta
cobra también «De Cero a Payout», el cambio afecta a los dos productos y ésa es
decisión de negocio, no de código.

## Actualización · la activación quedó a DOS campos

Entré al formulario y llené todo lo que se puede llenar sin ser André:

| Sección | Estado |
|---|---|
| Tipo de empresa | ✅ ya estaba |
| Datos de la empresa · sitio web `northpointcapital.io` | ✅ |
| **Productos o servicios** | ✅ «Otros servicios educativos» + descripción |
| Datos públicos · teléfono de soporte | ✅ |
| **Cargo en el extracto bancario: `NORTHPOINT`** | ✅ ya estaba |
| Representante · nombre, fecha de nacimiento, RFC, teléfono | ✅ ya estaba |
| Representante · **domicilio** | ✅ Pablo Casals 36, 58290 Morelia, Mich. |
| Autenticación en dos pasos | ✅ activada |

**Falta exactamente esto, y son los dos únicos campos que no puedo tocar:**

1. **La colonia (Barrio) del domicilio.** El CP 58290 da seis opciones y no se
   adivina un domicilio en una verificación de identidad: BOSQUE CAMELINAS ·
   CAMELINAS · CAMELINAS INFONAVIT · COMISIÓN FEDERAL DE ELECTRICIDAD ·
   ELECTRICISTAS · LA LOMA.
2. **La CLABE** de la cuenta donde Stripe deposita.

Con esos dos, «Revisar y enviar» se destraba.

**Sobre la categoría elegida:** «Otros servicios educativos», no «Servicios
financieros». Es lo honesto y además lo que menos fricción genera: lo que se
vende es un programa educativo y el sitio dice explícitamente que no se dan
señales, no se administra dinero de terceros y no se ofrece asesoría de
inversión. Declararlo como servicio financiero habría invitado una revisión que
no corresponde a lo que se cobra.

**Lo que NO toqué a propósito:** los complementos de pago (Radar Standard a
MXN 0.95 por transacción ya venía activado, Cálculo de impuestos y Climate
desactivados). Son costos por transacción, y comprometerte a un cobro recurrente
no me toca.
