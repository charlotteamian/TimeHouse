package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/**
 * 从健康连接读回来的心率样本算这次训练的心率指标。
 *
 * <p>之前对不上手表的原因有三个都在这里：统计窗口两端各多算了 2 分钟静息心率、
 * 平均用的是样本算术平均（手表给的是时间加权平均）、以及"读到几个点就当成结果写死"——
 * 手表配套 App 还没同步时，库里只有每几分钟一次的后台抽样，那是静息值不是运动值。
 *
 * <p>所以这里：只统计训练窗口内的样本、按时间加权、并且给出可靠性判定，
 * 不合格的读数不该被当成正式结果。
 */
public final class HeartRateStats {

    /** 训练分钟里至少要有这么高比例有样本，才算覆盖完整。 */
    public static final double MIN_COVERAGE = 0.6;

    /** 运动中的手表通常每几秒一个点；低于 2 点/分钟基本可以断定是后台抽样。 */
    public static final double MIN_SAMPLES_PER_MINUTE = 2.0;

    /** 时间加权时单个样本最多代表 30 秒，避免一个长空档被当成一段恒定心率。 */
    public static final long MAX_WEIGHT_SECONDS = 30;

    private final int average;
    private final int max;
    private final int min;
    private final int sampleCount;
    private final double coverage;
    private final boolean reliable;

    private HeartRateStats(int average, int max, int min, int sampleCount,
            double coverage, boolean reliable) {
        this.average = average;
        this.max = max;
        this.min = min;
        this.sampleCount = sampleCount;
        this.coverage = coverage;
        this.reliable = reliable;
    }

    /** 一个心率样本。 */
    public static final class Sample {
        private final long timeMillis;
        private final int bpm;

        public Sample(long timeMillis, int bpm) {
            this.timeMillis = timeMillis;
            this.bpm = bpm;
        }

        public long timeMillis() {
            return timeMillis;
        }

        public int bpm() {
            return bpm;
        }
    }

    /**
     * @param samples 任意顺序的样本，窗口外的会被丢掉
     * @param startMs 训练真正开始的时刻
     * @param endMs   训练结束的时刻
     */
    public static HeartRateStats of(List<Sample> samples, long startMs, long endMs) {
        List<Sample> inWindow = withinWindow(samples, startMs, endMs);
        if (inWindow.isEmpty()) {
            return new HeartRateStats(0, 0, 0, 0, 0, false);
        }
        Collections.sort(inWindow, new Comparator<Sample>() {
            @Override
            public int compare(Sample left, Sample right) {
                return Long.compare(left.timeMillis(), right.timeMillis());
            }
        });

        double weightedSum = 0;
        double weightTotal = 0;
        int max = Integer.MIN_VALUE;
        int min = Integer.MAX_VALUE;
        for (int i = 0; i < inWindow.size(); i++) {
            Sample sample = inWindow.get(i);
            long nextAt = i + 1 < inWindow.size() ? inWindow.get(i + 1).timeMillis() : endMs;
            long weight = Math.max(1000L, Math.min(MAX_WEIGHT_SECONDS * 1000L,
                    nextAt - sample.timeMillis()));
            weightedSum += (double) sample.bpm() * weight;
            weightTotal += weight;
            max = Math.max(max, sample.bpm());
            min = Math.min(min, sample.bpm());
        }

        double minutes = Math.max(1.0, (endMs - startMs) / 60000.0);
        double coverage = coverage(inWindow, startMs, endMs);
        boolean reliable = coverage >= MIN_COVERAGE
                && inWindow.size() / minutes >= MIN_SAMPLES_PER_MINUTE;
        int average = weightTotal > 0 ? (int) Math.round(weightedSum / weightTotal) : 0;
        return new HeartRateStats(average, max, min, inWindow.size(), coverage, reliable);
    }

    /** 时间加权平均心率。 */
    public int average() {
        return average;
    }

    public int max() {
        return max == Integer.MIN_VALUE ? 0 : max;
    }

    public int min() {
        return min == Integer.MAX_VALUE ? 0 : min;
    }

    public int sampleCount() {
        return sampleCount;
    }

    /** 训练分钟里有心率样本的比例。 */
    public double coverage() {
        return coverage;
    }

    /**
     * 采样够密、覆盖够全，才算这次训练真正的心率。
     * 不可靠时应该保留重试，而不是把后台抽样冒充成运动心率。
     */
    public boolean isReliable() {
        return reliable;
    }

    public boolean isEmpty() {
        return sampleCount == 0;
    }

    public String coverageLabel() {
        return sampleCount + " 个采样点 · 覆盖 " + Math.round(coverage * 100) + "%";
    }

    private static List<Sample> withinWindow(List<Sample> samples, long startMs, long endMs) {
        List<Sample> result = new ArrayList<Sample>();
        if (samples == null || endMs <= startMs) {
            return result;
        }
        for (Sample sample : samples) {
            if (sample == null || sample.bpm() <= 0) {
                continue;
            }
            if (sample.timeMillis() >= startMs && sample.timeMillis() <= endMs) {
                result.add(sample);
            }
        }
        return result;
    }

    /** 有样本的分钟数 / 训练总分钟数。 */
    private static double coverage(List<Sample> samples, long startMs, long endMs) {
        long totalMinutes = Math.max(1, (endMs - startMs) / 60000);
        Set<Long> covered = new LinkedHashSet<Long>();
        for (Sample sample : samples) {
            covered.add((sample.timeMillis() - startMs) / 60000);
        }
        return Math.min(1.0, covered.size() / (double) totalMinutes);
    }
}
