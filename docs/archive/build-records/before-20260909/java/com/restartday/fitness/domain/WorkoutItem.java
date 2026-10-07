package com.restartday.fitness.domain;

public final class WorkoutItem {
    private final Exercise exercise;
    private final Prescription prescription;
    private final boolean favorite;
    private final String reason;

    public WorkoutItem(Exercise exercise, Prescription prescription, boolean favorite, String reason) {
        this.exercise = exercise;
        this.prescription = prescription;
        this.favorite = favorite;
        this.reason = reason;
    }

    public Exercise exercise() {
        return exercise;
    }

    public Prescription prescription() {
        return prescription;
    }

    public boolean favorite() {
        return favorite;
    }

    public String reason() {
        return reason;
    }
}
