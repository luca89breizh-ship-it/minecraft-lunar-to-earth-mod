package fr.lunaire.fabric.content;

import fr.lunaire.Lunaire;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.function.UnaryOperator;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;

public final class ModItems {
    private ModItems() {}

    public static final List<Item> ALL = new ArrayList<>();

    private static final TagKey<Item> LUNAR_TOOL_MATERIALS = TagKey.create(Registries.ITEM, Lunaire.id("lunar_tool_materials"));
    private static final TagKey<Item> SPACESUIT_REPAIR = TagKey.create(Registries.ITEM, Lunaire.id("spacesuit_repair"));

    public static final ToolMaterial LUNAR_ROCK_MATERIAL =
            new ToolMaterial(BlockTags.INCORRECT_FOR_STONE_TOOL, 131, 4.0F, 1.0F, 5, LUNAR_TOOL_MATERIALS);

    public static final ResourceKey<EquipmentAsset> SPACESUIT_ASSET =
            ResourceKey.create(EquipmentAssets.ROOT_ID, Lunaire.id("spacesuit"));

    public static final ArmorMaterial SPACESUIT_MATERIAL = new ArmorMaterial(
            26, armorMap(), 12, SoundEvents.ARMOR_EQUIP_IRON, 1.0F, 0.0F, SPACESUIT_REPAIR, SPACESUIT_ASSET);

    private static EnumMap<ArmorType, Integer> armorMap() {
        EnumMap<ArmorType, Integer> map = new EnumMap<>(ArmorType.class);
        map.put(ArmorType.BOOTS, 2);
        map.put(ArmorType.LEGGINGS, 5);
        map.put(ArmorType.CHESTPLATE, 6);
        map.put(ArmorType.HELMET, 2);
        map.put(ArmorType.BODY, 6);
        return map;
    }

    public static final Item TITANIUM_INGOT = simple("titanium_ingot");
    public static final Item ALUMINUM_INGOT = simple("aluminum_ingot");
    public static final Item IRON_SCRAP = simple("iron_scrap");
    public static final Item METEORITE_SHARD = simple("meteorite_shard");
    public static final Item CIRCUIT_BOARD = simple("circuit_board");
    public static final Item OXYGEN_BOTTLE = simple("oxygen_bottle");
    public static final Item OXYGEN_BOTTLE_FULL = item("oxygen_bottle_full", p -> p.stacksTo(16));
    public static final Item HYDROGEN_CELL = simple("hydrogen_cell");
    public static final Item DAMAGED_AIR_PURIFIER = item("damaged_air_purifier", p -> p.stacksTo(1));
    public static final Item AIR_PURIFIER = item("air_purifier", p -> p.stacksTo(1));
    public static final Item ROCKET_BLUEPRINT = item("rocket_blueprint", p -> p.stacksTo(1));
    public static final Item REENTRY_MODULE = item("reentry_module", p -> p.stacksTo(1));

    public static final Item LUNAR_ROCK_PICKAXE = item("lunar_rock_pickaxe", p -> p.pickaxe(LUNAR_ROCK_MATERIAL, 1.0F, -2.8F));
    public static final Item LUNAR_ROCK_AXE = item("lunar_rock_axe", p -> p.axe(LUNAR_ROCK_MATERIAL, 6.0F, -3.2F));
    public static final Item LUNAR_ROCK_SHOVEL = item("lunar_rock_shovel", p -> p.shovel(LUNAR_ROCK_MATERIAL, 1.5F, -3.0F));
    public static final Item LUNAR_ROCK_SWORD = item("lunar_rock_sword", p -> p.sword(LUNAR_ROCK_MATERIAL, 3.0F, -2.4F));

    public static final Item SPACESUIT_HELMET = item("spacesuit_helmet", p -> p.humanoidArmor(SPACESUIT_MATERIAL, ArmorType.HELMET));
    public static final Item SPACESUIT_CHESTPLATE = item("spacesuit_chestplate", p -> p.humanoidArmor(SPACESUIT_MATERIAL, ArmorType.CHESTPLATE));
    public static final Item SPACESUIT_LEGGINGS = item("spacesuit_leggings", p -> p.humanoidArmor(SPACESUIT_MATERIAL, ArmorType.LEGGINGS));
    public static final Item SPACESUIT_BOOTS = item("spacesuit_boots", p -> p.humanoidArmor(SPACESUIT_MATERIAL, ArmorType.BOOTS));

    private static Item simple(String name) {
        return item(name, p -> p);
    }

    private static Item item(String name, UnaryOperator<Item.Properties> cfg) {
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, Lunaire.id(name));
        Item item = new Item(cfg.apply(new Item.Properties().setId(key)));
        Registry.register(BuiltInRegistries.ITEM, key, item);
        ALL.add(item);
        return item;
    }

    public static void init() {}
}
