package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * 按 目标 × 训练水平 × 每周天数 生成 8 周分阶段周期计划。
 *
 * 结构依据：
 *  - 分化选择保证每个大肌群每周 ≥2 次（ACSM 第11版；Schoenfeld 2016 频率荟萃）；
 *  - 周期化：适应(2周) → 发展(3周) → 强化(2周) → 减载/重测(1周)（NSCA）；
 *  - 组×次@RPE、休息按 ACSM/NSCA 的目标别参数区间取值；
 *  - 减脂/体适能目标叠加每周有氧分钟目标（ACSM / PAGA 2018：150-300 分钟中等强度）。
 */
public final class ProgramBuilder {

    public static final int TOTAL_WEEKS = 8;

    public TrainingProgram build(PlanGoal goal, TrainingLevel level, int daysPerWeek,
            Intensity intensityCap) {
        int days = Math.max(2, Math.min(5, daysPerWeek));
        List<ProgramFocus> split = splitFor(goal, days);
        String splitName = splitNameFor(goal, days);

        List<ProgramPhase> phases = new ArrayList<ProgramPhase>();
        phases.add(new ProgramPhase("ADAPT", "适应期", 1, 2,
                adjustSets(new Prescription(2, adaptReps(goal), "5-6", 90), level, 0),
                cap(Intensity.MEDIUM, intensityCap),
                aerobicMinutes(goal, 0), aerobicNote(goal, 0),
                "以动作质量为先：负荷留有余地（RPE 5-6），熟悉每个动作的发力和幅度。"));
        phases.add(new ProgramPhase("DEVELOP", "发展期", 3, 5,
                adjustSets(developPrescription(goal, level), level, 1),
                cap(developIntensity(goal), intensityCap),
                aerobicMinutes(goal, 1), aerobicNote(goal, 1),
                developDescription(goal)));
        phases.add(new ProgramPhase("INTENSIFY", "强化期", 6, 7,
                adjustSets(intensifyPrescription(goal, level), level, 1),
                cap(Intensity.HIGH, intensityCap),
                aerobicMinutes(goal, 2), aerobicNote(goal, 2),
                intensifyDescription(goal, level)));
        phases.add(new ProgramPhase("DELOAD", "减载 + 重测周", 8, 8,
                new Prescription(2, "8-10", "5-6", 90),
                cap(Intensity.LOW, intensityCap),
                aerobicMinutes(goal, 0), "轻松有氧为主，保持活动即可。",
                "训练量减半消化疲劳；周末重做一次状态自测（俯卧撑/平板/深蹲），"
                        + "对比 8 周前的结果，再决定下一周期的起点。"));

        List<String> refs = new ArrayList<String>(Arrays.asList(
                GuidelineRefs.ACSM_RT,
                GuidelineRefs.NSCA_PERIODIZATION,
                GuidelineRefs.FREQUENCY_META,
                GuidelineRefs.DELOAD));
        if (goal == PlanGoal.FAT_LOSS || goal == PlanGoal.GENERAL_FITNESS) {
            refs.add(GuidelineRefs.ACSM_AEROBIC);
        }

        String progression = "进阶规则（NSCA）：当每组都能以标准动作完成次数上限时，"
                + "下次同动作加重约 2-10%（小肌群取低值）；两周都完不成下限则减重 5-10%。";

        return new TrainingProgram(goal, level, days, TOTAL_WEEKS,
                phases, split, splitName, progression, refs);
    }

    // ------------------------------------------------------------------ 分化

    private List<ProgramFocus> splitFor(PlanGoal goal, int days) {
        boolean conditioning = goal == PlanGoal.FAT_LOSS || goal == PlanGoal.GENERAL_FITNESS;
        switch (days) {
            case 2:
                return Arrays.asList(ProgramFocus.FULL_A, ProgramFocus.FULL_B);
            case 3:
                return Arrays.asList(ProgramFocus.FULL_A, ProgramFocus.FULL_B, ProgramFocus.FULL_C);
            case 4:
                if (conditioning) {
                    return Arrays.asList(ProgramFocus.UPPER, ProgramFocus.LOWER,
                            ProgramFocus.CARDIO_CORE, ProgramFocus.FULL_B);
                }
                return Arrays.asList(ProgramFocus.UPPER, ProgramFocus.LOWER,
                        ProgramFocus.UPPER, ProgramFocus.LOWER);
            default:
                if (conditioning) {
                    return Arrays.asList(ProgramFocus.UPPER, ProgramFocus.LOWER,
                            ProgramFocus.CARDIO_CORE, ProgramFocus.UPPER, ProgramFocus.LOWER);
                }
                return Arrays.asList(ProgramFocus.PUSH, ProgramFocus.PULL, ProgramFocus.LEGS,
                        ProgramFocus.UPPER, ProgramFocus.LOWER);
        }
    }

    private String splitNameFor(PlanGoal goal, int days) {
        boolean conditioning = goal == PlanGoal.FAT_LOSS || goal == PlanGoal.GENERAL_FITNESS;
        switch (days) {
            case 2:
                return "全身 ×2（每肌群每周 2 次）";
            case 3:
                return "全身 A/B/C（每肌群每周 3 次）";
            case 4:
                return conditioning ? "上/下 + 有氧核心 + 全身" : "上/下 ×2（每肌群每周 2 次）";
            default:
                return conditioning ? "上/下 ×2 + 有氧核心日" : "推/拉/腿 + 上/下（每肌群每周 2 次）";
        }
    }

