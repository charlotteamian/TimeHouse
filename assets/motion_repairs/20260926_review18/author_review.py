#!/usr/bin/env python3
"""Author Batch 18 (20260926_review18) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0631", "0362", "0634", "0363", "0635", "0364", "0638", "0365", "0639", "0366"]
    review_candidates = ["0362", "0635", "0364", "0638", "0365", "0366"]

    definition_updates = {
        "0631": {
            "name_zh": "严格双力臂",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["upper back", "pectorals", "triceps", "biceps", "delts", "core"],
            "movement_patterns_zh": ["垂直拉", "高位支撑"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "正握（略宽于肩）悬垂于高位单杠下方，双臂伸直且肩带下沉收紧核心与双腿。",
                "呼气由背阔肌与上背发力爆发性垂直向上拉起身体，使胸部迅速越过横杠高度。",
                "到达横杠高度时快速翻转手腕切入杠上撑姿，双肘顺势顶在横杠上方。",
                "紧接由肱三头肌与胸肌发力推直双臂完成杠上锁定，再控制屈肘落回直臂悬垂位；每次拉起、推撑与下放计一次。",
            ],
        },
        "0362": {
            "name_zh": "平凳坐姿哑铃单臂颈后臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在稳固的平板训练凳上，挺胸收腹保持腰背直立，双脚分开踩实地面，非训练手扶住同侧大腿维持稳定。",
                "训练手持哑铃向上举起使上臂垂直紧贴头侧上方，肘关节伸直作为顶端起始位。",
                "保持上臂垂直固定不前后晃动，吸气缓慢屈肘将哑铃有控制地降向同侧脑后下方至肱三头肌充分拉伸。",
                "呼气收缩肱三头肌伸直肘关节将哑铃推回垂直顶位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0634": {
            "name_zh": "慢速离心卷腹",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "hip flexors"],
            "movement_patterns_zh": ["核心稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双膝弯曲约90度且双脚踩实地面，双手轻扶耳侧且手肘朝外。",
                "呼气由腹直肌发力将上背部卷离垫面至肩胛抬起约45度位置。",
                "吸气用3至4秒极慢速控制离心下降，使脊柱逐节缓缓贴回地面全程保持腹部持续张力。",
                "肩胛轻触垫面后即刻衔接下一次卷起；每次卷起与慢放离心计一次。",
            ],
        },
        "0363": {
            "name_zh": "哑铃单臂直立划船",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "biceps", "forearms"],
            "movement_patterns_zh": ["垂直拉", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立，挺胸收腹保持脊柱中立，训练手正握持哑铃自然垂于大腿前侧，非训练手放于体侧。",
                "保持核心稳定不向侧方倾倒，呼气由三角肌与斜方肌上束发力由肘部主导向上垂直提拉哑铃。",
                "拉至肘关节高于肩部水平、哑铃停在锁骨前方位置时短暂停顿，避免过度耸肩。",
                "吸气有控制地沿身体前侧缓慢下放回大腿前方；单侧完成规定次数后换另一侧。",
            ],
        },
        "0635": {
            "name_zh": "仰卧屈膝斜腹卷腹",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques"],
            "movement_patterns_zh": ["核心旋转", "核心稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在地面或训练垫上，双膝弯曲约90度、双脚全掌稳踩地面，双手轻扶耳后保持颈部放松不拉扯。",
                "收紧核心与骨盆使下腰贴实地面，呼气卷起上背并向一侧旋转躯干。",
                "转动至同侧肩胛离开地面、手肘朝向对侧膝盖斜上方时短暂停顿挤压腹斜肌。",
                "吸气有控制地缓慢还原至仰卧位，可单组专注同侧或左右交替完成；每次卷起转体与还原计一次。",
            ],
        },
        "0364": {
            "name_zh": "坐姿哑铃单臂腕弯举",
            "category": "lower arms",
            "equipment": "dumbbell",
            "target": "forearms",
            "muscle_group": "",
            "secondary_muscles": ["wrist flexors", "brachialis"],
            "movement_patterns_zh": ["腕屈伸"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在稳固的平板训练凳上，双腿分开且双脚踩实地面，非训练手轻扶大腿保持躯干稳定。",
                "训练手反握（掌心朝上）持一只哑铃，将该侧前臂贴稳于同侧大腿上，手腕顺势伸出膝盖前端悬空。",
                "保持前臂稳贴大腿不动，吸气放松手腕使哑铃向下伸展，再呼气收缩前臂屈肌向上弯举卷起腕关节。",
                "在最高点短暂停顿挤压前臂内侧后有控制地下放回起始伸展位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0638": {
            "name_zh": "助力单臂反握引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["upper back", "biceps", "forearms"],
            "movement_patterns_zh": ["垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "站于高位单杠下方，训练手以反握（掌心朝向自己）抓牢横杠，另一只手紧握训练侧手腕提供适度辅助稳定。",
                "悬垂时微屈下肢离地、收紧核心并下沉训练侧肩胛骨，避免借助双腿甩动借力。",
                "呼气由背阔肌与肱二头肌主导拉起身体，带动胸口与下巴升至横杠上方并短暂停顿。",
                "吸气有控制地缓慢放回直臂悬垂起始位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0365": {
            "name_zh": "平凳托臂哑铃双臂锤式弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "并排或略跨坐在稳固的平板训练凳一侧，双脚稳踩地面，略微俯身将双肘与上臂后侧贴靠在凳垫上表面，前臂自然向下方垂出凳缘。",
                "双手以掌心相对的对握各持一只哑铃垂于凳前下方作为起始位。",
                "保持上臂贴紧凳垫与双肩稳定不动，呼气由肱二头肌与肱桡肌发力向上弯举哑铃至接近肩前高度。",
                "在顶端短暂停顿挤压肌肉后，吸气沿原弧线有控制地缓慢下放回垂直起始位；每次弯举与下放计一次。",
            ],
        },
        "0639": {
            "name_zh": "平凳单臂臂屈伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "pectorals", "core"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "背对稳固的平板训练凳坐下，训练侧手掌按紧身侧边缘（手指朝前），非训练手自然放于腰际，双腿向身前伸直并以脚跟撑地。",
                "收紧核心与肩胛并将臀部悬空移出凳缘前侧，保持手臂伸直作为起始位。",
                "吸气有控制地屈肘缓慢下放臀部直至大臂接近水平、避免肩部前扣耸起。",
                "呼气由肱三头肌发力推直单侧手臂回到顶部锁定位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0366": {
            "name_zh": "平凳托臂哑铃单臂锤式弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "跨坐或正坐在稳固的平板训练凳前侧，双脚踩稳地面，非训练手扶在同侧大腿或凳面维持躯干稳定。",
                "训练手以掌心向内的对握持哑铃，将该侧肘部与上臂稳固垫靠在训练凳前端边缘上，前臂自然垂悬于凳缘前方。",
                "保持肘部紧贴凳垫不向上抬起借力，呼气由肱二头肌与前臂肌群发力屈肘将哑铃向上弯举至肩前。",
                "在最高点短暂停顿后，吸气缓慢伸肘下放回垂直悬垂位；单侧完成规定次数后换另一侧。",
            ],
        },
    }

    sources = {
        "0362": "https://exrx.net/WeightExercises/Triceps/DBOneArmTriExt",
        "0635": "https://exrx.net/WeightExercises/Obliques/BWTwistingCrunch",
        "0364": "https://exrx.net/WeightExercises/WristFlexors/DBOneArmWristCurl",
        "0638": "https://exrx.net/WeightExercises/LatissimusDorsi/BWOneArmChinup",
        "0365": "https://exrx.net/WeightExercises/Brachioradialis/DBHammerCurl",
        "0366": "https://exrx.net/WeightExercises/Brachioradialis/DBPreacherHammerCurl",
    }

    review_notes = {
        "0362": "纠正“哑铃单臂三头肌伸展（卧推上）”为“平凳坐姿哑铃单臂颈后臂屈伸”，补齐平板训练凳与过顶伸展负荷标签；原图仅有顶端与底端两姿往复，按解剖规范重制 2×2 四帧并经 1 次肘尖精修与整数平移（Q1 -8,0；Q2 -1,-1）配准，残差 ≤ 1.0 px（匹配分 ≥ 0.9709）。",
        "0635": "将原直译“地板斜腹卷腹”规范为“仰卧屈膝斜腹卷腹”，补齐核心旋转与稳定步骤；原四帧经整数平移（F1 +3,-1；F2 +1,+39）配准后臀腿及双脚支点残差 ≤ 1.0 px（匹配分 ≥ 0.9603）。",
        "0364": "规范“坐姿哑铃单臂腕弯举”反握掌心向上步骤并补齐平板训练凳支撑；原四帧经整数平移（F1 +20,0；F2 0,+1）配准后平凳、双脚及躯干三支点残差 0.0 px（匹配分 ≥ 0.9805）。",
        "0638": "将原名细化为“助力单臂反握引体向上”，补齐单杠必需支撑并清除第 1 帧底边 stray smudge；原四帧经整数平移（F1 +1,0）对齐后单杠四脚及顶角支点残差 ≤ 1.0 px（匹配分 ≥ 0.9868）。",
        "0365": "纠正原英译中误名（图谱与步骤实为俯靠平凳上的肘屈曲锤式弯举而非腕弯举）为“平凳托臂哑铃双臂锤式弯举”，补齐平板训练凳支撑；原四帧经整数平移（F1 +2,0；F2 0,+5）对齐后双侧凳脚与前脚支点残差 ≤ 1.41 px（匹配分 ≥ 0.9818）。",
        "0366": "纠正原英译中误名（实为单臂过凳托臂弯举）为“平凳托臂哑铃单臂锤式弯举”，补齐平板训练凳与单臂计次；原四帧经整数平移（F1 +18,0；F2 0,+3）配准后平凳前后支架与双脚支点残差 ≤ 1.0 px（匹配分 ≥ 0.9835）。",
    }

    pending = {
        "0631": "待修图 · 已将机械直译“引体向上（肌肉上）”纠正为“严格双力臂”并补齐单杠支持；原图第 3 帧推起上杠后横杠与深蹲架整体下移约 150 px（非同一固定机位），暂存待重制。",
        "0634": "待修图 · 已将“离心卷腹”细化为“慢速离心卷腹”并补齐离心下降要领；原图第 3 帧大腿小腿间存在 11 px 横向缩放位移差，暂存待重制。",
        "0363": "待修图 · 已规范哑铃单臂直立划船四步说明与站姿下背低负荷标签；原图第 3 帧提拉至高位时头肩相对双脚缩水压缩（头部匹配分 0.8685），暂存待重制。",
        "0639": "待修图 · 已纠正为平凳单臂臂屈伸并补平板训练凳与高位支撑负荷标签；原图屈肘下放时平凳相对脚跟独立前移 5–7 px 且第 3 帧脚跟竖直下沉 5 px，暂存待重制。",
    }

    result = {
        "batch": "20260926_review18",
        "version": "1.2.23",
        "version_code": 2026092601,
        "apk_name": "时光屋-1.2.23-第十八批动作复核.apk",
        "output": "build/review18-20260926",
        "report": "docs/releases/2026-09-26-review-batch18.md",
        "inspected": inspected,
        "definition_updates": definition_updates,
        "sources": sources,
        "review_candidates": review_candidates,
        "pending": pending,
        "registered_media": review_candidates,
        "original_pose_repairs": ["0635", "0364", "0638", "0365", "0366"],
        "generated_images_imported": 1,
        "image_generation_calls": 2,
        "review_notes": review_notes,
    }
    (B / "review-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    code_files = sorted(R.glob("app/src/main/java/**/*.java"))
    baseline = {str(p.relative_to(R)): sha(p) for p in code_files}
    (B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

    qa_spec = {
        "batch": "20260926_review18",
        "expected_checks": 25,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260926_review18")


if __name__ == "__main__":
    main()
