# 时光屋 1.1.0 · 从今天的一小步开始

本次集中改进「打开 → 安排 → 开练 → 被打断 → 保存」这条使用路径。

- 今日首页：8 / 15 / 25 分钟主课预算、轻松 / 日常模式，本地生成；有今日周期课时优先展示当天课表。设置仍是器械与伤痛信息的来源。
- 课程预览：开始按钮提前，动作改为紧凑列表，示范、详细要点按需展开。换动作后重新计算时间，不超过本次预算；迟到的 AI 回复不能覆盖新课程或正在进行的训练。
- 专注训练：大计时、当前组次和完成按钮在前，示范在后；底部可暂存或结束。
- 自动保留：每次组间转换和暂停保存进度，运行时约每两秒保存一次。离开、锁屏、返回首页均暂停；重开后明确点击继续。突然终止可能回退最近尚未写入的少量计时。
- 完成反馈：显示本次实际用时、实际完成组数、本周足迹；感受记录改为可选。提前结束保留已完成的组；整节周期课全部完成才标记完成。
- 原有历史记录、饮食、动作库及周期日历保持原存储结构。含暂停的训练会说明心率仍按整段起止区间统计，与扣除暂停后的训练用时口径不同。

## 构建与验证

原工程使用 Android SDK 脚本直接构建，无 Gradle。使用原有 `build/debug.keystore` 签名。输出为可覆盖安装的调试 APK，不是应用商店发布包。

```sh
bash scripts/build_android_debug.sh
# 此环境的 Python 运行时提供 Pillow，供原有动画资产校验使用。
PATH="/Users/restartday/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin:/opt/homebrew/bin:/usr/bin:/bin" bash scripts/run_domain_tests.sh
bash scripts/build_android_qa.sh
# 先安装 build/timehouse-debug.apk 与 build/android-qa/qa.apk 到专用模拟器。
python3 scripts/qa_today_flow.py --serial emulator-5554
```

UI 脚本只接受显式指定的模拟器。测试使用临时数据，退出时恢复原偏好、字体和显示尺寸，不清除应用数据。`android_qa/UiSnapshot.java` 是单独的只读测试 APK，用于读取动态计时界面，不包含在交付 APK 中。

实现遵循 Android 官方的[生命周期](https://developer.android.com/guide/components/activities/activity-lifecycle)与[状态保存](https://developer.android.com/topic/libraries/architecture/saving-states)说明；保存的是已用时与阶段进度，不持久化设备启动时间戳。

本次修改前的源文件副本位于 `build/before-20260906/`。完整模拟器结果与截图位于 `build/qa-20260906/`。具体通过情况见同目录 `ui-checks.json` 及最终验收记录。
