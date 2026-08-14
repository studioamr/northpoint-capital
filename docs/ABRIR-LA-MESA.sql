-- ═══════════════════════════════════════════════════════════════
--  NORTHPOINT · ABRIR LA MESA  (13-ago-2026)
--
--  André: «quita tantas trabas — que si se registran, luego luego
--  entren a la mesa». El código de invitación ya se fue del cliente;
--  esto es la otra mitad, del lado de la nube.
--
--  ⚠️  POR QUÉ NO ES UN SIMPLE `to authenticated`:
--  este proyecto de Supabase es el MISMO de SPOTTER, que ya tiene
--  ~10 usuarios registrados. Con una política de `authenticated` a
--  secas, esa gente —que se dio de alta para otra app y no tiene nada
--  que ver con la firma— podría leer la mesa: balances, cuentas y el
--  journal de todos. Eso no es lo que se pidió.
--
--  LO QUE HACE ESTE SCRIPT:
--    · quien se registra DESDE EL TERMINAL entra directo, sin código
--    · los usuarios de SPOTTER siguen sin ver nada
--
--  El mecanismo es simple: el alta del Terminal llama a unirse_a_mesa
--  (ya lo hace el cliente); esa función mete al usuario en la lista de
--  la mesa, y la RLS deja pasar a quien esté en esa lista.
--
--  DÓNDE SE CORRE: supabase.com → proyecto eskpyntqmioiwvaczpcl →
--  SQL Editor → pegar TODO → Run.
-- ═══════════════════════════════════════════════════════════════

-- ── 1 · la lista de la mesa ───────────────────────────────────
create table if not exists public.mesa_socios (
  uid     uuid primary key references auth.users(id) on delete cascade,
  correo  text,
  nombre  text,
  alta    timestamptz not null default now()
);

alter table public.mesa_socios enable row level security;

drop policy if exists "socios se ven entre ellos" on public.mesa_socios;
create policy "socios se ven entre ellos"
  on public.mesa_socios for select
  to authenticated
  using (exists (select 1 from public.mesa_socios m where m.uid = auth.uid()));

-- ── 2 · los que YA son de la mesa entran de una ────────────────
--  (los tres socios y cualquiera que ya haya iniciado sesión antes)
insert into public.mesa_socios (uid, correo, nombre)
select u.id, u.email, coalesce(u.raw_user_meta_data->>'name', split_part(u.email,'@',1))
from auth.users u
where u.email in (
  'andremacouzetruiz@gmail.com',
  'pabloochoa8am@outlook.com',
  'andre@northpoint.mx',
  'pablo@northpoint.mx',
  'mateo@northpoint.mx'
)
on conflict (uid) do nothing;

-- ── 3 · unirse_a_mesa: sin código, basta con tener sesión ──────
create or replace function public.unirse_a_mesa(codigo text default '',
                                                nombre text default '')
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  u uuid := auth.uid();
  c text;
begin
  if u is null then
    return 'sin-sesion';
  end if;
  select email into c from auth.users where id = u;
  insert into public.mesa_socios (uid, correo, nombre)
  values (u, c, nullif(nombre, ''))
  on conflict (uid) do update
    set nombre = coalesce(nullif(excluded.nombre, ''), mesa_socios.nombre);
  return 'ok';
end;
$$;

grant execute on function public.unirse_a_mesa(text, text) to authenticated;

-- ── 4 · la RLS de la mesa: pasa quien está en la lista ─────────
alter table public.northpoint_estado enable row level security;

drop policy if exists "socios leen"          on public.northpoint_estado;
drop policy if exists "socios escriben"      on public.northpoint_estado;
drop policy if exists "socios actualizan"    on public.northpoint_estado;
drop policy if exists "lista blanca lee"     on public.northpoint_estado;
drop policy if exists "lista blanca escribe" on public.northpoint_estado;
drop policy if exists "mesa lee"             on public.northpoint_estado;
drop policy if exists "mesa inserta"         on public.northpoint_estado;
drop policy if exists "mesa actualiza"       on public.northpoint_estado;

create policy "mesa lee"
  on public.northpoint_estado for select to authenticated
  using (exists (select 1 from public.mesa_socios m where m.uid = auth.uid()));

create policy "mesa inserta"
  on public.northpoint_estado for insert to authenticated
  with check (exists (select 1 from public.mesa_socios m where m.uid = auth.uid()));

create policy "mesa actualiza"
  on public.northpoint_estado for update to authenticated
  using (exists (select 1 from public.mesa_socios m where m.uid = auth.uid()))
  with check (exists (select 1 from public.mesa_socios m where m.uid = auth.uid()));

-- ── 5 · comprobación ──────────────────────────────────────────
select policyname, cmd from pg_policies
where schemaname='public' and tablename='northpoint_estado' order by policyname;

select correo, nombre, alta from public.mesa_socios order by alta;


-- ═══════════════════════════════════════════════════════════════
--  PARA METER A ALGUIEN A MANO (por ejemplo Rodrigo, si ya se
--  registró antes de este cambio):
--
--    insert into public.mesa_socios (uid, correo, nombre)
--    select id, email, 'Rodrigo' from auth.users
--    where email = 'el-correo-de-rodrigo@gmail.com'
--    on conflict (uid) do nothing;
--
--  PARA SACAR A ALGUIEN:
--    delete from public.mesa_socios where correo = 'quien@sea.com';
-- ═══════════════════════════════════════════════════════════════
