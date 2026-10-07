package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public final class RecommendationInput {
    private final String intentText;
    private final boolean unknownWorkout;
    private final Intensity intensity;
    private final int targetMinutes;
    private final List<String> equipment;
    private final List<PainPoint> painPoints;
    private final Set<String> favoriteExercises;
    private final Set<String> verifiedExercises;
    private final boolean includeUserUnverified;
    private final List<String> recentExerciseIds;
    private final double paceFactor;

    private RecommendationInput(Builder builder) {
        intentText = builder.intentText;
        unknownWorkout = builder.unknownWorkout;
        intensity = builder.intensity;
        targetMinutes = builder.targetMinutesSet ? builder.targetMinutes : intensity.estimatedMinutes();
        equipment = Collections.unmodifiableList(new ArrayList<String>(builder.equipment));
        painPoints = Collections.unmodifiableList(new ArrayList<PainPoint>(builder.painPoints));
        favoriteExercises = Collections.unmodifiableSet(new HashSet<String>(builder.favoriteExercises));
        verifiedExercises = Collections.unmodifiableSet(new HashSet<String>(builder.verifiedExercises));
        includeUserUnverified = builder.includeUserUnverified;
        recentExerciseIds = Collections.unmodifiableList(new ArrayList<String>(builder.recentExerciseIds));
        paceFactor = builder.paceFactor;
    }

    public String intentText() {
        return intentText;
    }

    public boolean unknownWorkout() {
        return unknownWorkout;
    }

    public Intensity intensity() {
        return intensity;
    }

    public int targetMinutes() {
        return targetMinutes;
    }

    public List<String> equipment() {
        return equipment;
    }

    public List<PainPoint> painPoints() {
        return painPoints;
    }

    public Set<String> favoriteExercises() {
        return favoriteExercises;
    }

    public Set<String> verifiedExercises() {
        return verifiedExercises;
    }

    public boolean includeUserUnverified() {
        return includeUserUnverified;
    }

    /** 最近练过的动作 id，按时间倒序（下标 0 = 最近一次）。用于避开刚练过的动作。 */
    public List<String> recentExerciseIds() {
        return recentExerciseIds;
    }

    /** 个人化的节奏系数，喂给 {@link SessionTimeModel} 让时长估算贴合本人实际。 */
    public double paceFactor() {
        return paceFactor;
    }

    public static final class Builder {
        private String intentText = "";
        private boolean unknownWorkout;
        private Intensity intensity = Intensity.MEDIUM;
        private int targetMinutes = Intensity.MEDIUM.estimatedMinutes();
        private boolean targetMinutesSet;
        private final List<String> equipment = new ArrayList<String>();
        private final List<PainPoint> painPoints = new ArrayList<PainPoint>();
        private Set<String> favoriteExercises = new HashSet<String>();
        private Set<String> verifiedExercises = new HashSet<String>();
        private boolean includeUserUnverified;
        private final List<String> recentExerciseIds = new ArrayList<String>();
        private double paceFactor = 1.0;

        public Builder intentText(String value) {
            intentText = value == null ? "" : value;
            return this;
        }

        public Builder unknownWorkout() {
            unknownWorkout = true;
            return this;
        }

        public Builder intensity(Intensity value) {
            intensity = value == null ? Intensity.MEDIUM : value;
            return this;
        }

        public Builder targetMinutes(int value) {
            if (value <= 0) {
                targetMinutes = 0;
            } else if (value <= 5) {
                targetMinutes = 5;
            } else if (value <= 15) {
                targetMinutes = 15;
            } else if (value <= 25) {
                targetMinutes = 25;
            } else if (value <= 40) {
                targetMinutes = 40;
            } else {
                targetMinutes = 55;
            }
            targetMinutesSet = true;
            return this;
        }

        public Builder equipment(String... values) {
            for (String value : values) {
                equipment.add(value);
            }
            return this;
        }

        public Builder pain(PainPoint value) {
            painPoints.add(value);
            return this;
        }

        public Builder favoriteExercises(Set<String> values) {
            favoriteExercises = values == null ? new HashSet<String>() : values;
            return this;
        }

        public Builder verifiedExercises(Set<String> values) {
            verifiedExercises = values == null ? new HashSet<String>() : values;
            return this;
        }

        public Builder includeUserUnverified(boolean value) {
            includeUserUnverified = value;
            return this;
        }

        /** @param values 最近练过的动作 id，按时间倒序 */
        public Builder recentExerciseIds(List<String> values) {
            recentExerciseIds.clear();
            if (values != null) {
                recentExerciseIds.addAll(values);
            }
            return this;
        }

        public Builder paceFactor(double value) {
            paceFactor = value;
            return this;
        }

        public RecommendationInput build() {
            return new RecommendationInput(this);
        }
    }
}
