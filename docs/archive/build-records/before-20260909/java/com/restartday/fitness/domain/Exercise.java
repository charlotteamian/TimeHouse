package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class Exercise {
    private final String id;
    private final String name;
    private final EvidenceStatus evidenceStatus;
    private final List<String> targetRegions;
    private final List<String> movementPatterns;
    private final List<String> equipment;
    private final List<String> primaryMuscles;
    private final List<String> secondaryMuscles;
    private final String difficulty;
    private final Map<String, StressLevel> jointStressTags;
    private final List<String> instructions;
    private final List<String> commonMistakes;
    private final List<String> substitutions;
    private final List<String> evidenceRefs;
    private final Map<Intensity, Prescription> prescriptions;
    private final String media;
    private final String source;

    private Exercise(Builder builder) {
        id = builder.id;
        name = builder.name;
        evidenceStatus = builder.evidenceStatus;
        media = builder.media;
        targetRegions = immutableCopy(builder.targetRegions);
        movementPatterns = immutableCopy(builder.movementPatterns);
        equipment = immutableCopy(builder.equipment);
        primaryMuscles = immutableCopy(builder.primaryMuscles);
        secondaryMuscles = immutableCopy(builder.secondaryMuscles);
        difficulty = builder.difficulty;
        jointStressTags = Collections.unmodifiableMap(new HashMap<String, StressLevel>(builder.jointStressTags));
        instructions = immutableCopy(builder.instructions);
        commonMistakes = immutableCopy(builder.commonMistakes);
        substitutions = immutableCopy(builder.substitutions);
        evidenceRefs = immutableCopy(builder.evidenceRefs);
        prescriptions = Collections.unmodifiableMap(new EnumMap<Intensity, Prescription>(builder.prescriptions));
        source = builder.source;
    }

    public String id() {
        return id;
    }

    public String name() {
        return name;
    }

    public EvidenceStatus evidenceStatus() {
        return evidenceStatus;
    }

    public String media() {
        return media;
    }

    public boolean hasMedia() {
        return media != null && media.length() > 0;
    }

    public List<String> targetRegions() {
        return targetRegions;
    }

    public List<String> movementPatterns() {
        return movementPatterns;
    }

    public List<String> equipment() {
        return equipment;
    }

    public List<String> primaryMuscles() {
        return primaryMuscles;
    }

    public List<String> secondaryMuscles() {
        return secondaryMuscles;
    }

    public String difficulty() {
        return difficulty;
    }

    public String source() {
        return source;
    }

    public StressLevel jointStress(String jointKey) {
        StressLevel level = jointStressTags.get(jointKey);
        return level == null ? StressLevel.NONE : level;
    }

    public List<String> instructions() {
        return instructions;
    }

    public List<String> commonMistakes() {
        return commonMistakes;
    }

    public List<String> substitutions() {
        return substitutions;
    }

    public List<String> evidenceRefs() {
        return evidenceRefs;
    }

    public Prescription prescription(Intensity intensity) {
        Prescription prescription = prescriptions.get(intensity);
        return prescription == null ? prescriptions.get(Intensity.MEDIUM) : prescription;
    }

    public boolean matchesAnyRegion(List<String> regions) {
        for (String region : regions) {
            if (targetRegions.contains(region)) {
                return true;
            }
        }
        return false;
    }

    public boolean matchesAnyPattern(List<String> patterns) {
        for (String pattern : patterns) {
            if (movementPatterns.contains(pattern)) {
                return true;
            }
        }
        return false;
    }

    public boolean hasAvailableEquipment(List<String> availableEquipment) {
        if (availableEquipment.isEmpty()) {
            return true;
        }
        for (String item : equipment) {
            if (availableEquipment.contains(item)) {
                return true;
            }
        }
        return false;
    }

    private static List<String> immutableCopy(List<String> source) {
        return Collections.unmodifiableList(new ArrayList<String>(source));
    }

    public static final class Builder {
        private final String id;
        private final String name;
        private EvidenceStatus evidenceStatus = EvidenceStatus.GUIDELINE_BACKED;
        private final List<String> targetRegions = new ArrayList<String>();
        private final List<String> movementPatterns = new ArrayList<String>();
        private final List<String> equipment = new ArrayList<String>();
        private final List<String> primaryMuscles = new ArrayList<String>();
        private final List<String> secondaryMuscles = new ArrayList<String>();
        private String difficulty = "beginner";
        private String media = "";
        private String source = "";
        private final Map<String, StressLevel> jointStressTags = new HashMap<String, StressLevel>();
        private final List<String> instructions = new ArrayList<String>();
        private final List<String> commonMistakes = new ArrayList<String>();
        private final List<String> substitutions = new ArrayList<String>();
        private final List<String> evidenceRefs = new ArrayList<String>();
        private final Map<Intensity, Prescription> prescriptions = new EnumMap<Intensity, Prescription>(Intensity.class);

        public Builder(String id, String name) {
            this.id = id;
            this.name = name;
        }

        public Builder evidence(EvidenceStatus value) {
            evidenceStatus = value;
            return this;
        }

        public Builder regions(String... values) {
            addAll(targetRegions, values);
            return this;
        }

        public Builder patterns(String... values) {
            addAll(movementPatterns, values);
            return this;
        }

        public Builder equipment(String... values) {
            addAll(equipment, values);
            return this;
        }

        public Builder primaryMuscles(String... values) {
            addAll(primaryMuscles, values);
            return this;
        }

        public Builder secondaryMuscles(String... values) {
            addAll(secondaryMuscles, values);
            return this;
        }

        public Builder difficulty(String value) {
            difficulty = value;
            return this;
        }

        public Builder media(String value) {
            media = value == null ? "" : value;
            return this;
        }

        public Builder source(String value) {
            source = value == null ? "" : value;
            return this;
        }

        public Builder stress(String jointKey, StressLevel level) {
            jointStressTags.put(jointKey, level);
            return this;
        }

        public Builder instructions(String... values) {
            addAll(instructions, values);
            return this;
        }

        public Builder mistakes(String... values) {
            addAll(commonMistakes, values);
            return this;
        }

        public Builder substitutions(String... values) {
            addAll(substitutions, values);
            return this;
        }

        public Builder evidenceRefs(String... values) {
            addAll(evidenceRefs, values);
            return this;
        }

        public Builder prescriptions(Prescription low, Prescription medium, Prescription high) {
            prescriptions.put(Intensity.LOW, low);
            prescriptions.put(Intensity.MEDIUM, medium);
            prescriptions.put(Intensity.HIGH, high);
            return this;
        }

        public Exercise build() {
            if (prescriptions.isEmpty()) {
                prescriptions(new Prescription(2, "10-12", "5-6", 75),
                        new Prescription(3, "8-12", "6-8", 90),
                        new Prescription(4, "6-10", "7-8", 120));
            }
            return new Exercise(this);
        }

        private static void addAll(List<String> target, String[] values) {
            for (String value : values) {
                target.add(value);
            }
        }
    }
}
