package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * 一份完整的周期训练计划：目标 × 水平 × 每周天数 → 分阶段 + 每周分化。
 * 只描述「结构」；某天的具体动作在开练时由推荐引擎按当日部位生成，
 * 这样伤痛、器械、证据过滤始终生效。
 */
public final class TrainingProgram {
    private final PlanGoal goal;
    private final TrainingLevel level;
    private final int daysPerWeek;
    private final int totalWeeks;
    private final List<ProgramPhase> phases;
    private final List<ProgramFocus> weekSplit;   // 每周各训练日的分工，长度 == daysPerWeek
    private final String splitName;
    private final String progressionRule;
    private final List<String> refs;

    public TrainingProgram(PlanGoal goal, TrainingLevel level, int daysPerWeek, int totalWeeks,
            List<ProgramPhase> phases, List<ProgramFocus> weekSplit, String splitName,
            String progressionRule, List<String> refs) {
        this.goal = goal;
        this.level = level;
        this.daysPerWeek = daysPerWeek;
        this.totalWeeks = totalWeeks;
        this.phases = Collections.unmodifiableList(new ArrayList<ProgramPhase>(phases));
        this.weekSplit = Collections.unmodifiableList(new ArrayList<ProgramFocus>(weekSplit));
        this.splitName = splitName;
        this.progressionRule = progressionRule;
        this.refs = Collections.unmodifiableList(new ArrayList<String>(refs));
    }

    public PlanGoal goal() {
        return goal;
    }

    public TrainingLevel level() {
        return level;
    }

    public int daysPerWeek() {
        return daysPerWeek;
    }

    public int totalWeeks() {
        return totalWeeks;
    }

    public List<ProgramPhase> phases() {
        return phases;
    }

    public List<ProgramFocus> weekSplit() {
        return weekSplit;
    }

    public String splitName() {
        return splitName;
    }

    public String progressionRule() {
        return progressionRule;
    }

    public List<String> refs() {
        return refs;
    }

    public ProgramPhase phaseForWeek(int week1Based) {
        for (ProgramPhase phase : phases) {
            if (phase.containsWeek(week1Based)) {
                return phase;
            }
        }
        return phases.get(phases.size() - 1);
    }

    public ProgramFocus focusForDay(int dayIndex0Based) {
        return weekSplit.get(Math.max(0, Math.min(weekSplit.size() - 1, dayIndex0Based)));
    }

    public int totalSessions() {
        return totalWeeks * daysPerWeek;
    }

    public String title() {
        return goal.label() + " · " + totalWeeks + " 周周期计划";
    }
}
