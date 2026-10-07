package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 每日能量与营养素目标（含出处），由 NutritionPlanner 计算。 */
public final class EnergyPlan {
    private final int bmrKcal;
    private final int tdeeKcal;
    private final int targetKcal;
    private final int proteinG;
    private final double proteinPerKg;
    private final int fatG;
    private final int carbG;
    private final int fiberMinG;
    private final int fiberMaxG;
    private final int waterMinMl;
    private final int waterMaxMl;
    private final List<String> notes;
    private final List<String> refs;

    public EnergyPlan(int bmrKcal, int tdeeKcal, int targetKcal, int proteinG, double proteinPerKg,
            int fatG, int carbG, int fiberMinG, int fiberMaxG, int waterMinMl, int waterMaxMl,
            List<String> notes, List<String> refs) {
        this.bmrKcal = bmrKcal;
        this.tdeeKcal = tdeeKcal;
        this.targetKcal = targetKcal;
        this.proteinG = proteinG;
        this.proteinPerKg = proteinPerKg;
        this.fatG = fatG;
        this.carbG = carbG;
        this.fiberMinG = fiberMinG;
        this.fiberMaxG = fiberMaxG;
        this.waterMinMl = waterMinMl;
        this.waterMaxMl = waterMaxMl;
        this.notes = Collections.unmodifiableList(new ArrayList<String>(notes));
        this.refs = Collections.unmodifiableList(new ArrayList<String>(refs));
    }

    public int bmrKcal() {
        return bmrKcal;
    }

    public int tdeeKcal() {
        return tdeeKcal;
    }

    public int targetKcal() {
        return targetKcal;
    }

    public int proteinG() {
        return proteinG;
    }

    public double proteinPerKg() {
        return proteinPerKg;
    }

    public int fatG() {
        return fatG;
    }

    public int carbG() {
        return carbG;
    }

    public int fiberMinG() {
        return fiberMinG;
    }

    public int fiberMaxG() {
        return fiberMaxG;
    }

    public int waterMinMl() {
        return waterMinMl;
    }

    public int waterMaxMl() {
        return waterMaxMl;
    }

    public List<String> notes() {
        return notes;
    }

    public List<String> refs() {
        return refs;
    }
}
