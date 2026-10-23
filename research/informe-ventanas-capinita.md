# Informe por ventanas de Capinita (2026-10-23)

Método: capturas de escritorio (1366 px) con un Chrome aparte y de solo lectura, más el texto de cada página. Capturas en `research/capturas/capinita/`. No se inició sesión ni se envió nada. **[O]** observado · **[I]** inferido.

## Plantilla común a todas las ventanas [O]
Barra lateral izquierda fija (Inicio, Tours "Nuevo", Rutas, Cooperativas, Lugares, Blog, Vialidad, Emprendedor); cabecera con "Agregar Negocio", búsqueda, tema claro/oscuro y cuenta; columna derecha con tour destacado y "Últimos Blogs"; tarjeta "Rutas Ecuador" fija abajo a la izquierda; botones de compartir (Facebook, WhatsApp, Messenger, X). Casi toda página repite al final el bloque "Recomendado para tu negocio" (3 apps de terceros) y la captación de emprendedores.

## Qué hace cada ventana
| Ventana | Qué hace | Cómo se usa | Observación clave |
|---|---|---|---|
| **Inicio** `/` | Portada: buscador de lugares con búsquedas frecuentes (cascada, mirador, aventura), cifras, 3 puertas de entrada (Rutas, Cooperativas, Terminales) y carrusel de tours | Escribir un lugar o elegir una tarjeta | Prioriza turismo y venta de tours; las cifras no tienen fuente |
| **Tours** `/tours` | Catálogo de 9 tours por categoría con precio y duración | "Ver Detalles" (PDF) o "Reservar" (WhatsApp) | Sin filtros ni ficha propia; reserva manual |
| **Rutas** `/ruta` | Buscador de transporte entre dos puntos | Elegir origen, luego destino (se habilita después) y "Buscar" | Solo 2 campos; las tarjetas de apps ocupan el sitio del resultado |
| **Detalle de ruta** `/ruta/<origen>-a-<destino>` | Ficha de un trayecto: pestañas Horarios, Mapa, Ruta, Estado, Servicios Turísticos | Filtrar horarios; "Comprar" / "Consultar" por cooperativa | Cada salida es una tarjeta con hora de salida/llegada, terminales, tipo (Directo/De Paso), precio y botón de contacto; algunos botones están desactivados |
| **Cooperativas** `/cooperativa-de-transporte` | Directorio de cooperativas con buscador y sello de verificación | Buscar por nombre o "Conocer más" | Calificaciones en 0; algunas sin foto real (bus genérico) |
| **Detalle de cooperativa** | Galería de fotos, tipo de servicio, pestañas (Horarios, Sucursales, Comodidades, Imágenes, Redes, Testimoniales), me gusta y compartir; rutas filtrables por cantón origen/destino | Filtrar y contactar por WhatsApp | La más completa en información; reseñas vacías |
| **Terminales** `/terminal-terrestre` | Listado de estaciones de buses con foto por ciudad | Elegir terminal | Tarjetas simples: foto, ciudad y nombre |
| **Detalle de terminal** | Dirección, cómo comprar pasajes, servicios, consejos y tabla de salidas | Leer | Contacto "na" |
| **Lugares** `/buscador-de-lugares-turisticos` | Buscador y rejilla de lugares con categoría (Hospedaje, Balneario, Aventura, Reserva, Cascada, Mirador) | Buscar o filtrar por etiqueta | Cada tarjeta lleva provincia, cantón, resumen y calificación 0; el paginador dice "1 a 2 de 5" sobre 12 tarjetas |
| **Vialidad** `/estado-vial-ecuador` | Estado de carreteras (ECU 911) | Buscar o filtrar por estado; tarjetas por tramo | Incluye ruta alterna y fuente; reportes con fechas antiguas pese a "cada minuto" |
| **Regiones** `/amazonia` `/sierra` `/costa` `/galapagos` | Guías editoriales largas por región (qué es, geografía, provincias y cantones, clima, cultura, gastronomía, fauna) | Leer y seguir a tours/lugares | Amazonía revisada visualmente; Sierra, Costa y Galápagos con captura pero **no revisadas** |
| **Blog** `/blog` y entrada | Listado y artículos con portada, autor, fecha, tiempo de lectura y "me gusta" | Leer; el texto enlaza al buscador de rutas | Entrada revisada: estructura de guía (qué es, cómo llegar, clima, mejor época); un único autor |
| **Emprendedor** `/promocionar-negocio-turistico` | Capta negocios turísticos: registro gratis en 4 pasos (cuenta, datos, validación, personalización) | "Iniciar ahora" o "Contáctanos" | El texto promete "cientos de personas" frente a "150 Mil+" en el inicio |
| **Iniciar sesión** `/iniciar-sesion` | Acceso con Google o correo y contraseña; "¿Olvidaste tu contraseña?" | Solo visto, no usado | Sí tiene formulario (el HTML inicial no lo mostraba: se carga después) |
| **Crear cuenta** `/crear-cuenta` | Registro con Google o formulario: nombre, correo, fecha de nacimiento, celular (+593), contraseña y repetirla | Solo visto, no enviado | Pide fecha de nacimiento sin explicar por qué |
| **Sobre nosotros / Servicios profesionales / Privacidad** | Equipo, servicios de desarrollo web ($100–$1500) y política de datos | Leer | Capturas guardadas de las dos primeras, no revisadas; la privacidad se leyó solo en texto |

## Cómo se conectan las ventanas [I]
Ciclo principal: **Inicio → Rutas → detalle de ruta → cooperativa → contacto por WhatsApp**, con **Vialidad** y **Terminales** como apoyo y **Lugares/Tours/Regiones/Blog** como captación de turismo y tráfico de búsqueda. **Emprendedor/Cuenta** alimenta el directorio y abre la venta de servicios.

## Lo que aprovechar y lo que evitar para nuestro proyecto
- Aprovechar: navegación lateral fija con 8 secciones claras; detalle de ruta con tarjetas de salida legibles; ruta alterna y fuente en estado vial; registro de negocios en pasos.
- Evitar: apps de terceros encima del contenido útil; cifras sin fuente; reseñas en 0 visibles; botones desactivados sin explicación; paginadores erróneos.

## Límites
Solo escritorio (la captura móvil con Chrome sin ventana no es fiable). Sin revisar: Sierra, Costa, Galápagos, Sobre nosotros, Servicios y unas 360 fichas del sitemap.
