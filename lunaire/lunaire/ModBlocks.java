package fr.lunaire.fabric.content;

import fr.lunaire.Lunaire;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.function.UnaryOperator;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour.Properties;
import net.minecraft.world.level.material.MapColor;

public final class ModBlocks {
    private ModBlocks() {}

    public static final List<Item> BLOCK_ITEMS = new ArrayList<>();

    public static final Block REGOLITH = block("regolith", p -> p.mapColor(MapColor.COLOR_LIGHT_GRAY).strength(0.6F).sound(SoundType.GRAVEL), Block::new);
    public static final Block HYDRATED_REGOLITH = block("hydrated_regolith", p -> p.mapColor(MapColor.COLOR_GRAY).strength(0.6F).sound(SoundType.GRAVEL), Block::new);
    public static final Block LUNAR_ROCK = block("lunar_rock", p -> p.mapColor(MapColor.STONE).strength(2.0F, 6.0F).sound(SoundType.STONE).requiresCorrectToolForDrops(), Block::new);
    public static final Block LUNAR_ICE = block("lunar_ice", p -> p.mapColor(MapColor.ICE).strength(0.8F).friction(0.98F).sound(SoundType.GLASS).requiresCorrectToolForDrops(), Block::new);
    public static final Block LUNAR_IRON_ORE = block("lunar_iron_ore", p -> p.mapColor(MapColor.STONE).strength(3.0F, 3.0F).sound(SoundType.STONE).requiresCorrectToolForDrops(), Block::new);
    public static final Block TITANIUM_ORE = block("titanium_ore", p -> p.mapColor(MapColor.STONE).strength(4.0F, 4.0F).sound(SoundType.STONE).requiresCorrectToolForDrops(), Block::new);
    public static final Block ALUMINUM_ORE = block("aluminum_ore", p -> p.mapColor(MapColor.STONE).strength(3.0F, 3.0F).sound(SoundType.STONE).requiresCorrectToolForDrops(), Block::new);
    public static final Block LAB_PLATING = block("lab_plating", p -> p.mapColor(MapColor.METAL).strength(3.0F, 6.0F).sound(SoundType.METAL).requiresCorrectToolForDrops(), Block::new);
    public static final Block ANCIENT_STONE = block("ancient_stone", p -> p.mapColor(MapColor.DIRT).strength(3.0F, 8.0F).sound(SoundType.STONE).requiresCorrectToolForDrops(), Block::new);
    public static final Block LAUNCH_PLATFORM = block("launch_platform", p -> p.mapColor(MapColor.METAL).strength(5.0F, 12.0F).sound(SoundType.METAL).requiresCorrectToolForDrops(), Block::new);
    public static final Block SOLAR_PANEL = block("solar_panel", p -> p.mapColor(MapColor.COLOR_BLUE).strength(2.0F, 3.0F).sound(SoundType.METAL).requiresCorrectToolForDrops(), Block::new);
    public static final Block ATMOSPHERE_SEALER = block("atmosphere_sealer", p -> p.mapColor(MapColor.METAL).strength(3.0F, 6.0F).sound(SoundType.METAL).requiresCorrectToolForDrops(), Block::new);
    public static final Block ELECTROLYZER = block("electrolyzer", p -> p.mapColor(MapColor.METAL).strength(3.0F, 6.0F).sound(SoundType.METAL).requiresCorrectToolForDrops(), Block::new);
    public static final Block HYDROGEN_GENERATOR = block("hydrogen_generator", p -> p.mapColor(MapColor.METAL).strength(3.0F, 6.0F).sound(SoundType.METAL).requiresCorrectToolForDrops()
            .lightLevel(s -> s.getValue(FueledBlock.LIT) ? 8 : 0), FueledBlock::new);
    public static final Block RADIATOR = block("radiator", p -> p.mapColor(MapColor.METAL).strength(3.0F, 6.0F).sound(SoundType.METAL).requiresCorrectToolForDrops()
            .lightLevel(s -> s.getValue(FueledBlock.LIT) ? 10 : 0), FueledBlock::new);

    private static Block block(String name, UnaryOperator<Properties> cfg, Function<Properties, Block> ctor) {
        ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, Lunaire.id(name));
        Block block = ctor.apply(cfg.apply(Properties.of()).setId(key));
        Registry.register(BuiltInRegistries.BLOCK, key, block);
        ResourceKey<Item> itemKey = ResourceKey.create(Registries.ITEM, Lunaire.id(name));
        Item item = new BlockItem(block, new Item.Properties().setId(itemKey).useBlockDescriptionPrefix());
        Registry.register(BuiltInRegistries.ITEM, itemKey, item);
        BLOCK_ITEMS.add(item);
        return block;
    }

    public static void init() {}
}
