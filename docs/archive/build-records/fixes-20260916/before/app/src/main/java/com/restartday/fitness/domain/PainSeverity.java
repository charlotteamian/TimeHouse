package com.restartday.fitness.domain;

public enum PainSeverity {
    MILD("轻微"),
    MODERATE("明显"),
    SEVERE("急性/严重");

    private final String label;

    PainSeverity(String label) {
        this.label = label;
    }

    public String label() {
        return label;
    }
}
