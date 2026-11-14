#!/usr/bin/env python3
"""Batch one hundred and twenty-four deferred items: verify anatomy, supports, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1749", "1750", "1751", "1752", "1754", "1755", "1756", "1758", "1767", "2135"]
tricep_ids = {"1749", "1750", "1751", "1752", "1754", "1755", "1767"}
abs_ids = {"1758", "2135"}
flat_bench_ids = {"1750", "1754", "1755"}
no_support_ids = {"1749", "1751", "1756", "2135"}
dynamic_ids = set(inspected) - {"2135"}
per_side_ids = {"1756"}
bilateral_ids = set(inspected) - per_side_ids
names = {
    e["id"]: e["name_zh"]
    for e in json.loads(Path("app/src/main/assets/exercises_1324.json").read_text())["exercises"]
}

stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + s for s in inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    row = lambda x: catalog["dataset_1324_" + x]

    check(not any("dataset_1324_" + x in known for x in inspected), "All ten inspected entries remain unreviewed during initial checks")
    check("supportReviewInvalidation=1" in raw, "Supporting equipment changes invalidate stale personal approval")
    check(
        all(row(x)["primary"] == ["肱三头肌"] for x in tricep_ids)
        and row("1756")["primary"] == ["臀肌"]
        and all(row(x)["primary"] == ["腹肌"] for x in abs_ids),
        "Primary muscle groups match triceps, glutes, and abs across Batch 124",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] for x in flat_bench_ids)
        and row("1752")["requiredEquipment"] == ["上斜训练凳"]
        and row("1758")["requiredEquipment"] == ["稳固踏台"]
        and row("1767")["requiredEquipment"] == ["双杠"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "Batch 124 enforces flat bench, incline bench, step box, and parallel bars supports cleanly",
    )
    check(
        row("2135")["isHold"]
        and not any(row(x)["isHold"] for x in dynamic_ids)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 124 enables isHold exclusively on 2135 plank and unilateral perSide pacing on 1756",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in tricep_ids)
        and row("1756")["shoulder"] == "NONE" and row("1756")["lower_back"] == "NONE" and row("1756")["knee"] == "MEDIUM"
        and row("1758")["shoulder"] == "NONE" and row("1758")["lower_back"] == "MEDIUM" and row("1758")["knee"] == "NONE"
        and row("2135")["shoulder"] == "NONE" and row("2135")["lower_back"] == "MEDIUM" and row("2135")["knee"] == "NONE",
        "Joint stress screening reflects triceps, single-leg deadlift, sit-up, and plank loadings accurately",
    )

    for xid in inspected:
        item = {
            "id": "dataset_1324_" + xid,
            "sets": 1,
            "reps": "" if xid == "2135" else "10",
            "rpe": "7",
            "rest": 30,
            "kind": "HOLD" if xid == "2135" else "REPS",
            "hold": 30 if xid == "2135" else 0,
            "perSide": xid in per_side_ids,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="平板训练凳|上斜训练凳|稳固踏台|双杠", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY-FOUR INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
