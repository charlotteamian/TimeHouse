#!/usr/bin/env python3
"""Author Batch 114 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261231_review114"
VERSION = "1.2.119"
VERSION_CODE = 2026123101

inspected = ["1378", "1383", "1384", "1385", "1388", "1389", "1391", "1392", "1393", "1394"]
review_candidates = []
registered_media = []

definition_updates = {
    "1378": {
        "name_zh": "站姿绳带勾脚单腿小腿拉伸",
        "category": "lower legs",
        "equipment": "rope",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "单腿直立站稳并保持躯干挺直，另一侧工作腿向前下方伸直，将辅助拉伸绳绕过该侧前脚掌底部，双手握紧绳索两端。",
            "保持支撑腿踩稳与核心微收紧，随手部温和向回牵拉绳索并带动工作腿适度上抬前伸。",
            "轻缓将工作侧脚尖勾向身体方向，感受小腿后侧腓肠肌与腘绳肌下端出现清晰舒适的牵拉感。",
            "在拉伸感充分处保持平稳深呼吸数秒后温和放松，单腿完成后换边重复。",
        ],
    },
    "1383": {
        "name_zh": "哈克机面朝内双脚提踵",
        "category": "lower legs",
        "equipment": "sled machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对哈克深蹲机靠背站上斜板踏台，双肩稳固顶住肩垫、双手扶握旁侧把手并打开安全锁。",
            "双脚与肩同宽，仅将前脚掌踩在踏台边缘，让双侧后脚跟自然悬空下沉充分拉长小腿。",
            "呼气小腿肌群集中发力向上蹬高双脚后跟，直至踝关节达到最高跖屈位。",
            "在顶峰收缩停顿片刻，吸气缓慢受控下沉脚跟低于踏板面充分拉伸，按计划重复。",
        ],
    },
    "1384": {
        "name_zh": "哈克机面朝内单腿提踵",
        "category": "lower legs",
        "equipment": "sled machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对哈克机站稳并将双肩卡稳垫下，双手扶住机架握把并打开安全锁扣。",
            "工作侧单脚前脚掌踩牢踏台边缘使脚跟悬空下沉，另一侧非工作腿屈膝向后抬离踏台。",
            "保持髋部稳定不向工作侧倾斜，呼气单侧小腿强力收缩向上推高脚跟至最高处。",
            "顶端收缩停顿片刻后吸气缓慢下沉脚跟还原，单腿完成计划次数后换腿重复。",
        ],
    },
    "1385": {
        "name_zh": "器械坐姿直腿蹬踏小腿提踵",
        "category": "lower legs",
        "equipment": "leverage machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整坐姿蹬腿机座椅前后距，背部紧贴靠垫，双脚与肩同宽仅以前脚掌踩稳前踏板下缘使脚跟悬空。",
            "伸直双膝（保留微屈避免完全锁死关节），双手紧握座椅两侧固定握把。",
            "先控制脚跟向身体侧屈踝下压充分拉长小腿后侧，随后呼气用前脚掌全力向上前推踏板完成跖屈提踵。",
            "顶端收缩挤压小腿停顿片刻后吸气受控还原，按计划重复。",
        ],
    },
    "1388": {
        "name_zh": "坐姿绳带单腿腓骨肌拉伸",
        "category": "lower legs",
        "equipment": "rope",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["ankles", "feet"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐于防滑地面或训练垫上，双腿向前自然伸直，将拉伸绳或弹力带绕过工作侧单脚前脚掌底部。",
            "保持工作腿伸直放松，双手拉紧绳带两端并轻微引导脚踝做温和内翻勾脚动作。",
            "向自己方向轻柔牵拉绳带，重点感受工作侧小腿外侧腓骨肌群得到循序拉伸。",
            "平稳深呼吸停留数秒后缓慢放松张力，单腿完成后换边重复。",
        ],
    },
    "1389": {
        "name_zh": "坐姿绳带单腿胫骨后肌拉伸",
        "category": "lower legs",
        "equipment": "rope",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在训练垫或地板上，双腿在体前伸直，用拉伸绳或带套住工作侧单脚前脚掌，双手握住绳带两端。",
            "维持工作侧膝关节微伸挺拔坐姿，温和勾回脚尖并配合极轻度外翻引导。",
            "缓缓向自身方向牵拉绳带，体会小腿深层与内后侧胫骨后肌延伸舒展。",
            "保持舒适牵拉感数秒后松弛复位，单腿完成后换边重复。",
        ],
    },
    "1391": {
        "name_zh": "倒蹬机双脚蹬踏小腿提踵",
        "category": "lower legs",
        "equipment": "sled machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐稳于倒蹬机上，腰背紧贴靠垫并握紧两侧安全手把，将双脚与肩同宽仅以前脚掌踩在踏板下缘。",
            "推起雪橇并打开安全卡扣，双腿伸至膝关节微屈稳定状态并锁住大肌群位置不变。",
            "吸气控制前脚掌屈踝让踏板随脚尖向自身方向下压充分拉伸小腿，随后呼气用前脚掌爆发或稳步推起脚跟伸展踝关节。",
            "顶峰收缩停顿片刻后控制还原下放，按计划次数结束后务必挂回安全锁。",
        ],
    },
    "1392": {
        "name_zh": "斜卧倒蹬机单腿小腿蹬伸",
        "category": "lower legs",
        "equipment": "sled machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "斜躺坐稳于斜卧倒蹬机上，腰背贴紧靠垫，将非工作侧脚稳固放回地面，工作侧单脚前脚掌踩在踏板下缘并打开安全锁。",
            "保持工作腿膝关节微屈固定不锁死，吸气控制脚跟向身体侧屈踝深沉拉伸单侧小腿。",
            "呼气单侧小腿肌肉集中发力，用前脚掌向前上方蹬伸推起雪橇踏板。",
            "在顶峰停顿片刻后控制放回深度拉伸位，单腿完成计划次数、挂回安全锁后再换腿重复。",
        ],
    },
    "1393": {
        "name_zh": "史密斯机扛杆站姿单腿提踵",
        "category": "lower legs",
        "equipment": "smith machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站在史密斯机正中背对开口或正向就位，将横杆扛稳在上背部斜方肌上方，双手抓握横杆并转开安全锁。",
            "工作侧单脚前脚掌踩实地面垫块或防滑地面，另一侧非工作腿屈膝后勾悬空离地。",
            "保持核心收紧躯干直立，呼气仅依靠工作腿踝关节发力将后脚跟尽力向上踮至最高点。",
            "顶峰停顿 1 秒后吸气缓慢受控下沉脚跟还原，单腿完成计划次数后换腿重复。",
        ],
    },
    "1394": {
        "name_zh": "史密斯机反站姿踏台提踵",
        "category": "lower legs",
        "equipment": "smith machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings"],
        "required_equipment_zh": ["稳固踏台"],
        "instructions_zh": [
            "在史密斯机横杆下方放置稳固踏台，站上踏台背对立柱方向将横杆扛稳于上背部，双手抓牢横杆并解锁。",
            "双脚与髋同宽仅以前脚掌踩在踏台前缘使后脚跟自然悬空下沉，充分预拉伸小腿。",
            "收紧核心避免腰椎前凸借力，呼气小腿发力将双侧后脚跟尽可能向上踮起至高点。",
            "顶端停顿片刻后吸气受控下放脚跟低于踏台平面，按计划重复。",
        ],
    },
}

pending = {
    "1378": "待修图 · 规范并纠正原名与步骤和抬腿勾脚拉绳画面不符为站姿绳带勾脚单腿小腿拉伸（激活单腿计次）；原动图仅 2 帧且右缘绳带裁切，待重制。",
    "1383": "待修图 · 纠正原名过简缺器械为哈克机面朝内双脚提踵；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1384": "待修图 · 规范为哈克机面朝内单腿提踵并保持单侧计次；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1385": "待修图 · 去括号规范为器械坐姿直腿蹬踏小腿提踵；原动图 10 帧且帧率与循环节奏不合规，待重制为标准 4 帧循环图。",
    "1388": "待修图 · 纠正腓肠肌误译为坐姿绳带单腿腓骨肌拉伸并激活单侧计次；原素材为仅 2 帧的满屏实景倾斜边框照片，待重制为标准 4 帧解剖循环图。",
    "1389": "待修图 · 规范为坐姿绳带单腿胫骨后肌拉伸并激活单侧计次；原素材为仅 2 帧的满屏实景照片，待重制为标准 4 帧解剖循环图。",
    "1391": "待修图 · 规范为倒蹬机双脚蹬踏小腿提踵；原动图 10 帧且底缘存在多余半圆黑色杂影，待重制为标准 4 帧循环图。",
    "1392": "待修图 · 规范为斜卧倒蹬机单腿小腿蹬伸并纠正步骤中双脚误写，保留单侧计次；原动图 10 帧且底缘存在杂点横杠，待重制为标准 4 帧循环图。",
    "1393": "待修图 · 规范为史密斯机扛杆站姿单腿提踵并纠正原步骤放在小腿上错写，保留单侧计次；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1394": "待修图 · 规范为史密斯机反站姿踏台提踵并补全稳固踏台支持器械及扛肩步骤；原动图仅 2 帧，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review114-20261231",
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
        "1394": ["稳固踏台"],
    },
    "expected_per_side_ids": ["1378", "1384", "1388", "1389", "1392", "1393"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
