# 解剖动作起止帧 Prompt v1

## 执行模式

- 使用内置 `imagegen`，每次生成一张独立 sheet。
- 每张最多传入 5 张本地风格参照；按动作分类从 `assets/motion_sheets/` 选择最相关图片。
- 参照图只用于风格、人物、器械、配色和 3 × 2 布局，不做拼贴或原图编辑。

## 共享提示词

```text
Use case: scientific-educational
Asset type: production source sheet for exercise animation start/end frames
Primary request: Create one new anatomical exercise motion sheet containing exactly three start/end pose pairs in a strict 3-row by 2-column grid. Each row is one exercise. Left cell is START; right cell is END.
Canvas/layout: landscape 3:2 ratio matching the references; equal-size cells; very thin pale-gray center divider and row dividers; pure white background; generous consistent padding; no cropping; no captions or labels.
Subject/style: match the reference sheets very closely. Use the same adult male anatomical fitness model across every cell, grayscale exposed-muscle medical illustration, realistic proportions, close-cropped dark hair, black shorts, barefoot. Equipment is matte black and gray, with green resistance bands only where required. Only the primary target muscles are tinted muted coral red. Fine gray anatomical linework, clean educational rendering, soft minimal grounding shadow only.
Scientific constraints: anatomically plausible joint positions and equipment interaction; exactly one complete body per cell; correct number of limbs, hands, and feet; matching identity, scale, viewpoint, equipment anchors, and camera within each pair; clearly different start and end range of motion.
Avoid: any text, arrows, numbers, logos, watermark, labels, decorative background, gym room, extra props, extra people, floating equipment, cut-off limbs, skeletal X-ray look, blue muscles, glossy plastic skin, inconsistent camera, or mixed exercise poses.
```

## 每行动作块

为每个动作补充一段独立、可判定的动作说明：

```text
Row N exercise: <English exercise name>, target <primary target>.
View: <front / side / rear three-quarter>.
Equipment: <type, fixed anchors, grip and support points>.
START: <joint positions and body alignment>.
END: <joint positions, range of motion and body alignment>.
Highlight <specific muscles> in coral red.
Keep <identity, scale, viewpoint, equipment anchors and camera> identical.
```

动作名或数据说明有歧义时，必须先把可见关节运动写清楚。若动作名与目标肌群冲突，则将该项留在待处理队列，不生成错误解剖图。

## 参照选择

- 背：`sheet_back_1.png`、`sheet_back_2.png`、`sheet_legs_back_2.png`
- 胸/推：`sheet_push_1.png`、`sheet_push_2.png`、`sheet_core_arms_2.png`
- 腰腹：`sheet_core_1.png`、`sheet_core_arms_2.png`、`sheet_legs_back_2.png`
- 腿臀：`sheet_legs_1.png`、`sheet_legs_back_2.png`、`sheet_core_1.png`
- 肩/手臂：`sheet_core_arms_2.png`、`sheet_push_2.png`、`sheet_back_2.png`

## 单张 QA

1. 先查 3 × 2 布局、完整人体、无文字、无多余人物。
2. 再查每行起止帧的关节变化、器械锚点和相同机位。
3. 最后查目标肌群标红；发现名称、步骤和目标肌群不一致时不通过。
4. 通过后在 `scripts/data/anatomy_sheet_manifest.json` 登记为 `qa_passed`，再生成 480 × 480 GIF 预览。
