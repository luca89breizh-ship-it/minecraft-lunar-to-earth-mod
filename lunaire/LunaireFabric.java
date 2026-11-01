package fr.lunaire.fabric;

import fr.lunaire.Lunaire;
import fr.lunaire.fabric.content.ModBlocks;
import fr.lunaire.fabric.content.ModEntities;
import fr.lunaire.fabric.content.ModItems;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

public final class LunaireFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        ModBlocks.init();
        ModItems.init();
        ModEntities.init();
        ModAttachments.init();

        CreativeModeTab tab = CreativeModeTab.builder(CreativeModeTab.Row.TOP, 0)
                .title(Component.translatable("itemGroup.lunaire"))
                .icon(() -> new ItemStack(ModBlocks.REGOLITH))
                .displayItems((params, output) -> {
                    ModBlocks.BLOCK_ITEMS.forEach(output::accept);
                    ModItems.ALL.forEach(output::accept);
                })
                .build();
        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, Lunaire.id("lunaire"), tab);

        LunarGravity.init();
        Machines.init();
        Launch.init();
        Survival.init();
    }
}
