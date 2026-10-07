package com.restartday.fitness.domain;

public enum StressLevel {
    NONE(0, "无"),
    LOW(1, "低"),
    MEDIUM(2, "中"),
    HIGH(3, "高");

    private final int weight;
    private final String label;

    StressLevel(int weight, String label) {
        this.weight = weight;
        this.label = label;
    }

    public boolean isAtLeast(StressLevel other) {
        return weight >= other.weight;
    }

    public String label() {
        return label;
    }
}
