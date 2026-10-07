#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-$HOME/Library/Android/sdk}}"
JAVA_HOME="${JAVA_HOME:-/Applications/Android Studio.app/Contents/jbr/Contents/Home}"
BUILD_TOOLS="${ANDROID_BUILD_TOOLS:-$SDK/build-tools/36.1.0}"
PLATFORM="${ANDROID_PLATFORM:-android-36}"
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"

if [[ ! -d "$BUILD_TOOLS" ]]; then
  BUILD_TOOLS="$(find "$SDK/build-tools" -maxdepth 1 -mindepth 1 -type d | sort | tail -1)"
fi

ANDROID_JAR="$SDK/platforms/$PLATFORM/android.jar"
AAPT2="$BUILD_TOOLS/aapt2"
D8="$BUILD_TOOLS/d8"
ZIPALIGN="$BUILD_TOOLS/zipalign"
APKSIGNER="$BUILD_TOOLS/apksigner"
JAVAC="$JAVA_HOME/bin/javac"
KEYTOOL="$JAVA_HOME/bin/keytool"

BUILD="$ROOT/build/android"
OUT_APK="$ROOT/build/timehouse-debug.apk"
KEYSTORE="${ANDROID_DEBUG_KEYSTORE:-$ROOT/.signing/debug.keystore}"

# Keep the signing identity outside disposable build output. Preserve the key
# used by existing phone installs when migrating an older local checkout.
if [[ ! -f "$KEYSTORE" && -f "$ROOT/build/debug.keystore" ]]; then
  mkdir -p "$(dirname "$KEYSTORE")"
  cp "$ROOT/build/debug.keystore" "$KEYSTORE"
  chmod 600 "$KEYSTORE"
fi

for tool in "$ANDROID_JAR" "$AAPT2" "$D8" "$ZIPALIGN" "$APKSIGNER" "$JAVAC" "$KEYTOOL"; do
  [[ -f "$tool" ]] || { echo "Missing Android/Java build dependency: $tool" >&2; exit 1; }
done

rm -rf "$BUILD"
mkdir -p "$BUILD/compiled" "$BUILD/generated" "$BUILD/classes" "$BUILD/dex" "$ROOT/build"

"$AAPT2" compile --dir "$ROOT/app/src/main/res" -o "$BUILD/compiled/resources.zip"

"$AAPT2" link \
  -I "$ANDROID_JAR" \
  --debug-mode \
  --manifest "$ROOT/app/src/main/AndroidManifest.xml" \
  -A "$ROOT/app/src/main/assets" \
  --java "$BUILD/generated" \
  --auto-add-overlay \
  -R "$BUILD/compiled/resources.zip" \
  -o "$BUILD/resources.apk"

"$JAVAC" -encoding UTF-8 -source 11 -target 11 \
  -classpath "$ANDROID_JAR" \
  -d "$BUILD/classes" \
  $(find "$ROOT/app/src/main/java" "$BUILD/generated" -name '*.java' | sort)

"$D8" --lib "$ANDROID_JAR" --output "$BUILD/dex" \
  $(find "$BUILD/classes" -name '*.class' | sort)

cp "$BUILD/resources.apk" "$BUILD/unsigned.apk"
(cd "$BUILD/dex" && zip -q -r "$BUILD/unsigned.apk" classes.dex)

if [[ ! -f "$KEYSTORE" ]]; then
  mkdir -p "$(dirname "$KEYSTORE")"
  "$KEYTOOL" -genkeypair \
    -keystore "$KEYSTORE" \
    -storepass android \
    -keypass android \
    -alias androiddebugkey \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000 \
    -dname "CN=Android Debug,O=Restartday,C=CN" >/dev/null
  chmod 600 "$KEYSTORE"
fi

"$ZIPALIGN" -f 4 "$BUILD/unsigned.apk" "$BUILD/aligned.apk"
"$APKSIGNER" sign \
  --ks "$KEYSTORE" \
  --ks-pass pass:android \
  --key-pass pass:android \
  --out "$OUT_APK" \
  "$BUILD/aligned.apk"

"$APKSIGNER" verify --print-certs "$OUT_APK" >/dev/null
echo "$OUT_APK"
