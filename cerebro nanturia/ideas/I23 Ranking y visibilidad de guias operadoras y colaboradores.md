---
id: I23
tipo: idea
titulo: "Ranking y visibilidad de guías, operadoras y colaboradores"
area: producto
estado: analizada
prioridad: media
riesgo_legal: bajo
fase: F2
origen: [A16, A23]
depende_de: [I21, I24]
relacionadas: [I13, I17]
confianza: media
tags: [idea, producto, nanturia]
---
# I23 · Ranking y visibilidad de guías, operadoras y colaboradores

> **Origen (audios):** [[A16 Sitio basico QR en hoteles y atribucion|A16]] [[A23 Asignacion automatica cupos y rutas precreadas|A23]] · **Área:** producto · **Prioridad:** media · **Riesgo legal:** bajo · **Fase:** F2 · **Confianza del análisis:** media
> **Depende de:** [[I21 Rutas sin dueno ficha unica y multiples proveedores|I21]] [[I24 QR en hoteles atribucion de origen y comision|I24]]
> **Relacionadas:** [[I13 Incumplimiento del guia no activa el tour o no se presenta|I13]] [[I17 Flujo de reserva con confirmacion de disponibilidad|I17]]

## Resumen fiel de lo dicho
Los guías que crean rutas aparecen primero en los resultados, salvo que otro tenga un puntaje tan alto que lo supere. Y todo colaborador (guía, hotel, restaurante) que traiga más clientes debe tener prioridad en el sistema para aparecer en los primeros puestos.

## Problema
Premiar el esfuerzo y la contribución sin sacrificar la calidad que ve el turista.

## Análisis
- Un ranking basado solo en volumen de referidos puede **degradar la experiencia** (quien trae más no necesariamente atiende mejor) y es manipulable.
- Los hoteles/restaurantes no «compiten» en el ranking de tours: su recompensa es otra (comisión/visibilidad como colaborador).

## Mejora propuesta
- **Score compuesto transparente** (ej.): 35 % reseñas · 25 % cumplimiento · 15 % tiempo de respuesta · 15 % conversión · 10 % bonus creador. Pesos ajustables y documentados.
- **Bonus de creador** temporal (decae con el tiempo) para no congelar ventajas.
- **Colaboradores**: tablero de desempeño y beneficios por nivel (Bronce/Plata/Oro) en lugar de posiciones en el ranking del turista.
- Antifraude: reseñas solo de reservas completadas; detección de patrones.

## Reglas de negocio (especificación)
```text
score = 0.35*rating + 0.25*cumplimiento + 0.15*resp_rapida + 0.15*conversion + 0.10*bonus_creador(t)
bonus_creador(t) = max(0, 1 - t/12meses)
```

## Riesgos
[[N08 Registro de riesgos#R16 Calidad desigual de guías y rutas|R16]], [[N08 Registro de riesgos#R04 Desintermediación o ventas cerradas fuera de la plataforma|R04]].

## Métricas de éxito
Correlación score↔satisfacción; % de clics en los 3 primeros resultados.

## Próximos pasos
Decidir pesos con datos del piloto.

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
