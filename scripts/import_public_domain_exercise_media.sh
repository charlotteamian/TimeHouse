#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_URL="https://github.com/yuhonas/free-exercise-db.git"
SOURCE_COMMIT="b0eed061e1c832b3ed815fbaa4b45b3cdc14df49"
DATASET="$ROOT/app/src/main/assets/exercises_1324.json"
RAW_DIR="$ROOT/app/src/main/res/raw"
MEDIA_MAP="$ROOT/scripts/data/free_exercise_media.json"
LICENSE_OUT="$ROOT/app/src/main/assets/licenses/free-exercise-db-UNLICENSE.txt"
PROCEDURAL_MANIFEST="$ROOT/scripts/data/procedural_animation_manifest.json"
MEDIA_TMP="$(mktemp -d /tmp/fitness-public-media.XXXXXX)"
trap 'rm -rf "$MEDIA_TMP"' EXIT

git -C "$MEDIA_TMP" init --quiet repo
git -C "$MEDIA_TMP/repo" remote add origin "$SOURCE_URL"
git -C "$MEDIA_TMP/repo" fetch --quiet --depth 1 origin "$SOURCE_COMMIT"
git -C "$MEDIA_TMP/repo" checkout --quiet FETCH_HEAD

jq -r 'to_entries[] | [(.value.name | ascii_downcase), .value.images[0], .value.images[1]] | @tsv' \
  "$MEDIA_TMP/repo/dist/exercises.json" | sort -t $'\t' -k1,1 > "$MEDIA_TMP/free.tsv"
jq -r '.exercises[] | [(.name | ascii_downcase), .id] | @tsv' \
  "$DATASET" | sort -t $'\t' -k1,1 > "$MEDIA_TMP/app.tsv"
join -t $'\t' -1 1 -2 1 "$MEDIA_TMP/app.tsv" "$MEDIA_TMP/free.tsv" > "$MEDIA_TMP/matches.tsv"

mkdir -p "$RAW_DIR" "$(dirname "$MEDIA_MAP")" "$(dirname "$LICENSE_OUT")"
find "$RAW_DIR" -maxdepth 1 -type f \( -name 'dataset_motion_*.jpg' -o -name 'dataset_motion_*.gif' \) -delete
"$ROOT/scripts/generate_exercise_gifs.py" \
  --matches "$MEDIA_TMP/matches.tsv" \
  --source-root "$MEDIA_TMP/repo" \
  --output-dir "$RAW_DIR"

jq -Rn '[inputs | split("\t") | {(.[1]): ("raw:dataset_motion_" + .[1])}] | add' \
  < "$MEDIA_TMP/matches.tsv" > "$MEDIA_MAP"
install -m 0644 "$MEDIA_TMP/repo/LICENSE.md" "$LICENSE_OUT"

count="$(wc -l < "$MEDIA_TMP/matches.tsv" | tr -d ' ')"
"$ROOT/scripts/generate_procedural_exercise_gifs.py" \
  --dataset "$DATASET" \
  --exact-media-map "$MEDIA_MAP" \
  --output-dir "$RAW_DIR" \
  --manifest "$PROCEDURAL_MANIFEST"
"$ROOT/scripts/validate_exercise_gifs.py" "$RAW_DIR" --expected-count 1324
echo "Imported $count exact-name public-domain animations and generated the remaining $((1324 - count)) procedural animations"
