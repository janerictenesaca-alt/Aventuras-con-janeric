# Herramientas del cerebro

`cerebro.mjs` une el cerebro del sitio web con esta bóveda, convierte los identificadores sueltos (`I07`, `H06`, `D02`…) en enlaces reales de Obsidian y valida que no quede nada roto. Necesita **Node 18 o superior** (ya lo tienes por el proyecto del sitio). No instala nada y **nunca modifica las carpetas originales del sitio**: solo las lee.

## Unir el cerebro del sitio con la bóveda de negocio

Ejecuta estos comandos en PowerShell **desde la carpeta raíz del proyecto del sitio** (la que contiene `cerebro-sitio-web` y `cerebro`).

1. Descargar la bóveda **junto** al proyecto, no dentro (una sola vez):

```powershell
git clone --branch claude/youthful-sagan-x9etu3 https://github.com/janerictenesaca-alt/Aventuras-con-janeric.git ..\Aventuras-con-janeric
```

2. Simular primero (no copia ni cambia nada):

```powershell
node ..\Aventuras-con-janeric\herramientas\cerebro.mjs fusionar --vault ..\Aventuras-con-janeric --sitio .
```

3. Si lo que muestra es correcto, aplicar:

```powershell
node ..\Aventuras-con-janeric\herramientas\cerebro.mjs fusionar --vault ..\Aventuras-con-janeric --sitio . --write
```

4. Abrir la carpeta `..\Aventuras-con-janeric` en Obsidian (*Open folder as vault*).

## Qué hace `fusionar`
- Copia `cerebro-sitio-web` a `cerebro nanturia\sitio web\auditoria\` y `cerebro` a `cerebro nanturia\sitio web\proyecto\`. Si el destino ya existe, se detiene (usa `--sobrescribir` solo si quieres reemplazarlo).
- En `auditoria` convierte por defecto `I01`–`I35` y `H01`–`H13` en enlaces a su nota (con `--ids IHDRVAN` también `D##`, `R##`, `V##`, `A##` y `N##`). En `proyecto` **solo corrige rutas**, porque ese cerebro tiene su propia numeración y no debe mezclarse. En tablas escapa la barra `\|`. No toca el frontmatter, los encabezados, los bloques de código, el código en línea ni las URLs, y conserva los finales de línea.
- Corrige enlaces de ruta que quedan rotos al mover carpetas (`[[cerebro/Nota]]` pasa a `[[Nota]]` si el nombre es único).
- Repara archivos en UTF-16 o con BOM (lo que genera `>` en Windows PowerShell 5.1) y los deja en UTF-8.
- Valida toda la bóveda e informa enlaces rotos o ambiguos, nombres repetidos, nombres inválidos en Windows y archivos en UTF-16.

## Comandos sueltos
```powershell
node ..\Aventuras-con-janeric\herramientas\cerebro.mjs validar --vault ..\Aventuras-con-janeric
node ..\Aventuras-con-janeric\herramientas\cerebro.mjs enlazar --vault ..\Aventuras-con-janeric --notas "<carpeta con notas>" --ids IH --write
```
Sin `--write`, `enlazar` y `fusionar` solo simulan.

## Límites
- Los enlaces escritos como `[texto](ruta/archivo.md)` (Markdown clásico) no se corrigen; solo los de Obsidian (`[[…]]`).
- Un identificador escrito solo como texto (por ejemplo «I07») se enlaza siempre; si un código con esa forma significa otra cosa, revísalo.
- Antes de subir estas notas a GitHub, revisa que no contengan datos privados (teléfonos, claves, correos).
