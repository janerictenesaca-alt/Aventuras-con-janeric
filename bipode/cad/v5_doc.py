"""Juego de planos del trípode tipo Vortex (v5), A3 horizontal.

Uso:  python3 v5_doc.py <carpeta_imagenes> <carpeta_fuentes>  ->  ../v5/plano/index.html
Reutiliza el estilo, el rótulo y las hojas de patas de v4_doc.py.
"""
import json
import math
import os
import sys
from html import escape

from shapely.geometry import LineString, Point, box

AQUI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(AQUI, "v4_doc.py"), encoding="utf-8").read()
src = src[:src.index("# ------------------------------------------------------------------ generar")]
ns = {"__name__": "v4doc", "__file__": os.path.join(AQUI, "v4_doc.py")}
exec(compile(src, "v4_doc", "exec"), ns)

import v4_geo as g4
import v5_geo as g
from v4_dibujo import Vista, f

img, hoja, render_hoja, CSS, vista_tubo, pulg = (ns["img"], ns["hoja"], ns["render_hoja"], ns["CSS"],
                                                  ns["vista_tubo"], ns["pulg"])
HOJAS, INDICE = ns["HOJAS"], ns["INDICE"]
HOJAS.clear()
INDICE.clear()
ns["TITULO"] = "Trípode de rescate"
ns["PROY"] = "VX-EC"

OUT = os.path.join(AQUI, "..", "v5", "plano")
os.makedirs(OUT, exist_ok=True)
ARM = json.load(open(os.path.join(AQUI, "..", "v5", "armado.json")))
V = ARM["volumenes"]
AL, AC = 2.70e-6, 7.85e-6
KG = {
    "01": V["01_cabeza_aframe"] * AL, "02": V["02_cabeza_gin_pole"] * AL, "03": V["03_pata_afuera"] * AL,
    "04": V["04_pata_adentro"] * AL, "05": V["05_pie_raptor"] * AC, "06": V["06_pie_plano"] * AC,
    "07": V["07_pasador_cabeza_1-2"] * AC, "08": V["08_pasador_pata_3-8"] * AC,
}


def m2(v):
    return f"{v:.2f}".replace(".", ",")


def indice(t):
    INDICE.append(t)


# ------------------------------------------------------------------ portada
def portada():
    c = f"""<div class="cont" style="grid-template-columns:150mm 1fr">
      <div class="bloque" style="gap:6mm;align-content:space-between">
        <div class="bloque" style="gap:4mm">
          <div class="kick">Juego de planos de fabricación · Rev. B</div>
          <h1 style="font-size:58pt;font-weight:700;letter-spacing:-.01em;line-height:.9">VX-EC<br><span style="color:var(--azul)">Trípode</span><br>de rescate</h1>
          <p class="lead">Copia del Arizona Vortex (Rock Exotica) armado como trípode: cabeza A-frame azul y cabeza gin pole
          naranja maquinadas en CNC, patas de aluminio 6061-T6 en tramos con pasadores de bola y pies Raptor.</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:5mm">
          <div class="cifra"><b>{m2(g.altura(2, 1) / 1000)} m</b><span>altura al punto de carga · 2 patas de afuera (Vortex 2,41 m)</span></div>
          <div class="cifra"><b>{m2(g.altura(3, 1) / 1000)} m</b><span>altura con 3 patas de afuera (Vortex 3,20 m)</span></div>
          <div class="cifra"><b>36 kN</b><span>rotura · carga de trabajo 9 kN (2 patas de afuera)</span></div>
          <div class="cifra"><b>35,3°</b><span>cada pata desde la vertical · trípode de patas iguales</span></div>
        </div>
        <div class="bloque">
          <h3>Contenido</h3>
          <table><tbody>
            {''.join(f'<tr><td class="m" style="width:12mm">{i + 2:02d}</td><td>{escape(t)}</td></tr>' for i, t in enumerate(INDICE))}
          </tbody></table>
        </div>
        <div class="ficha">
          <dt>Cliente</dt><dd>Aventuras con Janeric · Morona Santiago, Ecuador</dd>
          <dt>Referencia</dt><dd>Arizona Vortex · Rock Exotica · manual técnico, 80 págs.</dd>
          <dt>Reemplaza</dt><dd>Rev. A (bípode): ya no se usa</dd>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:120mm 1fr;gap:6mm;align-items:start">
        <div class="bloque" style="gap:3mm;padding-top:6mm">
          <img class="render" src="{img('t_cabt')}" style="width:120mm">
          <div class="chip" style="justify-self:start">CABEZA DE TRÍPODE · A-FRAME + GIN POLE</div>
          <img class="render" src="{img('t_cabt2')}" style="width:104mm;margin-top:8mm">
          <div class="chip" style="justify-self:start">VISTA DESDE ATRÁS</div>
        </div>
        <img class="render" src="{img('t_arm')}" style="height:225mm;justify-self:end">
      </div>
    </div>"""
    HOJAS.insert(0, dict(num="—", titulo="Portada", material="—", cantidad="", escala="—", contenido=c, nota="", zonas=""))


