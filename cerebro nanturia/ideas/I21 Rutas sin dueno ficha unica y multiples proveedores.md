---
id: I21
tipo: idea
titulo: "Rutas sin dueño: ficha única y múltiples proveedores"
area: producto
estado: analizada
prioridad: media
riesgo_legal: medio
fase: F2
origen: [A23, A26]
depende_de: [I15, I22]
relacionadas: [I03, I20, I23]
confianza: media
tags: [idea, producto, nanturia]
---
# I21 · Rutas sin dueño: ficha única y múltiples proveedores

> **Origen (audios):** [[A23 Asignacion automatica cupos y rutas precreadas|A23]] [[A26 Rutas duplicadas y precio por grupo|A26]] · **Área:** producto · **Prioridad:** media · **Riesgo legal:** medio · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I15 Modo turista y modo guia asistente de creacion de rutas|I15]] [[I22 Biblioteca de rutas precreadas y onboarding|I22]]
> **Relacionadas:** [[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]] [[I20 Asignacion automatica de guia cupos y desbordamiento|I20]] [[I23 Ranking y visibilidad de guias operadoras y colaboradores|I23]]

## Resumen fiel de lo dicho
Si dos guías quieren ofrecer la misma ruta (ej. una cascada en Méndez), se hace **una sola ficha** y cualquiera con usuario puede venderla; nadie es dueño. El primero que la creó recibe prioridad en las solicitudes. El precio depende del número de personas y se estabiliza en un rango.

## Problema
Evitar peleas por «propiedad» de rutas y duplicados que fragmentan la oferta.

## Análisis
- Separar **Ruta (producto canónico)** de **Oferta (proveedor que la opera)** resuelve la disputa y permite comparar proveedores por precio, reseñas y disponibilidad.
- Requisito legal: quien opere debe estar habilitado (clasificación y ámbito) → no basta con tener un usuario.
- Calidad: si «cualquiera» vende, la experiencia varía → reseñas por oferta y verificación de conocimiento de la ruta ([[I22 Biblioteca de rutas precreadas y onboarding|I22]]).
- Incentivo: el creador invierte trabajo; conviene reconocerlo.

## Mejora propuesta
- **Ruta canónica + ofertas** (`Ruta 1—N Oferta`).
- **Detección de duplicados** al subir (misma modalidad + mismo cantón + trazado con alto traslape + punto de inicio cercano) con revisión humana.
- **Crédito al creador** ([[N04 Decisiones abiertas#D10 Crédito al creador de ruta|D10]]): prioridad temporal en asignación + bono (ej. 2-3 % del PVP por X años) o bonus en ranking; evitar «propiedad» exclusiva.
- **Habilitación por ruta**: quiz/video corto + salida acompañada antes de operar.
- Precio de la oferta calculado por la misma escalera ([[I09 Precio decreciente por tamano de grupo escalera de precios|I09]]).

## Reglas de negocio (especificación)
```text
Ruta(id, creador_id, modalidad, canton, trazado, estado)
Oferta(ruta_id, proveedor_id, habilitada, rating, precio_neto_min)
oferta.habilitada = elegible(proveedor, ruta) AND conocimiento_verificado(proveedor, ruta)
creador_bonus = pct * PVP durante vigencia (si D10 aprobado)
```

## Riesgos
[[N08 Registro de riesgos#R16 Calidad desigual de guías y rutas|R16]], [[N08 Registro de riesgos#R04 Desintermediación o ventas cerradas fuera de la plataforma|R04]].

## Por verificar
[[N09 Verificaciones pendientes#V11 Límites de grupo por modalidad y por área protegida para las 16 rutas|V11]], [[N04 Decisiones abiertas#D10 Crédito al creador de ruta|D10]].

## Próximos pasos
Definir el modelo de datos de Ruta/Oferta en [[N06 Arquitectura de plataforma|N06]].

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
