package com.restartday.fitness.domain;

/**
 * 当前状态评估的输入：安全筛查（PAR-Q+ 简化）+ 训练史 + 体能自测。
 * 体能自测均为可在家完成的动作，允许留空（-1 表示未测）。
 */
public final class AssessmentInput {
    // 安全筛查（任一为 true → 建议就医后再开始，计划强度封顶为低）
    private final boolean heartCondition;      // 医生是否说过你有心脏病，且只应做医生推荐的活动
    private final boolean chestPainActivity;   // 活动时是否胸痛
    private final boolean chestPainRest;       // 近一个月未活动时是否胸痛
    private final boolean dizziness;           // 是否因头晕失去平衡或失去意识
    private final boolean boneJointProblem;    // 是否有会因活动加重的骨/关节问题
    private final boolean bloodPressureMeds;   // 是否在服用血压/心脏药物
    private final boolean otherReason;         // 是否有其他不宜活动的原因

    // 训练史
    private final int trainingMonths;          // 规律力量训练的累计月数
    private final int weeklySessions;          // 近 3 个月每周训练次数

    // 体能自测（-1 = 未测）
    private final int pushupMax;               // 一次性标准俯卧撑最多个数（女性可跪姿并注明）
    private final int plankSeconds;            // 平板支撑最长坚持秒数
    private final int squatCount60s;           // 60 秒徒手深蹲个数

    private AssessmentInput(Builder builder) {
        heartCondition = builder.heartCondition;
        chestPainActivity = builder.chestPainActivity;
        chestPainRest = builder.chestPainRest;
        dizziness = builder.dizziness;
        boneJointProblem = builder.boneJointProblem;
        bloodPressureMeds = builder.bloodPressureMeds;
        otherReason = builder.otherReason;
        trainingMonths = builder.trainingMonths;
        weeklySessions = builder.weeklySessions;
        pushupMax = builder.pushupMax;
        plankSeconds = builder.plankSeconds;
        squatCount60s = builder.squatCount60s;
    }

    public boolean anySafetyFlag() {
        return heartCondition || chestPainActivity || chestPainRest || dizziness
                || boneJointProblem || bloodPressureMeds || otherReason;
    }

    public boolean heartCondition() {
        return heartCondition;
    }

    public boolean chestPainActivity() {
        return chestPainActivity;
    }

    public boolean chestPainRest() {
        return chestPainRest;
    }

    public boolean dizziness() {
        return dizziness;
    }

    public boolean boneJointProblem() {
        return boneJointProblem;
    }

    public boolean bloodPressureMeds() {
        return bloodPressureMeds;
    }

    public boolean otherReason() {
        return otherReason;
    }

    public int trainingMonths() {
        return trainingMonths;
    }

    public int weeklySessions() {
        return weeklySessions;
    }

    public int pushupMax() {
        return pushupMax;
    }

    public int plankSeconds() {
        return plankSeconds;
    }

    public int squatCount60s() {
        return squatCount60s;
    }

    public static final class Builder {
        private boolean heartCondition;
        private boolean chestPainActivity;
        private boolean chestPainRest;
        private boolean dizziness;
        private boolean boneJointProblem;
        private boolean bloodPressureMeds;
        private boolean otherReason;
        private int trainingMonths;
        private int weeklySessions;
        private int pushupMax = -1;
        private int plankSeconds = -1;
        private int squatCount60s = -1;

        public Builder safetyFlags(boolean heart, boolean chestPainActive, boolean chestPainAtRest,
                boolean dizzy, boolean boneJoint, boolean bpMeds, boolean other) {
            heartCondition = heart;
            chestPainActivity = chestPainActive;
            chestPainRest = chestPainAtRest;
            dizziness = dizzy;
            boneJointProblem = boneJoint;
            bloodPressureMeds = bpMeds;
            otherReason = other;
            return this;
        }

        public Builder history(int months, int sessionsPerWeek) {
            trainingMonths = Math.max(0, months);
            weeklySessions = Math.max(0, sessionsPerWeek);
            return this;
        }

        public Builder pushupMax(int value) {
            pushupMax = value;
            return this;
        }

        public Builder plankSeconds(int value) {
            plankSeconds = value;
            return this;
        }

        public Builder squatCount60s(int value) {
            squatCount60s = value;
            return this;
        }

        public AssessmentInput build() {
            return new AssessmentInput(this);
        }
    }
}
