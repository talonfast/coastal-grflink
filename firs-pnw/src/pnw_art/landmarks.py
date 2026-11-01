"""
Multi-tile models of FIRS PNW's real sites, for make_art.py. Footprint X in 0..16*W (+X = map south-west),
Y in 0..16*D (+Y = map south-east), Z in pixels; the +X and +Y faces are the ones the player sees.
Sizes follow the real sites at the scenario's ~250 m per tile; aircraft are drawn oversized, as OpenTTD does.
"""

import numpy as np

from buildings import Building, _paving


def site(w, d):
    b = Building(w, d)
    b.style = "classic"
    return b


def font_sign(b, text, x_center, z_mid, y_face, mat, scale=1.0, font=None):
    """3x5 pixel lettering on the +Y face, `scale` pixels per font pixel, reading left to right on screen."""
    from make_art import FONT
    font = font or FONT
    total = len(text) * 4 - 1
    col_w, row_h = 0.5 * scale, 1.0 * scale

    def mask(X, Y, Z):
        c = np.floor((x_center - X) / col_w + total / 2).astype(int)
        r = np.floor((z_mid + 2.5 * row_h - Z) / row_h).astype(int)
        ok = (Y > y_face - 0.3) & (Y <= y_face + 0.05) & (c >= 0) & (c < total) & (r >= 0) & (r < 5)
        out = np.zeros(np.shape(X), bool)
        for i, ch in enumerate(text):
            if ch == " ":
                continue
            g = font[ch]
            for rr in range(5):
                for cc in range(3):
                    if g[rr][cc] == "1":
                        out |= ok & (c == i * 4 + cc) & (r == rr)
        return out
    half = total * col_w / 2 + 0.5
    b.sol(mask, mat, x_center - half, x_center + half)


def side_sign(b, text, y_center, z_mid, x_face, mat, scale=1.0):
    """Lettering on the +X face; along Y one unit is one screen pixel, so columns are 1 * scale wide."""
    from make_art import FONT
    total = len(text) * 4 - 1
    col_w, row_h = 1.0 * scale, 1.0 * scale

    def mask(X, Y, Z):
        c = np.floor((Y - y_center) / col_w + total / 2).astype(int)
        r = np.floor((z_mid + 2.5 * row_h - Z) / row_h).astype(int)
        ok = (X > x_face - 0.3) & (X <= x_face + 0.05) & (c >= 0) & (c < total) & (r >= 0) & (r < 5)
        out = np.zeros(np.shape(X), bool)
        for i, ch in enumerate(text):
            if ch == " ":
                continue
            g = FONT[ch]
            for rr in range(5):
                for cc in range(3):
                    if g[rr][cc] == "1":
                        out |= ok & (c == i * 4 + cc) & (r == rr)
        return out
    b.sol(mask, mat, x_face - 0.4, x_face + 0.1)


def ground(b, x0, x1, y0, y1, mat):
    b.bx(x0, x1, y0, y1, 0.0, 0.25, mat)


class NoseIn:
    """Lets the nose-to-+X aircraft helpers draw facing -Y (nose in to a building's +Y face), turned about
    (cx, cy): model X' maps to world -Y, model Y' to world +X."""

    def __init__(self, b, cx, cy):
        self.b, self.cx, self.cy = b, cx, cy

    def bx(self, x0, x1, y0, y1, z0, z1, mat):
        cx, cy = self.cx, self.cy
        self.b.bx(cx + (y0 - cy), cx + (y1 - cy), cy - (x1 - cx), cy - (x0 - cx), z0, z1, mat)

    def sol(self, fn, mat, *_):
        cx, cy = self.cx, self.cy
        self.b.sol(lambda X, Y, Z: fn(cx - (Y - cy), cy + (X - cx), Z), mat)


