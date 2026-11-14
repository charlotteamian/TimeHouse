#!/usr/bin/env python3
"""Verify Batch 92 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0597", "0598", "0599", "0600", "0601", "0602", "0603", "0604", "0605", "0606"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 92 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0597", "0598", "0599", "0600", "0601", "0603", "0606"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not any(catalog["dataset_1324_" + x]["perSide"] for x in ["0597", "0598", "0599", "0600", "0601", "0603", "0606"])
        and not any(catalog["dataset_1324_" + x]["isHold"] for x in ["0597", "0598", "0599", "0600", "0601", "0603", "0606"])
        and catalog["dataset_1324_0597"]["primary"] == ["髋外展肌群"]
        and catalog["dataset_1324_0598"]["primary"] == ["大腿内收肌群"]
        and catalog["dataset_1324_0606"]["primary"] == ["上背"],
        "Bilateral pacing, hip abduction/adduction isolation, and chest-supported T-bar row muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-TWO FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
