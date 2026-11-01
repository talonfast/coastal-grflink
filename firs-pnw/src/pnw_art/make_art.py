"""
FIRS PNW industry and cargo art, rendered with coastal-grflink's voxel renderer in its classic (8-bit,
base-set) style.

Each new industry keeps the tile layouts it was cloned from; this script repaints the building rectangles of
its sprite sheet (src/graphics/industries/<id>.png) with one-tile models, and the cargo icon slots of the new
cargos in src/graphics/cargoicons.png. Sheets whose rectangles are too short for their buildings are grown,
and the rectangle in the industry file is updated to match.

    python src/pnw_art/make_art.py            # render and write the sheets
    python src/pnw_art/make_art.py --check    # only check the written sheets
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path(__file__).resolve().parent.parent
GRFLINK = Path(r"G:\dev\coastal-grflink")
sys.path.insert(0, str(GRFLINK / "terminals" / "src"))
sys.path.insert(0, str(GRFLINK / "common"))
sys.path.insert(0, str(GRFLINK / "aircraft" / "src"))   # the BC Aviation airliner models

import buildings  # noqa: E402
import render  # noqa: E402
from buildings import Building, _paving, control_tower  # noqa: E402

# we only need 1x sprites: voxels 4x coarser than coastal-grflink's 4x-zoom default are still finer than a 1x pixel
buildings.BASE_STEP = 0.1

GFX = SRC / "graphics"
FIRS_PAL = Image.open(GFX / "industries" / "dairy.png").getpalette()[:768]
# indices FIRS shows differently from the DOS palette: its recolour ranges and animated colours; never use them
RESERVED = {i for i in range(256) if FIRS_PAL[3 * i:3 * i + 3] != list(render.DOS_PAL)[3 * i:3 * i + 3]}
ALLOWED = np.array([i for i in render.USABLE if i not in RESERVED])
ALLOWED_RGB = np.array([render.DOS_PAL[3 * i:3 * i + 3] for i in ALLOWED], np.float32)


def quantise(rgba):
    """RGBA float -> FIRS-safe DOS palette indices, 0 where transparent."""
    h, w, _ = rgba.shape
    rgb = rgba[..., :3].reshape(-1, 3)
    op = rgba[..., 3].reshape(-1) >= 0.5
    out = np.zeros(h * w, np.uint8)
    diff = rgb[op][:, None, :] - ALLOWED_RGB[None, :, :]
    d = ((diff * np.array([0.30, 0.59, 0.11]) * 3) ** 2).sum(-1) + 0.5 * (diff ** 2).sum(-1)
    out[op] = ALLOWED[np.argmin(d, axis=1)]
    return out.reshape(h, w)


# ---------------------------------------------------------------------------
# One-tile models. X, Y in 0..16 (footprint), Z in pixels. +X and +Y faces are the visible ones.
# ---------------------------------------------------------------------------

def tile():
    b = Building(1, 1)
    b.style = "classic"
    return b


# render.FONT has only the letters coastal-grflink needed; add the ones our signs use
FONT = {**render.FONT,
        "D": ["110", "101", "101", "101", "110"], "G": ["011", "100", "101", "101", "011"],
        "Q": ["010", "101", "101", "110", "011"], "M": ["101", "111", "111", "101", "101"],
        "P": ["110", "101", "110", "100", "100"], "T": ["111", "010", "010", "010", "010"]}


def sign(b, text, x_center, z_mid, y_face, mat, col_w=0.5):
    """3x5 pixel lettering standing on the +Y face, reading left to right on screen."""
    total = len(text) * 4 - 1

    def mask(X, Y, Z):
        c = np.floor((x_center - X) / col_w + total / 2).astype(int)
        r = np.floor(z_mid + 2.5 - Z).astype(int)
        ok = (Y > y_face - 0.3) & (Y <= y_face + 0.05) & (c >= 0) & (c < total) & (r >= 0) & (r < 5)
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
    half = total * col_w / 2 + 0.5
    b.sol(mask, mat, x_center - half, x_center + half)  # only scan the sign's own strip


def yard(mat="concrete"):
    b = tile()
    _paving(b, mat)
    return b


def hall(h, wall="white", roof="roofmetal", door="grey", text=None, text_mat="navy", text_bg=None):
    """Full-tile industrial hall; neighbouring halls of the same height join into one long building."""
    b = tile()
    _paving(b)
    b.bx(0.5, 15.5, 0.5, 15.5, 0.25, h, wall)
    b.bx(0.3, 15.7, 0.3, 15.7, h, h + 1.0, roof)
    b.bx(15.5, 15.65, 1.5, 14.5, h * 0.62, h * 0.74, "window")
    b.bx(3.5, 12.5, 15.5, 15.65, 0.25, min(h * 0.55, 12.0), door)
    if text:
        if text_bg:
            b.bx(1.0, 15.0, 15.5, 15.6, h - 7.5, h - 0.5, text_bg)
        sign(b, text, 8.0, h - 4.0, 15.7, text_mat)
    return b


def hangar(h, wall="white", roof="roofmetal", text=None, text_mat="navy"):
    """Hangar with a barrel roof and a big door on the +Y face."""
    b = tile()
    _paving(b)
    eave = h * 0.55
    b.bx(0.5, 15.5, 0.5, 15.5, 0.25, eave, wall)
    rise = h - eave
    b.sol(lambda X, Y, Z: (X > 0.3) & (X < 15.7) & (Z > eave) &
          (((X - 8.0) / 7.7) ** 2 + ((Z - eave) / rise) ** 2 <= 1.0), roof)
    b.bx(2.0, 14.0, 15.5, 15.65, 0.25, eave - 0.5, "grey")
    b.sol(lambda X, Y, Z: (Y > 15.5) & (Y < 15.65) & (X > 2.0) & (X < 14.0) & (Z < eave - 0.5) &
          (np.mod(X, 2.0) < 0.12), "steel")
    if text:
        sign(b, text, 8.0, eave + rise * 0.35, 15.7, text_mat)
    return b


def office(h, wall="stucco", glass="window", text=None, text_mat="navy"):
    b = tile()
    _paving(b)
    b.bx(2.5, 13.5, 2.5, 13.5, 0.25, h, wall)
    b.bx(2.3, 13.7, 2.3, 13.7, h, h + 0.8, "roof")
    for z in np.arange(2.5, h - 2.0, 4.0):
        b.bx(13.5, 13.62, 3.5, 12.5, z, z + 2.0, glass)
        b.bx(3.5, 12.5, 13.5, 13.62, z, z + 2.0, glass)
    if text:
        sign(b, text, 8.0, h - 1.8, 13.75, text_mat)
    return b


def tank(h, mat="white", r=6.0):
    b = tile()
    _paving(b)
    b.sol(lambda X, Y, Z: [(((X - 8) ** 2 + (Y - 8) ** 2 <= r * r) & (Z <= h), mat),
                           (((X - 8) ** 2 + (Y - 8) ** 2 <= r * r) & (Z <= h) & (np.mod(Z, 6.0) < 0.5), "steel"),
                           (((X - 8) ** 2 + (Y - 8) ** 2 <= (r * (1 - (Z - h) / 3.0)) ** 2) & (Z > h) & (Z <= h + 3.0), "roof")],
          None)
    b.bx(13.5, 16.0, 7.6, 8.4, 0.25, 1.4, "steel")         # pipe to the next tank
    return b


def silo(h, mat="white", around=None):
    b = around() if around else tile()
    if not around:
        _paving(b)
    b.sol(lambda X, Y, Z: (((X - 4) ** 2 + (Y - 4) ** 2 <= 9.0) & (Z <= h)) |
          (((X - 4) ** 2 + (Y - 4) ** 2 <= (3.0 * (1 - (Z - h) / 2.0)) ** 2) & (Z > h) & (Z <= h + 2.0)), mat)
    return b


def barn(h, wall="red", roof="roofgreen", grass=True):
    b = tile()
    _paving(b, "grass" if grass else "concrete")
    eave = h * 0.55
    b.bx(2.5, 13.5, 3.0, 13.0, 0.25, eave, wall)
    b.sol(lambda X, Y, Z: (X > 2.2) & (X < 13.8) & (Z > eave) & (Z <= eave + (5.4 - np.abs(Y - 8.0)) * (h - eave) / 5.4), roof)
    b.bx(6.0, 10.0, 13.0, 13.12, 0.25, eave * 0.85, "cream")
    return b


def farmhouse(h):
    return barn(h, wall="cream", roof="dark")


def crane(h):
    b = tile()
    _paving(b)
    for x in (2.0, 13.0):
        for y in (2.0, 13.0):
            b.bx(x, x + 1.0, y, y + 1.0, 0.25, h - 3.0, "orange")
    b.bx(1.5, 14.5, 1.5, 14.5, h - 3.0, h - 1.5, "orange")
    b.bx(6.0, 10.0, 6.0, 10.0, h - 1.5, h, "dark")
    b.bx(7.8, 8.2, 7.8, 8.2, h * 0.3, h - 3.0, "steel")
    return b


def slipway(h=12.0):
    """Ship hull on the slipway, bow to +X."""
    b = tile()
    _paving(b)
    half = lambda X: 4.2 * np.clip(1 - ((X - 8.0) / 8.0) ** 4, 0, 1)  # noqa: E731
    b.sol(lambda X, Y, Z: [((np.abs(Y - 8) <= half(X)) & (X > 0.5) & (X < 15.8) & (Z <= h * 0.55), "red"),
                           ((np.abs(Y - 8) <= half(X)) & (X > 0.5) & (X < 15.8) & (Z > h * 0.55) & (Z <= h * 0.75), "navy")], None)
    b.bx(2.0, 7.0, 5.5, 10.5, h * 0.75, h, "white")
    return b


def pier(deck="deckwood"):
    b = tile()
    b.bx(0.0, 16.0, 4.0, 12.0, 0.0, 1.2, deck)
    for x in (1.0, 7.5, 14.0):
        for y in (4.2, 11.2):
            b.bx(x, x + 0.6, y, y + 0.6, -1.0, 1.6, "timber")
    return b


def floatplane(base=None, mat="yellow"):
    """DHC-2 style floatplane, nose to +X, on a pier or on its own."""
    b = base() if base else tile()
    b.bx(4.0, 12.0, 7.3, 8.7, 3.0, 4.6, mat)                # fuselage
    b.bx(11.0, 12.6, 7.5, 8.5, 3.2, 4.4, "dark")             # cowling
    b.bx(7.0, 9.0, 1.5, 14.5, 4.6, 4.9, mat)                 # wing
    b.bx(4.0, 5.2, 7.7, 8.3, 4.6, 6.6, mat)                  # fin
    b.bx(4.0, 5.2, 5.5, 10.5, 4.4, 4.7, mat)                 # tailplane
    for y in (5.6, 9.6):
        b.bx(4.5, 11.5, y, y + 0.8, 1.2, 2.2, "white")       # floats
    return b


def dockhouse(h):
    b = pier()
    b.bx(3.0, 11.0, 4.5, 11.5, 1.2, h, "cedar")
    b.sol(lambda X, Y, Z: (X > 2.8) & (X < 11.2) & (Z > h) & (Z <= h + (3.8 - np.abs(Y - 8.0)) * 0.9), "roofgreen")
    b.bx(4.0, 6.0, 11.5, 11.62, 1.2, h - 1.5, "dark")
    return b


def supermarket(h, text="EDEKA"):
    b = tile()
    _paving(b, "asphalt")
    b.bx(1.0, 15.0, 1.5, 13.0, 0.25, h, "granite")           # warm grey cladding, as on real EDEKA markets
    b.bx(0.8, 15.2, 1.3, 13.2, h, h + 0.7, "asphalt")         # dark flat roof
    b.bx(1.0, 15.0, 13.0, 13.14, 0.25, 1.2, "navy")           # blue plinth under the glass
    b.bx(2.0, 14.0, 13.0, 13.12, 1.2, h * 0.55, "glass")
    b.bx(15.0, 15.14, 2.0, 12.5, h - 6.5, h - 0.2, "yellow")  # fascia wraps the side too
    b.bx(1.0, 15.0, 13.0, 13.15, h - 6.5, h - 0.2, "yellow")
    sign(b, text, 8.0, h - 3.3, 13.3, "navy")
    return b


def control(h):
    return control_tower()


def with_tower_mast(h):
    b = office(min(h, 14.0), "white", text=None)
    b.bx(7.6, 8.4, 7.6, 8.4, 14.8, h, "steel")
    return b


import landmarks  # noqa: E402  (imports FONT from this module)

# ---------------------------------------------------------------------------
# Industries: per building-rectangle models, cycled through the sheet's rectangles in reading order.
# A model takes the height budget (pixels above the tile's north corner) and returns a Building.
# ---------------------------------------------------------------------------

FLAT = [lambda h: yard()]

INDUSTRIES = {
    # real sites: one multi-tile model each (landmarks.py), with a layout generated to match
    "dreamlifter_delivery_airport": dict(landmark=landmarks.dreamlifter_airport,
                                         overlays=[(lambda: was_747(view=1), 54.0, 15.5, 0.25)]),
    "oil_terminal": dict(landmark=landmarks.oil_terminal),
    "aircraft_assembly_plant": dict(landmark=landmarks.renton_plant),
    "aircraft_qa_centre": dict(landmark=landmarks.everett_plant),
    "floatplane_factory": dict(landmark=landmarks.dhc_victoria),
    "customer_acceptance_centre": dict(landmark=landmarks.seattle_delivery_center),
    "aluminium_smelter": None,  # FIRS's own aluminium plant art
    "product_of_origin_dairy_farm": dict(models=[
        lambda h: barn(min(h, 18)), lambda h: silo(min(h, 17), around=lambda: barn(12, "red")),
        lambda h: farmhouse(min(h, 14)), lambda h: hall(min(h, 10), "white", "roofgreen"),
        lambda h: barn(min(h, 16), "red", "dark"), lambda h: silo(min(h, 17))]),
    "shipyard": dict(models=[
        lambda h: crane(min(h, 30)) if h > 20 else yard(),
        lambda h: hall(min(h, 26), "grey", "roofmetal") if h > 20 else yard("concrete"),
        lambda h: slipway(12.0) if h > 13 else yard(),
        lambda h: hall(min(h, 22), "ltblue", "roofmetal") if h > 20 else yard()]),
    "product_of_origin_sandwich_factory": dict(models=[
        lambda h: hall(min(h, 34), "white", "roofgreen", text="ORIGIN", text_mat="green"),
        lambda h: hall(min(h, 34), "white", "roofgreen"),
        lambda h: tank(min(h, 24), "white", r=5.0),
        lambda h: office(min(h, 26), "cream", text="EDEKA")]),
    "seaplane_base": dict(models=[
        lambda h: floatplane(pier) if h < 30 else dockhouse(12.0),
        lambda h: pier() if h < 30 else floatplane(lambda: dockhouse(9.0), "red"),
        lambda h: floatplane(pier, "red") if h < 30 else dockhouse(14.0)]),
    "edeka_grocery_store": dict(models=[lambda h: yard("asphalt") if h < 10 else supermarket(min(h, 14))]),
}


WAS_GRF = SRC.parent / "generated" / "was" / "WAS_World_Airliners_Set-0.1" / "was.grf"


def was_747(view):
    """The World Airliners Set's Boeing 747-400 (GPL v3; by PikkaBird and the WAS team), Boeing house livery, one of
    its eight directions. Using it makes FIRS PNW a personal set: FIRS itself is GPL v2 only, so the result must
    not be distributed."""
    import grf_v1
    if not WAS_GRF.exists():
        raise FileNotFoundError(f"extract WAS 0.1 from BaNaNaS (57a50001) to {WAS_GRF.parent}")
    entries = grf_v1.read(WAS_GRF)
    engine = grf_v1.engine_ids_named(entries, 0x03, "Boeing 747-400")[0]
    return grf_v1.vehicle_sprite_sets(entries, 0x03, engine)[1][view]


def add_overlay(sprites, overlay):
    """Paste a vehicle sprite standing at world (x, y, z) into the site: it joins the sprite of the last-drawn tile
    it covers, so the tiles drawn after it do not paint over it."""
    make, x, y, z = overlay
    sp = make()
    covered = [(tx, ty) for tx, ty, *_ in sprites if abs(tx * 16 + 8 - x) < 24 and abs(ty * 16 + 8 - y) < 24]
    ax, ay = max(covered, key=lambda t: (t[0] + t[1], t[0]))
    k = next(i for i, (tx, ty, *_) in enumerate(sprites) if (tx, ty) == (ax, ay))
    tx, ty, img, xo, yo = sprites[k]
    lx, ly = x - tx * 16, y - ty * 16
    px, py = int(round(2 * (ly - lx))) + sp.x_offs, int(round((lx + ly) - z)) + sp.y_offs   # sprite origin
    nx0, ny0 = min(xo, px), min(yo, py)
    nx1, ny1 = max(xo + img.shape[1], px + sp.w), max(yo + img.shape[0], py + sp.h)
    canvas = np.zeros((ny1 - ny0, nx1 - nx0), np.uint8)
    canvas[yo - ny0:yo - ny0 + img.shape[0], xo - nx0:xo - nx0 + img.shape[1]] = img
    region = canvas[py - ny0:py - ny0 + sp.h, px - nx0:px - nx0 + sp.w]
    # indices FIRS recolours or animates -> the nearest safe colour. WAS, like FIRS's sheets, uses the Windows
    # palette (32, 33 and 40 are greys there, browns in DOS), so read the colour from the sheet palette.
    sheet_pal = np.array(FIRS_PAL, np.float32).reshape(256, 3)
    safe = np.arange(256, dtype=np.uint8)
    for i in RESERVED:
        safe[i] = quantise(np.concatenate([sheet_pal[i], [1.0]])[None, None, :])[0, 0]
    pix = safe[sp.pixels]
    region[sp.pixels != 0] = pix[sp.pixels != 0]
    sprites[k] = (tx, ty, canvas, nx0, ny0)


def landmark_art(industry_id, spec):
    """Render a multi-tile site, pack its tile sprites into the industry's sheet and regenerate its tile, sprite
    and layout code (everything after the economy block) to match."""
    zoom, step = buildings.ZOOM, buildings.BASE_STEP
    buildings.ZOOM, buildings.BASE_STEP = 2, 0.2      # big sites: render at 2x, still finer than 1x pixels
    try:
        tiles = spec["landmark"]().render_object(views=(0,))[0]
    finally:
        buildings.ZOOM, buildings.BASE_STEP = zoom, step
    sprites = [(tx, ty, quantise(render.downsample(rgba, 2)), x0 // 2, y0 // 2) for tx, ty, rgba, x0, y0 in tiles]
    for overlay in spec.get("overlays", ()):
        add_overlay(sprites, overlay)
    rects, x = [], 10
    for tx, ty, img, xo, yo in sprites:
        rects.append((x, 10, img.shape[1], img.shape[0], xo, yo))
        x += img.shape[1] + 10
    sheet = np.zeros((max(r[3] for r in rects) + 20, x + 10), np.uint8)
    for rect, (_, _, img, xo, yo) in zip(rects, sprites):
        paint(sheet, rect, (img, xo, yo))
    png = GFX / "industries" / f"{industry_id}.png"
    save(sheet, png)
    if png.with_name(f"{industry_id}_snow.png").exists():
        save(sheet, png.with_name(f"{industry_id}_snow.png"))

    path = SRC / "industries" / f"{industry_id}.py"
    text = path.read_text(encoding="utf-8")
    code = [f'''industry.add_tile(
    id="{industry_id}_tile_1",
    location_checks=TileLocationChecks(disallow_industry_adjacent=True),
)

spriteset_ground = industry.add_spriteset(
    type="asphalt",
)
spriteset_ground_overlay = industry.add_spriteset(
    type="empty",
)
''']
    for (tx, ty, *_), rect in zip(sprites, rects):
        code.append(f'''industry.add_spritelayout(
    id="{industry_id}_spritelayout_{tx}_{ty}",
    tile="{industry_id}_tile_1",
    ground_sprite=spriteset_ground,
    ground_overlay=spriteset_ground_overlay,
    building_sprites=[industry.add_spriteset(sprites=[{rect}])],
    fences=[],
)
''')
    code.append(f'''industry.add_industry_layout(
    id="{industry_id}_industry_layout_1",
    layout=[
''' + "".join(f'        ({tx}, {ty}, "{industry_id}_spritelayout_{tx}_{ty}"),\n' for tx, ty, *_ in sprites) + "    ],\n)\n")
    path.write_text(text[:text.index("industry.add_tile(")] + "\n".join(code), encoding="utf-8")
    preview(industry_id, sprites)
    print(f"{industry_id}: {len(sprites)} tiles", flush=True)


def preview(industry_id, sprites):
    """The whole site assembled on grass, at 2x, in generated/previews/."""
    pal = np.array(FIRS_PAL, np.uint8).reshape(256, 3)
    out = Image.new("RGBA", (64 * 8 + 128, 32 * 8 + 160), (86, 132, 66, 255))
    cx, cy = out.width // 2, 120
    box = [out.width, out.height, 0, 0]
    for tx, ty, img, xo, yo in sorted(sprites, key=lambda s: s[0] + s[1]):
        rgba = np.dstack([pal[img], np.where(img == 0, 0, 255).astype(np.uint8)])
        px, py = cx + (ty - tx) * 32 + xo, cy + (tx + ty) * 16 + yo
        out.alpha_composite(Image.fromarray(rgba), (px, py))
        box = [min(box[0], px), min(box[1], py), max(box[2], px + img.shape[1]), max(box[3], py + img.shape[0])]
    out = out.crop((box[0] - 12, box[1] - 12, box[2] + 12, box[3] + 12))
    dest = SRC.parent / "generated" / "previews"
    dest.mkdir(parents=True, exist_ok=True)
    out.resize((out.width * 3, out.height * 3), Image.NEAREST).save(dest / f"{industry_id}.png")


def rectangles(industry_id):
    """Unique sprite rectangles (x, y, w, h, xoff, yoff) of an industry file, first offsets kept."""
    text = (SRC / "industries" / f"{industry_id}.py").read_text(encoding="utf-8")
    seen = {}
    for m in re.finditer(r"\((\d+), (\d+), (\d+), (\d+), (-?\d+), (-?\d+)\)", text):
        x, y, w, h, xo, yo = map(int, m.groups())
        seen.setdefault((x, y, w, h), (xo, yo))
    return sorted(((x, y, w, h) + seen[(x, y, w, h)] for x, y, w, h in seen), key=lambda r: (r[1], r[0]))


def grow(industry_id, height, yoff):
    """Make every rectangle `height` tall with the tile at the bottom; returns the new rectangles."""
    path = SRC / "industries" / f"{industry_id}.py"
    text = path.read_text(encoding="utf-8")
    old = rectangles(industry_id)
    new = []
    for x, y, w, h, xo, yo in old:
        r = (x, y, w, height, xo, yoff)
        text = text.replace(f"({x}, {y}, {w}, {h}, {xo}, {yo})", f"({x}, {y}, {w}, {height}, {xo}, {yoff})")
        new.append(r)
    path.write_text(text, encoding="utf-8")
    return new


def render_tile(b):
    """Model -> (palette indices at 1x, x offset, y offset) relative to the tile's north corner."""
    _, _, rgba, x0, y0 = b.render_object(views=(0,))[0][0]
    return quantise(render.downsample(rgba, render.ZOOM)), x0 // render.ZOOM, y0 // render.ZOOM


