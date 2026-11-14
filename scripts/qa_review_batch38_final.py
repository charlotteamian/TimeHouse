#!/usr/bin/env python3
"""Newly reviewed Batch 38 exercises (1331 incline row, 1380 seated single-leg calf raise) validation."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
new = ["1331", "1380"]
names = {
    e["id"]: e["name_zh"]
    for e in json.loads(Path("app/src/main/assets/exercises_1324.json").read_text())["exercises"]
}
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)


def tap(label):
    for attempt in range(6):
        for n in ui().iter("node"):
            if n.get("text") == label or n.get("content-desc") == label:
                x1, y1, x2, y2 = map(int, re.findall(r"-?\d+", n.get("bounds")))
                screen = re.findall(r"(\d+)x(\d+)", adb("shell", "wm", "size").decode())[-1]
                if 40 <= y1 < y2 <= int(screen[1]) - 20 and x2 > x1:
                    adb("shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
                    time.sleep(0.35)
                    return
        size = re.findall(r"(\d+)x(\d+)", adb("shell", "wm", "size").decode())[-1]
        width, height = map(int, size)
        adb("shell", "input", "swipe", str(width // 2), str(int(height * 0.72)),
            str(width // 2), str(int(height * 0.32)), "750")
        time.sleep(0.35)
    raise AssertionError("Missing UI control: " + label)


try:
    check(len(known) == 126 and all("dataset_1324_" + x in known for x in new), "New entries 1331 and 1380 enter the final bundled 126-item ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", "dataset_1324_1331,dataset_1324_1380",
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_1331"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1380"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1380"]["knee"] == "MEDIUM",
        "Loaded 1331 and 1380 pass safety and support requirements",
    )

    item_1331 = {"id": "dataset_1324_1331", "sets": 1, "reps": "10", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": False, "tempo": 3, "reason": "", "restAfter": 0}
    w1331 = {"version": 1, "title": "新复核动作开练验证1", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item_1331]}
    state_with(equipment="哑铃", workoutDraft=json.dumps(w1331, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check("还缺少必需器械" in texts() and not draft()["active"], names["1331"] + " cannot start without required incline bench")

    state_with(equipment="哑铃|上斜训练凳", workoutDraft=json.dumps(w1331, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_1331", names["1331"] + " enters normal bilateral training with incline bench")
    snapshot("1331-session")

    item_1380 = {"id": "dataset_1324_1380", "sets": 1, "reps": "12", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": True, "tempo": 3, "reason": "", "restAfter": 0}
    w1380 = {"version": 1, "title": "新复核动作开练验证2", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item_1380]}
    state_with(equipment="哑铃|平板训练凳", workoutDraft=json.dumps(w1380, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check("还缺少必需器械" in texts() and not draft()["active"], names["1380"] + " cannot start without required step platform")

    state_with(equipment="哑铃|平板训练凳|稳固踏台", workoutDraft=json.dumps(w1380, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_1380" and draft()["items"][0]["perSide"], names["1380"] + " enters single-leg training with flat bench and step")
    snapshot("1380-session")

    print("ALL BATCH THIRTY-EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
