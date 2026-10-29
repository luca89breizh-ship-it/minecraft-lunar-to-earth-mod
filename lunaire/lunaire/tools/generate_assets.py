#!/usr/bin/env python3
"""Génère les ressources (assets + data) et les textures 16x16 provisoires de Lunaire.

Usage : python3 tools/generate_assets.py   (depuis la racine du projet)
Les textures sont des placeholders procéduraux : remplacez-les par de vraies textures.
"""
import json
import random
from pathlib import Path

from PIL import Image

MOD = "lunaire"
ROOT = Path(__file__).resolve().parent.parent / "common" / "src" / "main" / "resources"

BLOCKS = {
    "regolith": {"fr": "Régolithe", "en": "Regolith", "base": (150, 146, 140), "var": 18, "tool": "shovel"},
    "lunar_rock": {"fr": "Roche lunaire", "en": "Lunar Rock", "base": (96, 98, 104), "var": 16, "tool": "pickaxe"},
    "lunar_ice": {"fr": "Glace lunaire", "en": "Lunar Ice", "base": (170, 205, 235), "var": 14, "tool": "pickaxe"},
}

ITEMS = {
    "damaged_air_purifier": {"fr": "Épurateur d'air portatif endommagé", "en": "Damaged Portable Air Purifier", "base": (120, 130, 140)},
    "meteorite_shard": {"fr": "Éclat de météorite", "en": "Meteorite Shard", "base": (70, 60, 80)},
    "circuit_board": {"fr": "Circuit imprimé", "en": "Circuit Board", "base": (40, 140, 80)},
    "iron_scrap": {"fr": "Morceau de fer", "en": "Iron Scrap", "base": (190, 190, 195)},
}


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def clamp(v):
    return max(0, min(255, v))


def block_texture(name, base, var):
    rng = random.Random(name)
    img = Image.new("RGBA", (16, 16))
    for x in range(16):
        for y in range(16):
            d = rng.randint(-var, var)
            img.putpixel((x, y), (clamp(base[0] + d), clamp(base[1] + d), clamp(base[2] + d), 255))
    path = ROOT / "assets" / MOD / "textures" / "block" / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def item_texture(name, base):
    rng = random.Random(name)
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    cx, cy = 8, 8
    for x in range(16):
        for y in range(16):
            if (x - cx) ** 2 + (y - cy) ** 2 <= 30:
                d = rng.randint(-20, 20)
                edge = 40 if (x - cx) ** 2 + (y - cy) ** 2 > 22 else 0
                img.putpixel((x, y), (clamp(base[0] + d - edge), clamp(base[1] + d - edge), clamp(base[2] + d - edge), 255))
    path = ROOT / "assets" / MOD / "textures" / "item" / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def main():
    assets = ROOT / "assets" / MOD
    data = ROOT / "data" / MOD

    lang_fr, lang_en = {}, {}
    mineable = {"pickaxe": [], "shovel": []}

    for name, b in BLOCKS.items():
        block_texture(name, b["base"], b["var"])
        write_json(assets / "blockstates" / f"{name}.json", {"variants": {"": {"model": f"{MOD}:block/{name}"}}})
        write_json(assets / "models" / "block" / f"{name}.json",
                   {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/{name}"}})
        write_json(assets / "items" / f"{name}.json",
                   {"model": {"type": "minecraft:model", "model": f"{MOD}:block/{name}"}})
        write_json(data / "loot_table" / "blocks" / f"{name}.json", {
            "type": "minecraft:block",
            "pools": [{
                "rolls": 1.0,
                "bonus_rolls": 0.0,
                "entries": [{"type": "minecraft:item", "name": f"{MOD}:{name}"}],
                "conditions": [{"condition": "minecraft:survives_explosion"}],
            }],
            "random_sequence": f"{MOD}:blocks/{name}",
        })
        mineable[b["tool"]].append(f"{MOD}:{name}")
        lang_fr[f"block.{MOD}.{name}"] = b["fr"]
        lang_en[f"block.{MOD}.{name}"] = b["en"]

    for name, i in ITEMS.items():
        item_texture(name, i["base"])
        write_json(assets / "models" / "item" / f"{name}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{name}"}})
        write_json(assets / "items" / f"{name}.json",
                   {"model": {"type": "minecraft:model", "model": f"{MOD}:item/{name}"}})
        lang_fr[f"item.{MOD}.{name}"] = i["fr"]
        lang_en[f"item.{MOD}.{name}"] = i["en"]

    for tool, values in mineable.items():
        write_json(ROOT / "data" / "minecraft" / "tags" / "block" / "mineable" / f"{tool}.json", {"values": values})

    write_json(assets / "lang" / "fr_fr.json", lang_fr)
    write_json(assets / "lang" / "en_us.json", lang_en)
    print("Ressources générées dans", ROOT)


if __name__ == "__main__":
    main()
