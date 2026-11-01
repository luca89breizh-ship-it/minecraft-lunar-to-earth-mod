"""Textures procédurales (16x16 blocs/objets, 64x64 créatures, 64x32 armure)."""
import random
from lg_core import Img, shade, noise_fill, ASSETS

BT = ASSETS / "textures" / "block"
IT = ASSETS / "textures" / "item"
ET = ASSETS / "textures" / "entity"

GREY = (150, 150, 155)
ROCK = (88, 88, 96)
REGO = (176, 172, 166)
ICE = (170, 215, 240)
IRON = (200, 150, 120)
TITAN = (120, 135, 170)
ALU = (205, 210, 220)


def block_noise(name, base, var=12, seed=1):
    img = Img(16, 16)
    noise_fill(img, 0, 0, 16, 16, base, var, seed)
    return img


def craters(img, base, seed, n=3):
    rng = random.Random(seed)
    for _ in range(n):
        cx, cy, r = rng.randint(2, 13), rng.randint(2, 13), rng.randint(1, 2)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    img.set(x, y, shade(base, -22))
    return img


def ore(base, color, seed):
    img = block_noise("o", base, 10, seed)
    rng = random.Random(seed * 7)
    for _ in range(5):
        cx, cy = rng.randint(2, 13), rng.randint(2, 13)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0)):
            img.set(cx + dx, cy + dy, shade(color, rng.randint(-18, 18)))
    return img


def panel(base, line, seed=3):
    img = block_noise("p", base, 5, seed)
    for i in range(16):
        for k in (0, 7, 8, 15):
            img.set(i, k, line)
            img.set(k, i, line)
    for p in ((2, 2), (13, 2), (2, 13), (13, 13)):
        img.set(*p, (230, 230, 235))
    return img


def machine(base, accent, seed, kind):
    img = Img(16, 16)
    noise_fill(img, 0, 0, 16, 16, base, 5, seed)
    for i in range(16):
        for k in (0, 15):
            img.set(i, k, shade(base, -35))
            img.set(k, i, shade(base, -35))
    if kind == "front":
        img.rect(4, 4, 8, 8, shade(base, -50))
        img.rect(5, 5, 6, 6, accent)
        img.rect(6, 6, 4, 4, shade(accent, 50))
    elif kind == "top":
        for y in range(2, 14):
            for x in range(2, 14):
                if (x + y) % 4 == 0:
                    img.set(x, y, accent)
    return img


def solar_top():
    img = Img(16, 16)
    noise_fill(img, 0, 0, 16, 16, (25, 45, 110), 8, 11)
    for i in range(16):
        for k in (0, 5, 10, 15):
            img.set(i, k, (190, 195, 205))
            img.set(k, i, (190, 195, 205))
    return img


def radiator(lit):
    img = Img(16, 16)
    noise_fill(img, 0, 0, 16, 16, (90, 90, 100), 5, 21)
    for y in range(16):
        c = (230, 110, 40) if lit else (60, 60, 68)
        if y % 3 == 1:
            img.rect(1, y, 14, 1, c)
    return img


def generate_blocks():
    B = lambda n, im: im.save(BT / f"{n}.png")
    B("regolith", craters(block_noise("r", REGO, 14, 2), REGO, 2))
    h = block_noise("hr", (120, 112, 105), 12, 4)
    for i in range(0, 16, 3):
        h.set(i, (i * 5) % 16, (70, 150, 220))
    B("hydrated_regolith", h)
    B("lunar_rock", craters(block_noise("l", ROCK, 10, 5), ROCK, 5, 2))
    ice = block_noise("i", ICE, 14, 6)
    for i in range(16):
        ice.set(i, (i * 3 + 2) % 16, (235, 248, 255))
    B("lunar_ice", ice)
    B("lunar_iron_ore", ore(ROCK, IRON, 7))
    B("titanium_ore", ore(ROCK, (150, 170, 215), 8))
    B("aluminum_ore", ore(ROCK, (225, 230, 240), 9))
    B("lab_plating", panel((205, 208, 214), (120, 124, 135)))
    B("ancient_stone", panel((120, 105, 90), (70, 60, 50), 5))
    B("launch_platform", panel((70, 72, 80), (230, 190, 40), 6))
    B("solar_panel_top", solar_top())
    B("solar_panel_side", machine((170, 172, 180), (60, 90, 190), 12, "none"))
    B("atmosphere_sealer_top", machine((150, 160, 170), (80, 200, 220), 13, "top"))
    B("atmosphere_sealer_side", machine((150, 160, 170), (80, 200, 220), 13, "front"))
    B("electrolyzer_top", machine((140, 140, 150), (70, 140, 230), 14, "top"))
    B("electrolyzer_side", machine((140, 140, 150), (70, 140, 230), 14, "front"))
    B("hydrogen_generator_top", machine((130, 130, 140), (200, 200, 90), 15, "top"))
    B("hydrogen_generator_side", machine((130, 130, 140), (90, 90, 90), 15, "front"))
    B("hydrogen_generator_side_lit", machine((130, 130, 140), (255, 200, 60), 15, "front"))
    B("radiator", radiator(False))
    B("radiator_lit", radiator(True))


