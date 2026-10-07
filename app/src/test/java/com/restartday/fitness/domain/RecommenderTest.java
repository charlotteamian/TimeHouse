package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;

public final class RecommenderTest {
    public static void main(String[] args) {
        RecommenderTest test = new RecommenderTest();
        test.backWorkoutAvoidsLowerBackLoadWhenWaistIsSensitive();
        test.favoriteExerciseRanksFirstOnlyWhenItPassesSafetyFilters();
        test.unknownWorkoutLowIntensityBuildsShortFullBodyPlan();
        test.userUnverifiedExercisesAreExcludedFromAutomaticRecommendations();
        test.defaultLibraryExercisesEnterAutomaticRecommendations();
        test.replacementKeepsSafetyAndAvoidsCurrentExercises();
        test.severePainDoesNotForceUnsafeHighIntensityPlan();
        test.customGroupIntentRecommendsItsExercisesEvenIfUnverified();
        test.targetDurationAdjustsPlanLength();
        test.shortEstimateIsReportedHonestlyWithAReason();
        test.fiveMinuteRecoveryCanBeOneMovement();
        test.unlimitedDurationIsEstimatedFromRecommendedExercises();
        test.recentlyUsedExercisesAreDeprioritised();
        System.out.println("RecommenderTest: all tests passed");
    }

    private final RecommendationEngine engine = new RecommendationEngine(SeedExercises.defaultExercises());

    public void backWorkoutAvoidsLowerBackLoadWhenWaistIsSensitive() {
        RecommendationInput input = new RecommendationInput.Builder()
                .intentText("我想练背，但腰有点不舒服，今天在家，强度中等")
                .intensity(Intensity.MEDIUM)
                .equipment("弹力带", "哑铃", "自重")
                .pain(PainPoint.lowerBack(PainSeverity.MILD))
                .build();

        WorkoutPlan plan = engine.recommend(input);

        assertContains(plan.title(), "背");
        assertAnyExercise(plan.items(), "弹力带划船");
        assertNoExercise(plan.items(), "杠铃俯身划船");
        assertTrue(plan.avoidanceNotes().stream().anyMatch(note -> note.contains("腰")),
                "Expected lower-back avoidance note");
        assertTrue(plan.items().stream().allMatch(item ->
                item.exercise().jointStress("lower_back") != StressLevel.HIGH),
                "Back workout should not include high lower-back stress exercises");
    }

    public void favoriteExerciseRanksFirstOnlyWhenItPassesSafetyFilters() {
        WorkoutPlan safePlan = engine.recommend(new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.MEDIUM)
                .equipment("高位下拉器", "哑铃", "自重")
                .favoriteExercises(new HashSet<>(Arrays.asList("exercise_lat_pulldown")))
                .build());

        assertEquals("高位下拉", safePlan.items().get(0).exercise().name(),
                "Favorite safe lat pulldown should rank first");

        WorkoutPlan shoulderPainPlan = engine.recommend(new RecommendationInput.Builder()
                .intentText("练上肢")
                .intensity(Intensity.MEDIUM)
                .equipment("哑铃", "自重", "固定器械")
                .favoriteExercises(new HashSet<>(Arrays.asList("exercise_seated_shoulder_press")))
                .pain(PainPoint.shoulder(PainSeverity.MODERATE))
                .build());

