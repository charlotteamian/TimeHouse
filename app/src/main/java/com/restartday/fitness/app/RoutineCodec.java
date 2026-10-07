package com.restartday.fitness.app;

import com.restartday.fitness.domain.*;
import org.json.*;
import java.util.*;
import java.util.function.Function;

/** Versioned local storage. Missing exercises cause a visible error, never silent substitutions. */
public final class RoutineCodec {
    private RoutineCodec() {}
    public static JSONObject item(WorkoutItem item) throws JSONException {
        Prescription p = item.prescription();
        return new JSONObject().put("id", item.exercise().id()).put("sets", p.sets())
                .put("reps", p.reps()).put("rpe", p.rpe()).put("rest", p.restSeconds())
                .put("kind", p.kind().name()).put("hold", p.holdSeconds()).put("perSide", p.perSide())
                .put("tempo", p.secondsPerRep()).put("reason", item.reason())
                .put("restAfter", item.restAfterSeconds()).put("weight", item.weight());
    }
    public static WorkoutItem item(JSONObject o, Function<String, Exercise> lookup) throws JSONException {
        Exercise e = lookup.apply(o.getString("id"));
        if (e == null) throw new IllegalArgumentException("动作已不存在：" + o.getString("id") + "，请恢复动作后重试");
        Prescription p = "HOLD".equals(o.getString("kind"))
                ? Prescription.hold(o.getInt("sets"), o.getInt("hold"), o.getString("rpe"), o.getInt("rest"), o.optBoolean("perSide"))
                : new Prescription(o.getInt("sets"), o.getString("reps"), o.getString("rpe"), o.getInt("rest"))
                        .withPerSide(o.optBoolean("perSide"));
        return new WorkoutItem(e, p.withSecondsPerRep(o.optDouble("tempo", 3)), false,
                o.optString("reason"), o.optInt("restAfter", o.optInt("rest")), o.optString("weight"));
    }
    public static JSONObject encode(WorkoutRoutine r) throws JSONException {
        JSONArray items = new JSONArray();
        for (WorkoutItem item : r.items()) items.put(item(item));
        return new JSONObject().put("version", 2).put("id", r.id()).put("name", r.name()).put("note", r.note())
                .put("circuit", r.circuit()).put("rounds", r.rounds()).put("roundRest", r.roundRest()).put("items", items);
    }
    public static WorkoutRoutine decode(JSONObject o, Function<String, Exercise> lookup) throws JSONException {
        if (o.getInt("version") != 1 && o.getInt("version") != 2) throw new IllegalArgumentException("动作组版本暂不支持");
        List<WorkoutItem> items = new ArrayList<>();
        JSONArray array = o.getJSONArray("items");
        for (int i = 0; i < array.length(); i++) {
            WorkoutItem decoded = item(array.getJSONObject(i), lookup);
            // Version 1 used one rest field for both between-set and between-exercise breaks.
            if (o.getInt("version") == 1) decoded = new WorkoutItem(decoded.exercise(), decoded.prescription(),
                    decoded.favorite(), decoded.reason(), decoded.prescription().restSeconds(), decoded.weight());
            items.add(decoded);
        }
        return new WorkoutRoutine(o.getString("id"), o.getString("name"), o.optString("note"),
                o.getBoolean("circuit"), o.getInt("rounds"), o.getInt("roundRest"), items);
    }
}
