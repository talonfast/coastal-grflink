"""
Buses, streetcars and trains on the ship voxel renderer.

Local coordinates: u along the vehicle (+u = front), v across (+v = left), w up; all in OpenTTD
world units. One articulated part or rail car is `length` units long (8 = a standard half-tile
vehicle). Widths and heights are exaggerated like the aircraft so the vehicles read at 1x zoom.

A shortened road vehicle part keeps its front at the full-length front (OpenTTD moves its centre
(8 - length) / 2 forward), so its model is built `shift` units ahead of the origin.
"""
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), "common"))

import numpy as np

import render
from render import Ship, SCALE, ZS

# Transit colours. Registered here rather than in render.MAT, which every set's render depends on.
for _name, _rgb in {
    "bctblue": (0, 74, 152), "bctred": (206, 32, 44), "bctgreen": (0, 132, 74),
    "tlblue": (0, 86, 162), "tlgreen": (110, 184, 40),
    "ssred": (196, 28, 40), "pdxteal": (0, 138, 146), "pdxblue": (28, 74, 156),
    "linknavy": (18, 40, 92), "linkteal": (0, 150, 140),
    "mk5blue": (0, 84, 172), "mk5dark": (0, 46, 112),
    "evergreen": (24, 74, 52), "cascream": (232, 224, 198), "mocha": (112, 76, 54),
    "edekayellow": (255, 210, 0), "edekablue": (0, 64, 152), "primer": (120, 160, 96),
    "bellows": (44, 44, 46), "lamp": (255, 246, 210), "taillamp": (220, 30, 30), "destsign": (250, 170, 40),
}.items():
    render.MAT_ID[_name] = render._next_mat[0]
    render.MAT_RGB[render._next_mat[0]] = _rgb
    render._next_mat[0] += 1


class Geo:
    """What a livery painter gets: local coordinates and the faces of the body."""

    def __init__(self, u, v, w, hl, B, z0, z1):
        self.u, self.v, self.w, self.z0, self.z1 = u, v, w, z0, z1
        self.side = np.abs(v) > B / 2 - 0.2
        self.front = (u > 0) & (u > hl - 0.2)
        self.rear = (u < 0) & (-u > hl - 0.2)
        self.right = v < 0                       # the kerb side in North America


def band(w, w0, w1):
    return (w > w0) & (w <= w1)


def panes(u, pitch, duty=0.82):
    """Window panes along u, with pillars between them."""
    return np.mod(u, pitch) < pitch * duty


def seg(U, W, p, q, t):
    """Points within t of the segment p-q in the u-w plane."""
    (pu, pw), (qu, qw) = p, q
    du, dw = qu - pu, qw - pw
    k = np.clip(((U - pu) * du + (W - pw) * dw) / (du * du + dw * dw), 0, 1)
    return (U - pu - k * du) ** 2 + (W - pw - k * dw) ** 2 <= t * t


