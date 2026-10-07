package com.restartday.fitness.app;

import android.content.Context;

import com.restartday.fitness.domain.FoodGroup;
import com.restartday.fitness.domain.MealPreset;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/** 读取 assets/quick_meals_cn.json 的「记一餐」快速录入预设。 */
public final class QuickMealLoader {

    private QuickMealLoader() {
    }

    public static List<MealPreset> load(Context context) {
        List<MealPreset> result = new ArrayList<MealPreset>();
        try {
            InputStream stream = context.getAssets().open("quick_meals_cn.json");
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            byte[] chunk = new byte[8192];
            int read;
            while ((read = stream.read(chunk)) > 0) {
                buffer.write(chunk, 0, read);
            }
            stream.close();
            JSONObject root = new JSONObject(new String(buffer.toByteArray(), StandardCharsets.UTF_8));
            JSONArray presets = root.optJSONArray("presets");
            if (presets == null) {
                return result;
            }
            for (int i = 0; i < presets.length(); i++) {
                MealPreset preset = parse(presets.optJSONObject(i));
                if (preset != null) {
                    result.add(preset);
                }
            }
        } catch (Exception ignored) {
            // 预设缺失不阻塞启动：「记一餐」会退化成只有手动输入和 AI 估算。
        }
        return result;
    }

    private static MealPreset parse(JSONObject object) {
        if (object == null) {
            return null;
        }
        try {
            Map<FoodGroup, Integer> groups = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
            JSONObject groupJson = object.optJSONObject("groups");
            if (groupJson != null) {
                Iterator<String> keys = groupJson.keys();
                while (keys.hasNext()) {
                    String key = keys.next();
                    FoodGroup group = FoodGroup.parse(key, null);
                    if (group != null) {
                        groups.put(group, groupJson.optInt(key));
                    }
                }
            }
            if (groups.isEmpty()) {
                return null;
            }
            MealPreset.Kind kind;
            try {
                kind = MealPreset.Kind.valueOf(object.optString("kind", "PORTION"));
            } catch (IllegalArgumentException unknown) {
                kind = MealPreset.Kind.PORTION;
            }
            return new MealPreset(
                    object.getString("id"),
                    object.getString("name"),
                    kind,
                    object.optString("hint", ""),
                    object.optInt("kcal"),
                    groups);
        } catch (Exception broken) {
            return null;
        }
    }
}
