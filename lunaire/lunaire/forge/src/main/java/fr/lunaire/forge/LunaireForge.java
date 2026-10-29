package fr.lunaire.forge;

import fr.lunaire.Lunaire;
import fr.lunaire.content.LunaireContent;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.eventbus.api.bus.BusGroup;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.RegisterEvent;

@Mod(Lunaire.MOD_ID)
public final class LunaireForge {
    public LunaireForge(FMLJavaModLoadingContext context) {
        BusGroup modBus = context.getModBusGroup();
        RegisterEvent.getBus(modBus).addListener(LunaireForge::onRegister);
        BuildCreativeModeTabContentsEvent.getBus(modBus).addListener(LunaireForge::onBuildTabs);
    }

    private static void onRegister(RegisterEvent event) {
        if (event.getRegistryKey().equals(Registries.BLOCK)) {
            for (LunaireContent.BlockDef def : LunaireContent.BLOCKS) {
                Block block = LunaireContent.createBlock(def);
                event.register(Registries.BLOCK, Lunaire.id(def.name()), () -> block);
            }
        } else if (event.getRegistryKey().equals(Registries.ITEM)) {
            for (LunaireContent.BlockDef def : LunaireContent.BLOCKS) {
                Item item = LunaireContent.createBlockItem(def.name());
                event.register(Registries.ITEM, Lunaire.id(def.name()), () -> item);
            }
            for (LunaireContent.ItemDef def : LunaireContent.ITEMS) {
                Item item = LunaireContent.createItem(def);
                event.register(Registries.ITEM, Lunaire.id(def.name()), () -> item);
            }
        }
    }

    private static void onBuildTabs(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey().equals(CreativeModeTabs.BUILDING_BLOCKS)
                || event.getTabKey().equals(CreativeModeTabs.INGREDIENTS)) {
            LunaireContent.itemsFor(event.getTabKey()).forEach(event::accept);
        }
    }
}
