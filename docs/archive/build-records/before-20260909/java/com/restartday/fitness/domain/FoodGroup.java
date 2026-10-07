package com.restartday.fitness.domain;

/**
 * 平衡膳食宝塔（中国居民膳食指南 2022）的食物类别。
 * min/max 为指南给出的成人每日推荐区间（克，奶类含液态奶当量；水单独处理）。
 */
public enum FoodGroup {
    GRAIN("谷类", 200, 300, 25, "米饭面条馒头，面包饼干也算"),
    WHOLE_GRAIN("全谷物和杂豆", 50, 150, 25, "糙米燕麦玉米红豆，是谷类的一部分"),
    TUBER("薯类", 50, 100, 50, "红薯、土豆、山药、芋头"),
    VEGETABLE("蔬菜", 300, 500, 50, "深色蔬菜占一半"),
    FRUIT("水果", 200, 350, 50, "整果优先，果汁不算"),
    ANIMAL("鱼禽肉蛋", 120, 200, 25, "鱼虾禽畜蛋，火腿肠等也算"),
    DAIRY("奶及奶制品", 300, 500, 100, "牛奶、酸奶、奶酪折算"),
    SOY_NUT("大豆及坚果", 25, 35, 5, "豆腐豆浆折大豆，坚果一小把"),
    OIL("烹调油", 25, 30, 5, "控制煎炸，少油烹调"),
    /** 宝塔之外的额外热量：无正向目标，只作提醒记录。 */
    OTHER("零食·其他", 0, 0, 50, "含糖饮料糕点糖果酒，宝塔外尽量少");

    private final String label;
    private final int minGrams;
    private final int maxGrams;
    private final int stepGrams;
    private final String hint;

    FoodGroup(String label, int minGrams, int maxGrams, int stepGrams, String hint) {
        this.label = label;
        this.minGrams = minGrams;
        this.maxGrams = maxGrams;
        this.stepGrams = stepGrams;
        this.hint = hint;
    }

    public String label() {
        return label;
    }

    public int minGrams() {
        return minGrams;
    }

    public int maxGrams() {
        return maxGrams;
    }

    /** ± 快速加减的默认步长（克）。 */
    public int stepGrams() {
        return stepGrams;
    }

    public String hint() {
        return hint;
    }

    public static FoodGroup parse(String name, FoodGroup fallback) {
        for (FoodGroup group : values()) {
            if (group.name().equals(name)) {
                return group;
            }
        }
        return fallback;
    }
}
