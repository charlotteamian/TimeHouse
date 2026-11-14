#!/usr/bin/env python3
"""Verify Milestone 1 (Batches 109-118) final package against registered review ledger and app source baseline."""
from pathlib import Path
import json
import hashlib
import zipfile
import subprocess
import os
import re

B = Path(__file__).resolve().parent
R = B.parents[2]
O = R / "build/review118-20270104"
O.mkdir(parents=True, exist_ok=True)
result = json.loads((B / "review-result.json").read_text(encoding="utf-8"))
apk = R / "build/timehouse-debug.apk"
sha = lambda b: hashlib.sha256(b).hexdigest()

milestone_batches = [
    "20261226_review109",
    "20261227_review110",
    "20261228_review111",
    "20261229_review112",
    "20261230_review113",
    "20261231_review114",
    "20270101_review115",
    "20270102_review116",
    "20270103_review117",
    "20270104_review118",
]

milestone_expected_updates = set()
milestone_registered_media = []
milestone_imported = 0
for mb in milestone_batches:
    mr = json.loads((R / "assets/motion_repairs" / mb / "review-result.json").read_text(encoding="utf-8"))
    milestone_expected_updates |= set(mr["definition_updates"])
    milestone_registered_media.extend(mr["registered_media"])
    milestone_imported += int(mr.get("generated_images_imported", 0))

with zipfile.ZipFile(apk) as a:
    assert a.testzip() is None
    for name in ["exercises_1324.json", "exercise_reviews.json"]:
        assert a.read("assets/" + name) == (R / "app/src/main/assets" / name).read_bytes()
    d = json.loads(a.read("assets/exercises_1324.json"))
    ld = json.loads(a.read("assets/exercise_reviews.json"))
    pd = json.loads((B / "before/exercises_1324.json").read_bytes())
    pd_milestone = json.loads((R / "assets/motion_repairs/20261226_review109/before/exercises_1324.json").read_bytes())
    assert ld["dataset_sha256"] == sha(a.read("assets/exercises_1324.json"))
    old = {e["id"]: e for e in pd["exercises"]}
    old_milestone = {e["id"]: e for e in pd_milestone["exercises"]}
    rows = {e["id"]: e for e in d["exercises"]}
    changes = [x for x in rows if rows[x] != old[x]]
    milestone_changes = [x for x in rows if rows[x] != old_milestone[x]]
    assert set(changes) == set(result["definition_updates"]), (set(changes), set(result["definition_updates"]))
    assert set(milestone_changes) == milestone_expected_updates, (set(milestone_changes) ^ milestone_expected_updates)
    for e in ld["reviewed"]:
        media = rows[e["id"].removeprefix("dataset_1324_")]["media"].removeprefix("raw:") + ".webp"
        path = "res/raw/" + media
        assert sha(a.read(path)) == e["media_sha256"] and a.read(path) == (R / "app/src/main/res/raw" / media).read_bytes()
    assert len(ld["reviewed"]) == 138 and not ({r["id"] for r in ld["reviewed"]} & {r["id"] for r in ld["pending"]})

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
assert "versionCode='2027010401'" in badging and "versionName='1.2.123'" in badging

summary = dict(
    version="1.2.123",
    version_code=2027010401,
    sha256=sha(apk.read_bytes()),
    bytes=apk.stat().st_size,
    changed_dataset_ids=milestone_changes,
    batch118_changed_dataset_ids=changes,
    changed_raw_assets=[f"res/raw/dataset_motion_{x}.webp" for x in milestone_registered_media],
    changed_app_code=code_changes,
    reviewed=len(ld["reviewed"]),
    unreviewed=1355 - len(ld["reviewed"]),
    pending_ledger=len(ld["pending"]),
    generated_images_imported=milestone_imported,
    apk_integrity="passed",
    dataset_and_review_hashes="passed",
    signature_verified=True,
    signer_sha256=signer,
)
(O / "package-verification.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
