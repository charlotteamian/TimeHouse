#!/usr/bin/env python3
"""Batch ninety-three candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0607", "0609", "0636", "0637", "0640", "0641", "0648", "0650", "0653", "0655"]
per_side_ids = {"0640"}
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
        all(row(x)["primary"] == ["肱三头肌"] for x in ["0607", "0637"])
        and row("0609")["primary"] == ["上背"]
        and row("0636")["primary"] == ["肱二头肌"]
        and all(row(x)["primary"] == ["腹肌"] for x in ["0640", "0641", "0650"])
        and row("0648")["primary"] == ["腘绳肌"]
        and all(row(x)["primary"] == ["胸肌"] for x in ["0653", "0655"]),
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
        "Batch 93 avoids hold triggers and configures unilateral medicine ball slam pacing cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0607", "0636", "0637", "0653", "0655"])
        and row("0609")["shoulder"] == "MEDIUM" and row("0609")["lower_back"] == "MEDIUM" and row("0609")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["0640", "0641", "0650"])
        and row("0648")["shoulder"] == "NONE" and row("0648")["lower_back"] == "NONE" and row("0648")["knee"] == "MEDIUM",
        "Joint stress screening reflects shoulder loading for extensions, curls, and push-ups, back loading for rope London bridge rows, waist loading for ball slams and crunches, and knee loading for power cleans",
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
        state_with(reviewedOnlyV1=False, equipment="自由重量|固定器械|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH NINETY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