    // ------------------------------------------------------------- 阶段处方

    private String adaptReps(PlanGoal goal) {
        return goal == PlanGoal.STRENGTH ? "8-10" : "10-12";
    }

    private Prescription developPrescription(PlanGoal goal, TrainingLevel level) {
        switch (goal) {
            case STRENGTH:
                return level == TrainingLevel.BEGINNER
                        ? new Prescription(3, "6-8", "7-8", 150)
                        : new Prescription(4, "5-8", "7-8", 150);
            case FAT_LOSS:
                return new Prescription(3, "10-15", "6-8", 60);
            case GENERAL_FITNESS:
                return new Prescription(3, "8-12", "6-7", 90);
            case MUSCLE_GAIN:
            default:
                return new Prescription(3, "8-12", "6-8", 90);
        }
    }

    private Intensity developIntensity(PlanGoal goal) {
        return goal == PlanGoal.STRENGTH ? Intensity.HIGH : Intensity.MEDIUM;
    }

    private String developDescription(PlanGoal goal) {
        switch (goal) {
            case STRENGTH:
                return "积累力量基础：多关节动作排最前，负荷逐周小幅上调，组间休息给足。";
            case FAT_LOSS:
                return "保肌 + 扩大消耗：力量课休息缩短、密度提高，并把每周有氧分钟数补足。";
            case GENERAL_FITNESS:
                return "力量与有氧并进：达到指南的每周基础活动量，动作覆盖推/拉/蹲/髋铰链。";
            case MUSCLE_GAIN:
            default:
                return "肌肥大主阶段：8-12 次区间逐步加重，每肌群每周至少 2 次刺激。";
        }
    }

    private Prescription intensifyPrescription(PlanGoal goal, TrainingLevel level) {
        switch (goal) {
            case STRENGTH:
                return level == TrainingLevel.BEGINNER
                        ? new Prescription(3, "5-8", "8", 180)
                        : new Prescription(4, "3-6", "8-9", 180);
            case FAT_LOSS:
                return new Prescription(3, "8-12", "7-8", 60);
            case GENERAL_FITNESS:
                return new Prescription(3, "8-10", "7-8", 90);
            case MUSCLE_GAIN:
            default:
                return level == TrainingLevel.BEGINNER
                        ? new Prescription(3, "8-12", "7-8", 120)
                        : new Prescription(4, "6-10", "7-9", 120);
        }
    }

    private String intensifyDescription(PlanGoal goal, TrainingLevel level) {
        String base;
        switch (goal) {
            case STRENGTH:
                base = "冲强度阶段：次数下调、负荷上调，接近但不到力竭（留 1-2 次余量）。";
                break;
            case FAT_LOSS:
                base = "维持力量强度防掉肌肉，有氧提到指南上限区间，可加入 1-2 次间歇。";
                break;
            case GENERAL_FITNESS:
                base = "小幅提高负荷与有氧时长，巩固前 5 周建立的习惯。";
                break;
            case MUSCLE_GAIN:
            default:
                base = "加深刺激：负荷上调、接近力竭（RPE 7-9），注意睡眠与蛋白质补足。";
                break;
        }
        if (level == TrainingLevel.BEGINNER) {
            base += " 初级阶段不追求极限重量，动作质量优先。";
        }
        return base;
    }

    /** 初级 -1 组（不低于 2），高级在发展/强化期 +1 组（不超过 5）。适应/减载不加。 */
    private Prescription adjustSets(Prescription base, TrainingLevel level, int phaseKind) {
        int sets = base.sets();
        if (level == TrainingLevel.BEGINNER) {
            sets = Math.max(2, sets - 1);
        } else if (level == TrainingLevel.ADVANCED && phaseKind == 1) {
            sets = Math.min(5, sets + 1);
        }
        if (sets == base.sets()) {
            return base;
        }
        return new Prescription(sets, base.reps(), base.rpe(), base.restSeconds());
    }

    private Intensity cap(Intensity wanted, Intensity capValue) {
        if (capValue == null) {
            return wanted;
        }
        return wanted.ordinal() <= capValue.ordinal() ? wanted : capValue;
    }

    // ---------------------------------------------------------------- 有氧

    /** phaseKind: 0 适应/减载, 1 发展, 2 强化。返回该阶段每周有氧分钟目标（0 = 不作要求）。 */
    private int aerobicMinutes(PlanGoal goal, int phaseKind) {
        if (goal == PlanGoal.FAT_LOSS) {
            return phaseKind == 0 ? 100 : phaseKind == 1 ? 150 : 250;
        }
        if (goal == PlanGoal.GENERAL_FITNESS) {
            return phaseKind == 0 ? 100 : 150;
        }
        return 0;
    }

    private String aerobicNote(PlanGoal goal, int phaseKind) {
        if (goal == PlanGoal.FAT_LOSS) {
            if (phaseKind == 2) {
                return "每周 250 分钟左右中等强度有氧（快走/骑行/椭圆机），其中 1-2 次可换成 15-20 分钟间歇。";
            }
            return "每周 " + aerobicMinutes(goal, phaseKind) + " 分钟中等强度有氧，可拆到力量课后 20-30 分钟或休息日完成。";
        }
        if (goal == PlanGoal.GENERAL_FITNESS) {
            return "每周 150 分钟中等强度有氧（说话略喘的程度），凑不成整段就按 10-15 分钟累计。";
        }
        return "力量为主，有氧不作硬性要求；休息日快走或骑行 20-30 分钟有助恢复。";
    }
}
