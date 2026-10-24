---
id: N08
tipo: sintesis
titulo: "Registro de riesgos"
estado: analizada
fecha: 2026-10-24
tags: [nanturia, riesgos]
---
# N08 · Registro de riesgos

> Probabilidad (P) e impacto (I): B=baja, M=media, A=alta. Revisión sugerida: mensual.

## R01 Incumplimiento normativo de agencia, intermediación y guías
P: M · I: A · Mitigación: [[N04 Decisiones abiertas#D02 Estructura habilitante agencia propia o venta bajo agencia aliada|D02]], verificaciones [[N09 Verificaciones pendientes#V01 Texto consolidado del Reglamento de Operación e Intermediación Turística|V01]]-[[N09 Verificaciones pendientes#V06 Legalidad de comisiones a colaboradores y de links de venta de guías|V06]], checklist de vigencias, asesoría legal.

## R02 Siniestro grave sin cobertura suficiente
P: B · I: A · Mitigación: [[I29 Seguros y requisitos de las plataformas globales|I29]], plan de contingencia y consentimiento informado ([[I18 Automatizacion documental legal por ruta|I18]]), selección estricta de operadoras.

## R03 Falla del proveedor por no presentarse
P: M · I: M · Mitigación: [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]] confirmaciones, suplentes, strikes; [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]] retención de pagos.

## R04 Desintermediación o ventas cerradas fuera de la plataforma
P: A · I: M · Mitigación: comisión por canal ([[I10 Estructura de precios comision y pago justo al guia|I10]]), chat enmascarado ([[I16 Bot intermediario cliente guia y prevencion de fuga de datos|I16]]), valor agregado (garantía, seguro, cobro), reseñas.

## R05 Contracargos y fraude de pago
P: M · I: M · Mitigación: política clara aceptada ([[I08 Reserva no reembolsable|I08]]), 3DS, verificación de identidad en reservas altas, fondo ([[N05 Modelo financiero y precios|N05]]).

## R06 Arranque en frío sin oferta ni demanda
P: A · I: A · Mitigación: biblioteca de rutas ([[I22 Biblioteca de rutas precreadas y onboarding|I22]]), operadoras ancla ([[I05 Alianzas ancla Cueva de los Tayos Mateo y empresa de Hernan|I05]]), QR hoteles ([[I24 QR en hoteles atribucion de origen y comision|I24]]), piloto concierge ([[I32 MVP concierge sitio basico tours cargados prueba y error|I32]]).

## R07 Dependencia de pocas operadoras ancla
P: M · I: A · Mitigación: diversificar a ≥ 3 por clúster, contratos con salida, scorecard ([[I01 Modelo en cadena con operadoras aliadas|I01]]).

## R08 Complejidad excesiva del MVP
P: A · I: A · Mitigación: puertas de fase ([[N07 Hoja de ruta por fases|N07]]); posponer 3D, bot, internacional, buses nacionales.

## R09 Protección de datos personales
P: M · I: M · Mitigación: minimización, consentimiento, retención, cifrado ([[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]]).

## R10 Reputación por una mala experiencia temprana
P: M · I: A · Mitigación: operar primero rutas de bajo riesgo; garantía Nanturia ([[I31 Estrategia de confianza frente a las grandes plataformas|I31]]); soporte humano.

## R11 Cambios regulatorios y transición institucional
P: M · I: M · Mitigación: revisión trimestral de normas ([[N03 Hallazgos criticos#H13 Autoridad en transición y vigencia de textos|H13]]), fecha de verificación por texto.

## R12 Sobrecarga operativa del fundador
P: A · I: M · Mitigación: automatizar solo cuellos de botella, documentar procesos, sumar un apoyo operativo ([[I22 Biblioteca de rutas precreadas y onboarding|I22]]).

## R13 Margen insuficiente por precio mal calibrado
P: M · I: M · Mitigación: costeo real por ruta, piso de precio, comisión mínima por salida ([[N05 Modelo financiero y precios|N05]]).

## R14 Daño al patrimonio o conflicto con comunidades
P: B · I: A · Mitigación: precisión reducida de coordenadas, permisos, acceso con guía ([[I26 Rutas digitales 3D datos de ruta de pago y explicaciones de pago|I26]], [[N09 Verificaciones pendientes#V12 Permisos de acceso a sitios, comunidades y patrimonio|V12]]).

## R15 Bloqueo de canales de mensajería o pagos
P: M · I: A · Mitigación: opt-in y plantillas ([[N09 Verificaciones pendientes#V13 Condiciones de WhatsApp Business API|V13]]), segundo proveedor de pagos, canal de correo de respaldo.

## R16 Calidad desigual de guías y rutas
P: M · I: M · Mitigación: habilitación por ruta ([[I22 Biblioteca de rutas precreadas y onboarding|I22]]), reseñas verificadas, auditorías de muestra, ranking ([[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]]).

## R17 Costos de infraestructura que crecen con el uso
P: M · I: M · Mitigación: auditoría de eficiencia ([[N07 Hoja de ruta por fases#F4 · Auditoría de eficiencia del código (al cerrar cada fase y antes de lanzar)|F4]]), plan de hosting verificado ([[N09 Verificaciones pendientes#V18 Costos y condiciones del hosting del sitio|V18]]), alertas de gasto y límites de presupuesto en el proveedor.
