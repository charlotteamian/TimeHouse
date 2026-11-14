#!/usr/bin/env python3
"""Author Batch 123 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270109_review123"
VERSION = "1.2.128"
VERSION_CODE = 2027010901

inspected = ["1723", "1724", "1725", "1726", "1727", "1728", "1744", "1745", "1747", "1748"]
review_candidates = []
registered_media = []

definition_updates = {
    "1723": {
        "name_zh": "站姿龙门架绳索单臂下压",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将单手拉环挂接于龙门架高位滑轮，侧身半步面向滑轮立稳，双脚微开踩实地面并收紧核心。",
            "工作侧单手正握或对握单手拉环、曲肘使大臂贴紧同侧肋旁固定，非工作手自然垂放体侧或轻扶肋侧稳定躯干。",
            "呼气固定肩肘位置，集中工作侧肱三头肌发力将拉环向下按压推直，感受臂后侧充分收紧。",
            "顶端稍停后吸气受控顺势曲肘回放至小臂略过水平起始位，单侧完成后换另一侧手臂重复。",
        ],
    },
    "1724": {
        "name_zh": "背站龙门架高位长绳过头臂屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将双头长绳连接至龙门架高位滑轮，背对滑轮双脚前后微开或与肩同宽踩稳、躯干微倾并收紧核心防塌腰。",
            "双手对握长绳两端举过头顶后方，使双侧大臂贴近耳侧斜前方固定、双肘先屈曲置于脑后拉伸位。",
            "呼气固定大臂角度，由肱三头肌发力向前上方伸直双肘拉开长绳。",
            "顶峰控制停顿片刻后吸气缓慢屈肘放回脑后起始拉伸位，按均匀节奏重复。",
        ],
    },
    "1725": {
        "name_zh": "上斜训练凳龙门架长绳过头臂屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "将上斜训练凳面向外侧摆在龙门架高滑轮前方，调节舒适斜角后背对滑轮仰靠坐稳在靠垫上、双脚踩实地面。",
            "双手对握由后上方高位滑轮引出的双头长绳两端，大臂抬起沿耳侧向前上方伸出并锁稳肩部。",
            "吸气控制前臂围绕肘关节向脑后充分屈肘下放，使肱三头肌得到深度预拉伸。",
            "呼气收缩肱三头肌沿原弧线向上推直长绳至肘接近伸直位（微屈不锁死），按计划重复。",
        ],
    },
    "1726": {
        "name_zh": "仰卧垫面龙门架低位长绳臂屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将双头长绳挂接至龙门架最低位滑轮，在滑轮前方铺好瑜伽垫并头朝滑轮仰卧，双膝弯曲踩实垫面以稳住腰背。",
            "双手对握长绳两端使掌心相对，将双臂垂直向上举至胸肩正上方作为起始预备位。",
            "固定大臂垂直稳定，吸气屈肘沿弧线可控将绳索两端放向头顶与前额上方附近。",
            "呼气集中肱三头肌发力伸直肘关节推回正上方起始位，按规范节奏重复。",
        ],
    },
    "1727": {
        "name_zh": "站姿龙门架反握单臂过头臂屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将单手拉环挂接于龙门架低位滑轮，背对滑轮双脚与肩同宽站稳并微收核心。",
            "工作侧单手采用掌心向上的反握握法从身后绕过头顶将手柄拉至正上方，使大臂竖直贴近耳侧固定。",
            "吸气控制单侧前臂向后下方屈肘放下至脑后深处，大臂与肩胛稳住不向前晃动。",
            "呼气由肱三头肌发力向上推直单臂还原，单侧完成后换另一侧手臂对称练习。",
        ],
    },
    "1728": {
        "name_zh": "俯身龙门架双臂臂后屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面向双侧龙门架中低位滑轮（不加挂大杆，双手直接抓握拉环或绳头末端），后退一步双脚微曲站稳。",
            "屈髋将上身前倾至接近四十五度并稳住脊柱中立，抬起双侧上臂贴近体侧后方与躯干基本平行、先屈肘约九十度。",
            "呼气固定大臂紧贴体侧，双小臂同时向正后方伸直推展直至肱三头肌充分顶峰收缩。",
            "微停顿控制后吸气缓慢屈肘回放至九十度起始位置，按计划重复。",
        ],
    },
    "1744": {
        "name_zh": "瑜伽球双臂反屈伸",
        "category": "upper arms",
        "equipment": "stability ball",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "先在瑜伽球前缘坐稳后双手分置臀部两侧球面（指尖朝向正前方或微斜外），双脚分开约与肩同宽稳踩防滑地面、膝呈约九十度。",
            "双臂发力稍微伸直推起躯干并将臀部略向前滑离球面少许，使重心稳妥落在双掌球面与双脚足底上。",
            "吸气沉肩夹紧双肘朝正后方缓慢弯曲肘关节下放躯干，避免含胸耸肩。",
            "呼气集中肱三头肌发力向下按压球面伸肘推回高位（肘微屈不锁死），按受控节奏重复。",
        ],
    },
    "1745": {
        "name_zh": "坐瑜伽球单臂哑铃三头肌负重拉伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "挺胸端坐在稳固的瑜伽球中央，双脚分开平踩地面稳住骨盆，另一侧闲置手轻扶同侧大腿帮助平衡。",
            "工作侧单手握持一只轻重量哑铃向上高举过头顶并让大臂贴近耳侧竖直稳固。",
            "吸气温和缓慢屈肘将哑铃放向脑后深处，借助轻哑铃重力充分牵拉延展肱三头肌长头。",
            "停顿感受柔和拉伸后呼气可控向上推回高举起始位，单侧完成后换另一侧手臂对称练习。",
        ],
    },
    "1747": {
        "name_zh": "瑜伽球坐姿曲杆杠铃颈后臂屈伸",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "挺胸收腹稳坐并微仰靠在瑜伽球上方，双脚稳踩防滑地面（膝约直角），双手窄距正握曲杆杠铃举起至头顶上方。",
            "沉肩收紧肘关节，使双侧大臂略向上斜方贴稳头侧不外撇晃动。",
            "吸气控制双小臂沿弧线缓慢向脑后方下放曲杆至肘充分弯曲，拉长肱三头肌。",
            "呼气集中肱三头肌收缩发力向上伸肘推回头顶上方高位，按均匀节奏重复。",
        ],
    },
    "1748": {
        "name_zh": "平凳仰卧曲杆杠铃窄握颈后臂屈伸",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧在平凳上，头背臀贴紧凳垫且双脚踩实地面，双手窄距正握曲杆杠铃伸直举于胸肩斜上方。",
            "固定肩关节与大臂角度使上臂略向头侧倾斜稳定，避免下放时双肘大幅向外张开。",
            "吸气缓慢屈肘沿弧线将曲杆控制下放至头顶后侧的颅后悬空位置。",
            "呼气由肱三头肌发力向上伸直双肘推回起始举重位，按规范节奏完成次数。",
        ],
    },
}

pending = {
    "1723": "待修图 · 纠正原中文步骤错写为“直杆附件”和“杠铃”（实图为单手拉环下压）并激活单侧计次为站姿龙门架绳索单臂下压；原动图 10 帧且上下边距 T:14, B:14<15，待重制为标准 4 帧循环图。",
    "1724": "待修图 · 规范站姿对握长绳姿态并命名为背站龙门架高位长绳过头臂屈伸；原动图 10 帧且 T:14, B:14<15，待重制为标准 4 帧循环图。",
    "1725": "待修图 · 纠正原中文步骤错写为“背对滑轮站立”并补全上斜训练凳支持器械为上斜训练凳龙门架长绳过头臂屈伸；原动图仅 2 帧且左右边距 L:14, R:14<15，待重制。",
    "1726": "待修图 · 规范为仰卧垫面龙门架低位长绳臂屈伸；原动图 10 帧且 L:14, R:12<15，待重制为标准 4 帧循环图。",
    "1727": "待修图 · 补全单臂定位以激活单侧计次并规范为站姿龙门架反握单臂过头臂屈伸；原动图 10 帧且 T:14, B:14<15，更在第 3 帧悬空区域出现断裂悬浮钢索与机械杂物伪影，待重制。",
    "1728": "待修图 · 补全原步骤遗漏的屈髋俯身动作要素为俯身龙门架双臂臂后屈伸；原动图 10 帧且 L:14, R:13<15，并在头后上方悬空处（y=67..71）存在一条横杠残影伪影，待重制。",
    "1744": "待修图 · 规范为瑜伽球双臂反屈伸；原 4 帧循环图右边距与上边距 R:12, T:12<15、足底锚点明显位移（y>=370 IoU=0.8437<0.96），且第 3 帧回到顶位而非顶峰/底端驻留（F1==F3 错序），待重制。",
    "1745": "待修图 · 纠正原数据器械误标为 stability ball 且名不副实问题（画面明确单手握哑铃过头屈肘负重拉伸），改标 dumbbell 并补瑜伽球支持器械、激活单臂单侧计次为坐瑜伽球单臂哑铃三头肌负重拉伸；原 4 帧图上下严重裁切（T:4, B:0<15）且第 3 帧球体明显位移（y>=370 IoU=0.6924<0.96），待重制。",
    "1747": "待修图 · 补全瑜伽球支持器械、去除步骤英文 EZ 为瑜伽球坐姿曲杆杠铃颈后臂屈伸；原动图 10 帧且上下边距 T:13, B:14<15（顶部杠铃接近切边），待重制。",
    "1748": "待修图 · 补全平板训练凳支持器械、去除括号与英文 ez 为平凳仰卧曲杆杠铃窄握颈后臂屈伸；原动图仅 2 帧（T:14, B:14<15）且第 2 帧人物出现严重解剖畸变（曲杆落至跨髋前方且左臂消失、完全偏离“颈后臂屈伸”动作轨迹），待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review123-20270109",
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
    "expected_per_side_ids": ["1723", "1727", "1745"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
