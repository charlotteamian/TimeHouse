#!/usr/bin/env python3
"""Sanity-check the builtin evidence-based recipe dataset.

Checks: unique ids, valid meal slots and FoodGroup keys, kcal consistent with
macros (4P+9F+4C within 15%), every recipe has rationale + refs incl. the
estimate disclaimer, and pagoda coverage across the set (each group supplied
by at least one recipe).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app/src/main/assets/recipes_cn_guideline.json"

VALID_GROUPS = {"GRAIN", "WHOLE_GRAIN", "TUBER", "VEGETABLE", "FRUIT",
                "ANIMAL", "DAIRY", "SOY_NUT", "OIL"}
VALID_SLOTS = {"早餐", "午餐", "晚餐", "加餐"}


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    recipes = data["recipes"]
    errors: list[str] = []
    ids = set()
    supplied_groups = set()

    for recipe in recipes:
        rid = recipe.get("id", "?")
        if rid in ids:
            errors.append(f"{rid}: duplicate id")
        ids.add(rid)

        slots = set(recipe.get("slots", []))
        if not slots or not slots <= VALID_SLOTS:
            errors.append(f"{rid}: bad slots {slots}")

        groups = recipe.get("groups", {})
        bad = set(groups) - VALID_GROUPS
        if bad:
            errors.append(f"{rid}: unknown food groups {bad}")
        supplied_groups |= set(groups)
        if groups.get("WHOLE_GRAIN", 0) > groups.get("GRAIN", 0) and "GRAIN" in groups:
            errors.append(f"{rid}: whole grain exceeds grain")

        kcal = recipe["kcal"]
        macro_kcal = 4 * recipe["protein"] + 9 * recipe["fat"] + 4 * recipe["carb"]
        if abs(macro_kcal - kcal) > 0.15 * kcal:
            errors.append(f"{rid}: kcal {kcal} vs macros {macro_kcal} (>15% off)")

        if not recipe.get("rationale"):
            errors.append(f"{rid}: missing rationale")
        refs = recipe.get("refs", [])
        if "ESTIMATE_NOTE" not in refs:
            errors.append(f"{rid}: missing ESTIMATE_NOTE ref")
        if len(refs) < 2:
            errors.append(f"{rid}: needs at least one guideline ref besides the disclaimer")
        if not recipe.get("ingredients") or not recipe.get("steps"):
            errors.append(f"{rid}: missing ingredients/steps")

    missing_groups = VALID_GROUPS - supplied_groups
    if missing_groups:
        errors.append(f"dataset covers no recipe for groups: {missing_groups}")

    slot_counts = {slot: 0 for slot in VALID_SLOTS}
    for recipe in recipes:
        for slot in recipe.get("slots", []):
            slot_counts[slot] += 1
    for slot, count in slot_counts.items():
        if count < 3:
            errors.append(f"slot {slot} has only {count} recipes (<3)")

    if errors:
        print("RecipeDataset: FAILED")
        for error in errors:
            print("  -", error)
        sys.exit(1)
    print(f"RecipeDataset: {len(recipes)} recipes validated "
          f"(slots: {', '.join(f'{s}×{c}' for s, c in sorted(slot_counts.items()))})")


if __name__ == "__main__":
    main()
