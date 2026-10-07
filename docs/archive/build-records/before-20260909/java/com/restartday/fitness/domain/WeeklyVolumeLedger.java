package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 每个肌群本周做了多少组——计划课和临时加练一起记。
 *
 * <p>这是把「有计划的健身」和「临时加练」连起来的那个机制：加练也是训练量，
 * 不记账的话，加练要么白练（练的是明天要练的部位），要么把周总量顶爆。
 *
 * <p>组数折算按 Schoenfeld 的直接组/间接组惯例：动作的主要部位记 1 组，
 * 其余目标部位各记 0.5 组。剂量区间见 {@link GuidelineRefs#VOLUME_DOSE_RESPONSE}。
 */
public final class WeeklyVolumeLedger {

    /** 只统计抗阻训练的部位；有氧和自定义分类不进容量账。 */
    public static final List<String> RESISTANCE_REGIONS = Collections.unmodifiableList(
            Arrays.asList("胸", "背", "腿", "臀", "肩", "手臂", "核心"));

    /** 间接参与的部位按半组计。 */
    private static final double SECONDARY_WEIGHT = 0.5;

    public enum Status {
        /** 低于建议下限，刺激可能不够。 */
        LOW,
        /** 在建议区间内。 */
        OK,
        /** 超过建议上限，收益递减且更吃恢复。 */
        HIGH
    }

    /** 一个肌群的本周账目。 */
    public static final class Entry {
        private final String region;
        private final double sets;
        private final int min;
        private final int max;

        Entry(String region, double sets, int min, int max) {
            this.region = region;
            this.sets = sets;
            this.min = min;
            this.max = max;
        }

        public String region() {
            return region;
        }

        /** 本周已完成的折算组数。 */
        public double sets() {
            return sets;
        }

        public int min() {
            return min;
        }

        public int max() {
            return max;
        }

        public Status status() {
            if (sets > max) {
                return Status.HIGH;
            }
            return sets < min ? Status.LOW : Status.OK;
        }

        /** 还能再练几组才到上限；已经超了返回 0。 */
        public double roomToCeiling() {
            return Math.max(0, max - sets);
        }

        public String label() {
            String rounded = sets == Math.rint(sets)
                    ? String.valueOf((int) sets)
                    : String.valueOf(Math.round(sets * 10) / 10.0);
            return region + " " + rounded + " 组（建议 " + min + "-" + max + "）";
        }
    }

    private final Map<String, Entry> entries;

    private WeeklyVolumeLedger(Map<String, Entry> entries) {
        this.entries = Collections.unmodifiableMap(entries);
    }

    /**
     * @param loads     本周内已完成的训练量
     * @param level     训练水平，决定建议区间
     * @param weekStart 本周起始时刻（毫秒），早于它的记录不计入
     */
    public static WeeklyVolumeLedger of(List<TrainingLoad> loads, TrainingLevel level,
            long weekStart) {
        Map<String, Double> totals = new LinkedHashMap<String, Double>();
        for (String region : RESISTANCE_REGIONS) {
            totals.put(region, 0.0);
        }
        if (loads != null) {
            for (TrainingLoad load : loads) {
                if (load == null || load.atMillis() < weekStart || load.sets() <= 0) {
                    continue;
                }
                for (int i = 0; i < load.regions().size(); i++) {
                    String region = load.regions().get(i);
                    if (!totals.containsKey(region)) {
                        continue;
                    }
                    double weight = i == 0 ? 1.0 : SECONDARY_WEIGHT;
                    totals.put(region, totals.get(region) + load.sets() * weight);
                }
            }
        }
        int min = minSetsFor(level);
        int max = maxSetsFor(level);
        Map<String, Entry> entries = new LinkedHashMap<String, Entry>();
        for (Map.Entry<String, Double> total : totals.entrySet()) {
            entries.put(total.getKey(), new Entry(total.getKey(), total.getValue(), min, max));
        }
        return new WeeklyVolumeLedger(entries);
    }

    public List<Entry> entries() {
        return new ArrayList<Entry>(entries.values());
    }

    public Entry forRegion(String region) {
        return entries.get(region);
    }

    /** 已经超过建议上限的肌群。 */
    public List<Entry> overloaded() {
        List<Entry> result = new ArrayList<Entry>();
        for (Entry entry : entries.values()) {
            if (entry.status() == Status.HIGH) {
                result.add(entry);
            }
        }
        return result;
    }

    /** 本周还欠刺激的肌群——加练时优先补这些。 */
    public List<Entry> underworked() {
        List<Entry> result = new ArrayList<Entry>();
        for (Entry entry : entries.values()) {
            if (entry.status() == Status.LOW) {
                result.add(entry);
            }
        }
        return result;
    }

    /**
     * 这套加练会把哪些肌群顶过上限。返回的是提示文本，空表示没问题。
     *
     * @param plannedSets 这次打算练的：部位 → 组数（已按主/次折算前的原始组数）
     */
    public List<String> warningsFor(List<TrainingLoad> plannedSets) {
        List<String> warnings = new ArrayList<String>();
        if (plannedSets == null || plannedSets.isEmpty()) {
            return warnings;
        }
        Map<String, Double> added = new LinkedHashMap<String, Double>();
        for (TrainingLoad load : plannedSets) {
            for (int i = 0; i < load.regions().size(); i++) {
                String region = load.regions().get(i);
                if (!entries.containsKey(region)) {
                    continue;
                }
                double weight = i == 0 ? 1.0 : SECONDARY_WEIGHT;
                Double prior = added.get(region);
                added.put(region, (prior == null ? 0 : prior) + load.sets() * weight);
            }
        }
        for (Map.Entry<String, Double> item : added.entrySet()) {
            Entry entry = entries.get(item.getKey());
            double after = entry.sets() + item.getValue();
            if (after > entry.max()) {
                warnings.add(item.getKey() + "本周会到 " + Math.round(after) + " 组，超过建议上限 "
                        + entry.max() + " 组：收益递减而且更吃恢复，下次计划课可以少做 1-2 组。");
            }
        }
        return warnings;
    }

    /** 初级先把频率和动作质量做稳，量不用堆。 */
    private static int minSetsFor(TrainingLevel level) {
        switch (level) {
            case ADVANCED:
                return 12;
            case INTERMEDIATE:
                return 10;
            default:
                return 6;
        }
    }

    private static int maxSetsFor(TrainingLevel level) {
        switch (level) {
            case ADVANCED:
                return 24;
            case INTERMEDIATE:
                return 20;
            default:
                return 14;
        }
    }
}
