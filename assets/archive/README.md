# 历史动作媒体原件归档

清理项目 `build/` 前，按原文件名与目录逐字节保留两批历史媒体：

- `raw-backup-20260725/`：1,348 个 WebP，原路径 `build/raw-backup-20260725/`。
- `replaced-static-exercise-images/`：113 个 JPEG，原路径 `build/replaced-static-exercise-images/`。

这些文件在当前 `assets/` 与 `app/src/main/assets/` 中没有字节相同的副本。此目录用于历史追溯，不参与 App 打包，也不改变动作定义或授予复核状态。`inventory.json` 记录每个文件的原路径、归档路径、字节数与 SHA-256，可用于校验复制完整性。
