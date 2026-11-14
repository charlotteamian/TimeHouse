#!/usr/bin/env python3
"""Author Batch 46 review updates, pending notes, sources, code baseline, and QA spec."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261024_review46"
VERSION = "1.2.51"
VERSION_CODE = 2026102401

inspected = ["2466", "1666", "2567", "1667", "2571", "1668", "2801", "1669", "2802", "1670"]
review_candidates = ["1669"]
registered_media = ["1669"]

definition_updates = {
    "2466": {
        "name_zh": "俯撑交替交叉抬膝登山跑",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["glutes", "quadriceps", "hamstrings", "shoulders", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "从直臂俯撑高位起姿开始，双手压实于肩关节正下方，双脚向后伸直以脚尖蹬地、头肩髋踝保持直线。",
            "收紧核心与臀腹稳定骨盆不塌腰、不过分抬臀，顺势将一侧膝盖斜向提向对侧手肘下方。",
            "迅速将腿还原后随呼吸切换另一条腿斜向交替提膝，保持平稳流畅节奏。",
        ],
    },
    "1666": {
        "name_zh": "平凳俯卧单臂锤式哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "俯卧在平板训练凳上，双腿向后分立以脚尖稳踩地面，非工作手轻握凳垫前缘固定躯干。",
            "工作手掌心朝内锤握一只哑铃自然垂臂向下伸直。",
            "保持大臂稳固定位不动，呼气顺锤握轨迹向上弯举哑铃靠向胸肩前方，停顿后缓慢放回并在完成后换臂。",
        ],
    },
    "2567": {
        "name_zh": "单侧坐姿盘腿转体梨状肌拉伸",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "glutes",
        "muscle_group": "glutes",
        "secondary_muscles": ["hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在地面上并将一侧腿伸直平贴地面，将另一侧腿屈膝跨过并把脚掌稳踩在伸直腿外侧地面。",
            "双手轻扶垫面及跨腿膝外侧协助稳定躯干直立，呼气轻轻向屈膝侧转动上身，用对侧手肘或手臂轻抵膝外侧增加深层臀肌拉伸。",
            "在舒适拉伸位短暂停顿感受臀部深层牵伸后缓慢回正，并在完成后换边拉伸。",
        ],
    },
    "1667": {
        "name_zh": "站姿单臂反握哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽直立站稳，非工作手自然垂放体侧维持躯干不晃动，工作手握住一只哑铃垂于身侧。",
            "保持大臂贴近躯干稳定不动，呼气以肘为轴向上弯举哑铃靠近胸肩前。",
            "顶点略作停顿感受肱二头肌充分收紧后吸气缓慢受控放回起始垂臂位，完成次数后换臂。",
        ],
    },
    "2571": {
        "name_zh": "四足跪姿前俯后坐臀腿拉伸",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "glutes",
        "muscle_group": "glutes",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "四足跪姿准备，双膝分开与髋同宽贴稳地面，双手在身前肩下伸直铺开按压地面。",
            "吸气维持脊柱中立平直，呼气有控制地顺势将臀部向后上方推坐同时延长双臂前伸。",
            "在后坐拉伸顶点短暂停顿感受臀部与腘绳肌舒展后缓慢前移还原，循环重复。",
        ],
    },
    "1668": {
        "name_zh": "瑜伽球坐姿单臂哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "端坐在瑜伽球顶部中央，双脚分开平踩地面保持核心挺直，非工作手轻搭在同侧大腿上稳定上身。",
            "工作手掌心朝上持一只哑铃垂臂伸直预备，保持大臂贴近身侧不动。",
            "呼气将哑铃向上弯举至肩前收缩位，停顿后吸气缓慢放回伸展起始位并在完成后换臂。",
        ],
    },
    "2801": {
        "name_zh": "仰卧屈膝交替转髋抬腿",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["obliques", "hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧平躺于地面，双手放在身体两侧稳定上背，双腿向正前方并拢伸直预备。",
            "收紧下腹屈膝抬起双腿至小腿水平，顺势将骨盆和屈曲双膝有控制地向一侧斜上拧转朝向对侧肩方向。",
            "在顶端略作停顿感受腹斜肌收缩后还原下放至近地面高度，再向另一侧交替重复。",
        ],
    },
    "1669": {
        "name_zh": "平凳坐姿抵腿单臂锤式哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐在平板训练凳前沿并保持背部直立、双脚分开平踩地面，非工作手轻搭对侧膝腿维持上身稳定。",
            "工作手掌心朝内锤握一只哑铃，将该侧肘部及大臂稳固贴抵于同侧大腿内侧膝关节上方。",
            "保持上臂稳抵大腿不动，呼气发力沿中立锤握弧线向上弯举哑铃靠向胸肩前方。",
            "在顶峰略作停顿感受肱二头肌与肱肌充分收紧后，吸气沿原轨迹缓慢受控放回起始位，完成目标次数后换臂。",
        ],
    },
    "2802": {
        "name_zh": "仰卧直腿交替转髋上举",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["obliques", "hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧平躺于地面，双腿并拢伸直，双手轻置臀部两侧下方或垫面以稳固骨盆与下背。",
            "收紧核心与下腹，保持双腿伸直抬离地面并顺势将髋部微向一侧斜上拧转朝向对侧肩方向。",
            "在最高点短暂停顿感受侧腹发力后缓慢下放双腿至近地面低位，再向相反一侧交替重复。",
        ],
    },
    "1670": {
        "name_zh": "站姿单臂哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽自然站直，非工作臂自然垂放体侧，工作手掌心朝前单臂握住哑铃充分伸直垂放。",
            "维持大臂稳定贴近躯干侧边不动，呼气发力弯举哑铃向上靠向胸肩前高位。",
            "顶峰停顿感受肱二头肌收缩后吸气缓慢放回垂臂起始位，完成规定次数后换另一侧手臂。",
        ],
    },
}

pending = {
    "2466": "待修图 · 登山跑支撑脚后移与提膝动态位姿变化（back_foot sc0=0.2557，max_res=10.63 px），已纠正“桥式/平板支撑”误述，待重制。",
    "1666": "待修图 · 经 F1 (+10,0)、F2 (0,+21) 平移后平凳左支腿 (+2) 与右支脚 (-2) 呈现 4 px 宽窄差异且面部匹配仅 0.7446（< 0.96），已补充平板训练凳与单臂资料，待重制。",
    "2567": "待修图 · F0 直腿坐姿切换至 F1/F2 跨腿扭转拉伸时下盘与髋膝大幅迁移（bottom sc0=0.3123/0.6068），已规范单侧与拉伸步骤，待重制。",
    "1667": "待修图 · 经 F1 (+3,0)、F2 (-2,0) 校准后 F2 双脚垂直 -1 px 而头顶 +1/+1 px（foot_right sc0=0.8801 < 0.96，head_crown sc0=0.8245 < 0.96），待重制。",
    "2571": "待修图 · 四足跪姿前俯后坐导致手掌与双膝大幅错位（bottom sc0=-0.0139/0.5124），已避免支撑与保持静态触发词，待重制。",
    "1668": "待修图 · 经原地测量头部相对于踩地双脚产生 -3 px 横移偏摆（head sc0=0.7976 < 0.96），已补充瑜伽球与单臂计数，待重制。",
    "2801": "待修图 · 仰卧屈膝抬腿向斜上方扭转骨盆导致下肢大幅迁移（bottom F2 sc0=0.0262），已清除原名性别标签，待重制。",
    "2802": "待修图 · 仰卧直腿转髋上举过程下肢大跨度升起（bottom sc0=0.0018/0.0034），已避免支撑静态词，待重制。",
    "1670": "待修图 · 经 F1 (+16,0) 对齐左右站姿后，F2 头部相对双脚存在 1 px 垂向伸缩差（dy2=0 时 head_crown sc0=0.9556 < 0.96；dy2=1 时 foot_right sc0=0.9478 < 0.96），诚实待重制。",
}

sources = {
    "1669": "https://raw.githubusercontent.com/exercemus/exercises/minified/exercises.json#dumbbell_one_arm_seated_hammer_curl"
}

review_notes = {
    "1669": "来源为 exercemus/exercises 公开动作库 1669（dumbbell one arm seated hammer curl）。补充平板训练凳必需支撑器械并核正肱二头肌/前臂目标及单臂分段计次，原地锁定 800/380/800/380 ms 四帧循环（F4=F2），纯白背景零边界截断，平凳左支腿、后支脚、右柱脚、双脚与头顶六大锚点均稳定对齐（最低匹配分 0.9728）。"
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review46-20261024",
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
    "expected_checks": 10,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_id": "1669",
    "candidate_required_equipment": ["平板训练凳"],
    "expected_per_side_ids": ["1666", "2567", "1667", "1668", "1669", "1670"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
