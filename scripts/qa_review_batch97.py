#!/usr/bin/env python3
"""Batch ninety-seven candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0764", "0765", "0766", "0767", "0768", "0769", "0770", "0771", "0772", "0773"]
per_side_ids = {"0768"}
no_support_ids = set(inspected)
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
        row("0764")["primary"] == ["胸肌"]
        and all(row(x)["primary"] == ["三角肌"] for x in ["0765", "0766", "0772"])
        and row("0767")["primary"] == ["斜方肌"]
        and row("0768")["primary"] == ["股四头肌"]
        and all(row(x)["primary"] == ["臀肌"] for x in ["0769", "0770"])
        and row("0771")["primary"] == ["前臂"]
        and row("0773")["primary"] == ["小腿肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 97 avoids hold triggers and configures unilateral split squat pacing cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0764", "0765", "0766", "0772"])
        and row("0767")["shoulder"] == "MEDIUM" and row("0767")["lower_back"] == "MEDIUM" and row("0767")["knee"] == "NONE"
        and row("0771")["shoulder"] == "NONE" and row("0771")["lower_back"] == "NONE" and row("0771")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in ["0768", "0769", "0770", "0773"]),
        "Joint stress screening reflects shoulder loading for presses, back loading for shrugs, zero joint stress for wrist curls, and knee loading for squats, lunges, and calf raises",
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
        state_with(reviewedOnlyV1=False, equipment="自由重量|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH NINETY-SEVEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
