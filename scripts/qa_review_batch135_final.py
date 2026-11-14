#!/usr/bin/env python3
"""Verify Batch 135 deferred SeedExercises cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = [
    "exercise_lat_pulldown",
    "exercise_band_row",
    "exercise_one_arm_dumbbell_row",
    "exercise_seated_row",
    "exercise_band_pulldown",
    "exercise_bent_over_barbell_row",
    "exercise_face_pull",
    "exercise_wall_pushup",
    "exercise_incline_pushup",
    "exercise_dumbbell_bench_press",
    "exercise_seated_chest_press",
    "exercise_seated_shoulder_press",
    "exercise_band_external_rotation",
    "exercise_sit_to_stand",
]
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])

stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any(eid in known for eid in inspected), "All 14 deferred Batch 135 SeedExercises entries stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join(inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not any(catalog[eid]["isHold"] for eid in inspected)
        and catalog["exercise_one_arm_dumbbell_row"]["perSide"]
        and not catalog["exercise_seated_shoulder_press"]["safeSevereShoulder"],
        "Batch 135 SeedExercises pacing and shoulder safety checks remain consistent after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND THIRTY-FIVE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
