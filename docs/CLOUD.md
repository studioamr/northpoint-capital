# NORTHPOINT · Nube compartida (la misma mesa para Pablo, Mateo y André)

Hoy el terminal guarda todo en la máquina de cada quien. Con esto, los tres ven y firman
**la misma** mesa de aprobaciones desde sus propias computadoras. Son unos 10 minutos y
se hace una sola vez.

---

## Antes de empezar: por qué la llave sí va en el código

En Supabase hay dos llaves y se confunden seguido:

| Llave | Va en el navegador | Qué pasa si se filtra |
|---|---|---|
| `anon` / publishable | **Sí, está diseñada para eso** | Nada por sí sola: sólo deja *intentar*, y la política decide |
| `service_role` | **Nunca** | Acceso total, se salta todas las políticas |

Lo que protege los datos **no es esconder la llave `anon`** — es la política **RLS** de la
tabla. La versión anterior de este instructivo traía `using (true) with check (true)`, que
significa *cualquiera con la URL puede leer y borrar la mesa*. Eso sí era un hueco real,
y es lo que corrige el paso 2.

**Nunca pegues la `service_role` en `app.html`.** El repositorio es público.

---

## Paso 1 · Crear el proyecto

Entra a https://supabase.com → **New project** (el plan gratis alcanza de sobra).
Nombre: `northpoint`. Guarda la contraseña de la base que te pida; no la vas a necesitar
para esto, pero sí para administrar después.

## Paso 2 · Crear la tabla con seguridad de verdad

**SQL Editor** → pega esto completo y córrelo:

```sql
create table if not exists northpoint_estado (
  id         int primary key,
  data       jsonb not null default '{}'::jsonb,
  rev        int  not null default 0,
  updated_at timestamptz default now()
);

insert into northpoint_estado (id, data, rev)
values (1, '{}'::jsonb, 0)
on conflict (id) do nothing;

alter table northpoint_estado enable row level security;

-- Sólo alguien con sesión iniciada puede leer o escribir.
-- Sin esto, cualquiera con la URL y la llave pública vería y borraría la mesa.
drop policy if exists "northpoint rw"      on northpoint_estado;
drop policy if exists "socios leen"        on northpoint_estado;
drop policy if exists "socios escriben"    on northpoint_estado;

create policy "socios leen" on northpoint_estado
  for select to authenticated using (true);

create policy "socios escriben" on northpoint_estado
  for update to authenticated using (true) with check (true);
```

## Paso 3 · Dar de alta a los tres socios

**Authentication → Users → Add user** (elige *Auto Confirm User* para no lidiar con correos).
Crea exactamente estos tres, cada quien con la contraseña que él elija:

| Correo | Quién |
|---|---|
| `pablo@northpoint.mx` | Pablo — CIO + Portfolio Manager |
| `mateo@northpoint.mx` | Mateo — CRO + Research |
| `andre@northpoint.mx` | André — Quant + COO |

> Si prefieren otros correos, cámbialos también en `app.html`, en el campo `correo` de
> `const USERS`. Lo que debe coincidir es el correo, no el usuario que se teclea al entrar.

**Cada quien pone su propia contraseña.** Nadie más la escribe, y no queda en el código:
Supabase la valida del lado del servidor.

## Paso 4 · Conectar la app

En `app.html` busca:

```js
const CLOUD = { url:'', anon:'' };
```

y pega lo que aparece en **Settings → API**:

```js
const CLOUD = { url:'https://xxxxx.supabase.co', anon:'eyJhbGciOi...' };
```

Sube el cambio y listo.

---

## Qué cambia al conectarla

- **El acceso deja de ser de adorno.** Sin nube, la clave del login sólo separa perfiles y
  está a la vista en el código. Con nube, la contraseña la valida Supabase y sin sesión
  válida la política RLS ni siquiera deja leer la mesa.
- **Las firmas ya no se pisan.** Cada guardado lleva número de revisión y escribe sólo si
  nadie tocó la fila desde su última lectura. Si alguien se adelantó, la app **fusiona por
  id** (trades, tesis, cuentas, posiciones) y reintenta. Las firmas de una misma tesis se
  suman: Pablo y Mateo pueden firmar al mismo tiempo sin borrarse.
- **Lo personal no viaja.** Tu perfil y la selección de cuentas se quedan en tu máquina.
  A la nube sólo sube lo que es de la mesa.
- **El indicador dice la verdad.** El pill de Aprobaciones muestra `SINCRONIZADA`,
  `SIN SESIÓN`, `SIN RESPUESTA` o `ERROR <código>` según lo que de verdad esté pasando.
  Antes decía "sincronizada" con sólo tener la URL puesta, aunque todas las peticiones
  estuvieran fallando.

## Si algo no jala

| Síntoma | Causa casi siempre |
|---|---|
| `ERROR 401` | La sesión venció y no pudo renovarse. Cierra sesión y vuelve a entrar. |
| `ERROR 404` | La tabla no existe o se llama distinto. Vuelve a correr el SQL del paso 2. |
| `ERROR 42501` | La política RLS no deja. Revisa que corriste las tres `create policy`. |
| `SIN SESIÓN` | La app tiene la nube configurada pero nadie ha entrado con su correo. |
| No aparece lo del otro socio | Revisa que los dos vean el mismo proyecto y que ambos entraron con su cuenta. |

## Lo que sigue faltando

- **No hay historial ni marcha atrás.** Es un documento que se sobrescribe (fusionando).
  Si alguien borra algo por error, se recupera del respaldo local, no de la nube.
- **La fusión favorece a quien guarda.** En un empate sobre el mismo registro gana la
  versión local de quien escribe. Para trades y firmas no estorba porque cada quien toca
  los suyos, pero no es un sistema de control de versiones.
- **Sigue sin haber roles del lado del servidor.** Cualquiera de los tres puede escribir
  cualquier cosa; quién puede firmar qué lo decide la app, no la base.
