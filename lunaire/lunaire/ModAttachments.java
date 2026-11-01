package fr.lunaire.fabric;

import com.mojang.serialization.Codec;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.network.codec.ByteBufCodecs;

public final class ModAttachments {
    private ModAttachments() {}

    public static final int O2_MAX = 3000; // dixièmes de seconde-équipement (voir Survival)

    /** Réserve d'oxygène du joueur (synchronisée avec le client pour la jauge). */
    public static final AttachmentType<Integer> OXYGEN = AttachmentRegistry.create(
            fr.lunaire.Lunaire.id("oxygen"),
            b -> b.initializer(() -> O2_MAX).persistent(Codec.INT)
                    .syncWith(ByteBufCodecs.INT, AttachmentSyncPredicate.targetOnly()));

    /** Intensité du tremblement d'écran pendant le décollage (ticks restants). */
    public static final AttachmentType<Integer> SHAKE = AttachmentRegistry.create(
            fr.lunaire.Lunaire.id("shake"),
            b -> b.initializer(() -> 0).syncWith(ByteBufCodecs.INT, AttachmentSyncPredicate.targetOnly()));

    /** 1 une fois la capsule de départ posée. */
    public static final AttachmentType<Integer> INTRO = AttachmentRegistry.create(
            fr.lunaire.Lunaire.id("intro"),
            b -> b.initializer(() -> 0).persistent(Codec.INT));

    public static void init() {}
}
