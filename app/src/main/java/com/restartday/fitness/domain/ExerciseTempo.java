package com.restartday.fitness.domain;

/**
 * 判断一个动作是「计次」还是「计时（等长保持）」，以及是不是单侧动作。
 *
 * <p>动作库（1324 条上游数据 + 内置种子）都没有这个字段，但时长核算和后续的语音播报
 * 都必须知道：平板支撑按"10-12 次"估时是没有意义的。这里用动作名和动作模式做确定性判断，
 * 不引入额外数据文件，改判定只改这一个类，并且可以被领域测试覆盖。
 */
public final class ExerciseTempo {

    /** 等长动作的保持秒数上下限：低于 20 秒起不到稳定训练效果，高于 60 秒对初学者意义不大。 */
    private static final int MIN_HOLD_SECONDS = 20;
    private static final int MAX_HOLD_SECONDS = 60;

    /** 名称里出现这些词就按等长保持处理。 */
    private static final String[] HOLD_NAME_KEYWORDS = {
            "平板", "支撑", "静蹲", "静态", "保持", "悬垂", "靠墙坐", "侧桥", "撑体", "顶峰收缩"
    };

    /** 名称里出现这些词就按单侧动作处理（一组要左右各做一遍）。 */
    private static final String[] PER_SIDE_NAME_KEYWORDS = {
            "单臂", "单腿", "单侧", "单手", "单脚"
    };

    private ExerciseTempo() {
    }

    /**
     * 把动作库里的原始处方修正成可估时的处方：等长动作换算成保持秒数，单侧动作补上标记。
     * 组数、RPE、休息一律保持不变——那些是周期计划的科学处方，不归这里管。
     */
    public static Prescription effective(Exercise exercise, Prescription base) {
        if (exercise == null || base == null) {
            return base;
        }
        if (exercise.name().contains("拍肩")) {
            return new Prescription(base.sets(), "10-15", base.rpe(), base.restSeconds()).withPerSide(true);
        }
        boolean perSide = base.perSide() || isPerSide(exercise);
        if (base.kind() == Prescription.Kind.HOLD) return base.withPerSide(perSide);
        if (isHold(exercise)) {
            return Prescription.hold(base.sets(), holdSecondsFor(base), base.rpe(),
                    base.restSeconds(), perSide);
        }
        return base.withPerSide(perSide);
    }

    /** 等长保持类动作（平板支撑、侧桥、靠墙静蹲……）。 */
    public static boolean isHold(Exercise exercise) {
        if (exercise == null) {
            return false;
        }
        String name = exercise.name();
        for (String keyword : HOLD_NAME_KEYWORDS) {
            if (name.contains(keyword)) {
                // 「臀桥」「桥式」是计次动作，不能因为含"桥"就误判；这里靠关键词本身足够精确，
                // 但"支撑"要排除"四点支撑爬行"这类明确带动作的名字。
                if ("支撑".equals(keyword) && (name.contains("爬") || name.contains("交替"))) {
                    continue;
                }
                return true;
            }
        }
        return false;
    }

    /** 单侧动作：一组要左右各做一遍，净工作时间翻倍。 */
    public static boolean isPerSide(Exercise exercise) {
        if (exercise == null) {
            return false;
        }
        String name = exercise.name();
        for (String keyword : PER_SIDE_NAME_KEYWORDS) {
            if (name.contains(keyword)) {
                return true;
            }
        }
        if (exercise.movementPatterns().contains("单腿")) {
            return true;
        }
        // 动作库自带的处方里写了 "8-10/侧" 的（死虫这类），阶段处方覆盖后也不能把这个信息丢掉。
        for (Intensity intensity : Intensity.values()) {
            Prescription own = exercise.prescription(intensity);
            if (own != null && own.perSide()) {
                return true;
            }
        }
        return false;
    }

    /**
     * 把计次处方换算成等长保持秒数：按同样的节奏折算，再收敛到 20-60 秒的合理区间并取 5 的整数。
     * 这样低强度阶段的平板约 25 秒、强化阶段约 45 秒，随周期处方自然变化。
     */
    static int holdSecondsFor(Prescription base) {
        int seconds = (int) Math.round(base.midReps() * base.secondsPerRep());
        seconds = Math.max(MIN_HOLD_SECONDS, Math.min(MAX_HOLD_SECONDS, seconds));
        return (seconds / 5) * 5;
    }
}
