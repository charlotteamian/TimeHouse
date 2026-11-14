#!/usr/bin/env python3
"""Author Batch 124 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270110_review124"
VERSION = "1.2.129"
VERSION_CODE = 2027011001

inspected = ["1749", "1750", "1751", "1752", "1754", "1755", "1756", "1758", "1767", "2135"]
review_candidates = []
registered_media = []

definition_updates = {
    "1749": {
        "name_zh": "站姿曲杆杠铃颈后臂屈伸",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站稳并收紧核心避免塌腰，双手窄距正握曲杆杠铃举起至头顶上方作为起始位。",
            "沉肩锁紧肩关节使双侧大臂贴近耳侧竖直固定，双肘朝前微收不大幅外撇。",
            "吸气控制双小臂沿弧线缓慢向脑后方弯曲下放曲杆至肘关节充分折叠。",
            "呼气集中肱三头肌收缩发力向上伸直肘部推举还原，按规范节奏重复。",
        ],
    },
    "1750": {
        "name_zh": "平凳仰卧药球胸前上抛",
        "category": "upper arms",
        "equipment": "medicine ball",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧在平凳上，头背臀稳贴凳面、双膝微屈双脚踩实地面，双手抓稳实心药球两侧托举在胸口上方。",
            "双肘夹向体侧斜下方约四十五度，吸气控制药球沉至贴近中胸前上方完成蓄力。",
            "呼气爆发性收缩肱三头肌与胸肩发力将药球垂直向上推抛脱手离胸。",
            "视线紧盯药球在正上方双手平稳缓冲接住并顺势屈肘卸力回落胸前，按安全节奏重复。",
        ],
    },
    "1751": {
        "name_zh": "站姿深蹲架安全销杠铃推举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "在深蹲力量架内将双侧安全保护销调至与上胸/锁骨同高的位置，横放杠铃并略宽于肩正握横杆站于杠铃下方。",
            "双脚与肩同宽踩稳地面，收紧腹部与臀部使脊柱中立直立、前臂几乎垂直地面。",
            "呼气集中肱三头肌与肩胸协同发力将杠铃从安全销上垂直向上推举过头顶至双臂接近伸直。",
            "顶峰略作控制后吸气匀速顺控垂直下放，轻放稳回安全销停顿消除反弹借力，按计划重复。",
        ],
    },
    "1752": {
        "name_zh": "史密斯机上斜训练凳仰卧臂屈伸",
        "category": "upper arms",
        "equipment": "smith machine",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "将上斜训练凳摆放在史密斯机正中央调好斜靠角度，斜躺稳坐于斜垫上且双脚踩实地面。",
            "双手略窄于肩或与肩同宽正握上方横杆旋转解锁，将横杆伸臂推稳于上胸至额前上方起始位。",
            "稳固上臂略微向后仰斜不动，吸气沿斜导轨缓慢屈肘控制横杆落向额头斜上方。",
            "呼气集中肱三头肌伸直肘部向上推回起始高度，训练结束后旋锁挂钩复位。",
        ],
    },
    "1754": {
        "name_zh": "平凳负重置片双臂反屈伸",
        "category": "upper arms",
        "equipment": "weighted",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "横向坐在平凳长边边缘，先将杠铃片平放稳于大腿前侧，双脚向前伸直以脚跟着地。",
            "双手在臀部两侧反手按紧凳面前沿（指尖朝前方），微移臀部前滑离开凳缘由双臂承托。",
            "吸气沉肩使肘尖朝正后方缓慢屈肘下沉臀背，控制下背顺直贴近凳缘上下移动。",
            "呼气集中肱三头肌向下按压凳面伸直手臂推回高位，按均匀节奏完成次数。",
        ],
    },
    "1755": {
        "name_zh": "平凳负重宽腿坐缘反屈伸",
        "category": "upper arms",
        "equipment": "weighted",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐在平凳长边边缘并在大腿上方稳妥叠放杠铃片，双腿略向前开立伸展以足跟着地增加稳定性。",
            "双手置于体侧臀旁扣住凳面边缘（手肘微向后夹不外翻），臀部前移悬空贴近凳缘。",
            "吸气沿垂直方向缓慢屈肘下放躯干直至上臂接近与地面平行。",
            "呼气集中肱三头肌发力伸直双肘推起躯干还原高位，按受控节奏重复。",
        ],
    },
    "1756": {
        "name_zh": "杠铃单腿硬拉",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立，双手略宽于大腿外侧正握杠铃自然垂放于体前，挺胸收腹收紧背部。",
            "将重心稳落于支撑侧单脚（工作侧腿微屈膝锁稳），另一侧腿稍微向后点离地面准备单腿铰链。",
            "吸气顺髋关节折屈前倾上身，同时悬空侧腿向正后方直腿抬升以与躯干成平衡直线，杠铃贴近支撑腿前侧平稳垂直下移。",
            "感受支撑侧臀大肌与腘绳肌充分拉长后，呼气由臀腿协同发力伸髋挺直上身拉起杠铃并收回悬空脚还原，完成单侧后换腿交替。",
        ],
    },
    "1758": {
        "name_zh": "稳固踏台辅助仰卧起坐",
        "category": "waist",
        "equipment": "assisted",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": ["稳固踏台"],
        "instructions_zh": [
            "面向稳固踏台铺好瑜伽垫仰卧于地面，双膝屈曲将双脚脚背或足跟稳妥勾抵在踏台下横梁内侧以借力锚定。",
            "双手轻扶耳侧或颈后（不抱头硬拽颈椎），双肘自然向两侧打开。",
            "呼气由上腹部收缩主导依次卷抬肩背向上坐起至躯干与地面约成四十五度高点。",
            "顶端停顿收腹控制片刻后，吸气按脊柱节段缓缓落回地面，按均匀节奏重复。",
        ],
    },
    "1767": {
        "name_zh": "高双杠负重臂屈伸",
        "category": "upper arms",
        "equipment": "weighted",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["双杠"],
        "instructions_zh": [
            "腰间系稳负重腰带并挂好杠铃片，走入高双杠之间双手握紧双侧平行杠面向上挺直双臂、双膝略后屈叠放。",
            "沉肩紧收躯干避免左右晃动，肘部适度夹近体侧斜后方以突出肱三头肌主导发力。",
            "吸气有控制地弯曲双肘下沉身体至上臂大约与地面平行位置。",
            "呼气集中肱三头肌向上推压双杠直至肘接近伸直还原高位，按受控节奏重复。",
        ],
    },
    "2135": {
        "name_zh": "负重平板支撑",
        "category": "waist",
        "equipment": "weighted",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "先俯卧于防滑瑜伽垫上，请同伴将适中重量杠铃片稳妥平放于中上背肩胛之间下方位置（或先佩戴负重背心）。",
            "双前臂平行俯撑垫面使双肘正位于肩关节正下方，双腿向后伸直并拢以双脚前脚掌撑稳地面。",
            "收紧腹核心与臀部将躯干与骨盆抬离地面，保持头肩髋踝呈一条稳固直线、不塌腰也不顶臀。",
            "均匀深呼吸持续维持规定计时秒数后有控制地轻放膝盖回垫撤片休息。",
        ],
    },
}

pending = {
    "1749": "待修图 · 去除命名“曲杆法式”简称并规范为站姿曲杆杠铃颈后臂屈伸；原动图 10 帧且上下边距 T:8, B:13<15，更在第 1~3 帧出现双手空握、直到第 4 帧才凭空出现杠铃并顶边裁切的严重失真，待重制。",
    "1750": "待修图 · 补全平板训练凳支持器械并修正步骤将药球混写为“健身球”问题（规范为平凳仰卧药球胸前上抛）；原动图 10 帧且 L:12, R:14<15，更在每帧长凳底缘正下方多出半颗散落截断的药球黑影伪影，待重制。",
    "1751": "待修图 · 修正原中文步骤错写“胸部正上方”并与原图深蹲架内站姿安全销推举实景对齐，规范为站姿深蹲架安全销杠铃推举；原动图 10 帧且上下边距 T:12, B:12<15（第 4 帧双手及杠铃顶出上边缘），待重制。",
    "1752": "待修图 · 补全上斜训练凳支持器械并统一步骤斜凳仰卧描述（规范为史密斯机上斜训练凳仰卧臂屈伸）；原动图仅 2 帧（T:14, B:14<15）且第 1 帧底部左侧存在两条杂乱残影点，待重制。",
    "1754": "待修图 · 纠正原中文名称严重误译“三凳俯卧撑”（实为大腿置负重片的平凳反臂屈伸）并补全平板训练凳支持器械；原动图 10 帧（L:13, R:14<15）且第 3 帧头顶上方存在淡淡悬浮圆形光环伪影，待重制。",
    "1755": "待修图 · 纠正原中文名称严重误译“三头肌下压”（实为坐缘负重反臂屈伸）并补全平板训练凳支持器械；原动图仅 2 帧且左右边距 L:14, R:14<15，待重制。",
    "1756": "待修图 · 清除原步骤中的“保持”触发词并规范为杠铃单腿硬拉（激活单侧计次）；原动图仅 2 帧且左右边距 L:14, R:14<15，待重制为标准 4 帧循环图。",
    "1758": "待修图 · 补全稳固踏台勾脚锚点支持器械并规范为稳固踏台辅助仰卧起坐；原动图 10 帧（L:14, R:14<15）且第 3 帧腹部与胸口上方悬空生长出截断手臂与上躯残影叠影伪影，待重制。",
    "1767": "待修图 · 纠正原中文名称严重误译“三头肌下压（高双杠）”并去括号、补全双杠支持器械为高双杠负重臂屈伸；原动图仅 2 帧且 T:14, B:14<15，待重制为标准 4 帧循环图。",
    "2135": "待修图 · 核准负重平板支撑静态计时定义并调整安放负重片安全步骤；原动图仅 2 帧（L:14, R:14<15）且左下脚踝正下方悬空存在一块黑色条形杂物伪影，待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review124-20270110",
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
    "expected_per_side_ids": ["1756"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
