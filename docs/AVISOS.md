# Avisos por correo a los socios

Cuando alguien abre una tesis, firma, o queda algo esperando, les llega un correo a los
tres. Ya está todo escrito y probado; falta que André conecte cuatro datos.

---

## Por qué no lo manda la app

El terminal es un sitio estático en GitHub Pages. Un navegador **no puede** mandar correo:
haría falta meter la contraseña del correo en el código, que es público. Así que el aviso
sale desde GitHub Actions, que sí corre en un servidor y guarda secretos de verdad.

El costo de hacerlo así es que **no es instantáneo**: el vigilante revisa cada 5 minutos,
que es el intervalo más corto que permite GitHub. Para «hay una tesis esperando tu firma»
alcanza de sobra.

---

## De qué avisa

| Evento | Ejemplo del asunto |
|---|---|
| Tesis nueva esperando firmas | `[Northpoint] Tesis nueva · ES SHORT` |
| Alguien firmó | `[Northpoint] Firma en NQ LONG` |
| Las cuatro firmas completas | `[Northpoint] LISTA PARA EJECUTAR · NQ LONG` |
| Tesis rechazada | `[Northpoint] Tesis rechazada · NQ LONG` |
| Trade con violación de disciplina | `[Northpoint] Violación · MNQ 2026-07-23` |
| Colchón de una cuenta cerca del corte | `[Northpoint] Colchón bajo · T4` |

El correo dice qué pasó, qué falta y a quién le toca. Cada aviso se manda **una sola vez**:
el vigilante guarda lo que ya avisó en `data/avisos-visto.json`.

---

## Lo que falta hacer (todo lo hace André)

### 1 · Los correos ~~faltan~~ ya están puestos ✓

En `data/avisos.json` quedaron los tres:

| Socio | Correo |
|---|---|
| Pablo | `pabloochoa8aM@outlook.com` |
| Mateo | `mateomacouzet2@gmail.com` |
| André | `andremacouzetruiz@gmail.com` |

El de Pablo es Outlook y no hay problema: **los destinatarios pueden ser de cualquier
proveedor**. El único que tiene que ser Gmail es el remitente, porque el envío va por
el SMTP de Google.

### 2 · Crear una contraseña de aplicación de Google

Google no deja que un programa use tu contraseña normal. Hay que generar una específica:

1. La cuenta desde la que van a salir los correos necesita **verificación en dos pasos activada**
   (myaccount.google.com → Seguridad).
2. Entrar a **myaccount.google.com/apppasswords**.
3. Nombre: `Northpoint avisos`. Google devuelve 16 letras.

Esas 16 letras son la `GMAIL_APP_PASSWORD`. **No es la contraseña del correo** y se puede
revocar cuando quieras sin tocar la cuenta.

### 3 · Sacar la llave secreta de Supabase

En el proyecto `spotter-ai` → **Settings → API Keys → Secret keys**, la que empieza con
`sb_secret_…`. El vigilante la necesita porque lee la mesa sin ser ninguno de los tres
socios, y la política RLS sólo deja pasar a los socios.

> **Esa llave nunca va en el repositorio.** Se pega únicamente en los secretos de GitHub,
> que están cifrados y no se pueden leer de vuelta ni desde la propia página.

### 4 · Guardar los cuatro secretos

En GitHub: repositorio → **Settings → Secrets and variables → Actions → New repository secret**.
Cuatro, con estos nombres exactos:

| Nombre | Valor |
|---|---|
| `SUPABASE_URL` | `https://eskpyntqmioiwvaczpcl.supabase.co` |
| `SUPABASE_SERVICE_KEY` | la `sb_secret_…` del paso 3 |
| `GMAIL_USER` | `andremacouzetruiz@gmail.com` (de ahí salen los avisos) |
| `GMAIL_APP_PASSWORD` | las 16 letras del paso 2 |

O con la terminal, que pide cada valor sin dejarlo en el historial:

```bash
gh secret set SUPABASE_URL --repo studioamr/northpoint-capital
gh secret set SUPABASE_SERVICE_KEY --repo studioamr/northpoint-capital
gh secret set GMAIL_USER --repo studioamr/northpoint-capital
gh secret set GMAIL_APP_PASSWORD --repo studioamr/northpoint-capital
```

### 5 · Probarlo

En la pestaña **Actions → Avisos a los socios → Run workflow**. La primera corrida sólo
toma una foto de lo que ya existe y no manda nada — es a propósito, para no inundar a
nadie con la mesa entera. A partir de la segunda avisa sólo lo nuevo.

---

## Ajustes

En `data/avisos.json`:

- `activo: false` apaga todos los avisos sin desconectar nada.
- Cada evento se puede apagar por separado en `avisar`.
- `colchon_minimo` es a partir de qué distancia del corte se avisa (por defecto 700 dólares).

## Si no llegan

| Síntoma | Causa casi siempre |
|---|---|
| El trabajo falla con "Faltan secretos" | Alguno de los cuatro no se guardó o tiene otro nombre |
| Falla en el login de Gmail | Se usó la contraseña normal en vez de la de aplicación |
| Corre pero dice "sin novedades" siempre | Nadie ha tocado la mesa, o la nube no está sincronizando |
| Dice que los correos siguen sin configurar | Falta el paso 1 |

## Lo que este sistema no hace

- **No es instantáneo.** Hay hasta 5 minutos de retraso.
- **Le avisa a los tres de todo.** No filtra por rol; si quieres que a Mateo sólo le
  lleguen las de riesgo, se puede hacer, pero hoy no está.
- **No hay calendario.** Los recordatorios de la ventana de 7:00 o de los payouts
  quincenales serían otro trabajo aparte.
