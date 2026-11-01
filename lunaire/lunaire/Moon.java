package fr.lunaire.fabric;

import fr.lunaire.Lunaire;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.dimension.DimensionType;

public final class Moon {
    private Moon() {}

    public static final ResourceKey<DimensionType> MOON_TYPE =
            ResourceKey.create(Registries.DIMENSION_TYPE, Lunaire.id("moon"));

    public static boolean isMoon(Level level) {
        return level.dimensionTypeRegistration().is(MOON_TYPE);
    }

    public static boolean isMoon(Player player) {
        return isMoon(player.level());
    }
}
