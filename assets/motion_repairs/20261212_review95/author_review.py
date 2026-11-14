#!/usr/bin/env python3
"""Author Batch 95 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261212_review95"
VERSION = "1.2.100"
VERSION_CODE = 2026121201

inspected = ["0743", "0744", "0746", "0747", "0748", "0749", "0750", "0751", "0752", "0753"]
review_candidates = []
registered_media = []

definition_updates = {
    "0743": {
        "name_zh": "雪橇机哈克深蹲",
        "category": "upper legs",
        "equipment": "sled machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背部与臀部平整贴靠在雪橇哈克深蹲机的滑动靠垫上，双肩稳固顶住上方承重肩垫。",
            "双脚平踏在下方倾斜踏板中央，间距与肩同宽，脚尖微向外展，双手握住两侧安全释放手柄。",
            "解开安全锁扣，吸气缓慢屈髋屈膝使身体沿斜向滑轨受控下沉，膝盖与脚尖方向保持一致，蹲至大腿与踏板呈约 90 度角。",
            "在下蹲最低点停顿 1 秒充分感受股四头肌与臀肌受力，呼气由足跟发力蹬伸踏板推起滑板回到起始直立位，膝盖不超伸锁死，按计划重复。",
        ],
    },
    "0744": {
        "name_zh": "雪橇机仰卧倒蹬腿举",
        "category": "upper legs",
        "equipment": "sled machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在雪橇腿举机滑动靠垫上，腰背部完全贴实靠背，双脚与肩同宽平稳踩踏在前侧大踏板中央。",
            "双手握紧座椅两侧的固定把手，双脚微蹬使滑板脱离保险架并扳开安全锁扣，核心收紧。",
            "吸气受控屈髋屈膝让踏板带着重量朝胸腹方向平稳下移，控制膝盖顺应脚尖朝向打开，下沉至大腿与小腿呈约 90 度角且臀部不离垫。",
            "在折叠最低点停顿 1 秒，呼气由臀部与大腿肌群协同发力蹬推踏板回到双腿接近完全伸展起始位，膝关节保持微屈，按计划重复。",
        ],
    },
    "0746": {
        "name_zh": "史密斯身后耸肩",
        "category": "back",
        "equipment": "smith machine",
        "target": "traps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对史密斯机杠铃直立站立，双脚与肩同宽，将杠铃高度调节至臀大肌下沿位置。",
            "双臂在身后自然下垂，双手正握（手心朝后）抓握杠铃杆，握距与肩同宽，微屈双膝保持腰背挺直。",
            "旋转杠铃解开安全挂钩，呼气由斜方肌上部与中后束主动发力，垂直向上将双肩向耳朵方向全力耸起。",
            "在最高耸肩点用力挤压收缩斜方肌停顿 1 秒，吸气匀速受控将双肩下沉完全放回起始深度拉伸位，手臂始终伸直不借力屈肘，按计划重复。",
        ],
    },
    "0747": {
        "name_zh": "史密斯颈后推举",
        "category": "shoulders",
        "equipment": "smith machine",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整史密斯机平凳或垂直坐椅，背对或面向导轨端坐，挺胸沉肩收紧腰腹核心。",
            "双手全握握住头顶上方杠铃杆，握距略宽于肩宽，手腕中立锁定，向上微推旋转解开杠铃安全锁扣。",
            "吸气缓慢受控屈肘将杠铃沿垂直滑轨平稳下放至后颈部或上斜方肌上方（约与耳垂平齐），肘部朝向两侧。",
            "在颈后触及预定深度停顿 1 秒，呼气由三角肌中束与前束发力沿导轨推起杠铃至手臂充分伸展顶点，肘部微屈不锁死，按计划重复。",
        ],
    },
    "0748": {
        "name_zh": "史密斯平凳卧推",
        "category": "chest",
        "equipment": "smith machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "平躺在史密斯机正下方的卧推平凳上，使杠铃垂直下落轨迹对准中下胸部中央，双脚平踩地面保持稳固。",
            "沉肩收紧肩胛骨，双手正手抓握杠铃，握距略宽于双肩，微推杠铃并转动手腕解开安全挂钩。",
            "吸气受控屈肘将杠铃缓慢平稳下落至轻触胸大肌表面，大臂与躯干呈约 60 至 75 度角以保护肩关节。",
            "在触胸最低点停顿 1 秒，呼气由胸大肌发力将杠铃沿滑轨推回手臂微屈伸展起始位，按计划重复。",
        ],
    },
    "0749": {
        "name_zh": "史密斯屈膝早安式躬身",
        "category": "upper legs",
        "equipment": "smith machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站立在史密斯机滑轨正下方，将杠铃平稳架在后肩上斜方肌丰厚处，双手握住杠铃两端维持平衡。",
            "双脚与髋同宽平稳站立，挺胸抬头收紧腹部，双膝微屈并在整个运动过程中保持这一屈曲角度不变。",
            "吸气保持脊柱完全中立，主动向后推移骨盆屈髋，躯干前倾平稳下俯至上半身与地面接近平行，感受腘绳肌与臀肌强力拉伸。",
            "在俯身最低点停顿 1 秒，呼气由臀大肌与腘绳肌收缩发力驱动髋关节向前推展，带动躯干回到直立起始位，按计划重复。",
        ],
    },
    "0750": {
        "name_zh": "史密斯椅式深蹲",
        "category": "upper legs",
        "equipment": "smith machine",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站立在史密斯机下方，将杠铃放置在斜方肌上，双手握紧杠铃，双脚向前迈出约 30 至 45 厘米，脚尖微外展。",
            "背部与躯干完全依靠杠铃的滑动支撑保持垂直，转动杠铃解锁安全销，收紧核心。",
            "吸气屈髋屈膝让身体如坐椅子般竖直下落，小腿保持几乎垂直于地面，深蹲直至大腿与地面完全平行。",
            "在蹲至大腿水平位停顿 1 秒充分孤立股四头肌发力，呼气由大腿前侧发力推地使躯干沿滑轨垂直上升回至起始位，按计划重复。",
        ],
    },
    "0751": {
        "name_zh": "史密斯平凳窄握卧推",
        "category": "upper arms",
        "equipment": "smith machine",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在史密斯机平凳上，使杠铃对准胸部下缘，双脚踩实地面保持下肢稳定。",
            "双手正手窄握杠铃杆，握距与肩同宽或略窄于肩宽，手腕保持中立不后翻，微推旋转解开杠铃锁扣。",
            "吸气缓慢下落杠铃，两肘向躯干两侧内夹，将杠铃轻触胸骨下部，充分拉伸肱三头肌长头与外侧头。",
            "在最低点停顿 1 秒，呼气主要由肱三头肌发力沿竖直导轨强力推起杠铃回到手臂接近伸展起始位，按计划重复。",
        ],
    },
    "0752": {
        "name_zh": "史密斯标准硬拉",
        "category": "upper legs",
        "equipment": "smith machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立在史密斯机导轨正下方踏板或地面上，杠铃高度调至小腿中段位置。",
            "屈髋屈膝俯身，挺胸沉肩保持背部平直中立，双手正反握或全正握抓握杠铃杆，握距略宽于双膝外侧。",
            "旋转杠铃解开挂钩，深吸气锁紧腹压，呼气由脚后跟蹬地，臀大肌与腘绳肌发力驱动髋部前送伸展站直身姿。",
            "在完全站立锁止点挤压臀部停顿 1 秒，吸气控制屈髋推臀让杠铃紧贴小腿缓慢受控下放至起始高度，按计划重复。",
        ],
    },
    "0753": {
        "name_zh": "史密斯下斜卧推",
        "category": "chest",
        "equipment": "smith machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "躺在调节为下斜 15 至 30 度的卧推凳上，双脚牢固卡紧在固定泡棉脚垫下方，头部在下、髋部在上。",
            "调整凳位使史密斯杠铃垂直落点位于胸肌下沿，双手全握杠铃握距略宽于肩，推起并转动手腕解锁。",
            "吸气缓慢屈肘将杠铃受控沿导轨垂直下放至轻触下胸部，肘部向外展开约 45 度保持肩关节舒展。",
            "在最低下落点停顿 1 秒，呼气由胸大肌下束集中发力将杠铃沿轨道推起至双臂微屈伸直起始位，按计划重复。",
        ],
    },
}

pending = {
    "0743": "待修图 · 规范深蹲名称为雪橇机哈克深蹲；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0744": "待修图 · 消除卧式直译规范为雪橇机仰卧倒蹬腿举；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0746": "待修图 · 消除背部直译规范为史密斯身后耸肩；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0747": "待修图 · 规范推举名称为史密斯颈后推举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0748": "待修图 · 消除粗糙直译规范为史密斯平凳卧推；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0749": "待修图 · 纠正硬拉错译规范为史密斯屈膝早安式躬身；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0750": "待修图 · 规范直译名称为史密斯椅式深蹲；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0751": "待修图 · 规范握距卧推为史密斯平凳窄握卧推；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0752": "待修图 · 规范硬拉动作为史密斯标准硬拉；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0753": "待修图 · 规范角度卧推为史密斯下斜卧推；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review95-20261212",
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
    "candidate_required_equipment": {},
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
