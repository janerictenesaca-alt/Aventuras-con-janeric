# Punto de control del benchmark (actualizado 2026-10-23)

## Capinita (https://www.capinita.com/)
- Inventario completo del sitemap: `research/evidencia/capinita-inventario-sitemap-2026-10-23.tsv` (381 URLs; 376×200, 4×404, 1×500).
- Fichas guardadas: ver `research/clips/INDICE.md` (23 páginas, escritorio; móvil en 4).
- Para reanudar: elegir URLs del TSV que NO estén en `INDICE.md`; ejecutar `node research/herramientas/clipper.mjs <URL> --sitio=capinita`; si la huella no cambia, solo se anota verificación.
- Pendiente de revisar a fondo: variantes de las plantillas repetidas (ruta, terminal, cooperativa, lugar) y comportamiento tras filtros/pestañas (requiere interacción: pedir autorización si implica enviar algo).
- Re-ejecutar el inventario cuando se quiera detectar cambios (compara estados y títulos).

## Segundo sitio: Airbnb Ecuador (https://www.airbnb.com.ec/) — indicado por el usuario el 2026-10-23
- Registro: `research/airbnb.md`; fichas en `research/clips/airbnb/` (7 páginas, 2 con móvil); capturas en `research/capturas/airbnb/`.
- Respetar `robots.txt`: NO visitar `/s/*/*` (búsqueda), `/book/`, `/rooms/*/reviews`, `/rooms/*/photos`, etc.; sin evadir anti-bots.
- Pendiente: portada completa y precios (se bloquean peticiones no-GET en modo solo lectura; probar permitiendo solo la configuración del cliente con autorización del usuario), servicios, otros destinos, análisis de JavaScript con REA, flujos con cuenta (sin autorización).
- Para reanudar: añadir URLs del sitemap por categoría (`sitemap-<categoría>-urls-N.xml.gz`) a mano, con pausas largas y pocas páginas por vez.