def paint(sheet, rect, sprite):
    x, y, w, h, xoff, yoff = rect
    img, x0, y0 = sprite
    sheet[y:y + h, x:x + w] = 0
    px, py = x + x0 - xoff, y + y0 - yoff
    ih, iw = img.shape
    sx0, sy0 = max(px, x), max(py, y)
    sx1, sy1 = min(px + iw, x + w), min(py + ih, y + h)
    if sx1 > sx0 and sy1 > sy0:
        part = img[sy0 - py:sy1 - py, sx0 - px:sx1 - px]
        dst = sheet[sy0:sy1, sx0:sx1]
        dst[part != 0] = part[part != 0]


def save(sheet, path):
    im = Image.fromarray(sheet, "P")
    im.putpalette(FIRS_PAL)
    im.save(path)


def industry_art(industry_id, spec):
    if spec is None:
        return
    if "landmark" in spec:
        return landmark_art(industry_id, spec)
    rects = rectangles(industry_id)
    if "grow" in spec:
        rects = grow(industry_id, *spec["grow"])
    png = GFX / "industries" / f"{industry_id}.png"
    sheet = np.array(Image.open(png))
    need_h = max(r[1] + r[3] for r in rects) + 10
    if sheet.shape[0] < need_h:
        sheet = np.vstack([sheet, np.zeros((need_h - sheet.shape[0], sheet.shape[1]), np.uint8)])
    cache = {}
    for k, rect in enumerate(rects):
        budget = -rect[5] - 2
        model = spec["models"][k % len(spec["models"])]
        key = (k % len(spec["models"]), budget)
        if key not in cache:
            cache[key] = render_tile(model(budget))
        paint(sheet, rect, cache[key])
    save(sheet, png)
    snow = png.with_name(f"{industry_id}_snow.png")
    if snow.exists():
        save(sheet, snow)
    print(f"{industry_id}: {len(rects)} rectangles, {len(cache)} sprites", flush=True)


