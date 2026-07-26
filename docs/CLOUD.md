# NORTHPOINT · Nube compartida (la misma mesa para André y Pablo)

**Estado: conectada, falta el paso 2 de [PONER-EN-MARCHA.md](PONER-EN-MARCHA.md).**
El backend está montado y la app apunta a él.

> **Para ponerla en marcha, la guía corta es [PONER-EN-MARCHA.md](PONER-EN-MARCHA.md).**
> Este documento es el detalle técnico de cómo está resuelta la sincronización.
> La mesa pasó por varias formaciones (llegó a ser cuatro, con Mateo y Gregorio) y
> volvió a ser **dos**: André y Pablo. La política de acceso en Supabase debe reflejar
> eso — el SQL de este documento ya está actualizado a los dos correos.

---

## Cómo quedó montado

| Qué | Dónde |
|---|---|
| Proyecto Supabase | `spotter-ai` (`eskpyntqmioiwvaczpcl`) |
| Tabla | `northpoint_estado` |
| Llave en `app.html` | `sb_publishable_…` (publicable, ver abajo) |

**Se reusó el proyecto de SPOTTER en vez de crear uno nuevo.** El plan gratis sólo
permite 2 proyectos activos y ya estaban ocupados por *Agrofin app* y *spotter-ai*.
Crear uno nuevo obligaba a pausar alguno; pausar SPOTTER habría tumbado el backend de
una app que ya está en manos de gente. Un proyecto de Supabase aguanta muchas tablas,
así que `northpoint_estado` vive junto a `posts` y `profiles` **sin tocarlas**.

Como el proyecto es compartido, la política **no** se conformó con "cualquiera con sesión":
está restringida a los dos correos de los socios. Un usuario de SPOTTER, aunque tenga
sesión válida en el mismo proyecto, no puede leer ni escribir la mesa.

---

## Por qué la llave sí va en el código

En Supabase hay dos llaves y se confunden seguido:

| Llave | Va en el navegador | Si se filtra |
|---|---|---|
| `sb_publishable_…` (antes `anon`) | **Sí, está diseñada para eso** — el propio panel dice *"Publishable keys can be safely shared publicly"* | Nada por sí sola: sólo deja *intentar*, y la política decide |
| `sb_secret_…` (antes `service_role`) | **Nunca** | Acceso total, se salta todas las políticas |

Lo que protege los datos no es esconder la llave publicable — es la política RLS.
**Nunca pegues la `sb_secret_…` en `app.html`.** El repositorio es público.

Comprobado desde fuera, sin sesión:

```
GET  northpoint_estado  → []        (no filtra nada)
PATCH northpoint_estado → []        (0 filas: no deja escribir)
```

---

## El SQL que se corrió

```sql
create table if not exists northpoint_estado (
  id         int primary key,
  data       jsonb not null default '{}'::jsonb,
  rev        int  not null default 0,
  updated_at timestamptz default now()
);
insert into northpoint_estado (id, data, rev) values (1, '{}'::jsonb, 0)
on conflict (id) do nothing;

alter table northpoint_estado enable row level security;

-- Sólo los dos socios. No basta con tener sesión en el proyecto.
create policy "socios leen" on northpoint_estado
  for select to authenticated
  using (auth.jwt() ->> 'email' in
    ('andre@northpoint.mx','pablo@northpoint.mx'));

create policy "socios escriben" on northpoint_estado
  for update to authenticated
  using (auth.jwt() ->> 'email' in
    ('andre@northpoint.mx','pablo@northpoint.mx'))
  with check (auth.jwt() ->> 'email' in
    ('andre@northpoint.mx','pablo@northpoint.mx'));
```

> Si el proyecto todavía tiene la política vieja (con `mateo@northpoint.mx` y/o
> `goyo@northpoint.mx` en la lista), hay que CORRER este SQL para reemplazarla —
> `create policy` no pisa una política existente con el mismo nombre sin el `drop`
> de antes. El paso a paso está en [PONER-EN-MARCHA.md](PONER-EN-MARCHA.md).

---

## Lo único que falta (2 minutos, lo hace André)

