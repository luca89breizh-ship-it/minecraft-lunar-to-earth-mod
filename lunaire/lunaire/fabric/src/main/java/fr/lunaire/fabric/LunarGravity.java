package fr.lunaire.fabric;

import fr.lunaire.Lunaire;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.Level;

/** Gravité lunaire : /6 de la gravité normale, saut ajusté pour monter d'environ 4 blocs. */
public final class LunarGravity {
    public static final ResourceKey<Level> MOON = ResourceKey.create(Registries.DIMENSION, Lunaire.id("moon"));

    private static final Identifier GRAVITY_ID = Lunaire.id("lunar_gravity");
    private static final Identifier JUMP_ID = Lunaire.id("lunar_jump");

    private LunarGravity() {}

    public static void init() {
        ServerTickEvents.END_SERVER_TICK.register(server -> {
            for (ServerPlayer player : server.getPlayerList().getPlayers()) {
                update(player);
            }
        });
    }

    private static void update(ServerPlayer player) {
        boolean onMoon = player.level().dimension().equals(MOON);
        apply(player.getAttribute(Attributes.GRAVITY), GRAVITY_ID, -5.0 / 6.0, onMoon);
        apply(player.getAttribute(Attributes.JUMP_STRENGTH), JUMP_ID, -0.22, onMoon);
    }

    private static void apply(AttributeInstance attribute, Identifier id, double amount, boolean enabled) {
        if (attribute == null) {
            return;
        }
        boolean present = attribute.getModifier(id) != null;
        if (enabled && !present) {
            attribute.addTransientModifier(
                    new AttributeModifier(id, amount, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL));
        } else if (!enabled && present) {
            attribute.removeModifier(id);
        }
    }
}
