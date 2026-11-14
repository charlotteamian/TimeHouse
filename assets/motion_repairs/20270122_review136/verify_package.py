#!/usr/bin/env python3
"""Verify Final Milestone Batch 136 (1.2.140, Batches 135-136, 待核逻辑 == 0) package against ledger and source baseline."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import zipfile

B = Path(__file__).resolve().parent
R = B.parents[2]
O = R / "build/review136-20270122"
O.mkdir(parents=True, exist_ok=True)
result = json.loads((B / "review-result.json").read_text(encoding="utf-8"))
apk = R / "build/timehouse-debug.apk"
sha = lambda b: hashlib.sha256(b).hexdigest()

batches = ["20270121_review135", "20270122_review136"]
inspected_group = []
for mb in batches:
    mr = json.loads((R / "assets/motion_repairs" / mb / "review-result.json").read_text(encoding="utf-8"))
    inspected_group.extend(mr["inspected"])

with zipfile.ZipFile(apk) as a:
    assert a.testzip() is None
    for name in ["exercises_1324.json", "exercise_reviews.json"]:
        assert a.read("assets/" + name) == (R / "app/src/main/assets" / name).read_bytes()
    d = json.loads(a.read("assets/exercises_1324.json"))
    ld = json.loads(a.read("assets/exercise_reviews.json"))
    pd = json.loads((B / "before/exercises_1324.json").read_bytes())
    pd_group = json.loads((R / "assets/motion_repairs/20270121_review135/before/exercises_1324.json").read_bytes())
    assert ld["dataset_sha256"] == sha(a.read("assets/exercises_1324.json"))
    old = {e["id"]: e for e in pd["exercises"]}
    old_group = {e["id"]: e for e in pd_group["exercises"]}
    rows = {e["id"]: e for e in d["exercises"]}
    changes = [x for x in rows if rows[x] != old[x]]
    group_changes = [x for x in rows if rows[x] != old_group[x]]
    assert changes == [] and group_changes == []
    for e in ld["reviewed"]:
        media = rows[e["id"].removeprefix("dataset_1324_")]["media"].removeprefix("raw:") + ".webp"
        path = "res/raw/" + media
        assert sha(a.read(path)) == e["media_sha256"] and a.read(path) == (R / "app/src/main/res/raw" / media).read_bytes()
    reviewed_ids = {r["id"] for r in ld["reviewed"]}
    pending_map = {r["id"]: r["note"] for r in ld["pending"]}
    assert len(ld["reviewed"]) == 142
    assert len(ld["pending"]) == 1210
    assert not (reviewed_ids & set(pending_map))
    assert all(eid in pending_map and pending_map[eid].startswith("待修图 · ") for eid in inspected_group)

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
assert "versionCode='2027012201'" in badging and "versionName='1.2.140'" in badging

summary = dict(
    version="1.2.140",
    version_code=2027012201,
    sha256=sha(apk.read_bytes()),
    bytes=apk.stat().st_size,
    changed_dataset_ids=group_changes,
    batch136_changed_dataset_ids=changes,
    inspected_seed_ids_batches_135_136=len(inspected_group),
    changed_raw_assets=[],
    changed_app_code=code_changes,
    reviewed=len(ld["reviewed"]),
    unreviewed=1355 - len(ld["reviewed"]),
    pending_ledger=len(ld["pending"]),
    generated_images_imported=0,
    apk_integrity="passed",
    dataset_and_review_hashes="passed",
    signature_verified=True,
    signer_sha256=signer,
)
(O / "package-verification.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
