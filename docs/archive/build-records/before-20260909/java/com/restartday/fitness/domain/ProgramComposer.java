package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * 按当日分化的「动作模式槽位」编排一次训练。
 *
 * <p>修的是这个问题：以前计划课把 {@link ProgramFocus} 拼成一句意图文本丢给关键词解析器，
 * 走的是"按分数排序取前 N"，{@link ProgramFocus#patterns()} 里定义的 蹲/推/拉/髋铰链
 * 从来没参与过生成。结果就是"全身 A"排出 俯卧撑+臀桥+死虫+鸟狗——没有蹲、没有拉，
 * 两个同质的抗伸展核心占掉一半名额。
 *
 * <p>这里改成：先按分化声明的模式建槽位，每个槽位在通过安全/器械过滤的候选里选，
 * 并对最近练过的动作降权，保证全身 A/B/C 真的不一样。
 */
public final class ProgramComposer {

    /** 最近用过的动作的降权幅度（越靠近现在扣得越多），保证跨天不重复。 */
    private static final int FRESHNESS_PENALTY_BASE = 70;
    private static final int FRESHNESS_PENALTY_STEP = 10;

    private static final int SCORE_REGION_MATCH = 40;
    private static final int SCORE_GUIDELINE_BACKED = 25;
    private static final int SCORE_FAVORITE = 15;
    private static final int SCORE_BEGINNER = 10;

    private ProgramComposer() {
    }

    /** 一个待填的槽位：优先按动作模式填，模式填不到再退到部位。 */
    public static final class Slot {
        private final String pattern;
        private final String region;

        private Slot(String pattern, String region) {
            this.pattern = pattern;
            this.region = region;
        }

        public static Slot pattern(String value) {
            return new Slot(value, null);
        }

        public static Slot region(String value) {
            return new Slot(null, value);
        }

        public boolean isPattern() {
            return pattern != null;
        }

        /** 稳定的字符串标识，用于持久化"这一天第几个槽位换成了哪个动作"。 */
        public String key() {
            return pattern != null ? "p:" + pattern : "r:" + region;
        }

        public String label() {
            return pattern != null ? pattern : region;
        }

        public static Slot parse(String key) {
            if (key == null || key.length() < 3) {
                return region("核心");
            }
            String value = key.substring(2);
            return key.startsWith("p:") ? pattern(value) : region(value);
        }

        boolean matches(Exercise exercise) {
            return pattern != null
                    ? exercise.movementPatterns().contains(pattern)
                    : exercise.targetRegions().contains(region);
        }
    }

    /** 一天编排的结果：动作、每个动作占的槽位、以及没填满时的说明。 */
    public static final class ComposedDay {
        private final List<WorkoutItem> items;
        private final List<String> slotKeys;
        private final List<String> notes;

        ComposedDay(List<WorkoutItem> items, List<String> slotKeys, List<String> notes) {
            this.items = Collections.unmodifiableList(items);
            this.slotKeys = Collections.unmodifiableList(slotKeys);
            this.notes = Collections.unmodifiableList(notes);
        }

        public List<WorkoutItem> items() {
            return items;
        }

        public List<String> slotKeys() {
            return slotKeys;
        }

        public List<String> notes() {
            return notes;
        }

        public List<String> exerciseIds() {
            List<String> ids = new ArrayList<String>(items.size());
            for (WorkoutItem item : items) {
                ids.add(item.exercise().id());
            }
            return ids;
        }
    }

    /** 当日的槽位清单：先按分化声明的动作模式，不够再按部位轮转补齐。 */
    public static List<Slot> slotsFor(ProgramFocus focus, int targetCount) {
        List<Slot> slots = new ArrayList<Slot>();
        for (String pattern : focus.patterns()) {
            if (slots.size() >= targetCount) {
                break;
            }
            slots.add(Slot.pattern(pattern));
        }
        List<String> regions = focus.regions();
        int index = 0;
        while (slots.size() < targetCount && !regions.isEmpty()) {
            slots.add(Slot.region(regions.get(index % regions.size())));
            index++;
        }
        return slots;
    }

    /**
     * 编排一天的训练。
     *
     * @param safePool     已经过安全 / 器械 / 证据过滤的候选（{@link RecommendationEngine#safeCandidates}）
     * @param recentIds    最近用过的动作 id，按时间倒序（下标 0 = 最近一次），用于跨天去重
     */
    public static ComposedDay composeDay(ProgramFocus focus, Prescription phasePrescription,
            List<Exercise> safePool, int targetCount,
            List<String> recentIds, Set<String> favoriteIds) {
        return composeDay(focus, phasePrescription, safePool, targetCount, recentIds, favoriteIds,
                null);
    }

    /**
     * @param slotPreferences 槽位 key → 按优先级排好的动作 id（例如 AI 给的推荐顺序）。
     *                        只是排序偏好：安全过滤、跨天去重仍然在这里强制执行，
     *                        偏好里没有可用的就退回本地评分。
     */
    public static ComposedDay composeDay(ProgramFocus focus, Prescription phasePrescription,
            List<Exercise> safePool, int targetCount,
            List<String> recentIds, Set<String> favoriteIds,
            Map<String, List<String>> slotPreferences) {
        List<Slot> slots = slotsFor(focus, Math.max(1, targetCount));
        List<WorkoutItem> items = new ArrayList<WorkoutItem>();
        List<String> slotKeys = new ArrayList<String>();
        List<String> notes = new ArrayList<String>();
        Set<String> used = new LinkedHashSet<String>();

        for (Slot slot : slots) {
            Exercise picked = preferred(slot, safePool, used, recentIds,
                    slotPreferences == null ? null : slotPreferences.get(slot.key()));
            if (picked == null) {
                picked = bestFor(slot, focus, safePool, used, recentIds, favoriteIds);
            }
            if (picked == null) {
                notes.add("没有找到匹配「" + slot.label() + "」且器械/伤痛允许的动作，本次跳过这个槽位。");
                continue;
            }
            used.add(picked.id());
            items.add(toItem(picked, phasePrescription, favoriteIds, slot));
            slotKeys.add(slot.key());
        }
        return new ComposedDay(items, slotKeys, notes);
    }

    /** 某个槽位的可选动作（供 UI 让用户自己挑替换）。按同样的排序规则，最多返回 limit 个。 */
    public static List<Exercise> candidatesFor(Slot slot, ProgramFocus focus,
            List<Exercise> safePool, Set<String> excludeIds,
            List<String> recentIds, Set<String> favoriteIds, int limit) {
        List<Exercise> matched = new ArrayList<Exercise>();
        for (Exercise exercise : safePool) {
            if (excludeIds.contains(exercise.id())) {
                continue;
            }
            if (slot.matches(exercise)) {
                matched.add(exercise);
            }
        }
        if (matched.isEmpty()) {
            for (Exercise exercise : safePool) {
                if (!excludeIds.contains(exercise.id()) && sharesRegion(exercise, focus)) {
                    matched.add(exercise);
                }
            }
        }
        sortByScore(matched, focus, recentIds, favoriteIds);
        return matched.size() > limit ? new ArrayList<Exercise>(matched.subList(0, limit)) : matched;
    }

    /** 把选定的动作套上阶段处方（等长/单侧由 {@link ExerciseTempo} 修正）。 */
    public static WorkoutItem toItem(Exercise exercise, Prescription phasePrescription,
            Set<String> favoriteIds, Slot slot) {
        Prescription prescription = ExerciseTempo.effective(exercise, phasePrescription);
        boolean favorite = favoriteIds != null && favoriteIds.contains(exercise.id());
        String reason = slot == null
                ? "计划课动作"
                : "填「" + slot.label() + "」槽位";
        return new WorkoutItem(exercise, prescription, favorite, reason);
    }

    /**
     * 按外部给的优先顺序挑：先要没用过、也不是最近练过的；实在都练过就退而求其次取第一个可用的。
     * 不在安全候选里的 id 一律忽略——AI 也不能往里塞过滤掉的动作。
     */
    private static Exercise preferred(Slot slot, List<Exercise> safePool, Set<String> used,
            List<String> recentIds, List<String> preferences) {
        if (preferences == null || preferences.isEmpty()) {
            return null;
        }
        Exercise fallback = null;
        for (String id : preferences) {
            if (used.contains(id)) {
                continue;
            }
            for (Exercise exercise : safePool) {
                if (!exercise.id().equals(id) || !slot.matches(exercise)) {
                    continue;
                }
                if (freshnessPenalty(id, recentIds) == 0) {
                    return exercise;
                }
                if (fallback == null) {
                    fallback = exercise;
                }
                break;
            }
        }
        return fallback;
    }

    private static Exercise bestFor(Slot slot, ProgramFocus focus, List<Exercise> safePool,
            Set<String> used, List<String> recentIds, Set<String> favoriteIds) {
        List<Exercise> matched = new ArrayList<Exercise>();
        for (Exercise exercise : safePool) {
            if (!used.contains(exercise.id()) && slot.matches(exercise)) {
                matched.add(exercise);
            }
        }
        if (matched.isEmpty()) {
            // 模式没有候选时退到部位，至少保证这一天的目标肌群被练到。
            for (Exercise exercise : safePool) {
                if (!used.contains(exercise.id()) && sharesRegion(exercise, focus)) {
                    matched.add(exercise);
                }
            }
        }
        if (matched.isEmpty()) {
            return null;
        }
        sortByScore(matched, focus, recentIds, favoriteIds);
        return matched.get(0);
    }

    private static void sortByScore(List<Exercise> candidates, final ProgramFocus focus,
            final List<String> recentIds, final Set<String> favoriteIds) {
        Collections.sort(candidates, new Comparator<Exercise>() {
            @Override
            public int compare(Exercise left, Exercise right) {
                int diff = score(right, focus, recentIds, favoriteIds)
                        - score(left, focus, recentIds, favoriteIds);
                return diff != 0 ? diff : left.id().compareTo(right.id());
            }
        });
    }

    private static int score(Exercise exercise, ProgramFocus focus,
            List<String> recentIds, Set<String> favoriteIds) {
        int score = 0;
        if (sharesRegion(exercise, focus)) {
            score += SCORE_REGION_MATCH;
        }
        if (exercise.evidenceStatus() == EvidenceStatus.GUIDELINE_BACKED) {
            score += SCORE_GUIDELINE_BACKED;
        }
        if (favoriteIds != null && favoriteIds.contains(exercise.id())) {
            score += SCORE_FAVORITE;
        }
        if (exercise.difficulty().contains("beginner")) {
            score += SCORE_BEGINNER;
        }
        score -= freshnessPenalty(exercise.id(), recentIds);
        return score;
    }

    /** 最近练过就降权：越靠近现在扣得越多，超出窗口不扣。 */
    private static int freshnessPenalty(String id, List<String> recentIds) {
        if (recentIds == null) {
            return 0;
        }
        int index = recentIds.indexOf(id);
        if (index < 0) {
            return 0;
        }
        return Math.max(0, FRESHNESS_PENALTY_BASE - index * FRESHNESS_PENALTY_STEP);
    }

    private static boolean sharesRegion(Exercise exercise, ProgramFocus focus) {
        for (String region : focus.regions()) {
            if (exercise.targetRegions().contains(region)) {
                return true;
            }
        }
        return false;
    }
}
