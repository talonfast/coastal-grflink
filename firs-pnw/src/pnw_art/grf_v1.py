"""
Minimal reader for container version 1 GRFs (the older format of sets like WAS), enough to pull out
8bpp sprites. Uses coastal-grflink's LZ77 and chunk decoders.

    entries = read(path)    # list of bytes (pseudo sprite) or Sprite
"""

import struct
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(r"G:\dev\coastal-grflink\common")))
from newgrf.decode import unchunk  # noqa: E402
from newgrf.lz77 import decompress as unlz77  # noqa: E402


@dataclass
class Sprite:
    w: int
    h: int
    x_offs: int
    y_offs: int
    pixels: np.ndarray        # H x W palette indices, 0 transparent


def lz77_until(data, pos, end):
    """TTD LZ77 (as newgrf.lz77.decompress) over the compressed bytes data[pos:end] -> (bytes, end)."""
    out = bytearray()
    while pos < end:
        code = data[pos]
        pos += 1
        if code < 0x80:
            n = code or 0x80
            out += data[pos:pos + n]
            pos += n
        else:
            c = code - 256
            off = ((c & 7) << 8) | data[pos]
            pos += 1
            n = -(c >> 3)
            start = len(out) - off
            out += out[start:start + n] if off >= n else (out[start:] * (n // off + 1))[:n]
    return bytes(out), pos


def read(path):
    data = open(path, "rb").read()
    pos, out = 0, []
    while pos + 2 <= len(data):
        (size,) = struct.unpack_from("<H", data, pos)
        pos += 2
        if size == 0:
            break
        info = data[pos]
        if info == 0xFF:
            out.append(bytes(data[pos + 1:pos + 1 + size]))
            pos += 1 + size
            continue
        h = data[pos + 1]
        w, xo, yo = struct.unpack_from("<Hhh", data, pos + 2)
        pos += 8
        # Version 1 pixel data is always LZ77-compressed. Info bit 1 set: `size` is the compressed size (header
        # included); clear: `size` is the decompressed size including the 8-byte header.
        if info & 0x02:
            raw, pos = lz77_until(data, pos, pos + size - 8)
        else:
            raw, pos = unlz77(data, pos, size - 8)
        if info & 0x08:                                   # chunked: 0x04 = one palette byte per pixel
            pixels = unchunk(bytes(raw), 0x04, w, h)[..., 0]
        else:
            pixels = np.frombuffer(bytes(raw), np.uint8)[:w * h].reshape(h, w)
        out.append(Sprite(w, h, xo, yo, pixels))
    return out


def ext_byte(d, i):
    """Extended byte: 0xFF means a word follows."""
    return (struct.unpack_from("<H", d, i + 1)[0], i + 3) if d[i] == 0xFF else (d[i], i + 1)


def vehicle_sprite_sets(entries, feature, engine_id):
    """Sprite sets (lists of Sprite) reachable from an engine's graphics chain, in the order the chain lists them.
    Follows action 3 -> basic, variational and random action 2 -> action 1 sets, using the IDs live at that point."""
    action1, nodes, i = [], {}, 0
    while i < len(entries):
        e = entries[i]
        if isinstance(e, bytes) and e and e[0] == 0x01 and e[1] == feature:
            nsets = e[2]
            nspr, _ = ext_byte(e, 3)
            sprites = [x for x in entries[i + 1:i + 1 + nsets * nspr]]
            action1 = [sprites[k * nspr:(k + 1) * nspr] for k in range(nsets)]
            i += 1 + nsets * nspr
            continue
        if isinstance(e, bytes) and e and e[0] == 0x02 and e[1] == feature:
            sid, typ = e[2], e[3]
            if typ in (0x80, 0x83, 0x84):                       # random
                n = e[6]
                refs = struct.unpack_from(f"<{n}H", e, 7)
                nodes[sid] = ("ref", [nodes.get(r) for r in refs if not r & 0x8000])
            elif typ < 0x80:                                     # basic: loaded / loading set numbers
                nl, nlo = e[3], e[4]
                sets = struct.unpack_from(f"<{nl + nlo}H", e, 5)
                nodes[sid] = ("sets", [action1[s] for s in sets if s < len(action1)])
            else:                                                # variational
                size = {0x81: 1, 0x82: 1, 0x85: 2, 0x86: 2, 0x89: 4, 0x8A: 4}[typ]
                j = 4
                while True:                                      # variable adjustments
                    var = e[j]; j += 1
                    if 0x60 <= var <= 0x7F:
                        j += 1
                    shift = e[j]; j += 1
                    j += size                                    # and-mask
                    if shift & 0x80:
                        j += 2 * size                            # add, divide/modulo
                    if not shift & 0x20:
                        break
                    j += 1                                       # next operator
                n = e[j]; j += 1
                refs = []
                for _ in range(n):
                    refs.append(struct.unpack_from("<H", e, j)[0]); j += 2 + 2 * size
                refs.append(struct.unpack_from("<H", e, j)[0])
                nodes[sid] = ("ref", [nodes.get(r) for r in refs if not r & 0x8000])
        if isinstance(e, bytes) and e and e[0] == 0x03 and e[1] == feature:
            nids = e[2] & 0x7F
            ids, j = [], 3
            for _ in range(nids):
                v, j = ext_byte(e, j)
                ids.append(v)
            if engine_id in ids and not e[2] & 0x80:
                ncid = e[j]; j += 1
                refs = [struct.unpack_from("<H", e, j + 3 * k + 1)[0] for k in range(ncid)]
                refs.append(struct.unpack_from("<H", e, j + 3 * ncid)[0])
                found, seen = [], set()

                def walk(node):
                    if node is None or id(node) in seen:
                        return
                    seen.add(id(node))
                    if node[0] == "sets":
                        found.extend(node[1])
                    else:
                        for child in node[1]:
                            walk(child)
                for r in reversed(refs):                          # default first
                    walk(nodes.get(r))
                return found
        i += 1
    return []


def engine_ids_named(entries, feature, text):
    """Engine IDs whose action 4 name (any language) contains text."""
    out = []
    for e in entries:
        if isinstance(e, bytes) and e and e[0] == 0x04 and e[1] == feature:
            lang, num = e[2], e[3]
            if lang & 0x80:
                first, j = struct.unpack_from("<H", e, 4)[0], 6
            else:
                first, j = e[4], 5
            names = e[j:].split(b"\x00")
            for k in range(num):
                if k < len(names) and text.encode() in names[k]:
                    out.append(first + k)
    return out