# ------------------------------------------------------------------ conjunto
def pandeo(n, hueco):
    E = 69000.0
    I_e = math.pi / 64 * (g4.EXT_OD ** 4 - (g4.EXT_OD - 2 * g4.EXT_E) ** 4)
    I_i = math.pi / 64 * (g4.MACHO_OD ** 4 - (g4.MACHO_OD - 2 * g4.MACHO_E) ** 4)
    L = g.largo(n, hueco) + 150
    Le = n * g4.PE_TUBO
    I = (I_e * Le + I_i * (L - Le)) / L
    P = math.pi ** 2 * E * I / L ** 2
    return L, P, 3 * P * math.cos(math.radians(g.BETA))


def hoja_conjunto():
    filas = ""
    for n in (2, 3):
        for h in (1, 2, 3, 4, 5):
            dest = h == 1
            filas += (f'<tr class="{"dest" if dest else ""}"><td class="m">{n}</td><td class="m">{h}</td><td class="m">{g4.expuestos(h)}</td>'
                      f'<td class="m">{m2(g.altura(n, h) / 1000)} m</td><td class="m">{m2(g.lado_triangulo(n, h) / 1000)} m</td>'
                      f'<td class="m">{"36 kN" if n == 2 else "22 kN"}</td><td class="m">{"9 kN (≈ 900 kg)" if n == 2 else "5,5 kN (≈ 550 kg)"}</td></tr>')
    L2, P2, T2 = pandeo(2, 1)
    L3, P3, T3 = pandeo(3, 1)
    c = f"""<div class="cont" style="grid-template-columns:112mm 112mm 1fr">
      <div class="bloque">
        <div class="kick">Conjunto armado</div><h2>Vista 3D</h2>
        <img class="render" src="{img('t_arm')}" style="height:160mm;justify-self:center">
        <p class="num" style="font-size:7.5pt;color:var(--gris)">Cada pata: 2 patas de afuera + pata de adentro en el hueco 1 (5 huecos a la vista) + pie Raptor. Maniotas amarillas en triángulo. Línea de carga roja desde la polea.</p>
      </div>
      <div class="bloque">
        <div class="kick">Conjunto armado</div><h2>Vista desde arriba</h2>
        <img class="render" src="{img('t_armt')}" style="height:118mm;justify-self:center">
        <p class="num" style="font-size:7.5pt;color:var(--gris)">Los pies forman un triángulo de lados iguales. La carga tiene que quedar en el centro del triángulo (manual Vortex, pág. 24).</p>
        <img class="render" src="{img('t_armf')}" style="height:40mm;justify-self:center">
      </div>
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Tabla de alturas</div><h2>Alturas y cargas</h2></div>
        <table><thead><tr><th>Patas afuera</th><th>Hueco</th><th>A la vista</th><th>Altura a B</th><th>Lado del triángulo</th><th>Rotura</th><th>Trabajo</th></tr></thead>
        <tbody>{filas}</tbody></table>
        <p style="font-size:8pt">Filas marcadas = tabla del manual del Vortex (pág. 31): trípode con 2 patas de afuera y 5 huecos a la vista → 2,41 m y 36 kN; con 3 patas → 3,20 m y 22 kN. Este diseño da {m2(g.altura(2, 1) / 1000)} m y {m2(g.altura(3, 1) / 1000)} m.</p>
        <div class="bloque" style="gap:1.5mm">
          <h3>Geometría del trípode</h3>
          <p style="font-size:8pt">La cabeza A-frame abre sus 2 patas 30° cada una. Para que las 3 patas queden iguales, la cabeza se inclina τ = {f(g.TAU, 2)}° y la gin pole gira en su bisagra hasta β = {f(g.BETA, 2)}°:
          sen τ = sen 30° / (cos 30° · √3) y sen β = 2 · cos 30° · sen τ. Así las 3 patas quedan a {f(g.BETA, 1)}° de la vertical.</p>
          <h3 style="margin-top:2mm">Comprobación: pandeo de las patas</h3>
          <p style="font-size:8pt">Euler, P = π²·E·I / L², aluminio E = 69 000 MPa. Fuerza en la cabeza que dobla las 3 patas: T = 3 · P · cos β.</p>
          <table><thead><tr><th>Armado</th><th>Largo pata</th><th>P por pata</th><th>T en la cabeza</th><th>Vortex</th></tr></thead><tbody>
          <tr><td>2 patas afuera</td><td class="m">{f(L2 / 1000, 2)} m</td><td class="m">{f(P2 / 1000, 1)} kN</td><td class="m">{f(T2 / 1000, 1)} kN</td><td class="m">36 kN</td></tr>
          <tr><td>3 patas afuera</td><td class="m">{f(L3 / 1000, 2)} m</td><td class="m">{f(P3 / 1000, 1)} kN</td><td class="m">{f(T3 / 1000, 1)} kN</td><td class="m">22 kN</td></tr>
          </tbody></table>
          <p style="font-size:8pt">El pandeo da más que la rotura del Vortex: en el trípode manda la resistencia de la cabeza y los pasadores, igual que en el original. La carga de trabajo es la rotura dividida para 4.</p>
        </div>
      </div>
    </div>"""
    hoja("CONJ", "Trípode: conjunto, alturas y cargas", "—", "", "S/E", c)
    indice("Trípode: conjunto, alturas y cargas")