# ---------------------------------------------------------------------------
# Cargo icons: 10x10, drawn as RGB pixel maps, quantised like the buildings
# ---------------------------------------------------------------------------

ICON_COLOURS = {".": None, "w": (238, 240, 242), "k": (40, 40, 44), "g": (150, 154, 160), "b": (40, 70, 150),
                "y": (240, 200, 40), "r": (190, 40, 30), "n": (30, 40, 90), "o": (220, 130, 30), "c": (240, 225, 170),
                "e": (90, 160, 60), "t": (200, 150, 90), "l": (120, 170, 220)}

ICONS = {
    "aircraft_parts": ["..........", "..gggggg..", ".gwwwwwwg.", ".gwggggwg.", ".gwg..gwg.",
                       ".gwggggwg.", ".gwwwwwwg.", "..gggggg..", "...g..g...", ".........."],
    "aircraft": ["....w.....", "....ww....", "....ww....", ".wwwwwwww.", "wwwwwwwwww",
                 "....ww....", "....ww....", "...wwww...", "....ww....", ".........."],
    "certified_aircraft": ["....w.....", "....ww....", "....ww...e", ".wwwwwwwe.", "wwwwwwwwe.",
                           "....wwe...", "...ewwe...", "....ee....", "....ww....", ".........."],
    "floatplanes": ["..........", "....y.....", "yyyyyyyyy.", "....yyyk..", "..yyyyyyk.",
                    "....g.g...", "..wwwwww..", "..........", "...wwwwww.", ".........."],
    "ships": ["..........", "....rr....", "....rr....", "..wwwwww..", "..wnnnnw..",
              "nnnnnnnnnn", ".nrrrrrrn.", "..rrrrrr..", "..........", ".........."],
    "jet_fuel": ["..........", "...gggg...", "..goooog..", "..gkkkkg..", "..goooog..",
                 "..goooog..", "..gkkkkg..", "..goooog..", "...gggg...", ".........."],
    "product_of_origin_dairy": ["....gg....", "...wwww...", "...wwww...", "..wwwwww..", "..weeeew..",
                                "..weeeew..", "..wwwwww..", "..wwwwww..", "..wwwwww..", ".........."],
    "edeka_gouda_sandwiches": ["..........", "..tttttt..", ".tccccccct", ".eeeeeeee.", ".yyyyyyyy.",
                               ".yyyyyyyy.", ".tccccccct", "..tttttt..", "..........", ".........."],
}


