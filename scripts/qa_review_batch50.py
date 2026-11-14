#!/usr/bin/env python3
"""Batch fifty candidates: verify all ten stay unreviewed while metadata, anatomy, and supports update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3168", "1732", "3193", "1733", "3201", "1734", "3202", "1735", "3203", "1736"]
per_side_ids = {"1732", "1735", "1736"}
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
        row("3168")["primary"] == ["上背"]
        and all(row(x)["primary"] == ["肱三头肌"] for x in ["1732", "1733", "1734", "1735", "1736"])
        and row("3193")["primary"] == ["腘绳肌", "臀肌"]
        and all(row(x)["primary"] == ["腹肌"] for x in ["3201", "3202", "3203"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("3168")["requiredEquipment"] == ["TRX 悬挂带"] and row("3168")["safeWithRequiredEquipment"] and not row("3168")["available"]["自重"]
        and row("3193")["requiredEquipment"] == ["罗马椅"] and row("3193")["safeWithRequiredEquipment"] and not row("3193")["available"]["自重"]
        and row("1733")["requiredEquipment"] == ["上斜训练凳"] and row("1733")["available"]["哑铃|上斜训练凳"] and not row("1733")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] and row(x)["safeWithRequiredEquipment"] and not row(x)["available"]["哑铃"] for x in ["1734", "1736"])
        and row("1735")["requiredEquipment"] == ["平板训练凳"] and row("1735")["available"]["哑铃|平板训练凳"] and not row("1735")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] for x in ["1732", "3201", "3202", "3203"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in ["3168", "3193", "1733", "3201", "1734", "3202", "3203"]),
        "Batch 50 avoids hold triggers while configuring unilateral/bilateral rep modes accurately",
    )
    check(
        row("3168")["lower_back"] == "MEDIUM"
        and row("3193")["knee"] == "MEDIUM"
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["1733", "1734", "1735", "1736"])
        and all(row(x)["lower_back"] == "MEDIUM" for x in ["3201", "3202", "3203"]),
        "Joint stress screening reflects knee load on GHR, lower-back load on rows/sit-ups, and curl/extension low axial load",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳|上斜训练凳|瑜伽球|TRX 悬挂带", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
