package com.restartday.fitness.domain;

import java.util.Arrays;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

public final class NutritionPlannerTest {
    public static void main(String[] args) {
        NutritionPlannerTest test = new NutritionPlannerTest();
        test.mifflinStJeorMatchesKnownValues();
        test.fatLossDeficitAndFloorAreApplied();
        test.muscleGainAddsSurplusAndSportProtein();
        test.generalFitnessUsesModerateProteinAboveRni();
        test.obeseProfileUsesAdjustedProteinBasis();
        test.pagodaTargetsInterpolateWithinGuidelineRanges();
        test.fiberWaterConstantsFollowGuideline();
        test.scorerPrefersProteinWhenProteinGapDominates();
        test.scorerPenalizesKcalOvershootAndFillsVegetableGap();
        System.out.println("NutritionPlannerTest: all tests passed");
    }

    private final NutritionPlanner planner = new NutritionPlanner();

    private void mifflinStJeorMatchesKnownValues() {
        // 男 30 岁 175cm 70kg：10*70 + 6.25*175 - 5*30 + 5 = 1648.75 ≈ 1649
        EnergyPlan man = planner.plan(new NutritionProfile(true, 30, 175, 70,
                ActivityLevel.MODERATE, PlanGoal.GENERAL_FITNESS));
        assertTrue(Math.abs(man.bmrKcal() - 1649) <= 1, "男性 BMR 应约 1649，实际 " + man.bmrKcal());
        assertTrue(Math.abs(man.tdeeKcal() - Math.round(1648.75 * 1.55)) <= 2,
                "TDEE 应为 BMR×1.55，实际 " + man.tdeeKcal());
        assertTrue(man.targetKcal() == man.tdeeKcal(), "体适能目标应为维持热量");

        // 女 28 岁 162cm 55kg：10*55 + 6.25*162 - 5*28 - 161 = 1261.5 ≈ 1262
        EnergyPlan woman = planner.plan(new NutritionProfile(false, 28, 162, 55,
                ActivityLevel.LIGHT, PlanGoal.GENERAL_FITNESS));
        assertTrue(Math.abs(woman.bmrKcal() - 1262) <= 1, "女性 BMR 应约 1262，实际 " + woman.bmrKcal());
    }

    private void fatLossDeficitAndFloorAreApplied() {
        EnergyPlan plan = planner.plan(new NutritionProfile(true, 30, 175, 70,
                ActivityLevel.MODERATE, PlanGoal.FAT_LOSS));
        assertTrue(plan.targetKcal() == plan.tdeeKcal() - 400,
                "减脂目标应为 TDEE-400，实际 " + plan.targetKcal());

        // 小体重久坐女性：TDEE-400 会低于 1200，应被安全下限抬起
        EnergyPlan small = planner.plan(new NutritionProfile(false, 25, 155, 45,
                ActivityLevel.SEDENTARY, PlanGoal.FAT_LOSS));
        assertTrue(small.targetKcal() >= 1200, "女性减脂热量不应低于 1200，实际 " + small.targetKcal());
        assertTrue(containsFragment(small.notes(), "安全下限"), "应提示按安全下限抬高");
    }

    private void muscleGainAddsSurplusAndSportProtein() {
        EnergyPlan plan = planner.plan(new NutritionProfile(true, 25, 178, 68,
                ActivityLevel.MODERATE, PlanGoal.MUSCLE_GAIN));
        assertTrue(plan.targetKcal() == plan.tdeeKcal() + 300, "增肌应 +300 kcal");
        assertTrue(Math.abs(plan.proteinG() - Math.round(68 * 1.8)) <= 1,
                "增肌蛋白应约 1.8g/kg，实际 " + plan.proteinG());
        assertTrue(plan.proteinPerKg() >= 1.6 && plan.proteinPerKg() <= 2.2,
                "运动人群蛋白应在 1.6-2.2g/kg 区间（Morton 2018/ISSN）");
    }

    private void generalFitnessUsesModerateProteinAboveRni() {
        EnergyPlan plan = planner.plan(new NutritionProfile(false, 35, 165, 58,
                ActivityLevel.LIGHT, PlanGoal.GENERAL_FITNESS));
        assertTrue(plan.proteinPerKg() == 1.2, "体适能蛋白应为 1.2g/kg");
        assertTrue(plan.proteinG() >= 55, "不应低于 DRIs 女性 RNI 55g，实际 " + plan.proteinG());
    }

