-- ═══════════════════════════════════════════════════════════════
--  NORTHPOINT · ABRIR LA MESA  (13-ago-2026)
--
--  André: «quita tantas trabas — que si se registran, luego luego
--  entren a la mesa».
--
--  El cliente ya no pide código de invitación. Esto es la otra mitad:
--  la nube tiene que dejar pasar a cualquiera con sesión, porque hoy
--  la política exige una lista blanca de correos y sin este cambio el
--  que se registre va a entrar y ver su Terminal EN BLANCO.
--
--  DÓNDE SE CORRE: supabase.com → proyecto eskpyntqmioiwvaczpcl →
--  SQL Editor → pegar TODO → Run.
--
--  ⚠️  LO QUE ESTO SIGNIFICA, SIN ADORNOS: a partir de aquí, cualquier
--  persona que se registre con cualquier correo ve la mesa COMPLETA —
--  balances, cuentas, el journal de todos los socios. No hay filtro.
--  Es exactamente lo que pediste; queda escrito para que nadie se
--  sorprenda después.
--
--  Si algún día quieres volver a cerrarla, al final está cómo.
-- ═══════════════════════════════════════════════════════════════

-- ── 1 · las políticas viejas de lista blanca ──────────────────
--  (si alguna no existe, el DROP IF EXISTS no rompe nada)
drop policy if exists "socios leen"        on public.northpoint_estado;
drop policy if exists "socios escriben"    on public.northpoint_estado;
drop policy if exists "socios actualizan"  on public.northpoint_estado;
drop policy if exists "lista blanca lee"   on public.northpoint_estado;
drop policy if exists "lista blanca escribe" on public.northpoint_estado;

-- ── 2 · la política nueva: basta con tener sesión ─────────────
alter table public.northpoint_estado enable row level security;

create policy "mesa abierta lee"
  on public.northpoint_estado for select
  to authenticated
  using (true);

create policy "mesa abierta inserta"
  on public.northpoint_estado for insert
  to authenticated
  with check (true);

create policy "mesa abierta actualiza"
  on public.northpoint_estado for update
  to authenticated
  using (true) with check (true);

-- ── 3 · unirse_a_mesa: que ya no exija código ────────────────
--  Se conserva la función porque el cliente la sigue llamando: ahora
--  simplemente confirma que hay sesión y contesta 'ok'.
create or replace function public.unirse_a_mesa(codigo text default '',
                                                nombre text default '')
returns text
language plpgsql
security definer
set search_path = public
as $$
begin
  if auth.uid() is null then
    return 'sin-sesion';
  end if;
  -- la mesa está abierta: quien tiene sesión, pasa
  return 'ok';
end;
$$;

grant execute on function public.unirse_a_mesa(text, text) to authenticated;

-- ── 4 · comprobación ──────────────────────────────────────────
--  Debe listar las tres políticas "mesa abierta …"
select policyname, cmd, roles
from pg_policies
where schemaname = 'public' and tablename = 'northpoint_estado'
order by policyname;


-- ═══════════════════════════════════════════════════════════════
--  SI ALGÚN DÍA QUIERES VOLVER A CERRARLA
--  (no correr ahora — es la receta para después)
--
--  drop policy "mesa abierta lee"       on public.northpoint_estado;
--  drop policy "mesa abierta inserta"   on public.northpoint_estado;
--  drop policy "mesa abierta actualiza" on public.northpoint_estado;
--
--  create policy "socios leen" on public.northpoint_estado for select
--    to authenticated
--    using (auth.jwt() ->> 'email' in (
--      'andremacouzetruiz@gmail.com',
--      'pabloochoa8am@outlook.com'
--      -- … agregar aquí a quien SÍ puede ver la mesa
--    ));
--  (y las gemelas de insert/update con el mismo in (…))
-- ═══════════════════════════════════════════════════════════════
