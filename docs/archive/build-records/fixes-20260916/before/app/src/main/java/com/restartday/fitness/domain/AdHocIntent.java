package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * 临时加练的一句话意图。
 *
 * <p>比 {@link RecommendationEngine} 里那个只做关键词 contains 的解析多三样东西，
 * 都是加练场景最常见的说法：
 * <ul>
 *   <li>否定——"不要练腿"、"除了腿"、"腿不练"；</li>
 *   <li>时间——"15 分钟"、"半小时"、"二十分钟"；</li>
 *   <li>目的——"想出汗"走循环，"腰有点僵/今天很累"走恢复。</li>
 * </ul>
 */
public final class AdHocIntent {

    public enum Mode {
        /** 常规抗阻：正常组间休息。 */
        STRENGTH,
        /** 想出汗/心肺：短休息、循环密度。 */
        CONDITIONING,
        /** 酸、僵、累：低强度活动开。 */
        RECOVERY
    }

    /** 部位关键词 → 目标部位。腿会带上臀，因为下肢动作基本都同时练到。 */
    private static final Map<String, List<String>> REGION_KEYWORDS = regionKeywords();

    private static final String[] NEGATIONS = {"不要", "不想", "别", "不练", "避开", "跳过", "除了", "不做"};
    private static final String[] RECOVERY_WORDS = {
            "恢复", "放松", "拉伸", "酸", "僵", "很累", "太累", "疲", "缓解", "活动开", "松一松", "轻一点"};
    private static final String[] CONDITIONING_WORDS = {
            "出汗", "流汗", "心肺", "有氧", "燃脂", "减脂", "喘", "热身一下", "动起来"};
    private static final String[] SINGLE_WORDS = {"一个动作", "只练一个", "单个动作", "只做一个"};

    private final List<String> regions;
    private final List<String> excludedRegions;
    private final int minutes;
    private final Mode mode;
    private final boolean singleMovement;

    private AdHocIntent(List<String> regions, List<String> excludedRegions, int minutes,
            Mode mode, boolean singleMovement) {
        this.regions = Collections.unmodifiableList(regions);
        this.excludedRegions = Collections.unmodifiableList(excludedRegions);
        this.minutes = minutes;
        this.mode = mode;
        this.singleMovement = singleMovement;
    }

    public static AdHocIntent parse(String rawText) {
        String text = rawText == null ? "" : rawText;
        Set<String> wanted = new LinkedHashSet<String>();
        Set<String> excluded = new LinkedHashSet<String>();

        for (Map.Entry<String, List<String>> entry : REGION_KEYWORDS.entrySet()) {
            String keyword = entry.getKey();
            int at = text.indexOf(keyword);
            while (at >= 0) {
                if (isNegated(text, at)) {
                    excluded.addAll(entry.getValue());
                } else {
                    wanted.addAll(entry.getValue());
                }
                at = text.indexOf(keyword, at + keyword.length());
            }
        }
        // 同时被点名和被否定时以否定为准：说"练上肢但不要练肩"，肩不该进来。
        wanted.removeAll(excluded);

        Mode mode = Mode.STRENGTH;
        if (containsAny(text, RECOVERY_WORDS)) {
            mode = Mode.RECOVERY;
        } else if (containsAny(text, CONDITIONING_WORDS)) {
            mode = Mode.CONDITIONING;
        }

        return new AdHocIntent(new ArrayList<String>(wanted), new ArrayList<String>(excluded),
                parseMinutes(text), mode, containsAny(text, SINGLE_WORDS));
    }

    /** 用户点名要练的部位；空表示没指定，由加练规划器按恢复状态和周容量决定。 */
    public List<String> regions() {
        return regions;
    }

    /** 明确不要练的部位。 */
    public List<String> excludedRegions() {
        return excludedRegions;
    }

    /** 从话里读出来的分钟数；0 表示没说，用界面上选的。 */
    public int minutes() {
        return minutes;
    }

    public Mode mode() {
        return mode;
    }

    public boolean singleMovement() {
        return singleMovement;
    }

    public boolean hasTarget() {
        return !regions.isEmpty();
    }

    /**
     * 关键词是不是被否定了。
     * 只看紧挨着前面的 4 个字，以及"腿不练"这种否定词收尾的情况——
     * 更远的窗口会把"练腿不练背"里的腿也误判成否定。
     */
    private static boolean isNegated(String text, int keywordAt) {
        String before = text.substring(Math.max(0, keywordAt - 4), keywordAt);
        for (String negation : NEGATIONS) {
            if (before.contains(negation)) {
                return true;
            }
        }
        String after = text.substring(Math.min(text.length(), keywordAt + 1));
        for (String negation : NEGATIONS) {
            // "腿不练" —— 否定词在句尾，后面没有别的部位可以承接这个否定。
            if (after.startsWith(negation) && !containsAnyRegion(after.substring(negation.length()))) {
                return true;
            }
        }
        return false;
    }