def icon_art():
    path = GFX / "cargoicons.png"
    sheet = np.array(Image.open(path))
    for cargo_id, rows in ICONS.items():
        m = re.search(r"icon_indices=\((\d+), (\d+)\)", (SRC / "cargos" / f"{cargo_id}.py").read_text(encoding="utf-8"))
        col, row = map(int, m.groups())
        rgba = np.zeros((10, 10, 4), np.float32)
        for y, line in enumerate(rows):
            for x, ch in enumerate(line):
                if ICON_COLOURS[ch]:
                    rgba[y, x] = ICON_COLOURS[ch] + (1.0,)
        sheet[10 + 20 * row:20 + 20 * row, 10 + 20 * col:20 + 20 * col] = quantise(rgba)
    save(sheet, path)
    print(f"cargo icons: {len(ICONS)}")


def check():
    """Every written sheet is 8-bit with the FIRS palette, and no new pixel uses a reserved index."""
    failures = []
    paths = [GFX / "industries" / f"{i}.png" for i, s in INDUSTRIES.items() if s] + [GFX / "cargoicons.png"]
    for path in paths:
        if not path.exists():
            failures.append(f"{path.name} missing")
            continue
        im = Image.open(path)
        if im.mode != "P" or im.getpalette()[:768] != FIRS_PAL:
            failures.append(f"{path.name} is not 8-bit with the FIRS palette")
    for industry_id, spec in INDUSTRIES.items():
        if not spec:
            continue
        sheet = np.array(Image.open(GFX / "industries" / f"{industry_id}.png"))
        for x, y, w, h, _, _ in rectangles(industry_id):
            used = set(np.unique(sheet[y:y + h, x:x + w])) - {0}
            if not used:
                failures.append(f"{industry_id} rectangle {(x, y)} is empty")
            if used & RESERVED:
                failures.append(f"{industry_id} rectangle {(x, y)} uses reserved indices {sorted(used & RESERVED)}")
    for f in failures:
        print("FAIL:", f)
    print(f"{len(failures)} failures")
    return 1 if failures else 0


def main():
    if "--check" not in sys.argv:
        only = [a for a in sys.argv[1:] if not a.startswith("--")]
        for industry_id, spec in INDUSTRIES.items():
            if not only or industry_id in only:
                industry_art(industry_id, spec)
        icon_art()
    return check()


if __name__ == "__main__":
    sys.exit(main())
