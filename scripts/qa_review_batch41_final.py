#!/usr/bin/env python3
"""Newly reviewed Batch 41 exercises (1764, 1624) require bar / flat bench and start bilaterally."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
new = ["1764", "1624"]
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
    check(len(known) == 130 and all("dataset_1324_" + x in known for x in new), "New entries 1764 and 1624 enter the final bundled 130-item ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", "dataset_1324_1764,dataset_1324_1624",
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        all(catalog["dataset_1324_" + x]["safeWithRequiredEquipment"] and not catalog["dataset_1324_" + x]["perSide"] for x in new),
        "Loaded hanging leg hip raise and reverse bench press pass safely as bilateral exercises",
    )

    for xid, miss_eq, good_eq in [
        ("1764", "自重", "自重|单杠"),
        ("1624", "哑铃", "哑铃|平板训练凳"),
    ]:
        item = {"id": "dataset_1324_" + xid, "sets": 1, "reps": "12", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": False, "tempo": 3, "reason": "", "restAfter": 0}
        workout = {"version": 1, "title": "新复核动作开练验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}

        state_with(equipment=miss_eq, workoutDraft=json.dumps(workout, ensure_ascii=False))
        tap("查看课程 →")
        tap("开始这一练 →")
        check("还缺少必需器械" in texts() and not draft()["active"], names[xid] + " cannot start without required supporting equipment")

        state_with(equipment=good_eq, workoutDraft=json.dumps(workout, ensure_ascii=False))
        tap("查看课程 →")
        tap("开始这一练 →")
        check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_" + xid and not draft()["items"][0]["perSide"], names[xid] + " enters bilateral training with required equipment")
        snapshot(xid + "-session")

    print("ALL BATCH FORTY-ONE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
