#!/usr/bin/env python3
"""Author Batch 47 review updates, pending notes, sources, code baseline, and QA spec."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261025_review47"
VERSION = "1.2.52"
VERSION_CODE = 2026102501

inspected = ["2963", "1671", "3011", "1672", "3012", "1673", "3019", "1674", "3119", "1675"]
review_candidates = ["1671", "1673"]
registered_media = ["1671", "1673"]

definition_updates = {
    "2963": {
        "name_zh": "罗马椅垫肘直腿举",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": ["罗马椅"],
        "instructions_zh": [
            "背靠罗马椅背垫，双前臂稳放在两侧护垫上并握紧扶手，上背挺直贴垫使下肢自然下垂。",
            "收紧腹直肌与核心，呼气保持双腿伸直向前上方缓缓抬起至与地面平行或略高。",
            "在最高点短暂停顿感受下腹收缩后吸气缓慢受控下放回垂直起始位。",
        ],
    },
    "1671": {
        "name_zh": "站姿单臂锤式哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽直立站稳，双手掌心相对各握一只哑铃垂放体侧。",
            "非工作侧手臂保持自然垂放不动，工作侧保持大臂稳贴躯干，呼气沿锤式轨迹单臂向上弯举哑铃靠向胸肩前方。",
            "在顶峰略作停顿感受肱二头肌与肱肌充分收缩后，吸气沿原轨迹缓慢受控放回体侧，完成规定次数后换臂。",
        ],
    },
    "3011": {
        "name_zh": "上斜训练凳直臂肩胛俯卧撑",
        "category": "chest",
        "equipment": "body weight",
        "target": "serratus anterior",
        "muscle_group": "serratus anterior",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "双手略宽于肩压稳在上斜训练凳边缘，双腿向后伸直并脚尖着地使身体呈斜直线。",
            "保持肘关节伸直或微屈锁定，吸气缓慢让胸口下沉令两侧肩胛骨向脊柱内侧靠拢挤压。",
            "随后呼气启动前锯肌发力推开凳面使肩胛骨向前外展饱满鼓起还原。",
        ],
    },
    "1672": {
        "name_zh": "牧师凳单臂佐特曼哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "稳坐在牧师凳上，双脚平踩地面，将工作侧上臂后侧稳定贴放在斜垫上，掌心朝上反握一只哑铃充分伸直。",
            "呼气将哑铃向上弯举至肩前收缩位，在顶点旋前手腕转为掌心朝前下方的正握握姿。",
            "吸气沿正握角度缓慢有控制地放回伸直位后转回反握，完成目标次数后换臂。",
        ],
    },
    "3012": {
        "name_zh": "站姿微蹲屈肘肩胛后缩",
        "category": "back",
        "equipment": "body weight",
        "target": "traps",
        "muscle_group": "traps",
        "secondary_muscles": ["rhomboids", "deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，先将双臂向前平举伸直预备。",
            "膝关节微屈顺势后坐半蹲并收紧背部，同时双臂屈肘向后拉动令两侧肩胛骨强烈挤压靠拢。",
            "在肩胛后缩顶点短暂停顿后顺势伸肘返回前平举预备位。",
        ],
    },
    "1673": {
        "name_zh": "瑜伽球抵臂单臂哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "分腿跨坐或跪蹲于瑜伽球后方双脚稳踩地面，非工作手轻扶垫压瑜伽球顶部稳定球身与躯干。",
            "工作侧手掌心朝前或微外旋单手持哑铃，将上臂后侧斜抵贴稳在瑜伽球前侧斜面上自然下垂伸直。",
            "保持上臂稳贴瑜伽球面不动，呼气发力向上弯举哑铃靠近胸肩前方。",
            "顶点停顿感受肱二头肌充分收紧后吸气缓慢受控下放归位，完成次数后换臂。",
        ],
    },
    "3019": {
        "name_zh": "高位斜拉杠自重俯仰引体划船",
        "category": "back",
        "equipment": "body weight",
        "target": "lats",
        "muscle_group": "lats",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": ["单杠"],
        "instructions_zh": [
            "在胸肩高度的单杠或斜拉横杠下方双脚蹬稳地面，身体向后斜直垂挂，双手略宽于肩正握紧抓横杠。",
            "收紧核心使肩髋脚踝保持一条直线，呼气收缩背阔肌并屈肘将上胸主动拉向横杠。",
            "顶点停顿后吸气缓慢伸臂下放回到斜垂起始位。",
        ],
    },
    "1674": {
        "name_zh": "上斜训练凳俯卧双臂锤式哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "调整上斜训练凳至约四十五度，胸腹贴靠垫面俯卧其上，双脚在后方分开蹬地稳定身体。",
            "双手掌心相对锤握一对哑铃自然垂直向下垂放，保持大臂垂直地面。",
            "维持大臂稳定不动，呼气同时向上弯举哑铃至肩侧高位，顶点停顿后吸气缓慢受控下放。",
        ],
    },
    "3119": {
        "name_zh": "自重前平举窄距深蹲",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["quadriceps", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽直立，双臂向前水平伸直抬起维持平衡，核心与腹部提前收紧。",
            "吸气向后推臀并屈膝下蹲至大腿接近水平，全程保持背部挺直与双臂前伸。",
            "在底部短暂停顿后呼气发力双脚蹬地起身回到站立位。",
        ],
    },
    "1675": {
        "name_zh": "上斜训练凳俯靠双臂哑铃蜘蛛弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "面对调整至约四十五度的上斜训练凳靠背俯身趴靠，双脚向后分踩地面稳定下盘，上胸稳贴斜垫上沿。",
            "双手反握一对哑铃使双臂完全垂直下垂伸直于靠背前方。",
            "保持上臂稳固不动，呼气收缩肱二头肌向上弯举哑铃至接近肩前，顶点停顿后缓慢放回。",
        ],
    },
}

pending = {
    "2963": "待修图 · 实测罗马椅底脚弯曲（chair_left_base F2 sc0=0.7849）同时头部产生 +2 px 横移（sc0=0.9128），已补充罗马椅，待重制。",
    "3011": "待修图 · 上斜肩胛俯卧撑过程中斜凳及躯干垂直位移 -24 px 且头肩旋转角度不同步（head sc0=0.0293），已补充上斜训练凳，待重制。",
    "1672": "待修图 · 彻底纠正上游严重错译“仰卧弯举”为牧师凳单臂佐特曼哑铃弯举并补全牧师凳，实测 F1 (+20,0)、F2 (0,+1) 后头顶仍下探 -1 px（head_crown sc0=0.9262 < 0.96；dy2=2 时长凳跌至 0.8784），待重制。",
    "3012": "待修图 · 站姿起手与微蹲后缩肘期间膝腿弯曲且躯干后移 -28 px，待重制。",
    "3019": "待修图 · 彻底纠正上游错译“卧推引体向上”为高位斜拉杠自重俯仰引体划船并补全单杠，实测身体与横杠多支点迁移（bottom F2 sc0=0.5014），待重制。",
    "1674": "待修图 · 经 F2 (0,+3) 对齐斜凳支脚与脚尖（0.996+）后，F2 头部仍独立抬离 (-1,-3) px（head sc0=0.8000 < 0.96），已补充上斜训练凳，待重制。",
    "3119": "待修图 · 彻底清除原名粗俗直译“厕所蹲”为自重前平举窄距深蹲，动作过程双膝外展与身高垂直下蹲重定位（bottom sc0=0.2921/0.4811），待重制。",
    "1675": "待修图 · 修正原步骤遗漏“上斜训练凳俯卧趴靠”要领的重大疏漏并补充上斜训练凳，实测 F2 头部抬离 -3 px（head (+3,-3) sc0=0.6525 < 0.96），待重制。",
}

sources = {
    "1671": "https://raw.githubusercontent.com/exercemus/exercises/minified/exercises.json#dumbbell_one_arm_standing_hammer_curl",
    "1673": "https://raw.githubusercontent.com/exercemus/exercises/minified/exercises.json#dumbbell_preacher_curl_over_exercise_ball",
}

review_notes = {
    "1671": "来源为 exercemus/exercises 公开动作库 1671（dumbbell one arm standing hammer curl）。核正图示双持垂臂、单侧弯举步骤及单臂分段计次，经 F1/F3 (+20, 0) 纯整数水平平移配准并锁定 800/380/800/380 ms 四帧循环（F4=F2），纯白背景零边界截断，左右双脚、左大腿、垂放非工作臂与头顶五大锚点残差均 ≤ 1.00 px（最低匹配分 0.9741）。",
    "1673": "来源为 exercemus/exercises 公开动作库 1673（dumbbell preacher curl over exercise ball）。彻底纠正上游严重错译“哑铃仰卧弯举（球上）”为瑜伽球抵臂单臂哑铃弯举并补全瑜伽球必需支撑器械及单臂计次，原地锁定 800/380/800/380 ms 四帧循环（F4=F2），纯白背景零边界截断，瑜伽球右下底座、左右双脚与头顶四大无遮挡锚点实现 0.00 px 零漂移（最低匹配分 0.9667）。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review47-20261025",
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
    "expected_checks": 13,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_ids": ["1671", "1673"],
    "candidate_required_equipment": {
        "1671": [],
        "1673": ["瑜伽球"],
    },
    "expected_per_side_ids": ["1671", "1672", "1673"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
