#!/usr/bin/env python3
"""Batch seventy-three candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0112", "0113", "0114", "0115", "0116", "0117", "0118", "0119", "0120", "0121"]
per_side_ids = {"0112", "0114"}
step_ids = {"0114"}
no_support_ids = {"0112", "0113", "0115", "0116", "0117", "0118", "0119", "0120", "0121"}
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
        row("0112")["primary"] == ["腹肌", "腹斜肌"]
        and row("0113")["primary"] == ["肱二头肌"]
        and all(row(x)["primary"] == ["臀肌"] for x in ["0114", "0115", "0117"])
        and row("0116")["primary"] == ["腘绳肌"]
        and row("0118")["primary"] == ["上背"]
        and all(row(x)["primary"] == ["三角肌"] for x in ["0119", "0120", "0121"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["稳固踏台"] and row(x)["safeWithRequiredEquipment"] for x in step_ids)
        and all(row(x)["requiredEquipment"] == [] for x in no_support_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 73 avoids hold triggers and configures unilateral twists and step-ups cleanly",
    )
    check(
        row("0112")["lower_back"] == "MEDIUM" and row("0112")["shoulder"] == "NONE" and row("0112")["knee"] == "NONE"
        and row("0113")["shoulder"] == "MEDIUM" and row("0113")["lower_back"] == "NONE" and row("0113")["knee"] == "NONE"
        and all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["shoulder"] == "NONE" for x in ["0114", "0115", "0116", "0117"])
        and row("0118")["shoulder"] == "MEDIUM" and row("0118")["lower_back"] == "MEDIUM" and row("0118")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0119", "0120", "0121"]),
        "Joint stress screening reflects shoulder loading for curls/rows/shrugs, back stress for twists/rows, and knee stress for step-ups/deadlifts",
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
        state_with(reviewedOnlyV1=False, equipment="杠铃|稳固踏台", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SEVENTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
