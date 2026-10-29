package fr.lunaire.fabric;

import fr.lunaire.Lunaire;
import fr.lunaire.content.LunaireContent;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;

public final class LunaireFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        for (LunaireContent.BlockDef def : LunaireContent.BLOCKS) {
            Block block = LunaireContent.createBlock(def);
            Registry.register(BuiltInRegistries.BLOCK, Lunaire.id(def.name()), block);
        }
        for (LunaireContent.BlockDef def : LunaireContent.BLOCKS) {
            Item item = LunaireContent.createBlockItem(def.name());
            Registry.register(BuiltInRegistries.ITEM, Lunaire.id(def.name()), item);
        }
        for (LunaireContent.ItemDef def : LunaireContent.ITEMS) {
            Item item = LunaireContent.createItem(def);
            Registry.register(BuiltInRegistries.ITEM, Lunaire.id(def.name()), item);
        }

        CreativeModeTab tab = CreativeModeTab.builder(CreativeModeTab.Row.TOP, 0)
                .title(Component.literal("Lunaire"))
                .icon(() -> new ItemStack(LunaireContent.itemsFor(CreativeModeTabs.BUILDING_BLOCKS).get(0)))
                .displayItems((params, output) -> {
                    LunaireContent.itemsFor(CreativeModeTabs.BUILDING_BLOCKS).forEach(i -> output.accept(i));
                    LunaireContent.itemsFor(CreativeModeTabs.INGREDIENTS).forEach(i -> output.accept(i));
                })
                .build();
        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, Lunaire.id("lunaire"), tab);
    }
}
