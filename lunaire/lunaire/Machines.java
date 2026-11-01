package fr.lunaire.fabric;

import fr.lunaire.fabric.content.FueledBlock;
import fr.lunaire.fabric.content.ModBlocks;
import fr.lunaire.fabric.content.ModItems;
import java.util.HashMap;
import java.util.Map;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.UseBlockCallback;
import net.fabricmc.fabric.api.event.player.UseItemCallback;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/** Interactions avec les machines : électrolyseur, générateur, radiateur, scelleur, régolithe, plateforme. */
public final class Machines {
    private Machines() {}

    /** Fin de combustion (temps de jeu) des machines allumées, par dimension+position. */
    private static final Map<String, Long> BURN_END = new HashMap<>();

    private static String key(Level level, BlockPos pos) {
        return level.dimension().toString() + pos.asLong();
    }

    public static void init() {
        UseBlockCallback.EVENT.register((player, level, hand, hit) -> {
            if (hand != InteractionHand.MAIN_HAND) {
                return InteractionResult.PASS;
            }
            BlockPos pos = hit.getBlockPos();
            BlockState state = level.getBlockState(pos);
            Block block = state.getBlock();
            ItemStack held = player.getItemInHand(hand);
            boolean machine = block == ModBlocks.ELECTROLYZER || block == ModBlocks.HYDROGEN_GENERATOR
                    || block == ModBlocks.RADIATOR || block == ModBlocks.ATMOSPHERE_SEALER
                    || block == ModBlocks.LAUNCH_PLATFORM
                    || (block == ModBlocks.REGOLITH && held.is(ModBlocks.LUNAR_ICE.asItem()));
            if (!machine) {
                return InteractionResult.PASS;
            }
            if (level.isClientSide() || !(player instanceof ServerPlayer sp)) {
                return InteractionResult.SUCCESS;
            }
            ServerLevel sl = (ServerLevel) level;
            if (block == ModBlocks.ELECTROLYZER) {
                electrolyze(sp, sl, pos, held);
            } else if (block == ModBlocks.HYDROGEN_GENERATOR || block == ModBlocks.RADIATOR) {
                fuel(sp, sl, pos, state, held);
            } else if (block == ModBlocks.ATMOSPHERE_SEALER) {
                int v = Habitat.enclosedVolume(sl, pos.above());
                if (v < 0) {
                    v = Habitat.enclosedVolume(sl, pos.north());
                }
                sp.sendSystemMessage(v > 0 ? Component.translatable("lunaire.sealed", v)
                        : Component.translatable("lunaire.leak"));
            } else if (block == ModBlocks.LAUNCH_PLATFORM) {
                Launch.tryStart(sp, held);
            } else {
                level.setBlock(pos, ModBlocks.HYDRATED_REGOLITH.defaultBlockState(), 3);
                held.shrink(1);
                sp.sendSystemMessage(Component.translatable("lunaire.hydrated"));
            }
            return InteractionResult.SUCCESS;
        });

        // Bouteille d'O₂ pleine : recharge la réserve d'oxygène
        UseItemCallback.EVENT.register((player, level, hand) -> {
            ItemStack stack = player.getItemInHand(hand);
            if (!stack.is(ModItems.OXYGEN_BOTTLE_FULL)) {
                return InteractionResult.PASS;
            }
            if (!level.isClientSide() && player instanceof ServerPlayer) {
                int o2 = player.getAttachedOrCreate(ModAttachments.OXYGEN);
                player.setAttached(ModAttachments.OXYGEN, Math.min(ModAttachments.O2_MAX, o2 + 1000));
                stack.shrink(1);
                player.getInventory().add(new ItemStack(ModItems.OXYGEN_BOTTLE));
            }
            return InteractionResult.SUCCESS;
        });

        // Les machines allumées s'éteignent à la fin de leur cellule
        ServerTickEvents.END_SERVER_TICK.register(server -> {
            if (server.getTickCount() % 20 != 0 || BURN_END.isEmpty()) {
                return;
            }
            for (ServerLevel level : server.getAllLevels()) {
                long now = level.getGameTime();
                BURN_END.entrySet().removeIf(e -> {
                    if (!e.getKey().startsWith(level.dimension().toString())) {
                        return false;
                    }
                    if (now < e.getValue()) {
                        return false;
                    }
                    long packed = Long.parseLong(e.getKey().substring(level.dimension().toString().length()));
                    BlockPos p = BlockPos.of(packed);
                    BlockState st = level.getBlockState(p);
                    if (st.getBlock() instanceof FueledBlock) {
                        level.setBlock(p, st.setValue(FueledBlock.LIT, false), 3);
                    }
                    return true;
                });
            }
        });
    }

    // ------------------------------------------------------------------ énergie

    public static boolean isDay(Level level) {
        return level.getGameTime() % 24000L < 12500L;
    }

    public static boolean isPowered(Level level, BlockPos center) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (int dx = -4; dx <= 4; dx++) {
            for (int dy = -3; dy <= 3; dy++) {
                for (int dz = -4; dz <= 4; dz++) {
                    p.set(center.getX() + dx, center.getY() + dy, center.getZ() + dz);
                    BlockState st = level.getBlockState(p);
                    if (st.is(ModBlocks.SOLAR_PANEL) && isDay(level) && level.canSeeSky(p.above())) {
                        return true;
                    }
                    if (st.is(ModBlocks.HYDROGEN_GENERATOR) && st.getValue(FueledBlock.LIT)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    public static boolean litRadiatorNear(Level level, BlockPos center, int r) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (int dx = -r; dx <= r; dx++) {
            for (int dy = -r; dy <= r; dy++) {
                for (int dz = -r; dz <= r; dz++) {
                    p.set(center.getX() + dx, center.getY() + dy, center.getZ() + dz);
                    BlockState st = level.getBlockState(p);
                    if (st.is(ModBlocks.RADIATOR) && st.getValue(FueledBlock.LIT)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    private static void electrolyze(ServerPlayer sp, ServerLevel level, BlockPos pos, ItemStack held) {
        if (!isPowered(level, pos)) {
            sp.sendSystemMessage(Component.translatable("lunaire.no_power"));
            return;
        }
        if (!held.is(ModBlocks.LUNAR_ICE.asItem())) {
            sp.sendSystemMessage(Component.translatable("lunaire.no_ice"));
            return;
        }
        Inventory inv = sp.getInventory();
        int made = 0;
        for (int i = 0; i < inv.getContainerSize() && made < 2; i++) {
            ItemStack s = inv.getItem(i);
            while (!s.isEmpty() && s.is(ModItems.OXYGEN_BOTTLE) && made < 2) {
                s.shrink(1);
                made++;
            }
        }
        if (made == 0) {
            sp.sendSystemMessage(Component.literal("Il faut une bouteille d'O₂ vide."));
            return;
        }
        held.shrink(1);
        inv.add(new ItemStack(ModItems.OXYGEN_BOTTLE_FULL, made));
        sp.sendSystemMessage(Component.translatable("lunaire.powered"));
    }

    private static void fuel(ServerPlayer sp, ServerLevel level, BlockPos pos, BlockState state, ItemStack held) {
        if (!held.is(ModItems.HYDROGEN_CELL)) {
            return;
        }
        held.shrink(1);
        long now = level.getGameTime();
        String k = key(level, pos);
        long end = Math.max(now, BURN_END.getOrDefault(k, now)) + 6000L;
        BURN_END.put(k, end);
        level.setBlock(pos, state.setValue(FueledBlock.LIT, true), 3);
        sp.sendSystemMessage(Component.translatable("lunaire.fuelled"));
    }
}