# ------------------------------------------------------------------ kit
PIEZAS = [
    ("01", "Cabeza A-frame (VXAF)", 1, "Bloque Al 6061-T6 de 430 × 180 × 70", "CNC 3 ejes, 2 caras + 2 casquillos inclinados; anodizado azul", "t_cab"),
    ("02", "Cabeza gin pole (VXGH)", 1, "Barra Al 6061-T6 Ø 130 × 220 o bloque 130 × 80 × 220", "CNC + torno; anodizado naranja", "t_gin"),
    ("03", "Pata de afuera (VXLL)", 7, "Tubo Al 6061-T6 2\" céd. 40 + espigón 2\" × 1/4\"", "Sierra, taladro, fresa; 2 pernos 3/8\"", "p06"),
    ("04", "Pata de adentro (VXUL)", 3, "Tubo Al 6061-T6 2\" × 1/4\" (Ø 50,8 × 6,35)", "Sierra, taladro, fresa (muesca)", "p07"),
    ("05", "Pie Raptor (VXRF)", 3, "Tubo acero Ø 63,5 × 6 + garra A36 12 mm", "Láser, soldadura MIG, recargue duro", "p08"),
    ("06", "Pie plano (VXFF)", 3, "Acero A36 10 mm + tubo acero Ø 63,5 × 6 + caucho 5 mm", "Láser, soldadura MIG", "p09"),
    ("07", "Pasador de cabeza 1/2\" (VXQR500)", 4, "Pasador de bola inox 17-4, 1/2\" × 4\"", "Se compra", "t_pin12"),
    ("08", "Pasador de pata 3/8\" (VXQR375)", 17, "Pasador de bola inox 17-4, 3/8\" × 3\"", "Se compra", "t_pin38"),
    ("09", "Polea de cabeza 1,5\"", 1, "Polea de rescate 38 mm, ≥ 36 kN", "Se compra", "t_polea"),
]


def hoja_kit():
    filas = "".join(f'<tr><td class="n">{n}</td><td><b>{escape(nom)}</b></td><td class="m">{q}</td><td>{escape(mat)}</td>'
                    f'<td>{escape(proc)}</td><td class="m">{f(KG.get(n, 0), 2) + " kg" if n in KG else "—"}</td></tr>'
                    for n, nom, q, mat, proc, r in PIEZAS)
    tiles = "".join(f'<div style="display:grid;gap:1mm;justify-items:center;border:0.2mm solid var(--linea);padding:2mm">'
                    f'<img class="render" src="{img(r)}" style="height:34mm;width:100%"><div style="display:flex;gap:2mm;align-items:baseline">'
                    f'<span class="num" style="color:var(--azul);font-weight:500">{n}</span><span style="font-size:8pt;font-weight:600">{escape(nom.split(" (")[0])}</span></div></div>'
                    for n, nom, q, mat, proc, r in PIEZAS)
    total = KG["01"] + KG["02"] + 6 * KG["03"] + 3 * KG["04"] + 3 * KG["05"] + 4 * KG["07"] + 15 * KG["08"]
    c = f"""<div class="cont" style="grid-template-rows:auto 1fr">
      <div style="display:grid;grid-template-columns:1fr 150mm;gap:10mm;align-items:end">
        <div class="bloque"><div class="kick">Lista de piezas · mismo kit que el Vortex (manual, pág. 7)</div><h2>Kit del trípode</h2></div>
        <div class="ficha"><dt>Peso armado</dt><dd class="num">{f(total, 1)} kg con 2 patas de afuera por pata y pies Raptor</dd>
        <dt>Colores</dt><dd>Cabeza A-frame azul · gin pole y pies naranja · patas natural · pasadores dorados</dd></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 150mm;gap:10mm">
        <table><thead><tr><th>N.º</th><th>Pieza</th><th>Cant.</th><th>Material</th><th>Proceso</th><th>Peso c/u</th></tr></thead><tbody>{filas}</tbody></table>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;align-content:start">{tiles}</div>
      </div>
    </div>"""
    hoja("KIT", "Kit del trípode", "Varios", "", "S/E", c)
    indice("Kit del trípode: lista de piezas")