    private void obeseProfileUsesAdjustedProteinBasis() {
        // BMI = 100/(1.7^2) ≈ 34.6 → 按 BMI24 体重 24*1.7^2 ≈ 69.4kg 计蛋白
        EnergyPlan plan = planner.plan(new NutritionProfile(true, 40, 170, 100,
                ActivityLevel.LIGHT, PlanGoal.FAT_LOSS));
        int expected = (int) Math.round(24 * 1.7 * 1.7 * 2.0);
        assertTrue(Math.abs(plan.proteinG() - expected) <= 2,
                "高 BMI 应按调整体重计蛋白（约 " + expected + "g），实际 " + plan.proteinG());
        assertTrue(containsFragment(plan.notes(), "调整体重"), "应说明调整体重口径");
    }

    private void pagodaTargetsInterpolateWithinGuidelineRanges() {
        PagodaTargets low = PagodaTargets.forEnergy(1500);   // 低于带宽 → 区间下限
        PagodaTargets mid = PagodaTargets.forEnergy(2000);
        PagodaTargets high = PagodaTargets.forEnergy(2600);  // 高于带宽 → 区间上限
        for (FoodGroup group : FoodGroup.values()) {
            assertTrue(low.gramsFor(group) == roundTo5(group.minGrams()),
                    group.label() + " 低能量应取区间下限");
            assertTrue(high.gramsFor(group) == roundTo5(group.maxGrams()),
                    group.label() + " 高能量应取区间上限");
            int m = mid.gramsFor(group);
            assertTrue(m >= group.minGrams() && m <= group.maxGrams(),
                    group.label() + " 中间能量应落在指南区间内");
        }
        assertTrue(mid.gramsFor(FoodGroup.VEGETABLE) == 400, "2000kcal 蔬菜应为 400g（300-500 中点）");
        assertTrue(mid.remaining(FoodGroup.VEGETABLE, 250) == 150, "蔬菜缺口计算错误");
    }

    private int roundTo5(int value) {
        return (int) Math.round(value / 5.0) * 5;
    }

    private void fiberWaterConstantsFollowGuideline() {
        EnergyPlan plan = planner.plan(new NutritionProfile(true, 30, 175, 70,
                ActivityLevel.MODERATE, PlanGoal.GENERAL_FITNESS));
        assertTrue(plan.fiberMinG() == 25 && plan.fiberMaxG() == 30, "纤维应为 25-30g（DRIs/指南）");
        assertTrue(plan.waterMinMl() == 1500 && plan.waterMaxMl() == 1700, "饮水应为 1500-1700ml（指南）");
    }

    private BuiltinRecipe recipe(String id, int kcal, int protein, int fiber,
            FoodGroup group, int grams, boolean trainingDay) {
        Map<FoodGroup, Integer> groups = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        groups.put(group, grams);
        return new BuiltinRecipe(id, id, Arrays.asList("午餐"), Arrays.<String>asList(),
                kcal, protein, 10, 40, fiber, groups,
                Arrays.<String>asList(), Arrays.<String>asList(), "", Arrays.<String>asList(), trainingDay);
    }

    private void scorerPrefersProteinWhenProteinGapDominates() {
        RecipeScorer scorer = new RecipeScorer();
        BuiltinRecipe highProtein = recipe("高蛋白", 450, 40, 4, FoodGroup.VEGETABLE, 100, true);
        BuiltinRecipe lowProtein = recipe("低蛋白", 450, 8, 4, FoodGroup.VEGETABLE, 100, true);
        List<RecipeScorer.Scored> ranked = scorer.rank(
                Arrays.asList(lowProtein, highProtein), "午餐",
                900, 60, PagodaTargets.forEnergy(2000), new int[FoodGroup.values().length], true);
        assertTrue(ranked.get(0).recipe.id().equals("高蛋白"),
                "蛋白缺口大时应优先高蛋白食谱，实际 " + ranked.get(0).recipe.id());
        assertTrue(ranked.get(0).reason.contains("蛋白"), "推荐理由应说明补蛋白");
    }

    private void scorerPenalizesKcalOvershootAndFillsVegetableGap() {
        RecipeScorer scorer = new RecipeScorer();
        BuiltinRecipe big = recipe("大分量", 900, 30, 5, FoodGroup.VEGETABLE, 150, true);
        BuiltinRecipe fit = recipe("适量", 420, 28, 5, FoodGroup.VEGETABLE, 200, true);
        List<RecipeScorer.Scored> ranked = scorer.rank(
                Arrays.asList(big, fit), "午餐",
                500, 30, PagodaTargets.forEnergy(2000), new int[FoodGroup.values().length], true);
        assertTrue(ranked.get(0).recipe.id().equals("适量"),
                "剩余热量 500 时应优先 420kcal 的食谱，实际 " + ranked.get(0).recipe.id());
    }

    private boolean containsFragment(List<String> notes, String fragment) {
        for (String note : notes) {
            if (note.contains(fragment)) {
                return true;
            }
        }
        return false;
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
