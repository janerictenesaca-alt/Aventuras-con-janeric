# Bípode A-frame v2

- `cad/geometria.py`: todas las medidas (una sola fuente).
- `cad/construir.py`: genera 3D (STEP, STL, GLB) y DXF de corte → `archivos/`.
- `cad/documento.py` + `cad/plantilla.html`: genera el documento → `documento/index.html`.
- `archivos/Bipode_A-frame_v2_plano.pdf`: el documento en PDF.

Regenerar: `pip install cadquery shapely ezdxf` y luego `cd cad && python3 construir.py && python3 documento.py`.
