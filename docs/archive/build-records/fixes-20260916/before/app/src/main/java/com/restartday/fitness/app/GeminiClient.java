package com.restartday.fitness.app;

import android.os.Handler;
import android.os.Looper;
import android.util.Base64;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

/**
 * Minimal client for Google's Gemini generateContent REST endpoint.
 *
 * The request runs on a background thread; the callback is delivered on the main thread.
 * Any failure (no network, bad key, rate limit, blocked/empty response) is surfaced through
 * {@link Callback#onError} so the caller can fall back to the local recommender.
 */
final class GeminiClient {

    interface Callback {
        void onResult(String text);

        void onError(String message);

        default void onModelFallback(String requestedModel, String fallbackModel) {
            // Callers that persist model settings can override this hook.
        }
    }

    private static final class RequestResult {
        final String text;
        final String requestedModel;
        final String fallbackModel;

        RequestResult(String text, String requestedModel, String fallbackModel) {
            this.text = text;
            this.requestedModel = requestedModel;
            this.fallbackModel = fallbackModel;
        }

        boolean usedFallback() {
            return fallbackModel != null && fallbackModel.length() > 0;
        }
    }

    private static final class ApiException extends RuntimeException {
        final int statusCode;

        ApiException(int statusCode, String message) {
            super(message);
            this.statusCode = statusCode;
        }
    }

    private final Handler main = new Handler(Looper.getMainLooper());

    void generate(final String apiKey, final String model, final String prompt, final Callback callback) {
        generate(apiKey, model, prompt, null, null, callback);
    }

    void generate(final String apiKey, final String model, final String prompt,
            final byte[] imageBytes, final String imageMimeType, final Callback callback) {
        generate(apiKey, model, prompt, imageBytes, imageMimeType, false, false, callback);
    }

    void generateWithGoogleSearch(final String apiKey, final String model, final String prompt,
            final Callback callback) {
        generate(apiKey, model, prompt, null, null, true, false, callback);
    }

    void generateWithUrlContext(final String apiKey, final String model, final String prompt,
            final Callback callback) {
        generate(apiKey, model, prompt, null, null, false, true, callback);
    }

