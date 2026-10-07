package com.restartday.fitness.domain;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public final class ProgramScheduleTest {
    public static void main(String[] args) {
        ProgramScheduleTest test = new ProgramScheduleTest();
        test.dayCoversTheSplitsMovementPatterns();
        test.fullBodyDaysAreNotTheSameWorkout();
        test.everyMuscleGroupIsTrainedAtLeastTwiceAWeek();
        test.scheduleLandsOnRealDatesAndNeverBeforeTheStart();
        test.missedSessionsAreMarkedNotPostponed();
        test.lowCompletionWeekIsFlaggedForRepeat();
        test.repeatingAWeekPushesLaterSessionsBackOneWeek();
        test.twoBadWeeksSuggestReplanning();
        System.out.println("ProgramScheduleTest: all tests passed");
    }

    private final List<Exercise> pool = SeedExercises.defaultExercises();
    private final Prescription adapt = new Prescription(2, "10-12", "5-6", 90);

    /**
     * 这是截图里那次训练暴露的问题：全身 A 排出 俯卧撑+臀桥+死虫+鸟狗，
     * 没有蹲、没有拉。槽位编排必须覆盖分化声明的动作模式。
     */
    private void dayCoversTheSplitsMovementPatterns() {
        ProgramComposer.ComposedDay day = ProgramComposer.composeDay(
                ProgramFocus.FULL_A, adapt, safePool(), 4,
                new ArrayList<String>(), new HashSet<String>());

        assertEquals(4, day.items().size(), "全身 A 应排满 4 个动作");
        Set<String> patterns = new HashSet<String>();
        for (WorkoutItem item : day.items()) {
            patterns.addAll(item.exercise().movementPatterns());
        }
        for (String required : ProgramFocus.FULL_A.patterns()) {
            assertTrue(patterns.contains(required),
                    "全身 A 必须覆盖「" + required + "」，实际动作模式：" + patterns);
        }
    }

    /** 全身 A/B/C 必须真的不一样——以前评分与日期无关，三天会取到几乎相同的动作。 */
    private void fullBodyDaysAreNotTheSameWorkout() {
        List<String> recent = new ArrayList<String>();
        List<List<String>> days = new ArrayList<List<String>>();
        ProgramFocus[] split = {ProgramFocus.FULL_A, ProgramFocus.FULL_B, ProgramFocus.FULL_C};
        for (ProgramFocus focus : split) {
            ProgramComposer.ComposedDay day = ProgramComposer.composeDay(
                    focus, adapt, safePool(), 4, recent, new HashSet<String>());
            days.add(day.exerciseIds());
            for (String id : day.exerciseIds()) {
                recent.remove(id);
                recent.add(0, id);
            }
        }
        for (int i = 0; i < days.size(); i++) {
            for (int j = i + 1; j < days.size(); j++) {
                Set<String> overlap = new HashSet<String>(days.get(i));
                overlap.retainAll(days.get(j));
                assertTrue(overlap.size() <= 1,
                        "第 " + (i + 1) + " 天和第 " + (j + 1) + " 天重复了 " + overlap.size()
                                + " 个动作：" + overlap);
            }
        }
    }

    /** ACSM / Schoenfeld 频率荟萃：每个大肌群每周至少练 2 次。 */
    private void everyMuscleGroupIsTrainedAtLeastTwiceAWeek() {
        TrainingProgram program = new ProgramBuilder()
                .build(PlanGoal.MUSCLE_GAIN, TrainingLevel.BEGINNER, 3, Intensity.MEDIUM);
        ProgramSchedule schedule = buildSchedule(program, LocalDate.of(2026, 7, 27).toEpochDay());

        Map<String, Integer> counts = new HashMap<String, Integer>();
        for (ScheduledSession session : schedule.sessions()) {
            if (session.week() != 1) {
                continue;
            }
            Set<String> regionsThisDay = new HashSet<String>();
            for (String id : session.exerciseIds()) {
                regionsThisDay.addAll(byId(id).targetRegions());
            }
            for (String region : regionsThisDay) {
                Integer prior = counts.get(region);
                counts.put(region, prior == null ? 1 : prior + 1);
            }
        }
        for (String region : new String[]{"胸", "背", "腿"}) {
            Integer count = counts.get(region);
            assertTrue(count != null && count >= 2,
                    region + " 每周只练了 " + count + " 次（应 ≥2）");
        }
    }

    private void scheduleLandsOnRealDatesAndNeverBeforeTheStart() {
        long start = LocalDate.of(2026, 7, 30).toEpochDay();  // 周四
        TrainingProgram program = new ProgramBuilder()
                .build(PlanGoal.GENERAL_FITNESS, TrainingLevel.BEGINNER, 3, Intensity.MEDIUM);
        ProgramSchedule schedule = buildSchedule(program, start);

        assertEquals(program.totalSessions(), schedule.totalCount(), "总次数");
        long previous = -1;
        for (ScheduledSession session : schedule.sessions()) {
            assertTrue(session.epochDay() >= start,
                    "不该把训练排在生成日之前：" + LocalDate.ofEpochDay(session.epochDay()));
            assertTrue(session.epochDay() >= previous, "日历必须按日期排序");
            previous = session.epochDay();
            assertTrue(!session.exerciseIds().isEmpty(), "每一天都要预生成动作，日历才有内容");
        }
    }

    private void missedSessionsAreMarkedNotPostponed() {
        long start = LocalDate.of(2026, 7, 27).toEpochDay();
        ProgramSchedule schedule = buildSchedule(program3Days(), start);
        long dayAfterFirst = schedule.sessions().get(0).epochDay() + 1;

        ProgramSchedule after = schedule.markMissedBefore(dayAfterFirst);
        assertEquals(ScheduledSession.Status.MISSED, after.sessions().get(0).status(), "漏练标记");
        // 保持周结构：后面的日期一天都不许动。
        for (int i = 0; i < schedule.sessions().size(); i++) {
            assertEquals(schedule.sessions().get(i).epochDay(), after.sessions().get(i).epochDay(),
                    "漏练不顺延，第 " + i + " 次的日期不该变");
        }
    }

    private void lowCompletionWeekIsFlaggedForRepeat() {
        long start = LocalDate.of(2026, 7, 27).toEpochDay();
        ProgramSchedule schedule = buildSchedule(program3Days(), start);
        long afterWeekOne = lastDayOfWeek(schedule, 1) + 1;

        // 第 1 周 3 次只完成 1 次 = 33% < 60%
        schedule = markDone(schedule, 1, 0);
        schedule = schedule.markMissedBefore(afterWeekOne);
        assertEquals(1, schedule.weekNeedingRepeat(afterWeekOne), "完成率不足的周应被标出来重做");

        // 完成 2/3 = 67% ≥ 60%，不该提示重做
        ProgramSchedule better = markDone(markDone(buildSchedule(program3Days(), start), 1, 0), 1, 1)
                .markMissedBefore(afterWeekOne);
        assertEquals(0, better.weekNeedingRepeat(afterWeekOne), "完成率达标的周不该提示重做");
    }

    private void repeatingAWeekPushesLaterSessionsBackOneWeek() {
        long start = LocalDate.of(2026, 7, 27).toEpochDay();
        ProgramSchedule schedule = buildSchedule(program3Days(), start);
        int before = schedule.totalCount();
        long weekTwoFirstDay = firstDayOfWeek(schedule, 2);

        ProgramSchedule repeated = schedule.repeatWeek(1);
        assertEquals(before + 3, repeated.totalCount(), "重做一周应该多出 3 次训练");
        assertEquals(weekTwoFirstDay + 7, firstDayOfWeek(repeated, 2), "后面的安排整体后移一周");

        int repeats = 0;
        for (ScheduledSession session : repeated.sessions()) {
            if (session.isRepeatWeek()) {
                repeats++;
                assertEquals(1, session.week(), "重做的是第 1 周，阶段处方跟着第 1 周");
                assertEquals(ScheduledSession.Status.PLANNED, session.status(), "重做的那周是待完成");
            }
        }
        assertEquals(3, repeats, "重做的次数");
    }

    private void twoBadWeeksSuggestReplanning() {
        long start = LocalDate.of(2026, 7, 27).toEpochDay();
        ProgramSchedule schedule = buildSchedule(program3Days(), start);
        long afterWeekTwo = lastDayOfWeek(schedule, 2) + 1;
        assertTrue(schedule.markMissedBefore(afterWeekTwo).shouldSuggestReplan(afterWeekTwo),
                "连续两周几乎没练，应该提示下调每周天数重新生成");

        ProgramSchedule good = buildSchedule(program3Days(), start);
        for (int week = 1; week <= 2; week++) {
            for (int day = 0; day < 3; day++) {
                good = markDone(good, week, day);
            }
        }
        assertTrue(!good.markMissedBefore(afterWeekTwo).shouldSuggestReplan(afterWeekTwo),
                "完成得好不该提示重新规划");
    }

    // ------------------------------------------------------------------ 辅助

    private TrainingProgram program3Days() {
        return new ProgramBuilder()
                .build(PlanGoal.MUSCLE_GAIN, TrainingLevel.BEGINNER, 3, Intensity.MEDIUM);
    }

    private ProgramSchedule buildSchedule(final TrainingProgram program, long start) {
        return ProgramSchedule.build(program, start,
                ProgramSchedule.defaultWeekdays(program.daysPerWeek()),
                new ProgramSchedule.DayComposer() {
                    @Override
                    public ProgramComposer.ComposedDay compose(int week, int dayIndex,
                            ProgramFocus focus, ProgramPhase phase, List<String> recentIds) {
                        return ProgramComposer.composeDay(focus, phase.prescription(), safePool(),
                                4, recentIds, new HashSet<String>());
                    }
                });
    }

    private ProgramSchedule markDone(ProgramSchedule schedule, int week, int dayIndex) {
        for (ScheduledSession session : schedule.sessions()) {
            if (session.week() == week && session.dayIndex() == dayIndex && !session.isRepeatWeek()) {
                return schedule.withSession(session.withStatus(ScheduledSession.Status.DONE));
            }
        }
        return schedule;
    }

    private long firstDayOfWeek(ProgramSchedule schedule, int week) {
        long first = Long.MAX_VALUE;
        for (ScheduledSession session : schedule.sessions()) {
            if (session.week() == week && !session.isRepeatWeek()) {
                first = Math.min(first, session.epochDay());
            }
        }
        return first;
    }

    private long lastDayOfWeek(ProgramSchedule schedule, int week) {
        long last = -1;
        for (ScheduledSession session : schedule.sessions()) {
            if (session.week() == week) {
                last = Math.max(last, session.epochDay());
            }
        }
        return last;
    }

    private List<Exercise> safePool() {
        List<Exercise> result = new ArrayList<Exercise>();
        for (Exercise exercise : pool) {
            if (exercise.evidenceStatus() != EvidenceStatus.USER_UNVERIFIED) {
                result.add(exercise);
            }
        }
        return result;
    }

    private Exercise byId(String id) {
        for (Exercise exercise : pool) {
            if (exercise.id().equals(id)) {
                return exercise;
            }
        }
        throw new AssertionError("Unknown exercise id " + id);
    }

    private static void assertEquals(Object expected, Object actual, String message) {
        if (!expected.equals(actual)) {
            throw new AssertionError(message + "\nExpected: " + expected + "\nActual: " + actual);
        }
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
