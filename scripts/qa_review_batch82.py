#!/usr/bin/env python3
"""Batch eighty-two candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0228", "0229", "0230", "0231", "0232", "0233", "0234", "0235", "0236", "0237"]
per_side_ids = {"0228", "0230", "0231", "0235"}
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
        row("0228")["primary"] == ["臀肌"]
        and row("0229")["primary"] == ["肱二头肌"]
        and row("0230")["primary"] == ["腹肌"]
        and row("0231")["primary"] == ["肱三头肌"]
        and all(row(x)["primary"] == ["背阔肌"] for x in ["0232", "0237"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["0233", "0235"])
        and all(row(x)["primary"] == ["上背"] for x in ["0234", "0236"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in inspected),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 82 avoids hold triggers and configures unilateral kickbacks, twists, extensions, and external rotations cleanly",
    )
    check(
        row("0228")["shoulder"] == "NONE" and row("0228")["lower_back"] == "NONE" and row("0228")["knee"] == "MEDIUM"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0229", "0231", "0233", "0235"])
        and row("0230")["shoulder"] == "NONE" and row("0230")["lower_back"] == "MEDIUM" and row("0230")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["0232", "0234", "0236", "0237"]),
        "Joint stress screening reflects knee loading for kickbacks, back loading for waist twists, shoulder and back loading for cable rows and pulldowns, and shoulder loading for arm extensions, curls, facepulls, and rotations",
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
        state_with(reviewedOnlyV1=False, equipment="固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH EIGHTY-TWO INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
