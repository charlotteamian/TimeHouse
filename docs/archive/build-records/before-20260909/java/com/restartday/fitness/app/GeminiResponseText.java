package com.restartday.fitness.app;

/** Extracts the first complete JSON value from a Gemini text response. */
final class GeminiResponseText {

    private GeminiResponseText() {
    }

    static String normalizeJson(String text) {
        String clean = text == null ? "" : text.trim();
        if (clean.startsWith("```")) {
            int firstLine = clean.indexOf('\n');
            int lastFence = clean.lastIndexOf("```");
            if (firstLine >= 0 && lastFence > firstLine) {
                clean = clean.substring(firstLine + 1, lastFence).trim();
            }
        }

        for (int start = 0; start < clean.length(); start++) {
            char opening = clean.charAt(start);
            if (opening != '{' && opening != '[') {
                continue;
            }
            int end = findJsonEnd(clean, start);
            if (end > start) {
                return clean.substring(start, end + 1).trim();
            }
        }
        return clean;
    }

    private static int findJsonEnd(String text, int start) {
        int objectDepth = 0;
        int arrayDepth = 0;
        boolean inString = false;
        boolean escaped = false;
        for (int i = start; i < text.length(); i++) {
            char current = text.charAt(i);
            if (inString) {
                if (escaped) {
                    escaped = false;
                } else if (current == '\\') {
                    escaped = true;
                } else if (current == '"') {
                    inString = false;
                }
                continue;
            }
            if (current == '"') {
                inString = true;
            } else if (current == '{') {
                objectDepth++;
            } else if (current == '}') {
                objectDepth--;
            } else if (current == '[') {
                arrayDepth++;
            } else if (current == ']') {
                arrayDepth--;
            }
            if (objectDepth < 0 || arrayDepth < 0) {
                return -1;
            }
            if (objectDepth == 0 && arrayDepth == 0) {
                return i;
            }
        }
        return -1;
    }
}
