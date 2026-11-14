#!/usr/bin/env python3
"""Batch thirty-six candidates: verify all ten stay unreviewed while metadata/supports update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1429", "1287", "1430", "1288", "1460", "1289", "1466", "1290", "1467", "1291"]
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
        row("1429")["primary"] == ["背阔肌"]
        and all(row(x)["primary"] == ["胸肌"] for x in ["1287", "1430", "1288", "1289", "1290", "1291"])
        and all(row(x)["primary"] == ["臀肌"] for x in ["1460", "1466"])
        and row("1467")["primary"] == ["肱三头肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("1429")["requiredEquipment"] == ["单杠"] and row("1429")["available"]["单杠"] and not row("1429")["available"]["自重"]
        and row("1287")["requiredEquipment"] == ["带勾脚的下斜训练凳"] and row("1287")["safeWithRequiredEquipment"] and not row("1287")["available"]["哑铃"]
        and row("1430")["requiredEquipment"] == ["双杠"] and row("1430")["available"]["双杠"] and not row("1430")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] and row(x)["safeWithRequiredEquipment"] and not row(x)["available"]["哑铃"] for x in ["1288", "1290", "1291"])
        and row("1289")["requiredEquipment"] == ["上斜训练凳"] and row("1289")["available"]["哑铃|上斜训练凳"] and not row("1289")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["available"]["自重"] for x in ["1460", "1466", "1467"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in ["1287", "1288", "1460", "1289", "1466", "1290", "1291"])
        and not any(row(x)["perSide"] for x in ["1429", "1430", "1467"]),
        "Batch 36 avoids false hold triggers on forearm push-up and dip while triggering unilateral counts cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" for x in ["1429", "1287", "1430", "1288", "1289", "1290", "1291"])
        and row("1460")["knee"] == "MEDIUM"
        and row("1466")["lower_back"] == "MEDIUM"
        and row("1291")["lower_back"] == "MEDIUM",
        "Joint stress screening reflects pull-up, dip, overhead ball press/pullover, lunge, and hip twist bridge loads",
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
            "perSide": xid in ("1287", "1288", "1460", "1289", "1466", "1290", "1291"),
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|单杠|双杠|上斜训练凳|带勾脚的下斜训练凳|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH THIRTY-SIX INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
