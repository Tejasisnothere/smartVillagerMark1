package net.tejas.tutorialmod.events;

import net.minecraft.client.Minecraft;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.RenderGuiOverlayEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = "tutorialmod", value = Dist.CLIENT)
public class ClientEvents {

    @SubscribeEvent
    public static void onRender(RenderGuiOverlayEvent.Post event) {

        Minecraft mc = Minecraft.getInstance();

        if (mc.player == null) return;

        String msg =
                "X: " + (int) mc.player.getX() +
                        " Y: " + (int) mc.player.getY() +
                        " Z: " + (int) mc.player.getZ() +
                        " Dir: " + mc.player.getDirection();

        event.getGuiGraphics().drawString(
                mc.font,
                msg,
                10,
                10,
                0xFFFFFF
        );

        if (mc.mouseHandler.isLeftPressed()) {
            event.getGuiGraphics().drawString(mc.font, "LEFT CLICK", 10, 25, 0xFF0000);
        }

        if (mc.player.zza != 0 || mc.player.xxa != 0) {
            event.getGuiGraphics().drawString(mc.font, "MOVING", 10, 40, 0x00FF00);
        }
    }
}