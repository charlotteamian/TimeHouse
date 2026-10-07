package com.restartday.fitness.domain;

/**
 * 周期计划中的一个阶段：给出该阶段力量课的统一处方（组×次@RPE、休息）、
 * 引擎强度档、每周有氧目标与说明。
 */
public final class ProgramPhase {
    private final String key;              // ADAPT / DEVELOP / INTENSIFY / DELOAD
    private final String name;
    private final int startWeek;           // 1-based，含
    private final int endWeek;             // 1-based，含
    private final Prescription prescription;
    private final Intensity intensity;     // 喂给推荐引擎的强度档
    private final int aerobicMinutesPerWeek;
    private final String aerobicNote;
    private final String description;

    public ProgramPhase(String key, String name, int startWeek, int endWeek,
            Prescription prescription, Intensity intensity,
            int aerobicMinutesPerWeek, String aerobicNote, String description) {
        this.key = key;
        this.name = name;
        this.startWeek = startWeek;
        this.endWeek = endWeek;
        this.prescription = prescription;
        this.intensity = intensity;
        this.aerobicMinutesPerWeek = aerobicMinutesPerWeek;
        this.aerobicNote = aerobicNote;
        this.description = description;
    }

    public String key() {
        return key;
    }

    public String name() {
        return name;
    }

    public int startWeek() {
        return startWeek;
    }

    public int endWeek() {
        return endWeek;
    }

    public boolean containsWeek(int week1Based) {
        return week1Based >= startWeek && week1Based <= endWeek;
    }

    public Prescription prescription() {
        return prescription;
    }

    public Intensity intensity() {
        return intensity;
    }

    public int aerobicMinutesPerWeek() {
        return aerobicMinutesPerWeek;
    }

    public String aerobicNote() {
        return aerobicNote;
    }

    public String description() {
        return description;
    }

    public String weeksLabel() {
        return startWeek == endWeek
                ? "第 " + startWeek + " 周"
                : "第 " + startWeek + "-" + endWeek + " 周";
    }
}