class Car(Ship):
    def __init__(self, length, width, top, shift=0.0):
        super().__init__(length + 2 * abs(shift), width, "double", taper=0.01, blunt=1.0)
        self.scale = 1.0 / SCALE                 # model units are world units
        self.wake = False
        self.weather = 0.0
        self.length, self.shift, self.top_z = length, shift, top

    def _top(self):
        return self.top_z + 1.6                  # room for a pantograph

    # --- geometry --------------------------------------------------------
    def body(self, z0, z1, paint=None, front=None, rear=None, trim=(0.0, 0.0), r_plan=0.35,
             r_roof=0.4, mat="white", ends=True):
        """Rounded box from w = z0 to z1. front / rear: None (upright end) or (rake, w_from, power):
        the end face leans back by `rake` at the roof, from height w_from. trim: (front, rear)
        shortens the body at that end (room for bellows or a gangway). ends=False: the painter
        sees no front or rear face (middle sections have no windscreen)."""
        def end_hl(W, end, t):
            hl = np.full(W.shape, self.length / 2 - t, np.float32)
            if end:
                rake, wf, pw = end
                hl -= rake * np.clip((W - wf) / (z1 - wf), 0, 1) ** pw
            return hl

        def fn(U, V, W):
            u = U - self.shift
            hl = np.where(u >= 0, end_hl(W, front, trim[0]), end_hl(W, rear, trim[1]))
            du = np.abs(u) - (hl - r_plan)
            dv = np.abs(V) - (self.B / 2 - r_plan)
            plan = ((du <= 0) | (dv <= 0) | (du ** 2 + dv ** 2 <= r_plan ** 2)) & (du <= r_plan)
            dz = W - (z1 - r_roof)
            dv2 = np.abs(V) - (self.B / 2 - r_roof)
            sect = (dz <= 0) | (dv2 <= 0) | (dz ** 2 + dv2 ** 2 <= r_roof ** 2)
            inside = plan & sect & (np.abs(V) <= self.B / 2) & (W > z0) & (W <= z1)
            out = [(inside, mat)]
            if paint:
                g = Geo(u, V, W, hl, self.B, z0, z1)
                if not ends:
                    g.front = g.rear = np.zeros_like(g.side)
                for m, name in paint(g):
                    out.append((inside & m, name))
            return out
        return self.solid(fn, None)

    def wheels(self, us, r=0.5, inset=0.1, depth=0.5, both=True):
        """Wheels (tyre with a steel hub) at the body sides, at positions us along the vehicle."""
        rw = r * 1.15 / ZS                        # round on screen despite the vertical stretch
        for uc in us:
            uc += self.shift

            def fn(U, V, W, uc=uc):
                av = np.abs(V) if both else -V
                rim = (av > self.B / 2 - inset - depth) & (av <= self.B / 2 - inset)
                q = ((U - uc) / r) ** 2 + ((W - rw) / rw) ** 2
                return [(rim & (q <= 1), "tyre"), (rim & (q <= 0.25) & (av > self.B / 2 - inset - 0.06), "steel")]
            self.solid(fn, None, uc - r, uc + r)
        return self

    def bogies(self, us, z_top, r=0.38, span=0.75):
        """Rail bogies: a dark frame with two wheelsets each, under the body."""
        for uc in us:
            self.box(uc + self.shift - span - 0.25, uc + self.shift + span + 0.25, -self.B / 2 + 0.3,
                     self.B / 2 - 0.3, r * 0.6, z_top, "dark")
            self.wheels([uc - span / 2 - 0.2, uc + span / 2 + 0.2], r=r, inset=0.2, depth=0.35)
        return self

    def bellows(self, end, z0, z1, depth=0.3):
        """Rubber concertina at an articulation (end +1 = front, -1 = rear)."""
        a = end * self.length / 2
        u0, u1 = sorted((a, a - end * depth))
        return self.box(u0 + self.shift, u1 + self.shift, -self.B / 2 + 0.25, self.B / 2 - 0.25,
                        z0 + 0.15, z1 - 0.25, "bellows")

    def pantograph(self, u, z):
        u += self.shift
        self.box(u - 0.4, u + 0.4, -0.5, 0.5, z, z + 0.15, "dark")

        def fn(U, V, W):
            arm = (np.abs(np.abs(V) - 0.3) < 0.06)
            lower = seg(U, W, (u - 0.35, z + 0.15), (u + 0.2, z + 0.8), 0.06)
            upper = seg(U, W, (u + 0.2, z + 0.8), (u - 0.1, z + 1.3), 0.06)
            head = (np.abs(U - (u - 0.1)) < 0.08) & (np.abs(V) < 0.6) & band(W, z + 1.25, z + 1.38)
            return [(arm & (lower | upper), "steel"), (head, "steel")]
        return self.solid(fn, None, u - 0.6, u + 0.6)


# --------------------------------------------------------------------------- buses

BUS_W = 2.7


