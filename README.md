# 时光屋

个人 Android 健身与饮食记录应用。包名 `com.restartday.fitness`，最低 Android 9（API 28）。完整 Java 源码、离线动作动画、中文资料、原始图稿、复核记录和制作脚本均在本仓库中。

仓库和安装包已公开，无需登录或配置 GitHub 访问令牌即可下载、检查更新。应用内填写的 AI API 密钥和个人记录保存在手机端；签名密钥通过 GitHub Actions Secret 保存，不在仓库或安装包中。

## 直接在 GitHub 更新

1. 打开 [项目仓库](https://github.com/charlotteamian/TimeHouse)，登录自己的 GitHub 账号。
2. 打开文件并点编辑按钮；修改多个文件时，在仓库页面按 `.`，或直接进入 [网页代码编辑器](https://github.dev/charlotteamian/TimeHouse)。
3. 在 Source Control 中提交修改，选择提交到 `main`；源码、资料或构建脚本变更会自动运行检查和构建。只改说明文档或原始图稿时，可到 Actions 手动运行。
4. 到 [Actions](https://github.com/charlotteamian/TimeHouse/actions/workflows/android.yml) 查看结果；检查与构建通过后，从 [最新开发构建](https://github.com/charlotteamian/TimeHouse/releases/tag/latest-build) 下载 `timehouse-debug.apk`。

网页编辑器的修改需要提交才会同步到 GitHub。APK 使用原有签名，可覆盖安装；`latest-build` 每次成功构建会替换为最新安装包。安装包放在公开 Release 中，不使用 Actions 长期存储大文件。

云端构建会自动增加安装包版本号，并在版本名后添加构建序号，如 `1.2.18+5`，因此后续 GitHub 修改会被 App 识别为新版。需要调整基础版本时修改 `app/src/main/AndroidManifest.xml`，不要降低其 `android:versionCode`。目前源码标记为 1.2.18；第十一批动作复核仍处于 `initial_validation`，迁移保留原状态。

## 从 App 更新

首次从 [最新版本](https://github.com/charlotteamian/TimeHouse/releases/tag/latest-build) 下载 `timehouse-debug.apk` 并覆盖安装。以前安装的私有更新版本需手动安装本次新版一次；之后到「设置 → 应用更新」点「检查更新」，有新版时可下载并打开系统安装界面。首次安装可能需要允许“时光屋”安装应用。

检查和下载均无需登录、无需令牌。新版启动时会删除旧更新功能保存的令牌及其加密密钥，训练、饮食、健康记录和 AI 设置保留。安装前校验文件大小、SHA-256、包名、版本号和原有签名。每次成功的云端构建会最后发布 `update.json`，供 App 检查版本。

本次公开更新与模拟器完整覆盖安装的验证见 [1.2.18 发布记录](docs/releases/2026-10-17-public-updates.md)。


## 项目入口

| 路径 | 用途 |
| --- | --- |
| `app/src/main/java/` | Android 界面、训练、饮食、健康记录与 AI 客户端 |
| `app/src/main/assets/` | 中文动作、食谱、快捷餐与动作复核账本 |
| `app/src/main/res/raw/` | 已封装的离线动作动画与语音 |
| `assets/` | 原始图稿、动作修复批次和人工复核证据 |
| `assets/archive/` | 清理前保存的历史媒体原件及 SHA-256 清单 |
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

本地 Git 使用浅层、按需下载的元数据，减少重复存储；完整提交历史保存在 GitHub。需要读取全部历史时可运行 `git fetch --unshallow --filter=blob:none origin`。已经保留的项目源文件仍可直接编辑。

网页操作参考：[GitHub 网页编辑器](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor)。
