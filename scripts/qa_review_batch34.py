#!/usr/bin/env python3
"""Batch thirty-four candidates: verify all ten stay unreviewed while metadata/supports update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1401", "1277", "1403", "1278", "1405", "1279", "1407", "1280", "1418", "1281"]
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
        all(row(x)["primary"] == ["背阔肌"] for x in ["1401", "1405"])
        and all(row(x)["primary"] == ["胸肌"] for x in ["1277", "1278", "1279", "1280", "1281"])
        and row("1403")["primary"] == ["肩胛提肌"]
        and row("1407")["primary"] == ["小腿肌"]
        and row("1418")["primary"] == ["臀肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("1401")["requiredEquipment"] == ["单杠"] and row("1401")["available"]["单杠"] and not row("1401")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] and row(x)["safeWithRequiredEquipment"] and not row(x)["available"]["哑铃"] for x in ["1277", "1280"])
        and row("1278")["requiredEquipment"] == ["上斜训练凳", "瑜伽球"] and row("1278")["safeWithRequiredEquipment"] and not row("1278")["available"]["哑铃|上斜训练凳"]
        and all(row(x)["requiredEquipment"] == ["上斜训练凳"] and row(x)["available"]["哑铃|上斜训练凳"] and not row(x)["available"]["哑铃"] for x in ["1279", "1281"])
        and row("1407")["requiredEquipment"] == ["墙面"] and row("1407")["available"]["墙面"] and not row("1407")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["available"]["自重"] for x in ["1403", "1405", "1418"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in ["1403", "1279", "1407", "1280", "1418", "1281"])
        and not any(row(x)["perSide"] for x in ["1401", "1277", "1278", "1405"]),
        "Batch 34 unilateral triggers match neck side stretch, one-arm incline/ball drills, wall calf stretch, and squat-to-knee-hug",
    )
    check(
        row("1401")["shoulder"] == "MEDIUM"
        and all(row(x)["shoulder"] == "MEDIUM" for x in ["1277", "1278", "1279", "1280", "1281"])
        and all(row(x)["knee"] == "MEDIUM" for x in ["1407", "1418"])
        and all(row(x)["lower_back"] == "LOW" for x in ["1403", "1405"]),
        "Joint stress screening reflects muscle-up, incline/fly shoulder loads, calf/squat knee loads, and standing posture",
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
            "perSide": xid in ("1403", "1279", "1407", "1280", "1418", "1281"),
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|单杠|墙面|上斜训练凳|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH THIRTY-FOUR INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
