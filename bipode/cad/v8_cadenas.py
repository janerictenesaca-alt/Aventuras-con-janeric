"""Cadenas de patas (mismas fórmulas que v8_build.py), para los planos."""
H, PASO = g.H_BOCA, g.PASO


def _larga(n=2, j=0):
    items, pins = [], []
    for k in range(n):
        items.append(("10", f"Pata de afuera {k + 1}", 902.0 * k, False))
        pins.append(902.0 * k - H)
    s_top = 902.0 * n - 2 * H - PASO * j
    items.append(("13", "Pata de adentro", s_top, False))
    pins.append(902.0 * n - H)
    s_pie = s_top + g.PI_L - 2 * H
    items.append(("14", "Pie", s_pie, False))
    pins.append(s_pie + H)
    return items, pins, s_pie + g.PIE_L - g4.GARRA_PUNTA


def _arriba(n=2):
    s_top = -H - (H + PASO)
    items, pins = [("13", "Pata de adentro", s_top, False)], [-H]
    boca = s_top + g.PI_L - 2 * H
    for k in range(n):
        items.append(("10", f"Pata de afuera {k + 1}", boca + 902.0, True))
        pins.append(boca + H)
        boca += 902.0
    items.append(("14", "Pie", boca, False))
    pins.append(boca + H)
    return items, pins, boca + g.PIE_L - g4.GARRA_PUNTA, s_top


ARM_A = _larga()
ARM_B = _arriba()
