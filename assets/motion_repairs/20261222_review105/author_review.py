#!/usr/bin/env python3
"""Author Batch 105 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261222_review105"
VERSION = "1.2.110"
VERSION_CODE = 2026122201

inspected = ["1004", "1005", "1007", "1008", "1009", "1010", "1011", "1012", "1013", "1014"]
review_candidates = []
registered_media = []

definition_updates = {
    "1004": {
        "name_zh": "站姿弹力带深蹲",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立踩住弹力带中段，双手各持把手提至肩膀上方，或将环状弹力带套在双膝上方。",
            "挺胸收紧核心，背部保持平直中立，双脚全脚掌贴实地面。",
            "吸气屈髋屈膝同时进行，臀部向后下方平稳坐下，膝盖轨迹向外展开与脚尖方向一致，下蹲至大腿与地面平行。",
            "呼气主要由臀大肌与股四头肌强力蹬地发力，推蹬全脚掌起立回至直立起始位，在最高点顶峰收紧臀肌停顿 1 秒，按计划重复。",
        ],
    },
    "1005": {
        "name_zh": "站姿弹力带卷腹",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带固定在身后或高位锚点上，背对锚点站立，双脚与肩同宽微屈膝站立。",
            "双手抓握把手拉至胸前或双肩颈侧，骨盆与下半身保持稳固锁定。",
            "呼气主要由腹直肌集中收缩发力，低头含胸向前下方卷屈躯干，使胸口平稳靠近髋部。",
            "在卷腹最底端顶峰收缩强力挤压腹肌停顿 1 秒，吸气匀速受控放慢躯干展开回至直立起始位，按计划重复。",
        ],
    },
    "1007": {
        "name_zh": "站姿弹力带转体卷腹",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带套在上背部穿过腋下胸前，或双手抓握把手置于体侧，双脚分开与肩同宽弹性站立。",
            "挺胸收腹，双肘微张处于身体两侧，微收下巴。",
            "呼气主要由腹直肌与腹斜肌协同收缩发力，向前下方卷屈躯干并带动上半身向一侧斜向扭转，单侧肘关节向对侧膝盖靠近。",
            "在转体卷腹最高点顶峰收缩挤压腹部停顿 1 秒，吸气匀速受控回正展开，随后向对侧交替转体卷屈，按计划重复。",
        ],
    },
    "1008": {
        "name_zh": "稳固踏台弹力带交替登阶",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": ["稳固踏台"],
        "instructions_zh": [
            "将环状弹力带套在双侧大腿下沿膝关节上方，面向稳固跳箱或踏台站立，双脚与髋同宽。",
            "单脚全脚掌完全踏实踩上踏台中央，挺胸沉肩收紧核心，躯干保持正直微前倾。",
            "呼气主要由登台侧臀大肌与股四头肌强力发力蹬伸踏面，推起身体垂直登顶踏台，对侧腿顺畅提膝或自然并拢。",
            "在踏台顶峰收紧臀肌停顿 1 秒，吸气受控放缓下放后侧腿平稳着地，左右腿交替登阶按计划重复。",
        ],
    },
    "1009": {
        "name_zh": "站姿弹力带直膝硬拉",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚踩住弹力带中段与肩同宽站立，双手正握弹力带两端把手垂于大腿前侧，双膝保持微屈弹性锁定不变角。",
            "挺胸沉肩锁死背部，深吸气核心收紧准备。",
            "吸气主要由屈髋铰链主导，臀部平稳向后推送，躯干沿平直脊柱前倾俯身直至大腿后侧腘绳肌产生深度拉伸感。",
            "在最底端拉伸点稍作停顿，呼气由臀大肌与腘绳肌强力向心收缩发力，向前挺髋站立回至直立起始位，在顶点顶峰收紧臀肌停顿 1 秒，按计划重复。",
        ],
    },
    "1010": {
        "name_zh": "站姿弹力带直腿硬拉",
        "category": "back",
        "equipment": "band",
        "target": "spine",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚踩在弹力带上与肩同宽站立，双手正握把手垂直下垂，双腿几乎完全伸直但膝盖不锁死反关节。",
            "挺胸收腹，竖脊肌与核心肌群维持全脊柱中立平直锁定。",
            "吸气以髋关节为转动轴心，躯干向前下方平稳折叠俯身，感受下背部与后链肌群平稳受控承重。",
            "俯身至躯干接近水平高度后，呼气主要由竖脊肌与臀大肌协同发力，驱动上半身平稳向后上方伸展拉回至直立起始位，在最高点顶峰收缩 1 秒，按计划重复。",
        ],
    },
    "1011": {
        "name_zh": "坐姿弹力带转体",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在训练垫或平凳上，双腿向前伸展或屈膝平踩地面，将弹力带中段绕在双脚足弓或体前固定锚点。",
            "双手对握把手收于胸腹前方，上半身挺胸微后倾约 15-30 度以预先激活腹直肌与腹斜肌。",
            "呼气主要由腹内斜肌与腹外斜肌发力，带动躯干受控向一侧平稳旋转，将双手带至侧腹附近。",
            "在侧转顶点顶峰收缩挤压腹斜肌停顿 1 秒，吸气匀速回正，顺畅向对侧旋转转体，左右交替按计划重复。",
        ],
    },
    "1012": {
        "name_zh": "站姿弹力带转体推举",
        "category": "shoulders",
        "equipment": "band",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚踩住弹力带与肩同宽站立，双手各持把手提至肩膀耳朵高度，掌心朝前上方。",
            "挺胸沉肩收腹，核心肌群保持紧绷蓄力。",
            "呼气主要由三角肌发力将弹力带推向头顶过头伸直手臂，同时躯干向一侧受控微转协同发力，下肢稳固抓地。",
            "在推举转体最高点顶峰收紧肩部与核心停顿 1 秒，吸气匀速受控降回把手至肩部起始位，随后换对侧转体推举，左右交替按计划重复。",
        ],
    },
    "1013": {
        "name_zh": "站姿弹力带反握下拉",
        "category": "back",
        "equipment": "band",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带挂在头顶高位锚点上，面对锚点双脚与肩同宽微屈膝站立，双手反握（掌心朝向自己）把手或带端。",
            "双臂完全向高处伸直带动背阔肌充分纵向舒展拉伸，挺胸沉肩锁死核心。",
            "呼气主要由背阔肌与肱二头肌集中收缩发力，屈肘将把手向下拉向胸口上沿，双肘主动向内向下拉沉。",
            "在下拉最低点顶峰收缩充分挤压背阔肌停顿 1 秒，吸气匀速受控放慢双臂回弹放至高位起始拉伸位，按计划重复。",
        ],
    },
    "1014": {
        "name_zh": "弹力带仰卧V字卷腹",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在训练垫上，双手全握弹力带两端过头伸直，双腿并拢伸直微悬空离地。",
            "深吸气蓄力准备，下背部紧贴地面。",
            "呼气腹直肌爆发强力向心收缩，上半身与双腿同时向上折起呈 V 字夹角，双手拉动弹力带向脚踝平稳延伸靠近。",
            "在 V 字折叠最高点顶峰收缩挤压腹肌停顿 1 秒，吸气匀速受控放缓下放身体回至起始悬空位，按计划重复。",
        ],
    },
}

pending = {
    "1004": "待修图 · 规范深蹲动作姿态为站姿弹力带深蹲；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1005": "待修图 · 规范站立卷腹姿态为站姿弹力带卷腹；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1007": "待修图 · 消除扭转卷腹直译规范为站姿弹力带转体卷腹；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1008": "待修图 · 纠正抬腿错译规范为稳固踏台弹力带交替登阶并补全稳固踏台支持器械；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1009": "待修图 · 规范直膝硬拉姿态为站姿弹力带直膝硬拉；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1010": "待修图 · 规范直腿硬拉命名为站姿弹力带直腿硬拉；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1011": "待修图 · 消除扭转直译规范为坐姿弹力带转体；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1012": "待修图 · 消除过头推直译规范为站姿弹力带转体推举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1013": "待修图 · 规范反手下拉为站姿弹力带反握下拉；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1014": "待修图 · 消除屈体卷腹直译规范为弹力带仰卧V字卷腹；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review105-20261222",
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
    "candidate_required_equipment": {"1008": ["稳固踏台"]},
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