def airliner(b, x, y, z, length, body="white", tail="navy", engines="grey", lcf=False):
    """Airliner on the ground, nose to +X, centred on (x, y). lcf: the Dreamlifter's swollen upper fuselage."""
    r = length * 0.06
    zc = z + r + 0.6
    x0, x1 = x - length / 2, x + length / 2

    def fuselage(X, Y, Z):
        u = (X - x0) / length                                    # 0 tail .. 1 nose
        taper = np.clip(np.minimum(u / 0.18, (1 - u) / 0.07), 0, 1) ** 0.6
        rr = r * np.maximum(taper, 0.15)
        return ((Y - y) ** 2 + (Z - zc) ** 2 <= rr ** 2) & (X > x0) & (X < x1)
    b.sol(fuselage, body, x0, x1)
    if lcf:
        R = r * 2.3
        b.sol(lambda X, Y, Z: ((Y - y) ** 2 + (Z - (zc + R - r)) ** 2 <= R ** 2) & (Z > zc) &
              (X > x0 + length * 0.22) & (X < x0 + length * 0.78), body, x0, x1)
    span = length * 0.95
    sweep = 0.45

    def wing(X, Y, Z):
        d = np.abs(Y - y)
        lead = x + length * 0.08 - sweep * d
        return (d < span / 2) & (X < lead) & (X > lead - length * 0.14 * (1 - d / span)) & (np.abs(Z - (zc - r * 0.5)) < 0.35)
    b.sol(wing, body, x0, x1)
    for side in (-1, 1):                                         # two engines under the wings
        ey = y + side * span * 0.17
        ex = x + length * 0.08 - sweep * span * 0.17
        b.sol(lambda X, Y, Z, ey=ey, ex=ex: ((Y - ey) ** 2 + (Z - (zc - r * 1.1)) ** 2 <= (r * 0.45) ** 2) &
              (X > ex - length * 0.02) & (X < ex + length * 0.1), engines, x0, x1)
    b.bx(x0 + length * 0.02, x0 + length * 0.14, y - 0.2, y + 0.2, zc, zc + length * 0.2, tail)       # fin

    def tailplane(X, Y, Z):
        d = np.abs(Y - y)
        lead = x0 + length * 0.16 - 0.5 * d
        return (d < length * 0.17) & (X < lead) & (X > lead - length * 0.07) & (np.abs(Z - zc) < 0.3)
    b.sol(tailplane, body, x0, x1)


def twin_otter(b, x, y, z, length=8.0, body="white", stripe="red"):
    """DHC-6 Twin Otter on floats: high wing, two engines, nose to +X."""
    zc = z + 2.6
    b.bx(x - length / 2, x + length / 2, y - 0.75, y + 0.75, zc - 0.8, zc + 0.8, body)
    b.bx(x - length / 2, x + length / 2, y - 0.77, y + 0.77, zc - 0.1, zc + 0.15, stripe)
    b.bx(x + length * 0.05, x + length * 0.2, y - length * 0.65, y + length * 0.65, zc + 0.8, zc + 1.05, body)
    for side in (-1, 1):
        b.bx(x + length * 0.1, x + length * 0.33, y + side * 1.6 - 0.35, y + side * 1.6 + 0.35, zc + 0.3, zc + 0.95, "dark")
        b.bx(x - length * 0.35, x + length * 0.35, y + side * 1.0 - 0.3, y + side * 1.0 + 0.3, z, z + 0.8, body)  # floats
    b.bx(x - length / 2, x - length / 2 + 1.2, y - 0.12, y + 0.12, zc + 0.8, zc + 3.0, stripe)


def b747():
    """Boeing 747-400 in Boeing house colours, built with BC Aviation's airliner model (coastal-grflink
    aircraft/src/aircraft.py) so it matches those aircraft: upper-deck hump, four engines, blue cheatline and fin."""
    import aircraft as AC
    a = AC.Aircraft(70.6, 64.4, 6.5)
    L, R = a.L, a.R
    a.fuselage(body="acwhite", door_u=(0.86, 0.5, 0.12, -0.26, -0.62))
    a.solid(lambda U, V, W: (V ** 2 + (W - (a.wc + R * 0.62)) ** 2 <=
                             (R * 0.86 * np.clip((U - (L / 2 - 0.40 * L)) / (0.12 * L), 0, 1) ** 0.5) ** 2) &
            (U < L / 2 - 0.05 * L) & (U > L / 2 - 0.40 * L), "acwhite", -L / 2, L / 2)          # upper deck
    a.paint(lambda U, V, W, dz, r: [((np.abs(dz - 0.05 * r) < 0.16 * r) & (U < L / 2 - 0.06 * L), "asnavy")])
    a.wing(0.12 * L / 2, 14.8 * AC.M, 4.0 * AC.M, 37.5)
    for v in (0.24, 0.44):
        a.engines(v, 2.7, 5.6, mat="acwhite")
    a.fin(10.6, 12.0, 4.6, 45, mat="asnavy")
    a.stabiliser(22.2, 6.5, 40, mat="acwhite")
    a.gear()
    return a


