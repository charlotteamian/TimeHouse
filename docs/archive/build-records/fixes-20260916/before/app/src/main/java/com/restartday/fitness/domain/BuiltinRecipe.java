package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

/** 内置的循证食谱：按宝塔结构设计，营养为《中国食物成分表》常见值估算。 */
public final class BuiltinRecipe {
    private final String id;
    private final String name;
    private final List<String> mealSlots;   // 早餐/午餐/晚餐/加餐
    private final List<String> tags;
    private final int kcal;
    private final int proteinG;
    private final int fatG;
    private final int carbG;
    private final int fiberG;
    private final Map<FoodGroup, Integer> groupGrams;
    private final List<String> ingredients;
    private final List<String> steps;
    private final String rationale;
    private final List<String> refs;
    private final boolean trainingDay;      // 更适合训练日（碳水/蛋白偏高）

    public BuiltinRecipe(String id, String name, List<String> mealSlots, List<String> tags,
            int kcal, int proteinG, int fatG, int carbG, int fiberG,
            Map<FoodGroup, Integer> groupGrams, List<String> ingredients, List<String> steps,
            String rationale, List<String> refs, boolean trainingDay) {
        this.id = id;
        this.name = name;
        this.mealSlots = Collections.unmodifiableList(new ArrayList<String>(mealSlots));
        this.tags = Collections.unmodifiableList(new ArrayList<String>(tags));
        this.kcal = kcal;
        this.proteinG = proteinG;
        this.fatG = fatG;
        this.carbG = carbG;
        this.fiberG = fiberG;
        this.groupGrams = Collections.unmodifiableMap(
                new EnumMap<FoodGroup, Integer>(groupGrams));
        this.ingredients = Collections.unmodifiableList(new ArrayList<String>(ingredients));
        this.steps = Collections.unmodifiableList(new ArrayList<String>(steps));
        this.rationale = rationale;
        this.refs = Collections.unmodifiableList(new ArrayList<String>(refs));
        this.trainingDay = trainingDay;
    }

    public String id() {
        return id;
    }

    public String name() {
        return name;
    }

    public List<String> mealSlots() {
        return mealSlots;
    }

    public List<String> tags() {
        return tags;
    }

    public int kcal() {
        return kcal;
    }

    public int proteinG() {
        return proteinG;
    }

    public int fatG() {
        return fatG;
    }

    public int carbG() {
        return carbG;
    }

    public int fiberG() {
        return fiberG;
    }

    public int groupGrams(FoodGroup group) {
        Integer value = groupGrams.get(group);
        return value == null ? 0 : value;
    }

    public Map<FoodGroup, Integer> allGroupGrams() {
        return groupGrams;
    }

    public List<String> ingredients() {
        return ingredients;
    }

    public List<String> steps() {
        return steps;
    }

    public String rationale() {
        return rationale;
    }

    public List<String> refs() {
        return refs;
    }

    public boolean trainingDay() {
        return trainingDay;
    }

    public String macroLabel() {
        return kcal + " kcal · 蛋白 " + proteinG + "g · 脂肪 " + fatG + "g · 碳水 " + carbG
                + "g · 纤维 " + fiberG + "g（估算）";
    }
}
