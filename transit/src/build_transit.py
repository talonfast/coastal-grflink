"""Build pnw-transit.grf from fleet.ROAD / fleet.RAIL and the rendered gfx/ (src/make_transit.py).

Usage: python src/build_transit.py [output.grf]
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "common"))
import fleet  # noqa: E402
from newgrf import GRF, cli  # noqa: E402
from newgrf import actions as A  # noqa: E402
from newgrf.sprites import sheet_sprites  # noqa: E402

VERSION = 1
NAME = "PNW Transit {SILVER}v%d" % VERSION
DESCRIPTION = ("Buses, streetcars and trains of the Pacific Northwest: BC Transit's Enviro500 double-decker, "
               "TransLink's articulated buses and the SkyTrain Mark V, the Seattle and Portland streetcars, "
               "Seattle's Link light rail (as trams) and the Amtrak Cascades Airo.{}{}Includes 32bpp sprites up "
               "to 4x zoom. Works with OpenTTD 13+ and JGR's Patch Pack.")

CARGO = ["PASS"]
CC_PASSENGERS = 0x01
CBM_ARTICULATED = 0x10
CLIMATES_ALL = 0x0F                       # temperate, arctic, tropical, toyland
RUNNING_COST_DIESEL, RUNNING_COST_ELECTRIC = 0x4C36, 0x4C3C
TRACTION = {"diesel": 0x08, "electric": 0x28}
VE_DIESEL, VE_DISABLED = 0x28, 0x40       # visual effect: type << 4 | position (8 = middle)
RV_TRAM, TRAIN_MU = 0x01, 0x04            # misc flags
VAR_CALLBACK, VAR_CALLBACK_PARAM = 0x0C, 0x10


def description(e):
    return "%s{}{BLACK}Real-world: {GOLD}%d{BLACK} km/h" % (e["desc"], e["kmh"])


def common_props(e, buyable):
    """Properties 02-06 are the same for every vehicle feature."""
    if not buyable:
        return [(0x06, A.b(0))]                             # articulated part: never in the build list
    return [(0x06, A.b(CLIMATES_ALL)), (0x04, A.b(e["model_life"])), (0x03, A.b(e["life"])), (0x02, A.b(7))]


def road_props(e, ids):
    buyable = "name" in e
    props = common_props(e, buyable) + [(0x0E, A.b(0xFF))]  # new graphics
    if buyable:
        props += [(0x1F, A.d(A.date(e["year"]))), (0x08, A.b(A.roadveh_speed_kmh(e["kmh"]))),
                  (0x09, A.b(e["run"])), (0x11, A.b(e["cost"])), (0x13, A.b(e["hp"] // 10))]
    props += [
        (0x0F, A.b(e["cap"])), (0x10, A.b(0)), (0x16, A.d(0)),
        (0x1D, A.w(CC_PASSENGERS)), (0x1E, A.w(0)),
        (0x14, A.b(round(e["t"] * 4))),
        (0x1C, A.b(RV_TRAM if e.get("tram") else 0)),
    ]
    if e.get("length", 8) != 8:
        props.append((0x23, A.b(8 - e["length"])))
    if e.get("parts"):
        props.append((0x17, A.b(CBM_ARTICULATED)))
    if e.get("variant_of"):
        props.append((0x26, A.w(ids[e["variant_of"]])))
    return props


def rail_props(e, ids):
    buyable = "name" in e
    props = common_props(e, buyable) + [
        (0x12, A.b(0xFD)),                                  # new graphics
        (0x05, A.b(0)),                                     # rail; electric traction makes it electrified rail
    ]
    if "traction" in e:
        props.append((0x19, A.b(TRACTION[e["traction"]])))
    if buyable:
        props += [(0x2A, A.d(A.date(e["year"]))), (0x09, A.w(A.train_speed_kmh(e["kmh"]))),
                  (0x17, A.b(e["cost"]))]
    power = e.get("hp", 0) if buyable else 0
    props += [(0x0B, A.w(power)), (0x16, A.b(e["t"] & 0xFF)), (0x24, A.b(e["t"] >> 8))]
    if power:
        props += [(0x0D, A.b(e["run"])),
                  (0x0E, A.d(RUNNING_COST_ELECTRIC if e["traction"] == "electric" else RUNNING_COST_DIESEL))]
    else:
        props.append((0x0D, A.b(0)))
    props += [
        (0x14, A.b(e["cap"])), (0x15, A.b(0)), (0x1D, A.d(0)),
        (0x28, A.w(CC_PASSENGERS if e["cap"] else 0)), (0x29, A.w(0)),
        (0x22, A.b(VE_DIESEL if e.get("traction") == "diesel" and power else VE_DISABLED)),
    ]
    if e.get("mu"):
        props.append((0x27, A.b(TRAIN_MU)))
    if e.get("parts"):
        props.append((0x1E, A.b(CBM_ARTICULATED)))
    if e.get("variant_of"):
        props.append((0x2F, A.w(ids[e["variant_of"]])))
    return props


def add_engine(grf, feature, num, e, ids, meta, name):
    grf.add(A.action0(feature, num, (road_props if feature == A.ROADVEHS else rail_props)(e, ids)))
    grf.add(A.action4_names(feature, num, [name]))
    sprites = sheet_sprites(os.path.join(ROOT, "gfx", e["gfx"]), meta[e["gfx"]])
    grf.add(A.action1(feature, 1, len(sprites)))
    for spr in sprites:
        grf.sprite(spr)

    g_gfx, g = 0, 1
    grf.add(A.action2_vehicle(feature, g_gfx, [0], [0]))
    callbacks = []
    if e.get("parts"):
        # Articulated parts by position (1, 2, ...): local engine ID, bit 14 = drawn reversed.
        parts = [(A.cb(ids[p] | (0x4000 if mirrored else 0)), i, i) for i, (p, mirrored) in enumerate(e["parts"], 1)]
        grf.add(A.varaction2(feature, g, [A.Adjust(VAR_CALLBACK_PARAM, mask=0xFF)], parts, A.cb(0x7FFF)))
        callbacks.append((g, A.CB_ARTICULATED, A.CB_ARTICULATED))
        g += 1
    g_world = g_gfx
    if callbacks:                                       # with no ranges, the callback ID would be the result
        g_world = g
        grf.add(A.varaction2(feature, g_world, [A.Adjust(VAR_CALLBACK, mask=0xFFFF)], callbacks, g_gfx))
    if "name" not in e:
        grf.add(A.action3(feature, [num], default=g_world))
        return
    text = grf.string(description(e))
    g_purchase = g + 1
    grf.add(A.varaction2(feature, g_purchase, [A.Adjust(VAR_CALLBACK, mask=0xFFFF)],
                         callbacks + [(A.cb(text - 0xD000), A.CB_ADDITIONAL_TEXT, A.CB_ADDITIONAL_TEXT)], g_gfx))
    grf.add(A.action3(feature, [num], default=g_world, cargo=[(0xFF, g_purchase)]))


def build(path, jobs=None):
    grf = GRF("TFBR", NAME, DESCRIPTION, VERSION, 1)
    with open(os.path.join(ROOT, "gfx", "transit.json")) as f:
        meta = json.load(f)
    for e in fleet.ROAD + fleet.RAIL:                   # descriptions first, in fleet order
        if "name" in e:
            grf.string(description(e))
    grf.add(A.cargo_table(CARGO))
    for feature, units, base in ((A.ROADVEHS, fleet.ROAD, fleet.RV_BASE), (A.TRAINS, fleet.RAIL, fleet.TRAIN_BASE)):
        ids = {e["id"]: base + n for n, e in enumerate(units)}   # list position = engine ID: append only!
        name = None
        for e in units:
            name = e.get("name", name)                  # parts carry their front's name
            add_engine(grf, feature, ids[e["id"]], e, ids, meta, name)
    grf.write(path, jobs)


if __name__ == "__main__":
    build(*cli.output(os.path.join(ROOT, "pnw-transit.grf")))
