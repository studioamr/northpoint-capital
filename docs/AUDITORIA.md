# Auditoría · qué falta para cobrar el bootcamp

**14 de agosto de 2026.** Revisión de las ocho páginas públicas, el flujo de
cobro, el estado legal y lo técnico. Todo lo que sigue está medido, no supuesto.

---

## El hallazgo de fondo

**Hoy no se puede cobrar nada.** No es un problema de diseño: no existe precio
publicado, ni botón de compra, ni pasarela conectada. El bootcamp se anuncia
—12 módulos, +48 hrs de video— pero no hay forma de que alguien pague.

Y aunque mañana pusieras un botón de Stripe, **te lo rechazarían**: las pasarelas
exigen términos, política de reembolso y aviso de riesgo publicados. El sitio no
tiene ninguno de los tres.

Esos son los dos bloqueos reales. Lo demás de esta lista es acabado.

---

## 🔴 Bloquea el cobro — sin esto no hay negocio

### 1 · No hay precio ni checkout
El bootcamp no dice cuánto cuesta ni cómo se paga. Los `$` que aparecen en la
página son ejemplos de trading, no precios.

**Qué hace falta:** decidir el precio, y conectar cobro. Para México y pagos
internacionales, **Stripe** es lo más limpio (acepta tarjeta extranjera y
maneja impuestos). **MercadoPago** si quieres OXXO y SPEI, que en México pesa.

### 2 · Cero páginas legales
| Documento | Estado |
|---|---|
| Términos y condiciones | ✗ no existe |
| Aviso de privacidad | ✗ no existe |
| Política de reembolso | ✗ no existe |
| Aviso de riesgo | ✗ no existe |

Los tres primeros los **exige la pasarela** para aprobarte. El cuarto te protege
a ti: vendes formación sobre futuros apalancados, y sin un descargo visible te
quedas expuesto si alguien pierde dinero y reclama.

El aviso de riesgo ya está escrito —lo dijiste en el guion del stream, «yo no soy
tu asesor financiero»— pero **no está en ninguna página del sitio**.

### 3 · Tu correo personal, expuesto en el código
El formulario apunta a `formsubmit.co/andremacouzetruiz@gmail.com`, y ese correo
queda **visible en el HTML** para cualquiera que mire el código o para un bot que
raspe la página. Dos consecuencias: spam garantizado, y se lee a proyecto de fin
de semana, no a firma que cobra.

**Arreglo:** un correo del dominio (`hola@northpointcapital.io`) y el formulario
por un servicio que no exponga la dirección.

---

## 🟠 Te cuesta ventas — se nota de inmediato

### 4 · Al compartir el link no sale nada
Ninguna página tiene `og:image`. Cuando pegas northpointcapital.io en WhatsApp,
Instagram o X, aparece **un rectángulo gris sin imagen**. Es lo primero que ve
alguien a quien le pasan tu link, y hoy dice «esto no está terminado».

Hacen falta tres imágenes de 1200×630: una para la landing, una para el perfil,
una para el bootcamp. Con los retratos que ya tienes se arman en minutos.

### 5 · El bootcamp está en inglés y todo lo demás en español
`bootcamp.html` sigue con `lang="en"` y el título *«The Bootcamp»*, mientras la
landing y el perfil ya están en español. Quien navega de una a otra siente que
son dos sitios distintos.

### 6 · El bootcamp no tiene `<h1>` ni descripción
Google no sabe de qué trata la página que quieres vender. Es la única de las tres
sin `<h1>` y sin `meta description`.

### 7 · Después de aplicar, nadie sabe qué sigue
El formulario redirige a `index.html#educacion` — de vuelta a la misma página.
Existe `gracias.html` y no se usa. Quien te manda su historial de payouts se
queda sin confirmación y sin saber cuánto vas a tardar en contestar.

---

## 🟡 Acabado — la diferencia entre «está bien» y «es serio»

### 8 · Faltan los archivos que todo sitio publicado tiene
`robots.txt` · `sitemap.xml` · `favicon.ico` · `404.html`

Sin favicon, tu pestaña en el navegador sale con un globo gris junto a las demás.
Sin 404, un link roto muestra la página de error de GitHub, con su logo.

### 9 · La landing tarda 2.9 s
| Página | Tiempo | Peso |
|---|---|---|
| `/` | **2.9 s** | 495 KB |
| `/perfil.html` | 0.86 s | 772 KB |
| `/bootcamp.html` | 1.06 s | 63 KB |

El perfil pesa más pero carga rápido porque sus imágenes van con `loading="lazy"`.
La landing no: son 110 KB de HTML en un solo archivo. Arriba de 3 s la gente se
va, y estás a un pelo.

### 10 · Páginas viejas todavía públicas
`EL-PLAN.html`, `dossier.html`, `invitacion.html` siguen accesibles y con
contenido de etapas anteriores. Cualquiera puede encontrarlas. Si ya no las usas,
sácalas; si sí, actualízalas.

---

## El orden para empezar a cobrar

**Semana 1 — desbloquear el cobro**
1. Decidir el precio del bootcamp
2. Escribir términos, privacidad, reembolso y aviso de riesgo
3. Abrir Stripe (o MercadoPago) y conectar el botón
4. Correo del dominio y sacar el personal del HTML

**Semana 2 — que se vea serio**
5. Las tres `og:image`
6. Bootcamp al español, con `h1` y descripción
7. `gracias.html` como destino del formulario
8. Favicon, robots, sitemap, 404

**Después — pulido**
9. Aligerar la landing
10. Limpiar las páginas viejas

---

## Lo que ya está bien, y no es poco

No todo es lista de pendientes. Esto ya está a la altura:

- **El récord de payouts con el desglose completo.** Trece retiros con fecha y
  monto, leídos de las fondeadoras. Es el activo más fuerte de la página y casi
  nadie en el nicho lo enseña así.
- **El terminal.** Un producto real, funcionando, con sincronización en la nube.
  Es lo que separa esto de una landing bonita.
- **La coherencia visual.** Landing, perfil y retratos hablan el mismo idioma
  gráfico. Eso normalmente cuesta dinero.
- **El dominio propio con HTTPS.** Ya no es un `github.io`.
- **El tono.** «Primero demuestras, después entras» y «un día sin trade es un día
  ganado» son posicionamiento de verdad, no relleno.