# ------------------------------------------------------------------ cabeza A-frame
def hoja_cabeza():
    P = g.perfil_cuerpo()
    minx, miny, maxx, maxy = P.bounds
    top = maxy
    v = Vista(minx - 60, miny - 80, maxx + 60, g.OREJA_Z[1] + 40, 250)
    for lado in (-1, 1):
        s = LineString([g.eje(lado, 0), g.eje(lado, g.CAS_L)]).buffer(g.HEMBRA_OD / 2, cap_style=2)
        v.forma(s, "pieza")
        v.linea(g.eje(lado, -15), g.eje(lado, g.CAS_L + 15), "eje")
        for gb in (50.0, 80.0, 110.0):
            x, z = g.eje(lado, g.CAS_L - gb)
            v.circulo(x, z, g.D38 / 2)
    v.forma(P.difference(box(-15.2, top - 16, 15.2, top + 10)))
    for sx in (-1, 1):
        x0, x1 = g.OREJA_X
        v.rect(sx * x0 if sx > 0 else -x1, g.OREJA_Z[0], x1 - x0, g.OREJA_Z[1] - g.OREJA_Z[0], "pieza")
    for b in g.bahias():
        v.forma(b, "fantasma")
    for lado in (-1, 1):
        v.forma(g.ventana(lado), "hueco")
    for n, x, z, d, _ in g.HUECOS:
        v.circulo(x, z, d / 2)
        v.eje_cruz(x, z, d / 2)
        v.texto(x + d / 2 + 2 * v.k, z + d / 2 + 0.5 * v.k, n, 0.8, "start", "etq")
    v.linea((0, g.C_HUECO[1]), (0, top), "oculta")
    v.texto(4, 30, "C", 0.8, "start", "etq")
    v.texto(0, top - 8, "D", 0.8, cls="etq")
    v.texto(g.eje(-1, 60)[0] + 42, g.eje(-1, 60)[1] - 18, "E", 0.8, cls="etq")
    v.texto(-22, g.OREJA_Z[1] + 4, "A", 0.8, cls="etq")
    xb1, zb1 = g.eje(1, g.CAS_L, g.HEMBRA_OD / 2)
    xb0, zb0 = g.eje(-1, g.CAS_L, g.HEMBRA_OD / 2)
    ext_x = max(maxx, xb1)
    v.cota_h(-ext_x, ext_x, miny, miny - 50, f"{f(2 * ext_x)} total (Vortex 417)")
    v.cota_h(minx, maxx, miny, miny - 26)
    zbot = min(g.eje(1, g.CAS_L, -g.HEMBRA_OD / 2)[1], zb1)
    v.cota_v(zbot, g.OREJA_Z[1], ext_x, ext_x + 22, f"{f(g.OREJA_Z[1] - zbot)} total (Vortex 165)")
    v.cota_h(-g.XC, g.XC, g.YT, g.OREJA_Z[1] + 18, f"{f(2 * g.XC)} entre ejes")
    v.cota(g.eje(1, 0), g.eje(1, g.CAS_L), -46, f"{f(g.CAS_L)} casquillo")
    v.nota(g.eje(-1, 150)[0], g.eje(-1, 150)[1], -70, miny - 70, "30° cada casquillo · Ø 63,5 / Ø 51,4 · huecos G a 50, 80 y 110 de la boca")
    frente = v.svg("Vista de frente", "Escala 1:1,7 · origen = hueco B")

    # vista desde arriba: fondo y orejas
    t = Vista(-150, -70, 150, 55, 108)
    t.rect(-120, -g.FONDO / 2, 240, g.FONDO, "pieza")
    t.rect(-120, -g.BAHIA / 2, 240, g.BAHIA, "fantasma")
    for sx in (-1, 1):
        x0, x1 = g.OREJA_X
        t.rect(sx * x0 if sx > 0 else -x1, -g.FONDO / 2, x1 - x0, g.FONDO, "pieza3")
    t.linea((-g.OREJA_X[1] - 8, 0), (g.OREJA_X[1] + 8, 0), "eje")
    t.cota_v(-g.FONDO / 2, g.FONDO / 2, 120, 134, f(g.FONDO))
    t.cota_v(-g.BAHIA / 2, g.BAHIA / 2, -120, -134, f(g.BAHIA))
    t.cota_h(-g.OREJA_X[0], g.OREJA_X[0], -g.FONDO / 2, -g.FONDO / 2 - 12, f(2 * g.OREJA_X[0]))
    t.cota_h(g.OREJA_X[0], g.OREJA_X[1], g.FONDO / 2, g.FONDO / 2 + 10, f(g.OREJA_X[1] - g.OREJA_X[0]))
    arriba = t.svg("Vista desde arriba (centro)", "Escala 1:2,8 · paredes 9,5 · bahía 44,5")

    filas = "".join(f'<tr><td class="n">{n}</td><td class="m">{f(x)}</td><td class="m">{f(z)}</td><td class="m">Ø {f(d)}</td>'
                    f'<td style="font-size:7.6pt">{escape(u)}</td></tr>' for n, x, z, d, u in g.HUECOS)
    filas += (f'<tr><td class="n">A</td><td class="m">X</td><td class="m">{f(g.OREJA_HUECO_Z)}</td><td class="m">Ø 13,1</td><td style="font-size:7.6pt">Orejas: bisagra de la gin pole, 2 pasadores 1/2"</td></tr>'
              f'<tr><td class="n">C</td><td class="m">0</td><td class="m">{f(g.C_HUECO[1])} a D</td><td class="m">Ø 13,1</td><td style="font-size:7.6pt">Unión central vertical</td></tr>'
              f'<tr><td class="n">D</td><td class="m">0</td><td class="m">{f(top)}</td><td class="m">R 15,2</td><td style="font-size:7.6pt">Canal para la cuerda</td></tr>'
              '<tr><td class="n">E</td><td class="m" colspan="3">(±54; −2) (±82; −4) (±64; −22) R 6</td><td style="font-size:7.6pt">Ventanas de anclaje de abajo</td></tr>'
              '<tr><td class="n">F · G</td><td class="m" colspan="3">3 ranuras 11 × 14 · Ø 9,9 a 50/80/110</td><td style="font-size:7.6pt">Alineación y pasador de pata</td></tr>')
    c = f"""<div class="cont" style="grid-template-columns:255mm 1fr">
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Pieza 01 · una sola pieza maquinada en CNC · 417 × 63,5 × 164 (Vortex 417 × 98 × 165 con pasadores)</div><h2>Cabeza A-frame</h2></div>
        {frente}
        <div style="display:flex;gap:8mm;align-items:start">{arriba}<img class="render" src="{img('t_cabb')}" style="height:44mm"></div>
      </div>
      <div class="bloque" style="gap:3mm">
        <img class="render" src="{img('t_cab')}" style="height:48mm">
        <dl class="ficha">
          <dt>Material</dt><dd>Bloque de aluminio 6061-T6 de 430 × 180 × 70 mm (o 7075-T6), con certificado</dd>
          <dt>Proceso</dt><dd>CNC de 3 ejes desde el archivo STEP 01_cabeza_aframe.step. Los casquillos a 30° se hacen girando la pieza en una mesa inclinable o con un 4.º eje.</dd>
          <dt>Peso</dt><dd class="num">{f(KG['01'], 2)} kg (Vortex 2,3 kg: se puede alivianar con más rebajes)</dd>
          <dt>Acabado</dt><dd>Anodizado duro azul. Filos redondeados R 1 en ventanas, orejas y canal D.</dd>
        </dl>
        <table><thead><tr><th>Punto</th><th>X</th><th>Z</th><th>Ø</th><th>Uso</th></tr></thead><tbody>{filas}</tbody></table>
      </div>
    </div>"""
    hoja("01", "Cabeza A-frame", "Al 6061-T6 · CNC", "1", "1:1,7", c, "Letras A a I iguales a la pág. 10 del manual del Vortex.")
    indice("01 · Cabeza A-frame (CNC)")


