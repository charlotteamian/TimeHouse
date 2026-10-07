package com.restartday.fitness.domain;

public enum Intensity {
    LOW("低", 4, 25),
    MEDIUM("中", 6, 40),
    HIGH("高", 8, 55);

    private final String label;
    private final int maxExercises;
    private final int estimatedMinutes;

    Intensity(String label, int maxExercises, int estimatedMinutes) {
        this.label = label;
        this.maxExercises = maxExercises;
        this.estimatedMinutes = estimatedMinutes;
    }

    public String label() {
        return label;
    }

    public int maxExercises() {
        return maxExercises;
    }

    public int estimatedMinutes() {
        return estimatedMinutes;
    }
}
