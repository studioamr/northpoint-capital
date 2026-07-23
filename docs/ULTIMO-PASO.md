# El último paso · 10 minutos

Todo lo demás está hecho. Falta **una sola cosa** y sólo la puedes hacer tú, porque son
cuentas y contraseñas: yo no las creo ni las tecleo.

---

## Antes de empezar

Ya quedó listo:

- El terminal limpio, sin nada de la simulación.
- Las **5 cuentas ya configuradas** (T1 a T5, Tradeify Select Evaluation 50k, arrancando
  hoy en $50,000). No las tienes que crear.
- Los 4 PDF de bienvenida en el Escritorio, carpeta `NORTHPOINT-bienvenida`.
- Los correos y mensajes de WhatsApp ya redactados en esa misma carpeta.

---

## 1 · Crear los cuatro accesos (5 min)

Entra a **supabase.com** → proyecto **spotter-ai** → **Authentication** → **Users** →
botón **Add user** → *Create new user*.

Cuatro veces, uno por socio. **Activa siempre la casilla `Auto Confirm User`** — si no,
la cuenta queda esperando un correo de confirmación que nunca va a llegar y no va a poder
entrar.

| Email | Password |
|---|---|
| `pablo@northpoint.mx` | `northpointpablo` |
| `mateo@northpoint.mx` | `northpointmateo` |
| `andre@northpoint.mx` | `northpointandre` |
| `goyo@northpoint.mx`  | `northpointgoyo`  |

> Esos correos **no existen ni tienen que existir**. Son sólo el identificador interno con
> el que Supabase reconoce a cada quien. Cada socio escribe en el terminal su usuario
> (`pablo.np`, `mateo.np`, `andre.np`, `goyo.np`) y la app hace la traducción sola.

**Las contraseñas tienen que ser exactamente ésas**, porque son las que van impresas en
los PDF que les vas a mandar. Si escribes otra, esa persona va a entrar igual pero en
**modo local**: vería su propia mesa vacía y su trabajo no le llegaría a nadie.

---

## 2 · Dar de alta a Goyo en la política (1 min)

En el mismo proyecto → **SQL Editor** → **New query** → pega esto completo y dale **Run**:

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

Esa lista existe porque el proyecto `spotter-ai` lo comparte SPOTTER, que tiene diez
usuarios registrados. Sin ella, cualquiera de ellos podría leer la mesa.

---

## 3 · Probarlo antes de mandar nada (3 min)

1. Abre https://studioamr.github.io/northpoint-capital/app.html
2. Entra con `andre.np` y `northpointandre`.
3. **Mira el indicador junto al reloj, arriba a la derecha.** Ahí está la verdad:

| Lo que dice | Qué significa |
|---|---|
| 🟢 **NUBE · SINCRONIZADA** | Listo. Lo que hagas le llega a los demás |
| 🟡 **NUBE · SIN SESIÓN — ESTADO LOCAL** | La contraseña no coincide con la de Supabase. Revisa el paso 1 |
| 🔴 **NUBE · ERROR 401 / 403** | Entró, pero la política lo rechaza. Revisa el paso 2 |

4. Si está en verde: propón una tesis de prueba en Aprobaciones.
5. Que Pablo entre con su acceso y confirme que **la ve aparecer**.
6. Bórrenla y ya. A partir de ahí es real.

**No mandes los PDF hasta que ese ida y vuelta funcione entre dos personas.**

---

## 4 · Recién entonces, mandarles su acceso

En el Escritorio, carpeta `NORTHPOINT-bienvenida`:

| Para | Archivo | Correo |
|---|---|---|
| Pablo | `Northpoint-Pablo.pdf` | pabloochoa8aM@outlook.com |
| Mateo | `Northpoint-Mateo.pdf` | mateomacouzet2@gmail.com |
| Goyo | `Northpoint-Gregorio.pdf` | scgregop12@gmail.com |

Los textos de los correos están en `correos-para-mandar.txt` y los de WhatsApp en
`mensajes-whatsapp.txt`.

**A cada quien sólo su hoja**: cada PDF trae la contraseña de su dueño escrita.

---

## Dos cosas que decidir antes de operar en serio

Salieron de simular un mes con tu 65% a 1:1, y son tuyas de decidir:

**Baja el riesgo por trade a 23 puntos de NQ ($460 por cuenta)** en vez de 25 ($500). Con
25, dos stops seguidos suman más de $1,000 y rompen el tope diario — no por mala suerte,
por aritmética: el deslizamiento se come el margen. En la simulación pasó el primer día.

**Ajusta la expectativa del plan.** Con 65% a 1:1 y parando después de la primera
ganadora, la esperanza real es **+$202 por cuenta por día**, no los $1,000 del plan. La
evaluación toma unos 15-16 días hábiles, no 3-5. El sistema está bien; la meta está mal
escrita. Y ése es el riesgo de verdad: si arrancan creyendo en los 3-5 días, la presión
de "ponerse al corriente" es lo que truena cuentas.
