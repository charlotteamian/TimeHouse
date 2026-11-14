#!/usr/bin/env python3
"""Author Batch 49 review updates, pending notes, sources, code baseline, and QA spec (1730 candidate; 9 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261027_review49"
VERSION = "1.2.54"
VERSION_CODE = 2026102701

inspected = ["3161", "1684", "3162", "1700", "3165", "1729", "3166", "1730", "3167", "1731"]
review_candidates = ["1730"]
registered_media = ["1730"]

definition_updates = {
    "3161": {
        "name_zh": "踩巾单臂俯身划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": ["毛巾"],
        "instructions_zh": [
            "双脚前后微错开与肩同宽站立，前脚稳踩长毛巾底端中央，膝盖微屈并屈髋俯身保持背部挺直。",
            "同侧或对侧单手抓握毛巾另一端自然下垂，非工作手自然摆于体侧维持稳定。",
            "呼气启动肩胛后缩与上背肌群，屈肘单臂将毛巾顺着腰腹方向拉向肋部并夹紧肩胛。",
            "在顶峰位置短暂停顿，随后吸气有控制地伸臂放回下垂伸展位。",
            "完成一侧规定次数后换另一只手臂并换脚踩巾重复练习。",
        ],
    },
    "1684": {
        "name_zh": "登台单腿站立提膝哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["quadriceps", "glutes", "hamstrings"],
        "required_equipment_zh": ["稳固踏台"],
        "instructions_zh": [
            "面对稳固踏台站立，双手对握各持一只哑铃自然垂于体侧，一侧整脚稳踩踏台面。",
            "核心收紧，蹬踩踏台发力站起至单腿直立，并将对侧屈膝腿提向胸前高度。",
            "在单腿站稳高位时，呼气屈肘向上完成双臂哑铃弯举至肩前高度。",
            "随后吸气有控制地下放哑铃并同步落回地面起始站姿，完成一侧次数后换腿练习。",
        ],
    },
    "3162": {
        "name_zh": "俯身站姿单臂哑铃划船",
        "category": "back",
        "equipment": "dumbbell",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚前后微错开或与肩同宽站稳，膝盖微屈、屈髋俯身使背部呈平直稳定位，核心收紧。",
            "一手正握或对握一只哑铃垂于肩下、手臂自然伸直，另一手自然垂置辅助平衡。",
            "呼气启动上背与背阔肌发力，屈肘贴近体侧将哑铃向上拉向腰肋部，夹紧肩胛骨。",
            "在动作最高点短暂停顿后吸气缓慢放回垂臂起始位，完成规定次数后换边练习另一侧手臂。",
        ],
    },
    "1700": {
        "name_zh": "哑铃借力过顶推举",
        "category": "shoulders",
        "equipment": "dumbbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽直立站稳，双手正握或微内收各持一只哑铃托举于肩前高度。",
            "躯干保持直立，快速轻微屈膝微蹲蓄力，随即下肢蹬地发力顺势爆发性向上推举哑铃过顶至双臂伸直。",
            "在过顶锁定位置短暂停顿控制核心不塌腰，随后有控制地缓慢下放哑铃回到肩前起始位，重复规定次数。",
        ],
    },
    "3165": {
        "name_zh": "站姿毛巾后拉划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "shoulders"],
        "required_equipment_zh": ["毛巾", "稳固立柱"],
        "instructions_zh": [
            "将长毛巾绕固在前方稳固立柱上，双脚分开与肩同宽微屈膝站立，双手抓握毛巾两端在身前伸直。",
            "核心收紧、背部保持平直，身体重心微向后倾以形成预张力。",
            "呼气时上背与肩胛后缩发力，双手屈肘沿着胸腹高度将毛巾拉向胸前，肘部贴近躯干后拉。",
            "在收缩顶峰短暂停顿后吸气缓慢前伸双臂回到预拉起始位，重复规定次数。",
        ],
    },
    "1729": {
        "name_zh": "平凳仰卧过顶交替哑铃臂屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧在稳固的平板训练凳上，双脚分开平踩地面，双手对握各持一只哑铃垂直举至胸肩正上方、肘微屈。",
            "保持非工作侧大臂垂直举稳不动，工作侧保持上臂竖直固定，吸气屈肘将哑铃朝头顶旁斜后方缓慢下放。",
            "感受肱三头肌充分伸展后，呼气发力伸肘推回起始竖直高位，随后交替另一侧手臂下放重复。",
        ],
    },
    "3166": {
        "name_zh": "高位拉杆斜身反向划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "shoulders"],
        "required_equipment_zh": ["单杠"],
        "instructions_zh": [
            "双脚分开稳踩地面并走近高位横杠下方，双手正握紧抓约肩腹或胸高位置的稳固横杠，身体向后斜倾使双臂伸直。",
            "从脚跟到肩背收紧呈斜直线，核心稳定、背部平直。",
            "呼气时上背与背阔肌发力屈肘将胸口拉近横杠，两侧肩胛骨向中间充分挤压。",
            "在顶峰略作停顿后吸气缓慢伸直双臂退回斜倾伸展起始位，重复规定次数。",
        ],
    },
    "1730": {
        "name_zh": "平凳坐姿俯身交替哑铃臂屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐在稳固的平板训练凳边缘，双脚分开平踩地面，双手对握各持一只哑铃自然垂于体侧或膝旁。",
            "屈髋俯身使背部保持平直并与地面接近斜平，核心收紧、头部呈中立顺延微低。",
            "抬起一侧工作大臂贴近躯干侧面并保持稳固固定，呼气时单侧伸直前臂将哑铃向后上方踢伸至肘部接近伸直，另一侧垂放持铃稳固不变。",
            "在后伸顶峰短暂停顿挤压肱三头肌后，吸气缓慢受控屈肘回到下垂预备位，并随后交替另一侧手臂完成规定次数。",
        ],
    },
    "3167": {
        "name_zh": "毛巾自重深蹲划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "shoulders", "quadriceps"],
        "required_equipment_zh": ["毛巾"],
        "instructions_zh": [
            "双脚分开与肩同宽直立站稳，双手正握短毛巾两端将其水平拉紧前平举于胸前。",
            "吸气屈膝推髋向后下方蹲低至大腿接近平行地面，双臂保持前伸绷紧毛巾。",
            "在深蹲同时或底位启动上背收缩将毛巾屈肘拉向胸口并夹紧肩胛骨。",
            "短暂停顿后蹬地起身返回直立，并同步前伸双臂复原预备姿势，重复规定次数。",
        ],
    },
    "1731": {
        "name_zh": "平凳坐姿窄握哑铃过顶推举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐在稳固的平板训练凳上，双脚平踩地面、躯干直立并收紧核心。",
            "双手窄距掌心朝前或微对握各持一只哑铃托于胸肩前上方高度、肘部贴近体前内收。",
            "呼气时肱三头肌与肩前束协同发力将哑铃垂直向上推举过顶至双臂接近伸直，避免过度塌腰后仰。",
            "在顶峰短暂控制后吸气缓慢沿垂直轨迹下放哑铃回到胸肩前侧起始位，重复规定次数。",
        ],
    },
}

pending = {
    "3161": "待修图 · 已去括号规范为踩巾单臂俯身划船（核正上背主训、毛巾支撑与单侧计次）；原图 F1 头部(-2,0)与前脚(-1,0)微偏且前脚 sc0=0.8583、毛巾底端右移 8 px(sc0=0.4485)，F2 躯干前倾随毛巾变形位移，待重制。",
    "1684": "待修图 · 已去括号规范为登台单腿站立提膝哑铃弯举（核正肱二头肌主训、稳固踏台与单侧计次）；原图 F0/F1/F3 触底 y=479、F2 触顶 y=0 裁边，且上下踏台重心高度变化无法固定锚点，待重制。",
    "3162": "待修图 · 纠正上游误标 body weight 及自重名，实为俯身站姿单臂哑铃划船（已改 dumbbell、上背主训与单侧计次）；原图 F1 头部(+27,+1)/后脚(+22,0)与前脚(+8,-2, ncc=0.2054)严重差速漂移，F2 双脚横纵偏移 4–7 px，待重制。",
    "1700": "待修图 · 已更名为哑铃借力过顶推举（核正三角肌主训）；原图 F0 触底 y=479、F2 哑铃触顶 y=0 截断，且下蹲蓄力与过顶伸展全程头脚偏移(F1 head sc0=0.1459)，待重制。",
    "3165": "待修图 · 已去括号并定名为站姿毛巾后拉划船（核正上背主训与毛巾/稳固立柱）；原图 F1/F2 头部偏移(-4,+1)/(-7,+3)而双脚大幅后移(-11..-14, 0)达 7 px 差异，待重制。",
    "1729": "待修图 · 已规范为平凳仰卧过顶交替哑铃臂屈伸（核正肱三头肌主训与平板训练凳）；经 F2(0,+25)对齐平凳与双脚后，面鼻下颌(face_nose_chin)在 F1 仍偏(+3,-1) px(res=3.16, sc0=0.7599)、在 F2 偏(+2,-1) px(res=2.24, sc0=0.7875)，且垂直持铃臂存在(-8,-3) px 独立漂移，待重制。",
    "3166": "待修图 · 已定名为高位拉杆斜身反向划船（核正上背主训与单杠必需器械）；原图 F1/F2 后脚以脚尖为轴明显滑动(foot_far sc0=0.8455/0.7885)，且铁架顶端较底座错开(-1,-1)，待重制。",
    "3167": "待修图 · 已去括号并规范为毛巾自重深蹲划船（核正上背主训、毛巾与股四头肌协同）；原图深蹲全程头部大幅下沉 65–81 px(head sc0=-0.0544/0.0303)且双脚位移 3–10 px，待重制。",
    "1731": "待修图 · 纠正图配矛盾为平凳坐姿窄握哑铃过顶推举（核正肱三头肌主训与平板训练凳）；原图 F0 触底 y=479、F2 触顶 y=0 截断，且 F1/F2 平凳与双脚相对 F0 偏移 2–9 px(bench_left_leg sc0=0.8628/0.8488)，待重制。",
}

sources = {
    "1730": "https://raw.githubusercontent.com/exercemus/exercises/minified/exercises.json#dumbbell_seated_bent_over_alternate_kickback",
}

review_notes = {
    "1730": "来源为 exercemus/exercises 公开动作库 1730（dumbbell seated bent over alternate kickback）。核正平凳坐姿俯身交替哑铃臂屈伸（补全平板训练凳必需器械、核正肱三头肌主训并清除上游误标肩部主训及未汉化 back 字段），原地 (0,0) 锁定 800/380/800/380 ms 四帧循环（F4=F2），纯白背景零边界截断，头部、平凳左/右支腿、近/远脚与垂放非工作臂六大锚点零漂移（max_anchor_residual_px = 0.00 px，min_anchor_match_score = 0.9961）。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review49-20261027",
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
    "candidate_ids": ["1730"],
    "candidate_required_equipment": {
        "1730": ["平板训练凳"],
    },
    "expected_per_side_ids": ["3161", "1684", "3162"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
