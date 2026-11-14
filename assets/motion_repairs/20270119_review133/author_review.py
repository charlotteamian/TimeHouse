#!/usr/bin/env python3
"""Author Batch 133 review updates, pending notes, code baseline, and QA spec (0 candidates; 5 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270119_review133"
VERSION = "1.2.138"
VERSION_CODE = 2027011901

inspected = ["3670", "3697", "3758", "3759", "3760"]
review_candidates = []
registered_media = []

definition_updates = {
    "3670": {
        "name_zh": "带勾脚下斜凳抱片仰卧起坐",
        "category": "waist",
        "equipment": "weighted",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors", "lower back"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "仰卧在带勾脚的下斜训练凳上，将小腿与脚背稳固卡在顶部脚垫下方，双手于胸前抱紧一块负重片。",
            "下背微贴靠垫并收紧腹部核心，随后呼气集中腹肌发力向上卷曲上半身脱离斜凳。",
            "继续卷起至躯干接近竖直高点略作停顿并充分挤压腹直肌，注意避免借惯性猛拽颈部或甩腰。",
            "随后吸气有控制地缓缓展开躯干下放回到斜凳起始躺姿，重复规定次数。",
        ],
    },
    "3697": {
        "name_zh": "绳索跪姿双绳后束划船",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["trapezius", "rhomboids", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将双头绳把连接至龙门架低位滑轮，面向滑轮双膝跪稳在地面或软垫上，背部挺直并收紧腹部。",
            "双手以掌心相对的对握姿势抓稳绳把末端，双臂向斜前方伸直拉出配重张力。",
            "呼气时先沉肩避免耸肩，集中三角肌后束发力带动双肘向后上方拉引绳把至肋下侧方，同时挤压肩胛骨。",
            "在后端略作停顿后，吸气沿原路径缓慢控制伸臂还原回起始前伸位，重复规定次数。",
        ],
    },
    "3758": {
        "name_zh": "站姿固定器械推胸",
        "category": "chest",
        "equipment": "leverage machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "走入站姿杠杆推胸器架内，双脚分开约与肩同宽稳踩地面，上背部贴实垂直靠背垫并微收腹部核心。",
            "双手正握与胸部同高的推把且沉肩不耸肩，确认前臂与推把发力方向基本一致。",
            "呼气时集中胸大肌发力向前推直双臂至肘关节微屈，感受胸肌中束收缩挤压，在前端略作停顿。",
            "随后吸气有控制地缓缓屈肘回放推把至胸前起始高度（配重不轻撞回落），重复规定次数。",
        ],
    },
    "3759": {
        "name_zh": "固定器械坐姿早安式体前屈",
        "category": "upper legs",
        "equipment": "leverage machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐上固定器械早安式座椅，双脚平踩前方防滑踏板、大腿前侧压稳在水平滚垫下方，双手抓牢座椅两侧稳固把手。",
            "挺胸收紧腹部与竖脊肌，脊柱中立不弯腰，双肩自然下沉。",
            "吸气以髋关节为轴缓缓控制向前屈髋折身，直至上半身接近与地面平行并感受臀肌与腘绳肌充分拉伸。",
            "呼气集中臀肌与大腿后侧发力带动躯干按控制节奏伸髋起立回到起始坐姿，重复规定次数。",
        ],
    },
    "3760": {
        "name_zh": "固定器械坐姿屈膝卷腹",
        "category": "waist",
        "equipment": "leverage machine",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐于杠杆卷腹器座椅并将腰背贴靠后方斜靠垫，小腿下端与脚背勾稳前方可动滚垫下方，双手抓牢座椅两侧稳固把手。",
            "呼气时集中腹直肌发力，上身顺势向前含胸卷曲躯干并同步屈髋提膝上拉滚垫，使胸肋向膝盖方向靠拢挤压腹部。",
            "在卷腹最紧缩的最高点略作停顿后，吸气缓慢控制舒展躯干并顺畅下放双腿回到起始位（配重勿直接落地碰撞），重复规定次数。",
        ],
    },
}

pending = {
    "3670": "待修图 · 纠正“将双手放在脑后或胸前”与实图抱负重片不一致问题、补充 required_equipment_zh=[\"带勾脚的下斜训练凳\"]（带勾脚下斜凳抱片仰卧起坐）；原动图仅 2 帧（L:14, R:14<15），斜凳整体角度与前脚垫位移致 y>=370 IoU=0.4163<0.96，待重制。",
    "3697": "待修图 · 消除“（绳索）（男）”冗余括号及“低电缆滑轮/保持”；原动图仅 2 帧（L:14, R:14<15），龙门架底座与双膝水平位移致 y>=370 IoU=0.3919<0.96，待重制为标准 4 帧循环图。",
    "3758": "待修图 · 纠正“调整座椅高度并坐在机器上”错配站姿实图步骤、消除“保持/（杠杆）”；原动图仅 2 帧（B:14, T:14<15），器械底座移位致 y>=370 IoU=0.8221<0.96，待重制。",
    "3759": "待修图 · 纠正“背部靠在垫子上”错配大腿前侧压垫早安式屈髋步骤、去除“坐姿挺身/（杠杆）/保持”；原动图仅 2 帧（L:12, R:14<15）且底座轻微位移（IoU=0.9463<0.96），待重制。",
    "3760": "待修图 · 纠正“向前挺胸”与“（第二式）（杠杆）”直译并消除“以获得支撑”；原动图仅 2 帧（L:14, R:14<15）且座椅底架略移（IoU=0.9107<0.96），待重制为标准 4 帧循环图。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review133-20270119",
    "inspected": inspected,
    "review_candidates": review_candidates,
    "registered_media": registered_media,
    "definition_updates": definition_updates,
    "pending": pending,
    "sources": {},
    "review_notes": {},
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
    "expected_checks": 11,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_ids": [],
    "candidate_required_equipment": {},
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
