"""Chequeo v10: choques entre piezas (volumen común > 1 mm³) en la cabeza, el trípode A y B y los accesorios."""
import itertools
import sys

sys.argv = [sys.argv[0]]
import v10_build as b


def choques(items, nombre):
    malos = []
    for (p1, s1), (p2, s2) in itertools.combinations(items, 2):
        b1, b2 = s1.val().BoundingBox(), s2.val().BoundingBox()
        if b1.xmax < b2.xmin or b2.xmax < b1.xmin or b1.ymax < b2.ymin or b2.ymax < b1.ymin or b1.zmax < b2.zmin or b2.zmax < b1.zmin:
            continue
        try:
            v = s1.intersect(s2).val().Volume()
        except Exception:
            v = 0.0
        if v > 1.0:
            malos.append((p1, p2, round(v, 1)))
    print(nombre, "choques:", malos if malos else "ninguno")
    return malos


# cabeza + gin pole (posición de trabajo) + pasadores de cabeza
cab = [(pid, s_) for pid, nom, s_, col, grp, mat, q in b.MUNDO if grp in ("cabeza", "gin") or pid.startswith("P-I")]
choques(cab, "cabeza")
tri = [(pid, s_) for pid, nom, s_, col, grp, mat, q in b.MUNDO if not pid.startswith("M")]
choques(tri, "trípode A")
triB = [(pid, s_) for pid, nom, s_, col, grp, mat, q in b.MUNDO_B if not pid.startswith("M")]
choques(triB, "trípode B")
for grupo in ("carrete", "ahp", "rotula"):  # 18d-18h: rosca M8, se toca a propósito
    choques([(it[0], it[2]) for it in b.ACC if it[4] == grupo], grupo)
