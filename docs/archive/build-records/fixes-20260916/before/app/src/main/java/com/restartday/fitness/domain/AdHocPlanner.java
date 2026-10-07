package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * 临时加练：当天临时想动一下时的组合生成。
 *
 * <p>和计划课的根本区别是**求解方向相反**：
 * 计划课里处方是周期计划定死的、时长是算出来的结果；
 * 加练里时长是硬约束——说 15 分钟就必须 15 分钟，动作数和组数是被解出来的。
 *
 * <p>另外加练不能把计划毁掉，所以要读三样东西：
 * 最近练过什么（{@link RecoveryState}）、明天计划课要练什么、
 * 本周各肌群还剩多少容量（{@link WeeklyVolumeLedger}）。
 */
public final class AdHocPlanner {

    /** 循环模式的组间休息，短到能带起心肺（ACSM 循环抗阻）。 */
    private static final int CIRCUIT_REST_SECONDS = 30;
    private static final int RECOVERY_REST_SECONDS = 30;

    private static final int SCORE_REGION_MATCH = 60;
    private static final int SCORE_UNDERWORKED = 25;
    private static final int SCORE_GUIDELINE = 20;
    private static final int SCORE_FAVORITE = 15;
    private static final int SCORE_BEGINNER = 8;
    private static final int PENALTY_RECOVERING = 45;
    private static final int PENALTY_TOMORROW = 35;
    /**
     * 最近完成或刚推荐过的动作只降权、不封禁：候选不足时仍能回退，候选充足时则
     * 在相同的蹲 / 髋 / 推 / 拉 / 核心槽位内换动作。这样既保留训练结构，也避免
     * 用户连续点“重新安排”时总看到同一套。
     */
    private static final int RECENT_PENALTY_BASE = 72;
    private static final int RECENT_PENALTY_STEP = 3;

    /** 同一个动作模式最多出现两次，避免一套里全是同质动作。 */
    private static final int MAX_PER_PATTERN = 2;

    private AdHocPlanner() {
    }

    /** 加练的输入。伤痛/器械过滤在外面由 {@link RecommendationEngine#safeCandidates} 完成。 */
    public static final class Request {
        private AdHocIntent intent = AdHocIntent.parse("");
        private int minutes = 15;
        private Intensity intensity = Intensity.MEDIUM;
        private TrainingLevel level = TrainingLevel.BEGINNER;
        private double paceFactor = 1.0;
        private RecoveryState recovery = RecoveryState.of(null, 0);
        private WeeklyVolumeLedger ledger;
        private Set<String> tomorrowRegions = new LinkedHashSet<String>();
        private Set<String> favoriteIds = new LinkedHashSet<String>();
        private List<String> recentExerciseIds = new ArrayList<String>();

        public Request intent(AdHocIntent value) {
            intent = value == null ? AdHocIntent.parse("") : value;
            return this;
        }

        public Request minutes(int value) {
            minutes = Math.max(3, value);
            return this;
        }

        public Request intensity(Intensity value) {
            intensity = value == null ? Intensity.MEDIUM : value;
            return this;
        }

        public Request level(TrainingLevel value) {
            level = value == null ? TrainingLevel.BEGINNER : value;
            return this;
        }

        public Request paceFactor(double value) {
            paceFactor = value;
            return this;
        }

        public Request recovery(RecoveryState value) {
            recovery = value == null ? RecoveryState.of(null, 0) : value;
            return this;
        }

        public Request ledger(WeeklyVolumeLedger value) {
            ledger = value;
            return this;
        }

        /** 明天计划课要练的部位——加练避开它，否则明天那节课的质量会崩。 */
        public Request tomorrowRegions(Set<String> value) {
            tomorrowRegions = value == null ? new LinkedHashSet<String>() : value;
            return this;
        }

        public Request favoriteIds(Set<String> value) {
            favoriteIds = value == null ? new LinkedHashSet<String>() : value;
            return this;
        }

        public Request recentExerciseIds(List<String> value) {
            recentExerciseIds = value == null ? new ArrayList<String>() : value;
            return this;
        }
    }

