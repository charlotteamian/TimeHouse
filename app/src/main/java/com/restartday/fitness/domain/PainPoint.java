package com.restartday.fitness.domain;

public final class PainPoint {
    private final String jointKey;
    private final String displayName;
    private final PainSeverity severity;

    private PainPoint(String jointKey, String displayName, PainSeverity severity) {
        this.jointKey = jointKey;
        this.displayName = displayName;
        this.severity = severity;
    }

    public static PainPoint shoulder(PainSeverity severity) {
        return new PainPoint("shoulder", "肩", severity);
    }

    public static PainPoint lowerBack(PainSeverity severity) {
        return new PainPoint("lower_back", "腰", severity);
    }

    public static PainPoint knee(PainSeverity severity) {
        return new PainPoint("knee", "膝", severity);
    }

    public String jointKey() {
        return jointKey;
    }

    public String displayName() {
        return displayName;
    }

    public PainSeverity severity() {
        return severity;
    }
}
