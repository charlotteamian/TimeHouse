# 第一百三十五批动作复核 · 2027-01-21

本批核查 `SeedExercises.java` 中前 14 条带本地示范动图的内置种子动作，结合全量帧分解表 `contact-seed-1.jpg`、四帧条带图与像素边界/支撑区 IoU 实测完成逐项审查：

## 核查结论（0 通过 / 14 转入待修图）

### 1. 程序插值 10 帧轮廓图（12 条，待重制为标准 4 帧关键帧图）
下列 12 项共用旧版程序插值 10 帧（`70ms × 10`）青蓝轮廓动图：存在角落非纯白像素 `[253, 253, 253]`、最小边距不足 `15 px`（`2..14 px`）、中段帧肢体半透明叠影重影，且多数底部支撑区 `y >= 370` `IoU < 0.96`；同时 `SeedExercises` 中均缺 `primaryMuscles`（`[]`），多条步骤含“保持”并缺少支撑器械约束（如墙壁、上斜支撑台、手扶支撑物、稳定座椅）：
1. `exercise_lat_pulldown`（高位下拉，`motion_lat_pulldown.webp`）：`T:14, B:11 < 15`，`IoU = 0.4367`，步骤一含“保持”。
2. `exercise_band_row`（弹力带划船，`motion_band_row.webp`）：`L:14, R:13 < 15`，`IoU = 0.6943`，步骤含两处“保持”。
3. `exercise_one_arm_dumbbell_row`（单臂哑铃划船，`motion_one_arm_dumbbell_row.webp`）：`L:12, R:14 < 15`，`IoU = 0.7786`，单侧计数（`perSide = true`），步骤提及一手支撑但 `requiredEquipment = []`。
4. `exercise_seated_row`（坐姿划船，`motion_seated_row.webp`）：`L:14, R:14 < 15`，`IoU = 0.3544`，步骤三含“保持”。
5. `exercise_band_pulldown`（弹力带下拉，`motion_band_pulldown.webp`）：`T:2, B:14 < 15`，`IoU = 0.1116`。
6. `exercise_bent_over_barbell_row`（杠铃俯身划船，`motion_bent_over_barbell_row.webp`）：`T:8, B:14 < 15`，`IoU = 0.3847`，步骤含两处“保持”。
7. `exercise_face_pull`（面拉，`motion_face_pull.webp`）：`L:14, R:14 < 15`，`IoU = 0.1706`。
8. `exercise_wall_pushup`（墙壁俯卧撑，`motion_wall_pushup.webp`）：`L:14, R:14 < 15`，`IoU = 0.3908`，缺 `requiredEquipment = ["墙面"]`，步骤含“保持”。
9. `exercise_incline_pushup`（上斜俯卧撑，`motion_incline_pushup.webp`）：`L:12, R:13 < 15`，`IoU = 0.4353`，缺稳固踏台/上斜训练凳支撑要求，步骤含两处“保持”。
10. `exercise_seated_chest_press`（坐姿推胸，`motion_seated_chest_press.webp`）：`T:14, B:14 < 15`，`IoU = 0.5392`。
11. `exercise_band_external_rotation`（弹力带外旋，`motion_band_external_rotation.webp`）：`L:13, R:13 < 15`，`IoU = 0.1959`。
12. `exercise_sit_to_stand`（坐站，`motion_sit_to_stand.webp`）：`T:12, B:7 < 15`，`IoU = 0.1652`，缺座椅支撑约束。

### 2. 有瑕疵的 4 帧实绘示范图（2 条）
13. `exercise_dumbbell_bench_press`（哑铃卧推，`motion_dumbbell_bench_press.webp`，`380ms × 4`，对应 `0289`）：角落 `[253,253,253]`、右缘 `R = 3 < 15 px`，且 `SeedExercises` 缺 `requiredEquipment = ["平板训练凳"]` 与 `primaryMuscles`。
14. `exercise_seated_shoulder_press`（坐姿肩推，`motion_seated_shoulder_press.webp`，`380ms × 4`，对应 `0405`）：`y >= 370 IoU = 0.9234`（`y >= 415 IoU = 0.8392 < 0.96`）、`F3` 头与靠背等比缩小约 12–16 px，且器械并列 `固定器械` 与缺 `requiredEquipment = ["直立靠背训练凳"]`。
