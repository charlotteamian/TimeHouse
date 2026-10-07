package com.restartday.fitness.app;

import android.content.Context;
import android.content.pm.PackageManager;
import android.health.connect.*;
import android.health.connect.datatypes.*;
import android.os.OutcomeReceiver;
import org.json.*;
import java.time.Instant;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.ToDoubleFunction;

/** Reads aggregates for exactly one workout window; calories are never estimated from heart rate. */
final class WatchMetricsReader {
    static final String ACTIVE = "android.permission.health.READ_ACTIVE_CALORIES_BURNED";
    static final String TOTAL = "android.permission.health.READ_TOTAL_CALORIES_BURNED";
    static final String STEPS = "android.permission.health.READ_STEPS";
    static final String DISTANCE = "android.permission.health.READ_DISTANCE";
    private final Context context;
    private final HealthConnectManager manager;
    private final long start, end;
    private final String origin;
    private final Consumer<JSONObject> callback;
    private final JSONObject result = new JSONObject();
    private int pending = 4;
    WatchMetricsReader(Context context, HealthConnectManager manager, long start, long end, String origin, Consumer<JSONObject> callback) {
        this.context = context; this.manager = manager; this.start = start; this.end = end; this.origin = origin; this.callback = callback;
    }
    void read() {
        read("activeKcal", ACTIVE, ActiveCaloriesBurnedRecord.ACTIVE_CALORIES_TOTAL, v -> v.getInCalories() / 1000.0, ActiveCaloriesBurnedRecord.class, r -> r.getEnergy().getInCalories() / 1000.0);
        read("totalKcal", TOTAL, TotalCaloriesBurnedRecord.ENERGY_TOTAL, v -> v.getInCalories() / 1000.0, TotalCaloriesBurnedRecord.class, r -> r.getEnergy().getInCalories() / 1000.0);
        read("steps", STEPS, StepsRecord.STEPS_COUNT_TOTAL, v -> v.doubleValue(), StepsRecord.class, r -> (double) r.getCount());
        read("distanceM", DISTANCE, DistanceRecord.DISTANCE_TOTAL, v -> v.getInMeters(), DistanceRecord.class, r -> r.getDistance().getInMeters());
    }
    private <T, R extends IntervalRecord> void read(String name, String permission, AggregationType<T> type, ToDoubleFunction<T> number, Class<R> rawType, ToDoubleFunction<R> rawNumber) {
        if (context.checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED) { finish(); return; }
        try {
            AggregateRecordsRequest.Builder<T> request = new AggregateRecordsRequest.Builder<T>(new TimeInstantRangeFilter.Builder()
                    .setStartTime(Instant.ofEpochMilli(start)).setEndTime(Instant.ofEpochMilli(end)).build()).addAggregationType(type);
            if (!origin.isEmpty()) request.addDataOriginsFilter(new DataOrigin.Builder().setPackageName(origin).build());
            manager.aggregate(request.build(), context.getMainExecutor(), new OutcomeReceiver<AggregateRecordsResponse<T>, HealthConnectException>() {
                public void onResult(AggregateRecordsResponse<T> response) {
                    try {
                        T value = response.get(type);
                        if (value == null || response.getDataOrigins(type).isEmpty()) {
                            // Aggregates can omit providers excluded from system priority. Never present
                            // the source-less basal-energy fallback as recorded workout calories.
                            readRaw(name, rawType, rawNumber, -1, new ArrayList<R>()); return;
                        }
                        if (Double.isFinite(number.applyAsDouble(value)) && number.applyAsDouble(value) >= 0) {
                            JSONArray sources = new JSONArray();
                            for (DataOrigin source : response.getDataOrigins(type)) sources.put(source.getPackageName());
                            // Total energy may include system-derived basal energy; preserve its provenance.
                            result.put(name, new JSONObject().put("value", number.applyAsDouble(value)).put("sources", sources)
                                    .put("start", start).put("end", end));
                        }
                    } catch (Exception ignored) { }
                    finish();
                }
                public void onError(HealthConnectException error) { error(name, error.getMessage()); finish(); }
            });
        } catch (Exception error) { error(name, error.getMessage()); finish(); }
    }
    private <R extends IntervalRecord> void readRaw(String name, Class<R> type, ToDoubleFunction<R> number, long token, List<R> rows) {
        try {
            ReadRecordsRequestUsingFilters.Builder<R> request = new ReadRecordsRequestUsingFilters.Builder<>(type)
                    .setTimeRangeFilter(new TimeInstantRangeFilter.Builder().setStartTime(Instant.ofEpochMilli(start))
                            .setEndTime(Instant.ofEpochMilli(end)).build()).setPageSize(1000);
            if (!origin.isEmpty()) request.addDataOrigins(new DataOrigin.Builder().setPackageName(origin).build());
            if (token >= 0) request.setPageToken(token);
            manager.readRecords(request.build(), context.getMainExecutor(), new OutcomeReceiver<ReadRecordsResponse<R>, HealthConnectException>() {
                public void onResult(ReadRecordsResponse<R> response) {
                    rows.addAll(response.getRecords());
                    if (response.getNextPageToken() != -1) { readRaw(name, type, number, response.getNextPageToken(), rows); return; }
                    try { storeRaw(name, rows, number); } catch (Exception e) { error(name, e.getMessage()); }
                    finish();
                }
                public void onError(HealthConnectException e) { error(name, e.getMessage()); finish(); }
            });
        } catch (Exception e) { error(name, e.getMessage()); finish(); }
    }

