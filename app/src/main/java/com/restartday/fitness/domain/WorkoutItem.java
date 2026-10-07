package com.restartday.fitness.domain;

public final class WorkoutItem {
    private final Exercise exercise;
    private final Prescription prescription;
    private final boolean favorite;
    private final String reason;
    private final int restAfterSeconds;
    private final String weight;

    public WorkoutItem(Exercise exercise, Prescription prescription, boolean favorite, String reason) {
        this(exercise, prescription, favorite, reason, 0);
    }

    public WorkoutItem(Exercise exercise, Prescription prescription, boolean favorite, String reason, int restAfterSeconds) {
        this(exercise, prescription, favorite, reason, restAfterSeconds, "");
    }

    public WorkoutItem(Exercise exercise, Prescription prescription, boolean favorite, String reason, int restAfterSeconds, String weight) {
        this.weight = weight == null ? "" : weight.trim();
        this.restAfterSeconds = Math.max(0, restAfterSeconds);
        this.exercise = exercise;
        this.prescription = prescription;
        this.favorite = favorite;
        this.reason = reason;
    }

    public String weight() { return weight; }

    public int restAfterSeconds() { return restAfterSeconds; }

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
