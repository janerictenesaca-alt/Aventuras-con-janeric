# Síntesis del producto (acumulativa)

Estado: **solo Capinita analizado**. El segundo sitio de referencia aún no se ha indicado (`<URL_SITIO_2>`), así que no hay comparativa entre sitios. Fecha: 2026-10-23. Confianza global: media (sin revisión visual ni móvil; contenido leído de segunda mano).

## 1. Tabla comparativa (fuente: research/capinita.md)
| Función / página | Capinita | Sitio 2 |
|---|---|---|
| Búsqueda de rutas origen→destino | Sí, solo 2 campos, sin filtros | pendiente |
| Horarios y precios por cooperativa | Sí, tablas con contacto WhatsApp | pendiente |
| Fichas de cooperativa y terminal | Sí (reseñas vacías) | pendiente |
| Estado vial en vivo | Sí (ECU 911, por provincia/estado) | pendiente |
| Directorio de lugares | Tarjetas + categorías; fichas rotas (404) | pendiente |
| Tours y reservas | 9 tours, reserva solo por WhatsApp | pendiente |
| Registro de negocios | Gratis, con validación manual | pendiente |
| Cuenta/login | Registro correo + Google | pendiente |
| Blog/guías por región | Sí, poco contenido | pendiente |

## 2. Mejores patrones (Capinita)
- Un solo lugar para transporte + turismo + estado vial, con URLs jerárquicas por región/provincia/cantón (bueno para SEO).
- Tabla de horarios con tipo (directo/de paso), precio y contacto directo por fila.
- Mensaje de WhatsApp prellenado con el tour y su enlace (cero fricción para reservar).
- Alta de negocios gratuita y "reclamar perfil" para cooperativas.

## 3. Descartar (con razón)
- Fichas con datos sin fecha de verificación → pérdida de confianza.
- Reserva 100 % por WhatsApp sin disponibilidad ni pago → no escala.
- Itinerarios en PDF externos → no indexables ni editables.
- Contadores de paginación erróneos y "Loading..." visibles → defectos de calidad.
- Cifras de impacto sin fuente.
- Bloques de tours repetidos y publicidad de servicios no relacionados dentro de las fichas.

## 4. Backlog MoSCoW (provisional, solo con Capinita)
- **Must:** buscador de rutas con filtros (hora, precio, cooperativa); fichas de ruta/cooperativa/terminal con fecha de última verificación; ficha propia de lugar y de tour dentro del sitio; diseño móvil primero; política de privacidad con derechos reales.
- **Should:** estado vial por provincia con fuente y hora; solicitud de reserva estructurada (no solo WhatsApp); reseñas moderadas; registro y reclamo de negocios con verificación.
- **Could:** notificaciones de estado vial; mapa interactivo; guías por región; varios idiomas.
- **Won't (por ahora):** pagos en línea; app nativa; marketplace de servicios de terceros.

## 5. Arquitectura propuesta (borrador)
Módulos: Transporte (rutas, cooperativas, terminales, horarios), Turismo (lugares, tours), Vialidad, Cuentas/Negocios, Contenido.
Modelo de datos: Región > Provincia > Cantón; Lugar; Terminal; Cooperativa; Ruta; Salida (horario + precio + cooperativa); Tour; Negocio; Usuario; Reseña; EstadoVial.
Pantallas: inicio, búsqueda de ruta, detalle, directorio, tours, estado vial, panel de negocio.

## 6. Stack
Pendiente: el repo solo contiene documentación, no hay stack actual que revisar. Referencia: Capinita usa Next.js en Vercel [M]. Decidir tras definir el proyecto.

## 7. Riesgos y decisiones pendientes
- Falta el sitio 2 y la revisión visual/móvil (Chrome bloqueó el dominio: hay que permitirlo en la extensión).
- Fuente y licencia de los datos viales (ECU 911) y de horarios por cooperativa.
- Originalidad: no copiar textos, imágenes, marcas ni datos de Capinita.
- Confianza: alta en lo medido con curl; media en el resto.
