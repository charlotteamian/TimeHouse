package com.restartday.fitness.domain;

/** 营养档案：能量与营养素目标的全部输入。 */
public final class NutritionProfile {
    private final boolean male;
    private final int age;
    private final double heightCm;
    private final double weightKg;
    private final ActivityLevel activity;
    private final PlanGoal goal;

    public NutritionProfile(boolean male, int age, double heightCm, double weightKg,
            ActivityLevel activity, PlanGoal goal) {
        this.male = male;
        this.age = Math.max(16, Math.min(80, age));
        this.heightCm = Math.max(120, Math.min(220, heightCm));
        this.weightKg = Math.max(35, Math.min(200, weightKg));
        this.activity = activity == null ? ActivityLevel.LIGHT : activity;
        this.goal = goal == null ? PlanGoal.GENERAL_FITNESS : goal;
    }

    public boolean male() {
        return male;
    }

    public int age() {
        return age;
    }

    public double heightCm() {
        return heightCm;
    }

    public double weightKg() {
        return weightKg;
    }

    public ActivityLevel activity() {
        return activity;
    }

    public PlanGoal goal() {
        return goal;
    }

    public double bmi() {
        double meters = heightCm / 100.0;
        return weightKg / (meters * meters);
    }
}
