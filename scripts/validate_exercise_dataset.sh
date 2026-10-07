#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATASET="$ROOT/app/src/main/assets/exercises_1324.json"
MEDIA_MAP="$ROOT/scripts/data/free_exercise_media.json"
MEDIA_DIR="$ROOT/app/src/main/res/raw"
PYTHON="${PYTHON:-python3}"

if [[ ! -f "$DATASET" ]]; then
  echo "Missing bundled exercise dataset: $DATASET" >&2
  exit 1
fi

count="$(jq '.exercises | length' "$DATASET")"
duplicate_ids="$(jq '[.exercises | group_by(.id)[] | select(length > 1)] | length' "$DATASET")"
missing_required="$(jq '[.exercises[] | select(
  (.id | length) == 0 or
  (.name | length) == 0 or
  (.name_zh | test("\\p{Han}") | not) or
  (.name_zh | gsub("V字"; "字") | test("[A-Za-z]")) or
  (.category | length) == 0 or
  (.equipment | length) == 0 or
  (.instructions_zh | length) == 0 or
  ([.instructions_zh[] | test("\\p{Han}")] | all | not)
)] | length' "$DATASET")"
media_fields="$(jq '[.exercises[] | select(has("image") or has("gif_url") or has("media_id"))] | length' "$DATASET")"
animated_media_count="$(jq '[.exercises[] | select(.media != "")] | length' "$DATASET")"
metadata_media_count="$(jq '.source.public_domain_media_matches' "$DATASET")"
metadata_animated_count="$(jq '.source.animated_media_count' "$DATASET")"
metadata_procedural_count="$(jq '.source.procedural_media_count' "$DATASET")"
upstream_media_included="$(jq '.source.upstream_restricted_media_included' "$DATASET")"
media_map_count="$(jq 'length' "$MEDIA_MAP")"
# Media ships as animated WebP (ImageDecoder-native, ~4x smaller than GIF); a
# stray legacy .gif with the same R.raw name would collide, so count both and
# reject leftover GIFs.
resource_media_count="$(find "$MEDIA_DIR" -maxdepth 1 -type f -name 'dataset_motion_*.webp' | wc -l | tr -d ' ')"
legacy_gif_count="$(find "$MEDIA_DIR" -maxdepth 1 -type f -name 'dataset_motion_*.gif' | wc -l | tr -d ' ')"
legacy_static_count="$(find "$MEDIA_DIR" -maxdepth 1 -type f -name 'dataset_motion_*.jpg' | wc -l | tr -d ' ')"

[[ "$count" == "1324" ]] || { echo "Expected 1324 exercises, got $count" >&2; exit 1; }
[[ "$duplicate_ids" == "0" ]] || { echo "Duplicate dataset IDs: $duplicate_ids" >&2; exit 1; }
[[ "$missing_required" == "0" ]] || { echo "Rows missing required app fields: $missing_required" >&2; exit 1; }
[[ "$media_fields" == "0" ]] || { echo "Restricted media references must not be bundled" >&2; exit 1; }
[[ "$upstream_media_included" == "false" ]] || { echo "Dataset incorrectly declares restricted upstream media" >&2; exit 1; }
[[ "$animated_media_count" == "1324" ]] || { echo "Every imported exercise must have animation media; got $animated_media_count" >&2; exit 1; }
[[ "$metadata_media_count" == "$media_map_count" ]] || { echo "Dataset media metadata mismatch: $metadata_media_count vs $media_map_count" >&2; exit 1; }
[[ "$metadata_animated_count" == "1324" ]] || { echo "Animated media metadata mismatch: $metadata_animated_count" >&2; exit 1; }
[[ "$metadata_procedural_count" == "$((1324 - media_map_count))" ]] || { echo "Procedural media metadata mismatch: $metadata_procedural_count" >&2; exit 1; }
[[ "$resource_media_count" == "1324" ]] || { echo "Exercise WebP resource count mismatch: $resource_media_count" >&2; exit 1; }
[[ "$legacy_gif_count" == "0" ]] || { echo "Legacy GIF previews collide with WebP R.raw names: $legacy_gif_count" >&2; exit 1; }
[[ "$legacy_static_count" == "0" ]] || { echo "Static exercise previews remain after animation generation: $legacy_static_count" >&2; exit 1; }

while IFS= read -r media_ref; do
  resource_name="${media_ref#raw:}"
  [[ -f "$MEDIA_DIR/$resource_name.webp" || -f "$MEDIA_DIR/$resource_name.gif" ]] || {
    echo "Missing public-domain media resource: $resource_name" >&2
    exit 1
  }
done < <(jq -r '.exercises[].media | select(. != "")' "$DATASET")

"$PYTHON" "$ROOT/scripts/validate_exercise_gifs.py" "$MEDIA_DIR" --expected-count 1324
"$PYTHON" "$ROOT/scripts/validate_exercise_gifs.py" "$MEDIA_DIR" --expected-count 24 --prefix motion_

echo "ExerciseDataset: 1324 Chinese records and 1324 animations validated ($media_map_count public-domain, $metadata_procedural_count procedural)"
