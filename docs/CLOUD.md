# CENIT · Nube colaborativa (mesa compartida entre Pablo, Mateo y André)

Hoy el Terminal guarda todo en el equipo de cada quien (localStorage). Para que los tres
vean y firmen LA MISMA mesa de aprobaciones desde sus propias máquinas (tipo Drive),
se conecta una nube gratuita de Supabase. Son ~5 minutos y solo se hace una vez.

## Pasos (los hace André)

1. Entrar a https://supabase.com → New project (gratis). Nombre: `cenit`.
2. En el proyecto: **SQL Editor** → pegar y correr esto:

```sql
create table if not exists northpoint_estado (
  id int primary key,
  data jsonb,
  updated_at timestamptz default now()
);
insert into northpoint_estado (id, data) values (1, '{}') on conflict do nothing;
alter table northpoint_estado enable row level security;
create policy "northpoint rw" on northpoint_estado for all using (true) with check (true);
```

3. En **Settings → API** copiar dos cosas:
   - Project URL (algo como `https://xxxx.supabase.co`)
   - `anon` public key

4. En `app.html`, buscar la línea:

```js
const CLOUD = { url:'', anon:'' };
```

   y pegar los valores:

```js
const CLOUD = { url:'https://xxxx.supabase.co', anon:'eyJ...' };
```

5. Listo. El pill de la vista Aprobaciones cambia a **NUBE · SINCRONIZADA**.
   Cada guardado se sube y cada 8 segundos se baja lo del resto del equipo.

## Notas

- La clave `anon` + política abierta = cualquiera con la clave puede leer/escribir.
  Para uso interno de los tres está bien; no publicar el repo con la clave dentro.
- El login de cada socio (usuario/clave del Terminal) NO viaja a la nube — solo el
  estado de la mesa (tesis, firmas, journal, posiciones, estudio).
- Estrategia de sincronía: último en guardar gana (last-write-wins). Suficiente para
  un equipo de tres que no edita el mismo campo al mismo segundo.
