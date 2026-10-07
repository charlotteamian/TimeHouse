package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 每个部位距离上次练过了多久——临时加练用它避开还在恢复的肌群。
 *
 * <p>依据：同一肌群的两次高强度刺激之间通常需要 48 小时左右恢复
 * （ACSM 抗阻训练建议：同一肌群不要连续两天大强度训练）。
 * 所以 48 小时内练过的部位在加练里降权，24 小时内的直接排除。
 */
public final class RecoveryState {

    /** 24 小时内练过：加练直接避开。 */
    public static final double HARD_BLOCK_HOURS = 24;

    /** 48 小时内练过：还在恢复，降权但不完全排除（用户明确点名要练时仍然给）。 */
    public static final double RECOVERING_HOURS = 48;

    private final Map<String, Double> hoursSince;

    private RecoveryState(Map<String, Double> hoursSince) {
        this.hoursSince = Collections.unmodifiableMap(hoursSince);
    }

    public static RecoveryState of(List<TrainingLoad> loads, long nowMillis) {
        Map<String, Long> lastAt = new LinkedHashMap<String, Long>();
        if (loads != null) {
            for (TrainingLoad load : loads) {
                if (load == null || load.sets() <= 0 || load.atMillis() > nowMillis) {
                    continue;
                }
                for (String region : load.regions()) {
                    Long prior = lastAt.get(region);
                    if (prior == null || load.atMillis() > prior) {
                        lastAt.put(region, load.atMillis());
                    }
                }
            }
        }
        Map<String, Double> hours = new LinkedHashMap<String, Double>();
        for (Map.Entry<String, Long> entry : lastAt.entrySet()) {
            hours.put(entry.getKey(), (nowMillis - entry.getValue()) / 3600000.0);
        }
        return new RecoveryState(hours);
    }

    /** 距离上次练这个部位过了多少小时；从没练过返回 {@link Double#MAX_VALUE}。 */
    public double hoursSince(String region) {
        Double value = hoursSince.get(region);
        return value == null ? Double.MAX_VALUE : value;
    }

    /** 24 小时内刚练过，加练应该避开。 */
    public boolean isBlocked(String region) {
        return hoursSince(region) < HARD_BLOCK_HOURS;
    }

    /** 48 小时内练过，还在恢复窗口里。 */
    public boolean isRecovering(String region) {
        return hoursSince(region) < RECOVERING_HOURS;
    }

    /** 还在恢复中的部位，按最近练过的排在前面。 */
    public List<String> recoveringRegions() {
        List<String> result = new ArrayList<String>();
        for (Map.Entry<String, Double> entry : hoursSince.entrySet()) {
            if (entry.getValue() < RECOVERING_HOURS) {
                result.add(entry.getKey());
            }
        }
        Collections.sort(result, (left, right) ->
                Double.compare(hoursSince(left), hoursSince(right)));
        return result;
    }

    public String describe(String region) {
        double hours = hoursSince(region);
        if (hours == Double.MAX_VALUE) {
            return region + "：最近没练过";
        }
        if (hours < 1) {
            return region + "：刚练完";
        }
        return region + "：" + Math.round(hours) + " 小时前练过";
    }
}
