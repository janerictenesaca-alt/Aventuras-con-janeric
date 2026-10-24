# Parte 1 de 6 · rol, objetivo y reglas de seguridad

> Copia **todo** el bloque y pégalo como un mensaje. Cuando Claude responda «✅ Parte 1/6 recibida», pega la parte 2.

````text
[PARTE 1 DE 6 — SOLO RECIBIR]
NO ejecutes nada todavía: no uses herramientas, no leas ni escribas archivos, no resumas, no empieces ninguna tarea.
Responde ÚNICAMENTE con esta línea exacta y espera la siguiente parte: «✅ Parte 1/6 recibida. Envíame la parte 2.»
────────── INICIO PARTE 1 DE 6 ──────────
Te voy a enviar un prompt largo dividido en 6 partes, una por mensaje, porque no cabe cómodo en uno solo.
REGLAS DEL PROCESO (valen hasta que llegue la orden final):
1. Mientras no recibas la PARTE 6 DE 6, NO ejecutes nada: no uses herramientas, no leas ni escribas archivos, no resumas, no hagas preguntas y no empieces ninguna tarea.
2. Después de cada parte responde ÚNICAMENTE con una línea: «✅ Parte k/6 recibida. Envíame la parte k+1.»
3. Si una parte llega fuera de orden o falta una anterior, responde solo: «⚠️ Falta la parte X. Envíala antes de continuar.»
4. Cuando recibas la PARTE 6 DE 6 (termina con «▶ ORDEN FINAL»), el prompt está completo: EJECÚTALO entero, en orden, empezando por la Fase 0.

# ROL
Eres un ingeniero de software senior y arquitecto de conocimiento. Vas a AUDITAR el proyecto del sitio web de Nanturia que está en el directorio actual y a construir un «cerebro» en Markdown compatible con Obsidian que describa qué existe, cómo funciona, qué falta y qué debe mejorarse. El cerebro se unirá a otro cerebro de negocio ya existente (ideas I01–I35, hallazgos legales H01–H13), por lo que debes respetar sus convenciones.

# OBJETIVO
1. Entender el proyecto completo (stack, módulos, datos, flujos, integraciones, despliegue).
2. Medir la cobertura del código frente al catálogo de ideas de negocio (que recibirás en las partes 3 y 4) y frente a las restricciones legales.
3. Detectar brechas, deuda técnica y riesgos de seguridad/privacidad.
4. Proponer un plan de mejora priorizado y accionable.
5. Entregar todo como notas Markdown enlazadas (wikilinks de Obsidian) con frontmatter YAML.

# REGLAS DE SEGURIDAD Y ENTORNO (Windows / PowerShell)
- El código es de SOLO LECTURA. Escribe únicamente dentro de `.\cerebro-sitio-web\` (créala). No modifiques, muevas ni borres nada fuera de ella.
- Prohibido: `Remove-Item`, `git reset`, `git clean`, `git push`, instalar paquetes, ejecutar el sitio con datos reales, hacer peticiones de red o abrir conexiones a bases de datos de producción. Si crees que necesitas algo así, DETENTE y pregunta.
- SECRETOS: nunca copies valores de `.env`, claves API, tokens, contraseñas ni cadenas de conexión. Registra solo el NOMBRE de la variable, su propósito y dónde se usa; el valor aparece como `[REDACTADO]`. Si encuentras un secreto escrito en el código, repórtalo como hallazgo crítico (sin reproducirlo).
- Excluye de los barridos: `.git`, `node_modules`, `dist`, `build`, `.next`, `.venv`, `venv`, `__pycache__`, `coverage` y binarios; los archivos de más de 1 MB solo se listan.
- CODIFICACIÓN: escribe en UTF-8 sin BOM. En Windows PowerShell 5.1, `>` y `Out-File` generan UTF-16: NO los uses. Escribe con tu herramienta de archivos o con `[System.IO.File]::WriteAllText($ruta, $texto, (New-Object System.Text.UTF8Encoding($false)))`.
- Nombres de archivo en ASCII, sin acentos ni los caracteres `: ? * " < > |`. Formato: `S## Titulo corto.md`.
- Si el repositorio `Aventuras-con-janeric` existe localmente, DESPUÉS de la ORDEN FINAL lee primero en `cerebro nanturia\`: `N00 Resumen ejecutivo`, `N03 Hallazgos criticos`, `N06 Arquitectura de plataforma`, `N13 Convenciones del cerebro`. Si no existe, usa el contexto de este prompt.
- No inventes. Si algo no se puede determinar del código, escribe «no determinado» y di qué evidencia faltó. Cada afirmación técnica lleva evidencia `ruta\archivo:línea`.
────────── FIN PARTE 1 DE 6 ──────────
Recuerda: NO ejecutes nada. Responde solo «✅ Parte 1/6 recibida. Envíame la parte 2.» y espera.
````
