# Parte 5 de 6 · tareas por fases

> Copia **todo** el bloque y pégalo como un mensaje. Cuando Claude responda «✅ Parte 5/6 recibida», pega la parte 6.

````text
[PARTE 5 DE 6 — SOLO RECIBIR]
NO ejecutes nada todavía: no uses herramientas, no leas ni escribas archivos, no resumas, no empieces ninguna tarea.
Responde ÚNICAMENTE con esta línea exacta y espera la siguiente parte: «✅ Parte 5/6 recibida. Envíame la parte 6.»
Si no tienes la parte 4 en esta conversación, responde solo: «⚠️ Falta la parte 4. Envíala antes de continuar.»
────────── INICIO PARTE 5 DE 6 ──────────
# TAREAS (se ejecutarán en orden SOLO después de la ORDEN FINAL; por ahora solo guárdalas)
## Fase 0 · Orientación
- Lista el árbol de archivos relevante. Sugerencia de comandos:
  - `git ls-files` (si hay Git) o `Get-ChildItem -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '\\(\.git|node_modules|dist|build|\.next|venv|\.venv|__pycache__|coverage)\\' }`
  - `Select-String -Path <archivos> -Pattern '<texto>'` para buscar; `Get-Content <archivo> -TotalCount 200` para leer por partes.
- Detecta el stack por manifiestos (`package.json`, `requirements.txt`, `pyproject.toml`, `composer.json`, `*.csproj`, `Dockerfile`, etc.), puntos de entrada, scripts de build/test y configuración de despliegue.
- Mide: nº de archivos, líneas por lenguaje, tamaño, antigüedad (último commit si hay Git).

## Fase 1 · Inventario y arquitectura
- Módulos/páginas/rutas HTTP/endpoints/componentes/servicios/trabajos programados y cómo se relacionan.
- Modelo de datos: entidades, relaciones, migraciones, índices. Contrasta con las entidades del cerebro de negocio (Proveedor, Guía, Ruta, Oferta, Salida, Reserva, Pago, Payout, Documento, Póliza, Colaborador, Equipo, Checklist).
- Integraciones (pagos, mapas, autenticación, correo, WhatsApp, almacenamiento, analítica): qué usa, con qué configuración (solo nombres de variables).
- Flujos críticos paso a paso con evidencia: registro de guía, creación de ruta, búsqueda, reserva, pago, cancelación/reembolso, check-in, payout.

## Fase 2 · Cobertura frente a las ideas
Para CADA idea I01–I35 asigna un estado: `implementado | parcial | ausente | contradice-norma | no-aplica`, con evidencia (`archivo:línea`), qué falta y esfuerzo estimado (S ≤ 1 día · M ≤ 1 semana · L > 1 semana).

## Fase 3 · Cumplimiento, seguridad y calidad
- Evalúa cada restricción H01–H13 como regla verificable en el producto (por ejemplo: ¿el pie del sitio muestra registro de turismo, LUAF, dirección y teléfono? ¿la capacidad máxima usa 16 y los límites por modalidad? ¿el guía puede cobrar por su cuenta? ¿hay política de cancelación aceptada explícitamente en el checkout?).
- Seguridad: autenticación y autorización por rol, validación de entradas, inyección, XSS/CSRF, subida de archivos, secretos en el repositorio, dependencias vulnerables conocidas (solo por inspección de manifiestos, sin instalar), registro/auditoría.
- Privacidad: datos personales almacenados, retención, consentimiento, exposición de contactos en chats.
- Calidad: pruebas existentes y cobertura, duplicación, tamaño de funciones, manejo de errores, rendimiento móvil, accesibilidad, i18n ES/EN, SEO.

## Fase 4 · Plan de mejora
- Lista priorizada (P0 crítico, P1 importante, P2 deseable) con: problema, evidencia, solución propuesta, esfuerzo S/M/L, dependencias y riesgo de no hacerlo.
- Propón la secuencia que desbloquee primero el piloto «concierge» (3 rutas, pago con retención, dossier de ruta, requisitos del canal virtual).
- Separa «reescribir» de «refactorizar»: no recomiendes reescrituras si un cambio local resuelve el problema.

## Fase 5 · Entrega
Genera la carpeta `cerebro-sitio-web\` con estos archivos (más un archivo `S2x` por cada módulo/funcionalidad relevante):
- `S00 Cobertura de ideas.md` · `S01 Resumen del proyecto.md` · `S02 Arquitectura y stack.md` · `S03 Mapa de modulos y rutas.md` · `S04 Modelo de datos.md` · `S05 Integraciones y configuracion.md` · `S06 Flujos criticos.md` · `S07 Cumplimiento legal en el producto.md` · `S08 Seguridad y privacidad.md` · `S09 Deuda tecnica y calidad.md` · `S10 Brechas y plan de mejora.md` · `S11 Decisiones tecnicas y preguntas abiertas.md` · `S12 Glosario del codigo.md`.
────────── FIN PARTE 5 DE 6 ──────────
Recuerda: NO ejecutes nada. Responde solo «✅ Parte 5/6 recibida. Envíame la parte 6.» y espera.
````
