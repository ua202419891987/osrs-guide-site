package com.osrsguru.plugin;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import okhttp3.*;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

/**
 * HTTP client for OSRS Guru RAG API.
 * Calls the three-layer AI pipeline: Local Guides → OSRS Wiki → LLM.
 */
public class OSRSGuruApiClient {

    private static final String API_BASE_URL = "https://osrs-rag-api.vercel.app";
    private static final MediaType JSON = MediaType.get("application/json; charset=utf-8");
    private final OkHttpClient httpClient;
    private final Gson gson;

    public OSRSGuruApiClient() {
        this.httpClient = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(25, TimeUnit.SECONDS)
                .build();
        this.gson = new Gson();
    }

    /**
     * Search the OSRS Guru knowledge base.
     *
     * @param query The player's question (e.g., "How to beat Vorkath?")
     * @return API response containing answer, source, model info
     */
    public SearchResult search(String query) throws IOException {
        String encodedQuery = java.net.URLEncoder.encode(query, "UTF-8");
        String url = API_BASE_URL + "/rag-api/search?q=" + encodedQuery;

        Request request = new Request.Builder()
                .url(url)
                .get()
                .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                return new SearchResult(
                    "⚠️ Unable to reach OSRS Guru AI. Check osrsguru.com in your browser.",
                    "error",
                    null
                );
            }

            JsonObject json = gson.fromJson(
                response.body() != null ? response.body().string() : "{}",
                JsonObject.class
            );

            return new SearchResult(
                json.has("answer") ? json.get("answer").getAsString() : "No answer found.",
                json.has("source") ? json.get("source").getAsString() : "unknown",
                json.has("model") ? json.get("model").getAsString() : null
            );
        }
    }

    /**
     * Quick GE price check for an item.
     * Uses the OSRS Wiki real-time price API via the RAG backend.
     */
    public String checkPrice(String itemName) throws IOException {
        String result = search("What is the current Grand Exchange price of " + itemName + "?");
        return result.answer;
    }

    /**
     * Search result container.
     */
    public static class SearchResult {
        public final String answer;
        public final String source;
        public final String model;

        public SearchResult(String answer, String source, String model) {
            this.answer = answer;
            this.source = source;
            this.model = model;
        }
    }
}
