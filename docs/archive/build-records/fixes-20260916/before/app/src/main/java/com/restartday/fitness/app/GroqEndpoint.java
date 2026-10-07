package com.restartday.fitness.app;

/** Normalizes Groq's OpenAI-compatible chat-completions endpoint. */
final class GroqEndpoint {

    static final String DEFAULT_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions";
    static final String DEFAULT_MODEL = "groq/compound-mini";

    private GroqEndpoint() {
    }

    static String normalize(String endpoint) {
        String value = endpoint == null ? "" : endpoint.trim();
        if (value.length() == 0) {
            return DEFAULT_ENDPOINT;
        }
        while (value.endsWith("/")) {
            value = value.substring(0, value.length() - 1);
        }
        if (value.endsWith("/openai/v1") || value.endsWith("/v1")) {
            value += "/chat/completions";
        }
        return value;
    }

    static boolean isSecure(String endpoint) {
        return normalize(endpoint).startsWith("https://");
    }
}
