#!/usr/bin/env python3
"""Use the local vision model as a zero-cloud-token semantic QA gate.

This is deliberately a review queue, not an automatic medical authority.  It
compares each generated sprite sheet with the exercise metadata and the old
movement guide, then writes one small result file per image so the run is fully
resumable.
"""

from __future__ import annotations

import argparse
import base64
import json
import time
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH = "20260910_720"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def encoded(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def ask(spec: dict, source: Path, model: str) -> dict:
    prompt = f"""You are a strict exercise-animation QA reviewer.
Image 1 is a newly generated 2x2 sprite sheet. Image 2 is an older movement-only guide and may have worse art, but it helps identify the intended motion.
Exercise: {spec['name_en']} ({spec['name']}); equipment: {spec['equipment']}; target: {spec['target']}.
Review Image 1 for: exactly four cells; one complete adult male per cell; same identity, camera, scale, supports, grips and fixed equipment; visible setup, halfway, peak and repeated-halfway phases; correct named exercise and equipment mechanics; plausible joints and limbs; grayscale anatomy with muted coral target muscles; white clean background; no text or extra objects.
Return only JSON with keys status (pass or review), motion_correct (boolean), equipment_correct (boolean), anatomy_consistent (boolean), style_match (boolean), reason (one short English sentence). Be skeptical. Use review for duplicate phases, wrong exercise, inconsistent anchors, missing equipment, extra/malformed limbs, cropping, or uncertain biomechanics."""
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [encoded(source), encoded(Path(spec["movement_guide"]))],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 300},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=600) as response:
        raw = json.load(response)
    text = raw.get("response") or raw.get("thinking") or ""
    result = json.loads(text)
    result.update({
        "id": spec["id"],
        "model": model,
        "seconds": round(time.monotonic() - started, 2),
        "prompt_sha256": spec["prompt_sha256"],
    })
    if result.get("status") not in {"pass", "review"}:
        result["status"] = "review"
        result["reason"] = "Local reviewer returned an invalid status."
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default=DEFAULT_BATCH)
    parser.add_argument("--model", default="qwen3-vl:8b-instruct")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--ids", nargs="*")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    batch = ROOT / "assets/motion_repairs" / args.batch
    output = batch / "visual_qa"
    output.mkdir(parents=True, exist_ok=True)
    specs = json.loads((batch / "prompts.json").read_text())
    wanted = set(args.ids or [])
    pending = []
    for spec in specs:
        source = batch / f"{spec['id']}.png"
        result = output / f"{spec['id']}.json"
        if not source.exists() or (wanted and spec["id"] not in wanted):
            continue
        if result.exists() and not args.force:
            continue
        pending.append((spec, source, result))
    if args.limit > 0:
        pending = pending[:args.limit]

    for index, (spec, source, result_path) in enumerate(pending, 1):
        try:
            result = ask(spec, source, args.model)
        except Exception as error:
            result = {
                "id": spec["id"], "status": "review",
                "reason": f"reviewer_error: {type(error).__name__}: {error}",
                "model": args.model, "prompt_sha256": spec["prompt_sha256"],
            }
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(f"{index}/{len(pending)} {spec['id']} {result['status']} {result.get('reason', '')}", flush=True)

    results = [json.loads(path.read_text()) for path in sorted(output.glob("*.json"))]
    summary = {
        "batch": args.batch,
        "reviewed": len(results),
        "status_counts": dict(Counter(row.get("status", "review") for row in results)),
        "review_ids": [row["id"] for row in results if row.get("status") != "pass"],
    }
    (batch / "visual-qa-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
