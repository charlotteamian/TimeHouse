#!/usr/bin/env python3
"""Verify Batch 59 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3419", "3546", "3420", "3547", "3433", "3548", "3470", "3560", "3523", "3635"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 59 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3419", "3546", "3420", "3547", "3523", "3635"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3419"]["isHold"]
        and catalog["dataset_1324_3420"]["isHold"]
        and catalog["dataset_1324_3546"]["perSide"]
        and catalog["dataset_1324_3546"]["available"]["哑铃|平板训练凳"]
        and catalog["dataset_1324_3547"]["available"]["哑铃|直立靠背训练凳"]
        and catalog["dataset_1324_3523"]["available"]["平板训练凳"]
        and catalog["dataset_1324_3635"]["perSide"],
        "Required benches, L/V-sit holds, and unilateral press/lunge modes remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-NINE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
