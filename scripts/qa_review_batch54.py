#!/usr/bin/env python3
"""Batch fifty-four candidates: verify all ten stay unreviewed while anatomy, supports, and steps update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3239", "2189", "3287", "2292", "3288", "2293", "3289", "2294", "3291", "2317"]
per_side_ids = {"3239"}
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
        row("3239")["primary"] == ["腹肌", "腹斜肌"]
        and all(row(x)["primary"] == ["肱三头肌"] for x in ["2189", "3287", "3289", "3291"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["2292", "2317"])
        and row("3288")["primary"] == ["胸肌"]
        and all(row(x)["primary"] == ["肱二头肌", "前臂"] for x in ["2293", "2294"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("2189")["requiredEquipment"] == ["直立靠背训练凳"]
        and row("2189")["available"]["哑铃|直立靠背训练凳"]
        and not row("2189")["available"]["哑铃"]
        and row("2317")["requiredEquipment"] == ["平板训练凳"]
        and row("2317")["available"]["哑铃|平板训练凳"]
        and not row("2317")["available"]["哑铃"]
        and row("3287")["requiredEquipment"] == ["平板训练凳"]
        and row("3287")["available"]["平板训练凳"]
        and all(row(x)["requiredEquipment"] == ["双杠"] and row(x)["available"]["双杠"] and not row(x)["available"]["自重"] for x in ["3288", "3289"])
        and all(row(x)["requiredEquipment"] == ["牧师凳"] and row(x)["safeWithRequiredEquipment"] and not row(x)["available"]["哑铃"] for x in ["2293", "2294"])
        and all(row(x)["requiredEquipment"] == [] for x in ["3239", "2292", "3291"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 54 avoids hold triggers while configuring unilateral/bilateral rep modes accurately",
    )
    check(
        row("3239")["lower_back"] == "MEDIUM"
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in inspected if x != "3239"),
        "Joint stress screening reflects axial plank load and arm/shoulder bench-and-bar safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳|直立靠背训练凳|双杠|牧师凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-FOUR INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
