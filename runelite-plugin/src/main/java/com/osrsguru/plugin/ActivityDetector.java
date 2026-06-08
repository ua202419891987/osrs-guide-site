package com.osrsguru.plugin;

import net.runelite.api.*;
import net.runelite.api.coords.WorldPoint;
import java.util.*;

/**
 * Detects what the player is currently doing in-game
 * and suggests relevant guides from osrsguru.com.
 */
public class ActivityDetector {

    // Boss region IDs → guide slugs
    private static final Map<Integer, String> BOSS_REGIONS = new HashMap<>();
    // Slayer NPC IDs → guide slugs
    private static final Map<Integer, String> SLAYER_NPCS = new HashMap<>();

    static {
        // Boss rooms (approximate region IDs)
        BOSS_REGIONS.put(9023, "osrs-how-to-beat-zulrah-beginners-rotation");           // Zulrah
        BOSS_REGIONS.put(11345, "osrs-low-gear-setup-vorkath-guide");                    // Vorkath
        BOSS_REGIONS.put(12887, "osrs-chambers-of-xeric-loot-profit-guide");             // CoX lobby
        BOSS_REGIONS.put(14674, "osrs-dagannoth-kings-guide-2026");                      // DKs
        BOSS_REGIONS.put(11346, "osrs-fire-cape-jad-guide-2026");                        // Fight Caves
        BOSS_REGIONS.put(13214, "osrs-phantom-muspah-guide-2026");                       // Phantom Muspah
        BOSS_REGIONS.put(13127, "osrs-royal-titans-guide-2026");                         // Royal Titans
        BOSS_REGIONS.put(4286,  "osrs-grotesque-guardians-guide-low-stats");             // Grotesque Guardians

        // Common Slayer NPCs
        SLAYER_NPCS.put(415,  "Abyssal Demon — guides/osrs-1-99-slayer-guide-2026");
        SLAYER_NPCS.put(7398, "Nechryael — guides/osrs-mid-game-breakthrough-guide-2026");
        SLAYER_NPCS.put(7404, "Gargoyle — guides/osrs-money-making-beginner-2026");
        SLAYER_NPCS.put(2085, "Hellhound — guides/osrs-1-99-slayer-guide-2026");
    }

    private final Client client;

    public ActivityDetector(Client client) {
        this.client = client;
    }

    /**
     * Detect what the player is doing and return a guide recommendation.
     */
    public String detectActivity() {
        Player player = client.getLocalPlayer();
        if (player == null) return null;

        WorldPoint loc = player.getWorldLocation();
        int regionId = loc.getRegionID();

        // Check if in a boss region
        if (BOSS_REGIONS.containsKey(regionId)) {
            String guideSlug = BOSS_REGIONS.get(regionId);
            return "https://osrsguru.com/guides/" + guideSlug + ".html";
        }

        // Check if fighting a Slayer NPC
        Actor interacting = player.getInteracting();
        if (interacting instanceof NPC) {
            NPC npc = (NPC) interacting;
            if (SLAYER_NPCS.containsKey(npc.getId())) {
                return SLAYER_NPCS.get(npc.getId());
            }
        }

        return null; // No specific activity detected
    }

    /**
     * Get a friendly label for what the player is doing.
     */
    public String getActivityLabel() {
        Player player = client.getLocalPlayer();
        if (player == null) return "Idle";

        Actor interacting = player.getInteracting();
        if (interacting instanceof NPC) {
            NPC npc = (NPC) interacting;
            String name = npc.getName();
            return name != null ? "Fighting " + name : "In combat";
        }

        WorldPoint loc = player.getWorldLocation();
        if (BOSS_REGIONS.containsKey(loc.getRegionID())) {
            return "In boss area";
        }

        return "Exploring";
    }
}
