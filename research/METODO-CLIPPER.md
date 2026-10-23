# Método "clipper": guardar y organizar páginas de referencia (equivalente local a Web Clipper)

Objetivo: documentar cada página pública de los sitios de referencia (Capinita y los que indique el usuario) de forma repetible, acumulativa y respetuosa.

## Qué herramientas había (revisado 2026-10-23)
| Herramienta | Estado |
|---|---|
| Nimbus Web Clipper | **No está conectado a Claude** ni comparte datos automáticamente; no se usa ni se instala |
| Claude in Chrome (extensión) | Bloquea capinita.com ("blocked by your site permissions"); solo el usuario puede cambiar esos permisos |
| `browser-use` | Necesita que el usuario active la depuración remota en `chrome://inspect`; no se hizo |
| WebFetch / `curl` | Funcionan para páginas públicas (texto y código servido) |
| Chrome aparte (headless, perfil temporal) | **Funciona**: capturas, DOM, red y consola sin tocar la sesión del usuario |
| Escritura en la carpeta de investigación | Disponible (`research/`) |

## Flujo
1. Comprobar que el sitio figura en `research/clips/sitios-autorizados.txt` (solo lo añade el usuario). El script se niega si no está.
2. Ejecutar desde la raíz del repo:
   `node research/herramientas/clipper.mjs <URL> --sitio=<nombre> [--captura] [--movil] [--forzar]`
   - `--captura`: guarda una captura PNG **solo cuando ayude a documentar algo visual** (`research/capturas/<sitio>/`).
   - `--movil`: emula 390 px (**no probado aún**).
3. El script, en solo lectura (no hace clic, no envía formularios, bloquea toda petición que no sea GET y bloquea la analítica del sitio para no alterarla), registra en `research/clips/<sitio>/<página>.md`: URL exacta y final, canónica, título, sitio, idioma, estado HTTP, fecha y hora, descripción meta, estructura de títulos, navegación (texto→ruta), precios publicados (líneas cortas), llamadas a la acción, campos de formularios (sin enviarlos), diseño medido (fuentes, colores, botón, desborde), medios, tecnología detectada, peticiones por host, errores y límites.
4. **El agente completa a mano** las dos líneas pendientes de cada consulta: **Síntesis fiel** (3–6 líneas con sus palabras, sin copiar) e **Inferencias [I]** (todo lo no comprobado). Nunca se da una inferencia como hecho.
5. Deduplicación: la clave es la URL normalizada (sin `www`, barra final ni `#`). Si el contenido no cambió (misma huella), solo se añade una línea "verificado sin cambios"; si cambió, se añade una sección nueva. **Nunca se sobrescribe un hallazgo.**
6. Índice: `research/clips/indice.json` (datos) y `research/clips/INDICE.md` (vista legible, regenerada). Los fallos se anotan en `research/clips/<sitio>/errores.log`.
7. Citar siempre la URL original en los informes para poder volver a consultarla.

## Reglas de respeto
- Solo páginas públicas y solo lectura: nada de iniciar sesión, formularios, reservas, compras ni panel.
- Solo resúmenes y fragmentos breves (títulos y rótulos); no copiar páginas completas, imágenes, código ni archivos del sitio.
- Capturas solo para documentar un elemento visual; se guardan en el repo y no se reutilizan.
- No instalar extensiones ni programas, no cambiar configuración global, no dar permisos amplios.

## Límites conocidos
- La "huella" se calcula con el texto visible; contenido muy dinámico (fechas, contadores) puede marcar "cambió" sin que haya un cambio relevante.
- Páginas que cargan datos tras interacciones (filtros, pestañas) solo se ven en su estado inicial.
- Entradas de consola se registran de forma básica (a veces solo "Event").
- No ve contenido tras login ni el servidor.
- `--movil` y las capturas a pantalla completa de páginas muy largas no se han validado (la captura se recorta a 2400 px de alto).
