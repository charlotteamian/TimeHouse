#!/usr/bin/env python3
"""Batch sixty-nine candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0071", "0072", "0073", "0074", "0075", "0076", "0077", "0078", "0079", "0080"]
per_side_ids = {"0077", "0078"}
incline_bench_ids = {"0072"}
flat_bench_ids = {"0073", "0079"}
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
        row("0071")["primary"] == ["腹肌"]
        and all(row(x)["primary"] == ["肱二头肌"] for x in ["0072", "0080"])
        and row("0073")["primary"] == ["背阔肌"]
        and all(row(x)["primary"] == ["臀肌"] for x in ["0074", "0077", "0078"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["0075", "0076"])
        and row("0079")["primary"] == ["前臂"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["上斜训练凳"] and row(x)["safeWithRequiredEquipment"] for x in incline_bench_ids)
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["safeWithRequiredEquipment"] for x in flat_bench_ids)
        and all(row(x)["requiredEquipment"] == [] for x in inspected if x not in incline_bench_ids and x not in flat_bench_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 69 avoids hold triggers and configures unilateral rear lunges cleanly",
    )
    check(
        row("0071")["lower_back"] == "MEDIUM" and row("0071")["shoulder"] == "NONE" and row("0071")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0072", "0080", "0075", "0076"])
        and row("0073")["shoulder"] == "MEDIUM" and row("0073")["lower_back"] == "MEDIUM" and row("0073")["knee"] == "NONE"
        and all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["shoulder"] == "NONE" for x in ["0074", "0077", "0078"])
        and row("0079")["shoulder"] == "NONE" and row("0079")["lower_back"] == "NONE" and row("0079")["knee"] == "NONE",
        "Joint stress screening reflects shoulder loading for curls/raises, back stress for pullovers/sit-ups, and knee stress for squats/lunges",
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
            "perSide": xid in per_side_ids,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="杠铃|平板训练凳|上斜训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SIXTY-NINE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