def _enviro500(livery):
    """Alexander Dennis Enviro500 (tri-axle, 12.8 m): BC Transit's Victoria double-decker."""
    z0, z1 = 0.45, 5.7
    c = Car(8, BUS_W, z1)

    def paint(g):
        u, w = g.u, g.w
        out = []
        if livery == "classic":                  # white with BC Transit blue and red bands
            out += [(w <= z0 + 0.55, "bctblue"), (band(w, 1.65, 1.85), "bctred"),
                    (band(w, 3.35, 3.85), "bctblue")]
        else:                                    # 2024: green front, white back, diagonal swoop
            out += [(u + 0.6 * (w - z0) > -0.4 + 0.25 * np.sin(w * 1.3), "bctgreen"),
                    (w <= z0 + 0.35, "dark")]
        out += [
            (g.side & band(w, 2.0, 3.2) & (u > -3.5) & (u < 3.0) & panes(u, 0.95), "window"),
            (g.side & band(w, 4.0, 5.25) & (u > -3.7) & (u < 3.7) & panes(u, 0.95), "window"),
            (g.side & g.right & band(w, z0, 3.3) & (((u > 2.75) & (u < 3.55)) | ((u > -0.3) & (u < 0.5))), "glass"),
            (g.front & band(w, 1.5, 3.2), "window"),
            (g.front & band(w, 3.4, 3.75), "dark"),
            (g.front & band(w, 3.5, 3.65) & (np.abs(g.v) < 0.8), "destsign"),
            (g.front & band(w, 4.0, 5.3), "window"),
            (g.front & band(w, 0.8, 1.1) & (np.abs(g.v) > 0.8), "lamp"),
            (g.rear & band(w, 1.0, 1.6) & (np.abs(g.v) > 1.0), "taillamp"),
            (g.rear & band(w, 0.6, 1.4) & (np.abs(g.v) < 0.9), "louvre"),
            (g.rear & band(w, 4.2, 5.2) & (np.abs(g.v) < 1.0), "window"),
            (w > z1 - 0.12, "roof"),
        ]
        return out
    c.body(z0, z1, paint, front=(0.15, 1.0, 1.0), r_plan=0.3, r_roof=0.35)
    return c.wheels([2.5, -1.6, -2.5])


def enviro500_classic():
    return _enviro500("classic")


def enviro500_green():
    return _enviro500("green")


def _translink_paint(rear_part):
    """TransLink white with a blue skirt and front, and the green splash towards the back."""
    def paint(g):
        u, w = g.u, g.w
        out = [(w <= 0.45 + 0.6, "tlblue"), (g.front & (w < 3.5), "tlblue")]
        if rear_part:
            out.append((g.side & (u - 0.7 * w < -2.2) & (w < 3.6), "tlgreen"))
        out += [
            (g.side & band(w, 1.9, 3.35) & panes(u, 1.0, 0.86), "window"),
            (g.front & band(w, 1.5, 3.5) & (np.abs(g.v) < 1.25), "window"),
            (g.front & band(w, 3.55, 3.85) & (np.abs(g.v) < 0.9), "destsign"),
            (g.front & band(w, 0.8, 1.1) & (np.abs(g.v) > 0.8), "lamp"),
            (g.rear & band(w, 1.0, 1.6) & (np.abs(g.v) > 1.0), "taillamp"),
            (g.rear & band(w, 0.6, 1.5) & (np.abs(g.v) < 0.9), "louvre"),
            (w > 4.0 - 0.12, "roof"),
        ]
        doors = ((2.85, 3.6), (-0.8, -0.05)) if not rear_part else ((1.4, 2.15),)
        for d0, d1 in doors:
            out.append((g.side & g.right & band(w, 0.45, 3.4) & (u > d0) & (u < d1), "glass"))
        return out
    return paint


def xde60_front():
    """New Flyer XDE60 (18 m articulated diesel-electric hybrid), front section."""
    c = Car(8, BUS_W, 4.0)
    c.body(0.45, 4.0, _translink_paint(False), front=(0.1, 1.0, 1.0), trim=(0.0, 0.3))
    c.bellows(-1, 0.45, 4.0)
    c.box(-1.2, 1.0, -0.9, 0.9, 4.0, 4.45, "roof")        # air conditioning
    c.box(1.6, 3.2, -1.0, 1.0, 4.0, 4.35, "roof")         # hybrid battery pod
    return c.wheels([2.4, -2.3])


def xde60_rear():
    """XDE60 rear section (7/8 long): the engine is at the back."""
    c = Car(7, BUS_W, 4.0, shift=0.5)
    c.body(0.45, 4.0, _translink_paint(True), trim=(0.3, 0.0))
    c.bellows(1, 0.45, 4.0)
    c.box(-3.4 + 0.5, -2.0 + 0.5, -1.0, 1.0, 4.0, 4.4, "roof")   # engine air intakes
    return c.wheels([-2.0])


# --------------------------------------------------------------------------- streetcars and LRVs

def _tram_cab(paint, B, z0, z1, nose, r_plan, pan=None):
    """Cab section: cab at the front, articulation at the back."""
    c = Car(8, B, z1)
    c.body(z0, z1, paint, front=nose, trim=(0.0, 0.25), r_plan=r_plan, r_roof=0.45)
    c.bellows(-1, z0, z1, 0.25)
    if pan is not None:
        c.pantograph(pan, z1)
    c.box(-1.0, 1.0, -0.9, 0.9, z1, z1 + 0.3, "roof")
    return c.wheels([2.3, -2.3], r=0.42, inset=0.25, depth=0.4)


