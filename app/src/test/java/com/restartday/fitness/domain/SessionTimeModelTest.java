package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.List;

public final class SessionTimeModelTest {
    public static void main(String[] args) {
        SessionTimeModelTest test = new SessionTimeModelTest();
        test.repsRangeAndPerSideMarkerAreParsed();
        test.holdPrescriptionUsesSecondsNotReps();
        test.itemTimeCoversWorkRestAndTransition();
        test.adaptPhaseSessionIsAboutTenMinutesNotForty();
        test.budgetSolvesForExerciseCount();
        test.calibrationMovesTowardsMeasuredDuration();
        test.holdExercisesAreDetectedAndConverted();
        System.out.println("SessionTimeModelTest: all tests passed");
    }

    private final SessionTimeModel model = new SessionTimeModel();

    private void repsRangeAndPerSideMarkerAreParsed() {
        Prescription plain = new Prescription(3, "8-12", "6-8", 90);
        assertEquals(8, plain.repsLow(), "repsLow");
        assertEquals(12, plain.repsHigh(), "repsHigh");
        assertTrue(!plain.perSide(), "8-12 is not a per-side prescription");
        assertEquals(10.0, plain.midReps(), "midReps");

        Prescription perSide = new Prescription(2, "8-10/侧", "5-6", 60);
        assertTrue(perSide.perSide(), "8-10/侧 must be detected as per-side");
        assertEquals(8, perSide.repsLow(), "per-side repsLow");
        assertEquals(10, perSide.repsHigh(), "per-side repsHigh");
        // 单侧动作一组要左右各做一遍，净工作时间翻倍。
        assertEquals(9.0 * 3 * 2, perSide.workSecondsPerSet(), "per-side work seconds double");
    }

    private void holdPrescriptionUsesSecondsNotReps() {
        Prescription plank = Prescription.hold(3, 30, "6-7", 60, false);
        assertEquals(Prescription.Kind.HOLD, plank.kind(), "kind");
        assertEquals(30.0, plank.workSecondsPerSet(), "hold work seconds");
        assertContains(plank.compactLabel(), "30 秒");
    }

    private void itemTimeCoversWorkRestAndTransition() {
        Prescription prescription = new Prescription(3, "8-12", "6-8", 90);
        // 3 组 × 10 次 × 3 秒 = 90 秒工作，2 段休息 = 180 秒，加 25 秒切换。
        assertEquals(90 + 180 + SessionTimeModel.TRANSITION_SECONDS,
                model.itemSeconds(prescription), "item seconds");
    }

    /**
     * 复现被报的那次训练：适应期 2 组 / 休息 90 秒 / 4 个动作。
     * 旧代码显示"预计 40 分钟"，实测 11:10。新模型必须算出 11 分钟量级。
     */
    private void adaptPhaseSessionIsAboutTenMinutesNotForty() {
        Prescription adapt = new Prescription(2, "10-12", "5-6", 90);
        List<WorkoutItem> items = itemsWith(adapt, 4);
        int minutes = model.sessionMinutes(items);
        assertTrue(minutes >= 9 && minutes <= 14,
                "适应期 4 个动作 × 2 组应该算出 9-14 分钟，实际 " + minutes);
    }

    private void budgetSolvesForExerciseCount() {
        Prescription medium = RecommendationEngine.typicalPrescription(Intensity.MEDIUM);
        int perItem = model.itemSeconds(medium);
        int count = model.fitExerciseCount(25, medium, 1, 8);
        assertEquals(Math.min(8, 25 * 60 / perItem), count, "25 分钟预算解出的动作数");
        assertTrue(model.sessionSeconds(itemsWith(medium, count)) <= 25 * 60,
                "解出来的动作数不能超预算");
        assertEquals(8, model.fitExerciseCount(0, medium, 1, 8), "不限时走上限");
    }

    private void calibrationMovesTowardsMeasuredDuration() {
        // 预计 600 秒、实际练了 900 秒 → 系数应该往上走，但不会一步到位。
        double next = SessionTimeModel.calibrated(1.0, 600, 900);
        assertTrue(next > 1.0 && next < 1.5, "校准应向实测靠拢且平滑，实际 " + next);
        assertEquals(1.0, SessionTimeModel.calibrated(1.0, 0, 900), "预计为 0 时不校准");
        // 极端值要被夹住，一次异常训练不能把系数带跑。
        assertTrue(SessionTimeModel.calibrated(1.0, 60, 6000) <= 1.8, "校准上限");
    }

    private void holdExercisesAreDetectedAndConverted() {
        Exercise plank = find("平板支撑");
        assertTrue(ExerciseTempo.isHold(plank), "平板支撑应判定为等长保持");
        Prescription effective = ExerciseTempo.effective(plank, new Prescription(2, "10-12", "5-6", 75));
        assertEquals(Prescription.Kind.HOLD, effective.kind(), "平板支撑处方应换成保持秒数");
        assertEquals(2, effective.sets(), "组数不变——那是周期计划的处方");
        assertEquals(75, effective.restSeconds(), "休息不变");
        assertTrue(effective.holdSeconds() >= 20 && effective.holdSeconds() <= 60,
                "保持秒数应落在 20-60 秒，实际 " + effective.holdSeconds());

        Exercise row = find("单臂哑铃划船");
        assertTrue(ExerciseTempo.isPerSide(row), "单臂动作应判定为单侧");
        assertTrue(!ExerciseTempo.isHold(row), "单臂划船不是等长动作");

        // 死虫的名字看不出单侧，但它自带的处方写着 "8-10/侧"；阶段处方覆盖后不能把这个丢掉。
        Exercise deadBug = find("死虫");
        assertTrue(ExerciseTempo.isPerSide(deadBug), "死虫应从自带处方识别为单侧动作");
        Prescription phased = ExerciseTempo.effective(deadBug, new Prescription(2, "10-12", "5-6", 90));
        assertTrue(phased.perSide(), "阶段处方覆盖后仍应保留单侧标记");
        assertEquals(11.0 * 3 * 2, phased.workSecondsPerSet(), "单侧动作的工作时间要翻倍");

        Exercise squat = find("杯式深蹲");
        assertTrue(!ExerciseTempo.isHold(squat), "深蹲是计次动作");
        Exercise pushup = find("墙壁俯卧撑");
        assertTrue(!ExerciseTempo.isHold(pushup), "俯卧撑不能因为带「撑」字被误判成等长动作");
    }

    private List<WorkoutItem> itemsWith(Prescription prescription, int count) {
        List<Exercise> pool = SeedExercises.defaultExercises();
        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        for (int i = 0; i < count; i++) {
            items.add(new WorkoutItem(pool.get(i % pool.size()), prescription, false, "test"));
        }
        return items;
    }

    private Exercise find(String name) {
        for (Exercise exercise : SeedExercises.defaultExercises()) {
            if (exercise.name().equals(name)) {
                return exercise;
            }
        }
        throw new AssertionError("Seed pool has no exercise named " + name);
    }

    private static void assertContains(String actual, String part) {
        assertTrue(actual.contains(part), "Expected [" + actual + "] to contain [" + part + "]");
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