    /**
     * 解出一套刚好塞进时间预算的加练。
     *
     * @param safePool 已经过伤痛/器械/证据过滤的候选
     */
    public static WorkoutPlan plan(List<Exercise> safePool, Request request) {
        AdHocIntent intent = request.intent;
        Intensity effectiveIntensity = intent.mode() == AdHocIntent.Mode.RECOVERY ? Intensity.LOW : request.intensity;
        int minutes = intent.minutes() > 0 ? intent.minutes() : request.minutes;
        List<String> notes = new ArrayList<String>();

        List<String> targets = resolveTargets(request, intent, notes);
        List<Exercise> ranked = rank(safePool, request, intent, targets);
        if (ranked.isEmpty()) {
            return new WorkoutPlan(titleFor(intent, minutes), effectiveIntensity, 0,
                    new ArrayList<WorkoutItem>(),
                    "当前器械、伤痛和排除条件下没有可用动作。",
                    notes, "请调整器械或放宽排除条件后再试。", true);
        }

        int wantedCount = intent.singleMovement() ? 1 : countFor(minutes, intent.mode());
        List<Exercise> picked = pick(ranked, Math.min(wantedCount, ranked.size()), intent);
        if (picked.size() < wantedCount && intent.hasTarget()) {
            notes.add("当前器械和安全设置下，" + join(intent.regions()) + "只有 " + picked.size()
                    + " 个可用动作，剩下的时间用来把组数做够。");
        }

        if (!intent.hasTarget() && !intent.singleMovement() && intent.mode() != AdHocIntent.Mode.RECOVERY) {
            for (String role : new String[]{"髋铰链", "推", "拉", "蹲"}) {
                boolean available = false;
                for (Exercise e : ranked) if (TrainingSelection.matches(e, role)) available = true;
                if (!available) notes.add("当前器械 / 恢复条件缺少「" + role + "」候选，本次无法覆盖该模式。");
            }
        }
        Solution solution = solve(picked, request, intent, minutes);
        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        for (int i = 0; i < solution.count; i++) {
            Exercise exercise = picked.get(i);
            items.add(new WorkoutItem(exercise,
                    ExerciseTempo.effective(exercise, solution.prescription),
                    request.favoriteIds.contains(exercise.id()),
                    TrainingSelection.role(exercise) + " · " + String.join(" / ", exercise.equipment())
                            + " · " + reasonForItem(exercise, request, targets)));
        }

        SessionTimeModel model = new SessionTimeModel(request.paceFactor);
        int estimated = model.sessionMinutes(items);
        addPlanNotes(notes, request, intent, items, minutes, estimated, solution);

        return new WorkoutPlan(titleFor(intent, minutes), effectiveIntensity, estimated, items,
                reasonFor(intent, targets, solution, minutes), notes,
                safetyMessageFor(intent), false);
    }

    /** 这套加练会给各肌群加多少组——用来记账和提示代价。 */
    public static List<TrainingLoad> loadOf(List<WorkoutItem> items, long atMillis) {
        List<TrainingLoad> loads = new ArrayList<TrainingLoad>();
        for (WorkoutItem item : items) {
            loads.add(new TrainingLoad(item.exercise().targetRegions(),
                    item.prescription().sets(), atMillis));
        }
        return loads;
    }

    // ------------------------------------------------------------------ 目标部位

