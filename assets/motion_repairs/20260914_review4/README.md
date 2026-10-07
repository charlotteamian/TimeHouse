# 第四批动作复核 · 2026-09-14

本批查看 10 个资料库条目，并尝试补齐种子条目“徒手深蹲”的图片。已通过复核的是 0286 哑铃交替肩上推举；其余保持未复核。当前阶段及最终测试结果见 `review-result.json`。

## 修复与纠正

- 0286 原名称“哑铃交替侧平举”与图文不符，实际为交替肩上推举。第二、第四帧右移 15 px，第三帧右移 1 px，双脚匹配残差不超过 2 px；原四帧、2.36 秒时长和前景像素均保留。核对左右交替、每侧动作计总次数以及肩、腰负荷。
- 0287 改为“哑铃坐姿阿诺德推举”；0288 改为“哑铃仰卧上拉”；0290 改为“哑铃坐姿肩上推举”并纠正步骤；0291 改为“哑铃触凳深蹲”并明确手持哑铃。四条需要训练凳，额外器械与支撑点尚未完整复核，不能因名称纠正就授予已复核。
- 0259、0283 的手掌与脚趾不能同时对齐；0658 与上批待修的 0659 是完全相同图片；0871 支撑及姿势比例待修；1368 只有部分往返弧线，未展示完整踝关节画圈方向。五条列入待修图。

## 徒手深蹲生成

内置 imagegen 生成一次、定向精修一次。提示词分别为 `squat-prompt.txt` 和 `squat-refinement.txt`；项目内源图为 `squat-source.png` 和 `squat-refined.png`。精修后最低位远脚仍偏约 13 px，近脚偏差约 2 px，不能通过整帧平移同时固定。两张图均未采用，未继续重复生成；原种子条目保持待补图。草稿哈希见 `draft-manifest.json`。

## 证据和续跑

`selected.json` 保留核查时的条目；`before/` 保留修改前资料。`contact-*.jpg` 是原四帧检查图。`anchor-measurements.json`、`registration-validation.json` 保存支撑点检查，`register_frames.py` 可复现 0286 修复。`0286-fixed.gif` 和 `0286-fixed-sheet.jpg` 可查看循环及各帧。

动作参考：[交替哑铃肩上推举](https://www.muscleandfitness.com/exercise/workouts/shoulder-exercises/alternating-dumbbell-shoulder-press/)、[钻石俯卧撑](https://www.puregym.com/exercises/chest/press-up/diamond-press-ups/)、[NASM 深蹲力学](https://www.nasm.org/resource-center/blog/training/biomechanics-of-the-squat)。图文检查与图片技术检查分别记录；质量未通过项不会为推进数量而提前标记。

## 最终验证

领域／数据检查、构建与 35 项模拟器检查全部通过；包括交替推举计次、肩腰负荷、动态播放、复核标签、训练选材及 TRX 筛选。安装包签名与上一版一致，19 条已复核媒体哈希均通过核对。交付版本 1.2.8；实体手机未复测。完整结果见 `build/review4-20260914/verification-summary.json`。
