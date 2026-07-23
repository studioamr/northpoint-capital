# NORTHPOINT · Nube compartida (la misma mesa para los cuatro socios)

**Estado: conectada.** El backend está montado y la app apunta a él.

> **Para ponerla en marcha, la guía corta es [PONER-EN-MARCHA.md](PONER-EN-MARCHA.md).**
> Este documento es el detalle técnico de cómo está resuelta la sincronización.
> Desde el 23 de julio de 2026 la mesa son **cuatro**: se sumó Gregorio (`goyo.np`),
> que también tiene que estar en la política de acceso.

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
está restringida a los tres correos de los socios. Un usuario de SPOTTER, aunque tenga
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

-- Sólo los tres socios. No basta con tener sesión en el proyecto.
create policy "socios leen" on northpoint_estado
  for select to authenticated
  using (auth.jwt() ->> 'email' in
    ('pablo@northpoint.mx','mateo@northpoint.mx','andre@northpoint.mx'));

create policy "socios escriben" on northpoint_estado
  for update to authenticated
  using (auth.jwt() ->> 'email' in
    ('pablo@northpoint.mx','mateo@northpoint.mx','andre@northpoint.mx'))
  with check (auth.jwt() ->> 'email' in
    ('pablo@northpoint.mx','mateo@northpoint.mx','andre@northpoint.mx'));
```

---

## Lo único que falta (2 minutos, lo hace André)

Dar de alta a los tres socios. **Yo no lo hago a propósito: implicaría que yo teclee
las contraseñas de Pablo y de Mateo, y esas claves deben ser suyas, no mías ni tuyas.**

Ve a **Authentication → Users** del proyecto `spotter-ai` y elige uno de los dos caminos:

**Camino A — Add user (lo más rápido).** Marca *Auto Confirm User* y crea:

| Usuario en el terminal | Correo (identificador en Supabase) | Quién |
|---|---|---|
| `pablo.np` | `pablo@northpoint.mx` | Pablo — CIO + Portfolio Manager |
| `mateo.np` | `mateo@northpoint.mx` | Mateo — CRO + Research |
| `andre.np` | `andre@northpoint.mx` | André — Quant + COO |

Pon una contraseña temporal y que cada quien la cambie al entrar.

**Camino B — Invite user (más limpio).** Supabase les manda un correo con liga y cada
quien pone su propia contraseña sin que nadie más la vea. Requiere que esos correos
existan de verdad; si `@northpoint.mx` no es un dominio tuyo, usa sus correos reales y
cámbialos también en `app.html`, en el campo `correo` de `const USERS`.

Ya con los usuarios creados, el pill de Aprobaciones pasa de `NUBE · SIN SESIÓN` a
`NUBE · SINCRONIZADA` en cuanto cada quien entre con su correo.

---

## Qué cambia ahora que está conectada

- **El acceso deja de ser de adorno.** Las claves `NP-KEY-0X` están a la vista en el
  código y sólo separaban perfiles. Ahora la contraseña la valida Supabase del lado del
  servidor, y sin sesión válida la política ni siquiera deja leer la mesa.
- **Las firmas ya no se pisan.** Cada guardado lleva número de revisión y escribe sólo si
  nadie tocó la fila desde su última lectura. Si alguien se adelantó, la app **fusiona
  por id** (trades, tesis, cuentas, posiciones) y reintenta. Las firmas de una misma
  tesis se suman: Pablo y Mateo pueden firmar al mismo tiempo sin borrarse.
- **Lo personal no viaja.** Tu perfil y tu selección de cuentas se quedan en tu máquina.
- **El indicador dice la verdad:** `SINCRONIZADA`, `SIN SESIÓN`, `SIN RESPUESTA` o
  `ERROR <código>` según lo que de verdad esté pasando.

## Si algo no jala

| Síntoma | Causa casi siempre |
|---|---|
| `SIN SESIÓN` | Todavía no existen los usuarios, o nadie ha entrado con su correo |
| `ERROR 401` | La sesión venció y no pudo renovarse. Cierra sesión y vuelve a entrar |
| `ERROR 42501` | El correo con el que entraste no está en la lista de la política |
| Entra pero no ve nada del otro | Revisa que los dos entraron con su correo, no con la clave local |

## Lo que sigue faltando

- **No hay historial ni marcha atrás.** Es un documento que se sobrescribe (fusionando).
  Si alguien borra algo por error, se recupera del respaldo local, no de la nube.
- **La fusión favorece a quien guarda.** En un empate sobre el mismo registro gana la
  versión local de quien escribe.
- **Los roles siguen siendo cosa de la app.** La base deja escribir a los tres por igual;
  quién puede firmar qué lo decide el terminal, no Postgres.
- **El proyecto es compartido con SPOTTER.** Si algún día SPOTTER crece o se separa,
  vale la pena mover NORTHPOINT a su propio proyecto.
