#!/usr/bin/env python3
"""Batch one hundred and twenty-five candidate (2138) & deferred items: semantics, supports, playback, and review gate."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageChops, ImageOps

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

new = ["2138"]
inspected = ["2138", "2139", "2141", "2142", "2144", "2186", "2187", "2202", "2203", "2204"]
chest_ids = {"2139", "2144", "2203"}
tricep_ids = {"2142", "2186", "2187"}
cardio_ids = {"2138", "2141"}
roller_ids = {"2202", "2203", "2204"}
no_support_ids = set(inspected) - {"2144", "2186", "2187"}
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
        all(row(x)["primary"] == ["心肺系统"] for x in cardio_ids)
        and all(row(x)["primary"] == ["胸肌"] for x in chest_ids)
        and all(row(x)["primary"] == ["肱三头肌"] for x in tricep_ids)
        and row("2202")["primary"] == ["臀肌"]
        and row("2204")["primary"] == ["腹肌"],
        "Primary muscle groups match cardio, chest, triceps, glutes, and abs across Batch 125",
    )
    check(
        row("2138")["equipment"] == ["动感单车"]
        and row("2139")["equipment"] == ["上肢功率车"]
        and row("2141")["equipment"] == ["椭圆机"]
        and row("2142")["equipment"] == ["滑雪训练机"]
        and all(row(x)["equipment"] == ["健腹轮 / 滚轮"] for x in roller_ids)
        and row("2144")["requiredEquipment"] == ["直立靠背训练凳"]
        and row("2186")["requiredEquipment"] == ["带勾脚的下斜训练凳"]
        and row("2187")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "Batch 125 enforces cardio machines, upright/decline/flat benches, and roller equipment accurately",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "All ten Batch 125 entries remain dynamic and bilateral",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in cardio_ids | {"2202"})
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in chest_ids | tricep_ids)
        and row("2204")["shoulder"] == "NONE" and row("2204")["lower_back"] == "MEDIUM" and row("2204")["knee"] == "NONE",
        "Joint stress screening reflects cardio, upper-body, glutes, and abs loadings accurately",
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

    for xid in inspected:
        item = {
            "id": "dataset_1324_" + xid,
            "sets": 1,
            "reps": "10",
            "rpe": "7",
            "rest": 30,
            "kind": "REPS",
            "hold": 0,
            "perSide": False,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "候选及暂缓门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="动感单车|上肢功率车|椭圆机|滑雪训练机|直立靠背训练凳|带勾脚的下斜训练凳|平板训练凳|健腹轮 / 滚轮|EZ 杠|杠铃", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    decoded = adb("shell", "am", "instrument", "-w", "-e", "media", "dataset_motion_2138", "com.restartday.fitness.qa/.UiSnapshot").decode()
    check("decodedAnimations=1" in decoded, "Android decodes Batch 125 candidate 2138 demonstration as animation")
    print("ALL BATCH ONE HUNDRED AND TWENTY-FIVE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
