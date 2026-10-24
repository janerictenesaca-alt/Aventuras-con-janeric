---
id: N18
tipo: sintesis
titulo: "Brief para la sesión Web Nanturia"
estado: instantanea
fecha: 2026-10-24
tags: [nanturia, sitio-web, brief]
---
# N18 · Brief para la sesión Web Nanturia

> Instantánea del 2026-10-24 para que la sesión **Web Nanturia** continúe sola, sin volver a la sesión «Audios & Ideas», que ya cumplió su trabajo. Si algo difiere, mandan [[N14 Estado actual del sitio web|N14]], [[N16 Tablero de pendientes|N16]] y [[N17 Decisiones del piloto propuesta|N17]].

## 1. Reparto de trabajo (propuesto)
- **Audios & Ideas** (nube): terminó. Creó el cerebro de negocio (27 audios, 35 ideas, marco legal, decisiones), la herramienta `herramientas/cerebro.mjs` y los prompts. Ya no se le consulta.
- **Claude en PowerShell** («Modelo de negocio Nanturia»): mantiene Obsidian, reconcilia notas, ejecuta TUTI y el git local.
- **Web Nanturia**: el código del sitio.

## 2. Reglas de Janeric (obligatorias)
- **ADELANTE:** el diseño y el cobro esperan esa palabra. Los textos sí se pueden corregir. Cada mejora de la auditoría de eficiencia también espera ADELANTE.
- **TUTI:** cierre en Obsidian (resumen en la nota diaria y actualización de las notas originales).
- **Fuente única:** el original es la carpeta del PC y GitHub solo es respaldo. No se copian notas.
- **Sin push** al repositorio público `Aventuras-con-janeric`. El repositorio privado «Nanturia» sí.
- Nunca inventar datos legales (registro de turismo, LUAF, dirección, teléfono 24 h).
- Respuestas cortas, con la acción primero.

## 3. Qué es Nanturia
Agencia de viajes digital (marketplace de tours de aventura y cultura en Ecuador, piloto en Morona Santiago): vende, cobra, verifica y respalda tours operados por guías y operadoras habilitadas. Resumen: [[N00 Resumen ejecutivo|N00]]. Nombre cerrado: **Nanturia**.

## 4. Dónde está todo
- Bóveda: `C:\Users\PC\Desktop\avturasconjaneric\Aventuras-con-janeric\cerebro nanturia` (rama `claude/youthful-sagan-x9etu3`). Entrada: [[N15 Mapa del proyecto y guia de colaboracion|N15]] y [[N16 Tablero de pendientes|N16]].
- Legal: [[N02 Marco legal Ecuador|N02]] y [[N03 Hallazgos criticos|N03]] · precios: [[N05 Modelo financiero y precios|N05]] · arquitectura: [[N06 Arquitectura de plataforma|N06]] · fases: [[N07 Hoja de ruta por fases|N07]] (F4 = auditoría de eficiencia) · estado del sitio: [[N14 Estado actual del sitio web|N14]] · decisiones propuestas: [[N17 Decisiones del piloto propuesta|N17]].
- Validar la bóveda: `node herramientas/cerebro.mjs validar --vault .` (debe dar 0 enlaces rotos).

## 5. Estado del sitio (auditoría)
Demo estática (Next.js 16.3.5, React 19.2.4, Tailwind 4, TypeScript; 2 890 líneas en `app/src`), sin servidor, base de datos, cuentas, pagos ni chat. De las 35 ideas del negocio: 0 implementadas, 10 parciales, 25 ausentes. De las 13 reglas legales: 8 incumplidas.

Riesgos principales:
1. La portada promete «pago protegido con pasarela» y «contacto directo» (`app/src/app/page.tsx:30-37`).
2. El pie no muestra registro de turismo, LUAF, dirección ni teléfono 24 h, y no hay páginas de términos, privacidad ni cancelación.
3. El asistente del guía permite cupo hasta 99 y no pide modalidad ni operador.
4. La reserva es un botón apagado y «enviar a revisión» no llega a nadie.
5. Los datos del guía quedan en `localStorage` sin aviso ni forma de borrarlos, y el sitio no manda cabeceras de seguridad.

