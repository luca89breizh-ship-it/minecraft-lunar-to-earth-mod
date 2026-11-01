package fr.lunaire;

import net.minecraft.resources.Identifier;

/** Constantes partagées entre les versions Fabric et Forge. */
public final class Lunaire {
    public static final String MOD_ID = "lunaire";

    private Lunaire() {}

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }
}
