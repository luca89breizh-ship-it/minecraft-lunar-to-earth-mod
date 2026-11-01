package fr.lunaire.fabric;

import fr.lunaire.fabric.content.ModBlocks;
import fr.lunaire.fabric.content.ModItems;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;

/** Décollage : compte à rebours de 10 s, tremblement d'écran, arrivée en parachute dans l'Overworld. */
public final class Launch {
    private Launch() {}

    private static final Map<UUID, Integer> COUNTDOWN = new HashMap<>();

    public static void init() {
        ServerTickEvents.END_SERVER_TICK.register(Launch::tick);
    }

    private static boolean hasBlueprint(ServerPlayer sp) {
        Inventory inv = sp.getInventory();
        for (int i = 0; i < inv.getContainerSize(); i++) {
            if (inv.getItem(i).is(ModItems.ROCKET_BLUEPRINT)) {
                return true;
            }
        }
        return false;
    }

    public static void tryStart(ServerPlayer sp, ItemStack held) {
        if (COUNTDOWN.containsKey(sp.getUUID())) {
            return;
        }
        if (!held.is(ModItems.REENTRY_MODULE) || !hasBlueprint(sp)) {
            sp.sendSystemMessage(Component.translatable("lunaire.no_blueprint"));
            return;
        }
        held.shrink(1);
        COUNTDOWN.put(sp.getUUID(), 200);
        sp.sendSystemMessage(Component.translatable("lunaire.launch"));
    }

    private static void tick(MinecraftServer server) {
        if (COUNTDOWN.isEmpty()) {
            return;
        }
        Iterator<Map.Entry<UUID, Integer>> it = COUNTDOWN.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<UUID, Integer> e = it.next();
            ServerPlayer sp = server.getPlayerList().getPlayer(e.getKey());
            if (sp == null) {
                it.remove();
                continue;
            }
            int t = e.getValue() - 1;
            e.setValue(t);
            if (t % 20 == 0 && t > 0) {
                sp.sendSystemMessage(Component.literal("T-" + (t / 20)), true);
            }
            if (t < 120) {
                sp.setAttached(ModAttachments.SHAKE, t > 0 ? 1 + (120 - t) / 12 : 0);
            }
            if (t <= 0) {
                it.remove();
                sp.setAttached(ModAttachments.SHAKE, 0);
                departToEarth(server, sp);
            }
        }
    }

    private static void departToEarth(MinecraftServer server, ServerPlayer sp) {
        String target = sp.level().dimension().toString().contains("minecraft:overworld")
                ? "lunaire:earth" : "minecraft:overworld";
        String id = sp.getStringUUID();
        var src = server.createCommandSourceStack().withSuppressedOutput();
        var cmds = server.getCommands();
        cmds.performPrefixedCommand(src, "execute in " + target + " run tp " + id + " 0 330 0");
        cmds.performPrefixedCommand(src, "effect give " + id + " minecraft:slow_falling 160 0 true");
        cmds.performPrefixedCommand(src, "effect give " + id + " minecraft:resistance 30 4 true");
        sp.setAttached(ModAttachments.OXYGEN, ModAttachments.O2_MAX);
        sp.sendSystemMessage(Component.literal("Bienvenue à la maison. Parachute déployé !"));
    }
}
