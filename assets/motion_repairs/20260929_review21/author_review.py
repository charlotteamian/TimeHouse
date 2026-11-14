#!/usr/bin/env python3
"""Author Batch 21 (20260929_review21) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0672", "0377", "0674", "0378", "0677", "0379", "0678", "0380", "0684", "0381"]
    review_candidates = ["0378", "0379"]

    definition_updates = {
        "0672": {
            "name_zh": "双杠直腿反撑臂屈伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["chest", "shoulders", "forearms"],
            "movement_patterns_zh": ["推", "垂直推"],
            "required_equipment_zh": ["双杠"],
            "instructions_zh": [
                "坐于双杠末端地面前方，双手向后撑握两根平行杠面，双腿向前伸直并用脚跟轻抵地面。",
                "双手撑起臀部使身体离开地面，保持胸口微抬、核心收紧，避免肩部向前耸起。",
                "吸气缓慢屈肘控制下放臀部，直到大臂大致与地面平行、感受肱三头肌充分拉伸。",
                "呼气用力推直双臂回到顶端起始位；每次下放与推起计一次。",
            ],
        },
        "0377": {
            "name_zh": "俯身哑铃后束划船",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids", "lats"],
            "movement_patterns_zh": ["水平拉", "髋铰链", "俯身稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立、膝关节微屈，屈髋俯身使躯干保持平直接近与地面呈三至四十五度角，双手掌心朝内各持一只哑铃垂于肩下方。",
                "保持腰背收紧中立且肩带下沉，避免含胸圆背或借惯性甩腰。",
                "呼气由三角肌后束带动双肘向斜外后方拉起哑铃，至上臂大致与躯干同高并向内收紧肩胛骨。",
                "在顶峰短暂停顿后，吸气有控制地缓慢下放回悬垂起始位；每次提拉与下放计一次。",
            ],
        },
        "0674": {
            "name_zh": "反握引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "forearms", "upper back"],
            "movement_patterns_zh": ["垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "双手约与肩同宽采用反握（掌心朝向自己）抓稳高位单杠，双臂伸直悬垂，小腿微屈向后交叠并收紧核心。",
                "先下沉并微收肩胛骨启动动作，避免靠甩腿或晃腰借力。",
                "呼气由背阔肌与肱二头肌协同发力将身体垂直拉起，引导下颌抬至单杠高度上方并在顶部短暂控住。",
                "吸气用两至三秒缓慢伸直双臂下放回悬垂起始位；每次拉起与还原计一次。",
            ],
        },
        "0378": {
            "name_zh": "俯身对握哑铃后飞鸟",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平外展", "俯身稳定", "髋铰链"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立、双膝微屈，保持脊柱中立屈髋俯身至上身接近水平或约三十度俯角，双手对握各持一只轻重量哑铃垂于肩下方。",
                "双肘微屈并锁定轻微固定角度，肩胛带保持下沉不耸肩、颈部与躯干保持一条直线。",
                "呼气由三角肌后束发力带动双臂沿弧线向身体两侧横向外展抬起，直到大臂大致与地面平行。",
                "在顶点短暂停顿感受肩后束收缩后，吸气有控制地沿原弧线缓慢下放回起始悬垂位；每次展开与下放计一次。",
            ],
        },
        "0677": {
            "name_zh": "吊环臂屈伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["chest", "shoulders", "core"],
            "movement_patterns_zh": ["垂直推"],
            "required_equipment_zh": ["吊环"],
            "instructions_zh": [
                "双手稳握与肩同宽的悬垂吊环并撑直双臂锁定在躯干两侧，收紧核心与臀腿保持吊环贴近身体稳定不晃动。",
                "保持双肘贴近体侧，吸气缓慢屈肘有控制地降低身体，直到大臂略低于水平高度或肩前舒适极限。",
                "在底端短暂停顿控制吊环外翻或外撇倾向，避免突然弹底。",
                "呼气由肱三头肌与胸大肌发力推直双臂回到顶端撑直位；每次下放与撑起计一次。",
            ],
        },
        "0379": {
            "name_zh": "上斜凳俯卧哑铃反向飞鸟",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平外展", "俯身稳定"],
            "required_equipment_zh": ["上斜训练凳"],
            "instructions_zh": [
                "将靠背调节至约三十至四十五度上斜角，俯卧贴靠在斜板上使胸廓与下颌上方轻抵靠背顶端、双脚前掌稳踩地面。",
                "双手各持一只轻重量哑铃以对握或微内旋角度自然垂于肩部下方，双肘微屈锁住轻微角度。",
                "保持胸腹全程贴实斜板不借力抬头甩腰，呼气由三角肌后束发力将双臂向两侧上方水平展开至与肩同高。",
                "在顶点短暂停顿感受肩后束与菱形肌收缩后，吸气缓慢有控制地沿原弧线放回肩下方；每次抬起与下放计一次。",
            ],
        },
        "0678": {
            "name_zh": "洛奇式前后交替引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "forearms", "upper back"],
            "movement_patterns_zh": ["垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "双手略宽于肩以正握抓稳高位单杠，全身直臂悬垂并收紧核心与臀腿防止前后晃动。",
                "第一次上拉由背阔肌带动将上胸拉向单杠前侧，随后有控制地缓慢下降回底端悬垂位。",
                "紧接着下一次上拉微微低头让单杠从后脑勺下方接近颈后上背高度，感受中上背部收缩后缓慢下放回悬垂位。",
                "若颈后活动度受限或肩前不适可改为全组胸前正握上拉；每次拉起与还原计一次。",
            ],
        },
        "0380": {
            "name_zh": "俯身哑铃后束侧平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平外展", "俯身稳定", "髋铰链"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立并微屈双膝，保持腰背平直俯身屈髋至接近四十五度，双手掌心朝后或相对各持一只哑铃垂于腿前。",
                "锁定肘关节微屈角度与肩带下沉位，颈部保持与脊柱同轴。",
                "呼气由三角肌后束主导带动双臂向两侧横向抬举，直至大臂与地面大致平行、避免耸肩代偿。",
                "顶峰短暂挤压后，吸气沿原弧线缓慢放回腿前悬垂位；每次平举与下放计一次。",
            ],
        },
        "0684": {
            "name_zh": "跑步机快跑",
            "category": "cardio",
            "equipment": "body weight",
            "target": "cardiovascular system",
            "muscle_group": "",
            "secondary_muscles": ["quadriceps", "hamstrings", "calves", "glutes"],
            "movement_patterns_zh": ["有氧", "跑跳"],
            "required_equipment_zh": ["跑步机"],
            "instructions_zh": [
                "站在跑带两侧边条上启动跑步机并调节合适配速后迈上跑带，目视前方、核心收紧保持躯干微前倾直立。",
                "双臂自然屈肘前后摆臂维持身体平衡，避免双手长时间紧抓扶手。",
                "随跑带节奏交替摆腿提膝并由中前足掌轻快落地过渡滚动蹬伸，保持呼吸均匀有节律。",
                "完成目标时间或距离后逐步降速慢走缓冲再停机下机。",
            ],
        },
        "0381": {
            "name_zh": "哑铃后撤弓步",
            "category": "upper legs",
            "equipment": "dumbbell",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["quadriceps", "hamstrings", "calves", "core"],
            "movement_patterns_zh": ["下肢推", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与髋同宽直立，双手掌心朝内各持一只哑铃垂于体侧，挺胸收紧核心稳定骨盆。",
                "保持躯干直立或极轻微前倾，一侧脚向正后方迈出一大步并以前脚掌稳踏地面。",
                "吸气垂直下沉重心屈膝下蹲，直到前大腿大致平行地面、后膝接近轻触地面上方一两厘米处且前膝对准脚尖方向。",
                "呼气由前侧脚跟蹬地发力伸直膝髋站回起始直立位；两侧交替或单侧完成后换边。",
            ],
        },
    }

    sources = {
        "0378": "https://exrx.net/WeightExercises/DeltoidPosterior/DBRearLateralRaise",
        "0379": "https://exrx.net/WeightExercises/DeltoidPosterior/DBLyingRearLateralRaise",
    }

    review_notes = {
        "0378": "核对站姿俯身对握哑铃后飞鸟（区别于现有 0383）的外展轨迹与三角肌后束、斜方肌、菱形肌联动及俯身稳定／髋铰链下背负荷标签；原四帧经整数平移（F1 +21,0；F2 0,+14）配准后前后双脚与头冠三锚点残差 ≤ 1.0 px（匹配分 ≥ 0.9755）。",
        "0379": "纠正原名称所含静态触发词“支撑”与错误站姿文字描述，依据图谱实为靠上斜凳俯卧的胸腹支撑飞鸟，规范为“上斜凳俯卧哑铃反向飞鸟”并补齐上斜训练凳与俯身稳定标签；原四帧经整数平移（F1 +4,0；F2 0,+20）配准后斜凳前脚与前后双脚、头冠四锚点残差 ≤ 2.0 px（匹配分 ≥ 0.9696）。",
    }

    pending = {
        "0672": "待修图 · 已纠正原误译“反向俯卧撑”为双杠直腿反撑臂屈伸并补齐双杠必需器械；原图第 1、2 帧双杠立柱与脚跟存在 16–25 px 独立位移与高度缩放，暂存待重制。",
        "0377": "待修图 · 已规范为俯身哑铃后束划船并补齐俯身稳定／髋铰链标签；原图第 2 帧抬头躯干相对前脚出现约 6.4 px 位移且第 1 帧后脚匹配分仅 0.9210，暂存待重制。",
        "0674": "待修图 · 已核对反握引体向上动作要点并补齐单杠支撑；原图第 2 帧头顶发冠贴上边 y=0 被削平裁切约 16 px 宽且第 0 帧底边 y=479 留有杂点，暂存待重制。",
        "0677": "待修图 · 已纠正原误译“环上俯卧撑”为吊环臂屈伸并补齐吊环所需器械；原图第 0 帧与第 2 帧几近一致（diff02=1.39），实质仅双姿交替且顶底贴边裁切，暂存待重制。",
        "0678": "待修图 · 已将“岩石引体向上下拉”规范为洛奇式前后交替引体向上并补齐单杠；原图第 1 帧门架宽度相对第 0 帧缩窄且第 2 帧顶梁与底座存在 7 px 独立纵移，暂存待重制。",
        "0380": "待修图 · 已规范为俯身哑铃后束侧平举并补齐俯身稳定／髋铰链标签；原图第 2 帧举臂至顶点时头部（dy=+4）相对髋臀（dy=+11）及双脚（dy=+8）存在约 5–7 px 纵向分离错位，暂存待重制。",
        "0684": "待修图 · 已纠正原图实为跑步机跑步却误写为原地慢跑并补齐跑步机所需器械；原图仅含 2 帧（[0, 1180 ms]）缺少 4 帧往复循环与过渡姿势，暂存待重制。",
        "0381": "待修图 · 已规范为哑铃后撤弓步并补齐站姿稳定／下肢推负荷标签；原图第 2 帧头顶及上方杂点触顶裁切（y=0）且跨帧脚部底边截断（y=479），步幅与身高比例不稳，暂存待重制。",
    }

    result = {
        "batch": "20260929_review21",
        "version": "1.2.26",
        "version_code": 2026092901,
        "apk_name": "时光屋-1.2.26-第二十一批动作复核.apk",
        "output": "build/review21-20260929",
        "report": "docs/releases/2026-09-29-review-batch21.md",
        "inspected": inspected,
        "definition_updates": definition_updates,
        "sources": sources,
        "review_candidates": review_candidates,
        "pending": pending,
        "registered_media": review_candidates,
        "original_pose_repairs": review_candidates,
        "generated_images_imported": 0,
        "image_generation_calls": 0,
        "quota_exhausted_reset_at": "2026-11-12T05:37:04Z",
        "review_notes": review_notes,
    }
    (B / "review-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    code_files = sorted(R.glob("app/src/main/java/**/*.java"))
    baseline = {str(p.relative_to(R)): sha(p) for p in code_files}
    (B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

    qa_spec = {
        "batch": "20260929_review21",
        "expected_checks": 13,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260929_review21")


if __name__ == "__main__":
    main()