    /**
     * 用户点名了就练点名的；没点名就自己挑：优先补本周欠刺激、且不在恢复窗口、
     * 也不是明天计划课要练的部位。
     */
    private static List<String> resolveTargets(Request request, AdHocIntent intent,
            List<String> notes) {
        if (intent.hasTarget()) {
            List<String> targets = new ArrayList<String>(intent.regions());
            for (String region : targets) {
                if (request.recovery.isRecovering(region)) {
                    notes.add(request.recovery.describe(region)
                            + "，还在恢复窗口内（约 48 小时）：这次按较轻的量安排。");
                }
                if (request.tomorrowRegions.contains(region)) {
                    notes.add("明天的计划课要练" + region + "：今天练它会影响明天那节课，"
                            + "建议只做轻量或换个部位。");
                }
            }
            return targets;
        }

        List<String> targets = new ArrayList<String>();
        if (request.ledger != null) {
            for (WeeklyVolumeLedger.Entry entry : request.ledger.underworked()) {
                String region = entry.region();
                if (!request.recovery.isRecovering(region)
                        && !request.tomorrowRegions.contains(region)
                        && !intent.excludedRegions().contains(region)) {
                    targets.add(region);
                }
            }
        }
        if (targets.isEmpty()) {
            for (String region : WeeklyVolumeLedger.RESISTANCE_REGIONS) {
                if (!request.recovery.isBlocked(region)
                        && !request.tomorrowRegions.contains(region)
                        && !intent.excludedRegions().contains(region)) {
                    targets.add(region);
                }
            }
        } else {
            notes.add("没指定部位，按本周还欠刺激的肌群来选："
                    + join(targets) + "（避开了刚练过的和明天计划要练的）。");
        }
        return targets;
    }

    // -------------------------------------------------------------------- 选动作

    private static List<Exercise> rank(List<Exercise> safePool, final Request request,
            final AdHocIntent intent, final List<String> targets) {
        List<Exercise> candidates = new ArrayList<Exercise>();
        List<Exercise> offTarget = new ArrayList<Exercise>();
        for (Exercise exercise : safePool) {
            if (request.level == TrainingLevel.BEGINNER && exercise.movementPatterns().contains("爆发力")) continue;
            if (sharesAny(exercise.targetRegions(), intent.excludedRegions())) {
                continue;
            }
            // 24 小时内刚练过的部位直接跳过，除非用户自己点名要练。
            boolean named = sharesAny(exercise.targetRegions(), intent.regions());
            if (!named && blockedByRecovery(exercise, request)) {
                continue;
            }
            if (intent.mode() == AdHocIntent.Mode.RECOVERY && !isGentle(exercise)) {
                continue;
            }
            // 点名要练哪里就练哪里：其他部位只作为候选不足时的备份。
            // 冲突（明天要练 / 还在恢复）用提示说明，不能悄悄换成别的部位。
            if (intent.hasTarget() && !named) {
                offTarget.add(exercise);
                continue;
            }
            candidates.add(exercise);
        }
        sortByScore(candidates, request, intent, targets);
        // 点名了部位就只给那个部位；候选实在太少（<2）才退回其他部位补位。
        if (!intent.hasTarget() || candidates.size() < 2) {
            sortByScore(offTarget, request, intent, targets);
            candidates.addAll(offTarget);
        }
        return candidates;
    }

    private static void sortByScore(List<Exercise> candidates, final Request request,
            final AdHocIntent intent, final List<String> targets) {
        Collections.sort(candidates, new Comparator<Exercise>() {
            @Override
            public int compare(Exercise left, Exercise right) {
                int diff = score(right, request, intent, targets)
                        - score(left, request, intent, targets);
                return diff != 0 ? diff : left.id().compareTo(right.id());
            }
        });
    }

    private static int score(Exercise exercise, Request request, AdHocIntent intent,
            List<String> targets) {
        int score = TrainingSelection.preference(exercise, intent.mode() == AdHocIntent.Mode.RECOVERY
                ? Intensity.LOW : request.intensity);
        if (sharesAny(exercise.targetRegions(), targets)) {
            score += SCORE_REGION_MATCH;
        }
        if (request.ledger != null) {
            for (String region : exercise.targetRegions()) {
                WeeklyVolumeLedger.Entry entry = request.ledger.forRegion(region);
                if (entry == null) {
                    continue;
                }
                if (entry.status() == WeeklyVolumeLedger.Status.LOW) {
                    score += SCORE_UNDERWORKED;
                } else if (entry.status() == WeeklyVolumeLedger.Status.HIGH) {
                    score -= SCORE_UNDERWORKED;
                }
            }
        }
        if (exercise.evidenceStatus() == EvidenceStatus.GUIDELINE_BACKED) {
            score += SCORE_GUIDELINE;
        }
        if (request.favoriteIds.contains(exercise.id())) {
            score += SCORE_FAVORITE;
        }
        if (exercise.difficulty().contains("beginner")) {
            score += SCORE_BEGINNER;
        }
        for (String region : exercise.targetRegions()) {
            // 用户点名的部位不扣分——冲突已经在说明里提示过了，不能因此把它挤出计划。
            if (intent.regions().contains(region)) {
                continue;
            }
            if (request.recovery.isRecovering(region)) {
                score -= PENALTY_RECOVERING;
            }
            if (request.tomorrowRegions.contains(region)) {
                score -= PENALTY_TOMORROW;
            }
        }
        int recentIndex = request.recentExerciseIds.indexOf(exercise.id());
        if (recentIndex >= 0) {
            score -= Math.max(0, RECENT_PENALTY_BASE - recentIndex * RECENT_PENALTY_STEP);
        }
        return score;
    }

