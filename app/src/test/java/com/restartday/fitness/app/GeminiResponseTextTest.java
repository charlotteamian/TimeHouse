package com.restartday.fitness.app;

public final class GeminiResponseTextTest {
    public static void main(String[] args) {
        assertEquals("{\"ids\":[\"a\"]}", GeminiResponseText.normalizeJson(
                "```json\n{\"ids\":[\"a\"]}\n```"));
        assertEquals("{\"ids\":[\"a\"]}", GeminiResponseText.normalizeJson(
                "{\"ids\":[\"a\"]}{\"ids\":[\"b\"]}"));
        assertEquals("{\"reason\":\"保留字符串里的 } 和 [ 字符\"}", GeminiResponseText.normalizeJson(
                "说明：{\"reason\":\"保留字符串里的 } 和 [ 字符\"} 尾注"));
        assertEquals("plain text", GeminiResponseText.normalizeJson(" plain text "));
        System.out.println("GeminiResponseTextTest: all tests passed");
    }

    private static void assertEquals(String expected, String actual) {
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + " but was " + actual);
        }
    }
}
