#!/usr/bin/env python3
"""Batch sixty-two candidates: verify all seven stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3667", "3669", "3671", "3672", "3679", "3698", "3785"]
per_side_ids = {"3667", "3669", "3671", "3672"}
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

    check(not any("dataset_1324_" + x in known for x in inspected), "All seven inspected entries remain unreviewed during initial checks")
    check("supportReviewInvalidation=1" in raw, "Supporting equipment changes invalidate stale personal approval")
    check(
        row("3667")["primary"] == ["臀肌"]
        and row("3669")["primary"] == ["上背"]
        and all(row(x)["primary"] == ["心肺系统", "股四头肌"] for x in ["3671", "3672"])
        and row("3679")["primary"] == ["腹肌", "髋屈肌群"]
        and row("3698")["primary"] == ["腹肌", "核心肌群"]
        and row("3785")["primary"] == ["胸肌"],
        "Primary muscle groups match corrected anatomical targets for all seven inspected entries",
    )
    check(
        row("3785")["requiredEquipment"] == ["稳固踏台"]
        and row("3785")["available"]["稳固踏台"]
        and not row("3785")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] for x in inspected if x != "3785"),
        "All seven inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 62 avoids hold triggers and configures unilateral lateral kicks, archer rotations, and skips cleanly",
    )
    check(
        all(row(x)["knee"] == "MEDIUM" for x in ["3667", "3671", "3672"])
        and row("3669")["lower_back"] == "MEDIUM"
        and all(row(x)["lower_back"] == "MEDIUM" for x in ["3679", "3698"])
        and row("3785")["lower_back"] == "NONE" and row("3785")["knee"] == "NONE",
        "Joint stress screening reflects lower-body knee load, core/back low-back stress, and push-up safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|稳固踏台", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SIXTY-TWO INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
