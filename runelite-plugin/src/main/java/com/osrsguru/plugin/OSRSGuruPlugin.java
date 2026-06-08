package com.osrsguru.plugin;

import lombok.extern.slf4j.Slf4j;
import net.runelite.api.*;
import net.runelite.api.events.GameTick;
import net.runelite.client.callback.ClientThread;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.ui.ClientToolbar;
import net.runelite.client.ui.NavigationButton;
import net.runelite.client.util.ImageUtil;

import javax.inject.Inject;
import javax.swing.*;
import java.awt.image.BufferedImage;
import java.io.IOException;

/**
 * OSRS Guru AI Plugin for RuneLite.
 *
 * Features:
 * - AI-powered search sidebar (connects to osrsguru.com RAG API)
 * - Auto-detects player activity and recommends relevant guides
 * - Quick GE price lookup
 * - Game overlay hints for boss mechanics
 */
@Slf4j
@PluginDescriptor(
    name = "OSRS Guru AI",
    description = "AI-powered OSRS guide assistant — ask questions, get boss tips, and check prices without leaving the game.",
    tags = {"ai", "guide", "wiki", "boss", "price", "osrsguru"}
)
public class OSRSGuruPlugin extends Plugin {

    @Inject
    private Client client;

    @Inject
    private ClientToolbar clientToolbar;

    @Inject
    private ClientThread clientThread;

    @Inject
    private ConfigManager configManager;

    private OSRSGuruPanel panel;
    private NavigationButton navButton;
    private ActivityDetector activityDetector;
    private OSRSGuruApiClient apiClient;

    // Activity tracking
    private String lastActivity = "";
    private int tickCounter = 0;
    private static final int ACTIVITY_CHECK_INTERVAL = 100; // ~10 seconds

    @Override
    protected void startUp() throws Exception {
        log.info("OSRS Guru AI Plugin started!");

        this.apiClient = new OSRSGuruApiClient();
        this.activityDetector = new ActivityDetector(client);

        // Create side panel
        this.panel = new OSRSGuruPanel(apiClient, activityDetector, this);

        // Create toolbar icon
        BufferedImage icon = ImageUtil.loadImageResource(
            getClass(), "/osrsguru-icon.png"
        );

        this.navButton = NavigationButton.builder()
            .tooltip("OSRS Guru AI Assistant")
            .icon(icon != null ? icon : createDefaultIcon())
            .priority(5)
            .panel(panel)
            .build();

        clientToolbar.addNavigation(navButton);
    }

    @Override
    protected void shutDown() throws Exception {
        log.info("OSRS Guru AI Plugin stopped!");
        clientToolbar.removeNavigation(navButton);
        panel = null;
    }

    @Subscribe
    public void onGameTick(GameTick event) {
        tickCounter++;
        if (tickCounter % ACTIVITY_CHECK_INTERVAL != 0) return;

        // Detect player activity and notify panel
        String guideUrl = activityDetector.detectActivity();
        String activityLabel = activityDetector.getActivityLabel();

        if (guideUrl != null && !activityLabel.equals(lastActivity)) {
            lastActivity = activityLabel;
            SwingUtilities.invokeLater(() -> {
                panel.onActivityDetected(activityLabel, guideUrl);
            });
        }
    }

    private BufferedImage createDefaultIcon() {
        // Fallback: 16x16 gold-colored icon
        BufferedImage img = new BufferedImage(16, 16, BufferedImage.TYPE_INT_ARGB);
        java.awt.Graphics2D g = img.createGraphics();
        g.setColor(new java.awt.Color(212, 175, 55)); // OSRS gold
        g.fillOval(0, 0, 15, 15);
        g.setColor(java.awt.Color.BLACK);
        g.setFont(new java.awt.Font("SansSerif", java.awt.Font.BOLD, 10));
        g.drawString("?", 4, 12);
        g.dispose();
        return img;
    }

    /** Panel callback: user clicked a guide link */
    public void openGuideUrl(String url) {
        // Open in browser via RuneLite utility
        net.runelite.client.util.LinkBrowser.browse(url);
    }
}
