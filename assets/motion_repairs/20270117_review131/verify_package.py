#!/usr/bin/env python3
"""Verify Candidate Batch 131 (Batches 129-131, approving 3144) final package against review ledger and source baseline."""
from pathlib import Path
import json
import hashlib
import zipfile
import subprocess
import os
import re

B = Path(__file__).resolve().parent
R = B.parents[2]
O = R / "build/review131-20270117"
O.mkdir(parents=True, exist_ok=True)
result = json.loads((B / "review-result.json").read_text(encoding="utf-8"))
apk = R / "build/timehouse-debug.apk"
sha = lambda b: hashlib.sha256(b).hexdigest()

batches = ["20270115_review129", "20270116_review130", "20270117_review131"]
expected_updates = set()
registered_media = []
imported = 0
for mb in batches:
    mr = json.loads((R / "assets/motion_repairs" / mb / "review-result.json").read_text(encoding="utf-8"))
    expected_updates |= set(mr["definition_updates"])
    registered_media.extend(mr["registered_media"])
    imported += int(mr.get("generated_images_imported", 0))

with zipfile.ZipFile(apk) as a:
    assert a.testzip() is None
    for name in ["exercises_1324.json", "exercise_reviews.json"]:
        assert a.read("assets/" + name) == (R / "app/src/main/assets" / name).read_bytes()
    d = json.loads(a.read("assets/exercises_1324.json"))
    ld = json.loads(a.read("assets/exercise_reviews.json"))
    pd = json.loads((B / "before/exercises_1324.json").read_bytes())
    pd_group = json.loads((R / "assets/motion_repairs/20270115_review129/before/exercises_1324.json").read_bytes())
    assert ld["dataset_sha256"] == sha(a.read("assets/exercises_1324.json"))
    old = {e["id"]: e for e in pd["exercises"]}
    old_group = {e["id"]: e for e in pd_group["exercises"]}
    rows = {e["id"]: e for e in d["exercises"]}
    changes = [x for x in rows if rows[x] != old[x]]
    group_changes = [x for x in rows if rows[x] != old_group[x]]
    assert set(changes) == set(result["definition_updates"]), (set(changes), set(result["definition_updates"]))
    assert set(group_changes) == expected_updates, (set(group_changes) ^ expected_updates)
    for e in ld["reviewed"]:
        media = rows[e["id"].removeprefix("dataset_1324_")]["media"].removeprefix("raw:") + ".webp"
        path = "res/raw/" + media
        assert sha(a.read(path)) == e["media_sha256"] and a.read(path) == (R / "app/src/main/res/raw" / media).read_bytes()
    reviewed_ids = {r["id"] for r in ld["reviewed"]}
    assert len(ld["reviewed"]) == 141 and "dataset_1324_3144" in reviewed_ids and not (reviewed_ids & {r["id"] for r in ld["pending"]})

base = json.loads((B / "code-baseline.json").read_text(encoding="utf-8"))
code_changes = [p for p, h in base.items() if sha((R / p).read_bytes()) != h]
assert code_changes == [], code_changes

BT = Path("/Users/restartday/Library/Android/sdk/build-tools/36.1.0")
env = dict(os.environ, JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home")


def cert(path: Path):
    text = subprocess.check_output([str(BT / "apksigner"), "verify", "--print-certs", str(path)], env=env, text=True)
    return re.search(r"certificate SHA-256 digest: (\w+)", text).group(1), text


signer, sign = cert(apk)
(O / "signature.txt").write_text(sign, encoding="utf-8")
badging = subprocess.check_output([str(BT / "aapt2"), "dump", "badging", str(apk)], text=True)
(O / "apk-badging.txt").write_text(badging, encoding="utf-8")
assert "versionCode='2027011701'" in badging and "versionName='1.2.136'" in badging

summary = dict(
    version="1.2.136",
    version_code=2027011701,
    sha256=sha(apk.read_bytes()),
    bytes=apk.stat().st_size,
    changed_dataset_ids=group_changes,
    batch131_changed_dataset_ids=changes,
    changed_raw_assets=[f"res/raw/dataset_motion_{x}.webp" for x in registered_media],
    changed_app_code=code_changes,
    reviewed=len(ld["reviewed"]),
    unreviewed=1355 - len(ld["reviewed"]),
    pending_ledger=len(ld["pending"]),
    generated_images_imported=imported,
    apk_integrity="passed",
    dataset_and_review_hashes="passed",
    signature_verified=True,
    signer_sha256=signer,
)
(O / "package-verification.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
