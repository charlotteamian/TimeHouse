#!/usr/bin/env python3
"""Verify Batch 40 final package against registered review evidence and app source baseline."""
from pathlib import Path
import json
import hashlib
import zipfile
import subprocess
import os
import re

B = Path(__file__).resolve().parent
R = B.parents[2]
O = R / "build/review40-20261018"
O.mkdir(parents=True, exist_ok=True)
result = json.loads((B / "review-result.json").read_text(encoding="utf-8"))
apk = R / "build/timehouse-debug.apk"
sha = lambda b: hashlib.sha256(b).hexdigest()

with zipfile.ZipFile(apk) as a:
    assert a.testzip() is None
    for name in ["exercises_1324.json", "exercise_reviews.json"]:
        assert a.read("assets/" + name) == (R / "app/src/main/assets" / name).read_bytes()
    d = json.loads(a.read("assets/exercises_1324.json"))
    ld = json.loads(a.read("assets/exercise_reviews.json"))
    pd = json.loads((B / "before/exercises_1324.json").read_bytes())
    assert ld["dataset_sha256"] == sha(a.read("assets/exercises_1324.json"))
    old = {e["id"]: e for e in pd["exercises"]}
    rows = {e["id"]: e for e in d["exercises"]}
    changes = [x for x in rows if rows[x] != old[x]]
    assert set(changes) == set(result["definition_updates"])
    for e in ld["reviewed"]:
        media = rows[e["id"].removeprefix("dataset_1324_")]["media"].removeprefix("raw:") + ".webp"
        path = "res/raw/" + media
        assert sha(a.read(path)) == e["media_sha256"] and a.read(path) == (R / "app/src/main/res/raw" / media).read_bytes()
    assert len(ld["reviewed"]) == 128 and not ({r["id"] for r in ld["reviewed"]} & {r["id"] for r in ld["pending"]})

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
assert "versionCode='2026101801'" in badging and "versionName='1.2.45'" in badging

summary = dict(
    version="1.2.45",
    version_code=2026101801,
    sha256=sha(apk.read_bytes()),
    bytes=apk.stat().st_size,
    changed_dataset_ids=changes,
    changed_raw_assets=[f"res/raw/dataset_motion_{x}.webp" for x in result["registered_media"]],
    changed_app_code=code_changes,
    reviewed=128,
    unreviewed=1227,
    generated_images_imported=result["generated_images_imported"],
    apk_integrity="passed",
    dataset_and_review_hashes="passed",
    signature_verified=True,
    signer_sha256=signer,
)
(O / "package-verification.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
