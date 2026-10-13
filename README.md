# Ganjan

Editor de video personal, hecho desde cero, con la misma distribución que CapCut de escritorio.
Funciona en el navegador (Chrome o Edge recomendado), sin instalar nada y sin internet.

## Cómo abrirlo
1. Abre una terminal en esta carpeta y ejecuta: `python3 -m http.server 8000`
2. Entra a http://localhost:8000 en Chrome.

(También puedes abrir `index.html` directamente, pero algunas funciones del navegador funcionan mejor con el servidor.)

## Qué incluye hoy
- Archivos multimedia (video, foto, audio), arrastrar y soltar
- Línea de tiempo con varias pistas, dividir, recortar, mover, duplicar, imán, zoom, bloquear/ocultar/silenciar pista
- Textos con estilos, stickers, filtros (+ intensidad), ajustes de color, efectos de video, transiciones, animaciones (entrada/salida/combo)
- Velocidad, volumen y fundidos, máscaras, mezcla, voltear, rotar, escalar en el reproductor
- Efectos de sonido propios y grabación de voz
- Deshacer/rehacer, guardado automático, exportar (MP4 si el navegador lo permite, si no WebM)

## Novedades 0.2 (estructura de CapCut)
- Menú con submenús (Archivo, Editar, Diseño con 4 diseños de pantalla, Más, Ayuda, Configuración)
- Biblioteca con barra lateral, categorías, búsqueda y favoritos (★) en Filtros, Efectos, Transiciones, Texto, Stickers y Animaciones
- Panel derecho: Video (Básico, Eliminar fondo con chroma key, Máscara), Audio (volumen en dB, fundidos, normalizar, modificador de voz),
  Velocidad (estándar y curvas), Animación (entrada, salida, combinado), Ajustar (LUT .cube, color, luz, HSL, curvas, círculo cromático)
- Capas de ajuste, subtítulos manuales e importación de .srt, copiar/cortar/pegar

## Pendiente
Fotogramas clave, efectos de velocidad, portada, plantillas de proyecto y todo lo que usa IA (subtítulos automáticos, quitar fondo, retoque, personajes de voz, etc.).