    /** Sum only whole, disjoint recorded intervals from one provider. Do not prorate daily totals. */
    private <R extends IntervalRecord> void storeRaw(String name, List<R> rows, ToDoubleFunction<R> number) throws JSONException {
        Map<String, List<R>> bySource = new TreeMap<>();
        for (R row : rows) {
            if (row.getStartTime().toEpochMilli() < start || row.getEndTime().toEpochMilli() > end
                    || !Double.isFinite(number.applyAsDouble(row)) || number.applyAsDouble(row) < 0) continue;
            bySource.computeIfAbsent(row.getMetadata().getDataOrigin().getPackageName(), k -> new ArrayList<>()).add(row);
        }
        long bestCoverage = 0; double bestValue = 0; String bestSource = null;
        for (Map.Entry<String, List<R>> entry : bySource.entrySet()) {
            List<R> source = entry.getValue();
            source.sort((a, b) -> b.getMetadata().getLastModifiedTime().compareTo(a.getMetadata().getLastModifiedTime()));
            R exact = null;
            for (R row : source) if (row.getStartTime().toEpochMilli() == start && row.getEndTime().toEpochMilli() == end) { exact = row; break; }
            if (exact != null) source = new ArrayList<>(Arrays.asList(exact));
            // The newest version wins for duplicate intervals, then require no overlaps.
            Map<String, R> unique = new LinkedHashMap<>();
            for (R row : source) unique.putIfAbsent(row.getStartTime() + "/" + row.getEndTime(), row);
            source = new ArrayList<>(unique.values()); source.sort((a, b) -> a.getStartTime().compareTo(b.getStartTime()));
            long last = start, coverage = 0; double value = 0; boolean overlaps = false;
            for (R row : source) {
                long from = row.getStartTime().toEpochMilli(), to = row.getEndTime().toEpochMilli();
                if (from < last) { overlaps = true; break; }
                coverage += Math.max(0, to - from); value += number.applyAsDouble(row); last = to;
            }
            if (!overlaps && coverage > bestCoverage) { bestCoverage = coverage; bestValue = value; bestSource = entry.getKey(); }
        }
        if (bestSource != null) result.put(name, new JSONObject().put("value", bestValue)
                .put("sources", new JSONArray().put(bestSource)).put("start", start).put("end", end)
                .put("coverage", Math.min(100, Math.round(bestCoverage * 100.0 / (end - start)))));
    }

    private void error(String name, String message) {
        try { result.put(name + "Error", message == null ? "读取失败" : message); } catch (JSONException ignored) { }
    }
    private void finish() { if (--pending == 0) callback.accept(result); }
}
