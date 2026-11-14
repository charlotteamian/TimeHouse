#!/usr/bin/env python3
"""Newly reviewed Batch 47 curls (1671, 1673) enforce required equipment and start unilaterally."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
new = ["1671", "1673"]
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
    check(len(known) == 136 and all("dataset_1324_" + x in known for x in new), "New entries 1671 and 1673 enter the final bundled 136-item ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", "dataset_1324_1671,dataset_1324_1673",
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        all(catalog["dataset_1324_" + x]["safeWithRequiredEquipment"] and catalog["dataset_1324_" + x]["perSide"] for x in new)
        and catalog["dataset_1324_1671"]["available"]["哑铃"]
        and not catalog["dataset_1324_1671"]["available"]["自重"],
        "Loaded standing hammer curl and ball preacher curl pass safely as unilateral biceps exercises",
    )

    # Verify 1671 starts unilaterally with dumbbells (and does not require extra support gear)
    item1 = {"id": "dataset_1324_1671", "sets": 1, "reps": "12", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": True, "tempo": 3, "reason": "", "restAfter": 0}
    w1 = {"version": 1, "title": "新复核动作开练验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item1]}
    state_with(equipment="哑铃", workoutDraft=json.dumps(w1, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_1671" and draft()["items"][0]["perSide"], names["1671"] + " enters unilateral training with dumbbells")
    snapshot("1671-session")

    # Verify 1673 requires exercise ball
    item2 = {"id": "dataset_1324_1673", "sets": 1, "reps": "12", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": True, "tempo": 3, "reason": "", "restAfter": 0}
    w2 = {"version": 1, "title": "新复核动作开练验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item2]}
    state_with(equipment="哑铃", workoutDraft=json.dumps(w2, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check("还缺少必需器械" in texts() and not draft()["active"], names["1673"] + " cannot start without required exercise ball")

    state_with(equipment="哑铃|瑜伽球", workoutDraft=json.dumps(w2, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_1673" and draft()["items"][0]["perSide"], names["1673"] + " enters unilateral training with exercise ball")
    snapshot("1673-session")

    print("ALL BATCH FORTY-SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