def _tram_mid(paint, B, z0, z1, length, pan=False, wheels=False):
    """Middle section between two articulations."""
    s = (8 - length) / 2
    c = Car(length, B, z1, shift=s)
    c.body(z0, z1, paint, trim=(0.25, 0.25), r_plan=0.15, r_roof=0.45, ends=False)
    if pan:
        c.pantograph(0.0, z1)
    if wheels:
        c.wheels([0.0], r=0.42, inset=0.25, depth=0.4)
    return c


def _streetcar_paint(lower, upper, belt="white"):
    def paint(g):
        u, w = g.u, g.w
        return [
            (w <= 2.05, lower), (band(w, 1.85, 2.05), belt), (w > 3.75, upper),
            (g.side & band(w, 2.05, 3.65) & panes(u, 1.05, 0.88), "window"),
            (g.side & band(w, 0.55, 3.65) & (np.abs(u - 1.0) < 0.45), "glass"),      # doors
            (g.front & band(w, 1.7, 3.9) & (np.abs(g.v) < 1.15), "window"),
            (g.front & band(w, 3.95, 4.3) & (np.abs(g.v) < 0.8), "destsign"),
            (g.front & band(w, 1.0, 1.25) & (np.abs(g.v) > 0.7), "lamp"),
            (w > 4.6 - 0.12, "roof"),
        ]
    return paint


TRAM_W, TRAM_Z0, TRAM_Z1 = 2.7, 0.55, 4.6
SEATTLE = _streetcar_paint("ssred", "ssred")
PORTLAND = _streetcar_paint("pdxteal", "pdxblue")


def seattle_cab():
    """Inekon 12 Trio, Seattle Streetcar (South Lake Union, 2007): cab section."""
    return _tram_cab(SEATTLE, TRAM_W, TRAM_Z0, TRAM_Z1, (0.45, 2.6, 1.5), 0.55)


def seattle_mid():
    return _tram_mid(SEATTLE, TRAM_W, TRAM_Z0, TRAM_Z1, 4, pan=True)


def portland_cab():
    """Skoda 10 T, Portland Streetcar (2001): cab section."""
    return _tram_cab(PORTLAND, TRAM_W, TRAM_Z0, TRAM_Z1, (0.6, 2.2, 1.2), 0.7)


def portland_mid():
    return _tram_mid(PORTLAND, TRAM_W, TRAM_Z0, TRAM_Z1, 4, pan=True)


LRV_W, LRV_Z0, LRV_Z1 = 3.0, 0.7, 5.0


def _link_paint(series):
    """Sound Transit Link: white with a navy skirt and the teal "waves" along the windows."""
    win0, win1 = (2.0, 3.7) if series == 1 else (1.8, 3.95)

    def paint(g):
        u, w = g.u, g.w
        wave = 1.55 + 0.18 * np.sin(u * 1.4)
        return [
            (w <= 1.35, "linknavy"),
            (band(w, wave - 0.15, wave + 0.12), "linkteal"),
            (band(w, wave + 0.12, wave + 0.24), "linknavy"),
            (g.side & band(w, win0, win1) & panes(u, 1.2, 0.88), "window"),
            (g.side & band(w, 0.7, win1) & (np.abs(u - 0.6) < 0.5), "glass"),       # doors
            (g.front & band(w, 1.0, 1.9), "linknavy"),
            (g.front & band(w, 1.9, 4.2) & (np.abs(g.v) < 1.3), "window"),
            (g.front & band(w, 4.25, 4.6) & (np.abs(g.v) < 0.9), "destsign"),
            (g.front & band(w, 1.25, 1.5) & (np.abs(g.v) > 0.85), "lamp"),
            (w > LRV_Z1 - 0.12, "roof"),
        ]
    return paint


def link1_cab():
    """Kinkisharyo low-floor LRV, Sound Transit Link Series 1 (2009): cab section."""
    return _tram_cab(_link_paint(1), LRV_W, LRV_Z0, LRV_Z1, (0.7, 2.4, 1.3), 0.5, pan=-2.2)


def link1_mid():
    return _tram_mid(_link_paint(1), LRV_W, LRV_Z0, LRV_Z1, 6, wheels=True)


def link2_cab():
    """Siemens S70, Sound Transit Link Series 2 (2021): rounder nose, bigger windows."""
    return _tram_cab(_link_paint(2), LRV_W, LRV_Z0, LRV_Z1, (0.9, 2.0, 1.6), 0.8, pan=-2.2)


