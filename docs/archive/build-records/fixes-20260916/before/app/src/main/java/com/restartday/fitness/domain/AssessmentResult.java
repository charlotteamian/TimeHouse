package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 状态评估结论：训练水平 + 强度上限 + 说明与依据。 */
public final class AssessmentResult {
    private final TrainingLevel level;
    private final Intensity intensityCap;
    private final boolean medicalClearanceAdvised;
    private final List<String> notes;
    private final List<String> refs;

    public AssessmentResult(TrainingLevel level, Intensity intensityCap,
            boolean medicalClearanceAdvised, List<String> notes, List<String> refs) {
        this.level = level;
        this.intensityCap = intensityCap;
        this.medicalClearanceAdvised = medicalClearanceAdvised;
        this.notes = Collections.unmodifiableList(new ArrayList<String>(notes));
        this.refs = Collections.unmodifiableList(new ArrayList<String>(refs));
    }

    public TrainingLevel level() {
        return level;
    }

    public Intensity intensityCap() {
        return intensityCap;
    }

    public boolean medicalClearanceAdvised() {
        return medicalClearanceAdvised;
    }

    public List<String> notes() {
        return notes;
    }

    public List<String> refs() {
        return refs;
    }
}
