package com.restartday.fitness.domain;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** User-authored prescription; expanding a circuit never re-ranks or changes the saved dose. */
public final class WorkoutRoutine {
    private final String id, name, note;
    private final boolean circuit;
    private final int rounds, roundRest;
    private final List<WorkoutItem> items;

    public WorkoutRoutine(String id, String name, String note, boolean circuit, int rounds,
            int roundRest, List<WorkoutItem> items) {
        if (id == null || id.isEmpty() || name == null || name.trim().isEmpty())
            throw new IllegalArgumentException("请填写动作组名称");
        if (rounds < 1 || rounds > 20 || roundRest < 0 || roundRest > 600)
            throw new IllegalArgumentException("轮数需为 1–20，轮间休息需为 0–600 秒");
        if (items == null || items.isEmpty() || items.size() > 30)
            throw new IllegalArgumentException("请添加 1–30 个动作");
        for (WorkoutItem item : items) {
            Prescription p = item.prescription();
            if (p == null || p.sets() < 1 || p.sets() > 20 || p.restSeconds() < 0 || p.restSeconds() > 600
                    || (p.kind() == Prescription.Kind.HOLD ? p.holdSeconds() < 5 || p.holdSeconds() > 3600
                    : p.repsLow() < 1 || p.repsHigh() > 500 || p.repsHigh() < p.repsLow()))
                throw new IllegalArgumentException("动作处方超出可保存范围");
        }
        this.id = id; this.name = name.trim(); this.note = note == null ? "" : note;
        this.circuit = circuit; this.rounds = rounds; this.roundRest = roundRest;
        this.items = Collections.unmodifiableList(new ArrayList<>(items));
    }
    public String id() { return id; }
    public String name() { return name; }
    public String note() { return note; }
    public boolean circuit() { return circuit; }
    public int rounds() { return rounds; }
    public int roundRest() { return roundRest; }
    public List<WorkoutItem> items() { return items; }
    public List<WorkoutItem> expand() {
        List<WorkoutItem> result = new ArrayList<>();
        int loops = circuit ? rounds : 1;
        for (int round = 0; round < loops; round++) {
            for (int i = 0; i < items.size(); i++) {
                WorkoutItem item = items.get(i);
                boolean last = i == items.size() - 1;
                boolean finished = last && round == loops - 1;
                int rest = finished ? 0 : circuit && last ? roundRest : item.prescription().restSeconds();
                result.add(new WorkoutItem(item.exercise(), item.prescription(), item.favorite(),
                        (circuit ? "第 " + (round + 1) + " / " + rounds + " 轮 · " : "") + item.reason(), rest));
            }
        }
        return result;
    }
}
