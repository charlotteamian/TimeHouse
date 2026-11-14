# 第一百三十六批动作复核（SeedExercises 清零封板）· 2027-01-22

本批对 `SeedExercises.java` 剩余最后 14 条带本地示范动图的内置动作进行逐帧可视化与像素边界/支撑区核验，全部转入 `待修图` 暂缓修理清单。至此，全库 `1355` 项（`1324` 条扩展库 + `31` 条核心种子动作）的 `待核逻辑` 队列正式清零（`待核逻辑 = 0`，`已完成 = 142`，`待修图 = 1210`，`待补图 = 3`）。

## 核查结论（0 通过 / 14 转入待修图）

### 1. 程序插值 10 帧轮廓图与未审核占位（8 条）
1. `exercise_glute_bridge`（臀桥，`motion_glute_bridge.webp`）：`10 帧 × 70ms`，角落 `[253,253,253]`、`L:14/R:14 < 15`，混标杠铃且缺 `primaryMuscles`。
2. `exercise_romanian_deadlift`（罗马尼亚硬拉，`motion_romanian_deadlift.webp`）：`T:14/B:14 < 15`、`y>=370 IoU = 0.1838`，步骤含“保持”。
3. `exercise_step_up`（台阶上步，`motion_step_up.webp`）：`T:13/B:13 < 15`、`y>=370 IoU = 0.1581`，单侧计数（`perSide = true`），缺 `requiredEquipment = ["稳固踏台"]`、步骤含“保持”。
4. `exercise_dead_bug`（死虫，`motion_dead_bug.webp`）：`L:14/R:14 < 15`，中段四肢半透明叠影，`perSide = true`，步骤含“保持”。
5. `exercise_plank`（平板支撑，`motion_plank.webp`）：`L:13/R:12 < 15`，帧间几乎静止（`mean_d02 = 0.66`），需重制标准 4 帧静态支撑图。
6. `exercise_pallof_press`（帕洛夫抗旋推，`motion_pallof_press.webp`）：`L:14/R:13 < 15`、`y>=370 IoU = 0.0368`。
7. `exercise_bird_dog`（鸟狗，`motion_bird_dog.webp`）：`L:14/R:13 < 15`，中段叠影，对侧交替动作缺“双侧”声明（`perSide = false`）、步骤含“保持”。
8. `custom_inverted_row_unverified`（自定义倒立划船，`motion_inverted_row.webp`）：`L:13/R:12 < 15`、`y>=370 IoU = 0.3750`；仍为 `USER_UNVERIFIED` 占位（`装备 = ["神秘器械"]`）。

### 2. 有边距或支撑区位移瑕疵的 4 帧实绘示范图（6 条）
9. `exercise_goblet_squat`（杯式深蹲，`motion_goblet_squat.webp`，`380ms × 4`，同 `1760`）：白底清晰，但 `y>=370 IoU = 0.7052`、`y>=415 IoU = 0.9100 < 0.96`（`F3` 前脚掌外移 `+6..12 px`），另混标壶铃、步骤含“保持”。
10. `exercise_dumbbell_curl`（哑铃弯举，`motion_dumbbell_curl.webp`，`380ms × 4`，同 `0294`）：角落 `[254,254,254]`、头部顶缘 `T = 4 < 15 px`。
11. `exercise_trx_row`（TRX 反向划船，`dataset_motion_0808.webp`，`380ms × 4`）：`y>=370 IoU = 0.8734`、`y>=415 IoU = 0.8558 < 0.96`（`F1` 鞋底高于 `F2–F4` 约 `28 px` 且 `F3` 墙面锚点上跳 `8 px`），步骤含“保持”。
12. `exercise_dumbbell_overhead_press`（哑铃推举，`dataset_motion_0426.webp`，`380ms × 4`）：角落 `[253,253,252]`、`T:0/B:1 < 15 px`（顶底皆触边）、`y>=370 IoU = 0.8993`，步骤含“保持”。
13. `exercise_kettlebell_swing`（壶铃摇摆，`dataset_motion_0549.webp`，`380ms × 4`）：`y>=370 IoU = 0.9465`、`y>=415 IoU = 0.0000`（`F1` 底缘 `y=451` 较 `F2–F4 y=406` 下移 `45 px`）。
14. `exercise_pushup`（俯卧撑，`dataset_motion_0662.webp`，`380ms × 4`）：角落 `[254,254,254]`、`R = 2 < 15 px`（右脚尖贴边），步骤含“保持”。
