package com.restartday.fitness.domain;

import java.util.EnumMap;
import java.util.Map;

public final class DayFoodLogTest {
    public static void main(String[] args) {
        DayFoodLogTest test = new DayFoodLogTest();
        test.recordAccumulatesTotalsAndKeepsHistory();
        test.undoSubtractsExactlyWhatWasAdded();
        test.undoOnlyTouchesTheChosenEntry();
        test.undoClampsAtZeroAfterManualEdit();
        test.undoRemovesOneRecipeIdPerEntry();
        test.undoIgnoresOutOfRangeIndex();
        test.manualEditsStayOutOfHistory();
        test.historyIsCappedButTotalsAreNot();
        test.restoreDoesNotDoubleCount();
        System.out.println("DayFoodLogTest: all tests passed");
    }

    private FoodLogEntry entry(String label, int kcal, int protein, int fiber,
            String recipeId, Object... groupPairs) {
        Map<FoodGroup, Integer> grams = new EnumMap<FoodGroup, Integer>(FoodGroup.class);
        for (int i = 0; i < groupPairs.length; i += 2) {
            grams.put((FoodGroup) groupPairs[i], (Integer) groupPairs[i + 1]);
        }
        return new FoodLogEntry(label, kcal, protein, fiber, grams, recipeId, 0L);
    }

    private void recordAccumulatesTotalsAndKeepsHistory() {
        DayFoodLog log = new DayFoodLog();
        log.record(entry("燕麦牛奶碗", 420, 22, 6, "oat_milk",
                FoodGroup.GRAIN, 60, FoodGroup.DAIRY, 250));
        assertTrue(log.kcal() == 420 && log.protein() == 22 && log.fiber() == 6,
                "记入应累加宏量，实际 " + log.kcal() + "/" + log.protein() + "/" + log.fiber());
        assertTrue(log.grams(FoodGroup.GRAIN) == 60 && log.grams(FoodGroup.DAIRY) == 250,
                "记入应累加宝塔克数");
        assertTrue(log.entries().size() == 1 && log.entries().get(0).label().equals("燕麦牛奶碗"),
                "记入应留下一条可撤销记录");
        assertTrue(log.recipeIds().size() == 1, "食谱 id 应记入");
    }

    private void undoSubtractsExactlyWhatWasAdded() {
        // 撤销必须让当日回到记入前，否则误点一次就会污染全天热量直到跨日。
        DayFoodLog log = new DayFoodLog();
        log.record(entry("黄焖鸡米饭", 750, 35, 4, "",
                FoodGroup.GRAIN, 100, FoodGroup.ANIMAL, 100, FoodGroup.OIL, 20));
        FoodLogEntry undone = log.undo(0);
        assertTrue(undone != null && undone.label().equals("黄焖鸡米饭"), "撤销应返回被撤的那笔");
        assertTrue(log.kcal() == 0 && log.protein() == 0 && log.fiber() == 0,
                "撤销后宏量应归零，实际 " + log.kcal() + "/" + log.protein() + "/" + log.fiber());
        assertTrue(log.grams(FoodGroup.GRAIN) == 0 && log.grams(FoodGroup.ANIMAL) == 0
                        && log.grams(FoodGroup.OIL) == 0, "撤销后克数应归零");
        assertTrue(log.entries().isEmpty(), "撤销后历史里不应再有这笔");
    }

    private void undoOnlyTouchesTheChosenEntry() {
        DayFoodLog log = new DayFoodLog();
        log.record(entry("早餐", 400, 20, 5, "", FoodGroup.GRAIN, 60));
        log.record(entry("误点的午餐", 800, 40, 8, "", FoodGroup.GRAIN, 100, FoodGroup.ANIMAL, 120));
        log.record(entry("加餐", 150, 5, 2, "", FoodGroup.FRUIT, 200));

        log.undo(1);
        assertTrue(log.kcal() == 550 && log.protein() == 25 && log.fiber() == 7,
                "只应减掉被撤的那笔，实际 " + log.kcal() + "/" + log.protein() + "/" + log.fiber());
        assertTrue(log.grams(FoodGroup.GRAIN) == 60, "另外两笔的谷类应原样保留");
        assertTrue(log.grams(FoodGroup.ANIMAL) == 0, "被撤那笔独有的类别应归零");
        assertTrue(log.grams(FoodGroup.FRUIT) == 200, "后一笔不应被牵连");
        assertTrue(log.entries().size() == 2
                        && log.entries().get(0).label().equals("早餐")
                        && log.entries().get(1).label().equals("加餐"),
                "剩余历史应保持原顺序");
    }

