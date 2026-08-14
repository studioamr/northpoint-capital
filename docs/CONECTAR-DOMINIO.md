# Conectar northpointcapital.io

Brody compró el dominio. Está en **GoDaddy** y ahora mismo apunta a la página de
aparcado de ellos. Esto es lo que falta para que sea la casa de NORTHPOINT.

---

## ⚠️ El orden importa

**Primero el DNS, después GitHub.** Si se activa el dominio en GitHub antes de
que el DNS apunte, GitHub empieza a redirigir la dirección vieja a la nueva — y
como la nueva todavía apunta al parking de GoDaddy, **el sitio se cae** hasta que
propague. Por eso el archivo `CNAME` no está en el repo todavía.

---

## Paso 1 · Los registros DNS · lo hace quien tenga la cuenta de GoDaddy

El dominio está a nombre del correo `segregopt12@gmail.com`, así que esto lo
tiene que hacer Brody (o darte acceso).

**GoDaddy → Mis productos → northpointcapital.io → DNS → Administrar zonas**

Borrar los registros `A` y `CNAME` que GoDaddy pone de fábrica (los que apuntan
a su parking) y dejar exactamente esto:

| Tipo | Nombre | Valor | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 600 |
| A | `@` | `185.199.109.153` | 600 |
| A | `@` | `185.199.110.153` | 600 |
| A | `@` | `185.199.111.153` | 600 |
| CNAME | `www` | `studioamr.github.io` | 600 |

Son **cuatro** registros A (los cuatro, no uno) más **un** CNAME. Las cuatro IP
son de GitHub Pages y son públicas y fijas.

**Para copiar y pegar en WhatsApp:**

```
GoDaddy → northpointcapital.io → DNS

Borra los A y CNAME que ya están, y pon:

A     @     185.199.108.153
A     @     185.199.109.153
A     @     185.199.110.153
A     @     185.199.111.153
CNAME www   studioamr.github.io

TTL 600 en todos. Nada más.
```

## Paso 2 · Esperar

Tarda de 10 minutos a unas horas. Se comprueba así:

```bash
dig +short northpointcapital.io A
```

Cuando conteste las cuatro `185.199.x.153`, ya está.

## Paso 3 · GitHub · esto lo hago yo

Cuando el DNS ya apunte:

1. Se agrega el archivo `CNAME` con `northpointcapital.io` al repo
2. Se activa el dominio en la configuración de Pages
3. Se espera a que GitHub emita el certificado (unos minutos) y se prende
   **Enforce HTTPS**

Después de eso:

| Antes | Después |
|---|---|
| studioamr.github.io/northpoint-capital | **northpointcapital.io** |
| …/app.html | **northpointcapital.io/app.html** |
| …/stream/overlay.html | **northpointcapital.io/stream/overlay.html** |

Las direcciones viejas siguen funcionando: GitHub las redirige solas.

## Paso 4 · Los links de adentro

Hay 13 links absolutos a la dirección vieja repartidos en la landing, el
bootcamp, el dossier, la invitación y las guías del stream. Se cambian todos de
una vez cuando el dominio esté vivo — antes no, porque quedarían apuntando a un
lugar que todavía no responde.

---

## Una cosa que hay que arreglar, sin prisa pero sin olvidarla

**El dominio está en la cuenta de Brody, no en la tuya.** Hoy no pasa nada
—claramente es un regalo y va en serio—, pero el dominio es la dirección del
negocio: si un día se pierde el acceso a ese correo, o simplemente no renueva,
NORTHPOINT se queda sin casa y sin manera de recuperarla rápido.

Lo que conviene, cuando haya chance y sin hacerlo raro:

- **Lo más limpio:** que te lo transfiera a una cuenta de GoDaddy tuya. Es
  gratis entre cuentas de GoDaddy y tarda unos minutos.
- **Lo mínimo:** que te dé acceso delegado al dominio, para que tú también
  puedas tocar el DNS y renovarlo si hace falta.

Y ponle **renovación automática**. Un `.io` que se vence se libera y lo puede
comprar cualquiera — hay gente que se dedica justo a eso.
