---
id: I09
tipo: idea
titulo: "Precio decreciente por tamaño de grupo («escalera de precios»)"
area: precios
estado: analizada
prioridad: alta
riesgo_legal: bajo
fase: F1
origen: [A14, A15, A26]
depende_de: [I10]
relacionadas: [I03, I21, I27]
confianza: alta
tags: [idea, precios, nanturia]
---
# I09 · Precio decreciente por tamaño de grupo («escalera de precios»)

> **Origen (audios):** [[A14 Precio por numero de personas|A14]] [[A15 Costo del guia y margen|A15]] [[A26 Rutas duplicadas y precio por grupo|A26]] · **Área:** precios · **Prioridad:** alta · **Riesgo legal:** bajo · **Fase:** F1 · **Confianza del análisis:** alta
> **Depende de:** [[I10 Estructura de precios comision y pago justo al guia|I10]]
> **Relacionadas:** [[I03 Red de operadoras revendedoras y consolidacion de grupos|I03]] [[I21 Rutas sin dueno ficha unica y multiples proveedores|I21]] [[I27 Co-venta entre guias de una ciudad para llenar el bus pooling|I27]]

## Resumen fiel de lo dicho
Con un solo cliente el precio debe ser alto (la logística es grande y el guía debe sentir que recibe un buen pago); con 2, baja; y sigue bajando con más personas «hasta cierto punto» para no abaratar demasiado. El sitio debe explicarlo con claridad e incentivar la compra mediante descuentos por grupo. Ejemplo: 1 persona $80; 2 personas $40 cada una. Si le comparten el link a alguien que pide para 2, 3… personas, el precio se recalcula.

## Problema
Cubrir el costo fijo de una salida con pocos clientes sin que el precio sea inviable con muchos.

## Análisis
- Matemática de costos: hay un **costo fijo por salida F** (mínimo del guía, logística) y un **costo variable por persona v**. El precio por persona debería ser `p(n) = (F/n + v) / (1 - t)`, con `t` la tasa de toma de Nanturia.
- La curva del ejemplo (total constante de $80) mantiene el ingreso fijo y deja al guía con el mismo pago sin importar el tamaño (con 8 personas serían $10 c/u): **no premia el crecimiento ni al guía** → ver comparación en [[N05 Modelo financiero y precios|N05]].
- Hay que fijar **piso y techo** para no abaratar de más (lo que el propio autor pide).

## Mejora propuesta
- **Pago al guía híbrido**: mínimo garantizado por salida + pago por persona (`G(n) = max(G_min, g·n)`). Así el guía gana más con más gente.
- **Escalones discretos** (1, 2, 3-4, 5+) en vez de una fórmula continua: más fáciles de entender.
- Etiquetar `n = 1` como **«salida privada»** (precio premium natural) y `n ≥ 2` como **«salida compartida»**.
- **«Compartir para bajar tu precio»**: si después entran más personas y el precio baja, se reembolsa automáticamente la diferencia a quienes ya reservaron → incentivo viral para compartir el link.
- Piso de precio por ruta y comisión mínima por salida para proteger el margen.

## Reglas de negocio (especificación)
```text
G(n)   = max(G_min, g_pp * n)
N(n)   = G(n) + v * n                    # neto del proveedor
p(n)   = clamp(N(n) / n / (1 - t), p_min, p_max)   # precio por persona
SI n aumenta DESPUES de reservar ENTONCES refund_diferencia = (p_pagado - p(n_nuevo))
```

## Riesgos
[[N08 Registro de riesgos#R13 Margen insuficiente por precio mal calibrado|R13]] precio mal calibrado · clientes esperando a que baje el precio (se mitiga con cutoff y escalones).

## Métricas de éxito
Margen de contribución por salida ≥ 20 % en todos los escalones; % de reservas que comparten el link.

## Por verificar
Costos reales por ruta (F y v) con datos del piloto.

## Próximos pasos
Costear las 3 rutas piloto y fijar tabla de escalones ([[N05 Modelo financiero y precios|N05]]).

---
Volver a: [[N00 Resumen ejecutivo|N00]] · Trazabilidad: [[N10 Matriz audio a idea|N10]]
