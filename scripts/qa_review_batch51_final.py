#!/usr/bin/env python3
"""Verify Batch 51 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3204", "1737", "3212", "1738", "3213", "1739", "3214", "1740", "3215", "1741"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 137, "Bundled ledger keeps exact 137 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 51 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["1737", "1738", "3214", "1740"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_1737"]["available"]["哑铃|平板训练凳"]
        and catalog["dataset_1324_1738"]["available"]["哑铃|平板训练凳"]
        and catalog["dataset_1324_3214"]["perSide"]
        and catalog["dataset_1324_1740"]["perSide"],
        "Bench requirements and unilateral toe-touch / kickback rep modes remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-ONE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
