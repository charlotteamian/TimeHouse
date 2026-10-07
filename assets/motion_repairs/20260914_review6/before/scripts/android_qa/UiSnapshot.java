package com.restartday.fitness.qa;

import android.app.Instrumentation;
import android.app.UiAutomation;
import android.os.Bundle;
import android.graphics.Rect;
import android.util.Base64;
import android.util.Xml;
import android.view.accessibility.AccessibilityNodeInfo;
import org.xmlpull.v1.XmlSerializer;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;

/** Read-only snapshot without waiting for a continuously running timer to become idle. */
public final class UiSnapshot extends Instrumentation {
    private String mediaNames;
    private String catalogIds;
    @Override public void onCreate(Bundle arguments) {
        super.onCreate(arguments);
        mediaNames = arguments == null ? null : arguments.getString("media");
        catalogIds = arguments == null ? null : arguments.getString("catalog");
        start();
    }
    @Override public void onStart() {
        Bundle result = new Bundle();
        try {
            if (catalogIds != null) {
                android.content.Context app = getContext().createPackageContext("com.restartday.fitness",
                        android.content.Context.CONTEXT_INCLUDE_CODE | android.content.Context.CONTEXT_IGNORE_SECURITY);
                ClassLoader loader = app.getClassLoader();
                Class<?> catalog = loader.loadClass("com.restartday.fitness.app.ExerciseDatasetLoader");
                Class<?> exercise = loader.loadClass("com.restartday.fitness.domain.Exercise");
                Class<?> tempo = loader.loadClass("com.restartday.fitness.domain.ExerciseTempo");
                java.util.List<?> exercises = (java.util.List<?>) catalog.getMethod("load", java.io.InputStream.class)
                        .invoke(null, app.getAssets().open("exercises_1324.json"));
                java.util.Set<String> wanted = new java.util.HashSet<>(java.util.Arrays.asList(catalogIds.split(",")));
                org.json.JSONObject rows = new org.json.JSONObject();
                for (Object item : exercises) {
                    String id = (String) exercise.getMethod("id").invoke(item);
                    if (!wanted.contains(id)) continue;
                    org.json.JSONObject row = new org.json.JSONObject();
                    row.put("name", exercise.getMethod("name").invoke(item));
                    row.put("patterns", new org.json.JSONArray((java.util.Collection<?>) exercise.getMethod("movementPatterns").invoke(item)));
                    row.put("primary", new org.json.JSONArray((java.util.Collection<?>) exercise.getMethod("primaryMuscles").invoke(item)));
                    row.put("isHold", tempo.getMethod("isHold", exercise).invoke(null, item));
                    row.put("perSide", tempo.getMethod("isPerSide", exercise).invoke(null, item));
                    for (String joint : new String[]{"shoulder", "lower_back", "knee"})
                        row.put(joint, exercise.getMethod("jointStress", String.class).invoke(item, joint).toString());
                    rows.put(id, row);
                }
                if (rows.length() != wanted.size()) throw new IllegalStateException("Missing requested catalog entries");
                result.putString("catalog", Base64.encodeToString(rows.toString().getBytes(StandardCharsets.UTF_8), Base64.NO_WRAP));
                finish(0, result);
                return;
            }
            if (mediaNames != null) {
                android.content.Context app = getContext().createPackageContext("com.restartday.fitness", 0);
                android.content.res.Resources resources = app.getResources();
                int count = 0;
                for (String name : mediaNames.split(",")) {
                    int id = resources.getIdentifier(name, "raw", "com.restartday.fitness");
                    if (id == 0) throw new IllegalStateException("Missing resource: " + name);
                    android.graphics.drawable.Drawable drawable = android.graphics.ImageDecoder.decodeDrawable(
                            android.graphics.ImageDecoder.createSource(resources, id));
                    if (!(drawable instanceof android.graphics.drawable.AnimatedImageDrawable))
                        throw new IllegalStateException("Not animated: " + name);
                    // Resources may scale intrinsic display size for the emulator density.
                    // Encoded 480x480 dimensions are checked separately by the asset validator.
                    if (drawable.getIntrinsicWidth() <= 0
                            || drawable.getIntrinsicWidth() != drawable.getIntrinsicHeight())
                        throw new IllegalStateException("Invalid display dimensions: " + name);
                    count++;
                }
                result.putInt("decodedAnimations", count);
                finish(0, result);
                return;
            }
            UiAutomation automation = getUiAutomation(UiAutomation.FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES);
            try { automation.waitForIdle(100, 3000); } catch (java.util.concurrent.TimeoutException ignored) { }
            AccessibilityNodeInfo root = automation.getRootInActiveWindow();
            for (int i = 0; root == null && i < 20; i++) {
                android.os.SystemClock.sleep(100);
                root = automation.getRootInActiveWindow();
            }
            if (root == null) throw new IllegalStateException("No active window");
            StringWriter writer = new StringWriter();
            XmlSerializer xml = Xml.newSerializer();
            xml.setOutput(writer);
            xml.startTag(null, "hierarchy");
            append(xml, root);
            xml.endTag(null, "hierarchy");
            xml.flush();
            result.putString("ui", Base64.encodeToString(writer.toString().getBytes(StandardCharsets.UTF_8), Base64.NO_WRAP));
            finish(0, result);
        } catch (Exception e) {
            result.putString("error", e.toString());
            finish(1, result);
        }
    }
    private void append(XmlSerializer xml, AccessibilityNodeInfo node) throws Exception {
        Rect rect = new Rect(); node.getBoundsInScreen(rect);
        xml.startTag(null, "node");
        xml.attribute(null, "text", node.getText() == null ? "" : node.getText().toString());
        xml.attribute(null, "content-desc", node.getContentDescription() == null ? "" : node.getContentDescription().toString());
        xml.attribute(null, "class", String.valueOf(node.getClassName()));
        xml.attribute(null, "clickable", String.valueOf(node.isClickable()));
        xml.attribute(null, "enabled", String.valueOf(node.isEnabled()));
        xml.attribute(null, "checkable", String.valueOf(node.isCheckable()));
        xml.attribute(null, "checked", String.valueOf(node.isChecked()));
        xml.attribute(null, "bounds", "[" + rect.left + "," + rect.top + "][" + rect.right + "," + rect.bottom + "]");
        for (int i = 0; i < node.getChildCount(); i++) {
            AccessibilityNodeInfo child = node.getChild(i);
            if (child != null) append(xml, child);
        }
        xml.endTag(null, "node");
    }
}
