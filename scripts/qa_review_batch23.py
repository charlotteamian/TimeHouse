#!/usr/bin/env python3
"""Batch twenty-three candidates: verify all ten stay unreviewed while metadata/supports update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0691", "0388", "0696", "0389", "0697", "0390", "0699", "0391", "0705", "0392"]
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
        all(row(x)["primary"] == ["腹肌"] for x in ["0691", "0705"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["0388", "0392"])
        and all(row(x)["primary"] == ["腘绳肌"] for x in ["0696", "0697"])
        and row("0389")["primary"] == ["肱三头肌"]
        and all(row(x)["primary"] == ["肱二头肌"] for x in ["0390", "0391"])
        and row("0699")["primary"] == ["胸肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("0691")["requiredEquipment"] == ["墙面"]
        and row("0691")["available"]["墙面"]
        and not row("0691")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["available"]["哑铃|平板训练凳"] and not row(x)["available"]["哑铃"] for x in ["0388", "0389", "0392"])
        and row("0390")["requiredEquipment"] == ["瑜伽球"]
        and not row("0390")["available"]["哑铃"]
        and row("0391")["requiredEquipment"] == ["直立靠背训练凳"]
        and row("0391")["available"]["哑铃|直立靠背训练凳"]
        and not row("0391")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] for x in ["0696", "0697", "0699", "0705"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        row("0705")["isHold"]
        and row("0705")["perSide"]
        and not any(row(x)["isHold"] or row(x)["perSide"] for x in inspected if x != "0705"),
        "Wall side crunch 0691 stays repetition-counted while unilateral side bridge 0705 uses isometric per-side hold",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" for x in ["0388", "0389", "0390", "0699", "0391", "0705", "0392"])
        and all(row(x)["lower_back"] == "MEDIUM" for x in ["0388", "0389", "0699"]),
        "Joint stress screening reflects overhead extension/press, high plank, and bench work",
    )

    for xid in inspected:
        item = {"id": "dataset_1324_" + xid, "sets": 1, "reps": "8", "rpe": "7", "rest": 30, "kind": "HOLD" if xid == "0705" else "REPS", "hold": 25 if xid == "0705" else 0, "perSide": xid == "0705", "tempo": 3, "reason": "", "restAfter": 0}
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|墙面|平板训练凳|直立靠背训练凳|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH TWENTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
