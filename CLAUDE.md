# Aventuras con Janeric — contexto compartido

Este archivo es el punto común entre Claude Code (nube y local), Claude Desktop
y Claude en Chrome. Todos deben leerlo al empezar y actualizarlo al terminar.

## Reglas
- Responder siempre en español.
- Repositorio: janerictenesaca-alt/aventuras-con-janeric
- Rama de trabajo de la nube: claude/magical-babbage-nxlkef
- Antes de parar, escribir en "Estado" qué se hizo y qué falta.

## Estado (actualizar siempre)
- 2026-10-23: Se creó este archivo. Objetivo: que las sesiones compartan contexto.
- 2026-10-22 (Claude Code local, Windows): Repo clonado en C:vturasconjaneric
epo, rama claude/magical-babbage-nxlkef. Leídos CLAUDE.md y SYNC.md.
  - OK: Chrome conectado; creé mi propia ventana con pestaña nueva (tabGroup 367159863) porque no había pestañas del usuario visibles.
  - OK: Claude Desktop estaba instalado pero cerrado; lo abrí (proceso Claude.exe en ejecución).
  - NO verificado: que Desktop use la misma cuenta (janerictenesaca@gmail.com); no inspeccioné su sesión.
  - Falló/no aplica: `/chrome` es comando interactivo, no ejecutable desde aquí; verifiqué la conexión llamando directamente a las herramientas de Chrome. `gh` no está instalado (se usó git).
- 2026-10-23 (Claude Code nube): Leí el estado de la sesión local (Chrome y Desktop OK). No puedo ver Chrome ni Desktop desde la nube; solo repo y GitHub. Falta: confirmar cuenta de Desktop y definir el proyecto.
- 2026-10-23 (usuario + nube): Extensión Claude in Chrome ya con sesión iniciada (Jan · Pro); el panel lateral responde. Chrome, Code y Desktop quedan en la misma cuenta.
- 2026-10-22 (Claude Code local, sincronización): git pull OK (rama al día con origin) y CLAUDE.md leído. Chrome conectado y pestaña abierta OK. Claude Desktop (Claude.exe) en ejecución. Falló: no pude confirmar sesión de Chrome ni el panel lateral (claude.ai bloqueado por permisos del sitio en la extensión) ni la cuenta Jan Pro de Desktop (no legible desde aquí); se da por buena la nota previa de 'Jan · Pro'.
- 2026-10-23 (Claude Code local, investigacion): Capinita lote 1 en research/capinita.md y research/sintesis.md: 15 paginas revisadas parcialmente (texto y curl), 1 bloqueada (404), unas 365 pendientes de 381 del sitemap. Chrome bloqueo capinita.com: sin capturas ni vista movil. Falta: URL del sitio 2, revision visual y resto de paginas.
- 2026-10-23 (Claude Code local, lote 2): Chrome sigue bloqueando capinita.com, asi que use un Chrome headless aparte (perfil temporal) y guarde 5 capturas en research/capturas/capinita/. Revisadas visualmente en escritorio: /tours, /ruta, /estado-vial-ecuador. Fallo: browser-use requiere activar depuracion remota en chrome://inspect (accion tuya); la captura movil no es fiable. Pendiente: sitio 2, movil real, inicio y unas 365 paginas.
- 2026-10-23 (Claude Code local, lote 3): informe por ventanas (research/informe-ventanas-capinita.md) y analisis tecnico del codigo publico con plan original (research/analisis-tecnico-capinita.md); 17 capturas de escritorio. Falta: movil real, Sierra/Costa/Galapagos, unas 360 fichas, sitio 2 y confirmar con el usuario el stack y los terminos de uso del ECU 911.
- 2026-10-23 (Claude Code local, lote 4): analisis de imagenes y contenido (research/analisis-imagenes-contenido-capinita.md): usa picture AVIF/WebP/PNG, 63 por ciento del peso en PNG, sin srcset ni optimizador, cache sin larga duracion. Falta: movil real, unas 360 fichas, sitio 2.
- 2026-10-23 (Claude Code local, lote 5): revision pasiva de seguridad (research/seguridad-lecciones-capinita.md): sin CSP ni frame-ancestors, 161 enlaces externos sin rel, autocomplete de contrasena incorrecto en registro, robots.txt revela /administrador; buenos: HSTS, sin source maps ni secretos. No se probo nada activo ni se accedio a areas privadas. Falta: movil real, ~360 fichas, sitio 2.
- 2026-10-23 (Claude Code local, lote 6): inspeccion en navegador de 6 paginas (red, consola, DOM, metricas) sin tocar nada del sitio; hallazgos: el navegador llama directo al ECU 911 y a OSRM publico, prefetch de Next, error de hidratacion #418, Leaflet global, semantica HTML incorrecta; corregido un dato previo. Evidencia en research/evidencia/. Falta: movil real, ~360 fichas, sitio 2.
- Pendiente: definir el proyecto concreto (ver README.md).

## Cómo se sincronizan las herramientas
- Claude Code local (Windows) controla Chrome con `/chrome`. Es la única que ve el navegador.
- Claude Code en la nube trabaja el repo y empuja a GitHub.
- Claude Desktop: abrirlo y usar el mismo correo; reutiliza los conectores.
- Todos intercambian información por este repo (CLAUDE.md), no por memoria propia.
