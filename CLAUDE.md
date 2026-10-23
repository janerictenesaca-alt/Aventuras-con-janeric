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
- 2026-10-22 (Claude Code local, Windows): Repo clonado en C:vturasconjanericepo, rama claude/magical-babbage-nxlkef. Leídos CLAUDE.md y SYNC.md.
  - OK: Chrome conectado; creé mi propia ventana con pestaña nueva (tabGroup 367159863) porque no había pestañas del usuario visibles.
  - OK: Claude Desktop estaba instalado pero cerrado; lo abrí (proceso Claude.exe en ejecución).
  - NO verificado: que Desktop use la misma cuenta (janerictenesaca@gmail.com); no inspeccioné su sesión.
  - Falló/no aplica: `/chrome` es comando interactivo, no ejecutable desde aquí; verifiqué la conexión llamando directamente a las herramientas de Chrome. `gh` no está instalado (se usó git).
- 2026-10-23 (Claude Code nube): Leí el estado de la sesión local (Chrome y Desktop OK). No puedo ver Chrome ni Desktop desde la nube; solo repo y GitHub. Falta: confirmar cuenta de Desktop y definir el proyecto.
- 2026-10-23 (usuario + nube): Extensión Claude in Chrome ya con sesión iniciada (Jan · Pro); el panel lateral responde. Chrome, Code y Desktop quedan en la misma cuenta.
- Pendiente: definir el proyecto concreto (ver README.md).

## Cómo se sincronizan las herramientas
- Claude Code local (Windows) controla Chrome con `/chrome`. Es la única que ve el navegador.
- Claude Code en la nube trabaja el repo y empuja a GitHub.
- Claude Desktop: abrirlo y usar el mismo correo; reutiliza los conectores.
- Todos intercambian información por este repo (CLAUDE.md), no por memoria propia.