    private static boolean containsAnyRegion(String text) {
        for (String keyword : REGION_KEYWORDS.keySet()) {
            if (text.contains(keyword)) {
                return true;
            }
        }
        return false;
    }

    private static boolean containsAny(String text, String[] words) {
        for (String word : words) {
            if (text.contains(word)) {
                return true;
            }
        }
        return false;
    }

    /** 支持 "15分钟"、"15分"、"半小时"、"一小时"、"二十分钟"。取不到返回 0。 */
    static int parseMinutes(String text) {
        if (text.contains("半小时")) {
            return 30;
        }
        if (text.contains("一刻钟")) {
            return 15;
        }
        int hourAt = indexOfAny(text, "小时", "个小时");
        if (hourAt > 0) {
            int hours = numberEndingAt(text, hourAt);
            if (hours > 0) {
                return Math.min(180, hours * 60);
            }
        }
        int minuteAt = indexOfAny(text, "分钟", "分");
        if (minuteAt > 0) {
            int minutes = numberEndingAt(text, minuteAt);
            if (minutes > 0) {
                return Math.min(180, minutes);
            }
        }
        return 0;
    }

    private static int indexOfAny(String text, String... needles) {
        for (String needle : needles) {
            int at = text.indexOf(needle);
            if (at >= 0) {
                return at;
            }
        }
        return -1;
    }

    /** 读出紧挨在 {@code endExclusive} 前面的数字，阿拉伯数字和中文数字都认。 */
    private static int numberEndingAt(String text, int endExclusive) {
        int start = endExclusive;
        while (start > 0 && isNumberChar(text.charAt(start - 1))) {
            start--;
        }
        if (start == endExclusive) {
            return 0;
        }
        String token = text.substring(start, endExclusive);
        try {
            return Integer.parseInt(token);
        } catch (NumberFormatException ignored) {
            return chineseNumber(token);
        }
    }

    private static boolean isNumberChar(char value) {
        return Character.isDigit(value) || "零一二两三四五六七八九十".indexOf(value) >= 0;
    }

    /** 中文数字 1-99：十、十五、二十、二十五…… */
    static int chineseNumber(String token) {
        final String digits = "零一二三四五六七八九";
        int tenAt = token.indexOf('十');
        if (tenAt < 0) {
            int value = digits.indexOf(token.charAt(0));
            if (value < 0 && token.charAt(0) == '两') {
                return 2;
            }
            return Math.max(0, value);
        }
        int tens = 1;
        if (tenAt > 0) {
            char high = token.charAt(tenAt - 1);
            tens = high == '两' ? 2 : Math.max(0, digits.indexOf(high));
        }
        int ones = 0;
        if (tenAt + 1 < token.length()) {
            char low = token.charAt(tenAt + 1);
            ones = low == '两' ? 2 : Math.max(0, digits.indexOf(low));
        }
        return tens * 10 + ones;
    }

    private static Map<String, List<String>> regionKeywords() {
        Map<String, List<String>> map = new LinkedHashMap<String, List<String>>();
        // 长关键词排在前面，避免 "上肢" 被 "肢" 之类的短词抢先匹配。
        map.put("上肢", Arrays.asList("胸", "背", "肩", "手臂"));
        map.put("下肢", Arrays.asList("腿", "臀"));
        map.put("胳膊", Arrays.asList("手臂"));
        map.put("手臂", Arrays.asList("手臂"));
        map.put("二头", Arrays.asList("手臂"));
        map.put("三头", Arrays.asList("手臂"));
        map.put("核心", Arrays.asList("核心"));
        map.put("腹肌", Arrays.asList("核心"));
        map.put("腹", Arrays.asList("核心"));
        map.put("背", Arrays.asList("背"));
        map.put("胸", Arrays.asList("胸"));
        map.put("腿", Arrays.asList("腿", "臀"));
        map.put("臀", Arrays.asList("臀"));
        map.put("屁股", Arrays.asList("臀"));
        map.put("肩", Arrays.asList("肩"));
        map.put("有氧", Arrays.asList("有氧"));
        map.put("心肺", Arrays.asList("有氧"));
        return Collections.unmodifiableMap(map);
    }
}
