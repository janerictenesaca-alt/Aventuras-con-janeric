# Prompt para Claude en PowerShell — Cerebro del sitio web de Nanturia

> Cómo usarlo: abre PowerShell en la carpeta raíz del proyecto del sitio web, inicia Claude Code y pega **todo lo que está dentro del bloque** de abajo. Resultado esperado: una carpeta `cerebro-sitio-web\` con notas en Markdown compatibles con Obsidian, lista para copiarse a la bóveda `cerebro nanturia\sitio web\`.

````text
# ROL
Eres un ingeniero de software senior y arquitecto de conocimiento. Vas a AUDITAR el proyecto del sitio web de Nanturia que está en el directorio actual y a construir un «cerebro» en Markdown compatible con Obsidian que describa qué existe, cómo funciona, qué falta y qué debe mejorarse. El cerebro se unirá a otro cerebro de negocio ya existente (ideas I01–I35, hallazgos legales H01–H13), por lo que debes respetar sus convenciones.

# OBJETIVO
1. Entender el proyecto completo (stack, módulos, datos, flujos, integraciones, despliegue).
2. Medir la cobertura del código frente al catálogo de ideas de negocio (abajo) y frente a las restricciones legales.
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
- Si el repositorio `Aventuras-con-janeric` existe localmente, lee primero en `cerebro nanturia\`: `N00 Resumen ejecutivo`, `N03 Hallazgos criticos`, `N06 Arquitectura de plataforma`, `N13 Convenciones del cerebro`. Si no existe, usa el contexto de este prompt.
- No inventes. Si algo no se puede determinar del código, escribe «no determinado» y di qué evidencia faltó. Cada afirmación técnica lleva evidencia `ruta\archivo:línea`.

# CONTEXTO DE NEGOCIO (resumen)
Nanturia es una agencia de viajes digital (marketplace vertical de tours de aventura y cultura en Ecuador, piloto en Morona Santiago). Vende, cobra, verifica y respalda tours operados por guías y operadoras habilitadas; gana comisión por canal y un fee de reserva. Piezas clave: salidas compartidas con precio decreciente por tamaño de grupo, pagos con retención y payout a T+2, dossier legal por ruta generado con plantillas, modo guía y modo turista, chat enmascarado, atribución por QR/links, rutas sin dueño (ficha única, varios proveedores), ES/EN.

# RESTRICCIONES LEGALES CRÍTICAS (el código debe respetarlas; valídalas como reglas)
- H01 · Intermediación solo vía agencia de viajes registrada → Vender tours es intermediación: la entidad que vende y factura debe ser una agencia de viajes registrada (mostrar registro y LUAF); ningún flujo presenta a un guía individual como vendedor.
- H02 · Aventura solo vía agencia, el guía no puede operar directo → Las modalidades de aventura (excepto senderismo) solo se asignan a proveedores tipo operador/agencia declarada; un guía sin agencia no puede publicar ni operar rafting, canyoning, cuevas, etc.
- H03 · El guía no puede hacer agenciamiento turístico → El guía no cobra ni contrata por su cuenta; los links de guía son «referidos» y la venta, el cobro y la factura son de la agencia.
- H04 · Tope de grupo de 16 y límites por modalidad → Capacidad por salida = min(16, límite del sitio, ratio por modalidad × guías asignados); nunca sobreasignar (ej.: canyoning 4, cabalgata 8, senderismo 8 por guía).
- H05 · Escalera de licencias distinta a la de los audios → Elegibilidad del guía por clasificación + ámbito (local = solo su cantón; nacional/aventura = continental en modalidades acreditadas) + vigencia de 4 años; no asumir una cadena local→aventura→nacional.
- H06 · La plataforma responde ante el cliente → Ante falla del proveedor el sistema reembolsa o sustituye al cliente y recobra del proveedor; nunca remite al cliente a reclamar al guía ni expone datos de contacto.
- H07 · Reserva no reembolsable vs derechos del usuario y retracto → Separar fee de reserva (no reembolsable salvo falla nuestra) y depósito (reembolsable por calendario); aceptación explícita de la política en el checkout.
- H08 · Requisitos obligatorios del canal virtual → El sitio muestra registro de turismo, LUAF, dirección física, correo, teléfono, seguridad de pago, protección de datos, declaración de responsabilidad, políticas de cobro/cancelación/reembolso y teléfono de asistencia.
- H09 · Teléfono de emergencia 24 h y chat sin contacto directo → La orden de servicio incluye teléfono de emergencia 24 h de la agencia (no del guía); el chat enmascarado no sustituye esa línea.
- H10 · Oficina física obligatoria para la agencia → La agencia tiene domicilio físico (oficina/coworking): el pie del sitio y los documentos legales muestran una dirección física real.
- H11 · Seguros obligatorios y monto sin verificar → Bloquear la venta si la póliza (RC y accidentes) del operador está vencida o no cubre la modalidad; alertas de vigencia.
- H12 · Comisiones a hoteles y transporte y prohibición de intermediar → No activar comisiones a hoteles/restaurantes/transportistas por «vender»; permitir QR de medición y pagos solo bajo la figura validada.
- H13 · Autoridad en transición y vigencia de textos → Guardar fecha de última verificación de cada norma y parametrizar requisitos legales (topes, ratios, vigencias) en configuración, no en constantes de código.
Aviso: lo anterior no es asesoría legal; marca cada regla como «cumple», «parcial», «incumple» o «no determinado».

# CATÁLOGO DE IDEAS DE NEGOCIO A CONTRASTAR CON EL CÓDIGO
- I01 · Modelo en cadena con operadoras aliadas — área: modelo · prioridad: alta · fase: F0 · riesgo legal: medio
- I02 · «Solo un medio»: traslado de responsabilidad al guía — área: legal-modelo · prioridad: alta · fase: F0 · riesgo legal: alto
- I03 · Red de operadoras revendedoras y consolidación de grupos — área: modelo · prioridad: alta · fase: F2 · riesgo legal: medio
- I04 · Tours internacionales para ecuatorianos vía operadoras aliadas — área: modelo · prioridad: baja · fase: F3 · riesgo legal: medio
- I05 · Alianzas ancla: Cueva de los Tayos (Mateo) y empresa de Hernán — área: modelo · prioridad: alta · fase: F0 · riesgo legal: medio
- I06 · Reclutamiento de guías desde el Catastro Turístico — área: crecimiento · prioridad: media · fase: F2 · riesgo legal: medio
- I07 · Pagos: retención de fondos, split y fondo de respaldo — área: pagos · prioridad: alta · fase: F1 · riesgo legal: medio
- I08 · Reserva no reembolsable — área: pagos · prioridad: alta · fase: F1 · riesgo legal: alto
- I09 · Precio decreciente por tamaño de grupo («escalera de precios») — área: precios · prioridad: alta · fase: F1 · riesgo legal: bajo
- I10 · Estructura de precios, comisión y pago justo al guía — área: precios · prioridad: alta · fase: F0 · riesgo legal: bajo
- I11 · Paridad de precios entre operadoras y transporte desde distintas ciudades — área: precios · prioridad: media · fase: F2 · riesgo legal: medio
- I12 · Cancelaciones y no-shows del cliente (pérdida propia por entradas prepagadas) — área: operación · prioridad: alta · fase: F1 · riesgo legal: bajo
- I13 · Incumplimiento del guía (no activa el tour o no se presenta) — área: operación · prioridad: alta · fase: F1 · riesgo legal: medio
- I14 · Plataforma estilo Airbnb solo para tours, con mapa y horarios de buses — área: producto · prioridad: alta · fase: F1 · riesgo legal: bajo
- I15 · Modo turista y modo guía; asistente de creación de rutas — área: producto · prioridad: alta · fase: F1 · riesgo legal: bajo
- I16 · Bot intermediario cliente↔guía y prevención de fuga de datos — área: producto · prioridad: media · fase: F2 · riesgo legal: medio
- I17 · Flujo de reserva con confirmación de disponibilidad — área: producto · prioridad: alta · fase: F1 · riesgo legal: bajo
- I18 · Automatización de la documentación legal por ruta («proyecto de ruta») — área: legal-operación · prioridad: alta · fase: F0 · riesgo legal: alto
- I19 · Almacenamiento documental («nube física»/NAS) y registro de equipos con QR — área: operación · prioridad: media · fase: F0 · riesgo legal: bajo
- I20 · Asignación automática de guía, cupos y desbordamiento — área: producto · prioridad: media · fase: F2 · riesgo legal: bajo
- I21 · Rutas sin dueño: ficha única y múltiples proveedores — área: producto · prioridad: media · fase: F2 · riesgo legal: medio
- I22 · Biblioteca de rutas precreadas y onboarding («departamento de creación de rutas») — área: crecimiento · prioridad: alta · fase: F0 · riesgo legal: bajo
- I23 · Ranking y visibilidad de guías, operadoras y colaboradores — área: producto · prioridad: media · fase: F2 · riesgo legal: bajo
- I24 · Códigos QR en hoteles, atribución de origen y comisión a colaboradores — área: crecimiento · prioridad: alta · fase: F0 · riesgo legal: alto
- I25 · Complementos de hospedaje y transporte (aceptar u omitir) — área: producto · prioridad: media · fase: F2 · riesgo legal: medio
- I26 · Rutas digitales 3D, datos de ruta de pago y explicaciones de pago — área: producto · prioridad: baja · fase: F3 · riesgo legal: medio
- I27 · Co-venta entre guías de una ciudad para llenar el bus (pooling de transporte) — área: modelo · prioridad: media · fase: F2 · riesgo legal: medio
- I28 · Enlaces de pago y de ruta compartibles (marketing viral) — área: crecimiento · prioridad: alta · fase: F1 · riesgo legal: medio
- I29 · Seguros y requisitos de las plataformas globales — área: legal · prioridad: alta · fase: F0 · riesgo legal: alto
- I30 · Marco legal de los guías, ámbitos y plan de habilitación — área: legal · prioridad: alta · fase: F0 · riesgo legal: medio
- I31 · Estrategia de confianza frente a Booking, Airbnb, TripAdvisor y Viator — área: crecimiento · prioridad: alta · fase: F0 · riesgo legal: bajo
- I32 · MVP concierge: sitio básico, tours cargados, prueba y error — área: estrategia · prioridad: alta · fase: F0 · riesgo legal: bajo
- I33 · Equipos y seguridad: arnés en El Churo y alquiler de equipos — área: operación · prioridad: media · fase: F0 · riesgo legal: medio
- I34 · Expansión: nacional primero, internacional después — área: estrategia · prioridad: media · fase: F3 · riesgo legal: medio
- I35 · Agente de ventas con IA (bot de ventas 24/7) — área: producto · prioridad: media · fase: F3 · riesgo legal: medio

# TAREAS (ejecuta en orden y deja constancia de cada fase)
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

# FORMATO DE CADA NOTA
Frontmatter YAML obligatorio (mismo esquema que el cerebro de negocio):
```yaml
---
id: S06
tipo: sitio-web
titulo: Flujos criticos
estado: analizada          # borrador | analizada | verificada
prioridad: alta            # alta | media | baja
origen: [codigo]
archivos: [src/checkout/pay.ts, src/api/bookings.ts]
cobertura: [I07: parcial, I08: ausente]
hallazgos: [H06: incumple]
confianza: media           # alta | media | baja
tags: [sitio-web, pagos]
---
```
Cuerpo: Resumen · Evidencia (ruta:línea) · Análisis · Brechas · Mejora propuesta · Esfuerzo · Riesgos · Próximos pasos · Relacionadas. Enlaza con wikilinks a las notas del cerebro de negocio por su nombre de archivo, por ejemplo `[[I07 Pagos retencion de fondos split y fondo de respaldo|I07]]` o `[[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente|H06]]`, y entre notas del sitio web con `[[S06 Flujos criticos]]`. Las reglas verificables van en bloques ```text con pseudocódigo.

