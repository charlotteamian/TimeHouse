package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * 按「今天还差什么」给内置食谱打分：
 * 蛋白缺口权重最高，其次蔬菜/全谷物/水果/奶/大豆缺口；
 * 明显超出剩余热量会扣分。返回带解释的推荐，绝不随机。
 */
public final class RecipeScorer {

    public static final class Scored {
        public final BuiltinRecipe recipe;
        public final double score;
        public final String reason;

        Scored(BuiltinRecipe recipe, double score, String reason) {
            this.recipe = recipe;
            this.score = score;
            this.reason = reason;
        }
    }

    /**
     * @param slot            早餐/午餐/晚餐/加餐；空串表示不限
     * @param remainingKcal   今日剩余热量（可为负）
     * @param remainingProtein 今日剩余蛋白（克）
     * @param targets         宝塔目标
     * @param eatenGrams      今日各类已吃克数（与 FoodGroup.ordinal 对应的数组）
     * @param trainingDay     今天是否训练日
     */
    public List<Scored> rank(List<BuiltinRecipe> recipes, String slot,
            int remainingKcal, int remainingProtein,
            PagodaTargets targets, int[] eatenGrams, boolean trainingDay) {
        List<Scored> result = new ArrayList<Scored>();
        for (BuiltinRecipe recipe : recipes) {
            if (slot != null && slot.length() > 0 && !recipe.mealSlots().contains(slot)) {
                continue;
            }
            StringBuilder reason = new StringBuilder();
            double score = 0;

            // 蛋白缺口：覆盖越多越好（上限为缺口本身，避免鼓励爆量）
            if (remainingProtein > 0) {
                double covered = Math.min(recipe.proteinG(), remainingProtein);
                score += covered * 3.0;
                if (recipe.proteinG() >= 20) {
                    reason.append("补蛋白 ").append(recipe.proteinG()).append("g；");
                }
            }

            // 宝塔缺口：蔬菜/全谷物权重高，水果/奶/大豆次之
            score += gapCoverage(recipe, FoodGroup.VEGETABLE, targets, eatenGrams) * 0.5;
            score += gapCoverage(recipe, FoodGroup.WHOLE_GRAIN, targets, eatenGrams) * 0.8;
            score += gapCoverage(recipe, FoodGroup.FRUIT, targets, eatenGrams) * 0.3;
            score += gapCoverage(recipe, FoodGroup.DAIRY, targets, eatenGrams) * 0.3;
            score += gapCoverage(recipe, FoodGroup.SOY_NUT, targets, eatenGrams) * 1.2;
            appendGapReason(reason, recipe, FoodGroup.VEGETABLE, targets, eatenGrams, 100, "补蔬菜");
            appendGapReason(reason, recipe, FoodGroup.WHOLE_GRAIN, targets, eatenGrams, 40, "补全谷物");
            appendGapReason(reason, recipe, FoodGroup.DAIRY, targets, eatenGrams, 150, "补奶类");

            // 纤维加分（指南 25-30g 普遍吃不够）
            score += recipe.fiberG() * 1.5;

            // 热量贴合：超出剩余热量的部分扣分；剩余热量很少时倾向轻食
            if (remainingKcal > 0 && recipe.kcal() > remainingKcal) {
                score -= (recipe.kcal() - remainingKcal) * 0.6;
                reason.append("热量略超出今日剩余；");
            } else if (remainingKcal <= 0) {
                score -= recipe.kcal() * 0.8;
            }

            // 训练日偏好：训练日选碳水/蛋白高的，休息日反之（轻微权重）
            if (trainingDay == recipe.trainingDay()) {
                score += 15;
                reason.append(trainingDay ? "适合训练日；" : "适合休息日；");
            }

            result.add(new Scored(recipe, score, reason.length() == 0
                    ? "与今日营养目标整体匹配" : reason.toString()));
        }
        Collections.sort(result, new Comparator<Scored>() {
            @Override
            public int compare(Scored left, Scored right) {
                return Double.compare(right.score, left.score);
            }
        });
        return result;
    }

    private double gapCoverage(BuiltinRecipe recipe, FoodGroup group,
            PagodaTargets targets, int[] eatenGrams) {
        int remaining = targets.remaining(group, eatenGrams[group.ordinal()]);
        if (remaining <= 0) {
            return 0;
        }
        return Math.min(recipe.groupGrams(group), remaining);
    }

    private void appendGapReason(StringBuilder reason, BuiltinRecipe recipe, FoodGroup group,
            PagodaTargets targets, int[] eatenGrams, int minGap, String label) {
        int remaining = targets.remaining(group, eatenGrams[group.ordinal()]);
        if (remaining >= minGap && recipe.groupGrams(group) > 0) {
            reason.append(label).append(" ").append(Math.min(recipe.groupGrams(group), remaining))
                    .append("g；");
        }
    }
}
