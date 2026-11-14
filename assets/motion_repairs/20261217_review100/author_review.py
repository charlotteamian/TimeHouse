#!/usr/bin/env python3
"""Author Batch 100 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261217_review100"
VERSION = "1.2.105"
VERSION_CODE = 2026121701

inspected = ["0849", "0850", "0851", "0852", "0853", "0854", "0856", "0857", "0859", "0860"]
review_candidates = []
registered_media = []

definition_updates = {
    "0849": {
        "name_zh": "瑜伽球坐姿负重转体",
        "category": "waist",
        "equipment": "weighted",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在瑜伽球球面上，双脚平踩地面与肩同宽，躯干保持挺直沉肩，维持下肢稳定支撑。",
            "双手抱持杠铃片或重物收于胸前，微收下巴，收紧腹直肌与腹斜肌核心。",
            "呼气由腹内斜肌与腹外斜肌发力，带动躯干受控向右侧平稳扭转，骨盆与膝盖保持朝向正前方不晃动。",
            "在转体侧顶点顶峰收缩停顿 1 秒，吸气匀速回正，顺畅向左侧旋转，左右交替按计划重复。",
        ],
    },
    "0850": {
        "name_zh": "瑜伽球坐姿单侧负重侧屈",
        "category": "waist",
        "equipment": "weighted",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在瑜伽球球面上，双脚分开与肩同宽平踩地面，保持骨盆水平与脊柱中立。",
            "单手持哑铃或杠铃片自然垂于体侧，另一手轻扶头后或叉腰维持平衡。",
            "吸气主要由持重侧对侧腹斜肌离心受控，让躯干向持重侧平稳侧屈下放重物。",
            "呼气由腹内斜肌与腹外斜肌强力向心收缩发力，将上半身拉回垂直中位并向对侧微提顶峰收缩 1 秒，按计划完成单侧后换边重复。",
        ],
    },
    "0851": {
        "name_zh": "负重西斯深蹲",
        "category": "upper legs",
        "equipment": "weighted",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立，单手或双手抱持杠铃片置于胸前，另一手可轻扶固定立柱或深蹲架辅助平衡。",
            "挺胸收紧核心，膝关节主动向前推送弯曲，脚跟自然抬起前脚掌抓地支撑，躯干与大腿保持同一直线向后倾斜。",
            "吸气下蹲至大腿股四头肌达到最大深度拉伸，保持下背部挺直核心锁紧。",
            "呼气由股四头肌全力收缩爆发发力，推蹬前脚掌将躯干与大腿推回直立起始位，在最高点顶峰收紧股四头肌，按计划重复。",
        ],
    },
    "0852": {
        "name_zh": "负重深蹲",
        "category": "upper legs",
        "equipment": "weighted",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quads", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽或略宽站立，脚尖微朝外自然展开约 15-30 度，双手抱持哑铃或杠铃片置于胸前。",
            "挺胸沉肩收紧核心，吸气屈髋屈膝同时进行，臀部向后下方平稳坐下，膝盖轨迹与脚尖方向保持一致。",
            "下蹲至大腿平行于地面或略低于膝关节水平，保持背部平直不弓腰。",
            "呼气由臀大肌与股四头肌协同强力发力，推蹬全脚掌站起回至起始直立位，在顶点顶峰收缩臀肌停顿 1 秒，按计划重复。",
        ],
    },
    "0853": {
        "name_zh": "站姿负重弯举",
        "category": "upper arms",
        "equipment": "weighted",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，双膝微屈弹性站立，双手各持哑铃或合抱杠铃片垂于身体前方，掌心朝前上方。",
            "挺胸收腹沉肩，双肘紧贴躯干两侧固定作为转动轴心。",
            "呼气主要由肱二头肌集中收缩发力，屈肘将负重向上弯举至胸前肩膀高度，大臂与躯干保持静止不借力前摆。",
            "在弯举最高顶点顶峰收缩挤压二头肌停顿 1 秒，吸气匀速受控放低负重回至起始手臂伸直位，按计划重复。",
        ],
    },
    "0854": {
        "name_zh": "站姿负重杠铃片捏握",
        "category": "lower arms",
        "equipment": "weighted",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽直立站立，双膝微屈，挺胸沉肩收紧核心。",
            "双手各用手指指腹捏住一片或两片光滑杠铃片边缘（指尖向内，掌心不贴紧片面），双臂自然垂于大腿两侧。",
            "屈指肌群与前臂肌群强力发力紧捏杠铃片，保持抓握张力不松懈，避免杠铃片滑落。",
            "全程保持呼吸均匀顺畅，稳定维持高强度捏握张力至目标时长或完成受控抓捏重复组，按计划重复。",
        ],
    },
    "0856": {
        "name_zh": "负重斯文德推胸",
        "category": "chest",
        "equipment": "weighted",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽自然站立，双手手掌对合，将一片或两片杠铃片牢固夹在双掌之间，紧贴胸部中央。",
            "挺胸沉肩锁死肩胛骨，双手掌心用力向内对挤杠铃片，使胸大肌内侧与中缝产生强烈的等长收缩。",
            "呼气保持双手持续向内强力对夹杠铃片的同时，平稳缓慢地将手臂向前水平推送完全伸直。",
            "在最远伸直点顶峰收缩停顿 1 秒深度挤压胸肌，吸气维持对挤张力受控收回双手至贴胸起始位，按计划重复。",
        ],
    },
    "0857": {
        "name_zh": "跪姿健腹轮前滚",
        "category": "waist",
        "equipment": "wheel roller",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["lower back", "lats", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双膝跪在训练垫上，小腿平贴地面，双手全握健腹轮两侧把手，垂直置于肩膀正下方地面。",
            "微收下巴，收紧腹部核心与骨盆后倾，背部保持微弓弧度锁紧核心。",
            "吸气主要由腹直肌离心发力受控，缓慢推动健腹轮向前平稳滚动，躯干与手臂向前延伸直至接近地面。",
            "在最远伸展受控点停顿 1 秒保持腹肌紧绷，呼气由腹直肌与背阔肌协同收缩，驱动身体拉回健腹轮至起始跪姿位，按计划重复。",
        ],
    },
    "0859": {
        "name_zh": "站姿手腕滚筒卷绳",
        "category": "lower arms",
        "equipment": "weighted",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，双手正握手腕滚筒横杆两侧，双臂向前水平伸直与地面平行抬至胸部高度。",
            "挺胸沉肩锁紧肩胛，将悬挂有负重杠铃片的绳索自然下垂延伸至地面。",
            "双臂保持水平固定，呼气由手腕伸肌与屈肌交替向内转动横杆卷起绳索，驱动杠铃片匀速向上提升。",
            "将重物卷至横杆顶端后，吸气手腕受控反向交替转动缓慢放低绳索回至底端，按计划重复。",
        ],
    },
    "0860": {
        "name_zh": "绳索单臂俯身臂屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对低位或中位滑轮绳索机站立，单手握住单手柄或绳索扣，后退一步使缆绳保持初始张力。",
            "屈髋屈膝俯身，上半身前倾约 45-60 度并保持背部平直，另一手扶在膝盖或机柱上维持稳定支撑。",
            "持握手臂的大臂紧贴体侧并向后抬起至与躯干接近平行，屈肘 90 度作为动作旋转轴心。",
            "呼气主要由肱三头肌强力向心收缩发力，伸展肘关节将前臂平稳向后上方伸直，直至整条手臂完全锁直。",
            "在手臂最顶端完全伸直点顶峰收缩挤压肱三头肌停顿 1 秒，吸气匀速受控屈肘放回前臂至 90 度起始位，按计划完成单侧后换边重复。",
        ],
    },
}

pending = {
    "0849": "待修图 · 消除括号后缀规范为瑜伽球坐姿负重转体；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0850": "待修图 · 规范单侧动作为瑜伽球坐姿单侧负重侧屈；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0851": "待修图 · 纠正坐姿深蹲严重错译规范为负重西斯深蹲；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0852": "待修图 · 规范负重深蹲标准动作命名；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0853": "待修图 · 规范站姿动作命名为站姿负重弯举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0854": "待修图 · 消除握力直译规范为站姿负重杠铃片捏握；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0856": "待修图 · 纠正推举直译规范为负重斯文德推胸；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0857": "待修图 · 消除轮式滚出直译规范为跪姿健腹轮前滚；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0859": "待修图 · 消除手腕滚轮直译规范为站姿手腕滚筒卷绳；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0860": "待修图 · 消除后推直译规范为绳索单臂俯身臂屈伸；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review100-20261217",
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
    "expected_per_side_ids": ["0850", "0860"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
