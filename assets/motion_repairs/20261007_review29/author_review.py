#!/usr/bin/env python3
"""Author Batch 29 (20261007_review29) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["1273", "0420", "1275", "0421", "1297", "0422", "1306", "0423", "1311", "0424"]
    review_candidates = ["0420", "0422"]

    definition_updates = {
        "1273": {
            "name_zh": "击掌俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "shoulders", "core"],
            "movement_patterns_zh": ["水平推", "高位支撑", "爆发推"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双手略宽于肩撑稳地面进入直臂高撑俯卧撑位，收紧核心与臀部保持头肩髋踝呈一条直线。",
                "吸气缓慢屈肘将胸部控制放低接近地面并略微蓄力。",
                "呼气由胸肌与肱三头肌协调发力爆发推起，使双手瞬间推离地面并在胸前完成一次轻快击掌。",
                "迅速将双掌稳稳落回肩下方缓冲接住身体并顺势控制回到高撑位；每次爆发击掌落地计一次。",
            ],
        },
        "0420": {
            "name_zh": "哑铃站立俯身臂后屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["shoulders"],
            "movement_patterns_zh": ["伸肘", "髋铰链", "俯身稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与髋同宽微微屈膝站立，双手掌心相对各握一只较轻重量哑铃，维持背部平直屈髋向前俯身约45度。",
                "将双侧上臂主动向上拉起夹紧体侧至与地面接近平行，先屈肘约90度保持大臂全程固定不动。",
                "呼气锁定双侧肩与上臂不前后晃动，仅由肱三头肌发力将双手哑铃沿直线向后上方彻底伸直肘关节。",
                "在顶峰伸直位短暂停顿感受肱三头肌收紧后，吸气缓慢控制屈肘回约90度垂直位；每次后伸与收回计一次。",
            ],
        },
        "1275": {
            "name_zh": "降膝俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "shoulders"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双手略宽于肩撑地进入直臂直腿高撑起始位，核心收紧保持身体成一直线。",
                "吸气有控制地屈肘缓缓向下放低胸部接近地面，控制双肘斜后45度内收。",
                "抵达底端推起困难处时，顺势将双膝稳稳降落轻点于地面并稍微勾起小腿转换为支撑减轻负荷。",
                "呼气发力伸直双肘推起上身后再恢复起始高撑位；每次完整下放与推起计一次。",
            ],
        },
        "0421": {
            "name_zh": "哑铃站立单臂集中弯举（第二式）",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "俯身稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚宽站并微屈膝盖，保持背部平直略向前俯身，将非训练手掌稳扶在同侧大腿前上方提供支撑。",
                "训练侧手臂垂直垂向地面持一只哑铃（掌心斜向前内侧），保持上臂稳定靠近大腿内前方不晃肩。",
                "呼气由肱二头肌与肱肌发力弯举哑铃向上接近前胸肩高，保持肘位置稳定。",
                "在顶峰短暂停顿收缩后，吸气缓慢伸直肘部放回垂直垂悬位；单侧完成规定次数后换臂。",
            ],
        },
        "1297": {
            "name_zh": "胸肌静态等长挤压",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps"],
            "movement_patterns_zh": ["水平内收", "静态等长"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，核心轻微收紧沉肩，保持脊柱中立不塌腰。",
                "抬起双臂并把双手掌心在胸骨正前方（肘微屈朝外斜放）合掌对齐并持续向内挤压发力。",
                "全程由左右胸大肌持续对抗主动内夹，保持呼吸均匀顺畅不憋气、双肩自然下沉。",
                "持续维持胸肌高度等长发力直至完成规定倒数秒数后缓慢放松放下手臂。",
            ],
        },
        "0422": {
            "name_zh": "手扶上斜凳站姿哑铃单臂弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "俯身稳定"],
            "required_equipment_zh": ["上斜训练凳"],
            "instructions_zh": [
                "站立在稳固的上斜训练凳旁或斜背后方，双脚大步分开微屈膝踩稳地面，将非训练侧手掌按稳在上斜凳背垫顶端并保持背部平直前倾。",
                "训练侧手臂完全垂直地面垂下正反偏前手掌（半旋后握法）抓稳一只哑铃，上臂与肩垂线保持稳定。",
                "呼气锁稳上臂位置不前后摆借力，由肱二头肌与肱肌收缩弯曲单侧肘关节向上弯举哑铃至接近前肩高度。",
                "在顶峰短暂停顿收紧二头肌后，吸气有控制地缓缓下放伸直手臂回垂悬起始位；单侧完成规定次数后换手。",
            ],
        },
        "1306": {
            "name_zh": "爆发腾空俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "shoulders", "core"],
            "movement_patterns_zh": ["水平推", "高位支撑", "爆发推"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双手略宽于肩按稳地面进入高撑直线俯卧撑位，收紧核心与臀腿。",
                "吸气有控制地屈肘将胸部降至接近地面位置积蓄弹性能。",
                "呼气全力爆发推动手掌将上半身推离地面腾空跃起，注意保持躯干整片抬升而不折腰。",
                "顺势屈肘缓冲轻柔落回地面承接力量并推直手臂复位；每次完整腾空复位计一次。",
            ],
        },
        "0423": {
            "name_zh": "哑铃站立单臂过顶臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "core"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，单手握持一只哑铃垂直高举过头顶并保持掌心斜向前内侧、非训练手自然垂于体侧。",
                "收紧腹肌与臀肌稳定肋骨防止反弓，使训练侧大臂尽量贴近耳侧并全程竖直固定不动。",
                "吸气缓慢屈肘沿着脑后斜下方放下哑铃至前臂贴近大臂、充分拉伸肱三头肌长头。",
                "呼气发力伸直单侧肘关节沿原轨迹推回过顶垂直位；单臂完成规定次数后换手。",
            ],
        },
        "1311": {
            "name_zh": "宽距俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "shoulders"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "俯卧撑准备时双手掌明显宽于肩距（约1.5倍肩宽）踩稳地面，核心与臀部收紧维持全身成一直线。",
                "保持肩胛骨适度下沉稳固而不耸肩。",
                "吸气控制屈肘向斜外后方（大臂与躯干呈约60度左右）下放胸口接近地面，感受胸大肌外侧充分拉开。",
                "呼气由胸大肌主导向上推直手臂回到高撑起始位；每次下放与推起计一次。",
            ],
        },
        "0424": {
            "name_zh": "站姿单臂哑铃对握过顶推举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "traps", "core"],
            "movement_patterns_zh": ["垂直推", "过顶伸展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽踩实地面站直，单手持一只哑铃采用掌心向内的对握法举至同侧肩外前方、前臂保持垂直地面。",
                "收紧对侧斜肌与腹部核心保持骨盆与双肩水平端正不向一侧明显倾斜或顶腰。",
                "呼气保持掌心朝内对握轨迹，由三角肌与肱三头肌发力垂直向上推举哑铃过头顶接近伸直。",
                "在最高点短暂停顿控制后，吸气缓慢顺原直线放回肩前方起始位；单侧完成规定次数后换臂。",
            ],
        },
    }

    sources = {
        "0420": "https://exrx.net/WeightExercises/Triceps/DBKickback",
        "0422": "https://exrx.net/WeightExercises/Biceps/DBSupinatingCurl",
    }

    review_notes = {
        "0420": "规范“哑铃站立俯身臂后屈伸”（双侧计数、补齐髋铰链与俯身稳定下背负荷标签及四步锁肘踢臂步骤）；原四帧零移位精确对齐，双脚、双膝及股四头肌与头冠三锚点残差 `0.0 px`（匹配分 `≥ 0.9892`）。",
        "0422": "规范“手扶上斜凳站姿哑铃单臂弯举”（单臂单侧计次、补齐必需支撑器械上斜训练凳与俯身稳定标签）；原四帧零移位精确对齐，双脚、上斜凳框、扶撑手及头冠四锚点残差 `≤ 2.0 px`（匹配分 `≥ 0.9717`）。",
    }

    pending = {
        "1273": "待修图 · 已补齐击掌俯卧撑爆发支撑与四步缓冲落地要点；原图第 0 帧触右缘 `x=479`、第 1 帧触左缘 `x=0`，且第 2 帧腾空拍掌相对前帧产生大幅跨图位置位移，暂存待重制。",
        "1275": "待修图 · 已纠正原误译“跳下俯卧撑”为降膝俯卧撑（贴切反映屈肘低位落膝助推）；原图第 0 帧触右缘 `x=479` 且高撑至落膝跪姿支撑点明显移动，暂存待重制。",
        "0421": "待修图 · 已规范为哑铃站立单臂集中弯举（第二式）并修正握法说明与肱肌协同标签；原图第 1 帧虽近水平平移（`+30, 0`）、第 2 帧近 `0, -3`，但站姿左脚（`+2`）、右脚（`0`）与头冠（`-1`）间仍存在 `3 px` 横向扭转错位（左脚匹配分 `0.9592 < 0.96`），且 `0418` 已优质入库，暂存待重制。",
        "1297": "待修图 · 已将“胸肌等长挤压”规范为胸肌静态等长挤压（确保触发等长静态计时与持续挤压要点）；原图第 2 帧头胸明显上移且转向，在双脚对齐时头部匹配分仅 `0.9303`（第 1 帧仅 `0.9428`，残差 `2.24 px > 2.0`），暂存待重制。",
        "1306": "待修图 · 已规范爆发腾空俯卧撑要点与核心协同肌群；原图三帧间撑地手脚位置反复跨幅跳移与腾空落差，无法固定支点配准，暂存待重制。",
        "0423": "待修图 · 已明确“哑铃站立单臂过顶臂屈伸”（单臂单侧计次）；原图第 0 帧与第 2 帧错用相同的顶部锁肘伸直姿态而非起止全幅度，且顶部哑铃触上缘 `y=0`、第 1 帧头部明显偏移（`sc=0.8647`），暂存待重制。",
        "1311": "待修图 · 已规范为宽距俯卧撑并纠正矛盾步骤文本；原图第 0、2 帧右脚触右缘 `x=479`、第 1 帧左手触左缘 `x=0` 且撑地掌与双脚明显滑移，暂存待重制。",
        "0424": "待修图 · 已规范为站姿单臂哑铃对握过顶推举（单臂单侧计次）；原图第 2 帧推举过顶时躯干明显歪斜压缩（`feet sc=0.9424`, `shorts sc=0.8927`, `head sc=0.7893`），暂存待重制。",
    }

    result = {
        "batch": "20261007_review29",
        "version": "1.2.34",
        "version_code": 2026100701,
        "apk_name": "时光屋-1.2.34-第二十九批动作复核.apk",
        "output": "build/review29-20261007",
        "report": "docs/releases/2026-10-07-review-batch29.md",
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
        "batch": "20261007_review29",
        "expected_checks": 13,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261007_review29")


if __name__ == "__main__":
    main()
