# Avisos por correo a los socios

Dos cosas distintas mandan correo a los tres socios:

- **el vigilante**, que revisa la mesa cada 5 minutos y avisa de lo que cambió;
- **los recordatorios**, que salen por reloj de lunes a viernes.

Ya está todo escrito y probado; falta que André conecte tres datos.

---

## Por qué no lo manda la app

El terminal es un sitio estático en GitHub Pages. Un navegador **no puede** mandar correo:
haría falta meter la contraseña del correo en el código, que es público. Así que el aviso
sale desde GitHub Actions, que sí corre en un servidor y guarda secretos de verdad.

El costo de hacerlo así es que **no es instantáneo**: el vigilante revisa cada 5 minutos,
que es el intervalo más corto que permite GitHub, y los cron pueden retrasarse unos
minutos más cuando el servicio anda cargado. Para «hay una tesis esperando tu firma»
alcanza de sobra.

---

## De qué avisa cuando algo cambia

| Evento | Ejemplo del asunto |
|---|---|
| Tesis nueva esperando firmas | `[Northpoint] Tesis nueva · ES SHORT` |
| Alguien firmó | `[Northpoint] Firma en NQ LONG` |
| Las cuatro firmas completas | `[Northpoint] LISTA PARA EJECUTAR · NQ LONG` |
| Tesis rechazada | `[Northpoint] Tesis rechazada · NQ LONG` |
| **Se registró un trade** | `[Northpoint] Trade · MNQ SHORT $600` |
| Trade con violación de disciplina | `[Northpoint] Violación · MNQ 2026-07-23` |
| Colchón de una cuenta cerca del corte | `[Northpoint] Colchón bajo · T4` |
| **Una cuenta cambió de fase** | `[Northpoint] Cambio de fase · T1` |
| **Una cuenta llegó a su objetivo** | `[Northpoint] Objetivo alcanzado · T1` |

El correo del trade trae todo: quién lo metió, instrumento, contratos, entrada y salida,
el P&L por cuenta y multiplicado por el copiador, si el setup era válido, cuánto lleva
la mesa ese día y cuánto falta para la meta. Si fue el segundo del día, lo dice: la
sesión se cierra ahí.

Cada aviso se manda **una sola vez**: el vigilante guarda lo que ya avisó en
`data/avisos-visto.json`.

La excepción es el colchón. Avisar una vez y callarse mientras la cuenta se hunde sería
inútil, así que se guarda con cuánto se avisó y vuelve a avisar cada que empeora otros
`colchon_paso` dólares (150 por defecto). Si el colchón se recupera por encima del
límite, el registro se borra y queda armado otra vez.

---

## El primer correo del día: overnight

A las **6:20**, antes que nada, le llega a cada socio **su propio correo** (no una copia
compartida) con lo que pasó mientras la mesa dormía:

- **Gráficas** del overnight de NQ y ES, con máximo, mínimo y cierre previo marcados.
- Cuánto se movió cada instrumento: NQ, ES, YM, RTY, oro, petróleo, dólar y el VIX.
- El **rango del overnight** de cada uno y dónde quedó el precio dentro de él — esos
  extremos son la liquidez que el rompimiento va a buscar.
- Los eventos rojos del día y los titulares de la noche.

Todo va también en texto, así que quien tenga las imágenes bloqueadas no se pierde nada.
Este correo **no depende de Supabase**: sale aunque la nube esté caída.

---

## De qué avisa por reloj

Lunes a viernes, hora de la mesa (Morelia):

| Hora | Asunto | Qué trae además |
|---|---|---|
| 6:20 | `Overnight · 23 jul` | Gráficas y niveles de la noche (arriba) |
| 6:50 | `La ventana abre a las 7:00` | Tesis firmadas sin ejecutar, tesis esperando firma, meta y riesgo del día |
| 7:20 | `El rango de apertura es a las 7:30` | La regla del rompimiento y el máximo de dos trades |
| 8:35 | `Cerró la ventana` | Los trades del día con su P&L y si se cumplió la meta |
| 9:00 los días 1 y 16 | `Corte quincenal` | Balance, fase y colchón de cada cuenta |

