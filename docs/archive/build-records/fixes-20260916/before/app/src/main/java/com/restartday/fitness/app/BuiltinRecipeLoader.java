package com.restartday.fitness.app;

import android.content.Context;

import com.restartday.fitness.domain.BuiltinRecipe;
import com.restartday.fitness.domain.FoodGroup;
import com.restartday.fitness.domain.GuidelineRefs;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/** 读取 assets/recipes_cn_guideline.json 的内置循证食谱。 */
public final class BuiltinRecipeLoader {

    private static final Map<String, String> REF_TEXT = new HashMap<String, String>();

    static {
        REF_TEXT.put("CDG_2022", GuidelineRefs.CDG_2022);
        REF_TEXT.put("CDG_FIBER", GuidelineRefs.CDG_FIBER);
        REF_TEXT.put("CDG_PROTEIN_RNI", GuidelineRefs.CDG_PROTEIN_RNI);
        REF_TEXT.put("SPORT_PROTEIN", GuidelineRefs.SPORT_PROTEIN);
        REF_TEXT.put("BMR_FORMULA", GuidelineRefs.BMR_FORMULA);
        REF_TEXT.put("ENERGY_RATE", GuidelineRefs.ENERGY_RATE);
        REF_TEXT.put("FAT_RANGE", GuidelineRefs.FAT_RANGE);
        REF_TEXT.put("ESTIMATE_NOTE", GuidelineRefs.ESTIMATE_NOTE);
        REF_TEXT.put("ACSM_RT", GuidelineRefs.ACSM_RT);
        REF_TEXT.put("ACSM_AEROBIC", GuidelineRefs.ACSM_AEROBIC);
    }

    private BuiltinRecipeLoader() {
    }

    public static List<BuiltinRecipe> load(Context context) {
        List<BuiltinRecipe> result = new ArrayList<BuiltinRecipe>();
        try {
            InputStream stream = context.getAssets().open("recipes_cn_guideline.json");
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            byte[] chunk = new byte[8192];
            int read;
            while ((read = stream.read(chunk)) > 0) {
                buffer.write(chunk, 0, read);
            }
            stream.close();
            JSONObject root = new JSONObject(new String(buffer.toByteArray(), StandardCharsets.UTF_8));
            JSONArray recipes = root.optJSONArray("recipes");
            if (recipes == null) {
                return result;
            }
            for (int i = 0; i < recipes.length(); i++) {
                BuiltinRecipe recipe = parse(recipes.optJSONObject(i));
                if (recipe != null) {
                    result.add(recipe);
                }
            }
        } catch (Exception ignored) {
            // 内置食谱缺失不阻塞启动；食物页会显示空态。
        }
        return result;
    }

    private static BuiltinRecipe parse(JSONObject object) {
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
            List<String> refs = new ArrayList<String>();
            JSONArray refArray = object.optJSONArray("refs");
            if (refArray != null) {
                for (int i = 0; i < refArray.length(); i++) {
                    String key = refArray.optString(i);
                    String text = REF_TEXT.get(key);
                    refs.add(text == null ? key : text);
                }
            }
            return new BuiltinRecipe(
                    object.getString("id"),
                    object.getString("name"),
                    toList(object.optJSONArray("slots")),
                    toList(object.optJSONArray("tags")),
                    object.optInt("kcal"),
                    object.optInt("protein"),
                    object.optInt("fat"),
                    object.optInt("carb"),
                    object.optInt("fiber"),
                    groups,
                    toList(object.optJSONArray("ingredients")),
                    toList(object.optJSONArray("steps")),
                    object.optString("rationale", ""),
                    refs,
                    object.optBoolean("trainingDay", false));
        } catch (Exception broken) {
            return null;
        }
    }

    private static List<String> toList(JSONArray array) {
        List<String> result = new ArrayList<String>();
        if (array != null) {
            for (int i = 0; i < array.length(); i++) {
                String value = array.optString(i, "");
                if (value.length() > 0) {
                    result.add(value);
                }
            }
        }
        return result;
    }
}
