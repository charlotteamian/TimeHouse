#!/usr/bin/env python3
"""Batch one hundred and ten candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1314", "1316", "1317", "1318", "1319", "1320", "1321", "1322", "1323", "1324"]
upper_back_ids = set(inspected) - {"1314", "1316"}
incline_ids = {"1317", "1318", "1322"}
no_support_ids = {"1319", "1320", "1321", "1323", "1324"}
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
        row("1314")["primary"] == ["脊柱"]
        and row("1316")["primary"] == ["背阔肌"]
        and all(row(x)["primary"] == ["上背"] for x in upper_back_ids),
        "Primary muscle groups match spine, lats, and upper back across all ten back entries",
    )
    check(
        row("1314")["requiredEquipment"] == ["墙面"]
        and row("1316")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == ["上斜训练凳"] for x in incline_ids)
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce exact wall, flat bench, and incline bench support rules",
    )
    check(
        not any(row(x)["isHold"] or row(x)["perSide"] for x in inspected),
        "All ten bilateral back exercises stay dynamic REPS with zero false hold or perSide triggers",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in inspected),
        "Joint stress screening reflects back category shoulder and lower back loading",
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
        state_with(reviewedOnlyV1=False, equipment="墙面|平板训练凳|上斜训练凳|瑜伽球|杠铃|绳索", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
