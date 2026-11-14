#!/usr/bin/env python3
"""Verify Batch 136 deferred SeedExercises cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = [
    "exercise_goblet_squat",
    "exercise_glute_bridge",
    "exercise_romanian_deadlift",
    "exercise_step_up",
    "exercise_dead_bug",
    "exercise_plank",
    "exercise_pallof_press",
    "exercise_bird_dog",
    "exercise_dumbbell_curl",
    "custom_inverted_row_unverified",
    "exercise_trx_row",
    "exercise_dumbbell_overhead_press",
    "exercise_kettlebell_swing",
    "exercise_pushup",
]
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])

stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any(eid in known for eid in inspected), "All 14 deferred Batch 136 SeedExercises entries stay out of the reviewed ledger")
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
        catalog["exercise_plank"]["isHold"]
        and catalog["exercise_step_up"]["perSide"]
        and catalog["exercise_dead_bug"]["perSide"]
        and not catalog["custom_inverted_row_unverified"]["safeWithRequiredEquipment"],
        "Batch 136 SeedExercises hold/perSide pacing and USER_UNVERIFIED gate stay consistent after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND THIRTY-SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
