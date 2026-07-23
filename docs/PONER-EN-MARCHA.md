# Poner la mesa en marcha para los cuatro

El terminal ya está listo. Lo único que falta son **cuentas y contraseñas**, y eso lo
tiene que hacer André: yo no creo cuentas ni tecleo contraseñas de nadie.

Son dos pasos en Supabase y toma unos minutos.

---

## Qué ya está resuelto

- La mesa se comparte: cuando alguien propone una tesis, firma o registra un trade,
  a los demás les aparece en menos de 8 segundos.
- Dos socios pueden firmar la misma tesis **al mismo tiempo** sin pisarse: las firmas
  se suman, no se reemplazan.
- Bajar la mesa dos veces no duplica nada.
- La política de seguridad está activa y verificada: sin sesión iniciada no se puede
  leer ni escribir la mesa, ni siquiera con la llave pública.
- «Borrar todo» ya **no** borra la mesa de los demás — sólo limpia tu equipo y vuelve a
  bajar la mesa compartida.

---

## Paso 1 · Crear los cuatro accesos

En Supabase → proyecto **spotter-ai** → **Authentication → Users → Add user**, con
**Auto Confirm User** activado (si no, quedan esperando un correo que nunca llega).

| Correo | Contraseña | Quién |
|---|---|---|
| `pablo@northpoint.mx` | `northpointpablo` | Pablo |
| `mateo@northpoint.mx` | `northpointmateo` | Mateo |
| `andre@northpoint.mx` | `northpointandre` | André |
| `goyo@northpoint.mx`  | `northpointgoyo`  | Gregorio |

> Esos correos **no son reales ni tienen que serlo**: son sólo el identificador con el
> que Supabase reconoce a cada quien. Lo que cada socio escribe en el terminal es su
> usuario (`pablo.np`, `mateo.np`, `andre.np`, `goyo.np`); el terminal lo traduce solo.

**Las contraseñas tienen que ser exactamente ésas**, porque son las que van impresas en
las hojas PDF que les vas a mandar. Si pones otra, entran igual pero **en modo local**:
verían su propia mesa vacía en vez de la compartida, y su trabajo no le llegaría a nadie.

Si ya creaste a Pablo, Mateo y André antes, revisa nada más que las contraseñas
coincidan y agrega a Goyo.

---

## Paso 2 · Dejar entrar a Goyo en la política

La tabla no se conforma con «tener cuenta»: exige estar en una lista de los socios.
Goyo es nuevo, así que hay que agregarlo.

En Supabase → **SQL Editor** → pega y ejecuta:

```sql
drop policy if exists "socios leen" on northpoint_estado;
drop policy if exists "socios escriben" on northpoint_estado;

create policy "socios leen" on northpoint_estado
for select to authenticated
using (auth.jwt() ->> 'email' in (
  'pablo@northpoint.mx','mateo@northpoint.mx',
  'andre@northpoint.mx','goyo@northpoint.mx'));

create policy "socios escriben" on northpoint_estado
for update to authenticated
using (auth.jwt() ->> 'email' in (
  'pablo@northpoint.mx','mateo@northpoint.mx',
  'andre@northpoint.mx','goyo@northpoint.mx'))
with check (auth.jwt() ->> 'email' in (
  'pablo@northpoint.mx','mateo@northpoint.mx',
  'andre@northpoint.mx','goyo@northpoint.mx'));
```

> Las políticas reales se llaman **`socios leen`** (SELECT) y **`socios escriben`**
> (UPDATE) — son dos, no una. Antes aquí decía `solo socios northpoint`, que no existe:
> ese SQL habría creado una tercera política suelta en vez de corregir las dos buenas.

Esa lista existe porque el proyecto `spotter-ai` es **compartido con SPOTTER**, que tiene
alrededor de diez usuarios registrados. Si la política dijera nada más «cualquiera con
sesión», cualquier usuario de SPOTTER podría leer la mesa. Por eso va por correo.

Cada vez que entre alguien nuevo a la mesa, hay que agregarlo aquí también.

---

## Paso 3 · Comprobar que quedó

1. Abre el terminal y entra con tu usuario y tu contraseña de Supabase.
2. Mira el indicador de arriba, junto al reloj:

| Dice | Significa |
|---|---|
| **NUBE · SINCRONIZADA** (verde) | Todo bien, lo que hagas le llega a los demás |
| **NUBE · SIN SESIÓN — ESTADO LOCAL** (ámbar) | La contraseña no coincide con Supabase, o no hay internet. Estás trabajando solo |
| **NUBE · ERROR …** (rojo) | Entró pero la política la está rechazando: revisa el paso 2 |

3. Propón una tesis de prueba. Pídele a alguien más que entre: le tiene que aparecer.
4. Bórrala cuando confirmen.

Ese indicador está en todas las pantallas a propósito. Si alguien ve ámbar, su trabajo
se está quedando en su equipo y hay que avisar.

---

## Lo que cada socio recibe

En la carpeta `credenciales/` (fuera del repositorio, porque lleva contraseñas):

- `Northpoint-Pablo.pdf`, `Northpoint-Mateo.pdf`, `Northpoint-André.pdf`,
  `Northpoint-Gregorio.pdf` — una hoja cada uno: sus accesos, sus cargos, sus deberes y
  las reglas que no se negocian.
- `correos-para-mandar.txt` y `mensajes-whatsapp.txt` — los mensajes ya redactados.

Manda a cada quien **sólo su hoja**: cada una lleva su contraseña escrita.

---

## Si algo no cuadra

| Síntoma | Causa casi siempre |
|---|---|
| Dice SIN SESIÓN aunque la contraseña sea correcta | Al crear el usuario faltó **Auto Confirm** |
| Dice ERROR 401 o 403 | El correo no está en la lista del paso 2 |
| Uno ve la mesa y otro no | Ese otro está en modo local: revisa su indicador |
| Alguien no aparece al firmar | Su usuario en Supabase no coincide con el `correo` de `USERS` en app.html |
