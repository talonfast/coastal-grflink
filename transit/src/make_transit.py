"""Render the transit vehicles (src/vehicles.py) to gfx/<model>[_1x|_2x|_4x].png and gfx/transit.json.
src/build_transit.py makes pnw-transit.grf from them.

Usage: python src/make_transit.py [--preview out.png] [models...]
"""
import json
import os
import sys
import time

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "common"))
import fleet  # noqa: E402
from render import save_sheet_8, save_sheet_32, views_at  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GFX = os.path.join(ROOT, "gfx")


def preview(rows, path):
    W = max(sum(r[0].shape[1] for r in row) + 10 * len(row) for row in rows) + 20
    H = sum(max(r[0].shape[0] for r in row) + 12 for row in rows) + 20
    out = Image.new("RGBA", (W, H), (120, 150, 110, 255))
    y = 10
    for row in rows:
        x = 10
        for rgba, xo, yo in row:
            im = Image.fromarray(np.dstack([np.clip(rgba[..., :3], 0, 255),
                                            np.clip(rgba[..., 3] * 255, 0, 255)]).astype(np.uint8))
            out.alpha_composite(im, (x, y))
            x += im.width + 10
        y += max(r[0].shape[0] for r in row) + 12
    out.save(path)


def main():
    args = sys.argv[1:]
    pv = None
    if "--preview" in args:
        i = args.index("--preview")
        pv = args[i + 1]
        del args[i:i + 2]
    os.makedirs(GFX, exist_ok=True)
    mpath = os.path.join(GFX, "transit.json")
    meta = json.load(open(mpath)) if os.path.exists(mpath) else {}
    rows = []
    for name, model in fleet.models().items():
        if args and name not in args:
            continue
        t = time.time()
        views = model().render()
        base = os.path.join(GFX, name)
        z1, z2, z4 = (views_at(views, z) for z in (1, 2, 4))
        meta[name] = {"8bpp": save_sheet_8(z1, base + ".png"), "1x": save_sheet_32(z1, base + "_1x.png"),
                      "2x": save_sheet_32(z2, base + "_2x.png"), "4x": save_sheet_32(z4, base + "_4x.png")}
        rows.append(z2)
        print("rendered %-18s %.1fs" % (name, time.time() - t), flush=True)
    json.dump(meta, open(mpath, "w"), indent=1)
    if pv and rows:
        preview(rows, pv)


if __name__ == "__main__":
    main()
