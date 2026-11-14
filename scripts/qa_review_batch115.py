#!/usr/bin/env python3
"""Batch one hundred and fifteen candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1395", "1396", "1408", "1409", "1410", "1411", "1412", "1413", "1416", "1417"]
calf_ids = {"1395", "1396"}
glute_ids = {"1408", "1409", "1410", "1416", "1417"}
forearm_ids = {"1411", "1412"}
bicep_ids = {"1413"}
per_side_ids = {"1395", "1410", "1413", "1416", "1417"}
bilateral_ids = set(inspected) - per_side_ids
no_support_ids = set(inspected) - {"1396", "1411", "1412"}
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
        all(row(x)["primary"] == ["小腿肌"] for x in calf_ids)
        and all(row(x)["primary"] == ["臀肌"] for x in glute_ids)
        and all(row(x)["primary"] == ["前臂"] for x in forearm_ids)
        and row("1413")["primary"] == ["肱二头肌"],
        "Primary muscle groups match calves, glutes, forearms, and biceps across all ten entries",
    )
    check(
        row("1396")["requiredEquipment"] == ["稳固踏台"]
        and row("1411")["requiredEquipment"] == ["平板训练凳"]
        and row("1412")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce step box and flat bench supports cleanly",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 115 avoids hold triggers and activates unilateral perSide pacing on 1395, 1410, 1413, 1416, and 1417",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in calf_ids | glute_ids)
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in forearm_ids)
        and row("1413")["shoulder"] == "MEDIUM" and row("1413")["lower_back"] == "NONE" and row("1413")["knee"] == "NONE",
        "Joint stress screening reflects lower leg, upper leg, forearm, and upper arm loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="稳固踏台|平板训练凳|史密斯机|弹力带|杠铃|绳索|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND FIFTEEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
