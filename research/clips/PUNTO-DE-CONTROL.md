# Punto de control del benchmark (actualizado 2026-10-23)

## Capinita (https://www.capinita.com/)
- Inventario completo del sitemap: `research/evidencia/capinita-inventario-sitemap-2026-10-23.tsv` (381 URLs; 376×200, 4×404, 1×500).
- Fichas guardadas: ver `research/clips/INDICE.md` (23 páginas, escritorio; móvil en 4).
- Para reanudar: elegir URLs del TSV que NO estén en `INDICE.md`; ejecutar `node research/herramientas/clipper.mjs <URL> --sitio=capinita`; si la huella no cambia, solo se anota verificación.
- Pendiente de revisar a fondo: variantes de las plantillas repetidas (ruta, terminal, cooperativa, lugar) y comportamiento tras filtros/pestañas (requiere interacción: pedir autorización si implica enviar algo).
- Re-ejecutar el inventario cuando se quiera detectar cambios (compara estados y títulos).

## Segundo sitio
- **PENDIENTE**: el usuario no ha dado la URL (el marcador `<URL_SITIO_2>` sigue sin reemplazar). Al recibirla: añadir su dominio a `sitios-autorizados.txt`, crear `research/<id-sitio>.md`, repetir inventario (sitemap) + fichas + móvil, y actualizar `sintesis.md`.
