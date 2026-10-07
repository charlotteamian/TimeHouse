package com.restartday.fitness.domain;

public final class DailyGapTest {
    public static void main(String[] args) {
        DailyGapTest test = new DailyGapTest();
        test.emptyDayShowsFullBudgetAndGaps();
        test.shortfallsAreSortedBiggestFirst();
        test.eatingClosesGapsAndSpendsBudget();
        test.overBudgetSteersTowardLightFood();
        test.satisfiedDayStopsAskingForMore();
        System.out.println("DailyGapTest: all tests passed");
    }

    private EnergyPlan plan() {
        return new NutritionPlanner().plan(new NutritionProfile(
                true, 30, 175, 70, ActivityLevel.MODERATE, PlanGoal.FAT_LOSS));
    }

    private void emptyDayShowsFullBudgetAndGaps() {
        EnergyPlan plan = plan();
        PagodaTargets targets = PagodaTargets.forEnergy(plan.targetKcal());
        DailyGap gap = DailyGap.of(plan, targets, new DayFoodLog());
        assertTrue(gap.remainingKcal() == plan.targetKcal(),
                "空白一天应剩满额热量，实际 " + gap.remainingKcal());
        assertTrue(gap.remainingProteinG() == plan.proteinG(), "空白一天蛋白应全缺");
        assertTrue(!gap.shortfalls().isEmpty(), "空白一天宝塔应有缺口");
        assertTrue(!gap.overBudget() && !gap.isSatisfied(), "空白一天既没超也没达标");
    }

    private void shortfallsAreSortedBiggestFirst() {
        // 缺口大的排前面，AI 提示词和页面提示都靠这个顺序决定先补什么。
        EnergyPlan plan = plan();
        PagodaTargets targets = PagodaTargets.forEnergy(plan.targetKcal());
        DailyGap gap = DailyGap.of(plan, targets, new DayFoodLog());
        int previous = Integer.MAX_VALUE;
        for (DailyGap.Shortfall shortfall : gap.shortfalls()) {
            assertTrue(shortfall.grams() <= previous,
                    "缺口应从大到小，实际 " + shortfall.group().label() + " " + shortfall.grams());
            assertTrue(shortfall.grams() > 0, "已达标的类别不应出现在缺口里");
            previous = shortfall.grams();
        }
    }

    private void eatingClosesGapsAndSpendsBudget() {
        EnergyPlan plan = plan();
        PagodaTargets targets = PagodaTargets.forEnergy(plan.targetKcal());
        DayFoodLog log = new DayFoodLog();
        log.setGrams(FoodGroup.VEGETABLE, 2000);      // 蔬菜远超目标
        log.restoreTotals(600, 40, 0, 0);
        DailyGap gap = DailyGap.of(plan, targets, log);
        assertTrue(gap.remainingKcal() == plan.targetKcal() - 600,
                "剩余热量应扣掉已吃，实际 " + gap.remainingKcal());
        assertTrue(gap.remainingProteinG() == plan.proteinG() - 40, "剩余蛋白应扣掉已吃");
        for (DailyGap.Shortfall shortfall : gap.shortfalls()) {
            assertTrue(shortfall.group() != FoodGroup.VEGETABLE,
                    "吃够的类别不应再出现在缺口里");
        }
        assertTrue(gap.promptBrief().contains("优先选能补上这些缺口"),
                "还有缺口时应引导补缺口，实际 " + gap.promptBrief());
    }

    private void overBudgetSteersTowardLightFood() {
        // 超了还推荐高热量的菜，等于这个功能白做。
        EnergyPlan plan = plan();
        PagodaTargets targets = PagodaTargets.forEnergy(plan.targetKcal());
        DayFoodLog log = new DayFoodLog();
        log.restoreTotals(plan.targetKcal() + 500, 0, 0, 0);
        DailyGap gap = DailyGap.of(plan, targets, log);
        assertTrue(gap.overBudget() && gap.remainingKcal() == -500,
                "超额应为负数，实际 " + gap.remainingKcal());
        assertTrue(gap.summary().contains("热量已超 500"), "页面提示应说明超了多少");
        assertTrue(gap.promptBrief().contains("清淡"), "提示词应要求清淡低热量");
    }

    private void satisfiedDayStopsAskingForMore() {
        EnergyPlan plan = plan();
        PagodaTargets targets = PagodaTargets.forEnergy(plan.targetKcal());
        DayFoodLog log = new DayFoodLog();
        for (FoodGroup group : FoodGroup.values()) {
            log.setGrams(group, 5000);
        }
        log.restoreTotals(0, plan.proteinG(), 0, 0);
        DailyGap gap = DailyGap.of(plan, targets, log);
        assertTrue(gap.isSatisfied(), "全部吃够应视为达标");
        assertTrue(gap.summary().contains("都达标了"), "达标时页面应说达标");
        assertTrue(gap.promptBrief().contains("缺口已经补齐"), "达标时提示词不应再要求补缺口");
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
