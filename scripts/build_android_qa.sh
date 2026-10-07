#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-$HOME/Library/Android/sdk}}"
JDK="${JAVA_HOME:-/Applications/Android Studio.app/Contents/jbr/Contents/Home}"
BT="${ANDROID_BUILD_TOOLS:-$SDK/build-tools/36.1.0}"
KEYSTORE="${ANDROID_DEBUG_KEYSTORE:-$ROOT/.signing/debug.keystore}"
OUT="$ROOT/build/android-qa"
mkdir -p "$OUT/classes" "$OUT/dex"
"$JDK/bin/javac" -encoding UTF-8 -source 11 -target 11 -cp "$SDK/platforms/android-36/android.jar" -d "$OUT/classes" "$ROOT/scripts/android_qa/UiSnapshot.java" "$ROOT/scripts/android_qa/HealthFixture.java"
JAVA_HOME="$JDK" "$BT/d8" --lib "$SDK/platforms/android-36/android.jar" --output "$OUT/dex" "$OUT"/classes/com/restartday/fitness/qa/*.class
"$BT/aapt2" link -I "$SDK/platforms/android-36/android.jar" --manifest "$ROOT/scripts/android_qa/AndroidManifest.xml" -o "$OUT/raw.apk"
(cd "$OUT/dex" && zip -q "$OUT/raw.apk" classes.dex)
"$BT/zipalign" -f 4 "$OUT/raw.apk" "$OUT/aligned.apk"
JAVA_HOME="$JDK" "$BT/apksigner" sign --ks "$KEYSTORE" --ks-pass pass:android --key-pass pass:android --out "$OUT/qa.apk" "$OUT/aligned.apk"
echo "$OUT/qa.apk"