    /** 按分数取前 N，但同一个动作模式最多两个，免得一套全是同质动作。 */
    private static List<Exercise> pick(List<Exercise> ranked, int count, AdHocIntent intent) {
        List<Exercise> picked = new ArrayList<Exercise>();
        // Main patterns precede accessories; a missing pattern is never replaced by duplicate core work.
        if (intent.mode() != AdHocIntent.Mode.RECOVERY && !intent.singleMovement()) {
            String[] slots = intent.hasTarget()
                    ? new String[]{"蹲", "髋铰链", "推", "拉", "核心", "有氧"}
                    : new String[]{"髋铰链", "推", "拉", "蹲", "核心"};
            Set<String> usedEquipment = new LinkedHashSet<String>();
            for (String slot : slots) {
                if (picked.size() >= count) break;
                Exercise best = null;
                int bestPreference = Integer.MIN_VALUE;
                for (int i = 0; i < ranked.size(); i++) {
                    Exercise e = ranked.get(i);
                    if (picked.contains(e) || !TrainingSelection.matches(e, slot)) continue;
                    int preference = -i * 3;
                    if (TrainingSelection.loaded(e) && Collections.disjoint(e.equipment(), usedEquipment)) preference += 8;
                    if (preference > bestPreference) { best = e; bestPreference = preference; }
                }
                if (best != null) { picked.add(best); usedEquipment.addAll(best.equipment()); }
            }
        }
        Map<String, Integer> patternUse = new HashMap<String, Integer>();
        for (Exercise e : picked) patternUse.merge(TrainingSelection.role(e), 1, Integer::sum);
        for (Exercise exercise : ranked) {
            if (picked.size() >= count) break;
            String role = TrainingSelection.role(exercise);
            int limit = role.equals("核心") ? 1 : MAX_PER_PATTERN;
            if (picked.contains(exercise) || patternUse.getOrDefault(role, 0) >= limit) continue;
            picked.add(exercise);
            patternUse.merge(role, 1, Integer::sum);
        }
        return picked;
    }

    // -------------------------------------------------------------- 时长硬约束求解

    private static final class Solution {
        private int count;
        private int sets;
        private Prescription prescription;
        private boolean trimmed;   // 为了塞进预算砍过动作数
    }

    /**
     * 时长是硬约束，组数和动作数是解。
     * 先在目标动作数上找塞得下的最大组数；组数掉到 1 组还塞不下，就减动作数再试——
     * 与其做 5 个动作各 1 组，不如做 3 个动作各 2-3 组。
     */
    private static Solution solve(List<Exercise> picked, Request request, AdHocIntent intent,
            int minutes) {
        SessionTimeModel model = new SessionTimeModel(request.paceFactor);
        int budgetSeconds = minutes * 60;
        int maxSets = maxSetsFor(intent.mode(), request.intensity);

        Solution fallback = new Solution();
        fallback.count = 1;
        fallback.sets = 1;
        fallback.prescription = prescriptionFor(intent, request, 1);

        for (int count = picked.size(); count >= 1; count--) {
            for (int sets = maxSets; sets >= 1; sets--) {
                Prescription prescription = prescriptionFor(intent, request, sets);
                if (fits(model, picked, count, prescription, budgetSeconds)) {
                    if (sets >= 2 || count == 1) {
                        Solution solution = new Solution();
                        solution.count = count;
                        solution.sets = sets;
                        solution.prescription = prescription;
                        solution.trimmed = count < picked.size();
                        return solution;
                    }
                    // 只塞得下 1 组：记下来，但先试试少做几个动作能不能换到 2 组以上。
                    fallback.count = count;
                    fallback.sets = sets;
                    fallback.prescription = prescription;
                    fallback.trimmed = count < picked.size();
                    break;
                }
            }
        }
        return fallback;
    }

