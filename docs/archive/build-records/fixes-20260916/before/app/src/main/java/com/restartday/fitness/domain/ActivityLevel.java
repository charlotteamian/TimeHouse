package com.restartday.fitness.domain;

/** 日常活动水平（用于 TDEE 估算的活动系数，通用范围 1.2-1.9）。 */
public enum ActivityLevel {
    SEDENTARY("久坐", "办公为主，几乎不运动", 1.2),
    LIGHT("轻度活动", "每周运动 1-3 次或走动较多", 1.375),
    MODERATE("中度活动", "每周运动 3-5 次", 1.55),
    ACTIVE("高度活动", "每周运动 6-7 次或体力工作", 1.725),
    VERY_ACTIVE("极高活动", "每天高强度训练或重体力劳动", 1.9);

    private final String label;
    private final String description;
    private final double factor;

    ActivityLevel(String label, String description, double factor) {
        this.label = label;
        this.description = description;
        this.factor = factor;
    }

    public String label() {
        return label;
    }

    public String description() {
        return description;
    }

    public double factor() {
        return factor;
    }

    public static ActivityLevel parse(String name, ActivityLevel fallback) {
        for (ActivityLevel level : values()) {
            if (level.name().equals(name)) {
                return level;
            }
        }
        return fallback;
    }
}
