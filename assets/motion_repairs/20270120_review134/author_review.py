#!/usr/bin/env python3
"""Author Batch 134 re-inspection of the 7 dataset_1324 pending 待核逻辑 items (1 candidate 0260; 6 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270120_review134"
VERSION = "1.2.139"
VERSION_CODE = 2027012001

inspected = ["0001", "0260", "0289", "0316", "0321", "0806", "0807"]
review_candidates = ["0260"]
registered_media = []

definition_updates = {
    "0260": {
        "name_zh": "仰卧收腹",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在瑜伽垫或平地上，双臂向头顶后方完全伸直，双腿并拢伸直且脚跟略微离地悬空。",
            "收紧腹部核心，呼气同时上卷肩胛骨并屈髋屈膝将双膝拉向胸前，双手随躯干前移沿着小腿外侧向脚踝方向伸出。",
            "颈部自然放松、下背贴稳地面不弓腰代偿；随后有控制地缓慢展开手臂和双腿回到起始悬空位，重复规定次数。",
        ],
    },
    "0289": {
        "name_zh": "哑铃卧推",
        "category": "chest",
        "equipment": "dumbbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧在平板训练凳上，双脚分开平踩地面，上背与臀部贴稳凳面、肩胛骨微后缩下沉。",
            "双手各握一只哑铃举至胸肩上方至双臂近乎伸直、掌心朝前（双铃间距略宽于肩）。",
            "吸气时缓慢屈肘并将上臂适度收夹于体侧约四十五至六十度，控制将哑铃下放至胸部外侧齐平高度。",
            "在底端略作停顿感受胸肌拉伸后，呼气集中胸大肌发力将哑铃稳步推回起始高位，重复规定次数。",
        ],
    },
    "0316": {
        "name_zh": "哑铃上斜宽弧夹推",
        "category": "chest",
        "equipment": "dumbbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "将上斜训练凳调至约四十五度角，仰靠坐稳并使肩背贴紧靠垫、双脚分开平踩地面。",
            "双手各持一只哑铃对举至胸上方高位，肘关节微屈不锁死、掌心朝前微内旋。",
            "吸气时大臂呈宽弧向两侧下方展开下降，控制屈肘下放至哑铃接近肩胸外侧并感受胸肌上束拉伸。",
            "呼气时由胸肌主导按弧线向上内侧夹推回到起始高位，重复规定次数。",
        ],
    },
    "0806": {
        "name_zh": "体操吊环前倾俯卧撑",
        "category": "chest",
        "equipment": "gymnastic rings",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将挂于稳固门框或龙门架横杠上的一对体操吊环调节至离地偏低适中高度。",
            "背对吊环悬挂处双手握紧两侧环圈，双脚向后迈步踩稳前脚掌，身体前倾呈一条斜直线、腹部与臀部收紧。",
            "吸气时有控制地缓慢屈肘下降胸部向双环之间靠近，稳定控制吊环不向外晃开。",
            "呼气集中胸大肌与肱三头肌发力向上推直双臂回到起始高点，重复规定次数。",
        ],
    },
    "0807": {
        "name_zh": "高单杠挂臂屈膝举腿",
        "category": "waist",
        "equipment": "pull-up bar",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双手略宽于肩以正握抓牢高单杠，双臂伸直沉肩稳定挂于杠下，双腿并拢自然垂下。",
            "呼气时集中下腹核心发力向上屈膝提起双腿，同时向胸腔方向后卷骨盆使膝盖靠近腹部或胸前。",
            "在最高点略作停顿减少身体前后摆动，随后吸气控制缓缓下放双腿回到起始直立悬垂前的伸直位置，重复规定次数。",
        ],
    },
}

pending = {
    "0001": "待修图 · 已核对四分之三仰卧起坐步骤无禁用词，但原 4 帧动图角落偏青灰 ([253,255,255])、R=7<15 且双脚/臀部跨帧移动（y>=370 IoU=0.2500<0.96），待重制。",
    "0289": "待修图 · 已补充 required_equipment_zh=[\"平板训练凳\"]、清理 muscle_group 与“保持”；原 4 帧动图底色非纯白 ([253,253,253]) 且右侧脚尖距画布边缘仅 R=3<15 px，待扩边距重制。",
    "0316": "待修图 · 已纠正“正手握握/保持”错漏及 muscle_group 并定名为哑铃上斜宽弧夹推；原 4 帧底色偏灰 ([254,253,253])、T=3<15、底座位移（IoU=0.7166<0.96）且仅两枚静态关键帧复用，待重制。",
    "0321": "待修图 · 已核对上斜训练凳与步骤无禁用词；原 4 帧底色非纯白 ([253,253,253])、F3 顶缘 T=3<15 且凳脚位移致 y>=370 IoU=0.8592<0.96，待重制。",
    "0806": "待修图 · 已将误用“悬挂训练器/悬架训练器/支撑/保持”按实图改写为体操吊环前倾俯卧撑并清零 muscle_group；原 4 帧顶框贴边 T=0<15、bg0=[254,255,255] 且支架/脚尖移位（IoU=0.8585<0.96），待重制。",
    "0807": "待修图 · 已消除名称禁用词“悬垂”（改高单杠挂臂屈膝举腿）、纠正正握步骤并清零 muscle_group；原 4 帧框架顶缘 T=3<15、bg0=[253,255,255] 且龙门架柱大幅内移（IoU=0.3170<0.96），待重制。",
}

sources = {
    "0260": "https://fitbod.me/exercises/",
}

review_notes = {
    "0260": "核对名称、自重属性、腹肌主目标及髋屈肌/下背辅助肌群；清理步骤三禁用词“保持”并确认颈部放松、下背贴地、双手沿小腿外侧向脚踝前伸。实测 480x480 4 帧 WebP（[800,380,800,380]，2.36s），纯白底 [255,255,255]、四边距 >=35 px、F2==F4（max_diff=0）、骶尾触地区域稳定在 y=320..321 px（<=1 px），参考 assets/motion_repairs/20260910/{manifest,prompts}.json#0260。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review134-20270120",
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
    "expected_checks": 15,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_ids": ["0260"],
    "candidate_required_equipment": {"0260": []},
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
