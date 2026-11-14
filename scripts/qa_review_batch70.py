#!/usr/bin/env python3
"""Batch seventy candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0081", "0082", "0083", "0084", "0085", "0086", "0087", "0088", "0089", "0090"]
preacher_ids = {"0081"}
flat_bench_ids = {"0082", "0083", "0086", "0087", "0089", "0090"}
flat_bench_step_ids = {"0088"}
no_support_ids = {"0084", "0085"}
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
        all(row(x)["primary"] == ["肱二头肌"] for x in ["0081", "0089"])
        and row("0082")["primary"] == ["前臂"]
        and all(row(x)["primary"] == ["腹肌"] for x in ["0083", "0084"])
        and all(row(x)["primary"] == ["臀肌"] for x in ["0085", "0090"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["0086", "0087"])
        and row("0088")["primary"] == ["小腿肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["牧师凳"] and row(x)["safeWithRequiredEquipment"] for x in preacher_ids)
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["safeWithRequiredEquipment"] for x in flat_bench_ids)
        and all(row(x)["requiredEquipment"] == ["平板训练凳", "稳固踏台"] and row(x)["safeWithRequiredEquipment"] for x in flat_bench_step_ids)
        and all(row(x)["requiredEquipment"] == [] for x in no_support_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "Batch 70 avoids hold triggers and configures bilateral reps cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0081", "0086", "0087", "0089"])
        and row("0082")["shoulder"] == "NONE" and row("0082")["lower_back"] == "NONE" and row("0082")["knee"] == "NONE"
        and all(row(x)["lower_back"] == "MEDIUM" and row(x)["shoulder"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0083", "0084"])
        and all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["shoulder"] == "NONE" for x in ["0085", "0088", "0090"]),
        "Joint stress screening reflects shoulder loading for presses/curls, back stress for rollouts, and knee stress for deadlifts/calves/good-mornings",
    )

    for xid in inspected:
        item = {
            "id": "dataset_1324_" + xid,
            "sets": 1,
            "reps": "8",
            "rpe": "7",
            "rest": 30,
            "kind": "REPS",
            "hold": 0,
            "perSide": False,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="杠铃|平板训练凳|稳固踏台|牧师凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SEVENTY INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
