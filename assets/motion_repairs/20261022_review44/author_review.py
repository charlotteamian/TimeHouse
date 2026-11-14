#!/usr/bin/env python3
"""Author Batch 44 review updates, pending notes, sources, code baseline, and QA spec."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261022_review44"
VERSION = "1.2.49"
VERSION_CODE = 2026102201

inspected = ["2300", "1656", "2312", "1657", "2329", "1658", "2333", "1659", "2355", "1660"]
review_candidates = ["1659"]
registered_media = ["1659"]

definition_updates = {
    "2300": {
        "name_zh": "低杆屈膝自重反向划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "upper back",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": ["低位横杠"],
        "instructions_zh": [
            "将横杠调节至约腰腹高度，屈膝平踩地面并在横杠正下方仰面垂挂，双手略宽于肩正手握稳横杠，双臂伸直。",
            "收紧核心与臀部维持肩髋稳固，呼气收缩肩胛骨并将上胸主动拉向横杠。",
            "在最高点略作停顿后吸气缓慢伸直双臂下放回到低位起始姿。",
        ],
    },
    "1656": {
        "name_zh": "半圆平衡球坐姿哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms", "shoulders"],
        "required_equipment_zh": ["半圆平衡球"],
        "instructions_zh": [
            "稳坐在半圆平衡球顶面，双脚分开平踩地面维持膝角约九十度，双手掌心朝前各握一只哑铃垂放体侧。",
            "维持大臂贴靠躯干两侧不动，呼气同时屈肘将哑铃向上弯举至胸肩前方。",
            "顶峰略作停顿感受肱二头肌收紧后吸气有控制地缓慢放回伸展起始位。",
        ],
    },
    "2312": {
        "name_zh": "仰卧交替肘触对侧膝卷腹",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["hip flexors", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧于地面并屈膝踩地，双手轻虚托于耳后脑侧，双肘自然向两侧打开。",
            "呼气收紧腹斜肌抬起一侧肩背离地并顺势拧转躯干，以对侧手肘迎向抬起的膝盖，同时将另一条腿向前低位伸直。",
            "停顿后还原并随呼吸换向交替完成左右两侧屈膝转体触肘。",
        ],
    },
    "1657": {
        "name_zh": "站姿双臂交叉前锤式哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽自然站直，双手掌心朝内各握一只哑铃垂放体侧。",
            "保持躯干稳定与手肘靠近体侧，呼气顺斜前弧线将一侧哑铃沿胸前交叉向上弯举靠近对侧肩部。",
            "在顶点略作停顿后吸气沿原路径缓慢放回体侧，再交替或依次完成动作。",
        ],
    },
    "2329": {
        "name_zh": "坐姿屈膝转体肘触膝",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["obliques", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在地面上屈膝约九十度，双脚与髋同宽平踩地面，上身略微后倾并双手轻托头后。",
            "收紧腹部与腹斜肌，呼气缓慢向一侧旋转躯干，令对侧手肘靠向同侧膝盖上方。",
            "停顿感受腹斜肌收缩后回中立位，随后向另一侧交替重复转体动作。",
        ],
    },
    "1658": {
        "name_zh": "交替前跨弓步哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["quadriceps", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢或与肩同宽站立，双手掌心朝前各握哑铃垂放于大腿两侧。",
            "一侧脚向前跨出并屈膝下沉成稳固弓步位（后膝顺势下沉接近地面），同时顺势将双臂哑铃弯举至肩前高度。",
            "在底部短暂停顿后发力推前脚跟蹬起回到站立位并同步放回哑铃，随后换另一侧腿前跨交替。",
        ],
    },
    "2333": {
        "name_zh": "单杠直臂收腹直腿举",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["hip flexors", "shoulders"],
        "required_equipment_zh": ["单杠"],
        "instructions_zh": [
            "双手与肩同宽正握紧抓单杠，双臂伸直且双腿并拢直立垂落准备。",
            "呼气收紧核心与下腹，保持双腿伸直并向前上方抬起至接近水平或略高位置。",
            "在顶点短暂停顿后吸气缓慢有控制地放回垂直位，避免依靠惯性前后摆荡。",
        ],
    },
    "1659": {
        "name_zh": "瑜伽球坐姿双臂锤式哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "端坐在瑜伽球顶部中央，双脚分开稳踩地面维持骨盆中立与核心微收，双手掌心相对锤握哑铃自然垂放体侧。",
            "保持上臂稳固夹紧体侧不动，呼气发力屈肘同时将一对哑铃向上弯举至肩前高位。",
            "顶峰略作停顿感受肱肌与肱二头肌充分收缩后，吸气沿原轨迹缓慢受控放回起始伸展位。",
        ],
    },
    "2355": {
        "name_zh": "单杠直臂屈膝收腹抬腿",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["hip flexors", "shoulders"],
        "required_equipment_zh": ["单杠"],
        "instructions_zh": [
            "双手正握单杠与肩同宽，双臂伸直且屈膝双腿自然垂放于下方。",
            "呼气集中腹部发力并微卷骨盆，向上方抬起双膝靠向胸腹前侧。",
            "在最高点短暂停顿后吸气有控制地伸髋放回起始低位。",
        ],
    },
    "1660": {
        "name_zh": "跪姿俯靠瑜伽球哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "双膝跪地并在身前放置一只瑜伽球，上身微前倾将双上臂后侧及手肘稳靠垫稳在瑜伽球面，双手反握持哑铃。",
            "维持上臂稳贴球面不动，呼气顺弧线将一对哑铃向上弯举至胸肩前方。",
            "顶点停顿感受肱二头肌收缩后吸气缓慢受控下放至伸直起始位。",
        ],
    },
}

pending = {
    "2300": "待修图 · 经 F1 (+6,0)、F2 (0,+20) 对齐后 F2 架体左右支脚及踩地双脚匹配均低于 0.96（rack_base_left 0.9292、rack_base_right 0.9234、feet 0.9410），已补充低位横杠器械，待重制。",
    "1656": "待修图 · 经 F1 (+12,0)、F2 (0,+10) 对齐半圆平衡球与双脚后 F2 头顶产生 (-2,+5) 明显偏移（head_crown sc0=0.7120 < 0.96，max_res=5.39 px），已清除音译博苏球并补全半圆平衡球，待重制。",
    "2312": "待修图 · 仰卧交替肘触膝过程肩背与对侧腿腾空大幅迁移（bottom F2 sc0=-0.0263），待重制。",
    "1657": "待修图 · 双脚位于 +14 px 而头顶位于 +11 px，足部相对头部横向差值达 3 px（max_res=3.16 px），已清除英文第二式注释，待重制。",
    "2329": "待修图 · 坐姿脊柱扭转时躯干与双膝角度和中心位置显著偏转（bottom F2 sc0=-0.0240），待重制。",
    "1658": "待修图 · F0 脚尖触底 5 px 且直立与前跨弓步双脚重心位置完全迁移，已修正悬停字样以避静态触发，待重制。",
    "2333": "待修图 · F0/F1 裁底 89/47 px 且 F2 顶部出现 y=0 脚尖残影（top=41 px），已纠偏误译“吊带悬垂”为单杠直臂并补充单杠，待重制。",
    "2355": "待修图 · 经 F1 (+20,0) 对齐头部后，左侧架体底座移位 -8 px（sc0=0.5444 < 0.96），立柱宽窄不一致，已纠偏误译“吊带悬垂”并补充单杠，待重制。",
    "1660": "待修图 · F2 俯压使瑜伽球变形偏移（ball_right sc0=0.8847 < 0.96）且头部与膝脚水平方向背离，已补充瑜伽球资料，待重制。",
}

sources = {
    "1659": "https://raw.githubusercontent.com/exercemus/exercises/minified/exercises.json#dumbbell_hammer_curl_on_exercise_ball"
}

review_notes = {
    "1659": "来源为 exercemus/exercises 公开动作库 1659（dumbbell hammer curl on exercise ball）。补充瑜伽球必需支撑器械并核正肱二头肌与前臂说明，全 4 帧统一向上平移 (0, -2) 消除 F2 底部 2 px 擦边并锁定 800/380/800/380 ms 循环（F4=F2），纯白背景零边界裁切，瑜伽球底部、左右双脚与头顶四大锚点原地 0.00 px 零漂移（最低匹配分 0.9929）。"
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review44-20261022",
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
    "candidate_id": "1659",
    "candidate_required_equipment": ["瑜伽球"],
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
