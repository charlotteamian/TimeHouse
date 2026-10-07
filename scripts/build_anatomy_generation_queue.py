#!/usr/bin/env python3
"""Build the stable queue for replacing procedural exercise art with anatomy sheets."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "app" / "src" / "main" / "assets" / "exercises_1324.json"
EXACT_MEDIA = ROOT / "scripts" / "data" / "free_exercise_media.json"
SHEET_MANIFEST = ROOT / "scripts" / "data" / "anatomy_sheet_manifest.json"
DEFAULT_OUTPUT = ROOT / "scripts" / "data" / "anatomy_generation_queue.json"

REFERENCE_BY_CATEGORY = {
    "back": ["sheet_back_1.png", "sheet_back_2.png", "sheet_legs_back_2.png"],
    "cardio": ["sheet_legs_1.png", "sheet_core_1.png", "sheet_push_1.png"],
    "chest": ["sheet_push_1.png", "sheet_push_2.png", "sheet_core_arms_2.png"],
    "lower arms": ["sheet_core_arms_2.png", "sheet_back_2.png", "sheet_push_2.png"],
    "lower legs": ["sheet_legs_1.png", "sheet_legs_back_2.png", "sheet_core_1.png"],
    "neck": ["sheet_back_1.png", "sheet_core_arms_2.png", "sheet_push_2.png"],
    "shoulders": ["sheet_push_2.png", "sheet_core_arms_2.png", "sheet_back_2.png"],
    "upper arms": ["sheet_core_arms_2.png", "sheet_push_2.png", "sheet_back_2.png"],
    "upper legs": ["sheet_legs_1.png", "sheet_legs_back_2.png", "sheet_core_1.png"],
    "waist": ["sheet_core_1.png", "sheet_core_arms_2.png", "sheet_legs_back_2.png"],
}


def chunks(rows: list[dict], size: int) -> list[list[dict]]:
    return [rows[index:index + size] for index in range(0, len(rows), size)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    dataset = json.loads(DATASET.read_text(encoding="utf-8"))["exercises"]
    exact_ids = set(json.loads(EXACT_MEDIA.read_text(encoding="utf-8")))
    sheet_manifest = json.loads(SHEET_MANIFEST.read_text(encoding="utf-8"))
    generated_ids = {
        str(exercise["id"])
        for sheet in sheet_manifest["sheets"]
        if sheet["status"] in {"generated", "technical_passed", "qa_passed", "installed"}
        for exercise in sheet["exercises"]
    }

    procedural = [row for row in dataset if str(row["id"]) not in exact_ids]
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in procedural:
        grouped[str(row["category"])].append(row)

    batches = []
    for category in sorted(grouped):
        category_slug = category.replace(" ", "_")
        for index, batch_rows in enumerate(chunks(grouped[category], 3), start=1):
            ids = [str(row["id"]) for row in batch_rows]
            completed = sum(exercise_id in generated_ids for exercise_id in ids)
            status = "complete" if completed == len(ids) else "partial" if completed else "pending"
            batches.append({
                "id": f"{category_slug}_{index:03d}",
                "category": category,
                "status": status,
                "recommended_references": REFERENCE_BY_CATEGORY.get(category, []),
                "exercises": [
                    {
                        "id": str(row["id"]),
                        "name": row["name"],
                        "name_zh": row.get("name_zh", ""),
                        "equipment": row.get("equipment", ""),
                        "target": row.get("target", ""),
                        "muscle_group": row.get("muscle_group", ""),
                        "instructions_zh": row.get("instructions_zh", []),
                        "generated": str(row["id"]) in generated_ids,
                    }
                    for row in batch_rows
                ],
            })

    payload = {
        "version": 1,
        "source_dataset": str(DATASET.relative_to(ROOT)),
        "source_exact_media": str(EXACT_MEDIA.relative_to(ROOT)),
        "style_contract": "docs/anatomy-motion-style-contract.md",
        "summary": {
            "dataset_exercises": len(dataset),
            "existing_exact_media": len(exact_ids),
            "anatomy_required": len(procedural),
            "anatomy_generated": len(generated_ids & {str(row["id"]) for row in procedural}),
            "anatomy_remaining": len(procedural) - len(generated_ids & {str(row["id"]) for row in procedural}),
            "planned_sheets": len(batches),
        },
        "batches": batches,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
