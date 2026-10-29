package fr.lunaire.content;

import fr.lunaire.Lunaire;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.UnaryOperator;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

/**
 * Contenu du mod, défini une seule fois pour Fabric et Forge.
 * Chaque loader ne fait que l'enregistrement dans les registres.
 */
public final class LunaireContent {
    private LunaireContent() {}

    // ---------------------------------------------------------------- Définitions

    public record BlockDef(String name, UnaryOperator<BlockBehaviour.Properties> properties) {}

    public record ItemDef(String name, int stackSize) {}

    /** Étape 1 : Régolithe (remplace la terre), Roche Lunaire (remplace la pierre), Glace Lunaire. */
    public static final List<BlockDef> BLOCKS = List.of(
            new BlockDef("regolith", p -> p
                    .mapColor(MapColor.COLOR_LIGHT_GRAY)
                    .strength(0.6F)
                    .sound(SoundType.GRAVEL)),
            new BlockDef("lunar_rock", p -> p
                    .mapColor(MapColor.STONE)
                    .strength(2.0F, 6.0F)
                    .sound(SoundType.STONE)
                    .requiresCorrectToolForDrops()),
            new BlockDef("lunar_ice", p -> p
                    .mapColor(MapColor.ICE)
                    .strength(0.8F)
                    .friction(0.98F)
                    .sound(SoundType.GLASS)
                    .requiresCorrectToolForDrops()));

    /** Objets simples : l'épurateur endommagé de la capsule, drops des golems, loot des labos. */
    public static final List<ItemDef> ITEMS = List.of(
            new ItemDef("damaged_air_purifier", 1),
            new ItemDef("meteorite_shard", 64),
            new ItemDef("circuit_board", 64),
            new ItemDef("iron_scrap", 64));

    // ---------------------------------------------------------------- Instances créées

    private static final Map<String, Block> CREATED_BLOCKS = new LinkedHashMap<>();
    private static final Map<String, Item> CREATED_BLOCK_ITEMS = new LinkedHashMap<>();
    private static final Map<String, Item> CREATED_ITEMS = new LinkedHashMap<>();

    /** Construit le bloc (sans l'enregistrer). L'id doit être posé dans les propriétés avant la construction. */
    public static Block createBlock(BlockDef def) {
        ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, Lunaire.id(def.name()));
        BlockBehaviour.Properties props = def.properties().apply(BlockBehaviour.Properties.of()).setId(key);
        Block block = new Block(props);
        CREATED_BLOCKS.put(def.name(), block);
        return block;
    }

    /** Construit le BlockItem d'un bloc déjà créé par {@link #createBlock}. */
    public static Item createBlockItem(String blockName) {
        Block block = CREATED_BLOCKS.get(blockName);
        if (block == null) {
            throw new IllegalStateException("Le bloc " + blockName + " doit être créé avant son item");
        }
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, Lunaire.id(blockName));
        Item item = new BlockItem(block, new Item.Properties().setId(key).useBlockDescriptionPrefix());
        CREATED_BLOCK_ITEMS.put(blockName, item);
        return item;
    }

    public static Item createItem(ItemDef def) {
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, Lunaire.id(def.name()));
        Item item = new Item(new Item.Properties().setId(key).stacksTo(def.stackSize()));
        CREATED_ITEMS.put(def.name(), item);
        return item;
    }

    // ---------------------------------------------------------------- Onglets créatifs

    /** Items à ajouter dans un onglet créatif vanilla donné. */
    public static List<Item> itemsFor(ResourceKey<CreativeModeTab> tab) {
        if (CreativeModeTabs.BUILDING_BLOCKS.equals(tab)) {
            return new ArrayList<>(CREATED_BLOCK_ITEMS.values());
        }
        if (CreativeModeTabs.INGREDIENTS.equals(tab)) {
            return new ArrayList<>(CREATED_ITEMS.values());
        }
        return List.of();
    }
}
