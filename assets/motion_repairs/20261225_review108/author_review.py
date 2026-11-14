#!/usr/bin/env python3
"""Author Batch 108 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261225_review108"
VERSION = "1.2.113"
VERSION_CODE = 2026122501

inspected = ["1267", "1268", "1269", "1270", "1272", "1296", "1298", "1299", "1300", "1301"]
review_candidates = []
registered_media = []

definition_updates = {
    "1267": {
        "name_zh": "瑜伽球仰靠龙门架绳索单臂推胸",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["delts", "triceps"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "将龙门架滑轮调整至与球上仰卧胸部齐平高度，上背部仰靠在瑜伽球上，双脚踏实地面挺髋保持桥式躯干平稳。",
            "单手握住绳索手柄置于胸部外侧，手腕中立，非工作手轻搭腹侧辅助对抗身体旋转力矩。",
            "呼气胸大肌发力驱动单臂平稳向前上方推起手柄，直至手臂伸直微屈肘。",
            "在顶点顶峰收缩挤压单侧胸肌并稳定核心停顿 1 秒，吸气受控放缓将手柄收回至胸侧起始位，单侧完成计划次数后换边重复。",
        ],
    },
    "1268": {
        "name_zh": "瑜伽球仰靠龙门架绳索推胸",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["delts", "triceps"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "将双侧龙门架滑轮调整至胸部水平高度，上背部仰靠在瑜伽球上，双脚踏实地面挺髋保持躯干平稳中立。",
            "双手各握一侧绳索手柄置于胸侧，手腕保持中立挺直，沉肩挺胸收紧核心。",
            "呼气胸大肌发力驱动双臂同时向前推起绳索手柄，双臂在胸部前方充分伸展微屈肘。",
            "在推起最高点顶峰收缩挤压胸肌停顿 1 秒，吸气受控放缓将双手收回至胸前起始位，按计划重复。",
        ],
    },
    "1269": {
        "name_zh": "站姿直立龙门架绳索夹胸",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["delts", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站在龙门架正中央，身体保持直立站姿，双脚与肩同宽微屈膝，核心收紧挺胸沉肩。",
            "双手各握两侧中高位滑轮手柄向体侧展开，双臂肘关节微屈锁定角度。",
            "呼气胸大肌发力驱动双臂沿水平圆弧轨迹向前内收环抱，双手在胸前交叉相错。",
            "在动作顶点充分顶峰挤压胸肌内侧停顿 1 秒，吸气受控放缓将双臂沿原弧线轨迹打开回至体侧起始位，按计划重复。",
        ],
    },
    "1270": {
        "name_zh": "站姿龙门架绳索上胸夹胸",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["delts", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将龙门架双侧滑轮调整至低位，站在机器中央前后弓步站立以稳固支撑重心，挺胸沉肩核心收紧。",
            "双手各握低位手柄置于体侧斜下方，手掌朝向斜前方，双肘微屈锁定角度。",
            "呼气胸大肌上束（上胸）强力收缩发力，带动双手沿斜前上方弧线内收向上提拉夹胸，双手在胸骨上沿前方相汇或轻度交叉。",
            "在动作最高点顶峰收缩强力挤压上胸停顿 1 秒，吸气匀速受控放慢将双手沿原斜弧线降回至体侧起始位，按计划重复。",
        ],
    },
    "1272": {
        "name_zh": "瑜伽球仰靠扩胸拉伸",
        "category": "chest",
        "equipment": "stability ball",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "背部仰靠在瑜伽球上，双脚踏实地面屈膝支撑骨盆，头部与上背完全放松贴合球体弧度。",
            "双臂向身体两侧自然水平或斜上方展开呈十字或 Y 字型，手心朝上，让重力自然带动双肩下沉。",
            "深吸气感受胸大肌、胸廓与前侧三角肌随身体后仰弧度得到充分被动舒展与拉伸。",
            "保持舒缓平稳呼吸 15 至 30 秒，呼气收拢双臂顺势借力起立，按计划重复。",
        ],
    },
    "1296": {
        "name_zh": "瑜伽球折体俯卧撑",
        "category": "chest",
        "equipment": "stability ball",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "双手撑地略宽于肩，双脚脚背或小腿平放在瑜伽球上，核心收紧呈平直俯卧撑姿态。",
            "收紧腹肌并屈髋将臀部向上推送推向天花板，双腿伸直将瑜伽球向前拉滚，使身体呈倒 V 字屈体姿势。",
            "吸气屈肘将头部与上半身受控向地面方向降低，肘部与躯干呈约 45 度角。",
            "呼气胸肌与三角肌前束协同发力，双臂强力推地伸直手臂回到倒 V 字支撑位，再受控将球后滚回至起始平身位，按计划重复。",
        ],
    },
    "1298": {
        "name_zh": "仰卧地面壶铃单臂推胸",
        "category": "chest",
        "equipment": "kettlebell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在训练垫或平整地面上，双腿屈膝，双脚平踩地面，核心收紧下背部贴实地面。",
            "单手握住壶铃把手，将壶铃球体稳妥架在小臂外侧与虎口之间，大臂平放在地面上，小臂垂直于地面。",
            "呼气胸大肌与肱三头肌发力，垂直向上推起壶铃至单臂完全伸直微屈肘位置。",
            "在顶点充分挤压胸肌停顿 1 秒，吸气受控放缓将大臂缓慢下放回落至地面轻触，单侧完成计划次数后换边重复。",
        ],
    },
    "1299": {
        "name_zh": "器械坐姿上斜推胸",
        "category": "chest",
        "equipment": "leverage machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整器械座椅高度，使双手握柄位于胸部上沿锁骨下方，后背与头部紧贴靠背，双脚平踩地面。",
            "双手握紧把手，双肘微沉内收，挺胸沉肩收腹。",
            "呼气胸大肌上部集中发力，向前上方平稳推出把手至双臂伸展微屈肘位置。",
            "在推起最高点充分挤压上胸停顿 1 秒，吸气受控放缓屈肘将把手回放至胸前起始位，按计划重复。",
        ],
    },
    "1300": {
        "name_zh": "器械坐姿下斜推胸",
        "category": "chest",
        "equipment": "leverage machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整器械座椅高度，使双手握柄位于下胸部位置，后背贴紧靠背，双脚踏稳地面。",
            "双手握紧推胸把手，手腕保持中立挺直，沉肩挺胸收紧核心。",
            "呼气胸大肌下束集中发力，向前下方平稳推出把手至双臂伸直微屈肘位置。",
            "在动作顶点顶峰收缩强力挤压下胸停顿 1 秒，吸气匀速受控放慢屈肘将把手收回至起始位，按计划重复。",
        ],
    },
    "1301": {
        "name_zh": "器械坐姿窄距推胸",
        "category": "chest",
        "equipment": "leverage machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整座椅至适宜高度，背部与臀部紧贴靠背，双脚平踩地面，挺胸沉肩锁死肩胛。",
            "双手采用窄握距握持内侧推柄，双肘内收贴近身体两侧前下方。",
            "呼气胸大肌内侧纤维与肱三头肌发力，向前平稳推起把手至双臂伸直微屈肘。",
            "在推起最高点顶峰收缩挤压胸肌中缝停顿 1 秒，吸气受控放慢将把手缓慢回放至胸前起始位，按计划重复。",
        ],
    },
}

pending = {
    "1267": "待修图 · 规范健身球单臂推胸为瑜伽球仰靠龙门架绳索单臂推胸并补全瑜伽球支持器械；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1268": "待修图 · 规范健身球推胸为瑜伽球仰靠龙门架绳索推胸并补全瑜伽球支持器械；原动图仅 2 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1269": "待修图 · 消除直臂交叉下压直译规范为站姿直立龙门架绳索夹胸；原动图仅 2 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1270": "待修图 · 规范上胸交叉动作为站姿龙门架绳索上胸夹胸；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1272": "待修图 · 消除球上胸拉伸口语直译规范为瑜伽球仰靠扩胸拉伸并补全瑜伽球支持器械；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1296": "待修图 · 消除屈体俯卧撑直译规范为瑜伽球折体俯卧撑并补全瑜伽球支持器械；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1298": "待修图 · 规范地面推举为仰卧地面壶铃单臂推胸；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1299": "待修图 · 消除杠杆上斜直译规范为器械坐姿上斜推胸；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1300": "待修图 · 消除杠杆下斜直译规范为器械坐姿下斜推胸；原动图仅 2 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1301": "待修图 · 消除机器内胸直译规范为器械坐姿窄距推胸；原动图仅 2 帧且帧率不合规，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review108-20261225",
    "inspected": inspected,
    "review_candidates": review_candidates,
    "registered_media": registered_media,
    "definition_updates": definition_updates,
    "pending": pending,
    "sources": sources,
    "review_notes": review_notes,
    "image_generation_calls": 0,
    "generated_images_imported": 0,
}
(B / "review-result.json").write_text(json.dumps(review_result, ensure_ascii=False, indent=2) + "\n")

code_paths = [
    "app/src/main/java",
    "scripts/validate_exercise_dataset.sh",
    "scripts/build_android_debug.sh",
]
baseline = {}
for rel in code_paths:
    p = R / rel
    if p.is_file():
        baseline[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    else:
        for f in sorted(p.rglob("*")):
            if f.is_file():
                baseline[str(f.relative_to(R))] = hashlib.sha256(f.read_bytes()).hexdigest()
(B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

qa_spec = {
    "batch": BATCH_ID,
    "expected_checks": 16,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_ids": [],
    "candidate_required_equipment": {
        "1267": ["瑜伽球"],
        "1268": ["瑜伽球"],
        "1272": ["瑜伽球"],
        "1296": ["瑜伽球"],
    },
    "expected_per_side_ids": ["1267", "1298"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
