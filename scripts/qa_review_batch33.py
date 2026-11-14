#!/usr/bin/env python3
"""Batch thirty-three candidates: catalog semantics, required supports, real loop and review gate."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageChops, ImageOps

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

new = ["0864", "1390"]
inspected = ["1387", "0863", "1390", "0864", "1397", "1201", "1398", "1274", "1399", "1276"]
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
        all(row(x)["primary"] == ["小腿肌"] for x in ["1387", "1390", "1397", "1398"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["0863", "0864"])
        and row("1201")["primary"] == ["心肺系统"]
        and all(row(x)["primary"] == ["胸肌"] for x in ["1274", "1276"])
        and row("1399")["primary"] == ["肱三头肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["墙面"] and row(x)["available"]["墙面"] and not row(x)["available"]["自重"] for x in ["1387", "1398"])
        and row("0863")["requiredEquipment"] == ["平板训练凳"] and row("0863")["available"]["哑铃|平板训练凳"] and not row("0863")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["available"]["平板训练凳"] and not row(x)["available"]["自重"] for x in ["1390", "1399"])
        and row("1276")["requiredEquipment"] == ["带勾脚的下斜训练凳"] and row("1276")["safeWithRequiredEquipment"] and not row("1276")["available"]["哑铃"] and not row("1276")["available"]["哑铃|下斜训练凳"]
        and row("1397")["requiredEquipment"] == [] and row("1397")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["available"]["哑铃"] and not row(x)["available"]["自重"] for x in ["0864", "1201", "1274"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in ["1387", "0863", "1390", "1398", "1276"])
        and not any(row(x)["perSide"] for x in ["0864", "1397", "1201", "1274", "1399"]),
        "Batch 33 triggers unilateral mode for single-leg/single-arm/unilateral drills while avoiding false holds",
    )
    check(
        all(row(x)["knee"] == "MEDIUM" for x in ["1387", "1390", "1397", "1398", "1201"])
        and all(row(x)["shoulder"] == "MEDIUM" for x in ["1274", "1276", "1399"])
        and row("0864")["lower_back"] == "LOW",
        "Joint stress screening reflects calf/cardio knee load, horizontal push shoulder load, and standing ER low back posture",
    )

    for xid in new:
        state_with(favorites="dataset_1324_" + xid)
        tap("动作库")
        tap("已标心")
        tap(names[xid])
        check("暂停示范" in texts() and any("未复核" in s for s in texts()), names[xid] + " plays while retaining its unreviewed label")
        snapshot(xid + "-detail")
        node = next(n for n in ui().iter("node") if n.get("class") == "android.widget.ImageView")
        bounds = tuple(map(int, re.findall(r"-?\d+", node.get("bounds"))))
        frames = []
        for i in range(12):
            im = Image.open(BytesIO(adb("exec-out", "screencap", "-p"))).convert("RGB").crop(bounds)
            im.save(out / f"{xid}-play-{i}.png")
            frames.append(im)
            time.sleep(0.28)
        check(any(ImageChops.difference(frames[0], im).getbbox() for im in frames[1:]), names[xid] + " changes poses during captured Android loops")
        frames[0].save(out / f"{xid}-android-loop.gif", save_all=True, append_images=frames[1:], duration=400, loop=0)
        sheet = Image.new("RGB", (1200, 900), "white")
        for i, im in enumerate(frames):
            sheet.paste(ImageOps.pad(im, (300, 300), color="white"), ((i % 4) * 300, (i // 4) * 300))
        sheet.save(out / f"{xid}-playback-contact.jpg", quality=92)
        item = {"id": "dataset_1324_" + xid, "sets": 1, "reps": "8", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": xid == "1390", "tempo": 3, "reason": "", "restAfter": 0}
        workout = {"version": 1, "title": "候选门控核查", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " cannot bypass 1.2.14 mandatory review gate")

    decoded = adb("shell", "am", "instrument", "-w", "-e", "media", "dataset_motion_0864,dataset_motion_1390", "com.restartday.fitness.qa/.UiSnapshot").decode()
    check("decodedAnimations=2" in decoded, "Android decodes both Batch 33 candidates as animations")
    print("ALL BATCH THIRTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
