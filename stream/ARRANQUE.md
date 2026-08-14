# NORTHPOINT · Arranque del stream — sesión de ASIA

Todo lo que hace falta para salir al aire hoy. La sesión de Asia corre
**18:00 – 01:35 hora de Nueva York** (16:00 – 23:35 en Morelia).

---

## 1 · Dónde sí puedes salir HOY

| Plataforma | Estado | Qué falta |
|---|---|---|
| **Kick** | ✅ **listo** — conectado y activo en Restream | nada, se puede hoy |
| YouTube | ⛔ bloqueado | activar *live streaming* en el canal: verificación por teléfono + **24 h** de espera |
| Facebook | ⛔ bloqueado por Meta | perfil con **+60 días** de antigüedad y **100 seguidores** de página |
| Twitch | ⛔ sin sesión | iniciar sesión una vez y Restream lo conecta solo |

**El estreno de hoy es por Kick.** Los demás entran solos al destrabarse: el
show de Restream ya reparte a todos los canales activos.

---

## 2 · Las escenas (Browser source en OBS o Restream Studio)

Un solo archivo, cuatro escenas. **Tamaño 1920×1080** en todas.

| Escena | URL |
|---|---|
| **En vivo** (transparente, sobre el chart) | `stream/overlay.html` |
| Empezamos en breve | `stream/overlay.html?escena=espera` |
| Volvemos en un momento | `stream/overlay.html?escena=pausa` |
| Sesión cerrada | `stream/overlay.html?escena=cierre` |

También sirven en línea, sin abrir archivos:

- `https://studioamr.github.io/northpoint-capital/stream/overlay.html`
- `…/overlay.html?escena=espera`

**Cómo montarlo en OBS** (3 minutos):

1. Fuente → **Navegador**
2. URL: la de arriba · Ancho **1920** · Alto **1080**
3. Deja marcado *"Apagar la fuente cuando no esté visible"* — así el reloj
   siempre reinicia limpio
4. La escena en vivo es **transparente**: pon debajo tu captura de pantalla
   (los dos charts) y el overlay flota encima

El reloj, la sesión activa, la barra de progreso y el "3h 30m LEFT" son
**reales**: los calcula el mismo modelo del Terminal, en hora de Nueva York.

---

## 3 · El orden del stream de hoy (60–90 min)

1. **Pantalla de espera** 3–5 min antes — deja que llegue gente
2. **Presentación (2 min)** — quién eres, qué es NORTHPOINT, qué van a ver
3. **El plan de la sesión (5 min)** — niveles marcados, qué esperas, qué NO
   sería trade hoy
4. **La espera** — aquí vive el contenido: explica lo que ves mientras no
   pasa nada. La paciencia *es* el show
5. **El trade (o el no-trade)** — pase lo que pase, se narra
6. **El journal en cámara (5 min)** — abre el Terminal y escribe el día
7. **Cierre** — recuerda el Discord y la hora de mañana

**En cámara se dice el QUÉ, nunca el CÓMO.** Nada de parámetros del método,
horarios exactos de la ventana, ni ajustes de los indicadores. Eso se
entrega en persona, dentro del programa.

---

## 4 · Título y descripción (ya cargados en Restream)

**Título** — `NORTHPOINT · Live Futures Desk`
Para hoy puedes ponerlo más específico:
`NORTHPOINT · Asia Session Live — One Trade a Day`

**Descripción**
> The NORTHPOINT desk, live — futures from the New York session, Mon–Fri.
> The firm: studioamr.github.io/northpoint-capital
> Join the community: discord.gg/TWeVqTTPS

---

## 5 · Antes de darle "En vivo" — la lista de 8

- [ ] Restream abierto con el show **NORTHPOINT · Live Futures Desk**
- [ ] Kick encendido (toggle azul) en la lista de canales
- [ ] Escena de espera al aire 3 min antes
- [ ] Los dos charts acomodados (5M contexto · 1M ejecución)
- [ ] **Terminal cerrado o en la pantalla que NO se comparte** — ahí viven
      cuentas, saldos y claves
- [ ] Micrófono probado (habla 10 s y escucha la grabación)
- [ ] Notificaciones del sistema en silencio
- [ ] Agua a la mano — la sesión es larga y el show es la espera