Sin secretos en el código. No se midió: pruebas, Lighthouse, vulnerabilidades de dependencias ni variables de Vercel.

## 6. Reglas legales que el sitio debe cumplir (resumen de [[N03 Hallazgos criticos|N03]])
- Vende y factura una **agencia de viajes registrada**; ningún flujo presenta al guía como vendedor ni le deja cobrar por su cuenta.
- Las modalidades de aventura, salvo senderismo, solo con operador o agencia declarada.
- Cupo por salida = mín(16, límite del sitio, ratio por modalidad × guías): senderismo 8, cabalgata 8, canyoning 4, cicloturismo con apoyo 16, escalada 2 o 4, montañismo 2 (6 en media montaña), rafting 5/6/7/9 por balsa más el guía. Mejor como configuración ([[N14 Estado actual del sitio web|N14]] §8).
- Pie y checkout con: registro de turismo, LUAF, dirección física, correo, teléfono 24 h, seguridad de pago, protección de datos, declaración de responsabilidad y políticas de cobro, cancelación y reembolso.
- Si falla el proveedor: reembolso o sustitución; nunca remitir al cliente al guía ni mostrar sus contactos.

## 7. Decisiones del piloto (propuesta [[N17 Decisiones del piloto propuesta|N17]], pendiente de aprobación)
- Comisión 80/20 fijo.
- Tres políticas de cancelación (Flexible 24 h, Moderada 3 días, Estricta 7 días); cada tour muestra la suya y se quita «Gratis hasta 48 h».
- Se retiene el 20 % solo si cancela el cliente; si falla el guía o no se llena el mínimo, se devuelve el 100 %.
- Anticipo con el saldo pagado por la plataforma hasta 48 h antes.
- Guías independientes con RUC. Reservas por WhatsApp u hoja, servidor en la fase 1. Marca pastel con vidrio.
- Precio por persona: p(n) = (G(n)/n + v) / (1 − t), con G(n) = máx(mínimo del guía, pago por persona × n) y t = 0,20 en el piloto ([[N05 Modelo financiero y precios|N05]]).

## 8. Qué hacer en el sitio, en orden
1. **Textos de portada** (S): quitar lo que no existe. «Contacto directo» contradice el modelo (chat enmascarado).
2. **Asistente del guía** (S/M): pedir modalidad y operador y limitar el cupo con la configuración legal. Si toca el diseño, pedir ADELANTE.
3. **Privacidad y seguridad** (S/M): aviso y botón «borrar mis datos» para `localStorage`; cabeceras de seguridad.
4. **Pie legal y páginas** (M): bloqueado hasta que Janeric defina quién vende y factura. Hasta entonces el sitio es informativo y sin reservas.
5. **Solicitud de reserva** (M): a WhatsApp u hoja, publicada junto con el pie legal real.
6. **Fase 1** (L): base de datos, pasarela con retención y pago al guía a T+2, salidas compartidas con precio por tamaño de grupo y cancelaciones por política.
7. **Auditoría de eficiencia** ([[N07 Hoja de ruta por fases|N07]] F4) al cerrar cada fase: peso, velocidad, costo y organización, medidos antes y después, sin cambiar el comportamiento. El hosting gratuito puede no permitir uso comercial: verificar ([[N09 Verificaciones pendientes|N09]] V18).

## 9. Preguntar a Janeric
- ¿El sitio ya está público?
- ¿Quién vende y factura (razón social, registro, LUAF, dirección, teléfono 24 h)?
- ¿Aprueba [[N17 Decisiones del piloto propuesta|N17]] y qué porcentaje de anticipo?
- ¿Qué números de WhatsApp de empresa?
- ¿Cuáles son las 3 rutas y zonas del piloto?
