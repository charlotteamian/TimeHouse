package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * 一天的饮食记录：宝塔各类克数 + 已记录食谱的宏量估算 + 饮水，
 * 外加一份「今天记入了哪几笔」的历史，用于撤销点错的那一笔。
 *
 * <p>两种写法分得很清楚：
 * <ul>
 *   <li>{@link #record} —— 一次性确认记入（食谱 / 记一餐），增量进历史，可 {@link #undo}；</li>
 *   <li>{@link #setGrams}、{@link #addGrams}、{@link #addWaterMl} —— 手动微调，
 *       本身就能改回去，不进历史，否则历史会被 ± 按钮刷屏。</li>
 * </ul>
 *
 * <p>所有累计量都夹在 0 以上：撤销时用户可能已经手动把某类改小了，
 * 这时按增量减会减成负数，负的克数和热量对用户没有任何意义。
 */
public final class DayFoodLog {

    /** 一天最多留多少笔可撤销记录：正常一天 3-8 笔，留 30 笔够用又不会撑大存档。 */
    public static final int MAX_ENTRIES = 30;

    private final int[] groups = new int[FoodGroup.values().length];
    private int kcal;
    private int protein;
    private int fiber;
    private int waterMl;
    private final List<String> recipeIds = new ArrayList<String>();
    private final List<FoodLogEntry> entries = new ArrayList<FoodLogEntry>();

    public int grams(FoodGroup group) {
        return groups[group.ordinal()];
    }

    /** 直接设为精确克数（点数字输入用）。 */
    public void setGrams(FoodGroup group, int value) {
        groups[group.ordinal()] = Math.max(0, value);
    }

    /** 加减克数（± 按钮用），减到 0 为止。 */
    public void addGrams(FoodGroup group, int delta) {
        setGrams(group, groups[group.ordinal()] + delta);
    }

    /** 按 {@link FoodGroup#ordinal()} 排列的克数快照，给 {@link RecipeScorer} 打分用。 */
    public int[] gramsByGroup() {
        return groups.clone();
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

    public int waterMl() {
        return waterMl;
    }

    /** 直接设为精确毫升数（点饮水数字输入用）。 */
    public void setWaterMl(int ml) {
        waterMl = Math.max(0, ml);
    }

    public void addWaterMl(int ml) {
        setWaterMl(waterMl + ml);
    }

    /** 今天记入过的内置食谱 id（同一份吃两次会出现两次）。 */
    public List<String> recipeIds() {
        return Collections.unmodifiableList(recipeIds);
    }

    /** 今天的记入历史，按记入先后排列。 */
    public List<FoodLogEntry> entries() {
        return Collections.unmodifiableList(entries);
    }

    /**
     * 确认记入一笔：累加到当日总量，并留一份增量以便撤销。
     * 超过 {@link #MAX_ENTRIES} 时丢掉最早的一笔历史（总量不动，只是那笔不再能撤销）。
     */
    public void record(FoodLogEntry entry) {
        if (entry == null) {
            return;
        }
        kcal += entry.kcal();
        protein += entry.protein();
        fiber += entry.fiber();
        for (Map.Entry<FoodGroup, Integer> part : entry.grams().entrySet()) {
            addGrams(part.getKey(), part.getValue());
        }
        if (entry.recipeId().length() > 0) {
            recipeIds.add(entry.recipeId());
        }
        entries.add(entry);
        while (entries.size() > MAX_ENTRIES) {
            entries.remove(0);
        }
    }

    /**
     * 撤销第 index 笔记录：把它的增量从当日总量里减回去（不减到负数），
     * 并从历史和已吃食谱里移除。
     *
     * @return 被撤销的那笔；下标越界返回 null
     */
    public FoodLogEntry undo(int index) {
        if (index < 0 || index >= entries.size()) {
            return null;
        }
        FoodLogEntry entry = entries.remove(index);
        kcal = Math.max(0, kcal - entry.kcal());
        protein = Math.max(0, protein - entry.protein());
        fiber = Math.max(0, fiber - entry.fiber());
        for (Map.Entry<FoodGroup, Integer> part : entry.grams().entrySet()) {
            addGrams(part.getKey(), -part.getValue());
        }
        if (entry.recipeId().length() > 0) {
            recipeIds.remove(entry.recipeId());   // 只移除一次出现，吃两份撤一份仍留一份
        }
        return entry;
    }

    /** 从存档恢复当日总量（不产生历史，历史用 {@link #restoreEntry} 逐条放回）。 */
    public void restoreTotals(int kcal, int protein, int fiber, int waterMl) {
        this.kcal = Math.max(0, kcal);
        this.protein = Math.max(0, protein);
        this.fiber = Math.max(0, fiber);
        this.waterMl = Math.max(0, waterMl);
    }

    /** 从存档恢复一条已吃食谱 id（总量已在 {@link #restoreTotals} 里，不再累加）。 */
    public void restoreRecipeId(String id) {
        if (id != null && id.length() > 0) {
            recipeIds.add(id);
        }
    }

    /** 从存档恢复一笔历史（只放回历史，不重复累加总量）。 */
    public void restoreEntry(FoodLogEntry entry) {
        if (entry != null && entries.size() < MAX_ENTRIES) {
            entries.add(entry);
        }
    }
}
