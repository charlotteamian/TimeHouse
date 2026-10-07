package com.restartday.fitness.domain;

/** 训练水平分级，由状态评估得出，决定周期计划的起始强度与进阶速度。 */
public enum TrainingLevel {
    BEGINNER("初级", "规律训练不足 6 个月：先建立动作模式，从低强度起步"),
    INTERMEDIATE("中级", "规律训练 6 个月至 2 年：可承受标准训练量与渐进负荷"),
    ADVANCED("高级", "规律训练 2 年以上：可使用更高强度与更大周训练量");

    private final String label;
    private final String summary;

    TrainingLevel(String label, String summary) {
        this.label = label;
        this.summary = summary;
    }

    public String label() {
        return label;
    }

    public String summary() {
        return summary;
    }

    public static TrainingLevel parse(String name, TrainingLevel fallback) {
        for (TrainingLevel level : values()) {
            if (level.name().equals(name)) {
                return level;
            }
        }
        return fallback;
    }
}