def place(b, a, x, y, z=0.25):
    """Copy an aircraft model's parts into a site, nose to +X, centred on (x, y)."""
    du, dv = x - b.cx, y - b.cy
    for kind, p in a.ops:
        if kind == "solid":
            b.solid(lambda U, V, W, fn=p["fn"]: fn(U - du, V - dv, W - z), p["mat"], p["u0"] + du, p["u1"] + du)
        elif kind == "box":
            b.box(p["u0"] + du, p["u1"] + du, p["v0"] + dv, p["v1"] + dv, p["z0"] + z, p["z1"] + z, p["mat"])
        else:
            raise ValueError(f"cannot place aircraft part {kind}")


def dreamlifter(b, x, y, z, length=32.0):
    """Boeing 747-400 LCF Dreamlifter, nose to +X: 747 cockpit hump ahead of the huge swollen cargo fuselage
    that tapers into the tail, swept low wings with four engines, Boeing-blue fin. Centred on (x, y)."""
    L = length
    xn, xt = x + L / 2, x - L / 2                                 # nose, tail
    r = L * 0.05                                                  # ordinary 747 fuselage radius
    zb = z + 1.4                                                  # belly clearance (gear)

    def u_of(X):
        return (X - xt) / L                                       # 0 tail .. 1 nose

    def lower(X, Y, Z):
        u = u_of(X)
        nose = np.clip((1 - u) / 0.08, 0, 1) ** 0.5              # round nose
        tail = np.clip(u / 0.25, 0, 1)                            # tail cone narrows...
        rr = r * np.minimum(nose, 0.35 + 0.65 * tail)
        zc = zb + r + (1 - tail) * r * 0.9                        # ...and sweeps up
        return ((Y - y) ** 2 + (Z - zc) ** 2 <= rr ** 2) & (X > xt) & (X < xn)
    b.sol(lower, "white", xt, xn)

    def cargo(X, Y, Z):                                           # the LCF's swollen upper lobe
        u = u_of(X)
        grow = np.clip((0.80 - u) / 0.07, 0, 1) * np.clip((u - 0.06) / 0.30, 0, 1) ** 0.7
        R = r * 2.4 * np.maximum(grow, 1e-3)
        zc = zb + r * 1.2 + R * 0.75
        return ((Y - y) ** 2 / 0.8 + (Z - zc) ** 2 <= R ** 2) & (Z >= zb + r) & (u > 0.06) & (u < 0.80)
    b.sol(cargo, "white", xt, xn)
    b.sol(lambda X, Y, Z: cargo(X, Y, Z) & (np.abs(Z - (zb + r * 2.6)) < 0.45), "navy", xt, xn)   # cheatline
    b.sol(lambda X, Y, Z: lower(X, Y, Z) & (Z < zb + r * 0.8), "grey", xt, xn)                     # grey belly

    def hump(X, Y, Z):                                            # 747 cockpit hump just ahead of the lobe
        u = u_of(X)
        return ((Y - y) ** 2 + (Z - (zb + r * 1.7)) ** 2 <= (r * 0.75) ** 2) & (u > 0.78) & (u < 0.9)
    b.sol(hump, "white", xt, xn)
    b.bx(xn - L * 0.07, xn - L * 0.05, y - r * 0.55, y + r * 0.55, zb + r * 1.95, zb + r * 2.15, "dark")   # cockpit glass
    b.bx(xt + L * 0.12, xn - L * 0.1, y - r * 0.5, y + r * 0.5, zb - 0.05, zb + 0.35, "grey")              # belly

    span, sweep, root = L * 0.9, 0.62, L * 0.2

    def wing(X, Y, Z):
        d = np.abs(Y - y)
        lead = x + L * 0.1 - sweep * d
        chord = root * (1 - 0.72 * d / (span / 2))
        return (d < span / 2) & (X < lead) & (X > lead - chord) & (np.abs(Z - (zb + r * 0.6 + d * 0.04)) < 0.32)
    b.sol(wing, "white", xt, xn)
    for frac in (0.22, 0.42):                                     # four engines on pylons
        for side in (-1, 1):
            d = span / 2 * frac
            ey, ex = y + side * d, x + L * 0.1 - sweep * d + L * 0.04
            ez = zb + r * 0.6 + d * 0.04 - 0.95
            b.sol(lambda X, Y, Z, ey=ey, ex=ex, ez=ez: ((Y - ey) ** 2 + (Z - ez) ** 2 <= 0.62 ** 2) &
                  (X > ex - 2.6) & (X < ex), "grey", xt, xn)
            b.sol(lambda X, Y, Z, ey=ey, ex=ex, ez=ez: ((Y - ey) ** 2 + (Z - ez) ** 2 <= 0.42 ** 2) &
                  (X > ex - 0.15) & (X < ex + 0.05), "dark", xt, xn)

    def tailplane(X, Y, Z):
        d = np.abs(Y - y)
        lead = xt + L * 0.17 - 0.65 * d
        chord = L * 0.11 * (1 - 0.6 * d / (L * 0.2))
        return (d < L * 0.2) & (X < lead) & (X > lead - chord) & (np.abs(Z - (zb + r * 2.2)) < 0.3)
    b.sol(tailplane, "white", xt, xn)

    def fin(X, Y, Z):
        h = Z - (zb + r * 2.3)
        lead = xt + L * 0.2 - 0.9 * h
        return (h > 0) & (h < L * 0.2) & (X < lead) & (X > lead - L * 0.13 * (1 - 0.45 * h / (L * 0.2))) & (np.abs(Y - y) < 0.28)
    b.sol(fin, "navy", xt, xn)
    for gx in (xn - L * 0.12, x - L * 0.02, x - L * 0.1):           # landing gear
        b.bx(gx - 0.5, gx + 0.5, y - 1.2, y + 1.2, z, zb, "dark")


