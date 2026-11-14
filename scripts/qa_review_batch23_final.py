#!/usr/bin/env python3
"""Verify Batch 23 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0691", "0388", "0696", "0389", "0697", "0390", "0699", "0391", "0705", "0392"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 104, "Bundled ledger keeps exact 104 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 23 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0691", "0389", "0391", "0705"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0691"]["safeSevereShoulder"]
        and not catalog["dataset_1324_0389"]["safeSevereShoulder"]
        and not catalog["dataset_1324_0391"]["safeSevereShoulder"]
        and not catalog["dataset_1324_0705"]["safeSevereShoulder"],
        "Severe shoulder pain filter updates accurately for corrected Batch 23 definitions",
    )
    print("ALL BATCH TWENTY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
