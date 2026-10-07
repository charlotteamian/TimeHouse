package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.List;

/**
 * 每日能量与营养素目标计算。
 *
 * 公式与参数：
 *  - BMR：Mifflin-St Jeor（男 = 10W + 6.25H − 5A + 5；女 = 10W + 6.25H − 5A − 161）；
 *  - TDEE = BMR × 活动系数（1.2-1.9）；
 *  - 目标热量：减脂 −400 kcal/天（约每周 0.4kg），不低于安全下限；增肌 +300；其余维持；
 *  - 蛋白质：一般 1.2 g/kg（高于 DRIs RNI 0.98 以配合训练），增肌/力量 1.8，减脂 2.0
 *    （Morton 2018 / ISSN：1.6-2.2 g/kg 区间内取值）；
 *  - 脂肪 27% 供能（DRIs 20-30% 中值），碳水补足剩余能量；
 *  - 膳食纤维 25-30g、水 1500-1700ml、盐 <5g（膳食指南 2022 / DRIs）。
 */
public final class NutritionPlanner {

    public EnergyPlan plan(NutritionProfile profile) {
        List<String> notes = new ArrayList<String>();
        List<String> refs = new ArrayList<String>();
        refs.add(GuidelineRefs.BMR_FORMULA);
        refs.add(GuidelineRefs.CDG_2022);
        refs.add(GuidelineRefs.CDG_FIBER);
        refs.add(GuidelineRefs.FAT_RANGE);

        double bmr = 10.0 * profile.weightKg() + 6.25 * profile.heightCm() - 5.0 * profile.age()
                + (profile.male() ? 5 : -161);
        double tdee = bmr * profile.activity().factor();

        double target = tdee;
        switch (profile.goal()) {
            case FAT_LOSS: {
                target = tdee - 400;
                refs.add(GuidelineRefs.ENERGY_RATE);
                int floor = safeFloor(profile);
                if (target < floor) {
                    target = floor;
                    notes.add("已按安全下限抬高目标热量：缺口过大不可持续，也容易掉肌肉。");
                }
                notes.add("目标约为每天 -400 kcal，对应每周约 0.3-0.5kg 的减重速率；建议每 2 周复核体重趋势。");
                break;
            }
            case MUSCLE_GAIN:
                target = tdee + 300;
                refs.add(GuidelineRefs.ENERGY_RATE);
                notes.add("增肌盈余约 +300 kcal/天，配合抗阻训练；体重每月上涨超过 1.5kg 时可下调盈余。");
                break;
            case STRENGTH:
            case GENERAL_FITNESS:
            default:
                notes.add("以维持热量为目标；如体重连续两周单向变化超过 0.5kg/周，可 ±200 kcal 微调。");
                break;
        }

        double proteinPerKg = proteinPerKg(profile.goal());
        refs.add(profile.goal() == PlanGoal.GENERAL_FITNESS
                ? GuidelineRefs.CDG_PROTEIN_RNI : GuidelineRefs.SPORT_PROTEIN);
        double proteinG = proteinPerKg * proteinWeightBasis(profile, notes);
        double proteinKcal = proteinG * 4;

        double fatG = target * 0.27 / 9.0;
        double carbG = (target - proteinKcal - fatG * 9) / 4.0;
        if (carbG < 100) {
            carbG = 100;
            notes.add("碳水已按 100g/天 下限保底（保证训练表现与膳食纤维来源），如仍不够请上调目标热量。");
        }

        return new EnergyPlan(
                (int) Math.round(bmr), (int) Math.round(tdee), (int) Math.round(target),
                (int) Math.round(proteinG), proteinPerKg,
                (int) Math.round(fatG), (int) Math.round(carbG),
                25, 30, 1500, 1700, notes, refs);
    }

    private double proteinPerKg(PlanGoal goal) {
        switch (goal) {
            case FAT_LOSS:
                return 2.0;
            case MUSCLE_GAIN:
            case STRENGTH:
                return 1.8;
            case GENERAL_FITNESS:
            default:
                return 1.2;
        }
    }

    /** BMI ≥ 28 时按「身高对应 BMI 24 的体重」计蛋白，避免按超重体重放大。 */
    private double proteinWeightBasis(NutritionProfile profile, List<String> notes) {
        if (profile.bmi() >= 28) {
            double meters = profile.heightCm() / 100.0;
            double adjusted = 24.0 * meters * meters;
            notes.add("蛋白质按调整体重（BMI 24 对应体重）估算，避免按当前体重放大摄入。");
            return adjusted;
        }
        return profile.weightKg();
    }

    /** 能量安全下限：不低于 BMR，且女 ≥1200 / 男 ≥1500 kcal（极低能量饮食需医学监督）。 */
    private int safeFloor(NutritionProfile profile) {
        double bmr = 10.0 * profile.weightKg() + 6.25 * profile.heightCm() - 5.0 * profile.age()
                + (profile.male() ? 5 : -161);
        return (int) Math.round(Math.max(bmr, profile.male() ? 1500 : 1200));
    }
}
