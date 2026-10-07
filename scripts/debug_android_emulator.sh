#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SDK="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
ADB="$SDK/platform-tools/adb"
EMULATOR="$SDK/emulator/emulator"
AVD="${ANDROID_AVD:-Medium_Phone_API_36.1}"
APK="$("$ROOT/scripts/build_android_debug.sh")"
LOG_DIR="$ROOT/build/debug"

mkdir -p "$LOG_DIR"

if ! "$ADB" devices | awk 'NR > 1 && $2 == "device" {found=1} END {exit(found ? 0 : 1)}'; then
  "$EMULATOR" -avd "$AVD" -no-snapshot-save -no-boot-anim >"$LOG_DIR/emulator.log" 2>&1 &
fi

"$ADB" wait-for-device

for _ in $(seq 1 120); do
  booted="$("$ADB" shell getprop sys.boot_completed 2>/dev/null | tr -d '\r' || true)"
  if [[ "$booted" == "1" ]]; then
    break
  fi
  sleep 1
done

"$ADB" install -r "$APK" >"$LOG_DIR/install.log"
"$ADB" shell pm clear com.restartday.fitness >"$LOG_DIR/clear.log" || true
"$ADB" shell am start -n com.restartday.fitness/.app.MainActivity >"$LOG_DIR/start.log"
sleep 3
"$ADB" exec-out screencap -p >"$LOG_DIR/home.png" || true
"$ADB" shell uiautomator dump /sdcard/fitness-home.xml >/dev/null 2>&1 || true
"$ADB" exec-out cat /sdcard/fitness-home.xml >"$LOG_DIR/home.xml" 2>/dev/null || true

"$ADB" shell input tap 180 1090
sleep 2
"$ADB" exec-out screencap -p >"$LOG_DIR/back-plan.png" || true
"$ADB" shell uiautomator dump /sdcard/fitness-back-plan.xml >/dev/null 2>&1 || true
"$ADB" exec-out cat /sdcard/fitness-back-plan.xml >"$LOG_DIR/back-plan.xml" 2>/dev/null || true

"$ADB" shell input tap 410 2250
sleep 1
"$ADB" exec-out screencap -p >"$LOG_DIR/library.png" || true
"$ADB" shell uiautomator dump /sdcard/fitness-library.xml >/dev/null 2>&1 || true
"$ADB" exec-out cat /sdcard/fitness-library.xml >"$LOG_DIR/library.xml" 2>/dev/null || true

"$ADB" shell am start \
  -a android.intent.action.SEND \
  -t text/plain \
  --es android.intent.extra.SUBJECT Shared_exercise_link \
  --es android.intent.extra.TEXT "https://example.com/demo-row" \
  -n com.restartday.fitness/.app.MainActivity >"$LOG_DIR/share.log" || true
sleep 2
"$ADB" exec-out screencap -p >"$LOG_DIR/share-inbox.png" || true
"$ADB" shell uiautomator dump /sdcard/fitness-share-inbox.xml >/dev/null 2>&1 || true
"$ADB" exec-out cat /sdcard/fitness-share-inbox.xml >"$LOG_DIR/share-inbox.xml" 2>/dev/null || true
"$ADB" logcat -d -t 300 >"$LOG_DIR/logcat.txt" || true

if rg -q "FATAL EXCEPTION|Process: com.restartday.fitness|com.restartday.fitness.*Exception" "$LOG_DIR/logcat.txt"; then
  echo "Crash-like output found in $LOG_DIR/logcat.txt" >&2
  exit 1
fi

echo "$LOG_DIR/home.png"
echo "$LOG_DIR/back-plan.png"
echo "$LOG_DIR/library.png"
echo "$LOG_DIR/share-inbox.png"
