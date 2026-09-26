"""Chequeo v9: metal alrededor de cada hueco de mosquetón (≥ 12 mm al borde y a otro hueco) y tiro por desgarre."""
from shapely.geometry import Point
import json, os
import v9_geo as g
g.Z_DOBLE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "v9", "armado.json")))["z_doble"]


def geo_huecos(hs, cs):
    out = [(h[0], Point(h[1], h[2]).buffer(h[3] / 2, quad_segs=48), h[3]) for h in hs]
    out += [(f"c{i + 1}", c, None) for i, c in enumerate(cs)]
    return out


def revisar(nombre, poly, hs=(), cs=(), t=12.7, fy=240.0, min_d=19.0):
    """Revisa huecos de Ø ≥ min_d (mosquetón) y cortes. fy: fluencia al corte aprox. (MPa) 6061-T6 ≈ 165, A36 ≈ 145."""
    todos = geo_huecos(hs, cs)
    filas = []
    for i, (n, geo, d) in enumerate(todos):
        if d is not None and d < min_d:
            continue
        borde = poly.exterior.distance(geo)
        otro = min([geo.distance(o) for j, (_, o, _) in enumerate(todos) if j != i] or [999])
        m = min(borde, otro)
        kn = 2 * borde * t * fy / 1000.0          # 2 planos de desgarre hacia el borde (kN)
        filas.append((n, round(borde, 1), round(otro, 1), round(kn), "OK" if m >= 11.95 else "CORTO"))
    print(nombre, filas)
    return filas


AL, AC = 165.0, 145.0
r = []
r += revisar("01 frontal", g.placa_frontal(), (), g.cortes_frontal(), g.T_FR, AL)
pf, hf = g.PUENTE
r += revisar("04 puente", pf, hf, (), g.T, AL)
ala, ov, tubo = g.perfil_ala()
r += revisar("05 ala", ala, (), ov[:-2], g.T, AL)          # las 2 ranuras de las orejas van llenas y soldadas
r += revisar("08 ojo", *g.OJO, (), g.T, AL)
for k in ("15", "16"):
    p, hs, cs = g.CAR_N if k == "15" else g.CAR_A
    r += revisar(k + " disco", p, hs, cs, g.T, AL)
for k in ("17c", "17d", "17f"):
    p, hs = g.AHP_PIEZAS[k]
    r += revisar(k, p, hs, (), g.AHP_T, AC)
r += revisar("18f base", *g.rot_base(), (), 10.0, AC)
malos = [f for f in r if f[-1] != "OK"]
print("CORTOS:", malos if malos else "ninguno")
