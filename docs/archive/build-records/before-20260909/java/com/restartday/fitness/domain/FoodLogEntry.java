package com.restartday.fitness.domain;

import java.util.Collections;
import java.util.EnumMap;
import java.util.Map;

/**
 * 一次「记入今天」写进 {@link DayFoodLog} 的增量：一份食谱，或「记一餐」确认的那一餐。
 *
 * <p>存在的理由：确认记入是一次点击就完成的累加，点错了以前只能等第二天。
 * 把每次写入的增量原样留一份，撤销时就能精确减回去，而不用反推「刚才加了多少」。
 *
 * <p>增量一律为非负：这是一次「吃了什么」的记录，不是修正。手动改克数走
 * {@link DayFoodLog#setGrams}，不进这份历史。
 */
public final class FoodLogEntry {

    private final String label;
    private final int kcal;
    private final int protein;
    private final int fiber;
    private final Map<FoodGroup, Integer> grams;
    private final String recipeId;
    private final long epochMillis;

    /**
     * @param label       给人看的名字，如「燕麦牛奶碗」「记一餐 · 黄焖鸡米饭 ×1」
     * @param recipeId    内置食谱 id；「记一餐」等没有食谱来源的传空串
     * @param epochMillis 记入时刻，用于按时间显示
     */
    public FoodLogEntry(String label, int kcal, int protein, int fiber,
            Map<FoodGroup, Integer> grams, String recipeId, long epochMillis) {
        this.label = label == null || label.length() == 0 ? "一次记录" : label;
        this.kcal = Math.max(0, kcal);
        this.protein = Math.max(0, protein);
        this.fiber = Math.max(0, fiber);
        this.recipeId = recipeId == null ? "" : recipeId;
        this.epochMillis = epochMillis;
        Map<FoodGroup, Integer> copy = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        if (grams != null) {
            for (Map.Entry<FoodGroup, Integer> entry : grams.entrySet()) {
                if (entry.getKey() != null && entry.getValue() != null && entry.getValue() > 0) {
                    copy.put(entry.getKey(), entry.getValue());
                }
            }
        }
        this.grams = Collections.unmodifiableMap(copy);
    }

    public String label() {
        return label;
    }

    public int kcal() {
        return kcal;
    }

    public int protein() {
        return protein;
    }

    public int fiber() {
        return fiber;
    }

    /** 本次写入的宝塔克数（生重），只含正值。 */
    public Map<FoodGroup, Integer> grams() {
        return grams;
    }

    /** 内置食谱 id，「记一餐」为空串。 */
    public String recipeId() {
        return recipeId;
    }

    public long epochMillis() {
        return epochMillis;
    }

    /** 一行说明这条记录加了什么，撤销前给用户看清楚要减掉什么。 */
    public String summary() {
        StringBuilder builder = new StringBuilder();
        if (kcal > 0) {
            builder.append(kcal).append(" kcal");
        }
        for (Map.Entry<FoodGroup, Integer> entry : grams.entrySet()) {
            if (builder.length() > 0) {
                builder.append(" · ");
            }
            builder.append(entry.getKey().label()).append(" ").append(entry.getValue()).append("g");
        }
        return builder.length() == 0 ? "没有可减的量" : builder.toString();
    }
}
