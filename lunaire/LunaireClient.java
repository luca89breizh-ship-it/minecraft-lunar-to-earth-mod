package fr.lunaire.fabric.client;

import fr.lunaire.Lunaire;
import fr.lunaire.fabric.ModAttachments;
import fr.lunaire.fabric.Moon;
import fr.lunaire.fabric.content.ModEntities;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.resources.Identifier;

public final class LunaireClient implements ClientModInitializer {
    public static final ModelLayerLocation SELENITE_LAYER = new ModelLayerLocation(Lunaire.id("selenite"), "main");
    public static final ModelLayerLocation GOLEM_LAYER = new ModelLayerLocation(Lunaire.id("dust_golem"), "main");

    @Override
    public void onInitializeClient() {
        ModelLayerRegistry.registerModelLayer(SELENITE_LAYER,
                () -> LayerDefinition.create(HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F), 64, 64));
        ModelLayerRegistry.registerModelLayer(GOLEM_LAYER,
                () -> LayerDefinition.create(HumanoidModel.createMesh(new CubeDeformation(0.45F), 0.0F), 64, 64));
        EntityRendererRegistry.register(ModEntities.SELENITE, SeleniteRenderer::new);
        EntityRendererRegistry.register(ModEntities.DUST_GOLEM, DustGolemRenderer::new);

        HudElementRegistry.attachElementAfter(VanillaHudElements.INFO_BAR_FOREGROUND,
                Lunaire.id("oxygen_gauge"), LunaireClient::renderOxygen);

        // Tremblement d'écran pendant le décollage
        ClientTickEvents.END_CLIENT_TICK.register(mc -> {
            LocalPlayer p = mc.player;
            if (p == null) {
                return;
            }
            int shake = p.getAttachedOrCreate(ModAttachments.SHAKE);
            if (shake > 0) {
                float amp = 0.4F + shake * 0.15F;
                p.setYRot(p.getYRot() + (p.getRandom().nextFloat() - 0.5F) * amp);
                p.setXRot(p.getXRot() + (p.getRandom().nextFloat() - 0.5F) * amp);
            }
        });
    }

    private static int argb(int a, int r, int g, int b) {
        return (a << 24) | (r << 16) | (g << 8) | b;
    }

    private static void renderOxygen(GuiGraphicsExtractor g, DeltaTracker tracker) {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer p = mc.player;
        if (p == null || !Moon.isMoon(p)) {
            return;
        }
        int o2 = p.getAttachedOrCreate(ModAttachments.OXYGEN);
        float ratio = Math.max(0F, Math.min(1F, o2 / (float) ModAttachments.O2_MAX));
        int w = 81, h = 7;
        int x = g.guiWidth() / 2 + 10;
        int y = g.guiHeight() - 52;
        g.fill(x - 1, y - 1, x + w + 1, y + h + 1, argb(255, 20, 20, 30));
        int color = ratio > 0.25F ? argb(255, 80, 200, 255) : argb(255, 255, 70, 70);
        g.fill(x, y, x + (int) (w * ratio), y + h, color);
        g.text(mc.font, "O2 " + (int) (ratio * 100) + "%", x, y - 10, argb(255, 255, 255, 255));
    }
}
