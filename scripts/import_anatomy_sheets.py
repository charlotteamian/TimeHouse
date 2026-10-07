#!/usr/bin/env python3
"""Import GPT-drawn anatomical motion sheets into the app as animations.

Idempotent pipeline for the ongoing GPT image workflow: it reads every wave
manifest under assets/anatomy_motion_sheets/waves/, resolves each exercise row
to its generated sheet, animates the start/end pair with the registration-based
animator, and writes:

  app/src/main/res/raw/dataset_motion_<id>.webp   (the app asset)
  build/anatomy-motion-gifs/dataset_motion_<id>.gif  (same frames, previewable)
  build/anatomy_regen_report.json                 (per-id animator metrics)

Re-run it any time new waves/sheets land — already-imported exercises are
simply refreshed.

Row mapping is taken from each wave batch's `exercises[].row` (authoritative).
Named "orphan" sheets that predate the wave format (exactly 3 ids in the file
name, no wave entry) fall back to filename order. The 4-id pilot sheet is skipped
as ambiguous.

    python3 scripts/import_anatomy_sheets.py            # import everything ready
    python3 scripts/import_anatomy_sheets.py --dry-run  # just report coverage
    python3 scripts/import_anatomy_sheets.py --ids 0007 0015   # subset only
"""

from __future__ import annotations

import argparse
import glob
import json
import multiprocessing as mp
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "assets/anatomy_motion_sheets/generated"
WAVES = ROOT / "assets/anatomy_motion_sheets/waves"
RAW = ROOT / "app/src/main/res/raw"
GIF_PREVIEWS = ROOT / "build/anatomy-motion-gifs"
REPORT = ROOT / "build/anatomy_regen_report.json"


def build_plan() -> tuple[list[dict], dict]:
    """Return (entries, stats). Each entry: {id, sheet, row, source}."""
    entries: list[dict] = []
    covered: set[str] = set()
    wave_sheets: set[str] = set()

    for wave_path in sorted(WAVES.glob("wave_*.json")):
        for batch in json.loads(wave_path.read_text()).get("batches", []):
            base = os.path.basename(batch.get("destination", ""))
            wave_sheets.add(base)
            if not (GEN / base).exists():
                continue
            for ex in batch.get("exercises", []):
                xid = str(ex["id"])
                if xid in covered:
                    continue
                entries.append({"id": xid, "sheet": base, "row": int(ex["row"]), "source": "wave"})
                covered.add(xid)

    for sheet in sorted(GEN.glob("*.png")):
        base = sheet.name
        if base in wave_sheets or "pilot" in base:
            continue
        ids = re.findall(r"(\d{4})", base)
        if len(ids) != 3:  # only unambiguous 3-row orphan sheets
            continue
        for row, xid in enumerate(ids):
            if xid in covered:
                continue
            entries.append({"id": xid, "sheet": base, "row": row, "source": "orphan"})
            covered.add(xid)

    pending = [os.path.basename(b.get("destination", ""))
               for w in WAVES.glob("wave_*.json")
               for b in json.loads(w.read_text()).get("batches", [])
               if not (GEN / os.path.basename(b.get("destination", ""))).exists()]
    # Reviewed repair batches own these ids; older bulk sheets must not overwrite them.
    repaired = set()
    for manifest in (ROOT / "assets/motion_repairs").glob("*/manifest.json"):
        for record in json.loads(manifest.read_text()):
            if not (ROOT / record["asset"]).exists():
                raise FileNotFoundError("Missing repaired asset: " + record["asset"])
            repaired.add(record["id"])
    entries = [entry for entry in entries if entry["id"] not in repaired]
    stats = {
        "protected_repairs": sorted(repaired),
        "wave": sum(e["source"] == "wave" for e in entries),
        "orphan": sum(e["source"] == "orphan" for e in entries),
        "pending_sheets": sorted(set(pending)),
    }
    return entries, stats


def _render(entry: dict) -> tuple[str, dict]:
    """Worker: animate one exercise; returns (id, metrics)."""
    import cv2
    cv2.setNumThreads(1)  # workers are already one-per-core
    import animate_anatomical_frames as animator

    start, end = animator.sheet_pair(GEN / entry["sheet"], entry["row"])
    out = RAW / f"dataset_motion_{entry['id']}.webp"
    preview = GIF_PREVIEWS / f"dataset_motion_{entry['id']}.gif"
    try:
        info = animator.animate(start, end, out, also=[preview])
    except Exception as exc:  # keep the batch alive; report the failure
        return entry["id"], {"error": f"{type(exc).__name__}: {exc}",
                             "sheet": entry["sheet"], "row": entry["row"]}
    stale = RAW / f"dataset_motion_{entry['id']}.gif"  # avoid duplicate R.raw name
    if stale.exists():
        stale.unlink()
    info.update({"sheet": entry["sheet"], "row": entry["row"]})
    return entry["id"], info


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ids", nargs="*", help="only regenerate these exercise ids")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 4) - 1))
    args = ap.parse_args()

    entries, stats = build_plan()
    if args.ids:
        wanted = set(args.ids)
        entries = [e for e in entries if e["id"] in wanted]
    print(f"exercises ready: {len(entries)}  (wave={stats['wave']}, orphan={stats['orphan']})")
    if stats["pending_sheets"]:
        print(f"waiting on {len(stats['pending_sheets'])} sheet(s) GPT hasn't generated yet:")
        for s in stats["pending_sheets"]:
            print(f"    {s}")
    if args.dry_run:
        return

    RAW.mkdir(parents=True, exist_ok=True)
    GIF_PREVIEWS.mkdir(parents=True, exist_ok=True)

    report: dict = {}
    if REPORT.exists() and args.ids:
        report = json.loads(REPORT.read_text())

    with mp.Pool(args.jobs) as pool:
        for i, (xid, info) in enumerate(pool.imap_unordered(_render, entries, chunksize=8), 1):
            report[xid] = info
            if i % 100 == 0 or i == len(entries):
                print(f"  {i}/{len(entries)} rendered")

    REPORT.write_text(json.dumps(report, indent=1, sort_keys=True))
    modes: dict = {}
    for info in report.values():
        modes[info.get("mode", "error")] = modes.get(info.get("mode", "error"), 0) + 1
    print(f"imported {len(entries)} animations into {RAW}")
    print(f"modes: {modes}")
    print(f"report: {REPORT}")


if __name__ == "__main__":
    main()
