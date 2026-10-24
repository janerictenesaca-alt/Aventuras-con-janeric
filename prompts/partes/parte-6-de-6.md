# Parte 6 de 6 · formato, calidad y entrega final

> Copia **todo** el bloque y pégalo como un mensaje. Esta es la última: al recibirla, Claude empezará a trabajar.

````text
[PARTE 6 DE 6 — ÚLTIMA PARTE]
Si no tienes las partes 1 a 5 en esta conversación, responde solo: «⚠️ Falta la parte X. Envíala antes de continuar.» y espera.
Si las tienes todas, recibe esta última parte y luego sigue la ORDEN FINAL que aparece al terminar.
────────── INICIO PARTE 6 DE 6 ──────────
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
Cuerpo: Resumen · Evidencia (ruta:línea) · Análisis · Brechas · Mejora propuesta · Esfuerzo · Riesgos · Próximos pasos · Relacionadas. Enlaza con wikilinks a las notas del cerebro de negocio por su nombre de archivo, por ejemplo `[[I07 Pagos retencion de fondos split y fondo de respaldo|I07]]` o `[[N03 Hallazgos criticos#H06 La plataforma responde ante el cliente|H06]]`, y entre notas del sitio web con `[[S06 Flujos criticos]]`. Dentro de tablas Markdown escribe el alias con barra invertida: `[[Nota\|alias]]`. Las reglas verificables van en bloques ```text con pseudocódigo.

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
    $t = $_.Groups[1].Value.Trim().TrimEnd('\'); if ($names -notcontains $t) { "{0} -> {1}" -f $_.Name, $t }
  }
}
```

# ENTREGA FINAL (en tu respuesta, máximo 25 líneas)
1. Qué stack y qué módulos encontraste.
2. Cobertura global (% de ideas implementadas / parciales / ausentes).
3. Los 5 riesgos o brechas más graves (incluye incumplimientos H01–H13 y problemas de seguridad).
4. Las 5 acciones de mayor impacto para el piloto, con esfuerzo.
5. Preguntas abiertas que necesitas que Janeric responda.
────────── FIN PARTE 6 DE 6 ──────────
▶ ORDEN FINAL: ya tienes las 6 partes (1 rol/reglas · 2 contexto/legal · 3-4 catálogo de ideas · 5 tareas · 6 formato/entrega). Confirma en UNA sola línea que las recibiste todas y EJECUTA ahora el prompt completo, en orden, empezando por la Fase 0. Si falta alguna parte, dime cuál y espera.
````
