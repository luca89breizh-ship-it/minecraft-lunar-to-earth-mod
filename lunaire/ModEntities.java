package fr.lunaire.fabric.content;

import fr.lunaire.Lunaire;
import fr.lunaire.fabric.entity.DustGolem;
import fr.lunaire.fabric.entity.Selenite;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricDefaultAttributeRegistry;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;

public final class ModEntities {
    private ModEntities() {}

    public static final EntityType<Selenite> SELENITE = register("selenite",
            EntityType.Builder.of(Selenite::new, MobCategory.MONSTER).sized(0.6F, 1.95F).clientTrackingRange(8));
    public static final EntityType<DustGolem> DUST_GOLEM = register("dust_golem",
            EntityType.Builder.of(DustGolem::new, MobCategory.MONSTER).sized(1.0F, 2.4F).clientTrackingRange(8));

    private static <T extends net.minecraft.world.entity.Entity> EntityType<T> register(String name, EntityType.Builder<T> builder) {
        ResourceKey<EntityType<?>> key = ResourceKey.create(Registries.ENTITY_TYPE, Lunaire.id(name));
        EntityType<T> type = builder.build(key);
        return Registry.register(BuiltInRegistries.ENTITY_TYPE, key, type);
    }

    public static void init() {
        FabricDefaultAttributeRegistry.register(SELENITE, Selenite.attributes());
        FabricDefaultAttributeRegistry.register(DUST_GOLEM, DustGolem.attributes());
    }
}
