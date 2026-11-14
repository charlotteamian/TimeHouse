#!/usr/bin/env python3
"""Author Batch 101 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261218_review101"
VERSION = "1.2.106"
VERSION_CODE = 2026121801

inspected = ["0861", "0862", "0866", "0868", "0869", "0873", "0874", "0968", "0969", "0970"]
review_candidates = []
registered_media = []

definition_updates = {
    "0861": {
        "name_zh": "绳索坐姿划船",
        "category": "back",
        "equipment": "cable",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["lats", "biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在绳索低位划船机平凳上，双脚平踩踏板边缘，双膝微屈维持弹性支撑，躯干挺直沉肩。",
            "双手对握双柄把手或横杆把手，手臂向前自然伸直带动肩胛骨充分向前舒展拉伸。",
            "呼气由上背肌群与背阔肌集中收缩发力，屈肘顺畅将把手平稳拉向肚脐前方，主动后缩并下沉双侧肩胛骨。",
            "在划船顶点顶峰收缩挤压上背肌群停顿 1 秒，吸气匀速受控放回双臂至起始拉伸位，躯干保持稳定不前后借力晃动，按计划重复。",
        ],
    },
    "0862": {
        "name_zh": "绳索站姿斜向转体",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧对低位或高位滑轮绳索机站立，双脚与肩同宽微屈膝站立，双手握住单手柄置于体侧斜上方或斜下方。",
            "挺胸收腹，双臂微屈微张锁定，核心肌群预先收紧以稳定下肢与骨盆。",
            "呼气主要由腹内斜肌与腹外斜肌发力，带动躯干受控沿对角线方向平稳斜向旋转推送手柄至对侧。",
            "在旋转顶点顶峰收紧腹斜肌停顿 1 秒，吸气匀速受控沿对角原轨迹缓慢放回手柄至起始位，左右交替或换边按计划重复。",
        ],
    },
    "0866": {
        "name_zh": "悬挂负重举腿提臀",
        "category": "waist",
        "equipment": "weighted",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双手正握单杠悬挂，握距与肩同宽，双脚脚踝稳固夹持哑铃或穿戴负重沙袋，身体自然下垂。",
            "挺胸沉肩锁死肩带，避免肩部被动耸起，核心肌群紧绷收紧以抑制身体前后晃动摆动。",
            "呼气主要由腹直肌强力收缩发力，骨盆向后向上卷动，带动双腿平稳向前上方抬升至大腿超过水平面并抬起臀部。",
            "在举腿卷骨盆最高点顶峰收缩停顿 1 秒充分挤压腹肌，吸气匀速受控放慢下放双腿回至起始垂悬位，按计划重复。",
        ],
    },
    "0868": {
        "name_zh": "绳索站姿弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对低位滑轮绳索机站立，双手反握直杆或双头绳把手，双脚平踩地面与肩同宽，双臂自然下垂。",
            "挺胸沉肩收腹，大臂贴紧身体两侧固定作为转动轴心，避免肩部与躯干借力前摆。",
            "呼气主要由肱二头肌集中收缩发力，屈肘将把手平稳向上弯举至胸前肩膀高度。",
            "在弯举顶点顶峰收缩挤压二头肌停顿 1 秒，吸气匀速受控放低把手回至起始手臂伸直位，按计划重复。",
        ],
    },
    "0869": {
        "name_zh": "器械坐姿推肩第二式",
        "category": "shoulders",
        "equipment": "leverage machine",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节器械座椅高度，使握把位置处于肩膀水平高度，端坐在座椅上，背部与臀部紧贴靠背，双脚平踩地面。",
            "双手对握或正握推肩手柄，挺胸收腹，双肘微张处于身体前侧斜切面平面内。",
            "呼气主要由三角肌前束与中束集中发力，协同肱三头肌向上平稳推起手柄至双臂接近伸直但肘关节不锁死。",
            "在推举顶点顶峰收缩停顿 1 秒挤压肩部肌群，吸气匀速受控缓慢放低手柄回至耳朵高度起始位，按计划重复。",
        ],
    },
    "0873": {
        "name_zh": "绳索仰卧反向卷腹",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors", "obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "平躺在训练垫上，脚踝佩戴脚环系于低位滑轮缆绳，或双手过头抓住低位把手，膝盖弯曲约 90 度并离地。",
            "下背部紧贴地面，微收下巴，腹部肌群预先收紧稳定骨盆。",
            "呼气由腹直肌下部集中收缩发力，带动骨盆与臀部向胸部方向卷起抬离地面，双膝向胸口受控靠近。",
            "在卷腹最高点顶峰收缩挤压下腹肌停顿 1 秒，吸气匀速受控放低骨盆与双腿回至起始位，下背部保持贴地，按计划重复。",
        ],
    },
    "0874": {
        "name_zh": "绳索站姿绳把卷腹",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对高位滑轮绳索机站立，双手全握双头绳把手两端拉至头后颈侧，双膝微屈维持下肢稳固站姿。",
            "固定双手与把手在耳侧头部位置，骨盆保持稳定中立不后仰。",
            "呼气由腹直肌集中收缩发力，低头含胸向前下方卷曲躯干，驱动手肘向膝盖方向弯屈卷拢。",
            "在卷腹最底端顶峰收缩强力挤压腹肌停顿 1 秒，吸气受控放缓躯干展开回至直立起始位，按计划重复。",
        ],
    },
    "0968": {
        "name_zh": "站姿弹力带交替弯举",
        "category": "upper arms",
        "equipment": "band",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚踩在弹力带中段与肩同宽站立，双手反握把手或带端垂于身体两侧，掌心朝前上方。",
            "挺胸沉肩收腹，双肘紧贴躯干两侧固定作为转动轴心。",
            "呼气单侧肱二头肌集中收缩发力，屈肘将一侧把手向上弯举至肩膀高度，另一侧手臂保持伸直稳定。",
            "在弯举顶点顶峰收缩挤压二头肌停顿 1 秒，吸气匀速受控放低，随后换对侧手臂屈肘弯举，左右交替按计划重复。",
        ],
    },
    "0969": {
        "name_zh": "弹力带仰卧交替V字卷腹",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors", "obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在训练垫上，双手拉住弹力带两端过头伸展，双腿伸直脚尖绷直微抬离地面。",
            "吸气预备，呼气腹直肌爆发向心收缩，上半身与单侧直腿同时折叠抬起呈 V 字形态，双手将弹力带拉向抬起的脚踝前方。",
            "在最高折叠点顶峰收缩挤压腹部核心停顿 1 秒，吸气匀速受控放平躯干与下肢回至悬空预备位。",
            "顺畅换对侧腿与躯干折叠卷屈，左右双腿交替按计划重复。",
        ],
    },
    "0970": {
        "name_zh": "弹力带辅助引体向上",
        "category": "back",
        "equipment": "band",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "upper back", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将环状弹力带一端穿套并牢固挂在单杠横杆中央，单脚或双膝踩入弹力带底圈提供向上弹性辅助。",
            "双手正握单杠，握距略宽于肩宽，双臂完全伸直垂悬，挺胸沉肩收紧核心。",
            "呼气主要由背阔肌与上背肌群集中收缩发力，双肘向身体两侧下方拉动，将胸部上沿拉向单杠，直至下巴超过横杆高度。",
            "在最高点顶峰收紧背阔肌停顿 1 秒，吸气在弹力带辅助下匀速受控放慢下放身体回至完全悬挂位，按计划重复。",
        ],
    },
}

pending = {
    "0861": "待修图 · 规范划船命名为绳索坐姿划船；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0862": "待修图 · 消除上下扭转直译规范为绳索站姿斜向转体；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0866": "待修图 · 规范抬腿抬髋命名为悬挂负重举腿提臀；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0868": "待修图 · 规范站姿动作命名为绳索站姿弯举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0869": "待修图 · 消除括号与英文标识规范为器械坐姿推肩第二式；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0873": "待修图 · 规范仰卧反向卷腹为绳索仰卧反向卷腹；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0874": "待修图 · 消除带绳索附件直译规范为绳索站姿绳把卷腹；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0968": "待修图 · 规范站姿交替动作为站姿弹力带交替弯举；原动图帧时长不合规且边缘杂色，待重制为标准 4 帧循环图。",
    "0969": "待修图 · 消除屈体卷腹直译规范为弹力带仰卧交替V字卷腹；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0970": "待修图 · 规范辅助引体动作为弹力带辅助引体向上；原动图严重顶底触边裁剪且帧时长不合规，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review101-20261218",
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
