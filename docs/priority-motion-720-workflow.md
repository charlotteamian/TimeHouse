# 八类器械剩余动作图工作流

## 目标与口径

- 范围只包含 App 映射后的自重、弹力带、哑铃、壶铃、TRX 悬挂带、瑜伽球、BOSU 球、动感单车。
- 初始设备字段筛出最近两批尚未覆盖的 725 个条目；严格语义审计发现 `2400 inverse leg curl (on pull-up cable machine)`、`1766 self assisted inverse leg curl`、`0684 run (equipment)` 和 `3637 wheel run` 被上游误标为自重，但步骤与原动画分别明确依赖绳索机、腿弯举机、跑步机和健腹轮，因此按“仅限八类器械”排除并写入 `scope-exclusions.json`。实际范围为 721 个条目，其中 5 对可复用，因此生成 716 张四阶段源图。
- 质量基线固定为 `assets/motion_repairs/20260910/`：一动作一张 2×2 四阶段图，不恢复旧的“一张图塞三个动作”方案。

## 为什么更省 token

1. 每个动作仍只调用一次内置 ImageGen，一张图同时给出 4 个阶段。
2. 每次输入一张最近合格图作为画风/解剖质量锚点，再输入由 App 原动画自动抽帧得到的动作参考图。动作含义由像素携带，不再为每项人工编写数百词提示。
3. 公共规则由脚本编译，任务状态、prompt 哈希和已有 PNG 都会落盘；中断后只补 `pending`，不重复生成。
4. 先运行本地尺寸、四格、留白、珊瑚红肌群和起止差异检查，再用批量联系表对照英文原名、完整步骤与旧动作图做人工语义复核；这两层 QA 不消耗云端图片额度，只把确认异常项送回重生。
5. 5 个真正重复动作复用同一成品，不进行没有视觉收益的重复调用；4 个上游器械错标项显式排除，不让绳索机、跑步机、健腹轮或腿弯举机内容混入交付包。

## 执行顺序

```bash
/opt/homebrew/Caskroom/miniforge/base/bin/python3 scripts/prepare_priority_motion_workflow.py
```

读取 `assets/motion_repairs/20260910_720/prompts.json`。每个条目使用 `style_reference` 和 `movement_guide` 两张本地参考图调用一次内置 ImageGen，把输出保存为同目录 `<id>.png`。每完成一张重新运行准备脚本即可刷新断点状态。

批量派发启用额度熔断：任何在途请求一旦返回 `usage_limit_reached` 或 HTTP 429，本轮 worker 不再领取新条目；尚未开始和失败的编号继续保持 `pending`，交给下一次定时续跑。这样最多只会损耗当时已经在途的少量请求，不会对整批剩余条目重复发送无效调用。

```bash
/opt/homebrew/Caskroom/miniforge/base/bin/python3 scripts/validate_priority_motion_batch.py
/opt/homebrew/Caskroom/miniforge/base/bin/python3 scripts/build_motion_repairs.py --batch 20260910_720
/opt/homebrew/Caskroom/miniforge/base/bin/python3 scripts/validate_priority_motion_batch.py --assets
bash scripts/run_domain_tests.sh
bash scripts/build_android_debug.sh
/opt/homebrew/Caskroom/miniforge/base/bin/python3 scripts/package_priority_motion_release.py
```

图片全部生成、复核并导入后，先处理本轮追加的强度/体能评估问题，再执行最终测试、构建与打包：

- 在设置中提供明确的“体能评估”管理入口。
- 已有评估可查看并修改，支持重新评估。
- 支持删除当前评估并恢复到“尚未评估”的状态；删除前需要确认，避免误触。
- 删除或重做后，今日训练的强度安全筛查与说明必须立即使用新状态，不继续引用旧评估日期或旧限制。
- 为评估状态迁移、修改、重做、删除及训练计划联动补充领域测试，并在模拟器验证入口可见、流程可完成。

最终打包前还要通过本轮界面和推荐回归：

- 今日 8 / 15 / 25 分钟按钮保持单行并留出明确间距；动作组编辑、排序和删除按钮不可贴合。
- 临时训练继续先覆盖蹲 / 髋 / 推 / 拉 / 核心等动作模式，再在相同模式内对最近完成或刚推荐的动作做软降权；候选不足时允许复用，不能为了“随机”破坏器械、伤痛、恢复或周训练量规则。
- “安排说明”必须直接写明动作模式、时长求解和轮换逻辑，让用户知道为什么推荐这些动作。
- 自定义动作可编辑主要器械，器械字段随动作保存并在重启后恢复。
- 相册图片 / GIF 选择后复制到 App 私有目录，不再长期引用易失效的 `content://` 地址；旧地址失效时显示可恢复提示和“重新选择”，不再提供打不开的浏览器入口。
- 模拟器分别验证推荐轮换与布局、自定义器械与 GIF 重启显示、体能评估与强度联动，并把日志和机器可读检查清单一并放入交付包。

源图检查全部通过后才允许导入；App 资产必须全部为 480×480、4 帧。最终压缩包应包含 APK、`workflow.json`、`scope-exclusions.json`、`manifest.json`、两份 QA JSON 和 SHA-256 清单，源 PNG 单独保留在工程内，避免把约 720 张无损源图塞入安装交付包。

## 质量边界

- 自动检查能守住画布、分格、裁切、前景、肌群色和帧差异，不能独立证明每个复杂动作的医学正确性。
- 本机 `qwen3-vl:8b-instruct` 试跑 165 张时产生 164 个告警，且多次误判标准动作，因此结果仅保留为旁证，不作为放行或重生依据。
- 异常项必须看原图；高风险或名称/步骤冲突的动作不能仅凭自动分数放行。
- 生成图不得覆盖最近两批源图；App 资产导入前保留原 WebP 备份。
- 技术门禁进入 `review` 的条目必须在联系表中人工查看，并用 `record_priority_motion_review.py` 留下显式放行记录；最终打包脚本会拒绝任何未解决项。
- 打包脚本只接受 716 张范围内源图、5 个复用、4 个显式器械错标排除、721 条导入清单、721 个四帧 App 资产、领域测试日志、构建日志、3 组模拟器 UI 回归和 APK 同时存在的状态。交付 ZIP 不重复装入源 PNG，但保留工作流、排除清单、QA、复核、构建和哈希证据。