def link2_mid():
    return _tram_mid(_link_paint(2), LRV_W, LRV_Z0, LRV_Z1, 6, wheels=True)


# --------------------------------------------------------------------------- trains

RAIL_W = 3.0


def _mk5_paint(g):
    """SkyTrain Mark V: all-over TransLink blue, dark skirt and window band."""
    u, w = g.u, g.w
    out = [
        (w <= 1.6, "mk5dark"),
        (g.side & band(w, 2.2, 3.6), "mk5dark"),
        (g.side & band(w, 2.3, 3.5) & panes(u, 0.9, 0.8), "window"),
        (g.front & band(w, 2.3, 4.0) & (np.abs(g.v) < 1.25), "window"),
        (g.front & band(w, 1.75, 1.95) & (np.abs(g.v) > 0.5) & (np.abs(g.v) < 1.3), "lamp"),
        (w > 4.8 - 0.12, "roof"),
    ]
    for uc in (-1.7, 1.7):                       # two doors per side
        door = g.side & band(w, 0.9, 3.95) & (np.abs(u - uc) < 0.5)
        out += [(door, "steel"), (door & band(w, 2.3, 3.6) & (np.abs(u - uc) < 0.4), "window")]
    return out


def mk5_cab():
    """Alstom Mark V SkyTrain (2025): cab car of the five-car train."""
    c = Car(8, RAIL_W, 4.8)
    c.body(0.9, 4.8, _mk5_paint, front=(1.0, 2.2, 1.6), trim=(0.0, 0.15), r_plan=0.7, r_roof=0.5,
           mat="mk5blue")
    c.box(-4.0, -3.85, -0.8, 0.8, 1.0, 4.4, "bellows")      # gangway
    return c.bogies([2.5, -2.5], 0.95)


def mk5_mid():
    c = Car(8, RAIL_W, 4.8)
    c.body(0.9, 4.8, _mk5_paint, trim=(0.15, 0.15), r_plan=0.1, r_roof=0.5, mat="mk5blue", ends=False)
    c.box(3.85, 4.0, -0.8, 0.8, 1.0, 4.4, "bellows")
    c.box(-4.0, -3.85, -0.8, 0.8, 1.0, 4.4, "bellows")
    return c.bogies([2.5, -2.5], 0.95)


def _cascades_paint(coach):
    """Amtrak Cascades: cream with an evergreen band under the roof, a mocha stripe and the
    Cascade Range drawn in evergreen along the bottom of the car."""
    def paint(g):
        u, w = g.u, g.w
        peaks = 2.1 + 0.55 * (1 - np.abs(np.mod(u * 0.55, 2.0) - 1)) * (0.6 + 0.4 * np.sin(u * 2.3) ** 2)
        out = [
            (g.side & band(w, 4.0, 4.5), "evergreen"),
            (w > 4.5, "roof"),
            (band(w, 1.0, 1.75), "mocha"),
            (g.side & band(w, 1.75, peaks), "evergreen"),
        ]
        if coach:
            out.append((g.side & band(w, 2.8, 3.85) & (np.abs(u) < 3.0) & panes(u, 0.85, 0.84), "window"))
            for uc in (-3.3, 3.3):
                out.append((g.side & band(w, 1.0, 4.0) & (np.abs(u - uc) < 0.3), "steel"))
        return out
    return paint


def _cab_paint(base, end):
    """Cab end: windscreen and lamps on the (end) face, end = "front" or "rear"."""
    def paint(g):
        face = getattr(g, end)
        v, w = np.abs(g.v), g.w
        return base(g) + [
            (face & band(w, 1.0, 2.8), "evergreen"),
            (face & band(w, 3.1, 4.3) & (v < 1.3), "window"),
            (face & band(w, 1.5, 1.8) & (v > 0.7) & (v < 1.3), "lamp"),
        ]
    return paint


def alc42e():
    """Siemens Charger ALC-42E in the Amtrak Cascades livery: the Airo trainset's locomotive."""
    c = Car(8, RAIL_W, 5.2)

    def paint(g):
        u, w = g.u, g.w
        return _cab_paint(_cascades_paint(False), "front")(g) + [
            (g.side & band(w, 3.2, 4.2) & (u > 2.4) & (u < 3.1), "window"),           # cab side window
            (g.side & band(w, 3.0, 4.2) & (u > -3.2) & (u < 1.6) & (np.mod(u, 0.3) < 0.12), "louvre"),
            (g.rear & band(w, 1.2, 1.5) & (np.abs(g.v) > 0.8), "lamp"),
        ]
    c.body(1.0, 5.2, paint, front=(1.5, 2.9, 1.0), trim=(0.0, 0.1), r_plan=0.4, r_roof=0.5, mat="cascream")
    c.box(-2.0, 0.5, -0.9, 0.9, 5.2, 5.45, "roof")              # radiator fans
    c.exhaust(-0.5, 0.0, 5.5)
    return c.bogies([2.4, -2.4], 1.0)


