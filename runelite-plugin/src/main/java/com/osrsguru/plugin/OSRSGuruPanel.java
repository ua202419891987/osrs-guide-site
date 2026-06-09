package com.osrsguru.plugin;

import net.runelite.client.ui.PluginPanel;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Side panel UI for OSRS Guru AI Plugin.
 *
 * Layout:
 * ┌──────────────────────────┐
 * │  🔍 [Search input field] │
 * │  [Ask] button            │
 * ├──────────────────────────┤
 * │  📋 Activity: Fighting.. │
 * │  → [Guide link]          │
 * ├──────────────────────────┤
 * │  💡 AI Answer:           │
 * │  (scrollable text area)  │
 * ├──────────────────────────┤
 * │  💰 Price Check:         │
 * │  [Item name] [Check]     │
 * └──────────────────────────┘
 */
public class OSRSGuruPanel extends PluginPanel {

    private static final Color BG_COLOR = new Color(39, 33, 26);      // Dark brown
    private static final Color GOLD = new Color(212, 175, 55);
    private static final Color TEXT_COLOR = new Color(232, 213, 181);
    private static final Color INPUT_BG = new Color(59, 38, 21);

    private final OSRSGuruApiClient apiClient;
    private final ActivityDetector activityDetector;
    private final OSRSGuruPlugin plugin;