# ------------------------------------------------------------------ gin pole
def hoja_gin():
    ax, ay, at = g.GP_ALA
    lx, ly, lz = g.GP_LENGUA
    L = g.GP_CAS_L
    v = Vista(-100, -L - 45, 110, at + lz + 30, 96)
    v.rect(-g.HEMBRA_OD / 2, -L, g.HEMBRA_OD, L, "pieza2")
    v.linea((-g.HEMBRA_ID / 2, -L), (-g.HEMBRA_ID / 2, -8), "oculta")
    v.linea((g.HEMBRA_ID / 2, -L), (g.HEMBRA_ID / 2, -8), "oculta")
    v.rect(-ax / 2, 0, ax, at, "pieza2")
    v.rect(-lx / 2, at, lx, lz - ly / 2, "pieza2")
    v.el.append(f'<path class="pieza2" d="M{-lx / 2},{-(at + lz - ly / 2)} A{lx / 2},{lx / 2} 0 0 1 {lx / 2},{-(at + lz - ly / 2)} Z"/>')
    for gb in (50, 80):
        v.circulo(0, -L + gb, g.D38 / 2)
    v.rect(-g.RANURA_A / 2, -L, g.RANURA_A, g.RANURA_P, "hueco")
    v.circulo(0, at + g.GP_HUECO_Z, g.D12 / 2)
    v.linea((0, -L - 10), (0, at + lz + 10), "eje")
    v.cota_v(-L, at + lz, ax / 2, ax / 2 + 14, f"{f(g.GP_TOTAL)} total (Vortex 212)")
    v.cota_v(-L, 0, -g.HEMBRA_OD / 2, -ax / 2 - 12, f(L))
    v.cota_h(-ax / 2, ax / 2, 0, -20, f"{f(ax)} (Vortex 127)")
    v.cota_v(0, at + g.GP_HUECO_Z, lx / 2, lx / 2 + 12, f(at + g.GP_HUECO_Z))
    v.cota_v(-L, -L + 50, g.HEMBRA_OD / 2, g.HEMBRA_OD / 2 + 10, "50")
    fr = v.svg("Vista de frente", "Escala 1:2,2")

    a = Vista(-80, -52, 80, 52, 78)
    a.el.append(f'<rect class="pieza2" x="{-ax / 2}" y="{-ay / 2}" width="{ax}" height="{ay}" rx="22"/>')
    for n, x, y in g.GP_ALA_HUECOS:
        a.circulo(x, y, 8)
        a.eje_cruz(x, y, 8)
    a.rect(-lx / 2, -ly / 2, lx, ly, "pieza3")
    a.cota_h(-ax / 2, ax / 2, -ay / 2, -ay / 2 - 10, f(ax))
    a.cota_v(-ay / 2, ay / 2, ax / 2, ax / 2 + 10, f"{f(ay)} (Vortex 76)")
    a.cota_h(-44, 44, 17, ay / 2 + 8, "88")
    ar = a.svg("Vista desde arriba", "Escala 1:2 · 4 huecos Ø 16")
    c = f"""<div class="cont" style="grid-template-columns:1fr 1fr">
      <div class="bloque" style="gap:5mm">
        <div class="bloque"><div class="kick">Pieza 02 · una sola pieza maquinada en CNC</div><h2>Cabeza gin pole</h2></div>
        <div style="display:flex;gap:10mm;align-items:start">{fr}{ar}</div>
      </div>
      <div class="bloque" style="gap:4mm">
        <div style="display:flex;gap:6mm;align-items:end"><img class="render" src="{img('t_gin')}" style="height:62mm"><img class="render" src="{img('t_cabt2')}" style="height:62mm"></div>
        <dl class="ficha">
          <dt>Material</dt><dd>Aluminio 6061-T6, bloque de 130 × 80 × 220 o barra Ø 130</dd>
          <dt>Casquillo</dt><dd>Ø 63,5 por fuera y Ø 51,4 por dentro, igual que los de la cabeza A-frame: acepta la pata de afuera (espigón) y la de adentro. Huecos Ø 9,9 a 50 y 80 de la boca. 3 ranuras F.</dd>
          <dt>Ala</dt><dd>127 × 76 × 20 con 4 huecos Ø 16 para mosquetón o vientos.</dd>
          <dt>Lengüeta</dt><dd>30 de grueso: entra entre las orejas A (separadas 30,4). Hueco Ø 13,1 en X para los 2 pasadores de cabeza de 1/2". Así la gin pole gira como bisagra (manual, pág. 11).</dd>
          <dt>Peso</dt><dd class="num">{f(KG['02'], 2)} kg (Vortex 1 kg)</dd>
        </dl>
        <div class="aviso"><b>Cómo se une</b>Poner la lengüeta entre las orejas A de la cabeza A-frame y meter los 2 pasadores de cabeza de 1/2", uno por cada lado. Revisar que la bola de cada pasador salga del otro lado.</div>
      </div>
    </div>"""
    hoja("02", "Cabeza gin pole", "Al 6061-T6 · CNC", "1", "1:2,2", c)
    indice("02 · Cabeza gin pole (CNC)")


