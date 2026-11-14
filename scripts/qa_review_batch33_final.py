#!/usr/bin/env python3
"""Newly reviewed Batch 33 exercises (0864 upright ER, 1390 seated calf stretch) validation."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
new = ["0864", "1390"]
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
    check(len(known) == 123 and all("dataset_1324_" + x in known for x in new), "New entries 0864 and 1390 enter the final bundled 123-item ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", "dataset_1324_0864,dataset_1324_1390",
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0864"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1390"]["safeWithRequiredEquipment"],
        "Loaded 0864 and 1390 pass equipment safety gating",
    )

    item_864 = {"id": "dataset_1324_0864", "sets": 1, "reps": "10", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": False, "tempo": 3, "reason": "", "restAfter": 0}
    w864 = {"version": 1, "title": "新复核动作开练验证1", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item_864]}
    state_with(equipment="哑铃", workoutDraft=json.dumps(w864, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_0864", names["0864"] + " enters normal bilateral training with dumbbell")
    snapshot("0864-session")

    item_1390 = {"id": "dataset_1324_1390", "sets": 1, "reps": "8", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": True, "tempo": 3, "reason": "", "restAfter": 0}
    w1390 = {"version": 1, "title": "新复核动作开练验证2", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item_1390]}

    state_with(equipment="自重", workoutDraft=json.dumps(w1390, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check("还缺少必需器械" in texts() and not draft()["active"], names["1390"] + " cannot start without required flat bench")

    state_with(equipment="自重|平板训练凳", workoutDraft=json.dumps(w1390, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_1390" and draft()["items"][0]["perSide"], names["1390"] + " enters single-leg training with flat bench")
    snapshot("1390-session")

    print("ALL BATCH THIRTY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
