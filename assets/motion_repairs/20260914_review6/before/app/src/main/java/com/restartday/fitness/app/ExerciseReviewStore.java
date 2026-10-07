package com.restartday.fitness.app;

import android.content.Context;
import android.net.Uri;
import com.restartday.fitness.domain.Exercise;
import com.restartday.fitness.domain.Intensity;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Editorial review is independent of provenance and recommendation safety checks. */
final class ExerciseReviewStore {
    private final Context context;
    private final Map<String, JSONObject> bundled = new HashMap<>();
    private final Map<String, String> rawHashes = new HashMap<>();
    private JSONObject personal = new JSONObject();
    String loadError = "";

    ExerciseReviewStore(Context context) { this.context = context; }

    void load(List<Exercise> exercises, String saved) {
        try { personal = new JSONObject(saved); }
        catch (Exception error) { loadError = "个人复核记录读取失败，暂按未复核处理"; }
        try {
            JSONObject root;
            try (InputStream in = context.getAssets().open("exercise_reviews.json")) {
                root = new JSONObject(new String(read(in), StandardCharsets.UTF_8));
            }
            try (InputStream in = context.getAssets().open(ExerciseDatasetLoader.ASSET_NAME)) {
                if (!root.getString("dataset_sha256").equals(hash(read(in)))) {
                    loadError = "动作资料已更新，内置复核需要重新确认";
                    return;
                }
            }
            Map<String, Exercise> byId = new HashMap<>();
            for (Exercise e : exercises) byId.put(e.id(), e);
            JSONArray rows = root.getJSONArray("reviewed");
            for (int i = 0; i < rows.length(); i++) {
                JSONObject row = rows.getJSONObject(i);
                Exercise e = byId.get(row.getString("id"));
                if (e == null || !row.getString("media_sha256").equals(mediaHash(e.media()))) continue;
                row.put("fingerprint", fingerprint(e, e.media()));
                row.put("approved", true);
                bundled.put(e.id(), row);
            }
            JSONArray pending = root.optJSONArray("pending");
            if (pending != null) for (int i = 0; i < pending.length(); i++) {
                JSONObject row = pending.getJSONObject(i);
                row.put("approved", false);
                row.put("reviewer", "本轮待办"); row.put("reviewed_at", "2026-09-13");
                bundled.put(row.getString("id"), row);
            }
        } catch (Exception error) { loadError = "内置复核清单读取失败，暂按未复核处理"; }
    }

    boolean reviewed(Exercise e, String media) {
        JSONObject row = record(e.id());
        return row != null && row.optBoolean("approved")
                && !mediaHash(media).isEmpty()
                && row.optString("fingerprint").equals(fingerprint(e, media));
    }

    String description(Exercise e, String media) {
        JSONObject row = record(e.id());
        if (row == null) return "未复核 · 待核对动作逻辑与示范";
        if (row.optBoolean("approved") && !reviewed(e, media)) return "未复核 · 资料或示范已变化，请重新核对";
        return (reviewed(e, media) ? "已复核" : "未复核") + " · "
                + row.optString("reviewed_at") + " · " + row.optString("reviewer")
                + "\n" + row.optString("note");
    }

    void set(Exercise e, String media, boolean approved, String note) throws Exception {
        if (approved && mediaHash(media).isEmpty()) throw new IllegalArgumentException("请先添加可读取的本地示范，再完成复核");
        JSONObject row = new JSONObject();
        row.put("approved", approved);
        row.put("fingerprint", fingerprint(e, media));
        row.put("reviewed_at", java.time.LocalDate.now().toString());
        row.put("reviewer", "本人复核");
        row.put("note", note);
        personal.put(e.id(), row);
    }

    String save() { return personal.toString(); }

    String source(Exercise e) {
        JSONObject row = record(e.id());
        return row == null ? "" : row.optString("source");
    }

    private JSONObject record(String id) {
        // A personal rejection always overrides an earlier bundled approval.
        return personal.has(id) ? personal.optJSONObject(id) : bundled.get(id);
    }

    private String fingerprint(Exercise e, String media) {
        StringBuilder b = new StringBuilder();
        for (Object value : new Object[]{e.id(), e.name(), e.targetRegions(), e.movementPatterns(),
                e.equipment(), e.primaryMuscles(), e.secondaryMuscles(), e.difficulty(),
                e.instructions(), e.commonMistakes(), e.substitutions(), e.evidenceStatus(), e.evidenceRefs(),
                e.jointStress("shoulder"), e.jointStress("lower_back"), e.jointStress("knee"),
                e.jointStress("elbow"), media, mediaHash(media)}) {
            String part = String.valueOf(value);
            b.append(part.length()).append(':').append(part);
        }
        for (Intensity intensity : Intensity.values()) b.append(e.prescription(intensity).compactLabel());
        return hash(b.toString().getBytes(StandardCharsets.UTF_8));
    }

    private String mediaHash(String media) {
        if (media == null || media.isEmpty()) return "";
        try {
            if (media.startsWith("raw:")) {
                if (rawHashes.containsKey(media)) return rawHashes.get(media);
                int id = context.getResources().getIdentifier(media.substring(4), "raw", context.getPackageName());
                if (id == 0) return "";
                try (InputStream in = context.getResources().openRawResource(id)) {
                    String value = hash(read(in)); rawHashes.put(media, value); return value;
                }
            }
            if (media.startsWith("file:") || media.startsWith("content:")) {
                try (InputStream in = context.getContentResolver().openInputStream(Uri.parse(media))) {
                    return in == null ? "" : hash(read(in));
                }
            }
        } catch (Exception ignored) { }
        return "";
    }

    private static byte[] read(InputStream in) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream(); byte[] buffer = new byte[8192]; int n;
        while ((n = in.read(buffer)) != -1) out.write(buffer, 0, n);
        return out.toByteArray();
    }

    private static String hash(byte[] bytes) {
        try {
            StringBuilder b = new StringBuilder();
            for (byte value : MessageDigest.getInstance("SHA-256").digest(bytes)) b.append(String.format("%02x", value & 255));
            return b.toString();
        } catch (Exception error) { throw new IllegalStateException(error); }
    }
}
