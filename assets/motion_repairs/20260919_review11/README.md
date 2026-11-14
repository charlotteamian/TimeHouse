# 第十一批动作复核证据（`20260919_review11`）

本批检查 10 条（`0467`、`0323`、`0469`、`0324`、`0471`、`0325`、`0472`、`0326`、`0473`、`0327`）。10 条全部完成修复或同画风重绘并通过支撑锚点像素级校验，经用户审阅确认成品后正式入账；累计 47 条已复核、1308 条未复核。

## 计划

- [x] 保留原件、逐帧检查，核对匹配来源与固定支点。
- [x] 修正 10 条动作资料，5 个动作原图四帧整数平移校准，5 个动作同画风 2×2 重绘并锁定固定支点。
- [x] 未复核状态下检查真实资料加载、器械条件和 Android 完整循环。
- [x] 写入 10 条通过项；完成实际开练与器械门控验证。
- [x] 核对 APK、素材、资料哈希及同签名覆盖安装，完成第十一批归档。

## 逐项判定

| ID | 视觉与资料结论 |
| --- | --- |
| 0467 | 通过（同画风重绘）。纠正“猩猩下巴”机翻误名为“反握悬挂举腿引体”，补单杠需求。重绘反握悬垂 → 半程引体抬膝 → 下巴过杠屈膝收腹 → 半程回落四帧闭环，左右立柱底座与双手握点 4 处锚点残差 `0.0 px`，匹配 `1.0`。 |
| 0323 | 通过（原图校准）。核对“哑铃上斜单臂侧平举”，补上斜训练凳与单侧计次规则。原四帧前后凳脚与双脚 4 处固定支点残差 `0.0 px`，匹配 `>= 0.9978`。 |
| 0469 | 通过（同画风重绘）。纠正“腹股沟卷腹”为“仰卧分腿屈膝卷腹”。重绘并固定骨盆、分腿屈膝与双脚踩地支撑，消除原图脚尖跨帧泄露与地面黑斑，3 处支撑锚点残差 `0.0 px`，匹配 `>= 0.9995`。 |
| 0324 | 通过（原图校准）。核对“哑铃上斜掌心相对推举”，补上斜训练凳。第 3 帧下移 `5 px` 恢复顶部安全白边并固定膝下底座与双脚，4 处支撑锚点残差 `0.0 px`，匹配 `1.0`。 |
| 0471 | 通过（同画风重绘）。核对“靠墙倒立俯卧撑”，补墙面与高位支撑筛选。修复原图屈肘下落时双掌沿地面外滑超过 `20 px` 问题，墙面与双掌撑地 4 处锚点残差 `0.0 px`，匹配 `1.0`。 |
| 0325 | 通过（同画风重绘）。纠正“哑铃上斜推举”为“哑铃上斜肩部推举”，补上斜训练凳。重绘肩高起始 → 半程推起 → 过顶推举锁定 → 半程回落四帧闭环，消除大腿垂持跳跃与贴顶问题，4 处支撑锚点残差 `0.0 px`，匹配 `1.0`。 |
| 0472 | 通过（原图校准）。核对“悬挂直腿抬腿”，补单杠与核心屈曲模式。原四帧左右立柱底座与双手握点 4 处支撑锚点残差 `0.0 px`，匹配 `>= 0.9899`。 |
| 0326 | 通过（原图校准）。纠正“哑铃上斜后侧平举”为“哑铃俯卧上斜后侧平举”，补上斜训练凳与水平外展模式。整数平移校准后前后凳脚与足部 3 处支撑锚点残差 `0.0 px`，匹配 `>= 0.9643`。 |
| 0473 | 通过（同画风重绘）。纠正“悬挂劈叉”机翻误名为“悬挂直腿折刀举腿”，补单杠。重绘赤足垂直悬垂 → 90° 水平直腿抬起 → 高折刀举腿触杠 → 90° 水平回落四帧闭环，立柱底座与握点 4 处锚点残差 `0.0 px`，匹配 `>= 0.9980`。 |
| 0327 | 通过（原图校准）。纠正“哑铃上斜划船”为“哑铃俯卧上斜划船”，补上斜训练凳与水平拉模式。整数平移 `(0,0), (8,0), (0,10), (8,0)` 校准后双脚与前后凳脚 3 处支撑锚点残差 `<= 1.0 px`，匹配 `>= 0.9613`。 |

## 资料来源

- `0467`：[Muscle & Strength Gorilla Chin](https://www.muscleandstrength.com/exercises/gorilla-chin.html)
- `0323`：[Muscle & Strength Incline One-Arm Dumbbell Lateral Raise](https://www.muscleandstrength.com/exercises/incline-one-arm-dumbbell-lateral-raise.html)
- `0469`：[Muscle & Strength Abdominal Crunch](https://www.muscleandstrength.com/exercises/crunch.html)
- `0324`：[Muscle & Strength Neutral-Grip Incline Dumbbell Bench Press](https://www.muscleandstrength.com/exercises/neutral-grip-incline-dumbbell-bench-press.html)
- `0471`：[Muscle & Strength Handstand Push-Up](https://www.muscleandstrength.com/exercises/handstand-push-up.html)
- `0325`：[Muscle & Strength Seated Dumbbell Press](https://www.muscleandstrength.com/exercises/seated-dumbbell-press.html)
- `0472`：[Muscle & Strength Hanging Leg Raise](https://www.muscleandstrength.com/exercises/hanging-leg-raise.html)
- `0326`：[StrengthLog Reverse Dumbbell Flyes](https://www.strengthlog.com/reverse-dumbbell-flyes/)
- `0473`：[CrossFit The Toes-to-Bar](https://www.crossfit.com/essentials/the-toes-to-bar)
- `0327`：[Muscle & Strength Chest-Supported Dumbbell Row](https://www.muscleandstrength.com/exercises/chest-supported-dumbbell-row.html)
