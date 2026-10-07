package com.restartday.fitness.app;

public final class GeminiModelNameTest {
    public static void main(String[] args) {
        assertEquals("gemini-3.5-flash", GeminiModelName.normalize(null));
        assertEquals("gemini-2.5-flash", GeminiModelName.normalize("models/gemini-2.5-flash"));
        assertEquals("gemini-2.5-flash", GeminiModelName.normalize(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"));
        assertEquals("gemini-3.5-flash", GeminiModelName.normalizeOptional(
                " /models/gemini-3.5-flash:generateContent?key=redacted "));
        assertEquals("", GeminiModelName.normalizeOptional("  "));
        System.out.println("GeminiModelNameTest: all tests passed");
    }

    private static void assertEquals(String expected, String actual) {
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + " but was " + actual);
        }
    }
}
