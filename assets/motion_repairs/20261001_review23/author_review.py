#!/usr/bin/env python3
"""Author Batch 23 (20261001_review23) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0691", "0388", "0696", "0389", "0697", "0390", "0699", "0391", "0705", "0392"]
    review_candidates = []

    definition_updates = {
        "0691": {
            "name_zh": "贴墙坐姿侧卷腹",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "core"],
            "movement_patterns_zh": ["核心侧屈", "核心稳定"],
            "required_equipment_zh": ["墙面"],
            "instructions_zh": [
                "屈膝坐在墙边地面上，双脚平踩地面、髋部与中上背轻轻靠稳墙面，双手轻扶耳侧或脑后且双肘向两侧打开。",
                "收紧核心稳定骨盆贴地，避免用双手向前拉扯颈椎。",
                "呼气由一侧腹内外斜肌发力带动上身沿墙面顺势向该侧侧屈下压，使同侧肋缘靠近髋骨。",
                "吸气缓慢有控制地回到正中坐姿后再向另一侧侧屈，左右交替完成预定次数。",
            ],
        },
        "0388": {
            "name_zh": "平凳坐姿哑铃交替肩上推举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "traps", "core"],
            "movement_patterns_zh": ["推", "垂直推", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "端坐在稳固的平板训练凳上，双脚分开踩实地面，核心收紧保持躯干直立不塌腰后仰，双手正握各持一只哑铃举至肩侧上方、掌心朝前。",
                "保持非工作侧哑铃稳停于肩部高度，小臂垂直地面。",
                "呼气由三角肌与肱三头肌发力将一侧哑铃垂直向上推举过头顶至肘部接近伸直（留轻微缓冲不锁死）。",
                "吸气有控制地降回肩侧后换另一侧交替推举；双侧交替完成预定次数。",
            ],
        },
        "0696": {
            "name_zh": "地面仰卧自助力腿弯举",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "hamstrings",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "calves"],
            "movement_patterns_zh": ["膝屈曲", "髋伸展"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双手掌心朝下平放体侧辅助稳定，单腿或双腿脚跟压住地面滑动（或另一脚轻抵协助给阻）。",
                "收紧核心与臀部，保持膝关节自然贴合发力方向。",
                "呼气由大腿后侧腘绳肌收缩主动屈膝将脚跟向臀部方向拉近，顺势略微抬离臀部协同控制轨迹。",
                "吸气在自加阻力可控前提下缓慢伸膝放回接近地面起始位；每次屈伸弯举计一次。",
            ],
        },
        "0389": {
            "name_zh": "平凳坐姿双手哑铃过顶臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms", "core"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "端坐在平板训练凳上，双脚分开稳踩地面、挺胸收紧核心防止下背反弓。",
                "双手叠掌稳托住一只哑铃内侧片端垂直高举过头顶作为起始位，双侧大臂夹紧靠近耳侧、肘尖朝前。",
                "锁定上臂贴近头部固定不动，吸气缓慢屈肘将哑铃沿脑后弧线降落至肱三头肌充分拉伸处。",
                "呼气发力伸直双肘沿原弧线推回过顶起始位；每次下放与推回计一次。",
            ],
        },
        "0697": {
            "name_zh": "仰卧自助力反向腿弯举",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "hamstrings",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "calves"],
            "movement_patterns_zh": ["膝屈曲", "髋伸展"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双手压实垫面辅助稳定骨盆，双腿先向前伸展准备由腘绳肌发力屈膝。",
                "收紧核心并使对侧脚掌配合轻抵施力脚踝或保持屈膝轨迹一致。",
                "呼气弯曲膝关节带动小腿向臀部后侧主动回收收缩腘绳肌，避免腰椎离开垫面借力。",
                "在屈膝顶峰控住片刻后，吸气缓慢伸展回起始伸直位；每次弯举与伸展计一次。",
            ],
        },
        "0390": {
            "name_zh": "瑜伽球坐姿哑铃双臂弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis", "core"],
            "movement_patterns_zh": ["肘屈曲", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "端坐在稳固不滑移的瑜伽球中央，双脚略宽于肩稳踩地面、收紧核心保持躯干直立与球体平稳，双手反握（掌心朝前）各持一只哑铃垂于体侧。",
                "上臂贴紧躯干两侧不动、肩带下沉不耸肩。",
                "呼气由肱二头肌发力向上屈肘弯举哑铃至接近肩前，全程保持瑜伽球稳定不前后晃动。",
                "顶峰短暂挤压后，吸气缓慢伸肘下放回体侧伸展位；每次弯举与还原计一次。",
            ],
        },
        "0699": {
            "name_zh": "肩部轻拍俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "delts", "core"],
            "movement_patterns_zh": ["水平推", "高位支撑", "核心抗旋"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双手略宽于肩踩稳地面进入高撑俯卧撑起始位，双脚分开约与髋同宽增强骨盆抗旋转稳定。",
                "吸气控制屈肘下放胸部接近地面，呼气推直双臂回到高撑直线位。",
                "保持骨盆水平不左右歪斜，抬起一只手轻拍对侧肩头并短暂停稳后落掌撑地。",
                "下一次俯卧撑推起后换另一只手轻拍对侧肩，左右交替计次；每完成一次俯卧撑与拍肩计一次。",
            ],
        },
        "0391": {
            "name_zh": "直立靠背凳坐姿哑铃弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["直立靠背训练凳"],
            "instructions_zh": [
                "坐在稳固的直立靠背训练凳上，臀、背与肩胛后侧稳贴竖直靠背，双脚平踩地面，双手反握各持一只哑铃垂于体侧。",
                "保持上臂稳停于肩下两侧不向前甩动、肩部下沉。",
                "呼气由肱二头肌发力向上屈肘弯举哑铃至接近肩前，前臂略做旋后。",
                "在顶峰短暂停顿后，吸气有控制地缓缓伸直双臂下放回体侧；每次弯举与下放计一次。",
            ],
        },
        "0705": {
            "name_zh": "单侧侧桥（第二式）",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "glutes", "shoulders"],
            "movement_patterns_zh": ["高位支撑", "核心侧稳"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "侧躺于地面或训练垫上，双腿伸直上下叠放并拢，下侧肘关节置于肩关节正下方、前臂垂直躯干紧贴地面撑稳，上侧手叉腰或贴放胯侧。",
                "收紧核心、腹内外斜肌与臀肌，呼气将髋部向上顶离地面使耳、肩、髋、膝与踝呈一条稳固斜直线。",
                "在顶点静力控住规定秒数，避免塌腰或骨盆前后翻转。",
                "时间结束后缓缓下放髋部并切换至另一侧完成同等保持时长。",
            ],
        },
        "0392": {
            "name_zh": "平凳坐姿哑铃前平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "pectorals"],
            "movement_patterns_zh": ["肩屈曲"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "端坐在稳固的平板训练凳上，双脚分开踩实地面、收紧核心维持脊柱直立，双手正握（掌心朝下或相对大腿上方）各持一只哑铃放在大腿前侧。",
                "双肘保持微屈固定角度、肩带下沉不耸肩。",
                "呼气由三角肌前束发力同时将双臂向前上方弧线抬举至与肩齐平（大臂大致平行地面），过程避免上身后仰借力。",
                "在顶端短暂停顿收缩后，吸气缓慢有控制地放回大腿上方起始位；每次举起与下放计一次。",
            ],
        },
    }

    sources = {}
    review_notes = {}

    pending = {
        "0691": "待修图 · 已将“坐姿侧卷腹（靠墙）”改为“贴墙坐姿侧卷腹”（避开静态“靠墙坐”词库误判）并补齐墙面支持；原图第 2 帧斜靠屈曲时墙面拐角与双脚相对第 0 帧产生约 14–22 px 平移与腿部比例漂移，暂存待重制。",
        "0388": "待修图 · 已规范为平凳坐姿哑铃交替肩上推举并补齐平板训练凳与过顶伸展负荷；原图第 0 帧底边触底（y=479）、第 2 帧上方哑铃被顶边裁断（y=0），且头部及静止臂（dy=+5）相对平凳支腿（dy=-4）存在约 9 px 纵向拉伸错位，暂存待重制。",
        "0696": "待修图 · 已核对地面仰卧自助力腿弯举文字；原图错画成脚尖点地仰卧顶髋（臀桥）且高亮错误肌群（股四头肌）与动作名称不符，同时第 2 帧头部与脚尖相对发生约 22 px 跨体位移，暂存待重制。",
        "0389": "待修图 · 已纠正原重大误译（dumbbell seated bench extension 原被译成“哑铃坐姿卧推伸展”，实为坐姿过顶臂屈伸）并补齐平板训练凳；原图第 2 帧人物与平凳整体缩小下移超过 30 px，无法与前帧配准，暂存待重制。",
        "0697": "待修图 · 已核对仰卧自助力反向腿弯举步骤；原图错画成仰卧曲膝抬腿卷腹（高亮前侧髋屈肌与大腿前侧）且第 2 帧头胸与下背产生 >10 px 跨体变形位移，暂存待重制。",
        "0390": "待修图 · 已规范为瑜伽球坐姿哑铃双臂弯举并补齐瑜伽球与核心稳定；原图第 2 帧双脚及球底对齐后头部出现约 5 px 纵向压缩（头顶匹配分仅 0.9081），暂存待重制。",
        "0699": "待修图 · 已规范为肩部轻拍俯卧撑并核对左右交替拍肩与高位支撑；原图第 1 帧降低姿态时双掌与双脚独立移位 8–14 px，第 2 帧单手拍肩同时支撑掌与后脚间距明显改变，暂存待重制。",
        "0391": "待修图 · 已规范为直立靠背凳坐姿哑铃弯举并补齐直立靠背训练凳；原图第 1、2 帧双脚对齐后直立凳左支腿相对双脚横移缩窄 4–5 px 且靠背出现约 10 px 纵向错位，暂存待重制。",
        "0705": "待修图 · 已规范为单侧侧桥（第二式）确保等长计时与单侧计次逻辑并存；原图第 1、2 帧起桥时前臂肘撑点与脚踝支点同向滑动 13–22 px，不能固定支点，暂存待重制。",
        "0392": "待修图 · 已规范为平凳坐姿哑铃前平举并补齐平板训练凳与肩屈曲；原图第 1 帧双脚对齐后平凳左支腿出现约 9 px 横向跳移，第 2 帧头部匹配分仅 0.9260（约 2.8 px 错位），暂存待重制。",
    }

    result = {
        "batch": "20261001_review23",
        "version": "1.2.28",
        "version_code": 2026100101,
        "apk_name": "时光屋-1.2.28-第二十三批动作复核.apk",
        "output": "build/review23-20261001",
        "report": "docs/releases/2026-10-01-review-batch23.md",
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
        "batch": "20261001_review23",
        "expected_checks": 16,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261001_review23")


if __name__ == "__main__":
    main()
