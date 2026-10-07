#!/usr/bin/env python3
"""Create the final priority-motion delivery only after every gate is complete."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH = "20260910_720"


def load_json(path: Path) -> object:
    if not path.exists():
        raise FileNotFoundError(f"Required release evidence is missing: {path.relative_to(ROOT)}")
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default=DEFAULT_BATCH)
    parser.add_argument("--domain-log", default="build/priority-motion-domain-tests.log")
    parser.add_argument("--build-log", default="build/priority-motion-build.log")
    parser.add_argument("--intensity-ui-log", default="build/qa-20260912-intensity-final.log")
    parser.add_argument("--display-ui-log", default="build/qa-20260912-display-rotation.log")
    parser.add_argument("--media-ui-log", default="build/qa-20260912-custom-media.log")
    args = parser.parse_args()

    batch = ROOT / "assets/motion_repairs" / args.batch
    prompts = load_json(batch / "prompts.json")
    reuse = load_json(batch / "reuse.json")
    exclusions = load_json(batch / "scope-exclusions.json")
    workflow = load_json(batch / "workflow.json")
    manifest = load_json(batch / "manifest.json")
    source_qa = load_json(batch / "source-qa.json")
    asset_qa = load_json(batch / "asset-qa.json")
    manual_review = load_json(batch / "manual-review.json")

    if len(prompts) != 716 or len(reuse) != 5 or len(exclusions) != 4:
        raise RuntimeError(
            "Scope drift: expected 716 new + 5 reuse + 4 explicit exclusions, "
            f"got {len(prompts)} + {len(reuse)} + {len(exclusions)}"
        )
    missing_sources = [row["id"] for row in prompts if not (batch / f"{row['id']}.png").exists()]
    if missing_sources:
        raise RuntimeError(f"Source batch is incomplete: {len(missing_sources)} missing")
    if workflow.get("status_counts", {}).get("generated") != 716:
        raise RuntimeError("workflow.json does not report 716 generated in-scope sources")

    manifest_ids = [str(row["id"]) for row in manifest]
    expected_ids = {str(row["id"]) for row in prompts} | set(reuse)
    if len(manifest_ids) != 721 or set(manifest_ids) != expected_ids:
        raise RuntimeError("Import manifest must cover exactly 721 unique in-scope dataset rows")

    source_results = source_qa.get("results", [])
    if len(source_results) != 716 or any(row["status"] == "missing" for row in source_results):
        raise RuntimeError("Source QA is incomplete")
    accepted = {
        str(row["id"])
        for row in manual_review.get("decisions", [])
        if row.get("status") == "accept"
    }
    blocked = [
        str(row["id"])
        for row in manual_review.get("decisions", [])
        if row.get("status") != "accept"
    ]
    if blocked:
        raise RuntimeError(f"Manual review still requests regeneration for {len(blocked)} items")
    unresolved = [row["id"] for row in source_results if row["status"] != "pass" and row["id"] not in accepted]
    if unresolved:
        raise RuntimeError(f"Manual review is incomplete for {len(unresolved)} technical-review items")

    asset_results = asset_qa.get("results", [])
    if len(asset_results) != 721 or any(row["status"] != "pass" for row in asset_results):
        raise RuntimeError("Installed animation assets have not passed the 721-item gate")

    apk = ROOT / "build/timehouse-debug.apk"
    domain_log = ROOT / args.domain_log
    build_log = ROOT / args.build_log
    intensity_ui_log = ROOT / args.intensity_ui_log
    display_ui_log = ROOT / args.display_ui_log
    media_ui_log = ROOT / args.media_ui_log
    for required in (apk, domain_log, build_log, intensity_ui_log, display_ui_log, media_ui_log):
        if not required.exists() or required.stat().st_size == 0:
            raise FileNotFoundError(f"Required build output is missing: {required.relative_to(ROOT)}")
    ui_requirements = [
        (intensity_ui_log, 21),
        (display_ui_log, 21),
        (media_ui_log, 6),
    ]
    for log, minimum in ui_requirements:
        passed = sum(line.startswith("PASS ") for line in log.read_text().splitlines())
        if passed < minimum or "Traceback" in log.read_text():
            raise RuntimeError(
                f"UI regression incomplete: {log.relative_to(ROOT)} has {passed}/{minimum} passes"
            )

    android_manifest = (ROOT / "app/src/main/AndroidManifest.xml").read_text()
    version_match = re.search(r'android:versionName="([^"]+)"', android_manifest)
    if not version_match:
        raise RuntimeError("Android versionName was not found")
    version = version_match.group(1)
    release_dir = ROOT / "build" / f"timehouse-{version}-priority-motion-720"
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True)

    apk_name = f"timehouse-{version}-priority-motion-720.apk"
    shutil.copy2(apk, release_dir / apk_name)
    evidence = [
        (batch / "workflow.json", "workflow.json"),
        (batch / "reuse.json", "reuse.json"),
        (batch / "scope-exclusions.json", "scope-exclusions.json"),
        (batch / "manifest.json", "manifest.json"),
        (batch / "source-qa.json", "source-qa.json"),
        (batch / "asset-qa.json", "asset-qa.json"),
        (batch / "manual-review.json", "manual-review.json"),
        (domain_log, "priority-motion-domain-tests.log"),
        (build_log, "priority-motion-build.log"),
        (intensity_ui_log, "intensity-assessment-ui.log"),
        (display_ui_log, "display-rotation-routines-ui.log"),
        (media_ui_log, "custom-equipment-media-ui.log"),
        (ROOT / "build/qa-20260912-display-rotation/ui-checks.json", "display-rotation-ui-checks.json"),
        (ROOT / "build/qa-20260912-custom-media/ui-checks.json", "custom-media-ui-checks.json"),
        (ROOT / "docs/priority-motion-720-workflow.md", "priority-motion-720-workflow.md"),
        (ROOT / "docs/releases/2026-09-12-priority-motion-assessment-ui.md", "2026-09-12-release-notes.md"),
    ]
    for optional in (batch / "visual-qa-summary.json",):
        if optional.exists():
            evidence.append((optional, optional.name))
    evidence_dir = release_dir / "evidence"
    evidence_dir.mkdir()
    for path, destination_name in evidence:
        if not path.exists() or path.stat().st_size == 0:
            raise FileNotFoundError(f"Required release evidence is missing: {path.relative_to(ROOT)}")
        shutil.copy2(path, evidence_dir / destination_name)

    packaged_files = sorted(path for path in release_dir.rglob("*") if path.is_file())
    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "batch": args.batch,
        "requested_new_images": 720,
        "in_scope_new_images": 716,
        "exact_duplicate_reuses": 5,
        "scope_exclusions": 4,
        "covered_dataset_rows": 721,
        "apk": apk_name,
        "apk_bytes": (release_dir / apk_name).stat().st_size,
        "apk_sha256": sha256(release_dir / apk_name),
        "source_qa": source_qa.get("status_counts", {}),
        "asset_qa": asset_qa.get("status_counts", {}),
        "ui_regressions": {
            "intensity_assessment": 21,
            "display_rotation_routines": 21,
            "custom_equipment_media": 6,
        },
    }
    (release_dir / "release-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    packaged_files = sorted(path for path in release_dir.rglob("*") if path.is_file())
    checksums = "".join(
        f"{sha256(path)}  {path.relative_to(release_dir)}\n" for path in packaged_files
    )
    (release_dir / "SHA256SUMS.txt").write_text(checksums)

    archive = release_dir.parent / f"{release_dir.name}.zip"
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for path in sorted(p for p in release_dir.rglob("*") if p.is_file()):
            package.write(path, Path(release_dir.name) / path.relative_to(release_dir))
    print(json.dumps({"release_dir": str(release_dir), "archive": str(archive), **summary}, ensure_ascii=False))


if __name__ == "__main__":
    main()
