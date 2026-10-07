#!/usr/bin/env python3
"""Record explicit human-visible review decisions for technical QA exceptions."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default="20260910_720")
    decision = parser.add_mutually_exclusive_group(required=True)
    decision.add_argument("--accept", nargs="+")
    decision.add_argument("--reject", nargs="+")
    parser.add_argument("--note", required=True)
    args = parser.parse_args()
    batch = ROOT / "assets/motion_repairs" / args.batch
    qa = json.loads((batch / "source-qa.json").read_text())
    known = {str(row["id"]) for row in qa["results"] if row["status"] != "missing"}
    requested = {str(item) for item in (args.accept or args.reject)}
    unknown = requested - known
    if unknown:
        raise RuntimeError(f"Cannot review missing or unknown ids: {sorted(unknown)}")
    output = batch / "manual-review.json"
    payload = json.loads(output.read_text()) if output.exists() else {"batch": args.batch, "decisions": []}
    decisions = {str(row["id"]): row for row in payload["decisions"]}
    reviewed_at = datetime.now(timezone.utc).isoformat()
    status = "accept" if args.accept else "regenerate"
    for exercise_id in sorted(requested):
        decisions[exercise_id] = {
            "id": exercise_id,
            "status": status,
            "reviewed_at": reviewed_at,
            "reviewer": "contact-sheet-visual-review",
            "note": args.note,
        }
    payload["decisions"] = [decisions[key] for key in sorted(decisions)]
    payload["updated_at"] = reviewed_at
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": status, "recorded": len(requested), "total_decisions": len(decisions)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
