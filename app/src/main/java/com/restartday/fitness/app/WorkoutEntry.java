package com.restartday.fitness.app;

import com.restartday.fitness.domain.*;
import org.json.*;

/** A historical snapshot remains usable even when its catalog exercise is edited or deleted. */
final class WorkoutEntry {
    final String id, name, weight, original;
    final Prescription dose; // null means a legacy record never stored its dose
    final int completed, restAfter;
    final boolean finished;
    WorkoutEntry(String id, String name, Prescription dose, int completed, boolean finished,
            int restAfter, String weight, String original) {
        this.id = id; this.name = name; this.dose = dose; this.completed = completed;
        this.finished = finished; this.restAfter = restAfter; this.weight = weight; this.original = original;
    }
    String line() {
        if (dose == null) return original + "\n次数 / 重量未记录，可补填";
        return (finished ? "✓ " : completed > 0 ? "◐ " : "○ ") + name + " · " + completed + "/" + dose.sets() + " 组 · 每组 "
                + (dose.kind() == Prescription.Kind.HOLD ? dose.holdSeconds() + " 秒" : dose.reps() + " 次")
                + (dose.perSide() ? " / 侧" : "") + (weight.isEmpty() ? "" : " · 重量 " + weight)
                + elapsedLabel()
                + "\n组间 " + dose.restSeconds() + " 秒 · 动作间 " + restAfter + " 秒";
    }
    private String elapsedLabel() {
        java.util.regex.Matcher m = java.util.regex.Pattern.compile(" · ([0-9]+:[0-9]{2})(?: ·|$)").matcher(original);
        return m.find() ? " · 用时 " + m.group(1) : "";
    }
    String stat() { return id + "|" + completed + "|" + (finished ? 1 : 0); }
    JSONObject json() throws JSONException {
        JSONObject o = new JSONObject().put("id", id).put("name", name).put("completed", completed)
                .put("finished", finished).put("restAfter", restAfter).put("weight", weight).put("original", original);
        if (dose != null) o.put("dose", new JSONObject().put("sets", dose.sets()).put("reps", dose.reps())
                .put("kind", dose.kind().name()).put("hold", dose.holdSeconds()).put("side", dose.perSide())
                .put("rest", dose.restSeconds()).put("rpe", dose.rpe()).put("tempo", dose.secondsPerRep()));
        return o;
    }
    static WorkoutEntry from(JSONObject o) {
        JSONObject p = o.optJSONObject("dose"); Prescription dose = null;
        if (p != null) dose = ("HOLD".equals(p.optString("kind"))
                ? Prescription.hold(p.optInt("sets"), p.optInt("hold"), p.optString("rpe"), p.optInt("rest"), p.optBoolean("side"))
                : new Prescription(p.optInt("sets"), p.optString("reps"), p.optString("rpe"), p.optInt("rest")).withPerSide(p.optBoolean("side")))
                .withSecondsPerRep(p.optDouble("tempo", 3));
        return new WorkoutEntry(o.optString("id"), o.optString("name"), dose, o.optInt("completed"), o.optBoolean("finished"),
                o.optInt("restAfter"), o.optString("weight"), o.optString("original"));
    }
}
