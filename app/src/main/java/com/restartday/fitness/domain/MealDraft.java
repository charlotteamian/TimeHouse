package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 「记一餐」的待确认草稿：把若干预设（或 AI 估算结果）按份数累加，
 * 用户确认后才一次性写进当日宝塔打卡。
 *
 * <p>份数以「半份」为最小步长：一份 = 2 halves，允许 0.5 份，
 * 因为「半碗饭」「一份半麻辣烫」是真实存在的说法，而 0.25 份没人能分辨。
 */
public final class MealDraft {

    /** 一份 = 2 个半份。 */
    public static final int HALVES_PER_SERVING = 2;

    private final Map<MealPreset, Integer> halves = new LinkedHashMap<MealPreset, Integer>();
    private final Map<FoodGroup, Integer> extraGrams =
            new EnumMap<FoodGroup, Integer>(FoodGroup.class);
    private int extraKcal;
    private String extraLabel = "";

    /** 加减份数（halfSteps 为正负的「半份」数），减到 0 即移除。 */
    public void adjust(MealPreset preset, int halfSteps) {
        Integer current = halves.get(preset);
        int next = (current == null ? 0 : current) + halfSteps;
        if (next <= 0) {
            halves.remove(preset);
        } else {
            halves.put(preset, next);
        }
    }

    public void addServing(MealPreset preset) {
        adjust(preset, HALVES_PER_SERVING);
    }

    public void remove(MealPreset preset) {
        halves.remove(preset);
    }

    public int halvesFor(MealPreset preset) {
        Integer value = halves.get(preset);
        return value == null ? 0 : value;
    }

    /** 份数文本，如「×1」「×1.5」。 */
    public String servingLabel(MealPreset preset) {
        int value = halvesFor(preset);
        if (value % HALVES_PER_SERVING == 0) {
            return "×" + (value / HALVES_PER_SERVING);
        }
        return "×" + (value / (double) HALVES_PER_SERVING);
    }

    public List<MealPreset> presets() {
        return Collections.unmodifiableList(new ArrayList<MealPreset>(halves.keySet()));
    }

    /**
     * 放入一条 AI 估算（或手填）的整餐结果，替换上一条。
     * 与预设分开存，这样用户加减预设份数时不会把 AI 那份也一起缩放。
     */
    public void setEstimate(String label, int kcal, Map<FoodGroup, Integer> grams) {
        extraGrams.clear();
        extraLabel = label == null ? "" : label;
        extraKcal = Math.max(0, kcal);
        if (grams != null) {
            for (Map.Entry<FoodGroup, Integer> entry : grams.entrySet()) {
                if (entry.getValue() != null && entry.getValue() > 0) {
                    extraGrams.put(entry.getKey(), entry.getValue());
                }
            }
        }
    }

    public void clearEstimate() {
        extraGrams.clear();
        extraKcal = 0;
        extraLabel = "";
    }

    public boolean hasEstimate() {
        return !extraGrams.isEmpty();
    }

    public String estimateLabel() {
        return extraLabel;
    }

    public Map<FoodGroup, Integer> estimateGrams() {
        return Collections.unmodifiableMap(extraGrams);
    }

    public boolean isEmpty() {
        return halves.isEmpty() && extraGrams.isEmpty();
    }

    public void clear() {
        halves.clear();
        clearEstimate();
    }

    /** 合计宝塔克数（生重），预设按份数缩放后与估算结果相加。 */
    public Map<FoodGroup, Integer> totalGrams() {
        Map<FoodGroup, Integer> total = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        for (Map.Entry<MealPreset, Integer> entry : halves.entrySet()) {
            double factor = entry.getValue() / (double) HALVES_PER_SERVING;
            for (Map.Entry<FoodGroup, Integer> part : entry.getKey().groupGrams().entrySet()) {
                int scaled = (int) Math.round(part.getValue() * factor);
                if (scaled > 0) {
                    Integer prev = total.get(part.getKey());
                    total.put(part.getKey(), (prev == null ? 0 : prev) + scaled);
                }
            }
        }
        for (Map.Entry<FoodGroup, Integer> entry : extraGrams.entrySet()) {
            Integer prev = total.get(entry.getKey());
            total.put(entry.getKey(), (prev == null ? 0 : prev) + entry.getValue());
        }
        return Collections.unmodifiableMap(total);
    }

    /** 合计估算热量（kcal）。 */
    public int totalKcal() {
        double total = extraKcal;
        for (Map.Entry<MealPreset, Integer> entry : halves.entrySet()) {
            total += entry.getKey().kcal() * entry.getValue() / (double) HALVES_PER_SERVING;
        }
        return (int) Math.round(total);
    }

    /** 这一餐都有什么，如「一拳米饭 ×1.5、黄焖鸡米饭 ×1」，记入后用作可撤销记录的名字。 */
    public String itemsLabel() {
        StringBuilder builder = new StringBuilder();
        for (Map.Entry<MealPreset, Integer> entry : halves.entrySet()) {
            if (builder.length() > 0) {
                builder.append("、");
            }
            builder.append(entry.getKey().name()).append(" ").append(servingLabel(entry.getKey()));
        }
        if (!extraGrams.isEmpty() && extraLabel.length() > 0) {
            if (builder.length() > 0) {
                builder.append("、");
            }
            builder.append(extraLabel);
        }
        return builder.length() == 0 ? "一餐" : builder.toString();
    }

    /** 一行摘要，用于确认前给用户看清楚要写入什么。 */
    public String summary() {
        StringBuilder builder = new StringBuilder();
        for (Map.Entry<FoodGroup, Integer> entry : totalGrams().entrySet()) {
            if (builder.length() > 0) {
                builder.append(" · ");
            }
            builder.append(entry.getKey().label()).append(" ").append(entry.getValue()).append("g");
        }
        return builder.length() == 0 ? "还没选任何东西" : builder.toString();
    }
}