    private static boolean fits(SessionTimeModel model, List<Exercise> picked, int count,
            Prescription prescription, int budgetSeconds) {
        int total = 0;
        for (int i = 0; i < count; i++) {
            total += model.itemSeconds(ExerciseTempo.effective(picked.get(i), prescription));
        }
        return total <= budgetSeconds;
    }

    private static int maxSetsFor(AdHocIntent.Mode mode, Intensity intensity) {
        if (mode == AdHocIntent.Mode.RECOVERY) {
            return 2;
        }
        return intensity == Intensity.HIGH ? 4 : 3;
    }

    private static Prescription prescriptionFor(AdHocIntent intent, Request request, int sets) {
        switch (intent.mode()) {
            case CONDITIONING:
                return new Prescription(sets, "12-15", "6-7", CIRCUIT_REST_SECONDS);
            case RECOVERY:
                return new Prescription(sets, "10-12", "4-5", RECOVERY_REST_SECONDS);
            case STRENGTH:
            default:
                switch (request.intensity) {
                    case LOW:
                        return new Prescription(sets, "10-12", "5-6", 60);
                    case HIGH:
                        return new Prescription(sets, "6-10", "7-8", 90);
                    default:
                        return new Prescription(sets, "8-12", "7-8", 75);
                }
        }
    }

    /** 时间预算对应的动作数上限；循环模式动作多一点、每个动作组数少一点。 */
    private static int countFor(int minutes, AdHocIntent.Mode mode) {
        int base;
        if (minutes <= 10) {
            base = 2;
        } else if (minutes <= 20) {
            base = 3;
        } else if (minutes <= 35) {
            base = 5;
        } else if (minutes <= 50) {
            base = 5;
        } else {
            base = 6;
        }
        return mode == AdHocIntent.Mode.CONDITIONING ? base + 1 : base;
    }

    // ---------------------------------------------------------------------- 文案

    private static void addPlanNotes(List<String> notes, Request request, AdHocIntent intent,
            List<WorkoutItem> items, int minutes, int estimated, Solution solution) {
        if (solution.trimmed) {
            notes.add(minutes + " 分钟只排得下 " + items.size() + " 个动作 × " + solution.sets
                    + " 组——与其每个动作只做 1 组，不如少做几个动作把组数做够。");
        }
        if (estimated > 0 && estimated < minutes - 4) {
            notes.add("按当前动作、组数与恢复条件，主课约 " + estimated + " 分钟；" + minutes
                    + " 分钟是可用上限，不靠重复辅助动作填满。");
        }
        if (request.ledger != null) {
            List<TrainingLoad> planned = loadOf(items, System.currentTimeMillis());
            notes.addAll(request.ledger.warningsFor(planned));
            String cost = volumeCost(items);
            if (cost.length() > 0) {
                notes.add("这次加练会占用本周容量：" + cost + "。");
            }
        }
        if (intent.mode() == AdHocIntent.Mode.CONDITIONING) {
            notes.add("循环模式：组间只休息 " + CIRCUIT_REST_SECONDS
                    + " 秒，动作之间尽量不停，靠密度带起心肺。");
        }
        if (!request.recentExerciseIds.isEmpty()) {
            notes.add("轮换规则：保留蹲 / 髋 / 推 / 拉 / 核心等训练结构，优先换掉最近完成或刚推荐过的同类动作；候选不足时才复用。");
        }
    }

