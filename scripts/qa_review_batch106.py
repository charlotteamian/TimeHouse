#!/usr/bin/env python3
"""Batch one hundred and six candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1015", "1016", "1017", "1018", "1022", "1023", "1253", "1254", "1255", "1256"]
per_side_ids = set()
no_support_ids = set(inspected) - {"1254", "1255", "1256"}
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
        row("1015")["primary"] == ["腹肌"]
        and row("1016")["primary"] == ["前臂"]
        and all(row(x)["primary"] == ["三角肌"] for x in ["1017", "1022"])
        and row("1018")["primary"] == ["斜方肌"]
        and row("1023")["primary"] == ["臀肌"]
        and row("1253")["primary"] == ["小腿肌"]
        and all(row(x)["primary"] == ["胸肌"] for x in ["1254", "1256"])
        and row("1255")["primary"] == ["背阔肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("1254")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == ["带勾脚的下斜训练凳"] for x in ["1255", "1256"])
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce exact required supporting equipment with bench and decline bench registered",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "Batch 106 avoids hold triggers and configures bilateral band, machine, and barbell pacing cleanly",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in ["1023", "1253"])
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["1018", "1255"])
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["1017", "1022", "1254", "1256"])
        and row("1015")["shoulder"] == "NONE" and row("1015")["lower_back"] == "MEDIUM" and row("1015")["knee"] == "NONE"
        and row("1016")["shoulder"] == "NONE" and row("1016")["lower_back"] == "NONE" and row("1016")["knee"] == "NONE",
        "Joint stress screening reflects knee loading for deadlifts and calf raises, core loading for pallof presses, back and shoulder loading for shrugs and pullovers, shoulder loading for raises and bench presses, and low stress for wrist curls",
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
        state_with(reviewedOnlyV1=False, equipment="弹力带|平板训练凳|杠铃|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND SIX INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