# CRITERIOS DE CALIDAD (autoevalúate antes de entregar)
- [ ] Ninguna afirmación sin evidencia `archivo:línea` o marcada «no determinado».
- [ ] Ningún secreto copiado; hallazgos de secretos reportados sin reproducir el valor.
- [ ] Las 35 ideas aparecen en `S00` con estado y esfuerzo; los 13 hallazgos legales en `S07` con estado.
- [ ] Todos los wikilinks apuntan a archivos existentes (valida con el script de abajo).
- [ ] Lenguaje técnico, preciso y conciso; sin relleno.
- [ ] Archivos en UTF-8 sin BOM y nombres ASCII.

Script de validación de enlaces (ajusta `$extra` a la carpeta del cerebro de negocio si la tienes):
```powershell
$root  = (Resolve-Path .\cerebro-sitio-web).Path
$extra = "..\Aventuras-con-janeric\cerebro nanturia"   # opcional
$names = @(); foreach ($p in @($root, $extra)) { if (Test-Path $p) { $names += Get-ChildItem $p -Recurse -Filter *.md | ForEach-Object { $_.BaseName } } }
Get-ChildItem $root -Recurse -Filter *.md | ForEach-Object {
  $txt = Get-Content $_.FullName -Raw -Encoding UTF8
  [regex]::Matches($txt, '\[\[([^\]\|#]+)') | ForEach-Object {
    $t = $_.Groups[1].Value.Trim(); if ($names -notcontains $t) { "{0} -> {1}" -f $_.Name, $t }
  }
}
```

# ENTREGA FINAL (en tu respuesta, máximo 25 líneas)
1. Qué stack y qué módulos encontraste.
2. Cobertura global (% de ideas implementadas / parciales / ausentes).
3. Los 5 riesgos o brechas más graves (incluye incumplimientos H01–H13 y problemas de seguridad).
4. Las 5 acciones de mayor impacto para el piloto, con esfuerzo.
5. Preguntas abiertas que necesitas que Janeric responda.
````
