# 时光屋 1.2.18：公开下载和应用内更新

按用户 2026-10-17 的新要求，`charlotteamian/TimeHouse` 仓库和 `latest-build` Release 改为公开。

旧版本的私有更新入口需要先手动覆盖安装本次新版一次：[下载 APK](https://github.com/charlotteamian/TimeHouse/releases/download/latest-build/timehouse-debug.apk)。随后直接进入「设置 → 应用更新 → 检查更新」，无需登录或配置 GitHub 令牌。

- 删除令牌输入、保存与清除入口，网络请求不再使用 Authorization。
- 启动自动清理旧 `github_updates` 偏好与 `fitness_github_update_token_v1` Keystore 密钥；健身数据和 AI 设置保留。
- 保留大小、SHA-256、包名、版本号、版本名和原签名校验；保留下载取消、临时包清理与系统安装授权流程。
- `main` 成功构建后更新公开 `latest-build`，最后发布 `update.json`；网页编辑方式仍见 [README](../../README.md)。

本次不改变动作素材、已复核状态或未完成的第十一批。

## 已验证

[云端检查与构建](https://github.com/charlotteamian/TimeHouse/actions/runs/38992109920)通过，发布版本 `1.2.18+5`，数字版本号 `2026101706`。公开仓库、Release、更新元数据及安装包均已通过匿名访问验证。

本地领域与资料检查、36 项更新策略检查、10 项设置与旧凭据迁移检查通过。独立 Android 16 / SDK 36 ARM64 模拟器实际下载 479,885,009 字节安装包，完成大小、SHA-256、版本、签名、只读 Provider 和临时下载清理验证，再经 App 设置和系统安装器覆盖安装；11 项完整安装检查通过。安装前后偏好文件逐字节相同，训练记录和 AI 设置保留，更新后能检查到“当前已是最新版本”。

详细结果、安装前后合成数据与截图见 [验证记录](../verification/public-updates-2026-10-17.json)。实体手机尚未测试。

验证后已删除本次 `build/`、专用模拟器磁盘、临时安装包和中断下载留下的 Git 临时 pack，清除约 6.7 GiB 临时占用；项目约 2.6 GiB，原始素材、动作复核记录及原签名密钥保留。见 [清理记录](../verification/public-updates-cleanup-2026-10-17.json)。
