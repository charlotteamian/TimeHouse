package com.restartday.fitness.domain;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class ProgramBuilderTest {
    public static void main(String[] args) {
        ProgramBuilderTest test = new ProgramBuilderTest();
        test.everyMuscleTrainedAtLeastTwiceAWeekOnResistanceSplits();
        test.eightWeeksCoveredByPhasesInOrder();
        test.deloadWeekReducesVolume();
        test.beginnerGetsFewerSetsAndNoHeavyTriples();
        test.advancedStrengthIntensifyUsesHeavyLowReps();
        test.fatLossCarriesAerobicTargetsAndConditioningDay();
        test.intensityCapFromAssessmentIsRespected();
        test.assessmentSafetyFlagCapsToLowAndAdvisesClearance();
        test.assessmentLevelsFollowHistoryAndTests();
        test.assessmentAnswersRemainAvailableForEditing();
        System.out.println("ProgramBuilderTest: all tests passed");
    }

    private final ProgramBuilder builder = new ProgramBuilder();

    private void everyMuscleTrainedAtLeastTwiceAWeekOnResistanceSplits() {
        String[] coreRegions = {"胸", "背", "腿"};
        for (PlanGoal goal : new PlanGoal[]{PlanGoal.MUSCLE_GAIN, PlanGoal.STRENGTH}) {
            for (int days = 2; days <= 5; days++) {
                TrainingProgram program = builder.build(goal, TrainingLevel.INTERMEDIATE, days, Intensity.HIGH);
                Map<String, Integer> weekly = regionCounts(program.weekSplit());
                for (String region : coreRegions) {
                    int count = weekly.containsKey(region) ? weekly.get(region) : 0;
                    assertTrue(count >= 2, goal + " " + days + "天分化中 " + region
                            + " 每周只有 " + count + " 次（应 ≥2，ACSM/频率荟萃）");
                }
            }
        }
    }

    private Map<String, Integer> regionCounts(List<ProgramFocus> split) {
        Map<String, Integer> counts = new HashMap<String, Integer>();
        for (ProgramFocus focus : split) {
            for (String region : focus.regions()) {
                Integer old = counts.get(region);
                counts.put(region, old == null ? 1 : old + 1);
            }
        }
        return counts;
    }

    private void eightWeeksCoveredByPhasesInOrder() {
        TrainingProgram program = builder.build(PlanGoal.MUSCLE_GAIN, TrainingLevel.INTERMEDIATE, 4, Intensity.HIGH);
        assertTrue(program.totalWeeks() == 8, "总周数应为 8");
        String previous = "";
        for (int week = 1; week <= 8; week++) {
            ProgramPhase phase = program.phaseForWeek(week);
            assertTrue(phase != null, "第 " + week + " 周没有阶段覆盖");
            previous = phase.key();
        }
        assertTrue("DELOAD".equals(previous), "最后一周应为减载周");
        assertTrue("ADAPT".equals(program.phaseForWeek(1).key()), "第 1 周应为适应期");
    }

    private void deloadWeekReducesVolume() {
        TrainingProgram program = builder.build(PlanGoal.MUSCLE_GAIN, TrainingLevel.ADVANCED, 4, Intensity.HIGH);
        ProgramPhase develop = program.phaseForWeek(4);
        ProgramPhase deload = program.phaseForWeek(8);
        assertTrue(deload.prescription().sets() < develop.prescription().sets(),
                "减载周组数应低于发展期");
        assertTrue(deload.intensity() == Intensity.LOW, "减载周引擎强度应为低");
    }

    private void beginnerGetsFewerSetsAndNoHeavyTriples() {
        TrainingProgram program = builder.build(PlanGoal.STRENGTH, TrainingLevel.BEGINNER, 3, Intensity.MEDIUM);
        ProgramPhase intensify = program.phaseForWeek(6);
        assertTrue(intensify.prescription().sets() <= 3, "初级强化期组数不应超过 3");
        assertTrue(!intensify.prescription().reps().startsWith("3"),
                "初级不应出现 3-6 次的大重量区间，实际 " + intensify.prescription().reps());
        TrainingProgram muscle = builder.build(PlanGoal.MUSCLE_GAIN, TrainingLevel.BEGINNER, 3, Intensity.MEDIUM);
        assertTrue(muscle.phaseForWeek(4).prescription().sets() == 2,
                "初级发展期应为基础组数 -1（3-1=2）");
    }

    private void advancedStrengthIntensifyUsesHeavyLowReps() {
        TrainingProgram program = builder.build(PlanGoal.STRENGTH, TrainingLevel.ADVANCED, 4, Intensity.HIGH);
        ProgramPhase intensify = program.phaseForWeek(7);
        assertTrue("3-6".equals(intensify.prescription().reps()),
                "高级力量强化期应为 3-6 次，实际 " + intensify.prescription().reps());
        assertTrue(intensify.prescription().restSeconds() >= 150, "大重量组间休息应 ≥150 秒");
        assertTrue(intensify.prescription().sets() == 5, "高级强化期应 +1 组到 5");
    }

    private void fatLossCarriesAerobicTargetsAndConditioningDay() {
        TrainingProgram program = builder.build(PlanGoal.FAT_LOSS, TrainingLevel.INTERMEDIATE, 4, Intensity.HIGH);
        assertTrue(program.weekSplit().contains(ProgramFocus.CARDIO_CORE),
                "减脂 4 天分化应包含有氧核心日");
        assertTrue(program.phaseForWeek(4).aerobicMinutesPerWeek() >= 150,
                "减脂发展期每周有氧应 ≥150 分钟（ACSM/PAGA）");
        assertTrue(program.phaseForWeek(6).aerobicMinutesPerWeek() > program.phaseForWeek(4).aerobicMinutesPerWeek(),
                "减脂强化期有氧应高于发展期");
        Map<String, Integer> counts = regionCounts(program.weekSplit());
        assertTrue(counts.get("胸") != null && counts.get("胸") >= 2, "减脂分化胸每周应 ≥2 次");
    }

    private void intensityCapFromAssessmentIsRespected() {
        TrainingProgram program = builder.build(PlanGoal.MUSCLE_GAIN, TrainingLevel.INTERMEDIATE, 3, Intensity.LOW);
        for (int week = 1; week <= 8; week++) {
            assertTrue(program.phaseForWeek(week).intensity() == Intensity.LOW,
                    "评估封顶为低强度时，第 " + week + " 周引擎强度应为低");
        }
    }

    private void assessmentSafetyFlagCapsToLowAndAdvisesClearance() {
        AssessmentInput input = new AssessmentInput.Builder()
                .safetyFlags(false, true, false, false, false, false, false)
                .history(36, 4)
                .pushupMax(30).plankSeconds(120).squatCount60s(50)
                .build();
        AssessmentResult result = new FitnessAssessment().evaluate(input);
        assertTrue(result.medicalClearanceAdvised(), "活动时胸痛应触发就医建议");
        assertTrue(result.intensityCap() == Intensity.LOW, "就医建议下强度应封顶为低");
    }

    private void assessmentLevelsFollowHistoryAndTests() {
        FitnessAssessment assessment = new FitnessAssessment();
        AssessmentResult beginner = assessment.evaluate(new AssessmentInput.Builder()
                .history(2, 1).build());
        assertTrue(beginner.level() == TrainingLevel.BEGINNER, "训练 2 个月应为初级");
        assertTrue(beginner.intensityCap() == Intensity.MEDIUM, "初级强度封顶应为中");

        AssessmentResult advanced = assessment.evaluate(new AssessmentInput.Builder()
                .history(36, 4).pushupMax(35).plankSeconds(150).squatCount60s(55).build());
        assertTrue(advanced.level() == TrainingLevel.ADVANCED, "训练 3 年每周 4 次且自测达标应为高级");

        AssessmentResult demoted = assessment.evaluate(new AssessmentInput.Builder()
                .history(36, 4).pushupMax(5).build());
        assertTrue(demoted.level() == TrainingLevel.INTERMEDIATE,
                "自测明显偏弱应从高级降到中级，实际 " + demoted.level());

        AssessmentResult untested = assessment.evaluate(new AssessmentInput.Builder()
                .history(12, 3).build());
        assertTrue(untested.level() == TrainingLevel.INTERMEDIATE, "未做自测不应降级");
    }

    private void assessmentAnswersRemainAvailableForEditing() {
        AssessmentInput input = new AssessmentInput.Builder()
                .safetyFlags(true, false, true, false, true, false, true)
                .history(18, 3)
                .pushupMax(16).plankSeconds(75).squatCount60s(38)
                .build();
        assertTrue(input.heartCondition() && !input.chestPainActivity()
                        && input.chestPainRest() && !input.dizziness()
                        && input.boneJointProblem() && !input.bloodPressureMeds()
                        && input.otherReason(),
                "安全筛查原始选项应可用于设置页准确回填");
        assertTrue(input.trainingMonths() == 18 && input.weeklySessions() == 3,
                "训练史应可用于评估修改");
        assertTrue(input.pushupMax() == 16 && input.plankSeconds() == 75
                        && input.squatCount60s() == 38,
                "可选自测值应可用于评估修改");
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
