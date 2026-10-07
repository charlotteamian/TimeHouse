# 第二批动作复核 · 2026-09-13

本批查看 11 条：上批遗留的 0276、3013、1685、0805、0809，以及 0300、0313、0336、1373、2368、3769。

已通过三条：

- **0300 哑铃罗马尼亚硬拉**：原图最低位的双脚同时偏移 (4,-18) px，原帧左移 4 px、下移 18 px 后对齐。两只脚的匹配残差均为 (0,0)，未改变帧数、时长或其他三个姿势。根据实际图示纠正变式名称、步骤、肌群和髋铰链模式。
- **0313 哑铃锤式弯举**：图示双脚固定、使用中立握，修正原说明中“转掌朝前”的错误。保留原图。
- **1685 深蹲至头顶伸展**：重制四格动作图，经一次手部边界修正后，使用原姿势平移对齐和统一白边封装成四帧示范；双脚模板匹配残余差异不超过 2 px，手部完整。修改说明和动作模式，补上肩部、腰部负荷标记。

`repair_existing.py` 从本目录 `before/dataset_motion_0300.webp` 可复现修图成品；`0300-validation.json` 保存哈希、位移和支撑点检查。`0300-fixed.gif` 可查看实际循环。

`pack_squat.py` 从最终源图 `1685.png` 生成 `1685-fixed.webp`；支撑点检查见 `1685-validation.json`，四帧总时长仍为 2.36 秒。`1685-fixed.gif` 和 `1685-fixed-sheet.jpg` 分别供循环及逐帧检查。

原本没有图的种子条目“哑铃推举”接入现有同动作 `dataset_motion_0426` 示范；补图没有自动授予该条目复核状态。

## 重制结果和未通过项

使用内置 imagegen 处理 5 个动作，共得到 7 张源图（含两次定向精修）。最终仅采用 1685。死虫式 0276、地板臀桥 3013、TRX 悬挂分腿蹲 0809 的草稿仍存在头部／骨盆、头部／脚底或前脚／上方锚点的独立漂移；死虫式还存在相邻格内容越界。TRX 站姿前伸 0805 已纠正朝向，但精修后脚底与固定锚点仍不同步。这 4 个动作均保留原素材和未复核状态。

生成期间曾遇到额度限制；用户继续后，确认额度恢复并完成 1685 和 0805 的生成与精修。因此目前未通过项的原因是画面质量，不是服务额度。

本批生成提示词保存在 `prompts.json`、`prompts-b.json`、`prompts-pending.json`，两次精修提示词为 `1685-refinement.txt` 和 `0805-refinement.txt`，工具为内置 imagegen。原图在 `before/` 中，未采用草稿及哈希见 `draft-manifest.json`。详细检查结果在 `review-result.json`、各动作的 validation JSON 和 `build/review2-20260913/generated-anchor-check.json`。

## 复核参考

- [NASM 哑铃罗马尼亚硬拉](https://www.nasm.org/resource-center/exercise-library/dumbbell-romanian-deadlift)
- [PureGym 锤式弯举](https://www.puregym.com/exercises/arms-and-shoulders/bicep-curl/hammer-curls/)
- [NASM 死虫式](https://www.nasm.org/resource-center/exercise-library/dead-bug)
- [NASM 地板臀桥](https://www.nasm.org/resource-center/blog/training/why-the-glute-bridge-belongs-in-almost-every-client-program)
- [TRX 基础动作与悬挂弓步](https://www.trxtraining.com/blogs/news/7-basic-movements)
- [TRX 站姿前伸](https://www.trxtraining.com/blogs/news/standing-ab-exercises)
- [FitMetrics 深蹲至头顶伸展](https://www.fitmetrics.ch/en/exercise/695299ee2c645-squat-with-overhead-reach)

最终页面复查另裁掉 0426 推举首帧底缘的 1 像素串格行；其他帧和全部人体姿势区域不变。
