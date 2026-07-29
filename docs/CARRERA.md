# NORTHPOINT · La carrera (liga mensual de la comunidad)

**Estado: RETIRADA de la app (29-jul-2026).** La sección se quitó de El
negocio ese mismo día por decisión de André; en su lugar, El camino a payout
muestra el proceso de cada socio (un punto por persona sobre la banda). La
tabla `northpoint_carrera` **sigue viva en Supabase** con sus políticas —
si algún día vuelve la liga, es reconectar la UI, no rehacer el backend.
El resto de este documento queda como referencia de cómo funcionaba.

Antes de retirarla estaba conectada y probada end-to-end: la app subía la
fila del participante y leía la liga completa.

> En la misma corrida se actualizó la política de `northpoint_estado` a los
> **tres** socios (salió `goyo@northpoint.mx` de la lista). El usuario de
> Goyo sigue existiendo en Authentication pero ya no puede leer ni escribir
> la mesa; si quieres, bórralo desde Authentication → Users.

---

## El SQL que se corrió (por si hay que reponerlo)

```sql
create table if not exists northpoint_carrera (
  id         text primary key,          -- dispositivo + mes (lo arma la app)
  codigo     text not null,             -- el código de la carrera
  nombre     text not null,             -- cómo quiere aparecer en la liga
  mes        text not null,             -- '2026-07': la temporada
  pnl        numeric not null default 0,
  sesiones   int not null default 0,
  winrate    numeric not null default 0,
  updated_at timestamptz default now()
);
create index if not exists carrera_codigo_mes on northpoint_carrera (codigo, mes);

alter table northpoint_carrera enable row level security;

-- Comunidad abierta: cualquiera con la app puede leer y escribir SU fila.
-- (La mesa privada de los socios vive en northpoint_estado y NO se toca:
--  esa sigue cerrada a los tres correos.)
create policy "carrera lee" on northpoint_carrera
  for select to anon, authenticated using (true);
create policy "carrera inserta" on northpoint_carrera
  for insert to anon, authenticated with check (true);
create policy "carrera actualiza" on northpoint_carrera
  for update to anon, authenticated using (true) with check (true);
```

Con eso puesto, cualquiera que abra Progreso con una carrera activa sube su
fila y ve las de los demás. Nada que cambiar en la app.

---

## Cómo funciona

- **Unirse**: en Progreso → La carrera pones tu nombre y el código que te
  pasaron. **Crear**: la app genera un código de 6 letras para compartir.
- **Qué se comparte**: P&L del mes, días operados y win rate. Nada más — ni
  trades individuales, ni cuentas, ni la mesa de los socios.
- **La temporada** es el mes en curso; el 1º del mes la liga arranca de cero
  (las filas viejas quedan por mes, no se borran).
- **Identidad**: cada dispositivo tiene un id aleatorio; tu fila sólo la
  actualiza tu equipo. La carrera es local por persona (no viaja con la mesa
  compartida de los socios).

## Lo que hay que saber (honestidad)

- La tabla es **abierta a propósito** (cualquiera con la app puede escribir):
  es una liga amistosa, no un sistema con cuentas. Alguien malicioso podría
  inventarse cifras — igual que en cualquier liga de honor.
- Los datos salen del journal de cada quien: la liga es tan honesta como el
  registro de cada participante.
