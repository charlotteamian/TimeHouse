# 第十二批动作复核证据（20260920_review12）

本批次对队列前 10 个未复核动作（`0474`、`0328`、`0475`、`0329`、`0476`、`0330`、`0484`、`0331`、`0488`、`0332`）逐一核对英文原意、器械要求、目标肌群、动作模式、四步文字说明与四帧完整回放。

## 逐项判定与修复方法

| 编号 | 原名 / 修正后中文名 | 修复方式 | 必需支撑器械 | 固定支点残差 / 最低匹配度 | 权威参考来源 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0474` | 悬挂直腿髋抬高 → **悬挂直腿举腿提臀** | 2×2 解剖插画重绘 + 支点配准 | `单杠` | `0.0 px` / `1.0000` | [ExRx Hanging Straight Leg Hip Raise](https://exrx.net/WeightExercises/RectusAbdominis/BWHangingStraightLegHipRaise) |
| `0328` | 哑铃上斜肩部上举 → **哑铃上斜直臂前锯肌推举** | 2×2 解剖插画重绘 + 支点配准 | `上斜训练凳` | `0.0 px` / `1.0000` | [ExRx Dumbbell Incline Shoulder Raise](https://exrx.net/WeightExercises/SerratusAnterior/DBInclineShoulderRaise) |
| `0475` | 悬挂直腿抬高 → **悬挂直腿举腿** | 原四帧整数平移校准 | `单杠` | `<= 1.0 px` / `0.9813` | [ExRx Hanging Straight Leg Raise](https://exrx.net/WeightExercises/HipFlexors/BWHangingStraightLegRaise) |
| `0329` | **哑铃上斜耸肩** | 原四帧整数平移校准 + 底座稳定 | `上斜训练凳` | `0.0 px` / `0.9907` | [ExRx Dumbbell Shrug](https://exrx.net/WeightExercises/TrapeziusUpper/DBShrug) |
| `0476` | 悬挂直腿转体髋抬高 → **悬挂直腿转体举腿** | 原四帧整数平移校准 | `单杠` | `<= 1.0 px` / `0.9833` | [ExRx Hanging Twisting Leg Hip Raise](https://exrx.net/WeightExercises/Obliques/BWHangingTwistingLegHipRaise) |
| `0330` | 哑铃上斜三头肌伸展 → **哑铃上斜仰卧臂屈伸** | 2×2 解剖插画重绘 + 支点配准 | `上斜训练凳` | `0.0 px` / `1.0000` | [ExRx Dumbbell Incline Triceps Extension](https://exrx.net/WeightExercises/Triceps/DBInclineTriExt) |
| `0484` | 屈膝臀抬高 → **仰卧屈膝臀桥** | 2×2 解剖插画重绘 + 地面支撑锁定 | 无（`自重`） | `0.0 px` / `0.9994` | [ACE Glute Bridge](https://www.acefitness.org/resources/everyone/exercise-library/49/glute-bridge/) |
| `0331` | 哑铃上斜扭转飞鸟 → **哑铃上斜旋转飞鸟** | 原四帧整数平移校准 + 底座稳定 | `上斜训练凳` | `0.0 px` / `0.9617` | [ExRx Dumbbell Incline Fly](https://exrx.net/WeightExercises/PectoralClavicular/DBInclineFly) |
| `0488` | 卧式超伸 → **罗马椅背屈伸** | 2×2 解剖插画重绘 + 罗马椅支点配准 | `带勾脚的下斜训练凳` | `0.0 px` / `1.0000` | [ExRx Back Extension](https://exrx.net/WeightExercises/ErectorSpinae/BBBentKneeGoodMorning) |
| `0332` | 哑铃铁十字 → **哑铃十字侧平举** | 原四帧整数平移校准 + 下肢稳定 | 无（`哑铃`） | `0.0 px` / `1.0000` | [ExRx Dumbbell Lateral Raise](https://exrx.net/WeightExercises/DeltoidLateral/DBLateralRaise) |

## 目录产物

- `before/`：复核前的原始 `exercises_1324.json`、`exercise_reviews.json`、`AndroidManifest.xml` 与 10 个 `.webp` 动画备份。
- `<id>-generated.png`：5 个重绘动作（`0474`、`0328`、`0330`、`0484`、`0488`）的 2×2 原始母版。
- `<id>-fixed-0..3.png`、`<id>-fixed-sheet.jpg`、`<id>-fixed.gif`、`<id>-fixed.webp`：配准后的四帧序列、2×2 拼图与 2.36 秒循环动画。
- `contact-1.jpg`、`contact-2.jpg`：10 个动作的四帧总览表。
- `anchor-measurements.json`、`registration-validation.json`：31 个固定支撑锚点测量数据与前景完整性校验。
