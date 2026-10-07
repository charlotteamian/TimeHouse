package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class WorkoutPlan {
    private final String title;
    private final Intensity intensity;
    private final int estimatedMinutes;
    private final List<WorkoutItem> items;
    private final String recommendationReason;
    private final List<String> avoidanceNotes;
    private final String safetyMessage;
    private final boolean safetyLimited;

    public WorkoutPlan(String title,
            Intensity intensity,
            int estimatedMinutes,
            List<WorkoutItem> items,
            String recommendationReason,
            List<String> avoidanceNotes,
            String safetyMessage,
            boolean safetyLimited) {
        this.title = title;
        this.intensity = intensity;
        this.estimatedMinutes = estimatedMinutes;
        this.items = Collections.unmodifiableList(new ArrayList<WorkoutItem>(items));
        this.recommendationReason = recommendationReason;
        this.avoidanceNotes = Collections.unmodifiableList(new ArrayList<String>(avoidanceNotes));
        this.safetyMessage = safetyMessage;
        this.safetyLimited = safetyLimited;
    }

    public String title() {
        return title;
    }

    public Intensity intensity() {
        return intensity;
    }

    public int estimatedMinutes() {
        return estimatedMinutes;
    }

    public List<WorkoutItem> items() {
        return items;
    }

    public String recommendationReason() {
        return recommendationReason;
    }

    public List<String> avoidanceNotes() {
        return avoidanceNotes;
    }

    public String safetyMessage() {
        return safetyMessage;
    }

    public boolean isSafetyLimited() {
        return safetyLimited;
    }
}