# ---------------------------------------------------------------------------
# Sites
# ---------------------------------------------------------------------------

def everett_plant():
    """Boeing Everett: the world's largest building by volume, six vast hangar doors on the flight-line side
    carrying the mural of Boeing jets. 4 x 2 tiles."""
    b = site(4, 2)
    _paving(b)
    b.bx(1.0, 63.0, 1.0, 30.0, 0.25, 30.0, "membrane")
    b.bx(0.8, 63.2, 0.8, 30.2, 30.0, 31.0, "roofmetal")
    for x in np.arange(6.0, 60.0, 8.0):                          # rooftop plant
        b.bx(x, x + 3.0, 8.0, 12.0, 31.0, 33.0, "grey")
    doors = [(2.0 + i * 10.0, 11.0 + i * 10.0) for i in range(6)]
    tails = ["navy", "red", "teal", "orange", "green", "navy"]
    for (d0, d1), tail in zip(doors, tails):
        xc = (d0 + d1) / 2

        def mural(X, Y, Z, xc=xc, d0=d0, d1=d1):   # bind this door's edges, not the loop's last
            u, v = xc - X, Z - 12.0                              # u across the door, v up from its middle
            plane = ((np.abs(v - 0.2 * u) < 1.5) & (np.abs(u) < 4.4)) | \
                    ((np.abs(u - 0.6 - 0.35 * np.abs(v - 0.2 * u)) < 1.0) & (np.abs(v - 0.2 * u) < 6.0))
            return (Y > 29.95) & (Y < 30.15) & (X > d0) & (X < d1) & (Z > 0.25) & (Z < 24.0) & plane
        b.bx(d0, d1, 30.0, 30.12, 0.25, 24.0, "blue")             # sky
        b.sol(mural, "white", d0, d1)
        b.sol(lambda X, Y, Z, xc=xc: (Y > 29.95) & (Y < 30.18) & (np.abs((xc - X) - 3.6) < 0.6) &
              (Z > 12.5) & (Z < 17.5), tail, d0, d1)             # coloured tail of each mural jet
    font_sign(b, "BOEING", 32.0, 27.0, 30.2, "navy", scale=1.0)
    side_sign(b, "BOEING", 15.5, 22.0, 63.2, "navy", scale=1.0)
    return b


