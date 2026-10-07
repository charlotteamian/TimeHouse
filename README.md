# 时光屋

个人 Android 健身与饮食记录应用。包名 `com.restartday.fitness`，最低 Android 9（API 28）。完整 Java 源码、离线动作动画、中文资料、原始图稿、复核记录和制作脚本均在本仓库中。

这是私人项目，仓库和安装包保持私有。应用内填写的 AI API 密钥和个人记录保存在手机端；签名密钥通过 GitHub Actions Secret 保存。

## 直接在 GitHub 更新

1. 打开 [私有仓库](https://github.com/charlotteamian/TimeHouse)，登录自己的 GitHub 账号。
2. 打开文件并点编辑按钮；修改多个文件时，在仓库页面按 `.`，或直接进入 [网页代码编辑器](https://github.dev/charlotteamian/TimeHouse)。
3. 在 Source Control 中提交修改，选择提交到 `main`；源码、资料或构建脚本变更会自动运行检查和构建。只改说明文档或原始图稿时，可到 Actions 手动运行。
4. 到 [Actions](https://github.com/charlotteamian/TimeHouse/actions/workflows/android.yml) 查看结果；检查与构建通过后，从 [最新开发构建](https://github.com/charlotteamian/TimeHouse/releases/tag/latest-build) 下载 `timehouse-debug.apk`。

网页编辑器的修改需要提交才会同步到 GitHub。APK 使用原有签名，可覆盖安装；`latest-build` 每次成功构建会替换为最新安装包。安装包放在私有 Release 中，不使用 Actions 长期存储大文件。

发布新版时，一并增加 `app/src/main/AndroidManifest.xml` 的 `android:versionCode`，并按需要更新 `android:versionName`。目前源码标记为 1.2.16；第十一批动作复核仍处于 `initial_validation`，迁移保留原状态。

## 项目入口

| 路径 | 用途 |
| --- | --- |
| `app/src/main/java/` | Android 界面、训练、饮食、健康记录与 AI 客户端 |
| `app/src/main/assets/` | 中文动作、食谱、快捷餐与动作复核账本 |
| `app/src/main/res/raw/` | 已封装的离线动作动画与语音 |
| `assets/` | 原始图稿、动作修复批次和人工复核证据 |
| `scripts/` | 测试、数据验证、构建与素材制作工具 |
| `docs/` | 设计、科学依据、复核规则和历史交付说明 |
| `docs/archive/build-records/` | 从旧 build 目录保存的历史源码快照与验收记录 |

继续动作复核前，先读 [持续复核流程](docs/exercise-review-workflow.md) 和 `assets/motion_repairs/review-workflow-state.json`。自动检查不会授予动作“已复核”状态。

## 本地检查与构建

现有构建使用 Android SDK 工具直接编译 Java，无需 Gradle。准备 JDK 21、Android SDK 平台 `android-36`、Build Tools `36.1.0`、Python 3.12、jq、zip 和 ffmpeg（含 ffprobe）。macOS 可沿用 Android Studio 的 JDK；Linux 设置 `JAVA_HOME` 和 `ANDROID_HOME`。

```bash
python3 -m pip install -r requirements-ci.txt
bash scripts/run_domain_tests.sh
python3 scripts/audit_exercise_reviews.py
bash scripts/build_android_debug.sh
```

构建输出为 `build/timehouse-debug.apk`。原有签名密钥保存在本地 `.signing/debug.keystore`，该目录不会进入 Git。GitHub Actions 使用仓库 Secret `ANDROID_DEBUG_KEYSTORE_BASE64` 恢复同一密钥。

重新制作图像素材时另需 numpy、OpenCV；已有动画直接参与构建。重新生成中文语音需 macOS 的 `say`，云端只检查已保存的语音。手机与模拟器交互 QA 在本地运行。

素材授权见 [第三方声明](THIRD_PARTY_NOTICES.md)。迁移与本地清理记录见 [GitHub 迁移说明](docs/github-migration.md)。

网页操作参考：[GitHub 网页编辑器](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor)。
