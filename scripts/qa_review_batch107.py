#!/usr/bin/env python3
"""Batch one hundred and seven candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1257", "1258", "1259", "1260", "1261", "1262", "1263", "1264", "1265", "1266"]
per_side_ids = {"1260", "1262", "1263", "1264", "1265", "1266"}
bilateral_ids = set(inspected) - per_side_ids
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
        all(row(x)["primary"] == ["胸肌"] for x in inspected),
        "Primary muscle groups match pectorals for all ten inspected chest entries",
    )
    check(
        row("1258")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == ["上斜训练凳"] for x in ["1257", "1265"])
        and all(row(x)["requiredEquipment"] == ["带勾脚的下斜训练凳"] for x in ["1260", "1261", "1262"])
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] for x in ["1263", "1264", "1266"])
        and row("1259")["requiredEquipment"] == [] and row("1259")["safeWithRequiredEquipment"],
        "All ten inspected entries enforce exact required supporting equipment across flat, incline, decline benches and stability balls",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 107 avoids hold triggers and configures unilateral and bilateral chest press and fly pacing cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in inspected),
        "Joint stress screening reflects conservative shoulder loading for all ten chest press, fly, and stretch entries",
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
        state_with(reviewedOnlyV1=False, equipment="杠铃|平板训练凳|上斜训练凳|带勾脚的下斜训练凳|瑜伽球|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND SEVEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
