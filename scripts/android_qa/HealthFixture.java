package com.restartday.fitness.qa;

import android.app.Instrumentation;
import android.os.*;
import android.health.connect.*;
import android.health.connect.datatypes.*;
import android.health.connect.datatypes.units.*;
import java.time.Instant;
import java.util.*;
import org.json.*;

/** Emulator test provider; caller deletes exactly the record IDs returned by insertion. */
public final class HealthFixture extends Instrumentation {
    private Bundle args;
    public void onCreate(Bundle arguments) { super.onCreate(arguments); args = arguments; start(); }
    private Metadata metadata() {
        return new Metadata.Builder().setDataOrigin(new DataOrigin.Builder().setPackageName(getContext().getPackageName()).build())
                .setClientRecordId("timehouse-qa-" + UUID.randomUUID()).build();
    }
    public void onStart() {
        HealthConnectManager manager = (HealthConnectManager) getContext().getSystemService("healthconnect");
        Bundle result = new Bundle();
        try {
            String remove = args.getString("delete");
            if (remove != null) {
                JSONArray array = new JSONArray(remove); List<RecordIdFilter> ids = new ArrayList<>();
                for (int i = 0; i < array.length(); i++) {
                    JSONObject row = array.getJSONObject(i);
                    Class<? extends android.health.connect.datatypes.Record> type = Class.forName(row.getString("type")).asSubclass(android.health.connect.datatypes.Record.class);
                    ids.add(RecordIdFilter.fromId(type, row.getString("id")));
                }
                manager.deleteRecords(ids, getContext().getMainExecutor(), new OutcomeReceiver<Void, HealthConnectException>() {
                    public void onResult(Void value) { result.putBoolean("deleted", true); finish(0, result); }
                    public void onError(HealthConnectException e) { result.putString("error", e.toString()); finish(1, result); }
                }); return;
            }
            long start = Long.parseLong(args.getString("start")), end = Long.parseLong(args.getString("end"));
            Instant from = Instant.ofEpochMilli(start), to = Instant.ofEpochMilli(end);
            List<android.health.connect.datatypes.Record> records = new ArrayList<>();
            records.add(new ExerciseSessionRecord.Builder(metadata(), from.minusSeconds(3600), to.plusSeconds(180), ExerciseSessionType.EXERCISE_SESSION_TYPE_STRENGTH_TRAINING).setTitle("QA unrelated long workout").build());
            records.add(new ExerciseSessionRecord.Builder(metadata(), from, to, ExerciseSessionType.EXERCISE_SESSION_TYPE_STRENGTH_TRAINING).setTitle("QA workout").build());
            records.add(new ActiveCaloriesBurnedRecord.Builder(metadata(), from, to, Energy.fromCalories(120000)).build());
            records.add(new TotalCaloriesBurnedRecord.Builder(metadata(), from, to, Energy.fromCalories(150000)).build());
            records.add(new StepsRecord.Builder(metadata(), from, to, 234).build());
            records.add(new DistanceRecord.Builder(metadata(), from, to, Length.fromMeters(180)).build());
            List<HeartRateRecord.HeartRateSample> points = new ArrayList<>();
            for (long time = start; time < end; time += 10000) points.add(new HeartRateRecord.HeartRateSample(90 + ((time - start) / 10000) % 40, Instant.ofEpochMilli(time)));
            records.add(new HeartRateRecord.Builder(metadata(), from, to, points).build());
            records.add(new ActiveCaloriesBurnedRecord.Builder(metadata(), to.plusSeconds(60), to.plusSeconds(120), Energy.fromCalories(900000)).build());
            manager.insertRecords(records, getContext().getMainExecutor(), new OutcomeReceiver<InsertRecordsResponse, HealthConnectException>() {
                public void onResult(InsertRecordsResponse response) {
                    JSONArray ids = new JSONArray();
                    try { for (android.health.connect.datatypes.Record r : response.getRecords())
                        ids.put(new JSONObject().put("type", r.getClass().getName()).put("id", r.getMetadata().getId())); }
                    catch (Exception e) { result.putString("error", e.toString()); }
                    result.putString("ids", ids.toString()); finish(0, result);
                }
                public void onError(HealthConnectException e) { result.putString("error", e.toString()); finish(1, result); }
            });
        } catch (Exception e) { result.putString("error", e.toString()); finish(1, result); }
    }
}
