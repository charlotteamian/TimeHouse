#!/usr/bin/env python3
"""Batch sixty-four candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0018", "0019", "0022", "0023", "0024", "0025", "0026", "0027", "0028", "0029"]
per_side_ids = {"0023"}
bench_ids = {"0022", "0024", "0025", "0026"}
towel_ids = {"0018"}
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
        all(row(x)["primary"] == ["肱三头肌"] for x in ["0018", "0019"])
        and row("0022")["primary"] == ["背阔肌"]
        and row("0023")["primary"] == ["肱二头肌"]
        and all(row(x)["primary"] == ["股四头肌"] for x in ["0024", "0026", "0028"])
        and row("0025")["primary"] == ["胸肌"]
        and row("0027")["primary"] == ["上背"]
        and row("0029")["primary"] == ["臀肌", "股四头肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["safeWithRequiredEquipment"] for x in bench_ids)
        and all(row(x)["requiredEquipment"] == ["毛巾"] and row(x)["safeWithRequiredEquipment"] for x in towel_ids)
        and all(row(x)["requiredEquipment"] == [] for x in inspected if x not in bench_ids and x not in towel_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 64 avoids hold triggers and configures unilateral alternating curls cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" for x in ["0018", "0019", "0023", "0025"])
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" for x in ["0022", "0027"])
        and all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" for x in ["0024", "0026", "0028", "0029"]),
        "Joint stress screening reflects shoulder and back loading for presses/rows and lower-body knee stress for squats",
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
        state_with(reviewedOnlyV1=False, equipment="杠铃|平板训练凳|辅助器械|毛巾", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SIXTY-FOUR INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
