#!/usr/bin/env python3
"""Batch fifty-eight candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3318", "3240", "3327", "3241", "3360", "3541", "3361", "3542", "3418", "3545"]
per_side_ids = {"3361", "3545"}
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
        row("3318")["primary"] == ["心肺系统", "腹斜肌"]
        and all(row(x)["primary"] == ["小腿肌"] for x in ["3240", "3241"])
        and all(row(x)["primary"] == ["胸肌"] for x in ["3327", "3545"])
        and row("3360")["primary"] == ["心肺系统", "核心肌群"]
        and row("3541")["primary"] == ["上背"]
        and row("3361")["primary"] == ["心肺系统", "股四头肌"]
        and row("3542")["primary"] == ["三角肌"]
        and row("3418")["primary"] == ["背阔肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["墙面", "瑜伽球"] and row(x)["safeWithRequiredEquipment"] and not row(x)["available"]["哑铃"] for x in ["3240", "3241"])
        and all(row(x)["requiredEquipment"] == ["上斜训练凳"] and row(x)["available"]["哑铃|上斜训练凳"] and not row(x)["available"]["哑铃"] for x in ["3541", "3542", "3545"])
        and row("3418")["requiredEquipment"] == ["单杠"]
        and row("3418")["available"]["单杠"]
        and not row("3418")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] for x in ["3318", "3327", "3360", "3361"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 58 avoids hold triggers and configures unilateral skater hops and alternate press cleanly",
    )
    check(
        all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" for x in ["3318", "3240", "3241", "3360", "3361"])
        and all(row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["3541", "3418"])
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["3327", "3542", "3545"]),
        "Joint stress screening reflects cardio/calf knee load, back/lat low-back pull stress, and chest/shoulder safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|单杠|上斜训练凳|墙面|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-EIGHT INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
