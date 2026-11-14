#!/usr/bin/env python3
"""Batch twenty-seven candidates: verify all ten stay unreviewed while metadata/supports update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0815", "0409", "0816", "0410", "0817", "0411", "0826", "0413", "0858", "0414"]
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
        all(row(x)["primary"] == ["肱三头肌"] for x in ["0815", "0816", "0817"])
        and row("0409")["primary"] == ["小腿肌"]
        and all(row(x)["primary"] == ["股四头肌"] for x in ["0410", "0411", "0413"])
        and row("0826")["primary"] == ["腹肌"]
        and row("0858")["primary"] == ["心肺系统"]
        and row("0414")["primary"] == ["三角肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("0815")["requiredEquipment"] == ["平板训练凳"]
        and row("0815")["available"]["平板训练凳"]
        and not row("0815")["available"]["自重"]
        and row("0409")["requiredEquipment"] == ["稳固踏台", "墙面"]
        and not row("0409")["available"]["哑铃"]
        and row("0410")["requiredEquipment"] == ["平板训练凳"]
        and row("0410")["available"]["哑铃|平板训练凳"]
        and not row("0410")["available"]["哑铃"]
        and row("0826")["requiredEquipment"] == ["单杠"]
        and row("0826")["available"]["单杠"]
        and not row("0826")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] for x in ["0816", "0817", "0411", "0413", "0858", "0414"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        all(row(x)["perSide"] and not row(x)["isHold"] for x in ["0409", "0410", "0817", "0411"])
        and all(not row(x)["perSide"] and not row(x)["isHold"] for x in ["0815", "0816", "0826", "0413", "0858", "0414"]),
        "Single-leg and single-arm entries count per side without triggering isometric hold rules",
    )
    check(
        all(row(x)["knee"] in ("LOW", "MEDIUM") for x in ["0409", "0410", "0411", "0413", "0858"])
        and row("0414")["shoulder"] == "MEDIUM"
        and row("0815")["shoulder"] in ("LOW", "MEDIUM"),
        "Joint stress screening reflects single-leg squat/calf, sprint, bench dip, and overhead press loads",
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
            "perSide": xid in ("0409", "0410", "0817", "0411"),
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳|稳固踏台|墙面|单杠", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH TWENTY-SEVEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
