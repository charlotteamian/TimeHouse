package com.restartday.fitness.domain;

/**
 * 一个动作的训练处方。
 *
 * <p>除了展示用的 {@code reps} 字符串，还解析出结构化的次数区间 / 保持秒数 / 单侧标记，
 * 这样 {@link SessionTimeModel} 才能正向算出这套处方真正需要多少时间——
 * 以前 reps 只是字符串，时长完全没法核算，UI 上的"预计 40 分钟"就是个没验算过的标签。
 */
public final class Prescription {

    /** 默认节奏：1 秒向心 + 2 秒离心。ACSM 对初学者建议的可控节奏。 */
    public static final double DEFAULT_SECONDS_PER_REP = 3.0;

    /** 次数区间无法解析时的兜底中位数。 */
    private static final int FALLBACK_MID_REPS = 10;

    public enum Kind {
        /** 计次动作：按次数 × 节奏估时。 */
        REPS,
        /** 计时（等长）动作：按保持秒数估时。 */
        HOLD
    }

    private final int sets;
    private final String reps;
    private final String rpe;
    private final int restSeconds;
    private final Kind kind;
    private final int repsLow;
    private final int repsHigh;
    private final int holdSeconds;
    private final boolean perSide;
    private final double secondsPerRep;

    public Prescription(int sets, String reps, String rpe, int restSeconds) {
        this.sets = sets;
        this.reps = reps == null ? "" : reps;
        this.rpe = rpe == null ? "" : rpe.trim();
        this.restSeconds = restSeconds;
        this.kind = Kind.REPS;
        this.holdSeconds = 0;
        this.perSide = containsPerSideMarker(this.reps);
        this.secondsPerRep = DEFAULT_SECONDS_PER_REP;
        int[] range = parseRange(this.reps);
        this.repsLow = range[0];
        this.repsHigh = range[1];
    }

    private Prescription(int sets, String reps, String rpe, int restSeconds, Kind kind,
            int repsLow, int repsHigh, int holdSeconds, boolean perSide, double secondsPerRep) {
        this.sets = sets;
        this.reps = reps == null ? "" : reps;
        this.rpe = rpe == null ? "" : rpe.trim();
        this.restSeconds = restSeconds;
        this.kind = kind;
        this.repsLow = repsLow;
        this.repsHigh = repsHigh;
        this.holdSeconds = holdSeconds;
        this.perSide = perSide;
        this.secondsPerRep = secondsPerRep;
    }

    /** 计时（等长）处方，例如平板支撑保持 30 秒。 */
    public static Prescription hold(int sets, int holdSeconds, String rpe, int restSeconds,
            boolean perSide) {
        String label = holdSeconds + " 秒" + (perSide ? "/侧" : "");
        return new Prescription(sets, label, rpe, restSeconds, Kind.HOLD,
                0, 0, Math.max(5, holdSeconds), perSide, DEFAULT_SECONDS_PER_REP);
    }

    public int sets() {
        return sets;
    }

    public String reps() {
        return reps;
    }

    public String rpe() {
        return rpe;
    }

    public int restSeconds() {
        return restSeconds;
    }

    public Kind kind() {
        return kind;
    }

    public int repsLow() {
        return repsLow;
    }

    public int repsHigh() {
        return repsHigh;
    }

    public int holdSeconds() {
        return holdSeconds;
    }

    /** 单侧动作：一组要左右各做一遍，工作时间翻倍。 */
    public boolean perSide() {
        return perSide;
    }

    public double secondsPerRep() {
        return secondsPerRep;
    }

    /** 次数区间中位数；无法解析时回退到 10。 */
    public double midReps() {
        if (repsLow > 0 && repsHigh > 0) {
            return (repsLow + repsHigh) / 2.0;
        }
        if (repsLow > 0) {
            return repsLow;
        }
        return FALLBACK_MID_REPS;
    }

    /** 一组的净工作秒数（不含组间休息）。 */
    public double workSecondsPerSet() {
        double base = kind == Kind.HOLD ? holdSeconds : midReps() * secondsPerRep;
        return perSide ? base * 2 : base;
    }

    public Prescription withRestSeconds(int seconds) {
        return new Prescription(sets, reps, rpe, Math.max(0, seconds), kind,
                repsLow, repsHigh, holdSeconds, perSide, secondsPerRep);
    }

    public Prescription withSets(int newSets) {
        if (newSets == sets) {
            return this;
        }
        return new Prescription(newSets, reps, rpe, restSeconds, kind,
                repsLow, repsHigh, holdSeconds, perSide, secondsPerRep);
    }

    public Prescription withPerSide(boolean value) {
        if (value == perSide) {
            return this;
        }
        return new Prescription(sets, reps, rpe, restSeconds, kind,
                repsLow, repsHigh, holdSeconds, value, secondsPerRep);
    }

    public Prescription withSecondsPerRep(double value) {
        return new Prescription(sets, reps, rpe, restSeconds, kind,
                repsLow, repsHigh, holdSeconds, perSide, Math.max(1.0, value));
    }

    public String compactLabel() {
        // 单侧标记要显示出来：阶段处方写的是 "10-12"，但死虫这类动作是每侧 10-12 次。
        String repsLabel = perSide && !containsPerSideMarker(reps) ? reps + "/侧" : reps;
        return sets + " x " + repsLabel + (rpe.isEmpty() ? "" : " · RPE " + rpe) + " · 休息 " + restSeconds + " 秒";
    }

    private static boolean containsPerSideMarker(String reps) {
        return reps.contains("/侧") || reps.contains("每侧") || reps.contains("单侧");
    }

    /**
     * 从 "10-12"、"8-12/侧"、"12"、"30 秒" 这类字符串里取出次数区间。
     * 取不到返回 {0, 0}，由 {@link #midReps()} 兜底。
     */
    private static int[] parseRange(String reps) {
        int low = 0;
        int high = 0;
        int index = 0;
        int length = reps.length();
        while (index < length && low == 0) {
            if (Character.isDigit(reps.charAt(index))) {
                int start = index;
                while (index < length && Character.isDigit(reps.charAt(index))) {
                    index++;
                }
                low = parseIntSafe(reps.substring(start, index));
            } else {
                index++;
            }
        }
        // 只有紧跟在分隔符后面的数字才算区间上限，"8-12/侧" 里的 "侧" 不参与。
        if (index < length && (reps.charAt(index) == '-' || reps.charAt(index) == '~')) {
            index++;
            int start = index;
            while (index < length && Character.isDigit(reps.charAt(index))) {
                index++;
            }
            high = parseIntSafe(reps.substring(start, index));
        }
        if (high < low) {
            high = low;
        }
        return new int[]{low, high};
    }

    private static int parseIntSafe(String value) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException ignored) {
            return 0;
        }
    }
}
