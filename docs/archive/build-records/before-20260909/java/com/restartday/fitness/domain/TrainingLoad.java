package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * 一次已完成的动作在训练量上的贡献：练了哪些部位、做了几组、什么时候练的。
 *
 * <p>{@link WeeklyVolumeLedger} 和 {@link RecoveryState} 都吃这个类型，
 * 这样领域层不用去查动作库——调用方把动作解析成部位后传进来即可。
 */
public final class TrainingLoad {

    private final List<String> regions;   // 第一个是主要部位，其余算间接
    private final int sets;
    private final long atMillis;

    public TrainingLoad(List<String> regions, int sets, long atMillis) {
        this.regions = Collections.unmodifiableList(
                regions == null ? new ArrayList<String>() : new ArrayList<String>(regions));
        this.sets = Math.max(0, sets);
        this.atMillis = atMillis;
    }

    /** 目标部位，第一个是主要部位。 */
    public List<String> regions() {
        return regions;
    }

    public int sets() {
        return sets;
    }

    public long atMillis() {
        return atMillis;
    }

    public String primaryRegion() {
        return regions.isEmpty() ? "" : regions.get(0);
    }
}
