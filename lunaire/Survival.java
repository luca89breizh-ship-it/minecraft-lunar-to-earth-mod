package fr.lunaire.fabric;

import fr.lunaire.fabric.content.ModItems;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.Item;

/** Systèmes de survie : oxygène, chaleur du jour, froid de la nuit, apparition des créatures, introduction. */
public final class Survival {
    private Survival() {}

    private static final Map<UUID, Integer> INTRO_QUEUE = new HashMap<>();
    private static final Map<UUID, Boolean> HABITAT_CACHE = new HashMap<>();

    public static void init() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            ServerPlayer sp = handler.getPlayer();
            if (Moon.isMoon(sp) && sp.getAttachedOrCreate(ModAttachments.INTRO) == 0) {
                INTRO_QUEUE.put(sp.getUUID(), 40);
            }
        });
        ServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) ->
                newPlayer.setAttached(ModAttachments.OXYGEN, ModAttachments.O2_MAX));
        ServerTickEvents.END_SERVER_TICK.register(Survival::tick);
    }

    private static int suitPieces(ServerPlayer sp) {
        int n = 0;
        for (Item item : new Item[]{ModItems.SPACESUIT_HELMET, ModItems.SPACESUIT_CHESTPLATE,
                ModItems.SPACESUIT_LEGGINGS, ModItems.SPACESUIT_BOOTS}) {
            for (EquipmentSlot slot : new EquipmentSlot[]{EquipmentSlot.HEAD, EquipmentSlot.CHEST,
                    EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
                if (sp.getItemBySlot(slot).is(item)) {
                    n++;
                    break;
                }
            }
        }
        return n;
    }

    private static boolean hasPurifier(ServerPlayer sp) {
        Inventory inv = sp.getInventory();
        for (int i = 0; i < inv.getContainerSize(); i++) {
            if (inv.getItem(i).is(ModItems.AIR_PURIFIER)) {
                return true;
            }
        }
        return false;
    }

    private static void tick(MinecraftServer server) {
        int t = server.getTickCount();
        for (ServerPlayer sp : server.getPlayerList().getPlayers()) {
            if (!Moon.isMoon(sp)) {
                continue;
            }
            Integer q = INTRO_QUEUE.get(sp.getUUID());
            if (q != null) {
                if (q <= 1) {
                    INTRO_QUEUE.remove(sp.getUUID());
                    intro(server, sp);
                } else {
                    INTRO_QUEUE.put(sp.getUUID(), q - 1);
                }
            }
            if (t % 20 == 0) {
                secondly(server, sp, t);
            }
        }
    }

    private static void intro(MinecraftServer server, ServerPlayer sp) {
        sp.setAttached(ModAttachments.INTRO, 1);
        var src = server.createCommandSourceStack().withSuppressedOutput();
        String id = sp.getStringUUID();
        server.getCommands().performPrefixedCommand(src,
                "execute as " + id + " at @s run place template lunaire:capsule ~-4 ~-1 ~-4");
        server.getCommands().performPrefixedCommand(src,
                "execute as " + id + " at @s run tp @s ~ ~1 ~");
        sp.sendSystemMessage(Component.translatable("lunaire.intro1"));
        sp.sendSystemMessage(Component.translatable("lunaire.intro2"));
    }

    private static void secondly(MinecraftServer server, ServerPlayer sp, int tick) {
        ServerLevel level = (ServerLevel) sp.level();
        BlockPos pos = sp.blockPosition();
        boolean habitat = Habitat.isPressurized(level, pos.above());
        HABITAT_CACHE.put(sp.getUUID(), habitat);
        boolean day = Machines.isDay(level);
        boolean sky = level.canSeeSky(pos.above());
        int suit = suitPieces(sp);

        // --- Oxygène (en dixièmes) : 10/s de base, réduit par l'épurateur et la combinaison
        int o2 = sp.getAttachedOrCreate(ModAttachments.OXYGEN);
        if (habitat) {
            o2 = Math.min(ModAttachments.O2_MAX, o2 + 60);
        } else {
            int drain = 10 - (hasPurifier(sp) ? 4 : 0) - suit;
            o2 = Math.max(0, o2 - drain);
        }
        sp.setAttached(ModAttachments.OXYGEN, o2);
        if (o2 <= 0 && !habitat) {
            sp.hurtServer(level, level.damageSources().generic(), 2.0F);
            sp.sendSystemMessage(Component.translatable("lunaire.suffocate"), true);
        }

        // --- Chaleur du jour : brûlures en plein soleil sans combinaison complète
        if (!habitat && day && sky && suit < 4) {
            sp.hurtServer(level, level.damageSources().onFire(), suit >= 2 ? 1.0F : 2.0F);
            sp.setRemainingFireTicks(40);
        }
        // --- Froid de la nuit : sauf à proximité d'un radiateur allumé
        if (!habitat && !day && !Machines.litRadiatorNear(level, pos, 6)) {
            sp.setTicksFrozen(Math.min(sp.getTicksRequiredToFreeze() + 20, sp.getTicksFrozen() + 40));
            if (tick % 40 == 0) {
                sp.hurtServer(level, level.damageSources().freeze(), suit >= 4 ? 0.5F : 1.0F);
            }
            server.getCommands().performPrefixedCommand(
                    server.createCommandSourceStack().withSuppressedOutput(),
                    "effect give " + sp.getStringUUID() + " minecraft:slowness 3 0 true");
        }

        // --- Apparition des créatures (toutes les 10 s)
        if (tick % 200 == 0) {
            spawnCreatures(server, sp, level, day);
        }
    }

    private static void spawnCreatures(MinecraftServer server, ServerPlayer sp, ServerLevel level, boolean day) {
        var rng = level.getRandom();
        var src = server.createCommandSourceStack().withSuppressedOutput();
        if (level.getEntitiesOfClass(net.minecraft.world.entity.monster.Monster.class,
                sp.getBoundingBox().inflate(60.0)).size() > 10) {
            return;
        }
        int attempts = 4;
        while (attempts-- > 0) {
            int dx = (rng.nextBoolean() ? 1 : -1) * (14 + rng.nextInt(22));
            int dz = (rng.nextBoolean() ? 1 : -1) * (14 + rng.nextInt(22));
            BlockPos start = sp.blockPosition().offset(dx, 8, dz);
            BlockPos ground = null;
            for (int y = 0; y < 24; y++) {
                BlockPos p = start.below(y);
                if (!level.getBlockState(p).getCollisionShape(level, p).isEmpty()
                        && level.getBlockState(p.above()).getCollisionShape(level, p.above()).isEmpty()) {
                    ground = p.above();
                    break;
                }
            }
            if (ground == null) {
                continue;
            }
            boolean sunlit = day && level.canSeeSky(ground);
            if (!sunlit && rng.nextInt(4) != 0 && !level.canSeeSky(ground)) {
                // Sélénites : en groupe, dans l'obscurité (grottes, ombres)
                int n = 2 + rng.nextInt(3);
                for (int i = 0; i < n; i++) {
                    server.getCommands().performPrefixedCommand(src, "execute in " + dimId(level)
                            + " run summon lunaire:selenite " + (ground.getX() + i) + " " + ground.getY() + " " + ground.getZ());
                }
                return;
            }
            if (sunlit && rng.nextInt(3) == 0) {
                server.getCommands().performPrefixedCommand(src, "execute in " + dimId(level)
                        + " run summon lunaire:dust_golem " + ground.getX() + " " + ground.getY() + " " + ground.getZ());
                return;
            }
        }
    }

    private static String dimId(ServerLevel level) {
        String s = level.dimension().toString(); // ResourceKey[minecraft:dimension / lunaire:moon]
        return s.substring(s.indexOf('/') + 1, s.length() - 1).trim();
    }
}
