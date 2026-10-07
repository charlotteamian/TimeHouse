package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public final class AdHocPlannerTest {
    public static void main(String[] args) {
        AdHocPlannerTest test = new AdHocPlannerTest();
        test.intentReadsNegationTimeAndPurpose();
        test.chineseAndArabicMinutesBothParse();
        test.timeBudgetIsAHardConstraint();
        test.shortBudgetPrefersFewerExercisesWithRealSets();
        test.recentlyTrainedRegionsAreAvoided();
        test.tomorrowsPlannedRegionsAreFlagged();
        test.namedRegionIsNotSwappedForUnderworkedOnes();
        test.weeklyVolumeDrivesTargetsWhenNoRegionAsked();
        test.overshootingWeeklyCeilingIsWarned();
        test.recoveryModeDropsHighStressWork();
        test.excludedRegionNeverAppears();
        test.regenerationRotatesExercisesWithoutBreakingStructure();
        System.out.println("AdHocPlannerTest: all tests passed");
    }

    private static final long HOUR = 3600_000L;
    private static final long NOW = 1_800_000_000_000L;

    private final List<Exercise> pool = safePool();

    // ------------------------------------------------------------------ 意图解析

    private void intentReadsNegationTimeAndPurpose() {
        AdHocIntent plain = AdHocIntent.parse("想练背");
        assertTrue(plain.regions().contains("背"), "应识别出练背");
        assertEquals(AdHocIntent.Mode.STRENGTH, plain.mode(), "默认是力量模式");

        AdHocIntent negated = AdHocIntent.parse("练上肢，不要练肩");
        assertTrue(negated.regions().contains("背"), "上肢应包含背");
        assertTrue(!negated.regions().contains("肩"), "被否定的肩不能进目标");
        assertTrue(negated.excludedRegions().contains("肩"), "肩应进排除名单");

        AdHocIntent trailing = AdHocIntent.parse("腿不练");
        assertTrue(trailing.excludedRegions().contains("腿"), "「腿不练」要识别成排除腿");

        // "练腿不练背"：否定词后面跟着另一个部位，这个否定属于背，不属于腿。
        AdHocIntent both = AdHocIntent.parse("练腿不练背");
        assertTrue(both.regions().contains("腿"), "练腿应保留");
        assertTrue(both.excludedRegions().contains("背"), "不练背应排除背");

        assertEquals(AdHocIntent.Mode.CONDITIONING, AdHocIntent.parse("就想出出汗").mode(), "出汗走循环");
        assertEquals(AdHocIntent.Mode.RECOVERY, AdHocIntent.parse("今天很累，腰有点僵").mode(), "累/僵走恢复");
    }

    private void chineseAndArabicMinutesBothParse() {
        assertEquals(15, AdHocIntent.parse("只有15分钟").minutes(), "阿拉伯数字分钟");
        assertEquals(20, AdHocIntent.parse("二十分钟练个背").minutes(), "中文数字分钟");
        assertEquals(30, AdHocIntent.parse("有半小时").minutes(), "半小时");
        assertEquals(15, AdHocIntent.parse("一刻钟").minutes(), "一刻钟");
        assertEquals(60, AdHocIntent.parse("一小时随便练练").minutes(), "一小时");
        assertEquals(0, AdHocIntent.parse("练背").minutes(), "没说时间就返回 0");
    }

    // ------------------------------------------------------------ 时长是硬约束

    private void timeBudgetIsAHardConstraint() {
        SessionTimeModel model = new SessionTimeModel();
        for (int minutes : new int[]{8, 15, 25, 40}) {
            WorkoutPlan plan = AdHocPlanner.plan(pool, request().minutes(minutes));
            assertTrue(!plan.items().isEmpty(), minutes + " 分钟应该排得出动作");
            int seconds = model.sessionSeconds(plan.items());
            assertTrue(seconds <= minutes * 60,
                    minutes + " 分钟的预算被超了：实际算出 " + seconds + " 秒");
            assertEquals(model.sessionMinutes(plan.items()), plan.estimatedMinutes(),
                    "时长必须按实际处方算");
        }
    }

    private void shortBudgetPrefersFewerExercisesWithRealSets() {
        WorkoutPlan plan = AdHocPlanner.plan(pool, request().minutes(8));
        assertTrue(plan.items().size() <= 3, "8 分钟不该塞一堆动作，实际 " + plan.items().size());
        for (WorkoutItem item : plan.items()) {
            assertTrue(item.prescription().sets() >= 2,
                    "宁可少做几个动作也要把组数做够，实际 " + item.prescription().sets() + " 组");
        }
    }

    // -------------------------------------------------------- 不破坏计划与恢复

    private void recentlyTrainedRegionsAreAvoided() {
        List<TrainingLoad> recent = Arrays.asList(
                new TrainingLoad(Arrays.asList("胸"), 4, NOW - 6 * HOUR));
        WorkoutPlan plan = AdHocPlanner.plan(pool, request()
                .recovery(RecoveryState.of(recent, NOW)));
        for (WorkoutItem item : plan.items()) {
            assertTrue(!item.exercise().targetRegions().contains("胸"),
                    "6 小时前刚练过胸，不该再排胸的动作：" + item.exercise().name());
        }
    }

    private void tomorrowsPlannedRegionsAreFlagged() {
        Set<String> tomorrow = new LinkedHashSet<String>(Arrays.asList("背"));
        WorkoutPlan plan = AdHocPlanner.plan(pool, request()
                .intent(AdHocIntent.parse("练背"))
                .tomorrowRegions(tomorrow));
        boolean warned = false;
        for (String note : plan.avoidanceNotes()) {
            warned = warned || note.contains("明天的计划课");
        }
        assertTrue(warned, "明天要练背，今天还练背就该提示冲突");
        // 但冲突只是提示：点名要练背，就得给背，不能悄悄换成别的部位。
        for (WorkoutItem item : plan.items()) {
            assertTrue(item.exercise().targetRegions().contains("背"),
                    "点名练背时不该混进别的部位：" + item.exercise().name()
                            + "（" + item.exercise().targetRegions() + "）");
        }
    }

    /** 说了练哪里就练哪里——本周别处欠刺激不能成为偷换部位的理由。 */
    private void namedRegionIsNotSwappedForUnderworkedOnes() {
        List<TrainingLoad> done = Arrays.asList(
                new TrainingLoad(Arrays.asList("背"), 8, NOW - 40 * HOUR));
        WeeklyVolumeLedger ledger = WeeklyVolumeLedger.of(done, TrainingLevel.BEGINNER,
                NOW - 120 * HOUR);
        WorkoutPlan plan = AdHocPlanner.plan(pool, request()
                .intent(AdHocIntent.parse("练背"))
                .minutes(25)
                .ledger(ledger));
        for (WorkoutItem item : plan.items()) {
            assertTrue(item.exercise().targetRegions().contains("背"),
                    "点名练背却排了 " + item.exercise().name());
        }
    }

    private void weeklyVolumeDrivesTargetsWhenNoRegionAsked() {
        // 本周胸背腿都练满了，只有肩一组没练。
        List<TrainingLoad> done = new ArrayList<TrainingLoad>();
        for (String region : new String[]{"胸", "背", "腿", "臀", "手臂", "核心"}) {
            done.add(new TrainingLoad(Arrays.asList(region), 12, NOW - 80 * HOUR));
        }
        WeeklyVolumeLedger ledger = WeeklyVolumeLedger.of(done, TrainingLevel.BEGINNER,
                NOW - 120 * HOUR);
        assertEquals(WeeklyVolumeLedger.Status.LOW, ledger.forRegion("肩").status(), "肩应判为欠刺激");

        WorkoutPlan plan = AdHocPlanner.plan(pool, request().ledger(ledger));
        boolean touchesShoulder = false;
        for (WorkoutItem item : plan.items()) {
            touchesShoulder = touchesShoulder || item.exercise().targetRegions().contains("肩");
        }
        assertTrue(touchesShoulder, "没指定部位时应优先补本周欠刺激的肩");
    }

    private void overshootingWeeklyCeilingIsWarned() {
        List<TrainingLoad> done = Arrays.asList(
                new TrainingLoad(Arrays.asList("背"), 14, NOW - 40 * HOUR));
        WeeklyVolumeLedger ledger = WeeklyVolumeLedger.of(done, TrainingLevel.BEGINNER,
                NOW - 120 * HOUR);
        assertEquals(0.0, ledger.forRegion("背").roomToCeiling(), "初级 14 组正好到上限，没有余量了");
        assertEquals(WeeklyVolumeLedger.Status.OK, ledger.forRegion("背").status(),
                "刚好等于上限还算合适，超过才算偏多");

        WorkoutPlan plan = AdHocPlanner.plan(pool, request()
                .intent(AdHocIntent.parse("再练个背"))
                .minutes(25)
                .ledger(ledger));
        boolean warned = false;
        for (String note : plan.avoidanceNotes()) {
            warned = warned || note.contains("超过建议上限");
        }
        assertTrue(warned, "顶爆周容量必须提示，否则加练会毁掉计划");
    }

    private void recoveryModeDropsHighStressWork() {
        WorkoutPlan plan = AdHocPlanner.plan(pool, request()
                .intent(AdHocIntent.parse("今天很累，就活动开"))
                .minutes(15));
        assertTrue(!plan.items().isEmpty(), "恢复模式也要给得出动作");
        for (WorkoutItem item : plan.items()) {
            assertTrue(!item.exercise().jointStress("lower_back").isAtLeast(StressLevel.HIGH),
                    "恢复模式不该出现腰部高压力动作：" + item.exercise().name());
            assertTrue(item.prescription().sets() <= 2, "恢复模式组数不超过 2");
        }
    }

    private void excludedRegionNeverAppears() {
        WorkoutPlan plan = AdHocPlanner.plan(pool, request()
                .intent(AdHocIntent.parse("练上肢，不要练肩"))
                .minutes(30));
        for (WorkoutItem item : plan.items()) {
            assertTrue(!item.exercise().targetRegions().contains("肩"),
                    "被排除的肩不该出现：" + item.exercise().name());
        }
    }

    /** 连续重排应换同类动作，而不是把科学的动作模式结构一起随机掉。 */
    private void regenerationRotatesExercisesWithoutBreakingStructure() {
        WorkoutPlan first = AdHocPlanner.plan(pool, request().minutes(25));
        List<String> recent = new ArrayList<String>();
        List<String> firstRoles = new ArrayList<String>();
        for (WorkoutItem item : first.items()) {
            recent.add(item.exercise().id());
            firstRoles.add(TrainingSelection.role(item.exercise()));
        }

        WorkoutPlan second = AdHocPlanner.plan(pool, request().minutes(25)
                .recentExerciseIds(recent));
        List<String> secondIds = new ArrayList<String>();
        List<String> secondRoles = new ArrayList<String>();
        for (WorkoutItem item : second.items()) {
            secondIds.add(item.exercise().id());
            secondRoles.add(TrainingSelection.role(item.exercise()));
        }

        assertEquals(firstRoles, secondRoles, "重排后应保留相同动作模式顺序");
        int changed = 0;
        for (int i = 0; i < Math.min(recent.size(), secondIds.size()); i++) {
            if (!recent.get(i).equals(secondIds.get(i))) changed++;
        }
        assertTrue(changed >= Math.min(2, secondIds.size()),
                "候选充足时至少轮换两个同类动作，实际只换了 " + changed + " 个");
        assertTrue(second.avoidanceNotes().toString().contains("轮换规则"),
                "安排说明应公开轮换逻辑");
    }

    // ------------------------------------------------------------------ 辅助

    private AdHocPlanner.Request request() {
        return new AdHocPlanner.Request()
                .minutes(20)
                .intensity(Intensity.MEDIUM)
                .level(TrainingLevel.BEGINNER)
                .recovery(RecoveryState.of(new ArrayList<TrainingLoad>(), NOW));
    }

    private List<Exercise> safePool() {
        List<Exercise> result = new ArrayList<Exercise>();
        for (Exercise exercise : SeedExercises.defaultExercises()) {
            if (exercise.evidenceStatus() != EvidenceStatus.USER_UNVERIFIED) {
                result.add(exercise);
            }
        }
        return result;
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