# ------------------------------------------------------------------ pies
def hoja_pies():
    G = g4.contorno_garra()
    minx, miny, maxx, maxy = G.bounds
    v = Vista(minx - 35, miny - 28, maxx + 40, g4.PIE_CAS_L + 30, 120)
    v.rect(-g4.HEMBRA_OD / 2, 0, g4.HEMBRA_OD, g4.PIE_CAS_L, "pieza3")
    v.linea((-51.5 / 2, 0), (-51.5 / 2, g4.PIE_CAS_L), "oculta")
    v.linea((51.5 / 2, 0), (51.5 / 2, g4.PIE_CAS_L), "oculta")
    v.forma(G.difference(box(-g4.HEMBRA_OD / 2, 0, g4.HEMBRA_OD / 2, 200)), "pieza2")
    v.poli([(-38, 0), (-38, 60), (38, 60), (38, 0)], "oculta", cerrado=False)
    for n, x, y, d, _ in g4.HUECOS_GARRA:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
        v.texto(x, y - d / 2 - 3.5 * v.k, n, 0.8, cls="etq")
    v.circulo(0, g4.PIE_CAS_L - g4.PIE_HUECO, g4.D38 / 2)
    v.linea((0, miny - 8), (0, g4.PIE_CAS_L + 8), "eje")
    v.cota_h(minx, maxx, miny, miny - 14)
    v.cota_v(g4.GARRA_PUNTA, g4.PIE_CAS_L, maxx, maxx + 24, f(g4.PIE_CAS_L - g4.GARRA_PUNTA))
    v.cota_v(g4.PIE_CAS_L - g4.PIE_HUECO, g4.PIE_CAS_L, -g4.HEMBRA_OD / 2, -g4.HEMBRA_OD / 2 - 12, "50")
    v.cota_v(0, 60, 38, 50, "60")
    v.nota(0, g4.GARRA_PUNTA + 4, -60, g4.GARRA_PUNTA + 20, "recargue duro")
    garra = v.svg("05 · Pie Raptor", "Escala 1:2,3 · garra 12 mm")
    b = Vista(-100, -100, 100, 100, 80)
    b.el.append('<rect class="pieza2" x="-75" y="-75" width="150" height="150" rx="14"/>')
    for n, x, y, d, _ in g4.HUECOS_BASE:
        b.circulo(x, y, d / 2)
        b.eje_cruz(x, y, d / 2)
    b.rect(-30, -9.5, 60, 4, "pieza3")
    b.rect(-30, 5.5, 60, 4, "pieza3")
    b.cota_h(-75, 75, -75, -88, "150")
    b.cota_h(-55, 55, 55, 88, "110")
    b.cota_v(-75, 75, 75, 88, "150")
    base = b.svg("06 · Base del pie plano", "Escala 1:2,5 · A36 10 mm · 4 × Ø 14")
    c = f"""<div class="cont" style="grid-template-columns:125mm 95mm 1fr">
      <div class="bloque" style="gap:4mm"><div class="bloque"><div class="kick">Piezas 05 y 06 · acero</div><h2>Pies</h2></div>{garra}</div>
      <div class="bloque" style="gap:4mm;padding-top:18mm">{base}<img class="render" src="{img('p09')}" style="height:56mm"></div>
      <div class="bloque" style="gap:4mm">
        <img class="render" src="{img('p08')}" style="height:62mm">
        <dl class="ficha">
          <dt>05 Raptor</dt><dd>Casquillo de tubo de acero Ø 63,5 × 6 (interior 51,5) de 120, con 2 ranuras de 12,4 × 60 abajo. La garra de A36 12 mm entra en las ranuras y se suelda con MIG por los dos lados. Punta con recargue duro. Pintura en polvo naranja. {f(KG['05'], 2)} kg.</dd>
          <dt>06 Plano</dt><dd>Base de 150 × 150 × 10 con 4 huecos Ø 14 (a 110 × 110) para empernarlo a la roca con tus pernos de 1/2". Orejas de 8 mm soldadas y una lengüeta que gira en un perno 1/2". Caucho de 5 mm abajo. {f(KG['06'], 2)} kg.</dd>
          <dt>Uso</dt><dd>Los 2 pies sirven en la pata de adentro y en el espigón de la pata de afuera (manual, pág. 14). Pasador de pata de 3/8" a 50 de la boca.</dd>
        </dl>
        <div class="aviso"><b>Asegurar los pies</b>Maniota entre cada par de pies, pie encajado en una grieta, empernado a la roca por los 4 huecos, o amarrado (manual, pág. 20).</div>
      </div>
    </div>"""
    hoja("05–06", "Pies Raptor y plano", "Acero A36", "3 + 3", "1:2,3", c)
    indice("05 y 06 · Pies Raptor y plano")


