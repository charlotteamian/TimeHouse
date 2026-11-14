#!/usr/bin/env python3
"""Author Batch 96 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261213_review96"
VERSION = "1.2.101"
VERSION_CODE = 2026121301

inspected = ["0754", "0755", "0756", "0757", "0758", "0759", "0760", "0761", "0762", "0763"]
review_candidates = []
registered_media = []

definition_updates = {
    "0754": {
        "name_zh": "史密斯下斜反握卧推",
        "category": "chest",
        "equipment": "smith machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "躺在调节为下斜 15 至 30 度的卧推凳上，双脚稳固勾紧固定脚垫，头部朝下。",
            "双手反握抓握史密斯杠铃杆（掌心朝向面部头部），握距略宽于双肩，推起旋转杠铃解开安全挂钩。",
            "吸气受控屈肘将杠铃缓慢平稳下落至中下胸部，保持肘部自然贴近身体两侧以更好地孤立胸肌上部与下束。",
            "在杠铃轻触胸部停顿 1 秒，呼气由胸大肌与肱三头肌发力将杠铃沿轨道垂直推回起始伸直位，按计划重复。",
        ],
    },
    "0755": {
        "name_zh": "史密斯哈克深蹲",
        "category": "upper legs",
        "equipment": "smith machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站在史密斯机滑轨正下方，双脚与肩同宽站立，双脚向前迈出约 20 至 30 厘米，脚尖微朝外展。",
            "将杠铃平稳架在后肩上斜方肌上，双手握紧杠铃，挺胸收腹，转动杠铃解开安全锁扣。",
            "吸气控制躯干几乎保持竖直，屈髋屈膝让身体顺着滑轨平稳下蹲，膝盖顺应脚尖方向前送，蹲至大腿与地面平行。",
            "在下蹲最低点停顿 1 秒充分感受股四头肌承重，呼气由足跟蹬地驱动身体沿滑轨直立推起回到起始位，按计划重复。",
        ],
    },
    "0756": {
        "name_zh": "史密斯仰卧臀桥",
        "category": "waist",
        "equipment": "smith machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["abs", "hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在史密斯机下方的训练垫上，双膝弯曲约 90 度，双脚与肩同宽平踩地面。",
            "将史密斯机杠铃下落并平稳架在骨盆髋部上方（可放置保护垫缓冲），双手扶稳杠铃解开安全锁扣。",
            "呼气收紧核心与腹部，双脚脚后跟发力蹬地驱动臀部向上推起髋部，直到膝、髋、肩呈一条平直斜线。",
            "在最高点顶峰收缩用力挤压臀大肌停顿 1 秒，吸气匀速受控将臀部下放回至贴近地面起始位，按计划重复。",
        ],
    },
    "0757": {
        "name_zh": "史密斯上斜卧推",
        "category": "chest",
        "equipment": "smith machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将史密斯机下方的斜凳靠背角度调节至约 30 至 45 度，背部完全贴靠靠背，双脚踩实地面。",
            "端坐于斜凳上挺胸沉肩，双手正手抓握杠铃，握距略宽于双肩，向上微推并旋转手腕解除安全挂钩。",
            "吸气缓慢屈肘将杠铃沿轨道平稳垂直下落至锁骨与上胸部上方，两肘向外展约 45 度。",
            "在杠铃轻触上胸部停顿 1 秒，呼气由胸大肌上束与肩前束爆发推起杠铃回到起始微屈伸展位，按计划重复。",
        ],
    },
    "0758": {
        "name_zh": "史密斯上斜反握卧推",
        "category": "chest",
        "equipment": "smith machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将卧推凳调节为上斜 30 度置于史密斯机正下方，端坐其上双脚平踏地面，腰背贴紧靠垫。",
            "双手反握抓握杠铃杆（掌心朝向头顶方向），握距略宽于双肩，微推并转动手腕解开安全卡扣。",
            "吸气控制屈肘将杠铃缓慢平稳下落至上胸部，肘部适度内收贴近躯干以深度刺激胸大肌锁骨头与肱三头肌。",
            "在上胸最低点停顿 1 秒，呼气由胸大肌上部集中发力沿导轨推回手臂微屈伸直起始位，按计划重复。",
        ],
    },
    "0759": {
        "name_zh": "史密斯上斜肩胛上推",
        "category": "chest",
        "equipment": "smith machine",
        "target": "serratus anterior",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "trapezius"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将上斜卧推凳调整至 30 至 45 度置于史密斯机下方，端坐靠背双脚踩实地面。",
            "双手正握抓住杠铃，握距与肩同宽，向上推起杠铃并旋转手腕解开安全挂钩，双臂伸直垂直指向天花板。",
            "肘关节全程锁定微屈不弯曲，深吸气沉肩将肩胛骨后缩紧贴靠垫。",
            "呼气由前锯肌与胸小肌主动收缩发力，推动两侧肩胛骨向前上方全力前伸，将杠铃推向更高顶点。",
            "在肩胛骨充分前伸最高点停顿 1 秒挤压前锯肌，吸气匀速受控让肩胛骨回缩至起始拉伸位，手臂保持伸直不屈肘，按计划重复。",
        ],
    },
    "0760": {
        "name_zh": "史密斯仰卧垂直腿举",
        "category": "upper legs",
        "equipment": "smith machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "平躺在史密斯机正下方的平垫或地面上，腰背部完全贴实地面，臀部位于杠铃的正下方。",
            "双脚平踩在上方史密斯机杠铃杆中央，双脚与肩同宽，脚心或足弓稳固抵紧杠铃，双手握住两侧安全把手解开锁扣。",
            "吸气控制双腿受控屈髋屈膝让杠铃沿垂直导轨缓慢下落，大腿贴向胸腹侧方，下沉至膝关节呈约 90 度角且臀部不离地。",
            "在最低折叠点停顿 1 秒，呼气由臀肌与股四头肌强力蹬推脚后跟将杠铃垂直推回高位起始位，膝盖保持微屈不锁死，按计划重复。",
        ],
    },
    "0761": {
        "name_zh": "史密斯俯身窄握划船",
        "category": "back",
        "equipment": "smith machine",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "rear deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立在史密斯机滑轨后方，屈髋俯身让上半身前倾约 45 度，背部挺直中立收紧核心。",
            "双手正手窄握杠铃杆，握距窄于双肩，微推并旋转杠铃解锁安全钩，手臂自然下垂充分拉伸背部。",
            "呼气由上背部、菱形肌与背阔肌主动收缩发力，屈肘沿大腿方向将杠铃向上提拉至下腹肚脐位置，两肘贴紧身体向后向上引。",
            "在最高拉升点用力夹紧肩胛骨停顿 1 秒，吸气匀速受控将杠铃缓慢放回起始手臂完全垂悬伸展位，按计划重复。",
        ],
    },
    "0762": {
        "name_zh": "史密斯俯身三角肌后束划船",
        "category": "shoulders",
        "equipment": "smith machine",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["trapezius", "rhomboids", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站立在史密斯杠铃后方，双脚与肩同宽，屈髋屈膝俯身至躯干接近与地面平行，保持脊柱平直中立。",
            "双手全正握抓握杠铃杆，握距宽于双肩，两臂自然垂直下垂，旋转杠铃解开安全挂钩。",
            "呼气主要由三角肌后束与上背肌群发力，将手肘向身体两侧高高向上提拉，上臂垂直于躯干向上打开至与背部平齐。",
            "在顶峰最高收缩点停顿 1 秒挤压后三角肌，吸气匀速受控放低杠铃回至初始下垂拉伸位，保持身体俯角稳定不晃动，按计划重复。",
        ],
    },
    "0763": {
        "name_zh": "史密斯反向小腿提踵",
        "category": "lower legs",
        "equipment": "smith machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["soleus"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站在史密斯机下方，双肩顶住上方软垫，前脚掌平踩在踏板或台阶边缘，脚后跟悬空。",
            "双腿微屈膝不超伸，挺胸收腹核心收紧，转动杠铃解开安全限位扣。",
            "先受控下沉脚后跟至踏板平面下方以深度拉伸小腿肌群，深吸气保持踝关节稳定。",
            "呼气由小腿三头肌发力强力推蹬前脚掌向上垂直提踵，使身体沿轨道升至最高点。",
            "在提踵最高点顶峰收缩挤压小腿停顿 1 秒，吸气受控匀速放回脚后跟至起始拉伸位，按计划重复。",
        ],
    },
}

pending = {
    "0754": "待修图 · 消除直译推规范为史密斯下斜反握卧推；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0755": "待修图 · 规范哈克深蹲名称为史密斯哈克深蹲；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0756": "待修图 · 规范臀推为史密斯仰卧臀桥并校正主训目标为臀肌；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0757": "待修图 · 规范卧推名称为史密斯上斜卧推；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0758": "待修图 · 消除推直译规范为史密斯上斜反握卧推；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0759": "待修图 · 纠正肩推错译为史密斯上斜肩胛上推并校准前锯肌；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0760": "待修图 · 规范腿推为史密斯仰卧垂直腿举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0761": "待修图 · 规范俯身划船名称为史密斯俯身窄握划船；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0762": "待修图 · 规范后三角划船为史密斯俯身三角肌后束划船；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0763": "待修图 · 规范小腿动作名称为史密斯反向小腿提踵；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review96-20261213",
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
