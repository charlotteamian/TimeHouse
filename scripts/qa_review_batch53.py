#!/usr/bin/env python3
"""Batch fifty-three candidates: verify all ten stay unreviewed while anatomy, supports, and steps update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3221", "2133", "3222", "2136", "3223", "2137", "3224", "2143", "3231", "2188"]
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
        row("3221")["primary"] == ["股四头肌"]
        and row("2133")["primary"] == ["股四头肌"]
        and all(row(x)["primary"] == ["心肺系统", "股四头肌"] for x in ["3222", "3223", "3224"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["2136", "2137", "2143"])
        and row("3231")["primary"] == ["脊柱", "腘绳肌"]
        and row("2188")["primary"] == ["肱三头肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("2137")["requiredEquipment"] == ["直立靠背训练凳"]
        and row("2137")["available"]["哑铃|直立靠背训练凳"]
        and not row("2137")["available"]["哑铃"]
        and row("2188")["requiredEquipment"] == ["平板训练凳"]
        and row("2188")["available"]["哑铃|平板训练凳"]
        and not row("2188")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] for x in ["3221", "2133", "3222", "2136", "3223", "3224", "2143", "3231"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "Batch 53 avoids hold triggers and configures bilateral rep modes cleanly",
    )
    check(
        all(row(x)["knee"] == "MEDIUM" for x in ["3221", "2133", "3222", "3223", "3224"])
        and row("3231")["lower_back"] == "MEDIUM"
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["2136", "2137", "2143", "2188"]),
        "Joint stress screening reflects knee load for squats/jumps/walk, low-back load for toe-touch, and standing/seated arm-day safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳|直立靠背训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
