#!/usr/bin/env python3
"""Author Batch 28 (20261006_review28) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0865", "0415", "0870", "0416", "1160", "0417", "1167", "0418", "1271", "0419"]
    review_candidates = ["1167", "0418"]

    definition_updates = {
        "0865": {
            "name_zh": "仰卧举腿提臀",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors", "core"],
            "movement_patterns_zh": ["核心屈曲", "下腹控制"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双手掌心朝下平放于臀侧地面稳住肩背，双腿并拢伸直轻悬或贴垫准备。",
                "微收下颌保持颈椎放松，下背轻轻压实垫面不留明显拱腰空隙。",
                "呼气由下腹肌主导先抬高双腿至接近垂直于地面，随后顺势轻微卷起骨盆与下臀向上发力冲顶。",
                "在顶点短暂停顿控制后，吸气有控制地先降回骨盆再缓慢放低双腿回起始位；每次举腿提臀计一次。",
            ],
        },
        "0415": {
            "name_zh": "哑铃站立交替侧平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "forearms"],
            "movement_patterns_zh": ["肩外展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，双手各握一只适中重量哑铃自然垂于大腿外侧，手掌朝内且肘部微屈固定。",
                "下沉肩胛、收紧核心避免躯干向侧方代偿甩摆。",
                "保持一侧哑铃稳垂于体侧不动，呼气由工作侧三角肌中束发力将另一侧手臂向正侧方平举至接近与肩同高。",
                "在肩高处略微停顿控制后，吸气缓慢下放回体侧起始位再换另一臂交替抬举；双侧交替稳定完成规定次数。",
            ],
        },
        "0870": {
            "name_zh": "仰卧屈膝提臀",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors", "obliques"],
            "movement_patterns_zh": ["核心屈曲", "下腹控制"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双臂伸直掌心朝下贴放体侧地面，屈膝抬起双腿使大腿大致垂直地面、小腿自然收拢。",
                "收紧下腹，下背部轻贴垫面准备向上卷动骨盆。",
                "呼气集中用腹直肌下部收缩向上卷起骨盆与臀部离开垫面，将双膝温和拉向胸口方向而非借腿部摆动。",
                "在最高处控住半秒后，吸气缓慢一节节放回臀腰落垫恢复屈膝预备位；每次提臀与放回计一次。",
            ],
        },
        "0416": {
            "name_zh": "哑铃站立弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，双手反握（掌心全程朝前）各持一只哑铃垂于身体前外侧，双肘自然贴近体侧。",
                "挺胸沉肩并收紧核心与臀部，全程避免前后仰腰甩借力量。",
                "固定双侧上臂垂直稳定不动，呼气由肱二头肌与肱肌发力弯曲双肘同时将哑铃向上弯举至肩前高度。",
                "在顶峰短暂停顿收紧后，吸气有控制地缓慢伸肘放回最低垂悬位（留微屈不锁死）；每次弯举与下放计一次。",
            ],
        },
        "1160": {
            "name_zh": "波比跳",
            "category": "cardio",
            "equipment": "body weight",
            "target": "cardiovascular system",
            "muscle_group": "",
            "secondary_muscles": ["quads", "hamstrings", "glutes", "calves", "shoulders", "chest"],
            "movement_patterns_zh": ["心肺", "全身爆发"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立准备，快速屈髋屈膝下蹲并用双手按稳肩前方地面。",
                "双手撑实后爆发向后踢腿跳成直臂高撑直线体态（高阶可衔接完成一次贴地俯卧撑），保持核心紧绷不塌腰。",
                "随即收紧腹部将双脚积极蹬跳回双手外侧成蹲姿。",
                "顺势由下肢驱动垂直向上轻盈跃起并双臂高举过头，前脚掌缓冲轻落回站立准备下一次循环；每次完整起伏计一次。",
            ],
        },
        "0417": {
            "name_zh": "哑铃站立提踵",
            "category": "lower legs",
            "equipment": "dumbbell",
            "target": "calves",
            "muscle_group": "",
            "secondary_muscles": ["soleus", "ankles"],
            "movement_patterns_zh": ["双腿", "踝跖屈"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚约与髋同宽平踩地面直立，双手各垂握一只哑铃自然放于大腿外侧、掌心朝内。",
                "挺胸收腹，双膝保持自然伸直略留缓冲不锁死，重心落在前脚掌。",
                "呼气由小腿三头肌发力向上垂直踮起双脚脚跟至最高处，保持双踝稳定不内外翻。",
                "在顶点停顿挤压小腿后，吸气有控制地缓缓降回脚跟着地起始位；每次踮起与下落计一次。",
            ],
        },
        "1167": {
            "name_zh": "动态扩胸拉伸",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders"],
            "movement_patterns_zh": ["拉伸", "动态扩胸"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，核心轻微收紧保持脊柱中立、沉肩不耸肩。",
                "将双臂平伸向身体两侧至与肩同高成大字张开，掌心朝前温和向后展开胸廓感受胸大肌与肩前束动态伸展。",
                "保持双臂处于肩高水平面内，有节奏地将双臂顺势向前摆拢并轻轻交错合抱在胸前。",
                "随即再流畅匀速摆臂重新大字打开扩胸，全程依托肌控往复摆动而不甩腰后仰；每次扩合摆动计一次。",
            ],
        },
        "0418": {
            "name_zh": "哑铃站立单臂集中弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "俯身稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚明显宽于肩站立并微屈双膝，保持背部平直向斜前方屈髋俯身约45度，将非训练侧手掌稳扶在同侧膝上方大腿前侧提供稳定支点。",
                "训练侧手臂垂直悬向地面握住一只哑铃（掌心偏向前内侧），保持上臂垂直锁稳并轻微稳定在同侧腿内前方不前后晃动。",
                "呼气集中由肱二头肌与肱肌收缩弯曲该侧肘关节，顺弧线将哑铃垂直拉起直至接近前肩胸前高度。",
                "在顶峰短暂停顿收缩后，吸气有控制地缓慢伸直肘部放回垂直垂悬起始位；单侧完成规定次数后换另一臂。",
            ],
        },
        "1271": {
            "name_zh": "胸肩前侧拉伸",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["delts"],
            "movement_patterns_zh": ["拉伸"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然直立，下沉肩胛并收紧核心防止肋骨外翻与塌腰。",
                "将双臂向身体后下方伸展并于身后轻握手指（或双手扶住门框／立柱两侧），缓慢夹紧双侧肩胛骨向后打开胸腔。",
                "略微抬胸向前温和递出胸骨，清晰感受两侧胸大肌与三角肌前束的温和牵伸感而不出现肩前刺痛。",
                "保持自然呼吸牵伸20至30秒后缓慢放松收回手臂；左右或重复完成预定次数。",
            ],
        },
        "0419": {
            "name_zh": "哑铃站立过顶前平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "upper chest"],
            "movement_patterns_zh": ["肩屈曲", "过顶伸展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立踩稳地面，双手正握各持一只较轻重量哑铃自然垂于大腿前侧、掌心朝向身体。",
                "收紧腹肌与臀肌锁定脊柱中立，防止双手高举过顶时下腰反弓借力。",
                "保持双肘微屈不锁死，呼气由三角肌前束发力沿着体前中线匀速向上抬起双臂并继续举至头顶上方高度。",
                "在顶端短暂停顿控制后，吸气沿原弧线缓慢有控制地放回大腿前侧起始位；每次高举与下放计一次。",
            ],
        },
    }

    sources = {
        "1167": "https://www.rehabhero.ca/exercise",
        "0418": "https://www.muscleandstrength.com/exercises/single-arm-dumbbell-concentration-curl.html",
    }

    review_notes = {
        "1167": "规范“动态扩胸拉伸”（双侧动态往复扩合而不包含静态“保持”词与错误计时要求），核对胸大肌／肩部肌群标签；原第 1 帧经纯整数水平平移 `(+29, 0)` 后双脚、裤腰、头冠三锚点残差 `≤ 1.0 px`（匹配分 `≥ 0.9640`）。",
        "0418": "规范“哑铃站立单臂集中弯举”（单臂单侧计次、补齐俯身稳定下背与非工作手扶腿支撑步骤、清除冗余肌群并补肱肌协同标签）；原四帧零漂移 `0.0 px` 精准对齐（四锚点残差 `0.0 px`，匹配分 `≥ 0.9860`）。",
    }

    pending = {
        "0865": "待修图 · 已纠正原错译“仰卧抬腿臀部”为仰卧举腿提臀并规范四步要点；原图第 1、2 帧头部与撑地手掌／臀部发生 6–26 px 横纵独立漂移（arms_hips sc=0.7227），暂存待重制。",
        "0415": "待修图 · 已规范为哑铃站立交替侧平举；原图第 1、2 帧双脚、裤腰、头冠与非工作侧左哑铃之间发生 3–8 px 独立位置偏移（sc=0.8517），且四帧循环仅举右侧未体现交替动作，暂存待重制。",
        "0870": "待修图 · 已纠正原错译“臀部向上”为仰卧屈膝提臀；原图第 0 帧脚尖触右缘 `x=479`、第 1 帧头顶触左缘 `x=0`，且第 2 帧头肩向上明显位移 `>20 px`，暂存待重制。",
        "0416": "待修图 · 已完善哑铃站立弯举反握说明与肱肌协同标签；原图第 2 帧垂直身高相对第 0 帧缩水约 4 px（h=462 vs 465），双脚对齐后头部产生 3.0 px 纵向错位（head sc=0.9001），暂存待重制。",
        "1160": "待修图 · 已补齐波比跳四步连贯要点与全身协同肌群；原图第 0 帧触底（y=479）、第 2 帧指尖截顶（y=0），且下蹲到腾空跳跃之间跨体位置跳移、缺少俯卧支撑帧，暂存待重制。",
        "0417": "待修图 · 已规范哑铃站立提踵双腿计次与踝关节协同标签；原图第 1、2 帧垫步踮脚后全身高度反而相对第 0 帧缩水约 26 px（h=393 vs 419）且双脚腾空离开原地面基线，暂存待重制。",
        "1271": "待修图 · 已按实际解剖原理重写胸肩前侧拉伸（需向后伸展／门框后展扩胸）；原图四帧实画手臂向体前抱拢缩胸而非向后打开胸肩，动作示意与名称及目标完全相反，暂存待重制。",
        "0419": "待修图 · 已规范哑铃站立过顶前平举并清理错误“肱二头肌”次要肌群；原图第 0 帧脚尖触底（y=479）、第 2 帧顶边哑铃被裁断（y=0），且双脚与躯干比例跨帧严重错位，暂存待重制。",
    }

    result = {
        "batch": "20261006_review28",
        "version": "1.2.33",
        "version_code": 2026100601,
        "apk_name": "时光屋-1.2.33-第二十八批动作复核.apk",
        "output": "build/review28-20261006",
        "report": "docs/releases/2026-10-06-review-batch28.md",
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
        "batch": "20261006_review28",
        "expected_checks": 13,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261006_review28")


if __name__ == "__main__":
    main()
