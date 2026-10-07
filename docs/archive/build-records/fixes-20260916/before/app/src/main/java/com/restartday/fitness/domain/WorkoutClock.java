package com.restartday.fitness.domain;

/** Monotonic active time. Pauses and time spent outside the app never complete a set. */
public final class WorkoutClock {
    private long accumulated;
    private long anchor;
    private long phaseStart;
    private long phaseDuration;
    private boolean paused = true;

    public void start(long now) {
        accumulated = 0;
        phaseStart = 0;
        phaseDuration = 0;
        anchor = now;
        paused = false;
    }

    public long elapsed(long now) {
        return accumulated + (paused ? 0 : Math.max(0, now - anchor));
    }

    public void pause(long now) {
        accumulated = elapsed(now);
        paused = true;
    }

    public void resume(long now) {
        if (!paused) return;
        anchor = now;
        paused = false;
    }

    public boolean isPaused() { return paused; }

    public void beginPhase(long durationMillis, long now) {
        phaseStart = elapsed(now);
        phaseDuration = Math.max(0, durationMillis);
    }

    public long phaseElapsed(long now) { return Math.max(0, elapsed(now) - phaseStart); }
    public long remaining(long now) { return Math.max(0, phaseDuration - phaseElapsed(now)); }
    public long phaseDuration() { return phaseDuration; }
    public long phaseStart() { return phaseStart; }
    public void extendPhase(long millis) { phaseDuration += Math.max(0, millis); }

    /** Stored durations survive process death and reboot; never persist uptime deadlines. */
    public void restore(long elapsedMillis, long phaseStartMillis, long durationMillis) {
        accumulated = Math.max(0, elapsedMillis);
        phaseStart = Math.max(0, Math.min(accumulated, phaseStartMillis));
        phaseDuration = Math.max(0, durationMillis);
        paused = true;
    }
}
