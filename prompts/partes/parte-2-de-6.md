# Parte 2 de 6 · contexto de negocio y restricciones legales

> Copia **todo** el bloque y pégalo como un mensaje. Cuando Claude responda «✅ Parte 2/6 recibida», pega la parte 3.

````text
[PARTE 2 DE 6 — SOLO RECIBIR]
NO ejecutes nada todavía: no uses herramientas, no leas ni escribas archivos, no resumas, no empieces ninguna tarea.
Responde ÚNICAMENTE con esta línea exacta y espera la siguiente parte: «✅ Parte 2/6 recibida. Envíame la parte 3.»
Si no tienes la parte 1 en esta conversación, responde solo: «⚠️ Falta la parte 1. Envíala antes de continuar.»
────────── INICIO PARTE 2 DE 6 ──────────
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
────────── FIN PARTE 2 DE 6 ──────────
Recuerda: NO ejecutes nada. Responde solo «✅ Parte 2/6 recibida. Envíame la parte 3.» y espera.
````