def renton_plant():
    """Boeing Renton (737 final assembly): two long assembly buildings on the shore of Lake Washington, blue
    hangar doors onto Renton airfield. 3 x 2 tiles."""
    b = site(3, 2)
    _paving(b)
    for y0, y1 in ((1.0, 15.0), (17.0, 31.0)):
        b.bx(1.0, 47.0, y0, y1, 0.25, 24.0, "concrete")
        b.bx(0.8, 47.2, y0 - 0.2, y1 + 0.2, 24.0, 25.0, "roofmetal")
        b.bx(4.0, 44.0, (y0 + y1) / 2 - 2.0, (y0 + y1) / 2 + 2.0, 25.0, 28.0, "roofmetal")   # roof monitor
        b.bx(4.0, 44.0, (y0 + y1) / 2 - 2.05, (y0 + y1) / 2 + 2.05, 25.6, 27.4, "window")
        b.bx(47.0, 47.12, y0 + 1.5, y1 - 1.5, 0.25, 18.0, "blue")        # end doors onto the airfield
    for d0 in (4.0, 19.0, 34.0):
        b.bx(d0, d0 + 10.0, 31.0, 31.12, 0.25, 18.0, "blue")             # flight-line doors
    font_sign(b, "BOEING", 24.0, 21.0, 31.2, "white", scale=1.0)
    return b


def jetbridge(b, rotunda, door, sill, z_rot=5.0, building_y=12.0):
    """Apron-drive passenger boarding bridge: fixed link and rotunda at the terminal, a telescoping tunnel sloping
    from the terminal's upper floor down to the door sill, a wheeled drive column near its outer end, and the cab
    against the fuselage at the door."""
    (rx, ry), (dx, dy) = rotunda, door
    cab_x = dx + 0.8                                                   # cab centre, beside the fuselage
    ex, ey = cab_x + 0.9, dy                                           # tunnel ends at the back of the cab
    b.bx(rx - 0.7, rx + 0.7, building_y, ry, z_rot, z_rot + 1.7, "white")                 # fixed link
    b.sol(lambda X, Y, Z: ((X - rx) ** 2 + (Y - ry) ** 2 <= 1.0) & (Z > z_rot - 0.3) & (Z < z_rot + 2.0), "grey",
          rx - 1.2, rx + 1.2)                                                             # rotunda
    b.sol(lambda X, Y, Z: ((X - rx) ** 2 + (Y - ry) ** 2 <= 0.16) & (Z <= z_rot - 0.3), "grey", rx - 0.5, rx + 0.5)

    vx, vy = ex - rx, ey - ry
    n = np.hypot(vx, vy)

    def along(X, Y):
        return np.clip(((X - rx) * vx + (Y - ry) * vy) / (n * n), 0, 1)

    def tunnel(X, Y, Z):
        t = along(X, Y)
        px, py = rx + t * vx, ry + t * vy
        floor = z_rot + (sill - z_rot) * t
        return ((X - px) ** 2 + (Y - py) ** 2 <= 0.75 ** 2) & (Z >= floor) & (Z <= floor + 1.6)
    lo, hi = min(rx, ex) - 1, max(rx, ex) + 1
    b.sol(tunnel, "white", lo, hi)
    b.sol(lambda X, Y, Z: tunnel(X, Y, Z) & (np.abs(Z - (z_rot + (sill - z_rot) * along(X, Y)) - 1.0) < 0.25), "glass", lo, hi)
    t = 0.75                                                           # drive column and its wheel bogie
    cx_, cy_ = rx + t * vx, ry + t * vy
    floor = z_rot + (sill - z_rot) * t
    b.bx(cx_ - 0.25, cx_ + 0.25, cy_ - 0.6, cy_ - 0.3, 0.6, floor, "grey")
    b.bx(cx_ - 0.25, cx_ + 0.25, cy_ + 0.3, cy_ + 0.6, 0.6, floor, "grey")
    b.bx(cx_ - 0.6, cx_ + 0.6, cy_ - 0.8, cy_ + 0.8, 0.25, 0.6, "dark")
    b.bx(cab_x - 0.8, cab_x + 0.8, dy - 0.9, dy + 0.9, sill - 0.2, sill + 1.8, "grey")    # cab at the door
    b.bx(dx - 0.05, cab_x - 0.8, dy - 0.7, dy + 0.7, sill, sill + 1.6, "dark")            # canopy to the fuselage


