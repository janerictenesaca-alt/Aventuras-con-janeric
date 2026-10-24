# Reglas de trabajo en este repositorio

Este repositorio es la bóveda de Obsidian del proyecto Nanturia. Entrada: `cerebro nanturia/N15 Mapa del proyecto y guia de colaboracion.md` y `cerebro nanturia/N16 Tablero de pendientes.md`.

## Fuente única, sin duplicados
- El original es la carpeta del PC de Janeric; este repositorio es solo su respaldo. Edita la nota original; no crees copias ni versiones paralelas de una nota.
- `cerebro nanturia/sitio web/` es una copia local de solo lectura, excluida de Git. No se sube.
- No hay generador de notas: los archivos Markdown son la fuente. Edítalos directamente.

## Seguridad
- El repositorio puede ser público: nunca escribas claves, contraseñas, tokens, teléfonos, correos ni datos de clientes.
- No subas `cerebro nanturia/sitio web/` ni `.obsidian/`.

## Formato
- IDs, nombres de archivo y frontmatter: `cerebro nanturia/N13 Convenciones del cerebro.md`.
- Nombres de archivo ASCII, sin `: ? * " < > |`. Enlaces `[[nombre exacto]]`; dentro de tablas el alias va con `\|`.
- Antes de entregar, valida: `node herramientas/cerebro.mjs validar --vault .` (debe dar 0 enlaces rotos).

## Eficiencia
- No imprimas archivos largos completos: lee solo las secciones necesarias.
- Responde corto, con la acción a tomar primero.
