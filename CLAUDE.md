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
- Pendiente: definir el proyecto concreto (ver README.md).

## Cómo se sincronizan las herramientas
- Claude Code local (Windows) controla Chrome con `/chrome`. Es la única que ve el navegador.
- Claude Code en la nube trabaja el repo y empuja a GitHub.
- Claude Desktop: abrirlo y usar el mismo correo; reutiliza los conectores.
- Todos intercambian información por este repo (CLAUDE.md), no por memoria propia.