Dar de alta a los dos socios. **Yo no lo hago a propósito: implicaría que yo teclee
la contraseña de Pablo, y esa clave debe ser suya, no mía ni tuya.**

Ve a **Authentication → Users** del proyecto `spotter-ai` y elige uno de los dos caminos:

**Camino A — Add user (lo más rápido).** Marca *Auto Confirm User* y crea:

| Usuario en el terminal | Correo (identificador en Supabase) | Quién |
|---|---|---|
| `andre.np` | `andre@northpoint.mx` | André |
| `pablo.np` | `pablo@northpoint.mx` | Pablo |

Pon una contraseña temporal y que cada quien la cambie al entrar. Los dos tienen los
mismos cinco cargos (Mesa, Riesgo, Payouts, Portafolio, Cuenta propia): son socios
parejos, sin división de roles.

**Camino B — Invite user (más limpio).** Supabase les manda un correo con liga y cada
quien pone su propia contraseña sin que nadie más la vea. Requiere que esos correos
existan de verdad; si `@northpoint.mx` no es un dominio tuyo, usa sus correos reales y
cámbialos también en `app.html`, en el campo `correo` de `const USERS`.

Ya con los usuarios creados, el indicador de arriba pasa de `TRABAJANDO SOLO` a
`NUBE · SINCRONIZADA` en cuanto cada quien entre con su correo. Ese indicador sólo
le habla a André y Pablo — a los invitados con acceso de prueba no les sale nada,
porque ellos trabajan aislados a propósito y no tienen "socio" con quien sincronizar.

---

## Qué cambia ahora que está conectada

- **El acceso deja de ser de adorno.** Las claves `NP-KEY-0X` están a la vista en el
  código y sólo separaban perfiles. Ahora la contraseña la valida Supabase del lado del
  servidor, y sin sesión válida la política ni siquiera deja leer la mesa.
- **Las firmas ya no se pisan.** Cada guardado lleva número de revisión y escribe sólo si
  nadie tocó la fila desde su última lectura. Si alguien se adelantó, la app **fusiona
  por id** (trades, tesis, cuentas, posiciones **y caja**) y reintenta. Las firmas de una
  misma tesis se suman: André y Pablo pueden firmar al mismo tiempo sin borrarse.
- **Caja se fusiona de verdad.** Hasta antes de esta revisión, `caja` (los ingresos y
  gastos reales) NO estaba en la lista de campos que se fusionan por id — el que
  sincronizaba último se quedaba con su arreglo completo y borraba en silencio los
  movimientos del otro. Corregido y probado con datos sintéticos: cada quien puede
  registrar un payout o un gasto en su propio equipo sin pisar al otro.
- **Lo personal no viaja.** Tu perfil y tu selección de cuentas se quedan en tu máquina.
- **El indicador dice la verdad:** `SINCRONIZADA`, `TRABAJANDO SOLO`, `SIN RESPUESTA` o
  `ERROR <código>` según lo que de verdad esté pasando — y sólo le aparece a André y
  Pablo, no a los invitados.

## Si algo no jala

| Síntoma | Causa casi siempre |
|---|---|
| `TRABAJANDO SOLO` | Todavía no existen los usuarios, o entraste con tu clave local en vez de la de Supabase |
| `ERROR 401` | La sesión venció y no pudo renovarse. Cierra sesión y vuelve a entrar |
| `ERROR 42501` | El correo con el que entraste no está en la lista de la política |
| Entra pero no ve nada del otro | Revisa que los dos entraron con su correo, no con la clave local |

## Lo que sigue faltando

- **No hay historial ni marcha atrás.** Es un documento que se sobrescribe (fusionando).
  Si alguien borra algo por error, se recupera del respaldo local, no de la nube.
- **La fusión favorece a quien guarda.** En un empate sobre el mismo registro gana la
  versión local de quien escribe.
- **Los roles siguen siendo cosa de la app.** La base deja escribir a los dos por igual;
  no hay división de cargos entre André y Pablo — son socios parejos.
- **El proyecto es compartido con SPOTTER.** Si algún día SPOTTER crece o se separa,
  vale la pena mover NORTHPOINT a su propio proyecto.