# ------------------------------------------------------------------ compras
def hoja_compras():
    filas = [
        ("07", "Pasador de bola con anillo, 1/2\" (12,7) × 4\" de agarre (101,6)", "4", "Inox 17-4 · ≥ 140 kN doble corte", "2 en la bisagra de la gin pole (orejas A) · 1 en B con la polea · 1 de repuesto o en I"),
        ("08", "Pasador de bola con anillo, 3/8\" (9,5) × 3\" de agarre (76,2)", "17", "Inox 17-4 · ≥ 80 kN doble corte", "Pata en la cabeza, uniones de patas, pie. Igual que el kit del Vortex"),
        ("—", "Perno hexagonal 3/8\"-16 × 3\" grado 8 + tuerca de seguridad", "14", "Acero aleado", "Espigón de cada pata de afuera (2 por pata) · llave 9/16\" (14 mm)"),
        ("—", "Pasador de acero Ø 9,5 × 20 (tope de alineación)", "7", "Acero 1045", "1 por pata de afuera"),
        ("—", "Perno 1/2\" × 2\" grado 8 + tuerca de seguridad", "3", "Acero aleado", "Bisagra de cada pie plano"),
        ("09", "Polea de rescate de 1,5\" (38 mm) para cuerda de 11 mm", "1", "Aluminio / acero · ≥ 36 kN", "Colgada del hueco B con un pasador de cabeza"),
        ("—", "Cinta de maniota 25 mm con hebilla de leva, 20 kN", "3", "Poliéster", "Una entre cada par de pies (triángulo) · 4 m c/u"),
        ("—", "Cuerda estática 11 mm (EN 1891 A) para vientos", "3 × 15 m", "Poliamida", "Solo si el trípode se inclina o la carga sale del triángulo"),
    ]
    tr = "".join(f'<tr><td class="n">{a}</td><td><b>{escape(b)}</b></td><td class="m">{c}</td><td>{escape(d)}</td><td>{escape(e)}</td></tr>' for a, b, c, d, e in filas)
    c = f"""<div class="cont" style="grid-template-rows:auto 1fr">
      <div style="display:grid;grid-template-columns:1fr 150mm;gap:10mm;align-items:end">
        <div class="bloque"><div class="kick">Piezas 07 a 09 y tornillería · se compran</div><h2>Pasadores, tornillería y cintas</h2></div>
        <div class="aviso"><b>No reemplazar por piezas de ferretería</b>Pasadores y pernos del grado indicado. Lo advierten los manuales del Vortex y del TerrAdaptor.</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 130mm;gap:10mm">
        <table><thead><tr><th>N.º</th><th>Qué</th><th>Cant.</th><th>Material</th><th>Dónde va</th></tr></thead><tbody>{tr}</tbody></table>
        <div class="bloque" style="gap:4mm">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm"><img class="render" src="{img('t_pin12')}" style="height:34mm"><img class="render" src="{img('t_polea')}" style="height:34mm"></div>
          <dl class="ficha">
            <dt>Dónde</dt><dd>"Ball lock pin" o "quick release pin" en McMaster-Carr o Amazon. La bola tiene que salir por completo del otro lado.</dd>
            <dt>Si no llegan</dt><dd>Un tornero puede hacer pasadores de acero 4140 Ø 12,7 y Ø 9,5 con un hueco de 3 mm en la punta para un pasador R.</dd>
          </dl>
        </div>
      </div>
    </div>"""
    hoja("07–09", "Pasadores, tornillería y cintas", "Varios", "", "S/E", c)
    indice("07 a 09 · Pasadores, tornillería, polea y cintas")


