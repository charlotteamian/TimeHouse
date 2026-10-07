package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public final class RecommendationEngine {

    /** 最近练过的动作的降权幅度，与 {@link ProgramComposer} 保持一致。 */
    private static final int RECENT_PENALTY_BASE = 70;
    private static final int RECENT_PENALTY_STEP = 10;

    private final List<Exercise> exercises;

    public RecommendationEngine(List<Exercise> exercises) {
        this.exercises = Collections.unmodifiableList(new ArrayList<Exercise>(exercises));
    }

    public WorkoutPlan recommend(RecommendationInput input) {
        ParsedIntent intent = parseIntent(input);
        List<String> notes = new ArrayList<String>();
        boolean safetyLimited = hasSeverePain(input) || (input.intensity() == Intensity.HIGH && !input.painPoints().isEmpty());
        Intensity effectiveIntensity = hasSeverePain(input) ? Intensity.LOW : input.intensity();
        if (intent.recovery) {
            effectiveIntensity = Intensity.LOW;
        }

        List<ScoredExercise> candidates = new ArrayList<ScoredExercise>();
        for (Exercise exercise : exercises) {
            boolean allowUnverified = input.includeUserUnverified()
                    || input.verifiedExercises().contains(exercise.id())
                    || sharesAny(exercise.targetRegions(), intent.requestedCustom);
            String rejectedReason = hardFilterReason(exercise, input, allowUnverified);
            if (rejectedReason != null) {
                addImportantExclusionNote(notes, exercise, input, rejectedReason);
                continue;
            }

            int score = score(exercise, intent, input);
            if (intent.targeted && !exercise.matchesAnyRegion(intent.goalRegions)
                    && !exercise.matchesAnyPattern(intent.movementPatterns)) {
                continue;
            }
            candidates.add(new ScoredExercise(exercise, score));
        }

        Collections.sort(candidates, new Comparator<ScoredExercise>() {
            @Override
            public int compare(ScoredExercise left, ScoredExercise right) {
                return right.score - left.score;
            }
        });

        List<WorkoutItem> items;
        if (intent.recovery) {
            items = selectRecovery(candidates, input);
        } else if (intent.unknown) {
            items = selectFullBody(candidates, input, effectiveIntensity);
        } else {
            items = selectTargeted(candidates, input, effectiveIntensity);
        }
        if (intent.singleMovement && items.size() > 1) {
            items = new ArrayList<WorkoutItem>(items.subList(0, 1));
        }

        if (items.isEmpty()) {
            safetyLimited = true;
            notes.add("没有足够安全且器械匹配的动作，建议降低强度、调整器械或先咨询专业人士。");
        }

        String title = titleFor(intent, effectiveIntensity, safetyLimited);
        String reason = reasonFor(intent, items);
        int estimatedMinutes = estimatedMinutesFor(input, items);
        addBudgetNote(notes, input, estimatedMinutes, intent.singleMovement);
        String safetyMessage = safetyMessage(input, safetyLimited, notes);
        return new WorkoutPlan(title, effectiveIntensity, estimatedMinutes, items,
                reason, unique(notes), safetyMessage, safetyLimited);
    }

    /**
     * All exercises that pass the hard safety, equipment and evidence filters for this input.
     * Callers (e.g. an AI selector) may reorder or pick among these, but must not add anything
     * outside this set — that keeps injury-avoidance and equipment rules enforced locally.
     */
    public List<Exercise> safeCandidates(RecommendationInput input) {
        ParsedIntent intent = parseIntent(input);
        List<Exercise> result = new ArrayList<Exercise>();
        for (Exercise exercise : exercises) {
            boolean allowUnverified = input.includeUserUnverified()
                    || input.verifiedExercises().contains(exercise.id())
                    || sharesAny(exercise.targetRegions(), intent.requestedCustom);
            if (hardFilterReason(exercise, input, allowUnverified) == null) {
                result.add(exercise);
            }
        }
        return result;
    }

    public WorkoutItem replacementFor(WorkoutItem current,
            RecommendationInput input,
            List<String> currentExerciseIds) {
        ParsedIntent intent = parseIntent(input);
        List<ScoredExercise> candidates = new ArrayList<ScoredExercise>();
        for (Exercise exercise : exercises) {
            if (currentExerciseIds.contains(exercise.id())) {
                continue;
            }
            boolean allowUnverified = input.includeUserUnverified()
                    || input.verifiedExercises().contains(exercise.id());
            if (hardFilterReason(exercise, input, allowUnverified) != null) {
                continue;
            }
            boolean sameRegion = sharesAny(exercise.targetRegions(), current.exercise().targetRegions());
            boolean samePattern = sharesAny(exercise.movementPatterns(), current.exercise().movementPatterns());
            if (!TrainingSelection.sameRole(current.exercise(), exercise)) {
                continue;
            }
            candidates.add(new ScoredExercise(exercise, score(exercise, intent, input)));
        }
        if (candidates.isEmpty()) {
            return null;
        }
        Collections.sort(candidates, new Comparator<ScoredExercise>() {
            @Override
            public int compare(ScoredExercise left, ScoredExercise right) {
                return right.score - left.score;
            }
        });
        return toWorkoutItem(candidates.get(0).exercise, input, input.intensity());
    }

    private ParsedIntent parseIntent(RecommendationInput input) {
        String text = input.intentText();
        ParsedIntent intent = new ParsedIntent();
        intent.singleMovement = text.contains("一个动作") || text.contains("只练一个")
                || text.contains("单个动作") || text.contains("只做一个");
        intent.recovery = text.contains("恢复") || text.contains("放松") || text.contains("拉伸");
        intent.unknown = input.unknownWorkout() || text.contains("不知道") || text.contains("随便")
                || text.contains("全身");

        if (intent.recovery) {
            intent.targeted = false;
            intent.unknown = false;
            Collections.addAll(intent.goalRegions, "核心", "臀", "肩", "背");
            Collections.addAll(intent.movementPatterns, "稳定", "抗伸展", "抗旋转", "肩袖", "髋伸展", "髋铰链");
            return intent;
        }

        if (text.contains("背")) {
            intent.goalRegions.add("背");
            intent.movementPatterns.add("拉");
            intent.targeted = true;
        }
        if (text.contains("腿") || text.contains("下肢")) {
            intent.goalRegions.add("腿");
            intent.goalRegions.add("臀");
            intent.movementPatterns.add("蹲");
            intent.movementPatterns.add("髋铰链");
            intent.movementPatterns.add("单腿");
            intent.targeted = true;
        }
        if (text.contains("胸")) {
            intent.goalRegions.add("胸");
            intent.movementPatterns.add("推");
            intent.targeted = true;
        }
        if (text.contains("肩")) {
            intent.goalRegions.add("肩");
            intent.movementPatterns.add("推");
            intent.movementPatterns.add("稳定");
            intent.targeted = true;
        }
        if (text.contains("核心") || text.contains("腹")) {
            intent.goalRegions.add("核心");
            intent.movementPatterns.add("核心");
            intent.targeted = true;
        }
        if (text.contains("手臂") || text.contains("二头") || text.contains("三头")) {
            intent.goalRegions.add("手臂");
            intent.movementPatterns.add("拉");
            intent.movementPatterns.add("推");
            intent.targeted = true;
        }
        if (text.contains("有氧") || text.contains("心肺")) {
            intent.goalRegions.add("有氧");
            intent.movementPatterns.add("有氧");
            intent.targeted = true;
        }
        if (text.contains("颈")) {
            intent.goalRegions.add("颈");
            intent.movementPatterns.add("颈部");
            intent.targeted = true;
        }
        if (text.contains("上肢")) {
            intent.goalRegions.add("背");
            intent.goalRegions.add("胸");
            intent.goalRegions.add("肩");
            intent.goalRegions.add("手臂");
            intent.movementPatterns.add("拉");
            intent.movementPatterns.add("推");
            intent.targeted = true;
        }

        // Custom groups (e.g. 足球 / 瑜伽): match any non-builtin category named in the text.
        for (String region : customRegionsInPool()) {
            if (text.contains(region)) {
                intent.goalRegions.add(region);
                intent.requestedCustom.add(region);
                intent.targeted = true;
            }
        }

        if (!intent.targeted || intent.unknown) {
            intent.unknown = true;
            intent.targeted = false;
            Collections.addAll(intent.goalRegions, "腿", "臀", "胸", "背", "核心");
            Collections.addAll(intent.movementPatterns, "蹲", "推", "拉", "髋铰链", "抗伸展", "稳定");
        }
        return intent;
    }

    private Set<String> customRegionsInPool() {
        Set<String> builtin = new HashSet<String>(Arrays.asList(
                "背", "胸", "腿", "臀", "肩", "核心", "手臂", "有氧", "颈"));
        Set<String> result = new LinkedHashSet<String>();
        for (Exercise exercise : exercises) {
            for (String region : exercise.targetRegions()) {
                if (!builtin.contains(region)) {
                    result.add(region);
                }
            }
        }
        return result;
    }

    private String hardFilterReason(Exercise exercise, RecommendationInput input, boolean allowUnverified) {
        if (exercise.evidenceStatus() == EvidenceStatus.REJECTED_OR_NEEDS_EDIT) {
            return "动作信息需要编辑，暂不推荐。";
        }
        if (exercise.evidenceStatus() == EvidenceStatus.USER_UNVERIFIED && !allowUnverified) {
            return "未验证动作默认不进入自动推荐。";
        }
        if (!exercise.hasAvailableEquipment(input.equipment())) {
            return "当前器械不可用。";
        }
        for (PainPoint pain : input.painPoints()) {
            StressLevel stress = exercise.jointStress(pain.jointKey());
            if (pain.severity() == PainSeverity.SEVERE && stress.isAtLeast(StressLevel.MEDIUM)) {
                return pain.displayName() + "为急性/严重状态，过滤中高压力动作。";
            }
            if (pain.severity() == PainSeverity.MODERATE && stress == StressLevel.HIGH) {
                return pain.displayName() + "明显不适，过滤高压力动作。";
            }
            if (pain.severity() == PainSeverity.MILD && stress == StressLevel.HIGH) {
                return pain.displayName() + "轻微不适，暂避高压力动作。";
            }
        }
        return null;
    }

    private void addImportantExclusionNote(List<String> notes, Exercise exercise, RecommendationInput input, String reason) {
        if (input.favoriteExercises().contains(exercise.id())) {
            notes.add(exercise.name() + "已标心，但因" + reason + "当前暂不推荐。");
        } else if (reason.contains("未验证")) {
            notes.add(exercise.name() + "是未验证动作，默认不进入自动推荐。");
        } else if (reason.contains("腰") || reason.contains("肩") || reason.contains("膝")) {
            notes.add(exercise.name() + "因" + reason + "已避开。");
        }
    }

    private int score(Exercise exercise, ParsedIntent intent, RecommendationInput input) {
        int score = TrainingSelection.preference(exercise, input.intensity());
        if (exercise.matchesAnyRegion(intent.goalRegions)) {
            score += 90;
        }
        if (exercise.matchesAnyPattern(intent.movementPatterns)) {
            score += 35;
        }
        if (input.favoriteExercises().contains(exercise.id())) {
            score += 50;
        }
        if (exercise.evidenceStatus() == EvidenceStatus.GUIDELINE_BACKED) {
            score += 15;
        }
        if (input.verifiedExercises().contains(exercise.id())) {
            score += 12;
        }
        if (exercise.difficulty().contains("beginner")) {
            score += 8;
        }
        // 刚练过的动作降权：越靠近现在扣得越多，避免每次生成都是同一套。
        int recentIndex = input.recentExerciseIds().indexOf(exercise.id());
        if (recentIndex >= 0) {
            score -= Math.max(0, RECENT_PENALTY_BASE - recentIndex * RECENT_PENALTY_STEP);
        }
        for (PainPoint pain : input.painPoints()) {
            StressLevel stress = exercise.jointStress(pain.jointKey());
            if (stress == StressLevel.MEDIUM) {
                score -= 15;
            } else if (stress == StressLevel.LOW || stress == StressLevel.NONE) {
                score += 6;
            }
        }
        return score;
    }

    private List<WorkoutItem> selectTargeted(List<ScoredExercise> candidates,
            RecommendationInput input,
            Intensity intensity) {
        int targetCount = targetExerciseCount(input, intensity);
        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        for (ScoredExercise candidate : candidates) {
            if (items.size() >= targetCount) {
                break;
            }
            items.add(toWorkoutItem(candidate.exercise, input, intensity));
        }
        return items;
    }

    private List<WorkoutItem> selectFullBody(List<ScoredExercise> candidates,
            RecommendationInput input,
            Intensity intensity) {
        List<String> requiredPatterns = new ArrayList<String>();
        Collections.addAll(requiredPatterns, "蹲", "推", "拉", "髋铰链", "抗伸展", "稳定");
        int targetCount = targetExerciseCount(input, intensity);
        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        Set<String> usedIds = new LinkedHashSet<String>();

        for (String pattern : requiredPatterns) {
            if (items.size() >= targetCount) {
                break;
            }
            for (ScoredExercise candidate : candidates) {
                if (!usedIds.contains(candidate.exercise.id()) && candidate.exercise.movementPatterns().contains(pattern)) {
                    items.add(toWorkoutItem(candidate.exercise, input, intensity));
                    usedIds.add(candidate.exercise.id());
                    break;
                }
            }
        }

        for (ScoredExercise candidate : candidates) {
            if (items.size() >= targetCount) {
                break;
            }
            if (!usedIds.contains(candidate.exercise.id())) {
                items.add(toWorkoutItem(candidate.exercise, input, intensity));
                usedIds.add(candidate.exercise.id());
            }
        }
        return items;
    }

    private List<WorkoutItem> selectRecovery(List<ScoredExercise> candidates, RecommendationInput input) {
        List<String> gentlePatterns = Arrays.asList("稳定", "抗伸展", "抗旋转", "肩袖", "髋伸展", "髋铰链");
        int targetCount = targetExerciseCount(input, Intensity.LOW);
        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        Set<String> usedIds = new LinkedHashSet<String>();

        for (ScoredExercise candidate : candidates) {
            if (items.size() >= targetCount) {
                break;
            }
            Exercise exercise = candidate.exercise;
            boolean gentle = exercise.matchesAnyPattern(gentlePatterns)
                    || exercise.targetRegions().contains("核心");
            boolean lowImpact = exercise.jointStress("lower_back").isAtLeast(StressLevel.HIGH) == false
                    && exercise.jointStress("knee").isAtLeast(StressLevel.HIGH) == false;
            if (gentle && lowImpact && !usedIds.contains(exercise.id())) {
                items.add(toWorkoutItem(exercise, input, Intensity.LOW));
                usedIds.add(exercise.id());
            }
        }

        for (ScoredExercise candidate : candidates) {
            if (items.size() >= targetCount) {
                break;
            }
            if (!usedIds.contains(candidate.exercise.id())) {
                items.add(toWorkoutItem(candidate.exercise, input, Intensity.LOW));
                usedIds.add(candidate.exercise.id());
            }
        }
        return items;
    }

    /**
     * 用时间预算反解动作数：按该强度档的典型处方算出单个动作要多久，再看预算装得下几个。
     * 以前是写死的查表（40 分钟 → 5 个），和最终生效的处方之间没有任何回算，
     * 于是"预计 40 分钟"的课实际只要 11 分钟。
     */
    private int targetExerciseCount(RecommendationInput input, Intensity intensity) {
        int minutes = input.targetMinutes();
        if (minutes <= 0) {
            return intensity.maxExercises();
        }
        SessionTimeModel model = new SessionTimeModel(input.paceFactor());
        return model.fitExerciseCount(minutes, typicalPrescription(intensity), 1,
                intensity.maxExercises());
    }

    /** 各强度档的典型处方，与 {@code Exercise.Builder} 的默认值一致，用来做时间预算。 */
    static Prescription typicalPrescription(Intensity intensity) {
        switch (intensity) {
            case LOW:
                return new Prescription(2, "10-12", "5-6", 75);
            case HIGH:
                return new Prescription(4, "6-10", "7-8", 120);
            case MEDIUM:
            default:
                return new Prescription(3, "8-12", "6-8", 90);
        }
    }

    /** 时长是算出来的，不是把用户输入原样回显。 */
    private int estimatedMinutesFor(RecommendationInput input, List<WorkoutItem> items) {
        return new SessionTimeModel(input.paceFactor()).sessionMinutes(items);
    }

    /**
     * 算出来比想练的时间短就直说，不假装填满了预算。
     * 差距来自强度档的动作数上限——那是训练量的安全上限，不该为了凑时间突破。
     */
    private void addBudgetNote(List<String> notes, RecommendationInput input,
            int estimatedMinutes, boolean singleMovement) {
        int requested = input.targetMinutes();
        if (singleMovement || requested <= 0 || estimatedMinutes <= 0) {
            return;
        }
        if (estimatedMinutes < requested - 5) {
            notes.add("这套主课约 " + estimatedMinutes + " 分钟，比你选的 " + requested
                    + " 分钟短：" + input.intensity().label() + "强度下动作数已到上限（"
                    + input.intensity().maxExercises() + " 个）。想填满时间可以提高强度，或补一段有氧。");
        } else if (estimatedMinutes > requested + 8) {
            notes.add("这套主课约 " + estimatedMinutes + " 分钟，比你选的 " + requested
                    + " 分钟长，时间紧的话可以先做前几个动作。");
        }
    }

    private WorkoutItem toWorkoutItem(Exercise exercise, RecommendationInput input, Intensity intensity) {
        boolean favorite = input.favoriteExercises().contains(exercise.id());
        String reason = favorite ? "已标心且通过安全、器械和证据过滤" : "匹配目标、器械和当前安全设置";
        Prescription prescription = ExerciseTempo.effective(exercise, exercise.prescription(intensity));
        return new WorkoutItem(exercise, prescription, favorite, reason);
    }

    private String titleFor(ParsedIntent intent, Intensity intensity, boolean safetyLimited) {
        String prefix = safetyLimited ? "安全降级 · " : "";
        if (intent.recovery) {
            return prefix + "恢复 · 灵活性与核心稳定";
        }
        if (intent.unknown) {
            return prefix + intensity.label() + "强度全身训练";
        }
        if (!intent.requestedCustom.isEmpty()) {
            return prefix + intensity.label() + "强度 · " + intent.requestedCustom.get(0) + "训练";
        }
        if (intent.goalRegions.contains("背")) {
            return prefix + intensity.label() + "强度背部训练";
        }
        if (intent.goalRegions.contains("胸")) {
            return prefix + intensity.label() + "强度胸部训练";
        }
        if (intent.goalRegions.contains("腿")) {
            return prefix + intensity.label() + "强度下肢训练";
        }
        if (intent.goalRegions.contains("肩")) {
            return prefix + intensity.label() + "强度上肢训练";
        }
        if (intent.goalRegions.contains("核心")) {
            return prefix + intensity.label() + "强度核心训练";
        }
        if (intent.goalRegions.contains("手臂")) {
            return prefix + intensity.label() + "强度手臂训练";
        }
        if (intent.goalRegions.contains("有氧")) {
            return prefix + intensity.label() + "强度有氧训练";
        }
        if (intent.goalRegions.contains("颈")) {
            return prefix + intensity.label() + "强度颈部训练";
        }
        return prefix + intensity.label() + "强度训练";
    }

    private String reasonFor(ParsedIntent intent, List<WorkoutItem> items) {
        if (intent.recovery) {
            return "恢复日组合以核心稳定、髋部和肩部灵活性为主，统一使用低强度，帮助在训练间隙保持活动而不增加关节负担。";
        }
        if (intent.unknown) {
            return "默认生成全身组合，尽量覆盖推、拉、下肢、髋和核心稳定，并按器械与伤痛设置过滤。";
        }
        return "根据目标部位和动作类型筛选，再按风险低、器械匹配、来源可信和标心偏好排序。";
    }

    private String safetyMessage(RecommendationInput input, boolean safetyLimited, List<String> notes) {
        if (hasSeverePain(input)) {
            return "已按急性/严重伤痛降低推荐风险。如果疼痛明显、麻木、放射痛或持续加重，请先咨询医生或物理治疗师。";
        }
        if (safetyLimited) {
            return "已根据你的伤痛设置避开部分动作。训练中如疼痛加重，请停止当前动作。";
        }
        if (!notes.isEmpty()) {
            return "已根据你的伤痛设置避开部分动作。训练中如疼痛加重，请停止当前动作。";
        }
        return "训练建议遵循低起点、慢进阶原则；如出现疼痛加重请停止。";
    }

    private boolean hasSeverePain(RecommendationInput input) {
        for (PainPoint pain : input.painPoints()) {
            if (pain.severity() == PainSeverity.SEVERE) {
                return true;
            }
        }
        return false;
    }

    private List<String> unique(List<String> notes) {
        return new ArrayList<String>(new LinkedHashSet<String>(notes));
    }

    private boolean sharesAny(List<String> left, List<String> right) {
        for (String value : left) {
            if (right.contains(value)) {
                return true;
            }
        }
        return false;
    }

    private static final class ParsedIntent {
        private final List<String> goalRegions = new ArrayList<String>();
        private final List<String> movementPatterns = new ArrayList<String>();
        private final List<String> requestedCustom = new ArrayList<String>();
        private boolean singleMovement;
        private boolean targeted;
        private boolean unknown;
        private boolean recovery;
    }

    private static final class ScoredExercise {
        private final Exercise exercise;
        private final int score;

        private ScoredExercise(Exercise exercise, int score) {
            this.exercise = exercise;
            this.score = score;
        }
    }
}
