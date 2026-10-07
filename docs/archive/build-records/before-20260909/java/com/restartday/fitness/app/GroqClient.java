package com.restartday.fitness.app;

import android.os.Handler;
import android.os.Looper;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

/** Minimal client for Groq's OpenAI-compatible Compound systems. */
final class GroqClient {

    interface Callback {
        void onResult(String text);

        void onError(String message);
    }

    private final Handler main = new Handler(Looper.getMainLooper());

    void generate(final String apiKey, final String endpoint, final String model, final String prompt,
            final boolean visitWebsite, final Callback callback) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    final String result = request(apiKey, endpoint, model, prompt, visitWebsite);
                    main.post(new Runnable() {
                        @Override
                        public void run() {
                            callback.onResult(result);
                        }
                    });
                } catch (Exception error) {
                    final String message = error.getMessage() == null ? "网络错误" : error.getMessage();
                    main.post(new Runnable() {
                        @Override
                        public void run() {
                            callback.onError(message);
                        }
                    });
                }
            }
        }).start();
    }

    private String request(String apiKey, String endpoint, String model, String prompt,
            boolean visitWebsite) throws Exception {
        String cleanEndpoint = GroqEndpoint.normalize(endpoint);
        if (!GroqEndpoint.isSecure(cleanEndpoint)) {
            throw new RuntimeException("Groq API 地址必须使用 https://");
        }
        String cleanModel = model == null || model.trim().length() == 0
                ? GroqEndpoint.DEFAULT_MODEL : model.trim();

        JSONObject userMessage = new JSONObject();
        userMessage.put("role", "user");
        userMessage.put("content", prompt);
        JSONArray messages = new JSONArray();
        messages.put(userMessage);
        JSONObject body = new JSONObject();
        body.put("model", cleanModel);
        body.put("messages", messages);
        body.put("temperature", 0.3);
        JSONObject tools = new JSONObject();
        JSONArray enabledTools = new JSONArray();
        enabledTools.put(visitWebsite ? "visit_website" : "web_search");
        tools.put("enabled_tools", enabledTools);
        JSONObject compoundCustom = new JSONObject();
        compoundCustom.put("tools", tools);
        body.put("compound_custom", compoundCustom);

        HttpURLConnection connection = (HttpURLConnection) new URL(cleanEndpoint).openConnection();
        try {
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            connection.setRequestProperty("Authorization", "Bearer " + apiKey.trim());
            // The basic-search version is smaller and works within Groq's free-tier context limits.
            connection.setRequestProperty("Groq-Model-Version", visitWebsite ? "latest" : "2025-07-23");
            connection.setRequestProperty("Connection", "close");
            connection.setConnectTimeout(12000);
            connection.setReadTimeout(45000);
            connection.setDoOutput(true);
            OutputStream output = connection.getOutputStream();
            try {
                output.write(body.toString().getBytes(StandardCharsets.UTF_8));
            } finally {
                output.close();
            }
            int code = connection.getResponseCode();
            boolean ok = code >= 200 && code < 300;
            InputStream input = ok ? connection.getInputStream() : connection.getErrorStream();
            String response = input == null ? "" : readAll(input);
            if (!ok) {
                throw new RuntimeException(describeError(code, response));
            }
            JSONObject root = new JSONObject(response);
            JSONArray choices = root.optJSONArray("choices");
            if (choices == null || choices.length() == 0) {
                throw new RuntimeException("Groq 没有返回内容");
            }
            JSONObject message = choices.getJSONObject(0).optJSONObject("message");
            String text = message == null ? "" : message.optString("content", "").trim();
            if (text.length() == 0) {
                throw new RuntimeException("Groq 返回为空");
            }
            return GeminiResponseText.normalizeJson(text);
        } finally {
            connection.disconnect();
        }
    }

    private String describeError(int code, String response) {
        String detail = "";
        try {
            JSONObject error = new JSONObject(response).optJSONObject("error");
            if (error != null) {
                detail = error.optString("message", "");
            }
        } catch (Exception ignored) {
            // Use the status-only fallback below.
        }
        if (code == 401 || code == 403) {
            return "Groq API Key 无效或无权限（" + code + "）";
        }
        if (code == 429) {
            return "Groq 免费额度暂时用完，请等待额度恢复（429）";
        }
        if (detail.length() > 140) {
            detail = detail.substring(0, 140);
        }
        return "Groq 接口错误 " + code + (detail.length() > 0 ? "：" + detail : "");
    }

    private String readAll(InputStream input) throws Exception {
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        byte[] chunk = new byte[8192];
        int read;
        while ((read = input.read(chunk)) != -1) {
            buffer.write(chunk, 0, read);
        }
        input.close();
        return new String(buffer.toByteArray(), StandardCharsets.UTF_8);
    }
}
