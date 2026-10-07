package com.restartday.fitness.domain;

import java.util.List;

/**
 * 一次训练要花多少时间——正向算出来，而不是回显用户输入的数字。
 *
 * <p>算的是「主课净时长」：从点开始到最后一组结束。热身和放松只作为建议分钟数单独给出，
 * 不混进估算——App 目前不引导热身/放松，混进去会让"预计"和秒表读数永远对不上，
 * 也就没法用实测数据反过来校准。
 *
 * <p>{@code paceFactor} 是按人校准的系数：每次完整完成的训练都会把
 * 「预计 vs 实际」的偏差平滑进去，跑几次之后估算就不会再偏。
 */
public final class SessionTimeModel {

    /** 换动作、看示范、调器械的固定开销。 */
    public static final int TRANSITION_SECONDS = 25;

    /** 建议热身分钟数（ACSM：5-10 分钟渐进热身，初学者取下限）。 */
    public static final int WARMUP_ADVICE_MINUTES = 4;

    /** 建议放松分钟数。 */
    public static final int COOLDOWN_ADVICE_MINUTES = 3;

    private static final double MIN_PACE = 0.6;
    private static final double MAX_PACE = 1.8;

    /** 新观测在校准里的权重，其余留给历史值，避免一次异常训练把系数带跑。 */
    private static final double CALIBRATION_WEIGHT = 0.3;

    private final double paceFactor;

    public SessionTimeModel() {
        this(1.0);
    }

    public SessionTimeModel(double paceFactor) {
        this.paceFactor = clampPace(paceFactor);
    }

    public double paceFactor() {
        return paceFactor;
    }

    /** 单个动作的耗时：各组工作 + 组间休息 + 一次切换开销。 */
    public int itemSeconds(Prescription prescription) {
        if (prescription == null) {
            return 0;
        }
        int sets = Math.max(1, prescription.sets());
        double work = sets * prescription.workSecondsPerSet();
        double rest = (sets - 1) * Math.max(0, prescription.restSeconds());
        return (int) Math.round((work + rest + TRANSITION_SECONDS) * paceFactor);
    }

    /** 主课净时长（秒），不含热身和放松。 */
    public int sessionSeconds(List<WorkoutItem> items) {
        if (items == null || items.isEmpty()) {
            return 0;
        }
        int total = 0;
        for (WorkoutItem item : items) {
            total += itemSeconds(item.prescription()) + (int) Math.round(item.restAfterSeconds() * paceFactor);
        }
        return total;
    }

    /** 主课净时长（分钟，向上取整）。 */
    public int sessionMinutes(List<WorkoutItem> items) {
        int seconds = sessionSeconds(items);
        return seconds <= 0 ? 0 : Math.max(1, (int) Math.ceil(seconds / 60.0));
    }

    /**
     * 给定时间预算和统一处方，能排下几个动作。
     * 计划课里处方是周期计划定的科学约束不能动，能动的只有动作数量——所以是解这个方向。
     */
    public int fitExerciseCount(int budgetMinutes, Prescription prescription, int min, int max) {
        int lower = Math.max(1, min);
        int upper = Math.max(lower, max);
        if (budgetMinutes <= 0) {
            return upper;
        }
        int per = itemSeconds(prescription);
        if (per <= 0) {
            return lower;
        }
        int count = (budgetMinutes * 60) / per;
        return Math.max(lower, Math.min(upper, count));
    }

    /** "主课 11 分钟（4 个动作 · 含组间休息 4 分钟）" 里的休息合计分钟数。 */
    public int restMinutes(List<WorkoutItem> items) {
        if (items == null || items.isEmpty()) {
            return 0;
        }
        double seconds = 0;
        for (WorkoutItem item : items) {
            Prescription prescription = item.prescription();
            int sets = Math.max(1, prescription.sets());
            seconds += item.restAfterSeconds();
            seconds += (sets - 1) * Math.max(0, prescription.restSeconds());
        }
        return (int) Math.round(seconds * paceFactor / 60.0);
    }

    /**
     * 用一次完整训练的实测时长校准节奏系数。
     * 只应在动作全部完成时调用——中途放弃的训练会把系数带得偏小。
     */
    public static double calibrated(double current, int predictedSeconds, int actualSeconds) {
        if (predictedSeconds <= 0 || actualSeconds <= 0) {
            return clampPace(current);
        }
        double base = clampPace(current);
        double observed = base * ((double) actualSeconds / predictedSeconds);
        return clampPace(base * (1 - CALIBRATION_WEIGHT) + observed * CALIBRATION_WEIGHT);
    }

    private static double clampPace(double value) {
        if (Double.isNaN(value) || value <= 0) {
            return 1.0;
        }
        return Math.max(MIN_PACE, Math.min(MAX_PACE, value));
    }
}
