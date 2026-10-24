---
id: I24
tipo: idea
titulo: "Códigos QR en hoteles, atribución de origen y comisión a colaboradores"
area: crecimiento
estado: analizada
prioridad: alta
riesgo_legal: alto
fase: F0
origen: [A16]
depende_de: [I28]
relacionadas: [I23, I31, I32]
confianza: media
tags: [idea, crecimiento, nanturia]
---
# I24 · Códigos QR en hoteles, atribución de origen y comisión a colaboradores

> **Origen (audios):** [[A16 Sitio basico QR en hoteles y atribucion|A16]] · **Área:** crecimiento · **Prioridad:** alta · **Riesgo legal:** alto · **Fase:** F0 · **Confianza del análisis:** media
> **Depende de:** [[I28 Enlaces de pago y de ruta compartibles marketing viral|I28]]
> **Relacionadas:** [[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]] [[I31 Estrategia de confianza frente a las grandes plataformas|I31]] [[I32 MVP concierge sitio basico tours cargados prueba y error|I32]]

## Resumen fiel de lo dicho
Crear QR para entregar a todos los hoteles; así se sabe de qué hotel viene cada cliente y se puede entregar una comisión. Los hoteles tendrían un servicio extra (información turística) y se forma un embudo de ventas. Llevar registro de origen (hotel, guía, restaurante, colaborador) y dar prioridad a quienes más traen.

## Problema
Distribución local barata y medición del origen de los clientes.

## Análisis
- **Técnicamente simple**: QR con parámetro `ref=<id>` + cookie de atribución (ej. 30 días) + dashboard.
- **Punto legal crítico** → [[N03 Hallazgos criticos#H12 Comisiones a hoteles y transporte y prohibición de intermediar|H12]]: el Reglamento de Operación e Intermediación (texto 2021-011, Disp. Gen. 2ª 🟡) prohíbe realizar operación e intermediación turística *a través de* personas que brinden alojamiento, alimentos y bebidas o transporte turístico. Una **comisión por vender** tours podría ser leída como intermediación vía hotel. En cambio, **mostrar un QR de información** y que la compra se haga directamente con la agencia podría encajar mejor, pero requiere criterio jurídico.
- También existe la figura del *representante de ventas* (comisionista) con requisitos exigentes (Art. 20-21: título/competencias, RUC, contrato, 3 años de experiencia) y responsabilidad solidaria.
- «Enganchador» (promoción invasiva en espacios públicos) no aplica a un QR pasivo en recepción, pero conviene confirmarlo.

## Mejora propuesta
- **Fase 0**: instalar QR en 5 hoteles del cantón piloto **solo para medición** (sin comisión), con cupón de bienvenida al huésped (5-10 %).
- **Estructura de pago** a evaluar con abogado/MINTUR: (a) fee de publicidad/espacio fijo mensual; (b) convenio de «información turística» con facturación de servicio de marketing; (c) representante de ventas formal (solo si el hotel puede cumplir).
- **Dashboard del colaborador**: escaneos, reservas, comisión estimada; pago mensual automático.
- Niveles de colaborador por desempeño ([[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]]).

## Reglas de negocio (especificación)
```text
qr.url = https://<dominio>/r/<colaborador_id>?utm_source=qr&utm_medium=hotel
atribucion = last_click dentro de 30 dias ; reserva.colaborador_id = ref
pago_colaborador = TBD segun D08  # NO activar hasta V06 resuelto
```

## Riesgos
[[N08 Registro de riesgos#R01 Incumplimiento normativo de agencia, intermediación y guías|R01]], [[N08 Registro de riesgos#R04 Desintermediación o ventas cerradas fuera de la plataforma|R04]], [[N08 Registro de riesgos#R12 Sobrecarga operativa del fundador|R12]].

## Por verificar
[[N09 Verificaciones pendientes#V06 Legalidad de comisiones a colaboradores y de links de venta de guías|V06]], [[N09 Verificaciones pendientes#V10 LOPDP bases de licitud, registro y uso del catastro para contactar guías|V10]].

## Próximos pasos
Imprimir 5 QR de prueba; abrir consulta legal sobre la forma de compensación ([[N04 Decisiones abiertas#D08 Programa de colaboradores y QR|D08]]).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
