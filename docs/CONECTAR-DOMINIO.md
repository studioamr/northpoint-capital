# northpointcapital.io · conectado

**Hecho el 14 de agosto de 2026.** Brody compró el dominio, cambió el DNS en
GoDaddy y NORTHPOINT ya vive ahí. Este documento queda como registro de cómo se
hizo y de lo que falta cuidar.

- **https://northpointcapital.io** — la firma
- **https://northpointcapital.io/app.html** — el Terminal
- **https://northpointcapital.io/stream/overlay.html** — el overlay del stream

Las direcciones viejas (`studioamr.github.io/northpoint-capital/…`) siguen
funcionando: GitHub las redirige solas.

---

## Cómo quedó

**En GoDaddy** — cuatro registros A al apex y un CNAME para `www`:

| Tipo | Nombre | Valor | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 600 |
| A | `@` | `185.199.109.153` | 600 |
| A | `@` | `185.199.110.153` | 600 |
| A | `@` | `185.199.111.153` | 600 |
| CNAME | `www` | `studioamr.github.io` | 600 |

**En el repo** — el archivo `CNAME` en la raíz con `northpointcapital.io`, y el
dominio activado en la configuración de Pages con HTTPS forzado.

### El orden importaba

Primero el DNS, después el `CNAME` del repo. Al revés, GitHub habría empezado a
redirigir la dirección vieja a la nueva mientras la nueva todavía apuntaba al
parking de GoDaddy: el sitio se cae hasta que propague. Por eso el archivo no se
agregó hasta comprobar que los nameservers de GoDaddy ya contestaban con las
cuatro IP de GitHub.

Se comprobó preguntándole al nameserver directo, sin pasar por caché:

```bash
dig +short @ns29.domaincontrol.com northpointcapital.io A
```

El resolver local puede seguir dando las IP viejas un rato — eso es su caché, no
un problema del dominio.

---

## Lo que hay que cuidar

**El dominio está en la cuenta de Brody, no en la de André.** Hoy no pasa nada
—claramente es un regalo y va en serio—, pero el dominio es la dirección del
negocio: si un día se pierde el acceso a ese correo, o simplemente no se renueva,
NORTHPOINT se queda sin casa y sin manera de recuperarla rápido.

Lo que conviene, cuando haya chance y sin hacerlo raro:

- **Lo más limpio:** que se lo transfiera a una cuenta de GoDaddy de André. Es
  gratis entre cuentas de GoDaddy y tarda unos minutos.
- **Lo mínimo:** acceso delegado al dominio, para poder tocar el DNS y renovarlo
  si hace falta.

Y **renovación automática**. Un `.io` que se vence se libera y lo puede comprar
cualquiera — hay gente que se dedica justo a eso.

---

## Si algún día hay que mover el sitio de lugar

1. Cambiar los cuatro registros A en GoDaddy al destino nuevo.
2. Esperar a que propague (`dig +short @ns29.domaincontrol.com …`).
3. Hasta entonces, no tocar el `CNAME` del repo.

Y los links absolutos del proyecto: son **14**, repartidos en la landing, el
bootcamp, el dossier, la invitación, el overlay y las guías del stream. Se
encuentran con:

```bash
grep -rn "northpointcapital.io" --include="*.html" --include="*.md" .
```