    private void undoClampsAtZeroAfterManualEdit() {
        // 记入后用户又手动把克数改小了，撤销不能把当日减成负数。
        DayFoodLog log = new DayFoodLog();
        log.record(entry("一份炒饭", 600, 15, 3, "", FoodGroup.GRAIN, 100));
        log.setGrams(FoodGroup.GRAIN, 20);
        log.undo(0);
        assertTrue(log.grams(FoodGroup.GRAIN) == 0,
                "减过头应停在 0，实际 " + log.grams(FoodGroup.GRAIN));

        DayFoodLog twice = new DayFoodLog();
        twice.record(entry("A", 300, 10, 2, "", FoodGroup.GRAIN, 50));
        twice.record(entry("B", 300, 10, 2, "", FoodGroup.GRAIN, 50));
        twice.undo(0);
        twice.undo(0);
        assertTrue(twice.kcal() == 0 && twice.protein() == 0 && twice.fiber() == 0
                        && twice.grams(FoodGroup.GRAIN) == 0,
                "全部撤销后应回到空白，实际 " + twice.kcal() + " kcal");
    }

    private void undoRemovesOneRecipeIdPerEntry() {
        DayFoodLog log = new DayFoodLog();
        log.record(entry("鸡胸沙拉", 350, 30, 6, "chicken_salad", FoodGroup.ANIMAL, 120));
        log.record(entry("鸡胸沙拉", 350, 30, 6, "chicken_salad", FoodGroup.ANIMAL, 120));
        log.undo(0);
        assertTrue(log.recipeIds().size() == 1 && log.recipeIds().get(0).equals("chicken_salad"),
                "吃两份撤一份应仍留一份，实际 " + log.recipeIds());
        assertTrue(log.grams(FoodGroup.ANIMAL) == 120, "另一份的克数应保留");
    }

    private void undoIgnoresOutOfRangeIndex() {
        DayFoodLog log = new DayFoodLog();
        log.record(entry("早餐", 400, 20, 5, "", FoodGroup.GRAIN, 60));
        assertTrue(log.undo(3) == null && log.undo(-1) == null, "越界撤销应返回 null");
        assertTrue(log.kcal() == 400 && log.entries().size() == 1, "越界撤销不应改动任何数据");
    }

    private void manualEditsStayOutOfHistory() {
        // ± 和「点数字设为」本身就能改回去，进历史只会把真正需要撤销的那几笔淹掉。
        DayFoodLog log = new DayFoodLog();
        log.addGrams(FoodGroup.VEGETABLE, 50);
        log.setGrams(FoodGroup.FRUIT, 200);
        log.addWaterMl(250);
        log.setWaterMl(330);
        assertTrue(log.entries().isEmpty(), "手动微调不应产生撤销记录");
        assertTrue(log.grams(FoodGroup.VEGETABLE) == 50 && log.grams(FoodGroup.FRUIT) == 200
                        && log.waterMl() == 330, "饮水应能设为任意毫升数");
        log.addGrams(FoodGroup.VEGETABLE, -500);
        assertTrue(log.grams(FoodGroup.VEGETABLE) == 0, "− 按钮减过头应停在 0");
        log.setWaterMl(-100);
        assertTrue(log.waterMl() == 0, "饮水不能被设为负数");
    }

    private void historyIsCappedButTotalsAreNot() {
        DayFoodLog log = new DayFoodLog();
        for (int i = 0; i < DayFoodLog.MAX_ENTRIES + 5; i++) {
            log.record(entry("第" + i + "笔", 10, 1, 1, "", FoodGroup.GRAIN, 1));
        }
        assertTrue(log.entries().size() == DayFoodLog.MAX_ENTRIES,
                "历史应封顶在 " + DayFoodLog.MAX_ENTRIES + "，实际 " + log.entries().size());
        assertTrue(log.kcal() == (DayFoodLog.MAX_ENTRIES + 5) * 10,
                "封顶只丢历史，总量必须照常累加，实际 " + log.kcal());
        assertTrue(log.entries().get(0).label().equals("第5笔"), "丢的应是最早的几笔");
    }

    private void restoreDoesNotDoubleCount() {
        // 读存档时总量已经存好了，历史只是放回去，不能再累加一遍。
        DayFoodLog log = new DayFoodLog();
        log.restoreTotals(700, 40, 9, 1000);
        log.setGrams(FoodGroup.GRAIN, 120);
        log.restoreRecipeId("oat_milk");
        log.restoreEntry(entry("燕麦牛奶碗", 420, 22, 6, "oat_milk", FoodGroup.GRAIN, 60));
        assertTrue(log.kcal() == 700 && log.protein() == 40 && log.fiber() == 9
                        && log.waterMl() == 1000, "恢复历史不应改动总量");
        assertTrue(log.grams(FoodGroup.GRAIN) == 120, "恢复历史不应改动克数");
        assertTrue(log.entries().size() == 1 && log.recipeIds().size() == 1,
                "恢复后应能继续撤销");

        log.undo(0);
        assertTrue(log.kcal() == 280 && log.grams(FoodGroup.GRAIN) == 60,
                "重启后撤销仍应精确减回，实际 " + log.kcal() + " kcal / "
                        + log.grams(FoodGroup.GRAIN) + "g");
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