def airo_coach():
    """Siemens Venture coach of the Cascades Airo trainset."""
    c = Car(8, RAIL_W, 5.0)
    c.body(1.0, 5.0, _cascades_paint(True), trim=(0.15, 0.15), r_plan=0.15, r_roof=0.55, mat="cascream",
           ends=False)
    c.box(3.85, 4.0, -0.8, 0.8, 1.1, 4.6, "bellows")
    c.box(-4.0, -3.85, -0.8, 0.8, 1.1, 4.6, "bellows")
    return c.bogies([2.6, -2.6], 1.0)


def airo_cab():
    """Airo cab car: a coach with a driving cab at the back, to end the train."""
    c = Car(8, RAIL_W, 5.0)
    c.body(1.0, 5.0, _cab_paint(_cascades_paint(True), "rear"), rear=(1.4, 2.9, 1.0), trim=(0.15, 0.0),
           r_plan=0.4, r_roof=0.55, mat="cascream")
    c.box(3.85, 4.0, -0.8, 0.8, 1.1, 4.6, "bellows")
    return c.bogies([2.6, -2.6], 1.0)


# ---------------------------------------------------------------------------
# FIRS PNW freight: aircraft and EDEKA sandwiches
# ---------------------------------------------------------------------------

render.FONT.setdefault("D", ["110", "101", "101", "101", "110"])   # render.FONT has no D; EDEKA needs one


def _flatcar():
    c = Car(8, RAIL_W, 4.6)
    c.box(-4.0, 4.0, -1.25, 1.25, 1.0, 1.35, "dark")
    return c


def aircraft_car():
    """Heavy flatcar with a 737 fuselage in green primer, the way Boeing's fuselages travel by rail."""
    c = _flatcar()
    c.ellipsoid(0.0, 0.0, 2.55, 3.95, 1.12, 1.18, "primer")
    c.solid(lambda U, V, W: (np.abs(W - 2.85) < 0.12) & (np.abs(U) < 3.0) & (np.mod(U, 0.45) < 0.2), "dark")
    for u in (-3.0, 3.0):
        c.box(u - 0.3, u + 0.3, -0.9, 0.9, 1.35, 1.75, "steel")       # cradles
    return c.bogies([2.6, -2.6], 1.0)


def _edeka_box(c, u0, u1, w0, w1, half_width):
    c.box(u0, u1, -half_width, half_width, w0, w1, "edekayellow")
    c.box(u0, u1, -half_width - 0.01, half_width + 0.01, w1 - 0.45, w1 - 0.2, "edekablue")
    mid, h = (w0 + w1 - 0.45) / 2, 0.9
    for side in (1, -1):                                              # lettering reads front-to-back on the left,
        c.solid(lambda U, V, W, side=side, um=(u0 + u1) / 2:            # back-to-front on the right
                (side * V > half_width - 0.05) & (side * V < half_width + 0.03) &
                render.text_mask(side * (um - U), W, "EDEKA", 0.0, mid, h), "edekablue", u0, u1)


def edeka_container_wagon():
    """Flatcar with two EDEKA reefer containers."""
    c = _flatcar()
    for u0, u1 in ((-3.9, -0.1), (0.1, 3.9)):
        _edeka_box(c, u0, u1, 1.35, 3.9, 1.2)
    return c.bogies([2.6, -2.6], 1.0)


def edeka_truck():
    """EDEKA box truck delivering Gouda sandwiches to the grocery stores."""
    c = Car(8, BUS_W, 4.2)
    c.box(2.3, 3.95, -1.15, 1.15, 0.45, 2.9, "white")
    c.box(3.9, 3.98, -1.0, 1.0, 1.8, 2.7, "window")
    c.box(3.9, 3.98, -1.0, 1.0, 0.7, 0.95, "lamp")
    _edeka_box(c, -4.0, 2.2, 0.55, 3.9, 1.25)
    return c.wheels([3.0, -1.4, -2.6])
