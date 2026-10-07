package com.restartday.fitness.domain;

/** 周期计划的训练目标。参数依据见 GuidelineRefs。 */
public enum PlanGoal {
    MUSCLE_GAIN("增肌", "以肌肥大为主：每肌群每周 2 次以上，8-12 次/组为主，逐步加量"),
    FAT_LOSS("减脂", "抗阻保肌 + 有氧扩大消耗：力量维持强度，配合每周 150-300 分钟有氧"),
    STRENGTH("力量", "以最大力量为主：多关节动作优先，4-8 次/组，休息更充分"),
    GENERAL_FITNESS("健康体适能", "力量 + 有氧 + 柔韧均衡，达到身体活动指南的基础推荐量");

    private final String label;
    private final String summary;

    PlanGoal(String label, String summary) {
        this.label = label;
        this.summary = summary;
    }

    public String label() {
        return label;
    }

    public String summary() {
        return summary;
    }

    public static PlanGoal parse(String name, PlanGoal fallback) {
        for (PlanGoal goal : values()) {
            if (goal.name().equals(name)) {
                return goal;
            }
        }
        return fallback;
    }
}
