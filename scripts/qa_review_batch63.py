#!/usr/bin/env python3
"""Batch sixty-three candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0007", "0009", "0010", "0011", "0012", "0013", "0014", "0015", "0016", "0017"]
per_side_ids = {"0007", "0012", "0014", "0016"}
bar_ids = {"0010", "0011"}
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
        row("0007")["primary"] == ["背阔肌"]
        and row("0009")["primary"] == ["胸肌"]
        and all(row(x)["primary"] == ["腹肌", "髋屈肌群"] for x in ["0010", "0011", "0013"])
        and all(row(x)["primary"] == ["腹肌", "腹斜肌"] for x in ["0012", "0014"])
        and all(row(x)["primary"] == ["背阔肌"] for x in ["0015", "0017"])
        and row("0016")["primary"] == ["腘绳肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["单杠"] and row(x)["safeWithRequiredEquipment"] for x in bar_ids)
        and all(not row(x)["available"]["自重"] for x in bar_ids)
        and all(row(x)["requiredEquipment"] == [] for x in inspected if x not in bar_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 63 avoids hold triggers and configures unilateral cable pulls, leg throws, twists, and curls cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" for x in ["0007", "0015", "0017"])
        and row("0009")["shoulder"] == "MEDIUM" and row("0009")["lower_back"] == "NONE"
        and all(row(x)["lower_back"] == "MEDIUM" and row(x)["shoulder"] == "NONE" for x in ["0010", "0011", "0012", "0013", "0014"])
        and row("0016")["knee"] == "MEDIUM" and row("0016")["lower_back"] == "NONE",
        "Joint stress screening reflects shoulder and back loading for pulls/dips and lower-body knee stress for curls",
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
        state_with(reviewedOnlyV1=False, equipment="自重|单杠|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SIXTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
