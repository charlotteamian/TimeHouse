package com.restartday.fitness.domain;

import java.util.Collections;
import java.util.EnumMap;
import java.util.Map;

/**
 * 「记一餐」的快速录入预设：一份常见外卖、一个份量法单位，或一样零食。
 *
 * <p>存在的理由：外卖和零食没法按类别估克数。用户能说出的是「一份黄焖鸡米饭」
 * 「一拳米饭」「一包薯片」，拆成宝塔类别是 App 的事，不是用户的事。
 *
 * <p><b>口径：groupGrams 一律是宝塔的生重/干重</b>（与 {@link BuiltinRecipe} 一致）。
 * 一碗熟米饭记 GRAIN 80（生米），不是熟重 200；一片吐司按面粉折算而不是面包净重。
 * 这是用户最容易记错、且会一路错 2-3 倍的地方，所以预设里全部预先折算好。
 */
public final class MealPreset {

    /** 预设的用途分组，决定在「记一餐」里显示在哪一栏。 */
    public enum Kind {
        PORTION("份量法", "用手估：拳、掌心、捧、拇指"),
        TAKEOUT("常见外卖", "点一份就记一份，克数已折算"),
        SNACK("零食饮料", "包装上有净含量就照抄");

        private final String label;
        private final String hint;

        Kind(String label, String hint) {
            this.label = label;
            this.hint = hint;
        }

        public String label() {
            return label;
        }

        public String hint() {
            return hint;
        }
    }

    private final String id;
    private final String name;
    private final Kind kind;
    private final String hint;
    private final int kcal;
    private final Map<FoodGroup, Integer> groupGrams;

    public MealPreset(String id, String name, Kind kind, String hint, int kcal,
            Map<FoodGroup, Integer> groupGrams) {
        this.id = id;
        this.name = name;
        this.kind = kind;
        this.hint = hint == null ? "" : hint;
        this.kcal = kcal;
        this.groupGrams = Collections.unmodifiableMap(
                new EnumMap<FoodGroup, Integer>(groupGrams));
    }

    public String id() {
        return id;
    }

    public String name() {
        return name;
    }

    public Kind kind() {
        return kind;
    }

    public String hint() {
        return hint;
    }

    /** 单份估算热量（kcal）。 */
    public int kcal() {
        return kcal;
    }

    /** 单份的宝塔构成（生重克）。 */
    public Map<FoodGroup, Integer> groupGrams() {
        return groupGrams;
    }

    /** 一行摘要，如「谷类 100g · 鱼禽肉蛋 100g · 烹调油 20g」。 */
    public String groupLabel() {
        StringBuilder builder = new StringBuilder();
        for (Map.Entry<FoodGroup, Integer> entry : groupGrams.entrySet()) {
            if (builder.length() > 0) {
                builder.append(" · ");
            }
            builder.append(entry.getKey().label()).append(" ").append(entry.getValue()).append("g");
        }
        return builder.toString();
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof MealPreset)) {
            return false;
        }
        return id.equals(((MealPreset) other).id);
    }

    @Override
    public int hashCode() {
        return id.hashCode();
    }
}
