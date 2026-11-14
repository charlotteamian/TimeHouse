#!/usr/bin/env python3
"""Author Batch 132 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270118_review132"
VERSION = "1.2.137"
VERSION_CODE = 2027011801

inspected = ["3305", "3312", "3313", "3562", "3563", "3641", "3642", "3643", "3644", "3666"]
review_candidates = []
registered_media = []

definition_updates = {
    "3305": {
        "name_zh": "站姿杠铃深蹲推举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "glutes", "hamstrings", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开约与肩同宽站立，正手略宽于肩握住杠铃并稳托于前三角肌与锁骨上方前架位，肘部略微朝前。",
            "挺胸收腹建立核心张力，吸气屈髋屈膝顺势下蹲至大腿约与地面平行。",
            "蹲至底端即刻呼气，凭借下肢脚后跟主动发力爆发性蹬地站起，并将下肢上升势能顺畅传导至双臂将杠铃垂直向上推举过头顶至双臂伸直。",
            "在顶峰略作稳定后控制屈肘沿垂直路径落回前肩架位，随即顺势衔接下一次下蹲推举，重复规定次数。",
        ],
    },
    "3312": {
        "name_zh": "高单杠负重标准双力臂",
        "category": "back",
        "equipment": "weighted",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "triceps", "shoulders", "forearms"],
        "required_equipment_zh": ["单杠"],
        "instructions_zh": [
            "系妥负重腰带并悬挂适量配重片，以略宽于肩的正握姿势（拇指扣紧并微前绕腕）抓牢高单杠，双臂伸直挂于杠下。",
            "收紧核心与下沉肩胛骨，随后呼气屈肘发力将胸口爆发性向上拉向单杠。",
            "当胸部接近或越过单杠高度时顺势前扣手腕、将双肘翻折至横杠上方完成过渡。",
            "随即将双臂推直将身体撑稳于杠上高点，再有控制地屈肘落回并展开双臂缓慢降回挂杠起始位，重复规定次数。",
        ],
    },
    "3313": {
        "name_zh": "双杠负重前倾偏胸臂屈伸",
        "category": "chest",
        "equipment": "weighted",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": ["双杠"],
        "instructions_zh": [
            "系妥负重腰带并挂好配重片，走入双杠架内双手抓稳双侧横杠并将双臂推直撑高起身（肘微屈不锁死），双膝微屈交叉后收、躯干略微前倾约二十度使重心偏向胸肌下部。",
            "沉肩微收核心，吸气时有控制地缓慢屈肘、双肘适度外展微斜，逐步降低身体直至上臂接近与地面平行、胸大肌外下缘感受明显拉伸。",
            "在底部略作停顿稳定张力，随后呼气集中胸肌与肱三头肌发力向上推直双臂回到起始高点，重复规定次数。",
        ],
    },
    "3562": {
        "name_zh": "平凳上背仰靠双腿杠铃臀桥",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "core"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐于平凳一侧前方地面，将肩胛骨下缘贴稳在横放的平凳边缘作为支点，双脚分开约与肩或髋同宽平踩地面、双膝屈曲约九十度。",
            "在髋部折痕处垫好护垫并平稳放置杠铃，双手正握杠身牢牢固定防滑。",
            "吸气微降髋至低位预备，随后呼气集中臀大肌发力并以双侧脚后跟主动蹬地，向上顶起骨盆直至大腿与躯干呈平直一条线（勿过度反弓腰椎）。",
            "在顶峰收缩位略作停顿并用力夹紧臀部，再缓慢控制下放回落，重复规定次数。",
        ],
    },
    "3563": {
        "name_zh": "站姿龙门架绳索单臂下拉",
        "category": "back",
        "equipment": "cable",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将单个握把连接至龙门架高位滑轮，面向滑轮站立且双脚分开与肩同宽，躯干微后仰或稳固核心直立。",
            "单手正握或对握抓牢手柄，手臂向前上方完全伸直拉紧配重，非工作手自然叉腰或轻扶体侧稳定平衡。",
            "呼气先下沉单侧肩胛，随后集中单侧背阔肌发力屈肘将手臂贴近体侧向下下拉至腰肋旁。",
            "在底端略作停顿并充分挤压目标侧背肌，再吸气控制缓慢还原回顶部拉伸位，单侧完成次数后换另一臂重复。",
        ],
    },
    "3641": {
        "name_zh": "跪姿双臂负重直臂上摆",
        "category": "shoulders",
        "equipment": "weighted",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双膝分开与髋同宽稳跪于软垫上，挺直脊柱与腰背、收紧臀部及腹部核心。",
            "双手各握持一只负重，双臂自然垂放在体侧偏前位置、肘微屈固定。",
            "呼气集中三角肌发力并顺势维持手臂近乎伸直，将双侧负重经体前圆弧顺畅向前上方摆举高过头顶。",
            "在最高点略作停顿控制而不反弓下背，随后吸气控制缓慢回放至起始位置，重复规定次数。",
        ],
    },
    "3642": {
        "name_zh": "负重弓步伸展",
        "category": "upper legs",
        "equipment": "weighted",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双手各持一只负重自然垂放体侧，双脚与肩同宽挺胸直立。",
            "先以一侧脚向前跨出较大步距踩稳地面，维持脊柱直立与核心收紧。",
            "吸气缓慢屈曲前侧髋膝下沉重心，直至前大腿接近与地面平行、后膝接近地面但不触地磕碰，充分感受后侧髋屈肌与臀腿拉伸发力。",
            "前脚掌与脚跟发力蹬地推回起始站姿，随后换另一侧腿迈步重复，双腿交替完成规定次数。",
        ],
    },
    "3643": {
        "name_zh": "高脚杯式负重哥萨克侧蹲",
        "category": "upper legs",
        "equipment": "weighted",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双手于胸前高脚杯式捧握负重，双脚大跨步宽距站立（远宽于肩），双侧脚尖略微朝外。",
            "挺胸收腹，吸气将身体重心顺势向一侧臀腿平移并屈膝深蹲，另一侧非承重腿全程伸直、脚掌或脚跟贴地延展。",
            "控制蹲至可维持躯干挺胸平衡的舒适最低深度，感受承重侧臀腿发力与伸直侧内收肌群拉伸。",
            "呼气以承重侧脚后跟主动蹬地推回中立直立位，随即向对侧移重下蹲，左右交替完成规定次数。",
        ],
    },
    "3644": {
        "name_zh": "负重箭步蹲前摆",
        "category": "upper legs",
        "equipment": "weighted",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开约与肩同宽站立，双手各持一只负重垂于大腿两侧、核心收紧。",
            "一侧脚向前迈出踩稳并顺势屈膝下沉成标准箭步蹲，同时随下蹲顺畅将双手握持的负重直臂向前上方平摆举至约与肩或胸眼齐平高度。",
            "控制前腿大腿约与地面平行后，呼气以前脚跟蹬地发力站回起始并拢站姿，双臂随之自然回摆下放至体侧。",
            "紧接换另一侧腿迈出重复，左右交替按受控节奏完成规定次数。",
        ],
    },
    "3666": {
        "name_zh": "斜坡跑步机步行",
        "category": "cardio",
        "equipment": "leverage machine",
        "target": "cardiovascular system",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": ["跑步机"],
        "instructions_zh": [
            "走上跑步机踩稳两侧边条后踩入跑带，预先调好安全磁扣，设定目标爬坡角度及平缓安全的步行起始配速。",
            "躯干自然微前倾直立、核心收紧、双眼平视前方、双臂随步幅自然摆动（双手尽量不长期死压扶手借力）。",
            "以前脚掌滚动至全脚掌落步，由臀腿与小腿协同推动持续平稳步行完成计划时长。",
            "训练接近结束时先逐步降低坡度与配速缓行放松过渡，待跑带完全停稳后再下机。",
        ],
    },
}

pending = {
    "3305": "待修图 · 改名明确前架杠铃深蹲推举定位（避开与普通肩推混淆，站姿杠铃深蹲推举）；原动图仅 2 帧且上下边距 T:14, B:14<15，待重制为标准 4 帧循环图。",
    "3312": "待修图 · 纠正“负重肌上（杠上）”机器直译及去除括号/“保持/悬挂”，补充 required_equipment_zh=[\"单杠\"]；原动图仅 2 帧且 T:14, B:14<15，待重制。",
    "3313": "待修图 · 纠正“负重直杠下压”错译为双杠负重前倾偏胸臂屈伸、按实图与原步骤补充 required_equipment_zh=[\"双杠\"]；原动图仅 2 帧且 T:13, B:14<15，待重制。",
    "3562": "待修图 · 纠正“双腿放凳”与去括号“（男）”、对齐 3523 命名为平凳上背仰靠双腿杠铃臀桥并补充 required_equipment_zh=[\"平板训练凳\"]；原动图 10 帧且 L:14, R:14<15，待重制。",
    "3563": "待修图 · 标注“单臂”确保启用 perSide、消除“电缆机/保持”；原 10 帧动图 L:14, R:14<15、龙门架横移致 y>=370 IoU=0.7606<0.96 且第 4 帧左肩下颌旁有淡黑残影，待重制。",
    "3641": "待修图 · 纠正“跪姿摆动步”误译与实景无跨步问题、消除“保持”并注明手中实绘一对哑铃；原仅 2 帧（T:12, B:14<15）且顶缘上方残留一双倒置裁断裸足伪影，待重制。",
    "3642": "待修图 · 消除“保持”并优化弓步步骤；原 10 帧动图 T:12, B:14<15、y>=370 IoU=0.6551<0.96，且第 3 帧前右腿膝部股四头肌处被大块白色缺口裁穿畸变，待重制。",
    "3643": "待修图 · 去“（男）”与“保持/重物”并规范高脚杯式负重哥萨克侧蹲；原动图仅 2 帧且上下边距 T:13, B:14<15，待重制为标准 4 帧循环图。",
    "3644": "待修图 · 消除“保持/重物/向前冲”并规范负重箭步蹲前摆；原动图仅 2 帧且上下边距 T:14, B:12<15，待重制为标准 4 帧循环图。",
    "3666": "待修图 · 补充 required_equipment_zh=[\"跑步机\"]、清除“保持”与“使其冷却”直译（斜坡跑步机步行）；原动图仅 2 帧且 L:14, R:14<15，待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review132-20270118",
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
    "expected_checks": 16,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_ids": [],
    "candidate_required_equipment": {},
    "expected_per_side_ids": ["3563"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
