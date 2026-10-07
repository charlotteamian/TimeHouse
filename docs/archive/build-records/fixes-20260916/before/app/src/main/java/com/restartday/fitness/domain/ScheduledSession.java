package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 日历上的一次训练：绑定到具体日期，动作在生成计划时就已排好。 */
public final class ScheduledSession {

    public enum Status {
        /** 还没到、或今天该做。 */
        PLANNED,
        /** 已完成。 */
        DONE,
        /** 用户主动跳过。 */
        SKIPPED,
        /** 日期已过但没练。保持周结构，不顺延。 */
        MISSED
    }

    private final int week;          // 1 基，对应周期计划的第几周（决定阶段处方）
    private final int dayIndex;      // 0 基，本周第几次训练（决定分化）
    private final long epochDay;
    private final ProgramFocus focus;
    private final List<String> exerciseIds;
    private final List<String> slotKeys;
    private final Status status;
    private final boolean repeatWeek;

    public ScheduledSession(int week, int dayIndex, long epochDay, ProgramFocus focus,
            List<String> exerciseIds, List<String> slotKeys, Status status, boolean repeatWeek) {
        this.week = week;
        this.dayIndex = dayIndex;
        this.epochDay = epochDay;
        this.focus = focus;
        this.exerciseIds = immutable(exerciseIds);
        this.slotKeys = immutable(slotKeys);
        this.status = status == null ? Status.PLANNED : status;
        this.repeatWeek = repeatWeek;
    }

    public int week() {
        return week;
    }

    public int dayIndex() {
        return dayIndex;
    }

    public long epochDay() {
        return epochDay;
    }

    public ProgramFocus focus() {
        return focus;
    }

    public List<String> exerciseIds() {
        return exerciseIds;
    }

    public List<String> slotKeys() {
        return slotKeys;
    }

    public Status status() {
        return status;
    }

    /** 是否是「完成率不足自动重做」插进来的一周。 */
    public boolean isRepeatWeek() {
        return repeatWeek;
    }

    public String key() {
        return week + ":" + dayIndex + ":" + epochDay;
    }

    public ScheduledSession withStatus(Status newStatus) {
        return new ScheduledSession(week, dayIndex, epochDay, focus, exerciseIds, slotKeys,
                newStatus, repeatWeek);
    }

    public ScheduledSession withDate(long newEpochDay) {
        return new ScheduledSession(week, dayIndex, newEpochDay, focus, exerciseIds, slotKeys,
                status, repeatWeek);
    }

    /** 替换某个槽位上的动作（用户在当日课表里换动作）。 */
    public ScheduledSession withExerciseAt(int index, String exerciseId) {
        if (index < 0 || index >= exerciseIds.size()) {
            return this;
        }
        List<String> updated = new ArrayList<String>(exerciseIds);
        updated.set(index, exerciseId);
        return new ScheduledSession(week, dayIndex, epochDay, focus, updated, slotKeys,
                status, repeatWeek);
    }

    private static List<String> immutable(List<String> source) {
        return Collections.unmodifiableList(
                source == null ? new ArrayList<String>() : new ArrayList<String>(source));
    }
}
