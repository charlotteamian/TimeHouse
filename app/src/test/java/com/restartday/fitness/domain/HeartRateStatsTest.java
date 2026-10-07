package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.List;

public final class HeartRateStatsTest {
    public static void main(String[] args) {
        HeartRateStatsTest test = new HeartRateStatsTest();
        test.samplesOutsideTheSessionAreIgnored();
        test.averageIsTimeWeightedNotSampleCounted();
        test.backgroundSpotReadingsAreRejectedAsUnreliable();
        test.denseWorkoutSeriesIsAccepted();
        test.aLongGapCannotDominateTheAverage();
        test.emptyInputIsEmptyNotZeroBpm();
        System.out.println("HeartRateStatsTest: all tests passed");
    }

    private static final long START = 1_800_000_000_000L;
    private static final long ELEVEN_MINUTES = 11 * 60 * 1000L;

    /**
     * 这是"平均 73 / 最低 64"的直接来源：旧代码窗口两端各多算 2 分钟，
     * 把热身前和结束后的静息心率算进了训练指标。
     */
    private void samplesOutsideTheSessionAreIgnored() {
        List<HeartRateStats.Sample> samples = new ArrayList<HeartRateStats.Sample>();
        samples.add(new HeartRateStats.Sample(START - 60_000, 62));   // 开练前的静息
        samples.add(new HeartRateStats.Sample(START + 60_000, 110));
        samples.add(new HeartRateStats.Sample(START + 120_000, 112));
        samples.add(new HeartRateStats.Sample(START + ELEVEN_MINUTES + 60_000, 66)); // 结束后

        HeartRateStats stats = HeartRateStats.of(samples, START, START + ELEVEN_MINUTES);
        assertEquals(2, stats.sampleCount(), "窗口外的样本必须被丢掉");
        assertEquals(110, stats.min(), "最低心率只能来自训练窗口内");
        assertEquals(112, stats.max(), "最高心率");
    }

    /** 手表给的是时间加权平均；样本算术平均会被密集采样段带偏。 */
    private void averageIsTimeWeightedNotSampleCounted() {
        List<HeartRateStats.Sample> samples = new ArrayList<HeartRateStats.Sample>();
        // 前 20 秒密集 5 个 150，之后一个 100 一直持续到结束。
        for (int i = 0; i < 5; i++) {
            samples.add(new HeartRateStats.Sample(START + i * 5_000L, 150));
        }
        samples.add(new HeartRateStats.Sample(START + 25_000, 100));
        long end = START + 120_000;

        HeartRateStats stats = HeartRateStats.of(samples, START, end);
        // 算术平均会是 (150×5 + 100)/6 ≈ 142；时间加权后 100 占的时间更长，应该明显低于它。
        assertTrue(stats.average() < 130,
                "时间加权平均应该压低短暂高值的权重，实际 " + stats.average());
        assertTrue(stats.average() > 100, "但仍高于最低值，实际 " + stats.average());
    }

    /**
     * 结束瞬间去读健康连接，拿到的是后台被动抽样（几分钟一个点的静息值）。
     * 这种读数必须判为不可靠、继续重试，而不是当成这次训练的心率写死。
     */
    private void backgroundSpotReadingsAreRejectedAsUnreliable() {
        List<HeartRateStats.Sample> samples = new ArrayList<HeartRateStats.Sample>();
        samples.add(new HeartRateStats.Sample(START + 30_000, 64));
        samples.add(new HeartRateStats.Sample(START + 5 * 60_000L, 73));
        samples.add(new HeartRateStats.Sample(START + 9 * 60_000L, 88));

        HeartRateStats stats = HeartRateStats.of(samples, START, START + ELEVEN_MINUTES);
        assertTrue(!stats.isEmpty(), "确实读到了样本");
        assertTrue(!stats.isReliable(), "3 个点撑 11 分钟应判为不可靠（后台抽样，不是运动心率）");
        assertTrue(stats.coverage() < HeartRateStats.MIN_COVERAGE, "覆盖率应低于门槛");
    }

    /** 手表同步完成后的运动心率序列：几秒一个点，应该被接受。 */
    private void denseWorkoutSeriesIsAccepted() {
        List<HeartRateStats.Sample> samples = new ArrayList<HeartRateStats.Sample>();
        for (long at = 0; at < ELEVEN_MINUTES; at += 10_000L) {
            samples.add(new HeartRateStats.Sample(START + at, 78 + (int) ((at / 10_000L) % 30)));
        }
        HeartRateStats stats = HeartRateStats.of(samples, START, START + ELEVEN_MINUTES);
        assertTrue(stats.isReliable(), "10 秒一个点的序列应判为可靠");
        assertTrue(stats.coverage() >= 0.9, "覆盖率应接近 100%，实际 " + stats.coverage());
        assertContains(stats.coverageLabel(), "覆盖");
    }

    /** 中间断了 5 分钟时，最后一个样本不能被当成 5 分钟的恒定心率。 */
    private void aLongGapCannotDominateTheAverage() {
        List<HeartRateStats.Sample> samples = new ArrayList<HeartRateStats.Sample>();
        samples.add(new HeartRateStats.Sample(START, 180));
        samples.add(new HeartRateStats.Sample(START + 10 * 60_000L, 60));

        HeartRateStats stats = HeartRateStats.of(samples, START, START + ELEVEN_MINUTES);
        // 两个样本各自最多代表 30 秒，所以平均应该接近两者的中点，而不是被 180 拉满。
        assertTrue(stats.average() > 100 && stats.average() < 140,
                "单个样本的权重要被上限夹住，实际 " + stats.average());
    }

    private void emptyInputIsEmptyNotZeroBpm() {
        HeartRateStats stats = HeartRateStats.of(new ArrayList<HeartRateStats.Sample>(),
                START, START + ELEVEN_MINUTES);
        assertTrue(stats.isEmpty(), "没有样本就是空");
        assertTrue(!stats.isReliable(), "空结果不可靠");
        assertEquals(0, stats.average(), "空结果不该给出心率值");
    }

    private static void assertContains(String actual, String part) {
        assertTrue(actual.contains(part), "Expected [" + actual + "] to contain [" + part + "]");
    }

    private static void assertEquals(Object expected, Object actual, String message) {
        if (!expected.equals(actual)) {
            throw new AssertionError(message + "\nExpected: " + expected + "\nActual: " + actual);
        }
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
