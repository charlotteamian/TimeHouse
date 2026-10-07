package com.restartday.fitness.domain;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * 一次训练课的部位分工（分化模板）。regions/patterns 与动作库标签一致，
 * 生成当日训练时直接喂给 RecommendationEngine，安全过滤逻辑完全复用。
 */
public enum ProgramFocus {
    FULL_A("全身 A", Arrays.asList("腿", "臀", "胸", "背", "核心"),
            Arrays.asList("蹲", "推", "拉", "抗伸展")),
    FULL_B("全身 B", Arrays.asList("腿", "臀", "胸", "肩", "背", "核心"),
            Arrays.asList("髋铰链", "推", "拉", "稳定")),
    FULL_C("全身 C", Arrays.asList("腿", "臀", "胸", "背", "核心"),
            Arrays.asList("单腿", "推", "拉", "髋铰链", "抗旋转")),
    PUSH("推（胸肩三头）", Arrays.asList("胸", "肩", "手臂"),
            Arrays.asList("推")),
    PULL("拉（背二头）", Arrays.asList("背", "手臂"),
            Arrays.asList("拉")),
    LEGS("腿（下肢臀）", Arrays.asList("腿", "臀", "核心"),
            Arrays.asList("蹲", "髋铰链", "单腿")),
    UPPER("上肢", Arrays.asList("胸", "背", "肩", "手臂"),
            Arrays.asList("推", "拉")),
    LOWER("下肢", Arrays.asList("腿", "臀", "核心"),
            Arrays.asList("蹲", "髋铰链", "单腿", "抗伸展")),
    CARDIO_CORE("有氧 + 核心", Arrays.asList("有氧", "核心"),
            Arrays.asList("有氧", "核心", "稳定"));

    private final String label;
    private final List<String> regions;
    private final List<String> patterns;

    ProgramFocus(String label, List<String> regions, List<String> patterns) {
        this.label = label;
        this.regions = Collections.unmodifiableList(regions);
        this.patterns = Collections.unmodifiableList(patterns);
    }

    public String label() {
        return label;
    }

    public List<String> regions() {
        return regions;
    }

    public List<String> patterns() {
        return patterns;
    }

    /** 供生成当日训练时拼给推荐引擎的意图文本。 */
    public String intentText() {
        StringBuilder builder = new StringBuilder();
        for (String region : regions) {
            builder.append(region);
        }
        return builder.toString();
    }

    public static ProgramFocus parse(String name, ProgramFocus fallback) {
        for (ProgramFocus focus : values()) {
            if (focus.name().equals(name)) {
                return focus;
            }
        }
        return fallback;
    }
}
