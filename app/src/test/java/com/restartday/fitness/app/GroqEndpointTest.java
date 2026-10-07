package com.restartday.fitness.app;

public final class GroqEndpointTest {
    public static void main(String[] args) {
        assertEquals(GroqEndpoint.DEFAULT_ENDPOINT, GroqEndpoint.normalize(null));
        assertEquals(GroqEndpoint.DEFAULT_ENDPOINT, GroqEndpoint.normalize("https://api.groq.com/openai/v1"));
        assertEquals(GroqEndpoint.DEFAULT_ENDPOINT, GroqEndpoint.normalize(
                "https://api.groq.com/openai/v1/chat/completions/"));
        assertTrue(GroqEndpoint.isSecure(GroqEndpoint.DEFAULT_ENDPOINT));
        assertTrue(!GroqEndpoint.isSecure("http://api.groq.com/openai/v1"));
        System.out.println("GroqEndpointTest: all tests passed");
    }

    private static void assertEquals(String expected, String actual) {
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + " but was " + actual);
        }
    }

    private static void assertTrue(boolean value) {
        if (!value) {
            throw new AssertionError("Expected true");
        }
    }
}
