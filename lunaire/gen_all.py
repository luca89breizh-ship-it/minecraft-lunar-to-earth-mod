#!/usr/bin/env python3
"""Génère toutes les ressources de Lunaire (données, modèles, textures, structures).

Lancé automatiquement par GitHub Actions avant la compilation :  python3 tools/gen_all.py
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lg_core import *  # noqa
import lg_tex

TOOLS = Path(__file__).resolve().parent
M = "lunaire:"

# ============================================================================ CONTENU
# (nom, type de modèle, outil, solidité, besoin outil, drop)
# modèle: all | column (end+side) | lit (column avec variante allumée) | radiator
BLOCKS = [
    ("regolith", "all", "shovel", 0.6, None, None),
    ("hydrated_regolith", "all", "shovel", 0.6, None, None),
    ("lunar_rock", "all", "pickaxe", 2.0, "wood", None),
    ("lunar_ice", "all", "pickaxe", 0.8, "wood", None),
    ("lunar_iron_ore", "all", "pickaxe", 3.0, "stone", "minecraft:iron_ingot"),
    ("titanium_ore", "all", "pickaxe", 4.0, "iron", M + "titanium_ingot"),
    ("aluminum_ore", "all", "pickaxe", 3.0, "stone", M + "aluminum_ingot"),
    ("lab_plating", "all", "pickaxe", 3.0, "wood", None),
    ("ancient_stone", "all", "pickaxe", 3.0, "wood", None),
    ("launch_platform", "all", "pickaxe", 5.0, "wood", None),
    ("solar_panel", "column", "pickaxe", 2.0, "wood", None),
    ("atmosphere_sealer", "column", "pickaxe", 3.0, "wood", None),
    ("electrolyzer", "column", "pickaxe", 3.0, "wood", None),
    ("hydrogen_generator", "lit", "pickaxe", 3.0, "wood", None),
    ("radiator", "radiator", "pickaxe", 3.0, "wood", None),
]

ITEMS = ["titanium_ingot", "aluminum_ingot", "iron_scrap", "meteorite_shard", "circuit_board",
         "oxygen_bottle", "oxygen_bottle_full", "hydrogen_cell", "damaged_air_purifier", "air_purifier",
         "rocket_blueprint", "reentry_module"]
TOOLS_ITEMS = ["lunar_rock_pickaxe", "lunar_rock_axe", "lunar_rock_shovel", "lunar_rock_sword"]
ARMOR = ["spacesuit_helmet", "spacesuit_chestplate", "spacesuit_leggings", "spacesuit_boots"]

LANG_FR = {
    "regolith": "Régolithe", "hydrated_regolith": "Régolithe hydratée", "lunar_rock": "Roche lunaire",
    "lunar_ice": "Glace lunaire", "lunar_iron_ore": "Minerai de fer lunaire", "titanium_ore": "Minerai de titane",
    "aluminum_ore": "Minerai d'aluminium", "lab_plating": "Plaque de laboratoire",
    "ancient_stone": "Pierre ancienne", "launch_platform": "Plateforme de lancement",
    "solar_panel": "Panneau solaire", "atmosphere_sealer": "Scelleur d'atmosphère",
    "electrolyzer": "Électrolyseur", "hydrogen_generator": "Générateur à hydrogène", "radiator": "Radiateur",
    "titanium_ingot": "Lingot de titane", "aluminum_ingot": "Lingot d'aluminium", "iron_scrap": "Morceau de fer",
    "meteorite_shard": "Éclat de météorite", "circuit_board": "Circuit imprimé",
    "oxygen_bottle": "Bouteille d'O₂ vide", "oxygen_bottle_full": "Bouteille d'O₂ pleine",
    "hydrogen_cell": "Cellule d'hydrogène", "damaged_air_purifier": "Épurateur d'air portatif endommagé",
    "air_purifier": "Épurateur d'air portatif", "rocket_blueprint": "Schéma de fusée (Tier 3)",
    "reentry_module": "Module de rentrée atmosphérique",
    "lunar_rock_pickaxe": "Pioche en roche lunaire", "lunar_rock_axe": "Hache en roche lunaire",
    "lunar_rock_shovel": "Pelle en roche lunaire", "lunar_rock_sword": "Épée en roche lunaire",
    "spacesuit_helmet": "Casque de combinaison renforcée", "spacesuit_chestplate": "Plastron de combinaison renforcée",
    "spacesuit_leggings": "Jambières de combinaison renforcée", "spacesuit_boots": "Bottes de combinaison renforcée",
}
LANG_EN = {
    "regolith": "Regolith", "hydrated_regolith": "Hydrated Regolith", "lunar_rock": "Lunar Rock",
    "lunar_ice": "Lunar Ice", "lunar_iron_ore": "Lunar Iron Ore", "titanium_ore": "Titanium Ore",
    "aluminum_ore": "Aluminum Ore", "lab_plating": "Lab Plating", "ancient_stone": "Ancient Stone",
    "launch_platform": "Launch Platform", "solar_panel": "Solar Panel", "atmosphere_sealer": "Atmosphere Sealer",
    "electrolyzer": "Electrolyzer", "hydrogen_generator": "Hydrogen Generator", "radiator": "Radiator",
    "titanium_ingot": "Titanium Ingot", "aluminum_ingot": "Aluminum Ingot", "iron_scrap": "Iron Scrap",
    "meteorite_shard": "Meteorite Shard", "circuit_board": "Circuit Board", "oxygen_bottle": "Empty O2 Bottle",
    "oxygen_bottle_full": "Full O2 Bottle", "hydrogen_cell": "Hydrogen Cell",
    "damaged_air_purifier": "Damaged Portable Air Purifier", "air_purifier": "Portable Air Purifier",
    "rocket_blueprint": "Rocket Blueprint (Tier 3)", "reentry_module": "Atmospheric Reentry Module",
    "lunar_rock_pickaxe": "Lunar Rock Pickaxe", "lunar_rock_axe": "Lunar Rock Axe",
    "lunar_rock_shovel": "Lunar Rock Shovel", "lunar_rock_sword": "Lunar Rock Sword",
    "spacesuit_helmet": "Reinforced Spacesuit Helmet", "spacesuit_chestplate": "Reinforced Spacesuit Chestplate",
    "spacesuit_leggings": "Reinforced Spacesuit Leggings", "spacesuit_boots": "Reinforced Spacesuit Boots",
}
EXTRA_FR = {
    "itemGroup.lunaire": "Lunaire", "entity.lunaire.selenite": "Sélénite de l'Ombre",
    "entity.lunaire.dust_golem": "Golem de poussière",
    "lunaire.hud.oxygen": "O₂", "lunaire.intro1": "Vous vous réveillez dans les débris de votre capsule de secours...",
    "lunaire.intro2": "Il n'y a pas d'air ici. Fouillez le coffre : un épurateur, endommagé, mais réparable.",
    "lunaire.suffocate": "Plus d'oxygène !", "lunaire.no_blueprint": "Il vous faut le schéma de fusée (Tier 3) et un module de rentrée.",
    "lunaire.powered": "Machine alimentée", "lunaire.no_power": "Pas d'énergie (panneau solaire de jour ou générateur à hydrogène allumé à proximité).",
    "lunaire.no_ice": "Il faut de la glace lunaire.", "lunaire.sealed": "Atmosphère scellée : %s blocs pressurisés.",
    "lunaire.leak": "Fuite : la pièce n'est pas étanche.", "lunaire.hydrated": "Régolithe hydratée !",
    "lunaire.launch": "Lancement dans 10 secondes !", "lunaire.fuelled": "Cellule insérée.",
}
EXTRA_EN = {
    "itemGroup.lunaire": "Lunaire", "entity.lunaire.selenite": "Shadow Selenite",
    "entity.lunaire.dust_golem": "Dust Golem",
    "lunaire.hud.oxygen": "O2", "lunaire.intro1": "You wake up in the debris of your rescue capsule...",
    "lunaire.intro2": "There is no air here. Check the chest: a damaged but repairable purifier.",
    "lunaire.suffocate": "Out of oxygen!", "lunaire.no_blueprint": "You need the Tier 3 rocket blueprint and a reentry module.",
    "lunaire.powered": "Machine powered", "lunaire.no_power": "No power (solar panel in daylight or lit hydrogen generator nearby).",
    "lunaire.no_ice": "You need lunar ice.", "lunaire.sealed": "Atmosphere sealed: %s blocks pressurized.",
    "lunaire.leak": "Leak: the room is not airtight.", "lunaire.hydrated": "Hydrated regolith!",
    "lunaire.launch": "Launch in 10 seconds!", "lunaire.fuelled": "Cell inserted.",
}


# ============================================================================ ASSETS

def gen_assets():
    lg_tex.generate_blocks()
    lg_tex.item_sprites()
    lg_tex.armor_textures()
    lg_tex.creature_textures()

    for name, kind, tool, hard, need, drop in BLOCKS:
        bs = ASSETS / "blockstates" / f"{name}.json"
        if kind == "lit":
            write_json(bs, {"variants": {"lit=false": {"model": f"{M}block/{name}"},
                                         "lit=true": {"model": f"{M}block/{name}_lit"}}})
            for suffix in ("", "_lit"):
                write_json(ASSETS / "models" / "block" / f"{name}{suffix}.json", {
                    "parent": "minecraft:block/cube_column",
                    "textures": {"end": f"{M}block/{name}_top", "side": f"{M}block/{name}_side{suffix}"}})
        elif kind == "radiator":
            write_json(bs, {"variants": {"lit=false": {"model": f"{M}block/{name}"},
                                         "lit=true": {"model": f"{M}block/{name}_lit"}}})
            for suffix in ("", "_lit"):
                write_json(ASSETS / "models" / "block" / f"{name}{suffix}.json", {
                    "parent": "minecraft:block/cube_all", "textures": {"all": f"{M}block/{name}{suffix}"}})
        elif kind == "column":
            write_json(bs, {"variants": {"": {"model": f"{M}block/{name}"}}})
            write_json(ASSETS / "models" / "block" / f"{name}.json", {
                "parent": "minecraft:block/cube_column",
                "textures": {"end": f"{M}block/{name}_top", "side": f"{M}block/{name}_side"}})
        else:
            write_json(bs, {"variants": {"": {"model": f"{M}block/{name}"}}})
            write_json(ASSETS / "models" / "block" / f"{name}.json", {
                "parent": "minecraft:block/cube_all", "textures": {"all": f"{M}block/{name}"}})
        write_json(ASSETS / "items" / f"{name}.json",
                   {"model": {"type": "minecraft:model", "model": f"{M}block/{name}"}})

    for name in ITEMS + TOOLS_ITEMS + ARMOR:
        parent = "minecraft:item/handheld" if name in TOOLS_ITEMS else "minecraft:item/generated"
        write_json(ASSETS / "models" / "item" / f"{name}.json",
                   {"parent": parent, "textures": {"layer0": f"{M}item/{name}"}})
        write_json(ASSETS / "items" / f"{name}.json",
                   {"model": {"type": "minecraft:model", "model": f"{M}item/{name}"}})

    write_json(ASSETS / "equipment" / "spacesuit.json", {
        "layers": {"humanoid": [{"texture": f"{M}spacesuit"}],
                   "humanoid_leggings": [{"texture": f"{M}spacesuit"}]}})

    lang_fr = {f"block.lunaire.{n}": LANG_FR[n] for n, *_ in BLOCKS}
    lang_fr.update({f"item.lunaire.{n}": LANG_FR[n] for n in ITEMS + TOOLS_ITEMS + ARMOR})
    lang_fr.update(EXTRA_FR)
    lang_en = {f"block.lunaire.{n}": LANG_EN[n] for n, *_ in BLOCKS}
    lang_en.update({f"item.lunaire.{n}": LANG_EN[n] for n in ITEMS + TOOLS_ITEMS + ARMOR})
    lang_en.update(EXTRA_EN)
    write_json(ASSETS / "lang" / "fr_fr.json", lang_fr)
    write_json(ASSETS / "lang" / "en_us.json", lang_en)


# ============================================================================ DONNÉES : LOOT, TAGS, RECIPES

def count(lo, hi):
    return {"type": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}


def entry(item, lo=None, hi=None, weight=None):
    e = {"type": "minecraft:item", "name": item}
    if lo is not None:
        e["modifier"] = count(lo, hi)
    if weight:
        e["weight"] = weight
    return e


def gen_loot():
    for name, kind, tool, hard, need, drop in BLOCKS:
        pool = {"rolls": 1, "condition": {"type": "minecraft:survives_explosion"},
                "entries": [{"type": "minecraft:item", "name": drop or f"{M}{name}"}]}
        write_json(DATA / "loot_table" / "blocks" / f"{name}.json", {
            "type": "minecraft:block", "pools": [pool], "random_sequence": f"{M}blocks/{name}"})

    write_json(DATA / "loot_table" / "chests" / "capsule.json", {
        "type": "minecraft:chest", "random_sequence": f"{M}chests/capsule", "pools": [
            {"rolls": 1, "entries": [entry(M + "damaged_air_purifier")]},
            {"rolls": 1, "entries": [entry(M + "oxygen_bottle_full", 2, 3)]},
            {"rolls": 1, "entries": [entry(M + "iron_scrap", 3, 5)]},
            {"rolls": 1, "entries": [entry(M + "circuit_board", 1, 2)]},
            {"rolls": 1, "entries": [entry(M + "oxygen_bottle", 1, 2)]}]})
    write_json(DATA / "loot_table" / "chests" / "lab.json", {
        "type": "minecraft:chest", "random_sequence": f"{M}chests/lab", "pools": [
            {"rolls": {"type": "minecraft:uniform", "min": 3, "max": 5}, "entries": [
                entry(M + "circuit_board", 1, 3, 30), entry(M + "iron_scrap", 2, 6, 30),
                entry("minecraft:iron_ingot", 1, 3, 12), entry(M + "oxygen_bottle_full", 1, 2, 15),
                entry(M + "hydrogen_cell", 1, 2, 12), entry(M + "aluminum_ingot", 1, 2, 8),
                entry(M + "titanium_ingot", 1, 1, 4), entry(M + "oxygen_bottle", 1, 2, 10)]}]})
    write_json(DATA / "loot_table" / "chests" / "temple.json", {
        "type": "minecraft:chest", "random_sequence": f"{M}chests/temple", "pools": [
            {"rolls": 1, "entries": [entry(M + "rocket_blueprint")]},
            {"rolls": {"type": "minecraft:uniform", "min": 2, "max": 4}, "entries": [
                entry(M + "titanium_ingot", 1, 3, 20), entry(M + "aluminum_ingot", 2, 4, 20),
                entry(M + "meteorite_shard", 1, 3, 15), entry(M + "circuit_board", 1, 2, 15),
                entry(M + "hydrogen_cell", 1, 2, 10)]}]})
    write_json(DATA / "loot_table" / "entities" / "dust_golem.json", {
        "type": "minecraft:entity", "random_sequence": f"{M}entities/dust_golem", "pools": [
            {"rolls": 1, "entries": [entry(M + "meteorite_shard", 1, 3)]},
            {"rolls": 1, "entries": [entry(M + "iron_scrap", 0, 2)]}]})
    write_json(DATA / "loot_table" / "entities" / "selenite.json", {
        "type": "minecraft:entity", "random_sequence": f"{M}entities/selenite", "pools": [
            {"rolls": 1, "entries": [entry(M + "oxygen_bottle", 0, 1)]}]})


def tag(path, values):
    write_json(path, {"values": values})


def gen_tags():
    T = VANILLA_DATA / "tags" / "block"
    by = {"pickaxe": [], "shovel": []}
    needs = {"stone": [], "iron": []}
    for name, kind, tool, hard, need, drop in BLOCKS:
        by[tool].append(M + name)
        if need in needs:
            needs[need].append(M + name)
    tag(T / "mineable" / "pickaxe.json", by["pickaxe"])
    tag(T / "mineable" / "shovel.json", by["shovel"])
    tag(T / "needs_stone_tool.json", needs["stone"])
    tag(T / "needs_iron_tool.json", needs["iron"])
    tag(T / "supports_vegetation.json", [M + "hydrated_regolith"])
    tag(T / "dirt.json", [M + "hydrated_regolith"])
    tag(DATA / "tags" / "item" / "spacesuit_repair.json",
        [M + "titanium_ingot", M + "aluminum_ingot"])
    tag(DATA / "tags" / "item" / "lunar_tool_materials.json", [M + "lunar_rock"])
    tag(DATA / "tags" / "worldgen" / "biome" / "has_structure" / "lab.json", [M + "lunar_plains"])
    tag(DATA / "tags" / "worldgen" / "biome" / "has_structure" / "temple.json", [M + "lunar_plains"])
    tag(VANILLA_DATA / "tags" / "worldgen" / "world_preset" / "normal.json", [M + "lunaire"])


def shaped(name, pattern, key, n=1, cat="misc"):
    write_json(DATA / "recipe" / f"{name}.json", {
        "type": "minecraft:crafting_shaped", "category": cat, "pattern": pattern, "key": key,
        "result": {"id": M + name, "count": n}})


def shapeless(name, ings, result_id=None, n=1, cat="misc"):
    write_json(DATA / "recipe" / f"{name}.json", {
        "type": "minecraft:crafting_shapeless", "category": cat, "ingredients": ings,
        "result": {"id": result_id or M + name, "count": n}})


def gen_recipes():
    ti, al, cb, sc, rock = M + "titanium_ingot", M + "aluminum_ingot", M + "circuit_board", M + "iron_scrap", M + "lunar_rock"
    ice, plat = M + "lunar_ice", M + "lab_plating"
    # Tier 1 : outils en roche lunaire (manche en morceau de fer)
    shaped("lunar_rock_pickaxe", ["RRR", " S ", " S "], {"R": rock, "S": sc}, cat="equipment")
    shaped("lunar_rock_axe", ["RR", "RS", " S"], {"R": rock, "S": sc}, cat="equipment")
    shaped("lunar_rock_shovel", ["R", "S", "S"], {"R": rock, "S": sc}, cat="equipment")
    shaped("lunar_rock_sword", ["R", "R", "S"], {"R": rock, "S": sc}, cat="equipment")
    # Réparation de l'épurateur
    shapeless("air_purifier", [M + "damaged_air_purifier", cb, sc])
    # Bouteille vide
    shaped("oxygen_bottle", ["A", "A"], {"A": al}, 2)
    shaped("lab_plating", ["IA", "AI"], {"I": "minecraft:iron_ingot", "A": al}, 4)
    shaped("circuit_board", ["SSS", "SAS"], {"S": sc, "A": al})
    shaped("hydrogen_cell", [" A ", "ABA", " A "], {"A": al, "B": M + "oxygen_bottle"})
    # Machines
    shaped("solar_panel", ["BBB", "CTC", "PPP"], {"B": "minecraft:blue_stained_glass", "C": cb, "T": ti, "P": plat})
    shaped("atmosphere_sealer", ["PPP", "CBC", "PPP"], {"P": plat, "C": cb, "B": M + "oxygen_bottle_full"})
    shaped("electrolyzer", ["PCP", "ABA", "PPP"], {"P": plat, "C": cb, "A": al, "B": M + "oxygen_bottle"})
    shaped("hydrogen_generator", ["PAP", "ACA", "PTP"], {"P": plat, "A": al, "C": cb, "T": ti})
    shaped("radiator", ["AAA", "CTC", "AAA"], {"A": al, "C": cb, "T": ti})
    # Tier 2 : combinaison renforcée
    shaped("spacesuit_helmet", ["AAA", "ACA"], {"A": al, "C": cb}, cat="equipment")
    shaped("spacesuit_chestplate", ["A A", "ATA", "AAA"], {"A": al, "T": ti}, cat="equipment")
    shaped("spacesuit_leggings", ["ATA", "A A", "A A"], {"A": al, "T": ti}, cat="equipment")
    shaped("spacesuit_boots", ["A A", "T T"], {"A": al, "T": ti}, cat="equipment")
    # Tier 3
    shaped("reentry_module", [" T ", "TCT", "AAA"], {"T": ti, "C": cb, "A": al})
    shaped("launch_platform", ["TTT", "PCP", "AAA"], {"T": ti, "P": plat, "C": cb, "A": al})


# ============================================================================ MONDE

def sky_dimension_type():
    dt = json.loads((TOOLS / "overworld_dimtype.json").read_text(encoding="utf-8"))
    a = dt["attributes"]
    a["minecraft:visual/sky_color"] = "#000000"
    a["minecraft:visual/fog_color"] = "#020205"
    a["minecraft:visual/ambient_light_color"] = "#22252b"
    for k in ("minecraft:visual/cloud_color", "minecraft:visual/cloud_height"):
        a.pop(k, None)
    a["minecraft:gameplay/bed_rule"] = {"can_set_spawn": "never", "can_sleep": "never", "destroy_on_use": False}
    dt["ambient_light"] = 0.08
    dt["timelines"] = "#lunaire:in_moon"
    dt["monster_spawn_light_level"] = 15
    write_json(DATA / "dimension_type" / "moon.json", dt)


def sky_timeline():
    tl = json.loads((TOOLS / "day_timeline.json").read_text(encoding="utf-8"))
    tracks = tl["tracks"]
    # ciel toujours noir (pas d'atmosphère), étoiles toujours visibles
    for k in ("minecraft:visual/sky_color", "minecraft:visual/fog_color", "minecraft:visual/cloud_color",
              "minecraft:visual/sunrise_sunset_color", "minecraft:visual/star_brightness"):
        tracks.pop(k, None)
    tracks["minecraft:visual/star_brightness"] = {"keyframes": [{"ticks": 0, "value": 1.0}]}
    tracks["minecraft:visual/sunrise_sunset_color"] = {"keyframes": [{"ticks": 0, "value": "#00000000"}]}
    write_json(DATA / "timeline" / "moon_day.json", tl)
    tag(DATA / "tags" / "timeline" / "in_moon.json", [M + "moon_day"])


def moon_world():
    sky_dimension_type()
    sky_timeline()
    ns = json.loads((TOOLS / "overworld_noise_settings.json").read_text(encoding="utf-8"))
    ns["default_block"] = M + "lunar_rock"
    ns["default_fluid"] = "minecraft:air"
    ns["sea_level"] = -64
    ns["material_rule"] = M + "moon"
    write_json(DATA / "worldgen" / "noise_settings" / "moon.json", ns)

    write_json(DATA / "worldgen" / "material_rule" / "moon.json", {
        "type": "minecraft:sequence", "sequence": [
            "minecraft:bedrock_floor",
            {"type": "minecraft:condition", "if_true": {"type": "minecraft:above_preliminary_surface"},
             "then_run": {"type": "minecraft:condition", "if_true": "minecraft:under_floor",
                          "then_run": {"type": "minecraft:block", "result_state": M + "regolith"}}}]})

    # Biome unique : plaines lunaires (ciel noir, aucun mob vanilla)
    spawns = {"ambient": [], "axolotls": [], "creature": [], "misc": [], "monster": [],
              "underground_water_creature": [], "water_ambient": [], "water_creature": []}
    biome = {
        "attributes": {"minecraft:gameplay/natural_mob_spawns": {
            "argument": {"spawn_costs": {}, "spawns_by_category": spawns}, "modifier": "overlay"},
            "minecraft:visual/sky_color": "#000000", "minecraft:visual/fog_color": "#020205"},
        "carvers": [], "downfall": 0.0, "effects": {"water_color": "#3f76e4"},
        "features": [[], [], [], [], [], [], [M + "ore_lunar_iron", M + "ore_titanium", M + "ore_aluminum",
                                           M + "ore_lunar_ice", M + "ice_surface"], [], [], [], []],
        "has_precipitation": False, "temperature": 0.0}
    write_json(DATA / "worldgen" / "biome" / "lunar_plains.json", biome)

    def ore_feature(block, size, count, lo, hi, name, disc=0.0):
        write_json(DATA / "worldgen" / "feature" / f"{name}.json", {
            "type": "minecraft:ore", "discard_chance_on_air_exposure": disc, "size": size, "targets": [{
                "state": M + block,
                "target": {"predicate_type": "minecraft:block_match", "block": M + "lunar_rock"}}]})
        write_json(DATA / "worldgen" / "placed_feature" / f"{name}.json", {
            "feature": M + name, "placement": [
                {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
                {"type": "minecraft:height_range", "height": {
                    "type": "minecraft:uniform", "min_inclusive": {"absolute": lo},
                    "max_inclusive": {"absolute": hi}}},
                {"type": "minecraft:biome"}]})

    ore_feature("lunar_iron_ore", 9, 14, -60, 100, "ore_lunar_iron")
    ore_feature("titanium_ore", 6, 6, -64, 20, "ore_titanium")
    ore_feature("aluminum_ore", 8, 10, -30, 80, "ore_aluminum")
    ore_feature("lunar_ice", 12, 8, 30, 110, "ore_lunar_ice")
    ore_feature("lunar_ice", 5, 2, 40, 120, "ice_surface", 0.0)

    dims = {
        "type": M + "moon",
        "generator": {"type": "minecraft:noise", "settings": M + "moon",
                      "biome_source": {"type": "minecraft:fixed", "biome": M + "lunar_plains"}}}
    write_json(DATA / "dimension" / "moon.json", dims)
    write_json(DATA / "dimension" / "earth.json", {
        "type": "minecraft:overworld",
        "generator": {"type": "minecraft:noise", "settings": "minecraft:overworld",
                      "biome_source": {"type": "minecraft:multi_noise", "preset": "minecraft:overworld"}}})

    # Type de monde « Lunaire » : l'Overworld EST la Lune
    write_json(DATA / "worldgen" / "world_preset" / "lunaire.json", {"dimensions": {
        "minecraft:overworld": dims,
        "minecraft:the_nether": {"type": "minecraft:the_nether", "generator": {
            "type": "minecraft:noise", "settings": "minecraft:nether",
            "biome_source": {"type": "minecraft:multi_noise", "preset": "minecraft:nether"}}},
        "minecraft:the_end": {"type": "minecraft:the_end", "generator": {
            "type": "minecraft:noise", "settings": "minecraft:end",
            "biome_source": {"type": "minecraft:the_end"}}}}})
    lang_key = "generator.lunaire.lunaire"
    return lang_key


# ============================================================================ STRUCTURES

LP, AN, SL = "lunaire:lab_plating", "lunaire:ancient_stone", "minecraft:air"


def build_capsule():
    t = Template(9, 6, 9)
    t.fill(0, 0, 0, 8, 5, 8, SL)
    t.fill(1, 0, 1, 7, 0, 7, LP)
    t.fill(1, 1, 1, 7, 4, 7, SL)
    # coque (dôme cassé)
    for x in range(1, 8):
        for z in range(1, 8):
            edge = x in (1, 7) or z in (1, 7)
            if edge:
                for y in range(1, 4):
                    if (x * 7 + z * 3 + y) % 5 != 0:  # trous = débris
                        t.set(x, y, z, LP)
            if 2 <= x <= 6 and 2 <= z <= 6 and (x + z) % 3 != 0:
                t.set(x, 4, z, LP)
    t.fill(4, 1, 1, 4, 2, 1, SL)  # entrée
    t.set(6, 1, 6, "lunaire:lab_plating")
    t.chest(5, 1, 5, "west", "lunaire:chests/capsule")
    t.set(2, 1, 6, "lunaire:solar_panel")
    t.write(DATA / "structure" / "capsule.nbt")


def build_lab():
    t = Template(13, 6, 11)
    t.fill(0, 0, 0, 12, 5, 10, SL)
    t.fill(0, 0, 0, 12, 0, 10, LP)
    t.fill(0, 5, 0, 12, 5, 10, LP)
    for y in range(1, 5):
        t.fill(0, y, 0, 12, y, 0, LP)
        t.fill(0, y, 10, 12, y, 10, LP)
        t.fill(0, y, 0, 0, y, 10, LP)
        t.fill(12, y, 0, 12, y, 10, LP)
    t.fill(6, 1, 0, 6, 2, 0, SL)  # porte
    for x in range(3, 10, 3):
        t.set(x, 1, 3, "minecraft:iron_block")
    t.fill(5, 1, 8, 8, 1, 8, "lunaire:solar_panel")
    t.chest(2, 1, 8, "south", "lunaire:chests/lab")
    t.chest(10, 1, 8, "south", "lunaire:chests/lab")
    # effondrement partiel : trous dans le toit
    for p in ((3, 5, 3), (4, 5, 4), (9, 5, 6), (8, 5, 2), (6, 5, 7)):
        t.set(*p, SL)
    t.write(DATA / "structure" / "lab.nbt")


def build_temple():
    t = Template(13, 9, 13)
    t.fill(0, 0, 0, 12, 8, 12, AN)
    t.fill(1, 1, 1, 11, 6, 11, SL)
    t.fill(5, 0, 5, 7, 0, 7, "lunaire:launch_platform")
    # piliers
    for x, z in ((2, 2), (2, 10), (10, 2), (10, 10)):
        t.fill(x, 1, z, x, 6, z, AN)
    # autel
    t.fill(5, 1, 5, 7, 1, 7, AN)
    t.chest(6, 2, 6, "south", "lunaire:chests/temple")
    # accès par le haut : escalier de puits
    t.fill(6, 6, 0, 6, 8, 0, SL)
    t.fill(6, 6, 1, 6, 6, 4, SL)
    t.fill(6, 7, 6, 6, 8, 6, SL)
    t.fill(6, 7, 6, 6, 8, 12, SL)
    t.fill(6, 7, 6, 6, 8, 6, SL)
    t.write(DATA / "structure" / "temple.nbt")


def structure(name, step, biomes_tag, start_h, adapt, salt, spacing, sep):
    write_json(DATA / "worldgen" / "template_pool" / f"{name}.json", {
        "elements": [{"element": {"element_type": "minecraft:single_pool_element", "location": f"{M}{name}",
                                  "processors": "minecraft:empty", "projection": "rigid"}, "weight": 1}],
        "fallback": "minecraft:empty"})
    write_json(DATA / "worldgen" / "structure" / f"{name}.json", {
        "type": "minecraft:jigsaw", "biomes": f"#{M}has_structure/{name}", "max_distance_from_center": 80,
        "project_start_to_heightmap": "WORLD_SURFACE_WG", "size": 1, "spawn_overrides": {},
        "start_height": {"absolute": start_h}, "start_pool": f"{M}{name}", "step": step,
        "terrain_adaptation": adapt, "use_expansion_hack": False})
    write_json(DATA / "worldgen" / "structure_set" / f"{name}.json", {
        "placement": {"type": "minecraft:random_spread", "salt": salt, "separation": sep, "spacing": spacing},
        "structures": [{"structure": f"{M}{name}", "weight": 1}]})


def gen_structures():
    build_capsule()
    build_lab()
    build_temple()
    structure("lab", "surface_structures", None, 0, "beard_thin", 91731, 14, 5)
    structure("temple", "underground_structures", None, -8, "none", 52817, 16, 6)


# ============================================================================ MAIN

def main():
    for p in (RES / "assets", RES / "data"):
        if p.exists():
            shutil.rmtree(p)
    gen_assets()
    gen_loot()
    gen_tags()
    gen_recipes()
    moon_world()
    gen_structures()
    # nom du type de monde
    for f, name in (("fr_fr", "Lunaire (la Lune)"), ("en_us", "Lunaire (the Moon)")):
        p = ASSETS / "lang" / f"{f}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d["generator.lunaire.lunaire"] = name
        write_json(p, d)
    n = sum(1 for _ in RES.rglob("*") if _.is_file())
    print(f"Lunaire : {n} fichiers générés dans {RES}")


if __name__ == "__main__":
    main()