# ------------------------------------------------------------------ fabricación y armado
def hoja_fab():
    pasos = [
        ("Material", "Bloque 6061-T6 para las 2 cabezas y tubos 2\" × 1/4\", 2\" cédula 40 y 2½\" × 1/4\" con certificado. No usar 6063 de ventanería."),
        ("CNC", "Mandar los STEP 01 y 02 a un taller de CNC. Pedir tolerancia ±0,05 en casquillos y huecos de pasador, y que prueben los pasadores antes de anodizar."),
        ("Patas", "7 patas de afuera (940 + espigón 230 metido 120, 2 pernos 3/8\", tope) y 3 de adentro (980). Huecos Ø 9,9 con prisma en V. Ranuras F con fresa."),
        ("Pies", "3 Raptor y 3 planos en acero, con láser y soldadura MIG. Recargue duro en la punta de la garra."),
        ("Acabado", "Anodizado duro: azul (A-frame), naranja (gin pole), natural (patas). Pies pintura en polvo naranja. Grabar VX-EC, número de serie, fecha y «Trabajo 9 kN»."),
        ("Prueba", f"Armar a {m2(g.altura(2, 1) / 1000)} m con 3 maniotas. Colgar 18 kN (≈ 1.800 kg) del hueco B por 3 minutos, sin personas, con tecle y dinamómetro. Repetir con 3 patas de afuera a 11 kN."),
        ("Revisión", "Ningún tubo doblado, ningún hueco ovalado, pasadores que salen con la mano. Si algo se deforma, no se usa. Anotar fecha y resultado."),
    ]
    tr = "".join(f'<div class="paso"><span class="k">{i + 1}</span><div><b>{escape(a)}</b><p>{escape(b)}</p></div></div>' for i, (a, b) in enumerate(pasos))
    campo = [
        "En el suelo: armar las 3 patas a la misma altura (2 patas de afuera + pata de adentro + pie). La pata de adentro va siempre abajo.",
        "Meter 2 patas en los casquillos de la cabeza A-frame y 1 en la gin pole. Unir la gin pole a las orejas A con 2 pasadores de 1/2\".",
        "Colgar la polea del hueco B con un pasador de cabeza antes de levantar.",
        "Levantar abriendo las patas hasta que los pies formen un triángulo de lados iguales (tabla de la hoja 02).",
        "Poner una maniota entre cada par de pies y tensarla. En roca, empernar los pies planos o encajar los Raptor en grietas.",
        "La carga tiene que quedar en el centro del triángulo y la línea de tiro cerca de la línea de carga (manual, págs. 18 y 24). Cargar poco a poco, con cuerda de seguridad aparte.",
    ]
    c = f"""<div class="cont" style="grid-template-columns:1fr 1fr">
      <div class="bloque" style="gap:3.2mm"><div class="bloque"><div class="kick">Taller</div><h2>Orden de fabricación</h2></div>{tr}</div>
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">En el lugar</div><h2>Armado del trípode</h2></div>
        <ol>{''.join(f'<li>{escape(t)}</li>' for t in campo)}</ol>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm">
          <table><thead><tr><th colspan="2">Dónde amarrar</th></tr></thead><tbody>
            <tr><td class="n">B</td><td>Polea o carga principal</td></tr>
            <tr><td class="n">C</td><td>Unión vertical central</td></tr>
            <tr><td class="n">I1–I4</td><td>Anclajes de la cabeza</td></tr>
            <tr><td class="n">E</td><td>Ventanas de anclaje de abajo</td></tr>
            <tr><td class="n">H</td><td>Amarres laterales hacia afuera</td></tr>
            <tr><td class="n">G1–G4</td><td>Ala de la gin pole</td></tr>
          </tbody></table>
          <table><thead><tr><th colspan="2">Nunca</th></tr></thead><tbody>
            <tr><td>✕</td><td>Usarlo sin las 3 maniotas</td></tr>
            <tr><td>✕</td><td>Dejar la carga fuera del triángulo sin un viento opuesto</td></tr>
            <tr><td>✕</td><td>Más de 3 patas de afuera por pata</td></tr>
            <tr><td>✕</td><td>Patas a distinta altura sin revisar la tabla</td></tr>
            <tr><td>✕</td><td>Pasadores de ferretería o doblados</td></tr>
          </tbody></table>
        </div>
        <div class="aviso"><b>Antes de usar con personas</b>Un ingeniero mecánico revisa y firma estos planos, y se hace la prueba de carga del paso 6. Solo el trípode de patas iguales tiene certificación CE en el Vortex (EN 795).</div>
      </div>
    </div>"""
    hoja("FAB", "Fabricación, prueba y armado", "—", "", "S/E", c)
    indice("Orden de fabricación, prueba de carga y armado del trípode")


hoja_conjunto()
hoja_kit()
hoja_cabeza()
hoja_gin()
ns["hoja_patas"]()
INDICE[-1] = "03 y 04 · Patas de afuera y de adentro"
HOJAS[-1]["num"] = "03–04"
HOJAS[-1]["cantidad"] = "7 + 3"
hoja_pies()
hoja_compras()
hoja_fab()
portada()
ns["REV"] = "B"
total = len(HOJAS)
html = ('<!doctype html><html lang="es"><head><meta charset="utf-8"><title>VX-EC Trípode · planos</title>'
        f'<style>{CSS}</style></head><body>' + "".join(render_hoja(h, i + 1, total) for i, h in enumerate(HOJAS)) + "</body></html>")
html = html.replace("Bípode A-Frame de rescate", "Trípode de rescate")
for a, b in (("06 · Pata de afuera", "03 · Pata de afuera"), ("07 · Pata de adentro", "04 · Pata de adentro"),
             ("Piezas 06 y 07", "Piezas 03 y 04"), (">06 Afuera<", ">03 Afuera<"), (">07 Adentro<", ">04 Adentro<")):
    html = html.replace(a, b)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
print("hojas", total)
