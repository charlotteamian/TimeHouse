package com.restartday.fitness.domain;

import java.util.EnumMap;
import java.util.Map;

public final class MealDraftTest {
    public static void main(String[] args) {
        MealDraftTest test = new MealDraftTest();
        test.singleServingUsesPresetGramsVerbatim();
        test.halfPortionsScaleAndRound();
        test.presetsAccumulateAcrossGroups();
        test.estimateIsSeparateFromPresetsAndUnscaled();
        test.removeAndClearEmptyTheDraft();
        test.servingLabelReadsNaturally();
        test.itemsLabelNamesEverythingInTheMeal();
        test.emptyDraftReportsNothing();
        System.out.println("MealDraftTest: all tests passed");
    }

    private MealPreset preset(String id, int kcal, Object... groupPairs) {
        Map<FoodGroup, Integer> groups = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        for (int i = 0; i < groupPairs.length; i += 2) {
            groups.put((FoodGroup) groupPairs[i], (Integer) groupPairs[i + 1]);
        }
        return new MealPreset(id, id, MealPreset.Kind.PORTION, "hint", kcal, groups);
    }

    private void singleServingUsesPresetGramsVerbatim() {
        // 一拳米饭 = 生米 80g（不是熟重 200g）。这条口径写错会让全天谷类虚高 2-3 倍。
        MealPreset rice = preset("一拳米饭", 280, FoodGroup.GRAIN, 80);
        MealDraft draft = new MealDraft();
        draft.addServing(rice);
        assertTrue(draft.totalGrams().get(FoodGroup.GRAIN) == 80,
                "一份应原样写入 80g，实际 " + draft.totalGrams().get(FoodGroup.GRAIN));
        assertTrue(draft.totalKcal() == 280, "一份热量应为 280，实际 " + draft.totalKcal());
    }

    private void halfPortionsScaleAndRound() {
        MealPreset rice = preset("一拳米饭", 280, FoodGroup.GRAIN, 80);
        MealDraft draft = new MealDraft();
        draft.addServing(rice);
        draft.adjust(rice, 1);                       // 1.5 份
        assertTrue(draft.totalGrams().get(FoodGroup.GRAIN) == 120,
                "1.5 份应为 120g，实际 " + draft.totalGrams().get(FoodGroup.GRAIN));
        assertTrue(draft.totalKcal() == 420, "1.5 份热量应为 420，实际 " + draft.totalKcal());

        // 奇数克数的半份要四舍五入到整数，不能截断成 0
        MealPreset nuts = preset("坚果", 60, FoodGroup.SOY_NUT, 5);
        MealDraft odd = new MealDraft();
        odd.adjust(nuts, 1);                          // 0.5 份 → 2.5g → 3g
        assertTrue(odd.totalGrams().get(FoodGroup.SOY_NUT) == 3,
                "2.5g 应进位为 3g，实际 " + odd.totalGrams().get(FoodGroup.SOY_NUT));
    }

    private void presetsAccumulateAcrossGroups() {
        MealPreset takeout = preset("黄焖鸡米饭", 750,
                FoodGroup.GRAIN, 100, FoodGroup.ANIMAL, 100, FoodGroup.OIL, 20);
        MealPreset milk = preset("一杯牛奶", 135, FoodGroup.DAIRY, 250);
        MealDraft draft = new MealDraft();
        draft.addServing(takeout);
        draft.addServing(milk);
        Map<FoodGroup, Integer> total = draft.totalGrams();
        assertTrue(total.get(FoodGroup.GRAIN) == 100 && total.get(FoodGroup.ANIMAL) == 100
                        && total.get(FoodGroup.OIL) == 20 && total.get(FoodGroup.DAIRY) == 250,
                "多个预设应按类别分别累加，实际 " + total);
        assertTrue(draft.totalKcal() == 885, "合计热量应为 885，实际 " + draft.totalKcal());
    }

