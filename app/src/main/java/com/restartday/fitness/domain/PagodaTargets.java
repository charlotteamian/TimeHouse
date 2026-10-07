package com.restartday.fitness.domain;

import java.util.Collections;
import java.util.EnumMap;
import java.util.Map;

/**
 * 把宝塔各类食物的推荐区间，按个人目标热量在区间内插值成当日克数目标。
 * 指南区间锚定普通成人（约 1600-2400 kcal）：低于/高于该带宽时取区间端点。
 * 这是对宝塔区间的插值应用，不是逐字引用指南的能量档位表。
 */
public final class PagodaTargets {
    private final Map<FoodGroup, Integer> grams;
    private final int targetKcal;

    private PagodaTargets(Map<FoodGroup, Integer> grams, int targetKcal) {
        this.grams = Collections.unmodifiableMap(grams);
        this.targetKcal = targetKcal;
    }

    public static PagodaTargets forEnergy(int targetKcal) {
        double t = (targetKcal - 1600) / 800.0;
        t = Math.max(0.0, Math.min(1.0, t));
        Map<FoodGroup, Integer> grams = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        for (FoodGroup group : FoodGroup.values()) {
            double value = group.minGrams() + t * (group.maxGrams() - group.minGrams());
            grams.put(group, (int) Math.round(value / 5.0) * 5);
        }
        return new PagodaTargets(grams, targetKcal);
    }

    public int targetKcal() {
        return targetKcal;
    }

    public int gramsFor(FoodGroup group) {
        Integer value = grams.get(group);
        return value == null ? 0 : value;
    }

    /** 剩余缺口（克），不小于 0。 */
    public int remaining(FoodGroup group, int eatenGrams) {
        return Math.max(0, gramsFor(group) - Math.max(0, eatenGrams));
    }

    /** 完成度 0-1（可超过 1，供 UI 判断超量）。 */
    public double progress(FoodGroup group, int eatenGrams) {
        int target = gramsFor(group);
        if (target <= 0) {
            return 0;
        }
        return Math.max(0, eatenGrams) / (double) target;
    }
}
