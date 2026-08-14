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

## Paso 3 · Pegarlos

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