    private void estimateIsSeparateFromPresetsAndUnscaled() {
        MealPreset rice = preset("一拳米饭", 280, FoodGroup.GRAIN, 80);
        Map<FoodGroup, Integer> aiGrams = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        aiGrams.put(FoodGroup.GRAIN, 50);
        aiGrams.put(FoodGroup.VEGETABLE, 120);

        MealDraft draft = new MealDraft();
        draft.addServing(rice);
        draft.setEstimate("AI：一份炒饭", 400, aiGrams);
        draft.adjust(rice, 2);                        // 米饭加到 2 份

        Map<FoodGroup, Integer> total = draft.totalGrams();
        assertTrue(total.get(FoodGroup.GRAIN) == 210,
                "预设 160g + 估算 50g = 210g，估算不应被份数缩放，实际 " + total.get(FoodGroup.GRAIN));
        assertTrue(total.get(FoodGroup.VEGETABLE) == 120, "估算的蔬菜应原样保留");
        assertTrue(draft.totalKcal() == 960, "560 + 400 = 960，实际 " + draft.totalKcal());

        draft.clearEstimate();
        assertTrue(!draft.hasEstimate() && draft.totalGrams().get(FoodGroup.VEGETABLE) == null,
                "清掉估算后不应残留蔬菜");
        assertTrue(draft.totalGrams().get(FoodGroup.GRAIN) == 160, "清估算不应动到预设");
    }

    private void removeAndClearEmptyTheDraft() {
        MealPreset rice = preset("一拳米饭", 280, FoodGroup.GRAIN, 80);
        MealDraft draft = new MealDraft();
        draft.addServing(rice);
        draft.adjust(rice, -5);                       // 减过头应移除而不是变负
        assertTrue(draft.isEmpty(), "减到 0 以下应移除条目");
        assertTrue(draft.totalGrams().isEmpty(), "空草稿不应产生克数");

        draft.addServing(rice);
        draft.setEstimate("AI", 100, singleton(FoodGroup.FRUIT, 50));
        draft.clear();
        assertTrue(draft.isEmpty() && draft.totalKcal() == 0, "clear 应同时清掉预设和估算");
    }

    private void servingLabelReadsNaturally() {
        MealPreset rice = preset("一拳米饭", 280, FoodGroup.GRAIN, 80);
        MealDraft draft = new MealDraft();
        draft.addServing(rice);
        assertTrue(draft.servingLabel(rice).equals("×1"), "整份应显示 ×1，实际 " + draft.servingLabel(rice));
        draft.adjust(rice, 1);
        assertTrue(draft.servingLabel(rice).equals("×1.5"),
                "半份应显示 ×1.5，实际 " + draft.servingLabel(rice));
    }

    private void itemsLabelNamesEverythingInTheMeal() {
        // 记入后这行字就是撤销列表里的名字，必须能认出是哪一餐。
        MealPreset rice = preset("一拳米饭", 280, FoodGroup.GRAIN, 80);
        MealPreset chicken = preset("黄焖鸡米饭", 750, FoodGroup.ANIMAL, 100);
        MealDraft draft = new MealDraft();
        draft.addServing(rice);
        draft.adjust(rice, 1);
        draft.addServing(chicken);
        assertTrue(draft.itemsLabel().equals("一拳米饭 ×1.5、黄焖鸡米饭 ×1"),
                "应列出每项和份数，实际 " + draft.itemsLabel());

        draft.setEstimate("AI · 一份炒饭", 400, singleton(FoodGroup.GRAIN, 50));
        assertTrue(draft.itemsLabel().endsWith("、AI · 一份炒饭"),
                "AI 估算也应出现在名字里，实际 " + draft.itemsLabel());
        assertTrue(new MealDraft().itemsLabel().equals("一餐"), "空草稿应有兜底名字");
    }

    private void emptyDraftReportsNothing() {
        MealDraft draft = new MealDraft();
        assertTrue(draft.isEmpty(), "新草稿应为空");
        assertTrue(draft.totalKcal() == 0, "空草稿热量应为 0");
        assertTrue(draft.summary().contains("还没选"), "空草稿摘要应提示未选择");
    }

    private Map<FoodGroup, Integer> singleton(FoodGroup group, int grams) {
        Map<FoodGroup, Integer> map = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        map.put(group, grams);
        return map;
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
