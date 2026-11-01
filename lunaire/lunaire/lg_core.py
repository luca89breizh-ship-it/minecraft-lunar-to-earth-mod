"""Outils de base du générateur Lunaire : écriture PNG, NBT, JSON, dessin de sprites.

Aucune dépendance externe (bibliothèque standard uniquement), pour tourner tel quel sur GitHub Actions.
"""
import gzip
import json
import random
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "common" / "src" / "main" / "resources"
MOD = "lunaire"
ASSETS = RES / "assets" / MOD
DATA = RES / "data" / MOD
VANILLA_DATA = RES / "data" / "minecraft"


# ----------------------------------------------------------------------------- fichiers

def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ----------------------------------------------------------------------------- images

def clamp(v):
    return max(0, min(255, int(v)))


class Img:
    """Image RGBA simple. Les pixels sont (r, g, b, a)."""

    def __init__(self, w, h, fill=(0, 0, 0, 0)):
        self.w, self.h = w, h
        self.px = [fill] * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            if len(c) == 3:
                c = (c[0], c[1], c[2], 255)
            self.px[y * self.w + x] = tuple(clamp(v) for v in c)

    def get(self, x, y):
        return self.px[y * self.w + x]

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            for x in range(self.w):
                raw.extend(self.px[y * self.w + x])

        def chunk(tag, data):
            body = tag + data
            return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        png += chunk(b"IEND", b"")
        path.write_bytes(png)


def shade(c, d):
    return (clamp(c[0] + d), clamp(c[1] + d), clamp(c[2] + d), c[3] if len(c) > 3 else 255)


def noise_fill(img, x0, y0, w, h, base, var, seed):
    rng = random.Random(seed)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            d = rng.randint(-var, var)
            img.set(x, y, shade(base, d))


def sprite(rows, palette):
    """Dessine un sprite à partir de lignes ASCII. '.' = transparent."""
    h = len(rows)
    w = max(len(r) for r in rows)
    img = Img(w, h)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != "." and ch != " ":
                img.set(x, y, palette[ch])
    return img


# ----------------------------------------------------------------------------- NBT (structures)

TAG_END, TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE = 0, 1, 2, 3, 4, 5, 6
TAG_BYTE_ARRAY, TAG_STRING, TAG_LIST, TAG_COMPOUND, TAG_INT_ARRAY = 7, 8, 9, 10, 11


class NInt(int):
    pass


class NList(list):
    """Liste NBT avec type d'éléments explicite."""

    def __init__(self, tag_type, items=()):
        super().__init__(items)
        self.tag_type = tag_type


def _w_str(s):
    b = s.encode("utf-8")
    return struct.pack(">H", len(b)) + b


def _w_payload(v):
    if isinstance(v, NInt) or (isinstance(v, int) and not isinstance(v, bool)):
        return TAG_INT, struct.pack(">i", v)
    if isinstance(v, str):
        return TAG_STRING, _w_str(v)
    if isinstance(v, dict):
        out = b""
        for k, val in v.items():
            t, p = _w_payload(val)
            out += struct.pack(">B", t) + _w_str(k) + p
        return TAG_COMPOUND, out + b"\x00"
    if isinstance(v, NList):
        out = struct.pack(">Bi", v.tag_type, len(v))
        for item in v:
            out += _w_payload(item)[1]
        return TAG_LIST, out
    raise TypeError(type(v))


def write_nbt_gz(path: Path, root: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    t, p = _w_payload(root)
    data = struct.pack(">B", t) + _w_str("") + p
    path.write_bytes(gzip.compress(data, 9, mtime=0))


class Template:
    """Structure Minecraft (.nbt) construite bloc par bloc."""

    DATA_VERSION = 5023  # Minecraft 26.3

    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.cells = {}  # (x,y,z) -> (name, props tuple, nbt)

    def set(self, x, y, z, name, props=None, nbt=None):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]:
            self.cells[(x, y, z)] = (name, tuple(sorted((props or {}).items())), nbt)

    def fill(self, x1, y1, z1, x2, y2, z2, name, props=None):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, name, props)

    def chest(self, x, y, z, facing, loot):
        self.set(x, y, z, "minecraft:chest",
                 {"facing": facing, "type": "single", "waterlogged": "false"},
                 {"id": "minecraft:chest", "LootTable": loot})

    def write(self, path: Path):
        palette_index = {}
        palette = NList(TAG_COMPOUND)
        blocks = NList(TAG_COMPOUND)
        for (x, y, z), (name, props, nbt) in sorted(self.cells.items(), key=lambda kv: (kv[0][1], kv[0][0], kv[0][2])):
            key = (name, props)
            if key not in palette_index:
                palette_index[key] = len(palette)
                entry = {"Name": name}
                if props:
                    entry["Properties"] = {k: v for k, v in props}
                palette.append(entry)
            block = {"pos": NList(TAG_INT, [x, y, z]), "state": palette_index[key]}
            if nbt:
                block["nbt"] = nbt
            blocks.append(block)
        root = {
            "DataVersion": self.DATA_VERSION,
            "size": NList(TAG_INT, list(self.size)),
            "palette": palette,
            "blocks": blocks,
            "entities": NList(TAG_END, []),
        }
        write_nbt_gz(path, root)
