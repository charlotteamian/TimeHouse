package com.restartday.fitness.app;

/** Normalizes model values copied from Google AI Studio or the Gemini Models API. */
final class GeminiModelName {

    static final String DEFAULT_MODEL = "gemini-3.5-flash";

    private GeminiModelName() {
    }

    static String normalize(String model) {
        String normalized = normalizeOptional(model);
        return normalized.length() == 0 ? DEFAULT_MODEL : normalized;
    }

    static String normalizeOptional(String model) {
        String value = model == null ? "" : model.trim();
        if (value.length() == 0) {
            return "";
        }

        int query = value.indexOf('?');
        if (query >= 0) {
            value = value.substring(0, query);
        }
        int fragment = value.indexOf('#');
        if (fragment >= 0) {
            value = value.substring(0, fragment);
        }
        int modelsPath = value.lastIndexOf("/models/");
        if (modelsPath >= 0) {
            value = value.substring(modelsPath + "/models/".length());
        } else if (value.startsWith("models/")) {
            value = value.substring("models/".length());
        }
        int method = value.indexOf(":generateContent");
        if (method >= 0) {
            value = value.substring(0, method);
        }
        while (value.startsWith("/")) {
            value = value.substring(1);
        }
        return value.trim();
    }
}