El de la apertura sale 6:50 y no 6:55 **a propósito**: GitHub retrasa los cron varios
minutos cuando hay carga, y más vale que llegue diez minutos antes a que llegue tarde.
Por la misma razón no hay que tomar la hora del correo como cronómetro.

El texto de cada uno se edita en `data/avisos.json` sin tocar código.

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

En **Actions → Avisos a los socios → Run workflow**. La primera corrida sólo toma una
foto de lo que ya existe y no manda nada — es a propósito, para no inundar a nadie con
la mesa entera. A partir de la segunda avisa sólo lo nuevo.

Lo mismo aplica al estrenar los avisos de trade: la primera corrida después de esta
actualización los fotografía en silencio en vez de mandar un correo por cada trade viejo.

Para probar un recordatorio sin esperar a mañana: **Actions → Recordatorios de la mesa →
Run workflow**, se elige cuál y se marca «forzar».

---

## Ajustes

Todo en `data/avisos.json`, sin tocar código:

- `activo: false` apaga **todo** sin desconectar nada.
- Cada evento se apaga por separado en `avisar`.
- Cada recordatorio se apaga con su propio `activo`, y su texto se edita en `cuerpo`.
- `colchon_minimo` (700) es a partir de qué distancia del corte se avisa;
  `colchon_paso` (150) es cuánto tiene que empeorar para volver a avisar.
- `dias_del_mes` del recordatorio de quincena decide en qué días sale (hoy 1 y 16).

### Si el equipo cambia de huso horario

La mesa opera en hora de Morelia, que es UTC-6 todo el año porque México ya no cambia
horario. Eso vive en **dos lugares que tienen que coincidir**: `utc_offset` en
`data/avisos.json` y los cron de `recordatorios.yml` y `overnight.yml`, que van en UTC
(hora local + 6). Si se cambia uno sin el otro, los avisos salen a deshoras.

`utc_offset` también es lo que usa `scripts/mercado.py` para traducir el calendario
económico, así que un cambio ahí arregla las tres cosas de un solo lugar.

### La hora del calendario económico

La fuente entrega cada evento en **hora de Nueva York**. Antes se guardaba ese número
pelón y el terminal lo mostraba como si fuera hora de la mesa: dos horas de diferencia
justo en la regla que dice que no se opera si un evento rojo cae en la ventana. Un ECB
a las 8:15 ET son las 6:15 aquí — *antes* de abrir, no adentro.

Ahora `hora` y `dia` van siempre en hora de la mesa, que es lo que la gente lee, y la de
Nueva York queda al lado como referencia (`hora_ny`) porque casi todo el material de
trading habla en ET. El terminal muestra las dos y lo dice en el encabezado.

## Si no llegan

| Síntoma | Causa casi siempre |
|---|---|
| El trabajo falla con "Faltan secretos" | Alguno de los cuatro no se guardó o tiene otro nombre |
| Falla en el login de Gmail | Se usó la contraseña normal en vez de la de aplicación |
| Corre pero dice "sin novedades" siempre | Nadie ha tocado la mesa, o la nube no está sincronizando |
| El recordatorio dice "ya se mandó hoy" | GitHub disparó el cron dos veces; el segundo se descarta solo |
| Los recordatorios llegan tarde | Retraso de GitHub; no hay forma de garantizar el minuto exacto |
| Llegan los de reloj pero no los de la mesa | El vigilante es otro trabajo: revisar Actions → Avisos a los socios |

## Lo que este sistema no hace

- **No es instantáneo.** Hay hasta 5 minutos de retraso en los avisos de la mesa, y los
  recordatorios pueden salir unos minutos después de su hora.
- **Le avisa a los tres de todo.** No filtra por rol; si quieres que a Mateo sólo le
  lleguen las de riesgo, se puede hacer, pero hoy no está.
- **No sabe de días festivos.** Los recordatorios salen los cinco días hábiles aunque
  el mercado esté cerrado.
- **Sólo ve lo que llegó a la nube.** Si un socio registra trades sin sincronizar, el
  vigilante no se entera hasta que suban.
