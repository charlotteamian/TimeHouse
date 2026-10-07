package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * 「今天还差什么」：剩余热量、剩余蛋白、宝塔各类还缺多少克。
 *
 * <p>存在的理由：推荐吃什么必须从这里出发，而不是随机翻菜谱或随手搜网页。
 * 同一份缺口同时喂给三个地方——页面上给人看的一行字、库内打分、AI 提示词，
 * 三处口径必须一致，所以算在一个地方。
 */
public final class DailyGap {

    /** 某一类还差多少克。 */
    public static final class Shortfall {
        private final FoodGroup group;
        private final int grams;

        private Shortfall(FoodGroup group, int grams) {
            this.group = group;
            this.grams = grams;
        }

        public FoodGroup group() {
            return group;
        }

        public int grams() {
            return grams;
        }
    }

    /** 只盯这几类：宝塔里最容易吃不够、且补上去确实有意义的。油和零食不在其中。 */
    private static final FoodGroup[] TRACKED = {
        FoodGroup.VEGETABLE, FoodGroup.WHOLE_GRAIN, FoodGroup.DAIRY,
        FoodGroup.FRUIT, FoodGroup.SOY_NUT, FoodGroup.ANIMAL,
    };

    private final int remainingKcal;
    private final int remainingProteinG;
    private final List<Shortfall> shortfalls;

    private DailyGap(int remainingKcal, int remainingProteinG, List<Shortfall> shortfalls) {
        this.remainingKcal = remainingKcal;
        this.remainingProteinG = remainingProteinG;
        this.shortfalls = Collections.unmodifiableList(shortfalls);
    }

    /**
     * @param eatenGrams 与 {@link FoodGroup#ordinal()} 对应的今日已吃克数
     */
    public static DailyGap of(EnergyPlan plan, PagodaTargets targets, DayFoodLog log) {
        int[] eatenGrams = log.gramsByGroup();
        List<Shortfall> gaps = new ArrayList<Shortfall>();
        for (FoodGroup group : TRACKED) {
            int remaining = targets.remaining(group, eatenGrams[group.ordinal()]);
            if (remaining > 0) {
                gaps.add(new Shortfall(group, remaining));
            }
        }
        Collections.sort(gaps, new Comparator<Shortfall>() {
            @Override
            public int compare(Shortfall left, Shortfall right) {
                return right.grams() - left.grams();
            }
        });
        return new DailyGap(plan.targetKcal() - log.kcal(), plan.proteinG() - log.protein(), gaps);
    }

    /** 今天还能吃多少 kcal；已经超了会是负数，推荐时该给清淡的。 */
    public int remainingKcal() {
        return remainingKcal;
    }

    public int remainingProteinG() {
        return remainingProteinG;
    }

    /** 还差的类别，缺口大的在前。 */
    public List<Shortfall> shortfalls() {
        return shortfalls;
    }

    public boolean overBudget() {
        return remainingKcal < 0;
    }

    public boolean isSatisfied() {
        return shortfalls.isEmpty() && remainingProteinG <= 0;
    }

    /** 页面上给人看的一行：先说缺口，再说还剩多少热量。 */
    public String summary() {
        StringBuilder builder = new StringBuilder();
        if (shortfalls.isEmpty()) {
            builder.append("宝塔重点类别都达标了");
        } else {
            builder.append("今天还差：");
            for (int i = 0; i < shortfalls.size(); i++) {
                if (i > 0) {
                    builder.append("、");
                }
                builder.append(shortfalls.get(i).group().label())
                        .append(shortfalls.get(i).grams()).append("g");
            }
        }
        if (remainingProteinG > 0) {
            builder.append("；蛋白还差 ").append(remainingProteinG).append("g");
        }
        if (remainingKcal < 0) {
            builder.append("；热量已超 ").append(-remainingKcal).append(" kcal");
        } else {
            builder.append("；还能吃约 ").append(remainingKcal).append(" kcal");
        }
        return builder.toString();
    }

    /** 喂给 AI 的缺口数据：说清楚数字，并挑明该往哪个方向选。 */
    public String promptBrief() {
        StringBuilder builder = new StringBuilder();
        builder.append("今日剩余热量约 ").append(remainingKcal).append(" kcal");
        builder.append("，蛋白质还差 ").append(Math.max(0, remainingProteinG)).append(" g");
        if (!shortfalls.isEmpty()) {
            builder.append("，平衡膳食宝塔还缺：");
            for (int i = 0; i < shortfalls.size(); i++) {
                if (i > 0) {
                    builder.append("、");
                }
                builder.append(shortfalls.get(i).group().label())
                        .append(" ").append(shortfalls.get(i).grams()).append("g");
            }
        }
        builder.append("。");
        if (overBudget()) {
            builder.append("热量已经超了，请选清淡、低热量、以蔬菜和优质蛋白为主的一道。");
        } else if (!shortfalls.isEmpty()) {
            builder.append("请优先选能补上这些缺口、且热量不超过剩余额度的一道。");
        } else {
            builder.append("缺口已经补齐，选一道热量在剩余额度内、口味符合用户当前状态的即可。");
        }
        return builder.toString();
    }
}
