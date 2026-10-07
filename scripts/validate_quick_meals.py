#!/usr/bin/env python3
"""Sanity-check the quick-log preset dataset (assets/quick_meals_cn.json).

These presets exist so users never convert cooked weight to the pagoda's raw
weight by hand, so the checks focus on that contract: unique ids, valid kinds
and FoodGroup keys, positive grams, a hint on every entry, kcal roughly
consistent with the declared groups, and enough coverage per kind.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app/src/main/assets/quick_meals_cn.json"

VALID_GROUPS = {"GRAIN", "WHOLE_GRAIN", "TUBER", "VEGETABLE", "FRUIT",
                "ANIMAL", "DAIRY", "SOY_NUT", "OIL", "OTHER"}
VALID_KINDS = {"PORTION", "TAKEOUT", "SNACK"}

# Rough kcal per gram of raw/dry weight, used only as an order-of-magnitude
# guard against typos like a missing zero. Deliberately loose.
# WHOLE_GRAIN is 0 because it is a subset of GRAIN, already counted.
# OTHER is 0 because the bucket spans beer (0.36 kcal/g) to chocolate
# (5.5 kcal/g) -- no single density is meaningful, so entries dominated by it
# get no kcal cross-check rather than a fake one.
KCAL_PER_G = {
    "GRAIN": 3.5, "WHOLE_GRAIN": 0.0,
    "TUBER": 0.8, "VEGETABLE": 0.25, "FRUIT": 0.45, "ANIMAL": 1.7,
    "DAIRY": 0.55, "SOY_NUT": 5.0, "OIL": 9.0, "OTHER": 0.0,
}
OTHER_SKIP_SHARE = 0.3
MIN_PER_KIND = 8


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    presets = data["presets"]
    errors: list[str] = []
    unchecked: list[str] = []
    ids: set[str] = set()
    kind_counts = {kind: 0 for kind in VALID_KINDS}

    for preset in presets:
        pid = preset.get("id", "?")
        if pid in ids:
            errors.append(f"{pid}: duplicate id")
        ids.add(pid)

        kind = preset.get("kind")
        if kind not in VALID_KINDS:
            errors.append(f"{pid}: bad kind {kind!r}")
        else:
            kind_counts[kind] += 1

        if not preset.get("name"):
            errors.append(f"{pid}: missing name")
        if not preset.get("hint"):
            errors.append(f"{pid}: missing hint (users need the conversion spelled out)")

        groups = preset.get("groups", {})
        if not groups:
            errors.append(f"{pid}: no food groups")
        bad = set(groups) - VALID_GROUPS
        if bad:
            errors.append(f"{pid}: unknown food groups {bad}")
        for key, grams in groups.items():
            if not isinstance(grams, int) or grams <= 0:
                errors.append(f"{pid}: group {key} has non-positive grams {grams!r}")
        if groups.get("WHOLE_GRAIN", 0) > groups.get("GRAIN", 0):
            errors.append(f"{pid}: whole grain exceeds grain")

        kcal = preset.get("kcal", 0)
        if not isinstance(kcal, int) or kcal <= 0:
            errors.append(f"{pid}: bad kcal {kcal!r}")
        else:
            total_g = sum(g for g in groups.values() if isinstance(g, int))
            other_share = groups.get("OTHER", 0) / total_g if total_g else 0
            rough = sum(KCAL_PER_G.get(k, 0) * g for k, g in groups.items())
            # Only catch gross errors: a 3x gap either way means a bad number.
            if other_share > OTHER_SKIP_SHARE:
                unchecked.append(pid)
            elif rough > 0 and not (rough / 3 <= kcal <= rough * 3):
                errors.append(f"{pid}: kcal {kcal} implausible vs groups (~{rough:.0f})")

    for kind, count in kind_counts.items():
        if count < MIN_PER_KIND:
            errors.append(f"kind {kind} has only {count} presets (<{MIN_PER_KIND})")

    if errors:
        print("QuickMeals: FAILED")
        for error in errors:
            print("  -", error)
        sys.exit(1)
    summary = (f"QuickMeals: {len(presets)} presets validated "
               f"({', '.join(f'{k}×{c}' for k, c in sorted(kind_counts.items()))})")
    if unchecked:
        summary += f"; kcal unchecked for {len(unchecked)} OTHER-dominated: {', '.join(unchecked)}"
    print(summary)


if __name__ == "__main__":
    main()
