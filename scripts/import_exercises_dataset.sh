#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_URL="https://github.com/hasaneyldrm/exercises-dataset.git"
SOURCE_COMMIT="7455efae41b330c265e7cd4b78dfa848e7ce5ebd"
ASSETS="$ROOT/app/src/main/assets"
TRANSLATIONS="$ROOT/scripts/data/exercise_names_zh.json"
PUBLIC_MEDIA="$ROOT/scripts/data/free_exercise_media.json"
IMPORT_TMP="$(mktemp -d /tmp/fitness-exercises-import.XXXXXX)"
trap 'rm -rf "$IMPORT_TMP"' EXIT

git -C "$IMPORT_TMP" init --quiet repo
git -C "$IMPORT_TMP/repo" remote add origin "$SOURCE_URL"
git -C "$IMPORT_TMP/repo" fetch --quiet --depth 1 origin "$SOURCE_COMMIT"
git -C "$IMPORT_TMP/repo" checkout --quiet FETCH_HEAD

mkdir -p "$ASSETS/licenses"
if [[ ! -f "$TRANSLATIONS" ]]; then
  echo "Missing Chinese name translations: $TRANSLATIONS" >&2
  echo "Run scripts/translate_exercise_names.py first." >&2
  exit 1
fi
if [[ ! -f "$PUBLIC_MEDIA" ]]; then
  echo "Missing public-domain media map: $PUBLIC_MEDIA" >&2
  exit 1
fi

jq -c --arg commit "$SOURCE_COMMIT" \
  --slurpfile names "$TRANSLATIONS" \
  --slurpfile media "$PUBLIC_MEDIA" '{
  source: {
    repository: "https://github.com/hasaneyldrm/exercises-dataset",
    commit: $commit,
    license: "MIT",
    imported_fields: [
      "id", "name", "category", "equipment", "target",
      "muscle_group", "secondary_muscles", "instruction_steps.zh",
      "public_domain_media_match"
    ],
    upstream_restricted_media_included: false,
    animated_media_count: 1324,
    public_domain_media_matches: ($media[0] | length),
    procedural_media_count: (1324 - ($media[0] | length))
  },
  exercises: [.[] | {
    id,
    name,
    name_zh: ($names[0][.id] // ""),
    media: ("raw:dataset_motion_" + .id),
    category,
    equipment,
    target,
    muscle_group,
    secondary_muscles,
    instructions_zh: .instruction_steps.zh
  }]
}' "$IMPORT_TMP/repo/data/exercises.json" > "$IMPORT_TMP/exercises_1324.json"

install -m 0644 "$IMPORT_TMP/exercises_1324.json" "$ASSETS/exercises_1324.json"
install -m 0644 "$IMPORT_TMP/repo/LICENSE" "$ASSETS/licenses/exercises-dataset-LICENSE.txt"

"$ROOT/scripts/import_public_domain_exercise_media.sh"
"$ROOT/scripts/validate_exercise_dataset.sh"
echo "Imported $SOURCE_COMMIT into $ASSETS"