    private static String volumeCost(List<WorkoutItem> items) {
        Map<String, Integer> perRegion = new HashMap<String, Integer>();
        for (WorkoutItem item : items) {
            String region = item.exercise().targetRegions().isEmpty()
                    ? "" : item.exercise().targetRegions().get(0);
            if (region.length() == 0) {
                continue;
            }
            Integer prior = perRegion.get(region);
            perRegion.put(region, (prior == null ? 0 : prior) + item.prescription().sets());
        }
        StringBuilder builder = new StringBuilder();
        for (Map.Entry<String, Integer> entry : perRegion.entrySet()) {
            if (builder.length() > 0) {
                builder.append("、");
            }
            builder.append(entry.getKey()).append(" ").append(entry.getValue()).append(" 组");
        }
        return builder.toString();
    }

    private static String titleFor(AdHocIntent intent, int minutes) {
        switch (intent.mode()) {
            case CONDITIONING:
                return minutes + " 分钟循环加练";
            case RECOVERY:
                return minutes + " 分钟恢复活动";
            default:
                return intent.hasTarget()
                        ? "专项训练 · " + join(intent.regions())
                        : "全身力量 · 日常训练";
        }
    }

    private static String reasonFor(AdHocIntent intent, List<String> targets, Solution solution,
            int minutes) {
        StringBuilder builder = new StringBuilder();
        builder.append("先安排髋、推、拉、蹲与核心，目标部位和可用候选决定本次覆盖；主动作优先使用已选器械，辅助动作放后。重新安排时保留这些动作模式，只在同类候选中轮换，既有变化也不破坏训练结构。时间按处方核算：").append(minutes).append(" 分钟的预算先扣掉动作切换和组间休息，")
                .append("再解出 ").append(solution.count).append(" 个动作 × ")
                .append(solution.sets).append(" 组。");
        if (!targets.isEmpty()) {
            builder.append("部位选的是 ").append(join(targets)).append("。");
        }
        switch (intent.mode()) {
            case CONDITIONING:
                builder.append(GuidelineRefs.CIRCUIT_TRAINING);
                break;
            case RECOVERY:
                builder.append("恢复模式只保留低关节压力的动作，目的是活动开而不是加训练量。");
                break;
            default:
                builder.append("近期训练与明日计划参与恢复筛选及排序（")
                        .append(GuidelineRefs.RECOVERY_WINDOW).append("）。");
                break;
        }
        return builder.toString();
    }

    private static String reasonForItem(Exercise exercise, Request request, List<String> targets) {
        if (request.favoriteIds.contains(exercise.id())) {
            return "已标心且通过安全与器械过滤";
        }
        if (request.ledger != null) {
            for (String region : exercise.targetRegions()) {
                WeeklyVolumeLedger.Entry entry = request.ledger.forRegion(region);
                if (entry != null && entry.status() == WeeklyVolumeLedger.Status.LOW) {
                    return "补本周欠刺激的" + region;
                }
            }
        }
        if (sharesAny(exercise.targetRegions(), targets)) {
            return "匹配今天想练的部位";
        }
        return "通过安全与器械过滤";
    }

    private static String safetyMessageFor(AdHocIntent intent) {
        if (intent.mode() == AdHocIntent.Mode.RECOVERY) {
            return "恢复日以活动开为主：动作幅度舒服就好，出现疼痛就停。";
        }
        return "加练也算训练量，会计入本周容量；如果疼痛加重请停止当前动作。";
    }

    // ---------------------------------------------------------------------- 工具

    private static boolean blockedByRecovery(Exercise exercise, Request request) {
        for (String region : exercise.targetRegions()) {
            if (request.recovery.isBlocked(region)) {
                return true;
            }
        }
        return false;
    }

    private static boolean isGentle(Exercise exercise) {
        return !exercise.jointStress("lower_back").isAtLeast(StressLevel.HIGH)
                && !exercise.jointStress("knee").isAtLeast(StressLevel.HIGH)
                && !exercise.jointStress("shoulder").isAtLeast(StressLevel.HIGH);
    }

    private static boolean sharesAny(List<String> left, List<String> right) {
        for (String value : left) {
            if (right.contains(value)) {
                return true;
            }
        }
        return false;
    }

    private static String join(List<String> values) {
        StringBuilder builder = new StringBuilder();
        for (String value : values) {
            if (builder.length() > 0) {
                builder.append(" / ");
            }
            builder.append(value);
        }
        return builder.toString();
    }
}