    private void generate(final String apiKey, final String model, final String prompt,
            final byte[] imageBytes, final String imageMimeType,
            final boolean googleSearch, final boolean urlContext, final Callback callback) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    final RequestResult result = request(apiKey, model, prompt, imageBytes, imageMimeType,
                            googleSearch, urlContext);
                    main.post(new Runnable() {
                        @Override
                        public void run() {
                            if (result.usedFallback()) {
                                callback.onModelFallback(result.requestedModel, result.fallbackModel);
                            }
                            callback.onResult(result.text);
                        }
                    });
                } catch (Exception e) {
                    final String message = e.getMessage() == null ? "网络错误" : e.getMessage();
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

    private RequestResult request(String apiKey, String model, String prompt,
            byte[] imageBytes, String imageMimeType, boolean googleSearch, boolean urlContext) throws Exception {
        String cleanModel = GeminiModelName.normalize(model);
        try {
            return new RequestResult(requestOnce(apiKey, cleanModel, prompt, imageBytes, imageMimeType,
                    googleSearch, urlContext), cleanModel, null);
        } catch (ApiException error) {
            boolean canFallback = error.statusCode == 404
                    && !GeminiModelName.DEFAULT_MODEL.equals(cleanModel);
            if (!canFallback) {
                throw error;
            }
            String text = requestOnce(apiKey, GeminiModelName.DEFAULT_MODEL, prompt, imageBytes, imageMimeType,
                    googleSearch, urlContext);
            return new RequestResult(text, cleanModel, GeminiModelName.DEFAULT_MODEL);
        }
    }

    private String requestOnce(String apiKey, String cleanModel, String prompt,
            byte[] imageBytes, String imageMimeType, boolean googleSearch, boolean urlContext) throws Exception {
        String endpoint = "https://generativelanguage.googleapis.com/v1beta/models/"
                + cleanModel + ":generateContent";

        JSONArray parts = new JSONArray();
        if (imageBytes != null && imageBytes.length > 0) {
            JSONObject inlineData = new JSONObject();
            inlineData.put("mimeType", imageMimeType == null || imageMimeType.length() == 0
                    ? "image/jpeg" : imageMimeType);
            inlineData.put("data", Base64.encodeToString(imageBytes, Base64.NO_WRAP));
            JSONObject imagePart = new JSONObject();
            imagePart.put("inlineData", inlineData);
            parts.put(imagePart);
        }
        JSONObject textPart = new JSONObject();
        textPart.put("text", prompt);
        parts.put(textPart);
        JSONObject content = new JSONObject();
        content.put("parts", parts);
        JSONArray contents = new JSONArray();
        contents.put(content);
        JSONObject generationConfig = new JSONObject();
        generationConfig.put("temperature", 0.7);
        // Gemini 2.x search grounding cannot always be combined with structured output.
        // Tool prompts still explicitly request JSON, and extractText() normalizes fences/prose.
        if (!googleSearch && !urlContext) {
            generationConfig.put("responseMimeType", "application/json");
        }
        JSONObject body = new JSONObject();
        body.put("contents", contents);
        body.put("generationConfig", generationConfig);
        if (googleSearch || urlContext) {
            JSONArray tools = new JSONArray();
            if (googleSearch) {
                JSONObject search = new JSONObject();
                search.put("google_search", new JSONObject());
                tools.put(search);
            }
            if (urlContext) {
                JSONObject context = new JSONObject();
                context.put("url_context", new JSONObject());
                tools.put(context);
            }
            body.put("tools", tools);
        }

        HttpURLConnection conn = (HttpURLConnection) new URL(endpoint).openConnection();
        try {
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            conn.setRequestProperty("x-goog-api-key", apiKey.trim());
            conn.setConnectTimeout(12000);
            conn.setReadTimeout(imageBytes != null && imageBytes.length > 0 ? 45000 : 25000);
            conn.setDoOutput(true);
            OutputStream out = conn.getOutputStream();
            try {
                out.write(body.toString().getBytes(StandardCharsets.UTF_8));
            } finally {
                out.close();
            }
            int code = conn.getResponseCode();
            boolean ok = code >= 200 && code < 300;
            InputStream is = ok ? conn.getInputStream() : conn.getErrorStream();
            String response = is == null ? "" : readAll(is);
            if (!ok) {
                throw new ApiException(code, describeError(code, response, cleanModel, googleSearch));
            }
            return extractText(response);
        } finally {
            conn.disconnect();
        }
    }

    private String extractText(String response) throws Exception {
        JSONObject root = new JSONObject(response);
        JSONArray candidates = root.optJSONArray("candidates");
        if (candidates == null || candidates.length() == 0) {
            JSONObject feedback = root.optJSONObject("promptFeedback");
            String blockReason = feedback == null ? "" : feedback.optString("blockReason", "");
            throw new RuntimeException(blockReason.length() > 0 ? "内容被拦截：" + blockReason : "模型没有返回内容");
        }
        JSONObject content = candidates.getJSONObject(0).optJSONObject("content");
        if (content == null) {
            throw new RuntimeException("模型返回为空");
        }
        JSONArray parts = content.optJSONArray("parts");
        StringBuilder answer = new StringBuilder();
        StringBuilder allText = new StringBuilder();
        if (parts != null) {
            for (int i = 0; i < parts.length(); i++) {
                JSONObject part = parts.getJSONObject(i);
                String partText = part.optString("text");
                allText.append(partText);
                if (!part.optBoolean("thought", false)) {
                    answer.append(partText);
                }
            }
        }
        String text = (answer.length() > 0 ? answer : allText).toString().trim();
        if (text.length() == 0) {
            throw new RuntimeException("模型返回为空");
        }
        return GeminiResponseText.normalizeJson(text);
    }

    private String describeError(int code, String response, String model, boolean googleSearch) {
        String detail = "";
        try {
            JSONObject error = new JSONObject(response).optJSONObject("error");
            if (error != null) {
                detail = error.optString("message", "");
            }
        } catch (Exception ignored) {
            // Non-JSON error body; fall back to the raw status code.
        }
        if (detail.length() > 140) {
            detail = detail.substring(0, 140);
        }
        if (code == 400 || code == 403) {
            return "API Key 无效或无权限（" + code + "）" + (detail.length() > 0 ? "：" + detail : "");
        }
        if (code == 429) {
            if (googleSearch) {
                return "Google Search 当前无可用额度，请检查或启用该 Key 所属项目的结算（429）";
            }
            return "已达免费额度上限，请稍后再试（429）";
        }
        if (code == 404) {
            return "模型不可用（404）：" + model + "。请改用 " + GeminiModelName.DEFAULT_MODEL;
        }
        return "接口错误 " + code + (detail.length() > 0 ? "：" + detail : "");
    }

    private String readAll(InputStream is) throws Exception {
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        byte[] chunk = new byte[8192];
        int read;
        while ((read = is.read(chunk)) != -1) {
            buffer.write(chunk, 0, read);
        }
        is.close();
        return new String(buffer.toByteArray(), StandardCharsets.UTF_8);
    }
}
