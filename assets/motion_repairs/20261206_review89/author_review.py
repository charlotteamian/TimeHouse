#!/usr/bin/env python3
"""Author Batch 89 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261206_review89"
VERSION = "1.2.94"
VERSION_CODE = 2026120601

inspected = ["0552", "0553", "0554", "0562", "0571", "0572", "0573", "0574", "0575", "0576"]
review_candidates = []
registered_media = []

definition_updates = {
    "0552": {
        "name_zh": "站姿双臂壶铃垂膝高翻",
        "category": "shoulders",
        "equipment": "kettlebell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "forearms", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽稳固站立，双手握持壶铃手柄自然垂于体前，屈髋微屈膝保持脊柱平直中立。",
            "挺胸沉肩紧收核心，目视前方，重心落于足弓中后部建立初始爆发拉起势能。",
            "呼气由臀腿协同爆发性伸髋蹬地，顺势带动双臂快速提拉壶铃，在壶铃上行至胸肩高度瞬间顺畅反转手腕进入架式位。",
            "在双肩架式位稳定承托停顿 1 秒，吸气顺势翻转手腕受控沿体前垂直路径落回起始垂膝位置，按规定次数重复。",
        ],
    },
    "0553": {
        "name_zh": "站姿双壶铃军式推举",
        "category": "shoulders",
        "equipment": "kettlebell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢或与肩同宽站立，双手各握持一个壶铃架在双肩前侧，掌心相对或微朝前，肘关节垂直朝向地面。",
            "收紧臀肌并紧绷核心维持骨盆中立，脊柱自然伸直挺胸沉肩，避免推举过程中骨盆前倾或后仰借力。",
            "呼气由双侧三角肌发力，驱动两个壶铃垂直向上推举至头顶上方直至双臂完全伸展锁定。",
            "在头顶最高点稳定停顿 1 秒充分感受肩部承重收缩，吸气控制两个壶铃缓慢匀速沿原推举轨迹落回肩前架式位，按计划重复。",
        ],
    },
    "0554": {
        "name_zh": "站姿单臂壶铃标准风车",
        "category": "waist",
        "equipment": "kettlebell",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "shoulders", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚开立略宽于肩，非负重侧脚尖向外旋转约 45 度，单臂将壶铃高举垂直锁定在头顶上方。",
            "挺胸收腹，目光始终保持仰视头顶壶铃，重心微微偏向负重侧腿部保持肩关节锁定稳定。",
            "吸气以负重侧髋关节为轴屈髋侧屈俯身，非负重侧手臂顺着同侧小腿内侧自然向下滑动下探至脚踝或地面。",
            "在最低拉伸点保持躯干与手臂稳定停顿 1 秒，呼气由腹斜肌群与臀部发力将身体拉回直立起始位，单侧做完后换另一侧。",
        ],
        "perSide": True,
    },
    "0562": {
        "name_zh": "站姿杠铃地雷管180度转体",
        "category": "waist",
        "equipment": "barbell",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "shoulders", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽稳固站立，双手在胸前正中紧握地雷管杠铃杆末端，手臂微屈保持锁止。",
            "挺胸立腰收紧腹部核心，双膝微屈，目光注视杠铃杆末端端点。",
            "吸气由躯干核心主导带动双臂划出顺畅弧线向一侧髋部方向转体下沉，髋关节协同微转保持平衡。",
            "在侧向转体最低点短暂停顿 1 秒，呼气由腹外斜肌与深层核心肌群爆发发力将杠铃沿大半圆弧线推回中线并划向对侧髋部，交替往返循环。",
        ],
    },
    "0571": {
        "name_zh": "器械坐姿交替窄握划船",
        "category": "back",
        "equipment": "leverage machine",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms", "lats"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整划船器械座椅高度与胸垫间距，坐在坐垫上双脚平踏前方踏板，挺胸背部平直贴靠胸垫。",
            "双手对握抓持两侧窄握手柄，初始手臂自然向前伸展，肩胛骨保持下沉稳定。",
            "呼气由一侧背阔肌与上背肌群协同发力，驱动单侧手柄向后拉向躯干侧方，对侧手柄保持平稳伸直固定。",
            "在拉至顶点肩胛骨完全收拢夹紧停顿 1 秒，吸气控制受控向前顺滑回放，随后无缝切换对侧进行单侧划船，交替循环完成规定次数。",
        ],
    },
    "0572": {
        "name_zh": "器械辅助反握引体向上",
        "category": "back",
        "equipment": "leverage machine",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "根据体能水平调节助力配重块，双手反握抓持器械横杆掌心朝向自己，双膝平稳跪在助力垫板中央。",
            "双臂向上伸展充分悬吊拉伸背阔肌，沉肩挺胸收紧核心，躯干保持垂直中立微向后仰。",
            "呼气由背阔肌与肱二头肌强力收缩，驱动身体向上拉起，肘部向身体两侧后下方夹紧，直至下巴超过握把高度。",
            "在最高点肩胛骨用力下压收紧停顿 1 秒，吸气受控抵抗助力平稳匀速下放身体回至初始悬臂拉伸状态，按计划重复。",
        ],
    },
    "0573": {
        "name_zh": "器械坐姿背屈伸",
        "category": "back",
        "equipment": "leverage machine",
        "target": "spine",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整背屈伸器械座椅高度与靠垫旋转轴心，确保阻力滚筒贴合在上背或肩胛骨下缘，双脚踩实踏板。",
            "坐在坐垫上双手握住两侧固定把手，上身自然微屈向前倾斜，下背部保持舒适拉伸状态。",
            "呼气由竖脊肌与后链肌群主动发力，克服器械阻力向后平稳伸展躯干，直至上身与髋部呈平直延伸线。",
            "在后屈伸顶点保持背肌与臀肌顶峰收紧停顿 1 秒，注意避免腰椎过度后仰超伸，吸气匀速受控前倾回放至起始位，按计划重复。",
        ],
    },
    "0574": {
        "name_zh": "站姿杠铃地雷管俯身划船",
        "category": "back",
        "equipment": "barbell",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms", "lats"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽微屈膝站立，屈髋俯身保持背部平直挺胸，双手正手抓握杠铃杆或地雷管手柄。",
            "肩胛骨下沉稳定，脊柱保持自然生理曲度，手臂自然下垂充分伸展。",
            "呼气由上背肌群与背阔肌主动收缩发力，屈肘沿身体侧向将杠铃平稳拉向下胸与腹部之间。",
            "拉至最高点用力收缩夹紧双侧肩胛骨停顿 1 秒，吸气匀速受控将杠铃下放回至初始悬垂拉伸状态，按计划重复。",
        ],
    },
    "0575": {
        "name_zh": "器械坐姿二头弯举",
        "category": "upper arms",
        "equipment": "leverage machine",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节弯举器械座椅高度，坐稳后将双臂平稳托放在倾斜托垫上，手肘与器械旋转轴心对齐。",
            "双手反握抓持旋转把手掌心朝上，上身微前倾保持挺胸，双臂在托垫上自然伸展。",
            "呼气由肱二头肌主动发力，克服器械阻力向上屈肘弯举把手，保持上臂与手肘紧贴托垫不抬起。",
            "弯举至顶点双峰用力挤压肱二头肌停顿 1 秒，吸气控制把手匀速缓慢下放回双臂接近完全伸展起始位，按计划重复。",
        ],
    },
    "0576": {
        "name_zh": "器械坐姿推胸",
        "category": "chest",
        "equipment": "leverage machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节推胸器械座椅高度，确保推胸握把位于胸部中中部水平线，背部与臀部紧贴靠背，双脚踩实地面。",
            "双手握紧推胸把手掌心朝下或微相对，沉肩挺胸，肩胛骨收紧贴紧后靠垫。",
            "呼气由胸大肌发力带动肱三头肌协同推进，向前平稳推起把手直至双臂充分伸展，注意手肘不超伸锁死。",
            "在推起最高点顶峰收缩胸大肌停顿 1 秒，吸气控制把手匀速缓慢后撤回放至胸大肌充分拉伸起始位，按计划重复。",
        ],
    },
}

pending = {
    "0552": "待修图 · 消除英文字符与机器直译规范为站姿双臂壶铃垂膝高翻；原动图首帧时长异常且边缘存在杂色像素，待重制为 4 帧循环图。",
    "0553": "待修图 · 规范军式推举规范为站姿双壶铃军式推举；原动图首帧时长异常且边缘存在杂色像素，待重制为 4 帧循环图。",
    "0554": "待修图 · 消除风车单一简译并激活单侧独立计次规范为站姿单臂壶铃标准风车；原动图首帧时长异常且边缘存在杂色像素，待重制为 4 帧循环图。",
    "0562": "待修图 · 消除数字缩写与机器错译规范为站姿杠铃地雷管180度转体；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0571": "待修图 · 消除杠杆直译规范器械术语为器械坐姿交替窄握划船；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0572": "待修图 · 消除杠杆直译并规范引体向上握法为器械辅助反握引体向上；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0573": "待修图 · 消除杠杆直译规范器械动作命名为器械坐姿背屈伸；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0574": "待修图 · 消除杠杆直译规范为站姿杠铃地雷管俯身划船；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0575": "待修图 · 消除杠杆直译规范器械动作命名为器械坐姿二头弯举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0576": "待修图 · 消除杠杆直译规范器械推胸术语为器械坐姿推胸；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review89-20261206",
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
    "expected_per_side_ids": ["0554"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
