---
id: N13
tipo: sintesis
titulo: "Convenciones del cerebro"
estado: analizada
fecha: 2026-10-24
tags: [nanturia, convenciones, integracion]
---
# N13 · Convenciones del cerebro

> Contrato de formato para que este cerebro y el **cerebro del sitio web** (generado con Claude en PowerShell) se puedan fusionar sin fricción en una sola bóveda de Obsidian.

## 1. Identificadores
| Prefijo | Significa | Ubicación |
|---|---|---|
| `A##` | Audio (transcripción literal) | `audios e ideas/audios/` |
| `I##` | Idea analizada | `cerebro nanturia/ideas/` |
| `N##` | Nota de síntesis (hub) | `cerebro nanturia/` |
| `H##` `D##` `R##` `V##` | Hallazgo · Decisión · Riesgo · Verificación (encabezados dentro de N03/N04/N08/N09) | `cerebro nanturia/` |
| `S##` | Nota del cerebro del sitio web (la crea la otra herramienta) | `cerebro nanturia/sitio web/` |

## 2. Nombres de archivo
ASCII sin acentos, sin `:`, `?`, `*`, `"`, `<`, `>` ni `|`; formato `<ID> <Titulo corto>.md`. Enlaces con el nombre del archivo y alias: `[[I07 Pagos retencion de fondos split y fondo de respaldo|I07]]`. Enlaces a encabezados: `[[N03 Hallazgos criticos#H01 ...|H01]]`.

## 3. Frontmatter (YAML)
```yaml
---
id: I07
tipo: idea            # audio | idea | sintesis | sitio-web | tecnica
titulo: ...
area: pagos
estado: analizada     # borrador | analizada | verificada | implementada | descartada
prioridad: alta       # alta | media | baja
riesgo_legal: medio   # ninguno | bajo | medio | alto
fase: F1              # F0 | F1 | F2 | F3
origen: [A02, A10]
depende_de: [I08]
relacionadas: [I12]
confianza: media      # alta | media | baja (confianza del analisis)
tags: [idea, pagos, nanturia]
---
```
Las notas del sitio web (`S##`) usan el mismo esquema con `tipo: sitio-web`, y los campos extra `archivos: []`, `cobertura: [I07: parcial]`.

## 4. Secciones estándar de una idea
Resumen fiel · Problema · Análisis · Mejora propuesta · Reglas de negocio (especificación) · Riesgos · Métricas · Por verificar · Próximos pasos. Las reglas van en bloque de código `text` con pseudocódigo.

## 5. Niveles de certeza
🟢 verificado en texto oficial · 🟡 fuente secundaria o versión anterior · 🔴 no verificado. Todo dato legal indica su nivel.

## 6. Cómo fusionar con el cerebro del sitio web
1. Copiar la carpeta del cerebro del sitio web a `cerebro nanturia/sitio web/`.
2. Cada nota `S##` enlaza las ideas `I##` que implementa y los hallazgos `H##` que cumple o incumple.
3. La nota de cobertura (`S00`) cruza **ideas × estado de implementación** y alimenta [[N07 Hoja de ruta por fases|N07]].
4. Validar enlaces rotos con el script de validación (ver `prompts/`).