def seattle_delivery_center():
    """Boeing's Seattle Delivery Center at Boeing Field: a three-storey glass-fronted building on the flight line
    with covered jetways to new 737s parked nose-in at two gates. 2 x 2 tiles."""
    b = site(2, 2)
    _paving(b)
    ground(b, 0, 32, 14, 32, "asphalt")
    b.bx(2.0, 30.0, 1.5, 12.0, 0.25, 15.0, "white")
    b.bx(1.8, 30.2, 1.3, 12.2, 15.0, 15.8, "roofmetal")
    b.bx(2.0, 30.0, 12.0, 12.12, 1.0, 14.0, "glass")                   # glass flight-line front
    for z in (5.0, 9.6):
        b.bx(2.0, 30.0, 12.0, 12.16, z, z + 0.5, "white")                # floor slabs
    b.bx(30.0, 30.12, 2.5, 11.0, 1.0, 14.0, "glass")
    font_sign(b, "BOEING", 16.0, 12.0, 12.25, "navy", scale=1.0)
    for cx in (9.0, 23.0):                                             # two gates, 737s parked nose-in
        L, cy = 11.0, 24.5
        airliner(NoseIn(b, cx, cy), cx, cy, 0.25, L, "white", "navy")
        r = L * 0.06
        # nose to -Y, so the aircraft's left (port) side is +X; L1 is just behind the cockpit
        jetbridge(b, (cx + 3.4, 13.4), (cx + r + 0.55, cy - L / 2 + L * 0.16), 0.25 + r + 0.6)
    return b


def dreamlifter_airport():
    """Paine Field, compressed: runway with markings, parallel taxiway, the Dreamlifter Operations Center, a
    control tower and a Dreamlifter (747 LCF) on the apron. 6 x 3 tiles."""
    b = site(6, 3)
    ground(b, 0, 96, 0, 48, "grass")
    ground(b, 0, 96, 36, 45, "asphalt")                                   # runway
    b.sol(lambda X, Y, Z: (Z <= 0.3) & (np.abs(Y - 40.5) < 0.25) & (np.mod(X, 6.0) < 3.0) & (X > 8) & (X < 88), "white")
    b.sol(lambda X, Y, Z: (Z <= 0.3) & ((X < 5.0) | (X > 91.0)) & (np.mod(Y - 36.0, 1.6) < 0.8) & (Y > 37) & (Y < 44), "white")
    ground(b, 6, 90, 29, 33, "asphalt")                                   # taxiway
    for x in (10.0, 86.0):
        ground(b, x, x + 3, 33, 36, "asphalt")                             # connectors
    ground(b, 2, 80, 2, 29, "asphalt")                                    # apron, same grey as the taxiways
    b.bx(4.0, 28.0, 3.0, 19.0, 0.25, 14.0, "white")                       # Dreamlifter Operations Center hangar
    b.sol(lambda X, Y, Z: (X > 3.8) & (X < 28.2) & (Z > 14.0) & (((Y - 11.0) / 8.2) ** 2 + ((Z - 14.0) / 5.0) ** 2 <= 1), "roofmetal", 3.8, 28.2)
    b.bx(6.0, 26.0, 19.0, 19.12, 0.25, 13.0, "grey")
    font_sign(b, "BOEING", 16.0, 16.5, 19.1, "navy")
    # control tower
    b.sol(lambda X, Y, Z: (((X - 34.0) ** 2 + (Y - 8.0) ** 2) <= 1.8 ** 2) & (Z <= 22.0), "white", 31.0, 37.0)
    b.bx(31.5, 36.5, 5.5, 10.5, 22.0, 25.0, "glass")
    b.bx(31.2, 36.8, 5.2, 10.8, 25.0, 25.8, "white")
    b.bx(33.0, 35.0, 11.0, 14.0, 0.25, 4.0, "white")
    # the 747 itself is WAS's sprite, pasted in by make_art (see INDUSTRIES overlays)
    return b


