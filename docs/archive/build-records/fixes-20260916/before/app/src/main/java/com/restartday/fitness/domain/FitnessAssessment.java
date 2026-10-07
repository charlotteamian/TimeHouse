package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.List;

/**
 * 当前状态评估：安全筛查决定是否降级与就医提示，
 * 训练史为主、体能自测为辅得出训练水平。
 *
 * 分级逻辑（简化自 ACSM 体适能评估思路，训练史权重最高）：
 *  - 初级：规律训练 < 6 个月，或每周 < 2 次；
 *  - 中级：6-24 个月且每周 ≥2 次；
 *  - 高级：≥24 个月且每周 ≥3 次；
 * 体能自测只用于「降半级」：自测明显偏弱时，中/高级各降一级起步，宁低勿高。
 */
public final class FitnessAssessment {

    public AssessmentResult evaluate(AssessmentInput input) {
        List<String> notes = new ArrayList<String>();
        List<String> refs = new ArrayList<String>();
        refs.add(GuidelineRefs.PARQ);
        refs.add(GuidelineRefs.LEVEL_NOTE);

        boolean clearance = input.anySafetyFlag();
        if (clearance) {
            notes.add("安全筛查存在「是」的回答：建议先咨询医生/物理治疗师，再开始或升级训练计划。");
        }
        if (input.boneJointProblem()) {
            notes.add("骨/关节问题：请同时在训练页设置对应伤痛部位，推荐会自动避开高压力动作。");
        }

        TrainingLevel byHistory = levelFromHistory(input.trainingMonths(), input.weeklySessions());
        TrainingLevel level = capByFitnessTests(byHistory, input, notes);

        Intensity cap;
        if (clearance) {
            cap = Intensity.LOW;
            notes.add("在获得专业意见前，计划强度封顶为低强度。");
        } else if (level == TrainingLevel.BEGINNER) {
            cap = Intensity.MEDIUM;
            notes.add("初级阶段先以低-中强度建立动作质量，再逐步进阶（低起点、慢进阶）。");
        } else {
            cap = Intensity.HIGH;
        }

        if (level != byHistory) {
            notes.add("体能自测结果偏弱，按更稳妥的一级起步；4 周后可重测上调。");
        }
        return new AssessmentResult(level, cap, clearance, notes, refs);
    }

    private TrainingLevel levelFromHistory(int months, int weekly) {
        if (months >= 24 && weekly >= 3) {
            return TrainingLevel.ADVANCED;
        }
        if (months >= 6 && weekly >= 2) {
            return TrainingLevel.INTERMEDIATE;
        }
        return TrainingLevel.BEGINNER;
    }

    /** 自测明显弱于该级别预期时降一级；未测不影响。阈值取宽松下限，避免误判。 */
    private TrainingLevel capByFitnessTests(TrainingLevel level, AssessmentInput input, List<String> notes) {
        if (level == TrainingLevel.BEGINNER) {
            return level;
        }
        boolean weak = false;
        if (input.pushupMax() >= 0 && input.pushupMax() < 10) {
            weak = true;
        }
        if (input.plankSeconds() >= 0 && input.plankSeconds() < 40) {
            weak = true;
        }
        if (input.squatCount60s() >= 0 && input.squatCount60s() < 25) {
            weak = true;
        }
        if (!weak) {
            return level;
        }
        return level == TrainingLevel.ADVANCED ? TrainingLevel.INTERMEDIATE : TrainingLevel.BEGINNER;
    }
}