    private JTextField searchField;
    private JButton searchButton;
    private JTextArea answerArea;
    private JLabel activityLabel;
    private JLabel guideLink;
    private JTextField priceField;
    private JButton priceButton;

    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    public OSRSGuruPanel(OSRSGuruApiClient apiClient, ActivityDetector activityDetector, OSRSGuruPlugin plugin) {
        this.apiClient = apiClient;
        this.activityDetector = activityDetector;
        this.plugin = plugin;

        setLayout(new BorderLayout(0, 8));
        setBackground(BG_COLOR);
        setBorder(new EmptyBorder(10, 10, 10, 10));

        // ── Top: Search ──
        JPanel searchPanel = new JPanel(new BorderLayout(5, 0));
        searchPanel.setBackground(BG_COLOR);
        searchField = new JTextField();
        searchField.setBackground(INPUT_BG);
        searchField.setForeground(GOLD);
        searchField.setCaretColor(GOLD);
        searchField.putClientProperty("JTextField.placeholderText", "Ask about OSRS...");
        searchButton = new JButton("Ask");
        styleButton(searchButton);
        searchPanel.add(searchField, BorderLayout.CENTER);
        searchPanel.add(searchButton, BorderLayout.EAST);
        add(searchPanel, BorderLayout.NORTH);

        // ── Center: Answer area + Activity ──
        JPanel centerPanel = new JPanel(new BorderLayout(0, 5));
        centerPanel.setBackground(BG_COLOR);

        activityLabel = new JLabel(" ");
        activityLabel.setForeground(new Color(200, 180, 150));
        activityLabel.setFont(new Font("SansSerif", Font.ITALIC, 11));
        centerPanel.add(activityLabel, BorderLayout.NORTH);

        guideLink = new JLabel(" ");
        guideLink.setForeground(new Color(100, 180, 255));
        guideLink.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        guideLink.setFont(new Font("SansSerif", Font.PLAIN, 11));
        centerPanel.add(guideLink, BorderLayout.CENTER);

        answerArea = new JTextArea();
        answerArea.setEditable(false);
        answerArea.setLineWrap(true);
        answerArea.setWrapStyleWord(true);
        answerArea.setBackground(new Color(30, 25, 20));
        answerArea.setForeground(TEXT_COLOR);
        answerArea.setFont(new Font("SansSerif", Font.PLAIN, 12));
        JScrollPane scrollPane = new JScrollPane(answerArea);
        scrollPane.setBorder(null);
        scrollPane.setPreferredSize(new Dimension(280, 350));
        centerPanel.add(scrollPane, BorderLayout.SOUTH);
        add(centerPanel, BorderLayout.CENTER);

        // ── Bottom: Price Check ──
        JPanel pricePanel = new JPanel(new BorderLayout(5, 0));
        pricePanel.setBackground(BG_COLOR);
        priceField = new JTextField();
        priceField.setBackground(INPUT_BG);
        priceField.setForeground(GOLD);
        priceField.setCaretColor(GOLD);
        priceField.putClientProperty("JTextField.placeholderText", "Item name...");
        priceButton = new JButton("Price");
        styleButton(priceButton);
        pricePanel.add(priceField, BorderLayout.CENTER);
        pricePanel.add(priceButton, BorderLayout.EAST);
        add(pricePanel, BorderLayout.SOUTH);

        // ── Event Handlers ──
        searchButton.addActionListener(e -> performSearch());
        searchField.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) performSearch();
            }
        });
        priceButton.addActionListener(e -> performPriceCheck());
        priceField.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) performPriceCheck();
            }
        });
        guideLink.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent e) {
                String url = guideLink.getText();
                if (url != null && url.startsWith("http")) {
                    plugin.openGuideUrl(url);
                }
            }
        });
    }

    private void performSearch() {
        String query = searchField.getText().trim();
        if (query.isEmpty()) return;

        setLoading(true);
        answerArea.setText("🤔 Asking OSRS Guru AI...\n");

        executor.submit(() -> {
            try {
                OSRSGuruApiClient.SearchResult result = apiClient.search(query);
                SwingUtilities.invokeLater(() -> {
                    answerArea.setText(formatAnswer(result));
                    setLoading(false);
                });
            } catch (IOException e) {
                SwingUtilities.invokeLater(() -> {
                    answerArea.setText("❌ Error: " + e.getMessage());
                    setLoading(false);
                });
            }
        });
    }

    private void performPriceCheck() {
        String item = priceField.getText().trim();
        if (item.isEmpty()) return;

        priceButton.setEnabled(false);
        priceButton.setText("...");

        executor.submit(() -> {
            try {
                String price = apiClient.checkPrice(item);
                SwingUtilities.invokeLater(() -> {
                    answerArea.setText("💰 Price Check: " + item + "\n\n" + price);
                    priceButton.setEnabled(true);
                    priceButton.setText("Price");
                });
            } catch (IOException e) {
                SwingUtilities.invokeLater(() -> {
                    answerArea.setText("❌ Price check failed: " + e.getMessage());
                    priceButton.setEnabled(true);
                    priceButton.setText("Price");
                });
            }
        });
    }

    /** Called by plugin when activity is detected */
    public void onActivityDetected(String activity, String guideUrl) {
        SwingUtilities.invokeLater(() -> {
            activityLabel.setText("📍 " + activity + " — guide available:");
            guideLink.setText(guideUrl);
        });
    }

    private String formatAnswer(OSRSGuruApiClient.SearchResult result) {
        StringBuilder sb = new StringBuilder();
        String sourceEmoji = switch (result.source) {
            case "osrsguru_rag" -> "📚";
            case "osrsguru_wiki" -> "📚📖";
            case "osrs_wiki" -> "📖";
            default -> "🤖";
        };
        sb.append(sourceEmoji).append(" ").append(result.answer).append("\n\n");
        sb.append("— via osrsguru.com");
        if (result.model != null) {
            sb.append(" (").append(result.model).append(")");
        }
        return sb.toString();
    }

    private void setLoading(boolean loading) {
        searchButton.setEnabled(!loading);
        searchButton.setText(loading ? "..." : "Ask");
    }

    private void styleButton(JButton button) {
        button.setBackground(new Color(212, 175, 55, 80));
        button.setForeground(GOLD);
        button.setBorder(BorderFactory.createLineBorder(GOLD, 1));
        button.setFocusPainted(false);
        button.setFont(new Font("SansSerif", Font.BOLD, 11));
    }
}
