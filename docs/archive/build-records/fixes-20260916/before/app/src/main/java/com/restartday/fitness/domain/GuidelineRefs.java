package com.restartday.fitness.domain;

/**
 * 全部推荐参数的出处集中在这里，UI 与生成逻辑只引用常量，
 * 保证「每条推荐都能指回一条指南」。
 */
public final class GuidelineRefs {

    // —— 训练 ——
    public static final String ACSM_RT =
            "ACSM《运动测试与处方指南》(第11版)：每个大肌群每周训练 2-3 天；"
                    + "初学者每动作 1-3 组、8-12 次（约 60-70% 1RM），组间休息 2-3 分钟（大负荷）或 1-2 分钟";
    public static final String ACSM_AEROBIC =
            "ACSM 与美国《身体活动指南》(PAGA 2018)：每周 150-300 分钟中等强度有氧，"
                    + "或 75-150 分钟高强度，可等量组合；每周至少 2 天抗阻训练";
    public static final String ACSM_FLEX =
            "ACSM：柔韧性练习每周 ≥2-3 天，每个静态拉伸保持 10-30 秒、重复 2-4 次";
    public static final String NSCA_PERIODIZATION =
            "NSCA《肌力与体能训练精要》：周期化安排（适应期→积累期→强化期→减载），"
                    + "当能以良好动作完成目标次数上限时，负荷渐进 2-10%";
    public static final String FREQUENCY_META =
            "Schoenfeld 等 2016 荟萃分析：同等周训练量下，每肌群每周 ≥2 次优于 1 次";
    public static final String PARQ =
            "PAR-Q+（2021）身体活动准备问卷：用于运动前健康筛查，任一「是」建议先咨询医生";
    public static final String DELOAD =
            "NSCA/ACSM 训练计划共识：每 3-6 周安排一个降低训练量的减载周以管理疲劳";
    public static final String LEVEL_NOTE =
            "训练水平分级与体能自测为简化自评，参考 ACSM 体适能评估思路，不作为医学诊断";
    public static final String VOLUME_DOSE_RESPONSE =
            "Schoenfeld 等 2017 剂量-反应荟萃：每肌群每周 ≥10 组的增长优于 <10 组，"
                    + "但继续加量收益递减且更依赖恢复；组数按主要部位 1 组、间接参与 0.5 组折算";
    public static final String RECOVERY_WINDOW =
            "ACSM 抗阻训练建议：同一肌群不宜连续两天进行大强度训练，"
                    + "两次刺激之间通常需要约 48 小时恢复";
    public static final String CIRCUIT_TRAINING =
            "ACSM：循环抗阻训练（多动作连续进行、组间休息 ≤30 秒）可在较短时间内"
                    + "同时获得肌力与心肺刺激，适合时间受限的训练日";

    // —— 营养 ——
    public static final String CDG_2022 =
            "《中国居民膳食指南(2022)》平衡膳食宝塔：谷类 200-300g（含全谷物和杂豆 50-150g）、"
                    + "薯类 50-100g、蔬菜 300-500g（深色占一半）、水果 200-350g、"
                    + "动物性食物 120-200g（每周至少 2 次水产、每天一个鸡蛋）、"
                    + "奶及奶制品 300-500g、大豆及坚果 25-35g、油 25-30g、盐 <5g、水 1500-1700ml";
    public static final String CDG_FIBER =
            "中国营养学会 DRIs 及《中国居民膳食指南(2022)》：成人膳食纤维每天 25-30g";
    public static final String CDG_PROTEIN_RNI =
            "中国营养学会 DRIs：一般成年人蛋白质 RNI 男 65g/天、女 55g/天（约 0.98g/kg）";
    public static final String SPORT_PROTEIN =
            "Morton 等 2018 荟萃分析与 ISSN 立场声明：抗阻训练人群蛋白质 1.6-2.2g/kg/天有利于增肌与减脂保肌";
    public static final String BMR_FORMULA =
            "Mifflin-St Jeor 公式（1990）：静息能量消耗估算，ADA 评估其在成人中误差最小";
    public static final String ENERGY_RATE =
            "减重速率建议：每周约 0.25-0.5kg（约每天 300-500kcal 缺口），避免极低能量饮食；"
                    + "增肌盈余约 +300kcal/天并配合抗阻训练";
    public static final String FAT_RANGE =
            "中国营养学会 DRIs：成人脂肪供能比 20-30%；添加糖 <50g/天，最好 <25g";
    public static final String ESTIMATE_NOTE =
            "食谱营养数值按《中国食物成分表》常见值估算，仅供对照参考";

    private GuidelineRefs() {
    }
}