        assertNoExercise(shoulderPainPlan.items(), "坐姿肩推");
        assertTrue(shoulderPainPlan.avoidanceNotes().stream()
                        .anyMatch(note -> note.contains("已标心") && note.contains("肩")),
                "Favorite shoulder press should be explained as skipped due to shoulder pain");
    }

    public void unknownWorkoutLowIntensityBuildsShortFullBodyPlan() {
        WorkoutPlan plan = engine.recommend(new RecommendationInput.Builder()
                .unknownWorkout()
                .intensity(Intensity.LOW)
                .equipment("自重", "弹力带")
                .build());

        assertContains(plan.title(), "全身");
        assertTrue(plan.items().size() >= 3 && plan.items().size() <= 4,
                "Low intensity unknown workout should have 3-4 movements");
        assertTrue(plan.items().stream().allMatch(item -> item.prescription().sets() <= 2),
                "Low intensity prescriptions should stay at 1-2 sets");
        assertTrue(plan.recommendationReason().contains("推") || plan.recommendationReason().contains("拉"),
                "Full body reason should explain movement pattern coverage");
    }

    public void userUnverifiedExercisesAreExcludedFromAutomaticRecommendations() {
        WorkoutPlan plan = engine.recommend(new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.MEDIUM)
                .equipment("自重", "弹力带", "神秘器械")
                .includeUserUnverified(false)
                .favoriteExercises(new HashSet<>(Arrays.asList("custom_inverted_row_unverified")))
                .build());

        assertNoExercise(plan.items(), "自定义倒立划船");
        assertTrue(plan.avoidanceNotes().stream().anyMatch(note -> note.contains("未验证")),
                "Unverified favorite should be explained as excluded");
    }

    public void defaultLibraryExercisesEnterAutomaticRecommendations() {
        Exercise imported = new Exercise.Builder("dataset_1324_demo", "默认库划船")
                .evidence(EvidenceStatus.DEFAULT_LIBRARY)
                .regions("背")
                .patterns("拉")
                .equipment("自重")
                .instructions("保持躯干稳定，完成划船动作。")
                .build();
        RecommendationEngine importedEngine = new RecommendationEngine(Arrays.asList(imported));

        WorkoutPlan plan = importedEngine.recommend(new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.MEDIUM)
                .equipment("自重")
                .includeUserUnverified(false)
                .build());

        assertAnyExercise(plan.items(), "默认库划船");
    }

    public void replacementKeepsSafetyAndAvoidsCurrentExercises() {
        RecommendationInput input = new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.MEDIUM)
                .equipment("弹力带", "哑铃", "自重", "杠铃")
                .pain(PainPoint.lowerBack(PainSeverity.MILD))
                .build();
        WorkoutPlan plan = engine.recommend(input);

        WorkoutItem replacement = engine.replacementFor(plan.items().get(0), input,
                Arrays.asList(plan.items().get(0).exercise().id()));

        assertTrue(replacement != null, "Expected a replacement exercise");
        assertTrue(!replacement.exercise().id().equals(plan.items().get(0).exercise().id()),
                "Replacement should not repeat the current exercise");
        assertTrue(replacement.exercise().jointStress("lower_back") != StressLevel.HIGH,
                "Replacement should keep lower-back safety filtering");
    }

    public void severePainDoesNotForceUnsafeHighIntensityPlan() {
        WorkoutPlan plan = engine.recommend(new RecommendationInput.Builder()
                .intentText("腰急性疼痛，想练下肢高强度")
                .intensity(Intensity.HIGH)
                .equipment("杠铃", "哑铃", "自重")
                .pain(PainPoint.lowerBack(PainSeverity.SEVERE))
                .build());

        assertTrue(plan.isSafetyLimited(), "Severe pain should produce a safety-limited plan");
        assertTrue(plan.safetyMessage().contains("咨询医生") || plan.safetyMessage().contains("物理治疗师"),
                "Severe pain safety copy should direct user to a professional");
        assertTrue(plan.items().stream().noneMatch(item ->
                item.exercise().jointStress("lower_back").isAtLeast(StressLevel.MEDIUM)),
                "Severe lower-back pain should filter medium and high lower-back stress");
    }

    public void customGroupIntentRecommendsItsExercisesEvenIfUnverified() {
        List<Exercise> pool = new ArrayList<>(SeedExercises.defaultExercises());
        pool.add(new Exercise.Builder("custom_football_1", "足球绕桩")
                .evidence(EvidenceStatus.USER_UNVERIFIED)
                .regions("足球")
                .patterns("稳定")
                .equipment("自重")
                .instructions("绕过标志桶快速变向。")
                .build());
        RecommendationEngine footballEngine = new RecommendationEngine(pool);

        WorkoutPlan plan = footballEngine.recommend(new RecommendationInput.Builder()
                .intentText("我想训练足球动作")
                .intensity(Intensity.MEDIUM)
                .equipment("自重")
                .build());

        assertAnyExercise(plan.items(), "足球绕桩");
        assertContains(plan.title(), "足球");

        // Without naming the custom group, the unverified exercise stays out of auto recommendations.
        WorkoutPlan generic = footballEngine.recommend(new RecommendationInput.Builder()
                .unknownWorkout()
                .intensity(Intensity.MEDIUM)
                .equipment("自重")
                .build());
        assertNoExercise(generic.items(), "足球绕桩");
    }

    public void targetDurationAdjustsPlanLength() {
        WorkoutPlan shortPlan = engine.recommend(new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.HIGH)
                .targetMinutes(15)
                .equipment("高位下拉器", "固定器械", "弹力带", "哑铃", "杠铃")
                .build());

        WorkoutPlan longPlan = engine.recommend(new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.HIGH)
                .targetMinutes(55)
                .equipment("高位下拉器", "固定器械", "弹力带", "哑铃", "杠铃")
                .build());

        assertTrue(shortPlan.items().size() < longPlan.items().size(),
                "Long duration should include more exercises when safe candidates exist");
        assertTrue(shortPlan.estimatedMinutes() < longPlan.estimatedMinutes(),
                "Long duration should estimate a longer session");
        // 估算必须是按实际处方算出来的，不能是把用户输入的分钟数原样回显。
        assertEstimateMatchesPrescriptions(shortPlan);
        assertEstimateMatchesPrescriptions(longPlan);
    }

    /** 排不满预算时要如实给出更短的时长，并说明原因，而不是假装填满了。 */
    public void shortEstimateIsReportedHonestlyWithAReason() {
        WorkoutPlan plan = engine.recommend(new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.LOW)
                .targetMinutes(55)
                .equipment("高位下拉器", "固定器械", "弹力带", "哑铃")
                .build());

        assertEstimateMatchesPrescriptions(plan);
        assertTrue(plan.estimatedMinutes() < 55,
                "Low intensity caps exercise count, so the honest estimate must be shorter than 55");
        boolean explained = false;
        for (String note : plan.avoidanceNotes()) {
            explained = explained || note.contains("比你选的");
        }
        assertTrue(explained, "A shorter-than-requested session must say why");
    }

    public void fiveMinuteRecoveryCanBeOneMovement() {
        WorkoutPlan plan = engine.recommend(new RecommendationInput.Builder()
                .intentText("今天很累，只想做一个超短放松动作")
                .intensity(Intensity.LOW)
                .targetMinutes(5)
                .equipment("自重", "弹力带")
                .build());

        assertEquals(1, plan.items().size(), "Five-minute recovery should allow one movement");
        assertEstimateMatchesPrescriptions(plan);
    }

    /** 最近练过的动作应该被降权，避免每次生成都是同一套。 */
    public void recentlyUsedExercisesAreDeprioritised() {
        RecommendationInput.Builder base = new RecommendationInput.Builder()
                .intentText("我想练背")
                .intensity(Intensity.MEDIUM)
                .targetMinutes(25)
                .equipment("高位下拉器", "固定器械", "弹力带", "哑铃");

        WorkoutPlan first = engine.recommend(base.build());
        String firstPick = first.items().get(0).exercise().id();

        WorkoutPlan second = engine.recommend(base
                .recentExerciseIds(Arrays.asList(firstPick))
                .build());

        assertTrue(!second.items().get(0).exercise().id().equals(firstPick),
                "A freshly used exercise should not lead the next plan again");
    }

    private static void assertEstimateMatchesPrescriptions(WorkoutPlan plan) {
        int expected = new SessionTimeModel().sessionMinutes(plan.items());
        assertEquals(expected, plan.estimatedMinutes(),
                "Estimated minutes must be computed from the actual prescriptions");
    }

    public void unlimitedDurationIsEstimatedFromRecommendedExercises() {
        WorkoutPlan plan = engine.recommend(new RecommendationInput.Builder()
                .unknownWorkout()
                .intensity(Intensity.LOW)
                .targetMinutes(0)
                .equipment("自重", "弹力带")
                .build());

        assertTrue(plan.items().size() >= 1, "Unlimited plan should still recommend safe exercises");
        assertTrue(plan.estimatedMinutes() >= 5,
                "Unlimited plan should estimate time from the selected exercises instead of returning zero");
    }

    private static void assertAnyExercise(List<WorkoutItem> items, String name) {
        assertTrue(items.stream().anyMatch(item -> item.exercise().name().equals(name)),
                "Expected exercise: " + name);
    }

    private static void assertNoExercise(List<WorkoutItem> items, String name) {
        assertTrue(items.stream().noneMatch(item -> item.exercise().name().equals(name)),
                "Did not expect exercise: " + name);
    }

    private static void assertContains(String actual, String expectedPart) {
        assertTrue(actual.contains(expectedPart),
                "Expected [" + actual + "] to contain [" + expectedPart + "]");
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