def oil_terminal():
    """Marine oil terminal: tank farm inside bund walls, pipe racks and a tanker jetty with loading arms at the
    shoreline end. 3 x 2 tiles; place it with the jetty (+X end) on the coast."""
    b = site(3, 2)
    _paving(b, "concrete")
    ground(b, 1, 31, 1, 31, "grass")
    b.bx(1.0, 31.0, 1.0, 1.6, 0.25, 1.4, "concrete")                       # bund walls
    b.bx(1.0, 31.0, 30.4, 31.0, 0.25, 1.4, "concrete")
    b.bx(1.0, 1.6, 1.0, 31.0, 0.25, 1.4, "concrete")
    b.bx(30.4, 31.0, 1.0, 31.0, 0.25, 1.4, "concrete")
    for cx, cy in ((8.5, 8.5), (23.5, 8.5), (8.5, 23.5), (23.5, 23.5)):
        b.sol(lambda X, Y, Z, cx=cx, cy=cy: [
            ((((X - cx) ** 2 + (Y - cy) ** 2) <= 5.6 ** 2) & (Z <= 11.0), "white"),
            ((((X - cx) ** 2 + (Y - cy) ** 2) <= 5.6 ** 2) & (Z <= 11.0) & (np.abs(Z - 7.0) < 0.6), "red"),
            ((((X - cx) ** 2 + (Y - cy) ** 2) <= (5.6 * (1 - (Z - 11.0) / 2.0)) ** 2) & (Z > 11.0) & (Z <= 13.0), "roof")],
            None, cx - 6, cx + 6)
    for y in (15.0, 17.0):                                                 # pipe rack to the jetty
        b.bx(16.0, 44.0, y - 0.3, y + 0.3, 2.0, 2.6, "steel")
    for x in np.arange(18.0, 44.0, 4.0):
        b.bx(x, x + 0.4, 14.4, 17.6, 0.25, 2.0, "grey")
    ground(b, 33, 48, 2, 30, "concrete")
    b.bx(44.0, 48.0, 2.0, 30.0, 0.25, 1.6, "concrete")                      # jetty head
    for y in (7.0, 16.0, 25.0):                                            # loading arms
        b.bx(45.0, 45.6, y - 0.3, y + 0.3, 1.6, 7.0, "orange")
        b.bx(45.0, 47.6, y - 0.3, y + 0.3, 6.6, 7.2, "orange")
    b.bx(36.0, 41.0, 22.0, 28.0, 0.25, 4.5, "white")                         # control building
    return b


def dhc_victoria():
    """De Havilland Canada at Victoria International Airport (de Havilland Way): a big white manufacturing hangar
    with a red band and the company name, an office wing, and Twin Otters on floats outside. 2 x 2 tiles."""
    b = site(2, 2)
    _paving(b)
    ground(b, 0, 32, 20, 32, "asphalt")
    b.bx(2.0, 30.0, 2.0, 19.0, 0.25, 18.0, "white")                         # hangar
    b.sol(lambda X, Y, Z: (X > 1.8) & (X < 30.2) & (Z > 18.0) & (Z <= 18.0 + (8.7 - np.abs(Y - 10.5)) * 0.45), "roofmetal", 1.8, 30.2)
    b.bx(2.0, 30.0, 18.98, 19.1, 12.0, 14.0, "red")                          # red band
    b.bx(30.0, 30.12, 2.5, 18.5, 12.0, 14.0, "red")
    b.bx(4.0, 20.0, 19.0, 19.12, 0.25, 11.0, "grey")                          # hangar door
    b.sol(lambda X, Y, Z: (Y > 18.95) & (Y < 19.15) & (X > 4) & (X < 20) & (Z < 11) & (np.mod(X, 2.0) < 0.12), "steel", 4.0, 20.0)
    font_sign(b, "DE HAVILLAND", 16.0, 16.0, 19.2, "red")
    b.bx(22.0, 30.0, 12.0, 19.0, 0.25, 9.0, "stucco")                         # office wing
    b.bx(22.0, 30.0, 19.0, 19.12, 2.0, 7.5, "glass")
    twin_otter(b, 9.0, 26.0, 0.25)
    twin_otter(b, 22.0, 27.0, 0.25, body="white", stripe="navy")
    return b
