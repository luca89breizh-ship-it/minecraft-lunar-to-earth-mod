package fr.lunaire.fabric;

import fr.lunaire.Lunaire;
import fr.lunaire.content.LunaireContent;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;

public final class LunaireFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        // Blocs d'abord, puis leurs items, puis les objets simples.
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

        // Onglets créatifs vanilla.
        ItemGroupEvents.modifyEntriesEvent(CreativeModeTabs.BUILDING_BLOCKS)
                .register(entries -> LunaireContent.itemsFor(CreativeModeTabs.BUILDING_BLOCKS).forEach(entries::accept));
        ItemGroupEvents.modifyEntriesEvent(CreativeModeTabs.INGREDIENTS)
                .register(entries -> LunaireContent.itemsFor(CreativeModeTabs.INGREDIENTS).forEach(entries::accept));
    }
}
