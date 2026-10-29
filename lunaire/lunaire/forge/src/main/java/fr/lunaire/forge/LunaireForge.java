package fr.lunaire.forge;

import fr.lunaire.Lunaire;
import fr.lunaire.content.LunaireContent;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.eventbus.api.bus.BusGroup;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.RegisterEvent;

@Mod(Lunaire.MOD_ID)
public final class LunaireForge {
    public LunaireForge(FMLJavaModLoadingContext context) {
        BusGroup modBus = context.getModBusGroup();
        RegisterEvent.getBus(modBus).addListener(LunaireForge::onRegister);
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
        } else if (event.getRegistryKey().equals(Registries.CREATIVE_MODE_TAB)) {
            CreativeModeTab tab = CreativeModeTab.builder(CreativeModeTab.Row.TOP, 0)
                    .title(Component.literal("Lunaire"))
                    .icon(() -> new ItemStack(LunaireContent.itemsFor(CreativeModeTabs.BUILDING_BLOCKS).get(0)))
                    .displayItems((params, output) -> {
                        LunaireContent.itemsFor(CreativeModeTabs.BUILDING_BLOCKS).forEach(i -> output.accept(i));
                        LunaireContent.itemsFor(CreativeModeTabs.INGREDIENTS).forEach(i -> output.accept(i));
                    })
                    .build();
            event.register(Registries.CREATIVE_MODE_TAB, Lunaire.id("lunaire"), () -> tab);
        }
    }
}
