# 第五批动作复核 · 2026-09-14

本批核查 10 条资料库动作，保留原姿势修复 3 张动态图，2 条已通过完整复核。当前验收状态以 `review-result.json` 为准；另外 8 条仍为未复核。没有调用图片生成，没有重试上批失败的深蹲和 TRX 草稿。

## 图片修复

- 1427 侧卧单腿髋外展：第二／第四帧右移 4 px，第三帧下移 57 px；下侧肘、上侧手掌、下侧小腿贴地边缘同时稳定。两脚在初始姿势重叠，脚趾整块会混入正在抬起的上侧脚，因此支撑腿采用未被遮挡的贴地边缘测量。修后残差不超过 2 px。
- 0298 哑铃单臂交叉锤式弯举：第二／第四帧右移 22 px，第三帧下移 2 px；两脚及头部残差不超过 2 px。左右各做计次，原来的名字无法表达单侧处方，现已明确。
- 0001 四分之三仰卧起坐：第三帧下移 20 px，脚部与臀部固定。纠正起坐名称及主肌群，但变式的起止范围仍需匹配原始教练示范；图片修好后继续保持未复核。原 Bodybuilding.com 对应页面本轮无法读取，没有用相似变式自动替代其复核证据。

三个动作均保留原四帧、2.36 秒循环和前景像素；只平移封装，无人体拉伸、插帧、光流和混合重影。`register_frames.py` 可复现，`registration-validation.json` 保存哈希、偏移与测量结果。

## 图文、计次和待办

1427 核对侧卧、抬上侧直腿和不翻髋，删去“尽可能高”的错误提示；0298 明确单臂完成后换侧，核对肘屈肌群。两条已通过移动端验收，随安装包交付。

其余条目记录如下：

| ID | 结果 |
|---|---|
| 0292 | 补充扶凳步骤、纠正主肌群；图片支撑基本稳定，但额外训练凳尚未进入完整选材条件，保持未复核 |
| 1428 | 只有手腕往返位置，没有完整圆周；高亮肌群在上臂，待修图 |
| 0295 | clean 应译为翻举；现图的接铃与屈膝阶段不清晰，继续待修图 |
| 3016 | 卷起帧脚与臀的水平位移相差约 8 px，不能整体对齐 |
| 0296 | 实际条目应是窄握卧推，现图误画成坐姿过顶推举；已纠正名称及仰卧步骤，图片仍待重制 |
| 0297 | 名称加入单臂以正确计算左右两侧；左右脚和凳子的位移不同，待修图及训练凳条件复核 |
| 0002 | 最大侧弯时两脚水平位移相差 13 px，不能整体对齐 |
| 0001 | 图片位置修复，变式范围仍待核对 |

`selected.json` 与 `before/` 保存原始条目和原图；`contact-*.jpg` 是原四帧初筛图；`measure_anchors.py`、`anchor-measurements.json` 是测量过程。生产变更由 `apply_review.py` 记录，该脚本只供复现，不可重复执行。

## 资料依据

- [ACE：侧卧髋外展](https://www.acefitness.org/resources/everyone/exercise-library/38/side-lying-hip-abduction/)
- [Muscle & Fitness：交叉锤式弯举](https://www.muscleandfitness.com/exercise/workouts/arm-exercises/cross-body-dumbbell-hammer-curl/)
- [PureGym：单臂哑铃划船与扶稳固支撑物变式](https://www.puregym.com/exercises/back/rows/single-arm-dumbbell-row/)
- [CrossFit：clean 的提铃至肩与接铃过程](https://www.crossfit.com/essentials/foundational-movement-clean-what-is-a-clean)
- [Muscle & Strength：窄握哑铃卧推](https://www.muscleandstrength.com/exercises/close-grip-dumbbell-press.html)
- [NHS：站姿侧弯](https://www.nhs.uk/live-well/exercise/flexibility-exercises/)

## 验证

领域／数据检查和构建已通过，APK 内只修改 7 条动作定义和 3 个 raw 媒体；既有已复核动作的内容未改动。新增侧卧下肢动作可在肩腰受限时进入候选，因此“空候选不退回未复核”的测试夹具补充严重膝部限制，保持原断言。

最终模拟器检查、安装包路径和签名见 `build/review5-20260914/verification-summary.json`。实体手机未复测。

最终结果：42 项模拟器检查全部通过，三张修复图的实际循环已逐帧查看；安装包签名与上一版一致，21 条复核媒体及资料哈希均核对通过。已交付 1.2.9 安装包。
