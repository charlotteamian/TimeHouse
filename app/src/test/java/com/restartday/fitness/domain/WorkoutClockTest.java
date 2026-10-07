package com.restartday.fitness.domain;

public final class WorkoutClockTest {
    public static void main(String[] args) {
        WorkoutClock c = new WorkoutClock();
        c.start(1000);
        c.beginPhase(30000, 6000);
        c.pause(16000);
        check(c.elapsed(900000) == 15000, "background time must not count");
        check(c.remaining(900000) == 20000, "hold must not finish in background");
        c.pause(900000);
        c.resume(900000);
        c.resume(900500);
        check(c.remaining(905000) == 15000, "resume must preserve countdown");
        c.extendPhase(20000);
        check(c.remaining(905000) == 35000, "rest extension survives pause");
        WorkoutClock restored = new WorkoutClock();
        restored.restore(c.elapsed(905000), c.phaseStart(), c.phaseDuration());
        check(restored.isPaused(), "restoration requires explicit resume");
        check(restored.elapsed(5) == 20000, "reboot uptime may be smaller");
        restored.resume(5);
        check(restored.remaining(10005) == 25000, "restored rest must tick normally");
        restored.beginPhase(0, 10005);
        check(restored.phaseElapsed(12005) == 2000, "rep stopwatch starts at zero");
        check(restored.elapsed(12005) == 32000, "total spans multiple phases");
        restored.start(30000);
        check(restored.elapsed(30000) == 0, "new session resets previous time");
        restored.beginPhase(75000, 30000);
        restored.pause(32000);
        restored.setPhaseDuration(10000);
        check(restored.remaining(99999) == 8000, "shortening rest keeps elapsed time and excludes pause");
        restored.setPhaseDuration(0);
        check(restored.remaining(99999) == 0 && restored.isPaused(), "zero-rest edit remains paused until explicit resume");
        System.out.println("WorkoutClockTest: 12 checks passed");
    }

    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }
}
