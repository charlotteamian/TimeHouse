#!/usr/bin/env python3
"""Verify Batch 118 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1479", "1496", "1545", "1559", "1560", "1564", "1582", "1599", "1614", "1615"]
ham_ids = {"1560", "1582", "1599"}
glute_ids = {"1545", "1559"}
bicep_ids = {"1614", "1615"}
per_side_ids = {"1559", "1564", "1582"}
bilateral_ids = set(inspected) - per_side_ids
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 118 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not any(catalog["dataset_1324_" + x]["isHold"] for x in inspected)
        and all(catalog["dataset_1324_" + x]["perSide"] for x in per_side_ids)
        and all(not catalog["dataset_1324_" + x]["perSide"] for x in bilateral_ids)
        and catalog["dataset_1324_1479"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_1496"]["primary"] == ["腹肌"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["臀肌"] for x in glute_ids)
        and all(catalog["dataset_1324_" + x]["primary"] == ["腘绳肌"] for x in ham_ids)
        and catalog["dataset_1324_1564"]["primary"] == ["股四头肌"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["肱二头肌"] for x in bicep_ids),
        "Unilateral pacing and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND EIGHTEEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
