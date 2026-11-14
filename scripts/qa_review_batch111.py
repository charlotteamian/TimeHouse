#!/usr/bin/env python3
"""Batch one hundred and eleven candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1325", "1332", "1333", "1334", "1335", "1336", "1338", "1339", "1341", "1342"]
per_side_ids = {"1332", "1339", "1342"}
bilateral_ids = set(inspected) - per_side_ids
lats_ids = {"1325", "1332", "1339", "1341", "1342"}
spine_ids = {"1333", "1334", "1335", "1336", "1338"}
wall_ids = {"1333", "1334", "1335"}
ball_support_ids = {"1332", "1339"}
no_support_ids = {"1325", "1336", "1338", "1341", "1342"}
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
        all(row(x)["primary"] == ["背阔肌"] for x in lats_ids)
        and all(row(x)["primary"] == ["脊柱"] for x in spine_ids),
        "Primary muscle groups match lats and spine across all ten back entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["墙面"] for x in wall_ids)
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] for x in ball_support_ids)
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce exact wall and stability ball support rules",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 111 avoids hold triggers and activates unilateral perSide pacing on 1332, 1339, and 1342",
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
            "perSide": xid in per_side_ids,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="墙面|瑜伽球|哑铃|绳索", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND ELEVEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
