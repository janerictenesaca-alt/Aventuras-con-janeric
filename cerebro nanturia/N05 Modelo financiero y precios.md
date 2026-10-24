---
id: N05
tipo: sintesis
titulo: "Modelo financiero y precios"
estado: analizada
fecha: 2026-10-24
tags: [nanturia, finanzas, precios]
---
# N05 · Modelo financiero y precios

> Modelo **ilustrativo**: todos los valores marcados como *supuesto* deben reemplazarse con costos reales del piloto. Reúne [[I09 Precio decreciente por tamano de grupo escalera de precios|I09]], [[I10 Estructura de precios comision y pago justo al guia|I10]], [[I07 Pagos retencion de fondos split y fondo de respaldo|I07]], [[I08 Reserva no reembolsable|I08]].

## 1. Variables
| Símbolo | Significado | Valor de ejemplo (supuesto) |
|---|---|---|
| `G_min` | pago mínimo garantizado al guía por salida | $35 (el audio habla de $30-40) |
| `g` | pago al guía por persona | $15 (el audio habla de $15 por persona en aventura) |
| `v` | costo variable por persona (entradas, refrigerio) | $5 |
| `t` | tasa de toma de Nanturia sobre el precio de venta | 30 % |
| `n` | número de personas en la salida | 1…8 |

## 2. Fórmulas
```text
G(n)   = max(G_min, g * n)             # pago al guia
N(n)   = G(n) + v * n                  # neto del proveedor
P(n)   = N(n) / (1 - t)                # precio total de la salida
p(n)   = P(n) / n                      # precio por persona (luego redondear y aplicar piso/techo)
toma(n)= P(n) * t                      # ingreso bruto de Nanturia
```

## 3. Resultado con el ejemplo
| n | Pago guía | Costos variables | Neto proveedor | Precio total | **Precio por persona** | Toma Nanturia (30 %) |
|---|---|---|---|---|---|---|
| 1 | $35 | $5 | $40 | $57,14 | **$57,14** | $17,14 |
| 2 | $35 | $10 | $45 | $64,29 | **$32,14** | $19,29 |
| 3 | $45 | $15 | $60 | $85,71 | **$28,57** | $25,71 |
| 4 | $60 | $20 | $80 | $114,29 | **$28,57** | $34,29 |
| 5 | $75 | $25 | $100 | $142,86 | **$28,57** | $42,86 |
| 6 | $90 | $30 | $120 | $171,43 | **$28,57** | $51,43 |
| 8 | $120 | $40 | $160 | $228,57 | **$28,57** | $68,57 |

**Lectura:** el precio por persona cae de $57 a ≈ $29 y **se estabiliza solo** (piso natural) porque el guía cobra por persona a partir del tercer cliente. Presentación sugerida: escalones 1 → $57,50 · 2 → $32,50 · 3 o más → $29.

## 4. Comparación con la curva del audio ([[A15 Costo del guia y margen|A15]])
En el ejemplo del audio, 1 persona paga $80 y 2 pagan $40 cada una → **el total se mantiene en $80**. Con el guía en $40 y la toma en 30 % ($24):

| n | Precio por persona | Total | Guía | Toma Nanturia |
|---|---|---|---|---|
| 1 | $80 | $80 | $40 | $24 |
| 2 | $40 | $80 | $40 | $24 |
| 4 | $20 | $80 | $40 | $24 |
| 8 | $10 | $80 | $40 | $24 |

Problemas: con 8 personas el precio por persona ($10) sería inviable; el guía cobra igual con 1 o con 8 (no hay incentivo a llenar el grupo); Nanturia gana lo mismo siempre. **Recomendación:** pago al guía híbrido (mínimo + por persona) con piso de precio.

## 5. Realidad de la unidad económica
Con tomas de $17 a $51 por salida, Nanturia necesita **volumen** o **tickets más altos** para cubrir sus costos fijos. Salidas por mes necesarias para cubrir costos fijos *supuestos*:

| Costos fijos mensuales (supuesto) | n=1 (toma $17,14) | n=3 (toma $25,71) | n=6 (toma $51,43) |
|---|---|---|---|
| $500 | 30 salidas | 20 salidas | 10 salidas |
| $1 000 | 59 salidas | 39 salidas | 20 salidas |

Implicaciones: (1) priorizar rutas de **mayor ticket** (cuevas, rafting, paquetes) además de las de $29; (2) los costos de cumplimiento de una agencia (oficina, personal, seguro, contador) pueden ser superiores a $500/mes → validar en [[N09 Verificaciones pendientes#V02 Requisitos exactos para ser agencia y costos|V02]]; (3) las líneas de ingreso secundarias ([[I25 Complementos de hospedaje y transporte aceptar u omitir|I25]], [[I10 Estructura de precios comision y pago justo al guia|I10]]) mejoran el margen.

## 6. Fondo de contingencia
Exposición mensual esperada = ventas mensuales × tasa de falla del proveedor (con payouts a T+2, solo hay riesgo en el lapso entre cobro y servicio y en contracargos).

| Ventas mensuales | Falla 2 % | Falla 3 % | Falla 5 % |
|---|---|---|---|
| $5 000 | $100 | $150 | $250 |
| $10 000 | $200 | $300 | $500 |
| $20 000 | $400 | $600 | $1 000 |

Regla: mantener un fondo ≥ **2×** la exposición esperada. Ejemplo: ventas $10 000 y falla 3 % → fondo ≈ $600.

## 7. Política de cancelación (propuesta, [[I08 Reserva no reembolsable|I08]])
| Momento | Fee de reserva | Depósito |
|---|---|---|
| Hasta T-72 h | No reembolsable | 100 % |
| T-72 h a T-24 h | No reembolsable | 50 % |
| Menos de 24 h / no-show | No reembolsable | 0 % |
| Falla del proveedor o de Nanturia | **Reembolsable 100 %** | **100 %** |
| Mínimo de grupo no alcanzado | **Reembolsable 100 %** | **100 %** |
| Fuerza mayor/clima | Reprogramar o reembolso menos costos no recuperables | idem |

## 8. Comisión por canal (propuesta, [[N04 Decisiones abiertas#D07 Comisión por canal|D07]])
| Canal | Take rate | Nota |
|---|---|---|
| Cliente captado por Nanturia | ≈ 30 % | Cubre marketing, soporte, riesgo |
| Cliente traído por el link del guía | ≈ 20 % | Reduce incentivo a evadir |
| Reventa por operadora | 10-15 % | Precio único; comisión fija |
| Colaboradores (hotel/restaurante) | TBD | Sujeto a [[N09 Verificaciones pendientes#V06 Legalidad de comisiones a colaboradores y de links de venta de guías\|V06]] |
