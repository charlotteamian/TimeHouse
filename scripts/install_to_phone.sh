#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/Library/Android/sdk/platform-tools:$PATH"
APK="$ROOT/build/timehouse-debug.apk"

if [[ ! -f "$APK" ]]; then
  echo "APK not found, building first..."
  bash "$ROOT/scripts/build_android_debug.sh"
fi

echo "=================================================="
echo "手机安装助手"
echo "正在检测真机连接..."
echo "=================================================="

LAST_STATE=""
while true; do
  # Check if there is an unauthorized physical device
  UNAUTH=$(adb devices 2>/dev/null | awk '$2=="unauthorized" && !/emulator/{print $1; exit}')
  if [[ -n "$UNAUTH" ]]; then
    if [[ "$LAST_STATE" != "unauthorized" ]]; then
      echo "⚠️ 检测到手机 ($UNAUTH)，但尚未授权！"
      echo "👉 请查看手机屏幕，点击【允许 USB 调试】（建议勾选“始终允许这台计算机”）"
      LAST_STATE="unauthorized"
    fi
    sleep 2
    continue
  fi

  # Check if there is an authorized physical device
  DEV=$(adb devices 2>/dev/null | awk '$2=="device" && !/emulator/{print $1; exit}')
  if [[ -n "$DEV" ]]; then
    MODEL=$(adb -s "$DEV" shell getprop ro.product.model 2>/dev/null || echo "Android Phone")
    echo "=================================================="
    echo "✅ 成功识别到手机: $MODEL (设备号: $DEV)"
    echo "📦 正在安装最新 APK: $APK ..."
    echo "=================================================="
    
    INSTALL_OUT=$(adb -s "$DEV" install -r -d -t "$APK" 2>&1)
    echo "$INSTALL_OUT"
    
    if echo "$INSTALL_OUT" | grep -q "Success"; then
      echo "🚀 正在启动应用..."
      adb -s "$DEV" shell am start -n com.restartday.fitness/.app.MainActivity
      echo "🎉 安装并启动成功！"
      exit 0
    elif echo "$INSTALL_OUT" | grep -q "INSTALL_FAILED_USER_RESTRICTED"; then
      echo "⚠️ 安装被系统拦截: 请在一加手机【开发者选项】中开启【禁止权限监控】或允许通过 USB 安装应用。"
      sleep 4
    else
      echo "⚠️ 安装未成功，正在重试..."
      sleep 3
    fi
  else
    if [[ "$LAST_STATE" != "waiting" ]]; then
      echo "⏳ 等待手机接入并开启 USB 调试..."
      LAST_STATE="waiting"
    fi
    sleep 2
  fi
done
