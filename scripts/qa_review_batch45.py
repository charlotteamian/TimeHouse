#!/usr/bin/env python3
"""Batch forty-five candidates: catalog semantics, required supports, real loop and review gate."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageChops, ImageOps

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

new = ["1665"]
inspected = ["2363", "1661", "2398", "1662", "2400", "1663", "2429", "1664", "2462", "1665"]
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
        all(row(x)["primary"] == ["胸肌"] for x in ["2363", "2462"])
        and all(row(x)["primary"] == ["肱二头肌"] for x in ["1661", "1662", "1663", "1664", "1665"])
        and row("2398")["primary"] == ["肱三头肌"]
        and row("2400")["primary"] == ["腘绳肌"]
        and row("2429")["primary"] == ["腹肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("2363")["requiredEquipment"] == ["双杠"] and row("2363")["available"]["双杠"] and not row("2363")["available"]["自重"]
        and row("2462")["requiredEquipment"] == ["单杠"] and row("2462")["available"]["单杠"] and not row("2462")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["available"]["哑铃|平板训练凳"] and not row(x)["available"]["哑铃"] for x in ["1661", "1662", "1665"])
        and row("1663")["requiredEquipment"] == ["牧师凳"] and row("1663")["safeWithRequiredEquipment"] and not row("1663")["available"]["哑铃"]
        and row("2400")["requiredEquipment"] == ["平板训练凳", "龙门架绳索"] and row("2400")["safeWithRequiredEquipment"] and not row("2400")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] for x in ["2398", "2429", "1664"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in ["1663", "1665"])
        and not any(row(x)["perSide"] for x in ["2363", "1661", "2398", "1662", "2400", "2429", "1664", "2462"]),
        "Batch 45 avoids hold triggers while configuring unilateral/bilateral rep modes accurately",
    )
    check(
        row("2400")["knee"] == "MEDIUM"
        and row("1665")["knee"] == "NONE" and row("1665")["lower_back"] == "NONE",
        "Joint stress screening reflects leg-curl knee load and low axial stress on prone dumbbell curl",
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
        item = {"id": "dataset_1324_" + xid, "sets": 1, "reps": "12", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": True, "tempo": 3, "reason": "", "restAfter": 0}
        workout = {"version": 1, "title": "候选门控核查", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " cannot bypass 1.2.14 mandatory review gate")

    decoded = adb("shell", "am", "instrument", "-w", "-e", "media", "dataset_motion_1665", "com.restartday.fitness.qa/.UiSnapshot").decode()
    check("decodedAnimations=1" in decoded, "Android decodes candidate one-arm prone curl demonstration as an animation")
    print("ALL BATCH FORTY-FIVE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