# ----------------------------------------------------------------------------- objets

def draw(rows, pal):
    from lg_core import sprite
    return sprite(rows, pal)


def item_sprites():
    I = lambda n, im: im.save(IT / f"{n}.png")
    ing = lambda c: draw([
        "................",
        "................",
        "................",
        ".....hhhhhhh....",
        "....hmmmmmmmd...",
        "...hmmmmmmmdd...",
        "..hmmmmmmmdd....",
        "..mmmmmmmdd.....",
        "..dddddddd......",
        "................",
    ] + ["................"] * 6, {"h": shade(c, 40), "m": c, "d": shade(c, -45)})
    I("titanium_ingot", ing(TITAN))
    I("aluminum_ingot", ing(ALU))
    I("iron_scrap", draw([
        "................", "................", "................", "......gg........",
        ".....gGGg.......", "....gGGGGg..g...", "....gGGDGGggg...", ".....gGGDDGGg...",
        "......ggGGDg....", ".......gggg.....",
    ] + ["................"] * 6, {"g": (110, 110, 118), "G": (170, 170, 176), "D": (80, 70, 70)}))
    I("meteorite_shard", draw([
        "................", ".......c........", "......cvc.......", ".....cvVvc......",
        ".....cvVvc......", "....cvVVVvc.....", "....cvVVVvc.....", ".....cvVvc......",
        "......ccc.......",
    ] + ["................"] * 7, {"c": (60, 30, 110), "v": (150, 90, 230), "V": (220, 190, 255)}))
    I("circuit_board", draw([
        "................", "................", "..GGGGGGGGGGGG..", "..GtGGGGtGGGGG..",
        "..GGGgGGGGgGGG..", "..GggGGGGGGgGG..", "..GGGgGcGGgGGG..", "..GtGGGGGGGtGG..",
        "..GGGGGGGGGGGG..", "..GGGGGGGGGGGG..",
    ] + ["................"] * 6, {"G": (30, 120, 60), "t": (220, 180, 60), "g": (70, 190, 100), "c": (30, 30, 30)}))
    bottle = lambda fill: draw([
        "................", "......kkkk......", "......kwwk......", ".......ww.......",
        "......wwww......", ".....wwwwww.....", ".....wFFFFw.....", ".....wFFFFw.....",
        ".....wFFFFw.....", ".....wFFFFw.....", ".....wwwwww.....",
    ] + ["................"] * 5, {"k": (70, 70, 80), "w": (200, 220, 235), "F": fill})
    I("oxygen_bottle", bottle((200, 220, 235, 60)))
    I("oxygen_bottle_full", bottle((90, 190, 255)))
    I("hydrogen_cell", draw([
        "................", ".....kkkkkk.....", "....kYYYYYYk....", "....kyyyyyyk....",
        "....kyyHHyyk....", "....kyyHHyyk....", "....kyyyyyyk....", "....kyyyyyyk....",
        "....kYYYYYYk....", ".....kkkkkk.....",
    ] + ["................"] * 6, {"k": (50, 50, 60), "Y": (230, 230, 120), "y": (200, 200, 90), "H": (255, 255, 255)}))
    pur = lambda dmg: draw([
        "................", "................", "...bbbbbbbbbb...", "..bBBBBBBBBBBb..",
        "..bBfffffffBb...", "..bBfFFFFFfBb...", "..bBfFxFxFfBb...", "..bBfFFFFFfBb...",
        "..bBfffffffBb...", "..bBBBBBBBBBBb..", "...bbbbbbbbbb...",
    ] + ["................"] * 5, {"b": (40, 40, 50), "B": (200, 205, 215), "f": (90, 95, 105),
                                    "F": (60, 60, 70), "x": (200, 60, 60) if dmg else (80, 230, 120)})
    I("damaged_air_purifier", pur(True))
    I("air_purifier", pur(False))
    I("rocket_blueprint", draw([
        "................", "..BBBBBBBBBBBB..", "..BwwwwwwwwwwB..", "..BwLLLLLLLwB...",
        "..BwwwwwwwwwwB..", "..BwLLLwLLLwB...", "..BwwwwwwwwwwB..", "..BwLLLLLwwwB...",
        "..BwwwwwwwwwwB..", "..BBBBBBBBBBBB..",
    ] + ["................"] * 6, {"B": (20, 60, 140), "w": (40, 110, 200), "L": (200, 230, 255)}))
    I("reentry_module", draw([
        "................", ".......rr.......", "......rWWr......", ".....rWWWWr.....",
        "....rWWbbWWr....", "....rWWbbWWr....", "...rWWWWWWWWr...", "...rWWWWWWWWr...",
        "..rrrrrrrrrrrr..", "..ooo.oooo.ooo..", "...o..oooo..o...",
    ] + ["................"] * 5, {"r": (110, 40, 40), "W": (225, 228, 235), "b": (60, 120, 200), "o": (255, 160, 40)}))

    # outils : tête en roche lunaire, manche en ferraille
    H, S, D = (118, 118, 128), (150, 130, 110), (80, 80, 90)
    pal = {"h": H, "s": S, "d": D}
    tools = {
        "lunar_rock_pickaxe": [
            "................", "....hhhhhh......", "...hddddddh.....", "..hd...sdh......",
            ".......ss.......", "......ss........", ".....ss.........", "....ss..........",
            "...ss...........", "..ss............", ".ss.............",
        ],
        "lunar_rock_axe": [
            "................", ".....hhh........", "....hdddh.......", "....hddshh......",
            ".....hss.dh.....", "......ss........", ".....ss.........", "....ss..........",
            "...ss...........", "..ss............", ".ss.............",
        ],
        "lunar_rock_shovel": [
            "................", "...........hh...", "..........hddh..", "..........hddh..",
            "...........hh...", "..........ss....", ".........ss.....", "........ss......",
            ".......ss.......", "......ss........", ".....ss.........", "....ss..........",
        ],
        "lunar_rock_sword": [
            "................", "..............hh", ".............hdh", "............hdh.",
            "...........hdh..", "..........hdh...", ".s.......hdh....", "..s.....hdh.....",
            "...s...hdh......", "....s.hdh.......", ".....ssh........", "....ss.s........",
        ],
    }
    for n, rows in tools.items():
        I(n, draw(rows + ["................"] * (16 - len(rows)), pal))

    def suit(kind):
        W, G, V = (225, 228, 235), (150, 155, 165), (230, 180, 60)
        pal2 = {"W": W, "G": G, "V": V, "k": (60, 62, 72)}
        shapes = {
            "helmet": ["................", "................", ".....kkkkkk.....", "....kWWWWWWk....",
                       "...kWWWWWWWWk...", "...kWVVVVVVWk...", "...kWVVVVVVWk...", "...kWWWWWWWWk...",
                       "...kWGWWWWGWk...", "...kGG....GGk..."],
            "chestplate": ["................", "...kkk....kkk...", "..kWWWkkkkWWWk..", "..kWWWWWWWWWWk..",
                           "..kWWWVVVVWWWk..", "..kWWWVGGVWWWk..", "..kWWWWWWWWWWk..", "...kWWWWWWWWk...",
                           "...kWWWWWWWWk...", "...kkkkkkkkkk..."],
            "leggings": ["................", "...kkkkkkkkkk...", "...kWWWWWWWWk...", "...kWGGWWGGWk...",
                         "...kWWWkkWWWk...", "...kWWWk.kWWWk..", "...kWWWk.kWWWk..", "...kWWWk.kWWWk..",
                         "...kGGGk.kGGGk..", "...kkkk...kkk..."],
            "boots": ["................", "................", "................", "................",
                      "..kkk......kkk..", ".kWWWk....kWWWk.", ".kWWWk....kWWWk.", ".kWWWWk..kWWWWk.",
                      ".kGGGGk..kGGGGk.", ".kkkkkk..kkkkkk."],
        }
        rows = shapes[kind]
        return draw(rows + ["................"] * (16 - len(rows)), pal2)

    for k in ("helmet", "chestplate", "leggings", "boots"):
        I(f"spacesuit_{k}", suit(k))


