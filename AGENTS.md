# 时光屋项目约定

- 使用 `scripts/build_android_debug.sh` 直接构建，项目没有 Gradle 构建入口。
- 修改后按范围运行 `scripts/run_domain_tests.sh`、`scripts/audit_exercise_reviews.py` 和 APK 构建；手机/模拟器交互不由云端数据检查代替。
- 原始素材和动作定义属于项目源文件，不按缓存清理。动作资料、媒体或审核相关修改前读取 `docs/exercise-review-workflow.md`、`docs/anatomy-motion-style-contract.md` 和 `assets/motion_repairs/review-workflow-state.json`。
- 保留未完成批次，技术检查或生成成功不能自动授予动作“已复核”状态。
- `.signing/debug.keystore` 是覆盖安装使用的原有密钥，不删除、不重新生成、不提交到 Git。云端通过 `ANDROID_DEBUG_KEYSTORE_BASE64` Secret 恢复同一密钥。
- 仓库和 Release 保持私有。手机更新读取 `latest-build` Release，私人访问令牌由用户在手机配置，不嵌入源码或安装包。
- 历史 build 文本记录已归档到 `docs/archive/build-records/`，原位置对应关系见其 `inventory.json`。
