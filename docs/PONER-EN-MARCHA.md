# Poner la mesa en marcha para los dos

El terminal ya está listo. Lo único que falta son **cuentas y contraseñas**, y eso lo
tiene que hacer André: yo no creo cuentas ni tecleo contraseñas de nadie — ni la tuya
ni la de Pablo.

Son dos pasos en Supabase y toma unos minutos.

---

## Qué ya está resuelto

- La mesa se comparte: cuando uno de los dos propone una tesis, firma o registra un
  trade, al otro le aparece en menos de 8 segundos.
- Los dos pueden firmar la misma tesis **al mismo tiempo** sin pisarse: las firmas
  se suman, no se reemplazan.
- Bajar la mesa dos veces no duplica nada.
- Los ingresos y gastos de caja (payouts cobrados, lo que costó operar) se fusionan
  por id — antes de hoy esto NO era cierto: si uno registraba un movimiento y el otro
  sincronizaba después, el segundo borraba en silencio el del primero. Ya corregido
  y probado con datos sintéticos antes de escribir esto.
- La política de seguridad está activa y verificada: sin sesión iniciada no se puede
  leer ni escribir la mesa, ni siquiera con la llave pública.
- «Borrar todo» ya **no** borra la mesa del otro — sólo limpia tu equipo y vuelve a
  bajar la mesa compartida.
- El indicador de arriba (junto al reloj) sólo le habla a quien de verdad depende de
  la nube: a ti y a Pablo. A los invitados con acceso de prueba no les sale nada,
  porque ellos trabajan aislados a propósito.

---

## Paso 1 · Crear los dos accesos

En Supabase → proyecto **spotter-ai** → **Authentication → Users → Add user**, con
**Auto Confirm User** activado (si no, quedan esperando un correo que nunca llega).

| Correo | Contraseña | Quién |
|---|---|---|
| `andre@northpoint.mx` | (la que tú elijas) | André |
| `pablo@northpoint.mx` | (la que tú elijas) | Pablo |

> Esos correos **no son reales ni tienen que serlo**: son sólo el identificador con el
> que Supabase reconoce a cada quien. Lo que cada uno escribe en el terminal es su
> usuario (`andre.np`, `pablo.np`); el terminal lo traduce solo.

Si ya habías creado a Mateo o a Goyo en algún intento anterior, no hace falta borrarlos
—simplemente ya no van a poder entrar a la mesa después del paso 2— pero si prefieres
limpieza total, bórralos también en Authentication → Users.

Ponle a Pablo una contraseña temporal y que la cambie él mismo al entrar (Configuración
→ Cambiar contraseña). Esa contraseña es de él, no tuya: no se la pidas de vuelta.

---

## Paso 2 · Dejar entrar sólo a los dos en la política

La tabla no se conforma con «tener cuenta»: exige estar en una lista. Ahora mismo esa
lista tiene cuatro correos (Pablo, Mateo, André, Goyo) porque así se armó cuando el plan
era un equipo de cuatro. Hay que dejarla en dos.

En Supabase → **SQL Editor** → pega y ejecuta:

```sql
drop policy if exists "socios leen" on northpoint_estado;
drop policy if exists "socios escriben" on northpoint_estado;

create policy "socios leen" on northpoint_estado
for select to authenticated
using (auth.jwt() ->> 'email' in (
  'andre@northpoint.mx','pablo@northpoint.mx'));

create policy "socios escriben" on northpoint_estado
for update to authenticated
using (auth.jwt() ->> 'email' in (
  'andre@northpoint.mx','pablo@northpoint.mx'))
with check (auth.jwt() ->> 'email' in (
  'andre@northpoint.mx','pablo@northpoint.mx'));
```

Con esto, aunque Mateo o Goyo todavía tengan cuenta en Supabase, ya no pueden leer ni
escribir la mesa — la política los deja fuera aunque inicien sesión.

> Las políticas reales se llaman **`socios leen`** (SELECT) y **`socios escriben`**
> (UPDATE) — son dos, no una.

Esa lista existe porque el proyecto `spotter-ai` es **compartido con SPOTTER**, que tiene
alrededor de diez usuarios registrados. Si la política dijera nada más «cualquiera con
sesión», cualquier usuario de SPOTTER podría leer la mesa. Por eso va por correo.

---

## Paso 3 · Comprobar que quedó

1. Abre el terminal y entra con tu usuario y tu contraseña de Supabase (no la local).
2. Mira el indicador de arriba, junto al reloj:

| Dice | Significa |
|---|---|
| **NUBE · SINCRONIZADA** (verde) | Todo bien, lo que hagas le llega a Pablo |
| **TRABAJANDO SOLO · esto no le llega a tu socio** (ámbar) | La contraseña no coincide con Supabase, o no hay internet. Tu trabajo se está quedando en tu equipo |
| **NUBE · ERROR …** (rojo) | Entraste pero la política te está rechazando: revisa el paso 2 |

3. Propón una tesis de prueba. Pídele a Pablo que entre desde su equipo: le tiene que
   aparecer.
4. Bórrala cuando confirmen los dos.

---

## Si algo no cuadra

| Síntoma | Causa casi siempre |
|---|---|
| Dice "trabajando solo" aunque la contraseña sea correcta | Al crear el usuario faltó **Auto Confirm** |
| Dice ERROR 401 o 403 | El correo no está en la lista del paso 2, o el SQL no se corrió |
| Uno ve la mesa y el otro no | El que no ve está en modo local: revisa su indicador |
| Alguien no aparece al firmar | Su usuario en Supabase no coincide con el `correo` de `USERS` en `app.html` |
| Ves los movimientos de caja del otro duplicados o incompletos | No debería pasar — la fusión por id ya está corregida. Si pasa, avísame con el detalle exacto |
