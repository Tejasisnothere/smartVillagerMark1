package net.tejas.tutorialmod.events;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.event.entity.player.AttackEntityEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.tejas.tutorialmod.API;

import java.util.concurrent.CompletableFuture;

@Mod.EventBusSubscriber(modid = "tutorialmod") // IMPORTANT: no Dist.CLIENT here
public class ServerEvents {

    @SubscribeEvent
    public static void onChat(ServerChatEvent event) {

        String message = event.getMessage().getString();
        String playerName = event.getUsername();
        String uuid = event.getPlayer().getUUID().toString();
        Player player = event.getPlayer();
        System.out.println("[" + uuid + "] " + playerName + ": " + message);

        CompletableFuture<String> reply = API.sendJSON(message, uuid);
        System.out.println(reply);

        reply.thenAccept(response -> {
            player.getServer().execute(() -> {
                player.sendSystemMessage(
                        net.minecraft.network.chat.Component.literal("Villager: " + response)
                );
            });
        });
    }

    @SubscribeEvent
    public static void onAttack(AttackEntityEvent event) {

        if (event.getTarget() instanceof LivingEntity target) {

            Player player = event.getEntity();

            System.out.println(
                    player.getName().getString()
                            + " attacked "
                            + target.getName().getString()
            );

            System.out.println("Target ID: " + target.getId());
        }
    }

    @SubscribeEvent
    public static void onRightClickEntity(PlayerInteractEvent.EntityInteract event) {
        if (event.getLevel().isClientSide()) return;
        if (event.getHand() != InteractionHand.MAIN_HAND) return;
        Player player = event.getEntity();
        Entity target = event.getTarget();



        System.out.println(
                player.getName().getString()
                        + " right-clicked "
                        + target.getName().getString()
        );

        CompletableFuture<String> reply = API.selectVillager(player.getUUID().toString(),target.getUUID().toString());


        reply.thenAccept(response -> {
            player.getServer().execute(() -> {
                player.sendSystemMessage(
                        net.minecraft.network.chat.Component.literal("Villager: " + response)
                );
            });
        });
    }
}