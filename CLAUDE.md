# Aventuras con Janeric

Repositorio para documentar las aventuras de Janeric y las de sus clientes. Contiene guiones para videos en la carpeta `guiones aventurasconjaneric/`.

## Palabra clave: TUTI

Si el usuario escribe **TUTI** (en cualquier combinación de mayúsculas/minúsculas, solo o dentro de un mensaje), ejecuta de inmediato el procedimiento de traspaso de contexto, sin pedir confirmación:

1. Genera UN SOLO bloque de texto, autocontenido y listo para pegar en una sesión nueva, con esta estructura exacta:
   - `## 1. OBJETIVO`: meta final en 2-3 líneas y estado actual en una frase.
   - `## 2. DECISIONES TOMADAS (no reabrir)`: lista numerada, cada una con decisión y motivo en una línea.
   - `## 3. RESTRICCIONES Y REGLAS`: estilo, formato, tono, convenciones y lo que NUNCA se debe hacer.
   - `## 4. ARCHIVOS Y RUTAS`: ruta exacta de cada archivo relevante con una línea de qué contiene o qué se cambió; rama de git activa y último commit relevante.
   - `## 5. TRABAJO COMPLETADO`: qué está terminado y cómo se verificó.
   - `## 6. PENDIENTE (por prioridad)`: cada tarea con qué falta, archivo implicado y criterio de "terminado".
   - `## 7. ERRORES CONOCIDOS Y LECCIONES`: fallas ocurridas, causa y solución.
   - `## 8. ENLACES, PERSONAS Y DATOS EXTERNOS`: URLs, nombres y referencias. Nunca credenciales; solo dónde se guardan.
   - `## 9. SUPUESTOS NO CONFIRMADOS`: todo lo que se dio por cierto sin confirmación.
2. Reglas del bloque: no resumas de más, conserva nombres, cifras y rutas literales, no inventes nada. Si falta un dato, escribe `DESCONOCIDO`.
3. Guarda el bloque en dos sitios:
   - Un archivo NUEVO en `resumenes/` llamado `YYYY-MM-DD_HHMM_resumen.md` (fecha y hora actuales, obténlas con `date`). Nunca borres ni sobrescribas resúmenes anteriores: son el historial y el respaldo.
   - Una copia en `HANDOFF.md` en la raíz del repo (sobrescribiendo el anterior), que es el que se lee al empezar una sesión nueva.
4. Haz commit de ambos archivos con el mensaje `Guarda resumen TUTI YYYY-MM-DD_HHMM` y súbelo a GitHub con `git push -u origin <rama de trabajo actual>`. Si el push falla por red, reintenta hasta 4 veces (2s, 4s, 8s, 16s). No abras pull request.
5. Muestra el bloque en el chat y confirma explícitamente: nombre del archivo creado en `resumenes/`, y si el commit y el push se hicieron bien o fallaron. Termina diciendo: "Listo. Abre un chat nuevo y escribe TUTI para continuar desde aquí."

## Inicio de sesión

Al empezar una sesión nueva, si existe `HANDOFF.md`, léelo antes de hacer cambios y sigue este protocolo:

1. Trátalo como fuente de verdad del proyecto y contrástalo con el estado real de los archivos y el `git log` reciente. Si hay diferencias, repórtalas.
2. Si el usuario escribe TUTI en una sesión nueva (sin nada que traspasar), haz esto en lugar de generar un traspaso: "Antes de seguir, hazme todas las preguntas que necesites para tener la información completa", con las preguntas agrupadas y numeradas. No ejecutes nada hasta que el usuario conteste.
3. Después de las respuestas, resume en 5 líneas lo entendido y espera el "adelante".

## Reglas de trabajo

- Haz cambios pequeños y verificables, y di cómo verificaste cada uno.
- Si algo contradice una decisión de la sección 2 de `HANDOFF.md`, avisa antes de actuar.
- Si el chat se alarga o notas que pierdes detalles (olvidas decisiones, repites errores), avisa al usuario y sugiérele escribir TUTI.
