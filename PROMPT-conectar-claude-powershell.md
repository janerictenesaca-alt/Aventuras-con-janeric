# Prompt para Claude Code en PowerShell (Windows)

Pégalo tal cual en la ventana de PowerShell donde está Claude Code.
Sirve para que ese Claude suba su avance a GitHub y deje un archivo de estado
que Claude Desktop (donde le mandas capturas) pueda leer, y viceversa.

```
Necesito conectar esta conversación con mi Claude Code Desktop y con mi Claude
de la nube. Los tres comparten información SOLO por el repositorio privado
janerictenesaca-alt/nanturia (rama main). Responde siempre en español.

PASO 1 — Diagnóstico (no cambies nada todavía):
- Entra a la carpeta local del proyecto (Escritorio\avturasconjaneric\sitio web
  nanturia) y ejecuta: git status, git log --oneline -10, git remote -v y
  git diff --stat origin/main.
- Dime qué hay SIN commit y SIN push. En el repo de GitHub solo veo
  investigación y docs/ARQUITECTURA-NANTURIA.md, no veo código del sitio; si ya
  tienes código (carpeta app/, package.json, etc.), probablemente está solo en
  mi PC.

PASO 2 — Subir el avance (pídeme confirmación una sola vez antes del push):
- Antes de subir, revisa que NO entren secretos: .env, claves de API, tokens,
  node_modules, .next, carpetas de build ni archivos pesados innecesarios.
  Añade lo que falte a .gitignore.
- Haz commit con un mensaje claro y push a la rama main de
  janerictenesaca-alt/nanturia.

PASO 3 — Crear el archivo de estado: ESTADO-SITIO.md en la raíz del repo, con:
1. Resumen: qué es el sitio hoy y qué porcentaje aproximado está hecho.
2. Pila real que estás usando (framework, estilos, base de datos, hosting) y si
   difiere de docs/ARQUITECTURA-NANTURIA.md.
3. Decisiones que ya tomamos de la sección 10 de ese documento (alcance,
   identidad visual, colores, tipografía, logo, WhatsApp o formulario,
   presupuesto).
4. Páginas y funciones: lista con estado (hecha / a medias / pendiente).
5. Cómo correr el sitio en local (comandos exactos) y la URL local.
6. Qué pantallas conviene que yo revise con capturas en Claude Desktop (lista
   concreta, con la ruta o URL de cada una).
7. Problemas abiertos y siguiente paso recomendado.
Actualiza también la sección "Estado" de CLAUDE.md con una línea fechada que
apunte a ESTADO-SITIO.md. Haz commit y push.

PASO 4 — Protocolo de ida y vuelta (guárdalo en CLAUDE.md, sección "Cómo se
sincronizan las herramientas"):
- Al EMPEZAR cada sesión: git pull, leer CLAUDE.md, ESTADO-SITIO.md y
  FEEDBACK-DESKTOP.md.
- Al TERMINAR cada sesión: actualizar ESTADO-SITIO.md y CLAUDE.md, commit y
  push.
- FEEDBACK-DESKTOP.md es el archivo donde Claude Desktop anotará lo que ve en
  mis capturas de pantalla (qué está mal, qué cambiar, con la pantalla y la
  fecha). Tú lo lees y aplicas esos cambios; cuando termines uno, márcalo como
  hecho en ese mismo archivo.
- Nunca borres entradas de otro Claude; solo añade o marca como hecho.
- Si algo en el estado contradice lo que ves en el código, gana el código y
  corriges el archivo de estado.

Al final dime: qué subiste, qué no pudiste hacer y por qué, y el enlace del
commit.
```

## Cómo se usa el ciclo

1. PowerShell construye el sitio y deja `ESTADO-SITIO.md` al día en GitHub.
2. En Claude Desktop haces `git pull` (o le pides que lea el repo), le mandas
   tus capturas y él escribe sus observaciones en `FEEDBACK-DESKTOP.md`.
3. PowerShell lee ese archivo al empezar y aplica los cambios.
4. La sesión en la nube puede leer y empujar lo mismo desde GitHub.

## Nota

Una conversación no puede "conectarse" a otra directamente: cada Claude solo ve
sus propios mensajes. El repositorio es el puente, y por eso el prompt obliga a
que todo avance quede escrito y subido.