def armor_textures():
    for layer, name in (("humanoid", "spacesuit"), ("humanoid_leggings", "spacesuit")):
        img = Img(64, 32)
        noise_fill(img, 0, 0, 64, 32, (215, 218, 226), 8, 31)
        for x in range(64):
            for y in (7, 15, 23, 31):
                img.set(x, y, (140, 145, 155))
        if layer == "humanoid":
            img.rect(9, 10, 6, 3, (230, 175, 50))  # visière
            img.rect(10, 11, 4, 1, (255, 215, 110))
            img.rect(20, 20, 8, 2, (230, 175, 50))  # plastron
        img.save(ET / "equipment" / layer / f"{name}.png")


def creature_textures():
    # Sélénite : cristal pâle cyan, yeux lumineux
    img = Img(64, 64)
    noise_fill(img, 0, 0, 64, 64, (150, 215, 235), 18, 41)
    for x in range(0, 64, 4):
        for y in range(0, 64):
            if (x + y) % 9 == 0:
                img.set(x, y, (235, 250, 255))
    img.rect(10, 12, 2, 2, (255, 255, 120))
    img.rect(13, 12, 2, 2, (255, 255, 120))
    img.rect(11, 14, 3, 1, (60, 100, 130))
    img.save(ET / "selenite.png")
    # Golem : poussière grise, cœur orange
    g = Img(64, 64)
    noise_fill(g, 0, 0, 64, 64, (110, 100, 92), 16, 42)
    for x in range(64):
        for y in range(64):
            if (x * 3 + y * 5) % 11 == 0:
                g.set(x, y, (75, 68, 62))
    g.rect(10, 12, 2, 2, (255, 150, 40))
    g.rect(13, 12, 2, 2, (255, 150, 40))
    g.rect(20, 22, 8, 4, (255, 140, 40))
    g.save(ET / "dust_golem.png")
