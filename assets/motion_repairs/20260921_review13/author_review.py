#!/usr/bin/env python3
"""Author Batch 13 (20260921_review13) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0489", "0335", "0490", "0337", "0491", "0338", "0492", "0339", "0493", "0340"]
    review_candidates = ["0335", "0490", "0337", "0491", "0338"]

    definition_updates = {
        "0489": {
            "name_zh": "罗马椅抱胸背屈伸",
            "category": "back",
            "equipment": "body weight",
            "target": "lower back",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "hamstrings"],
            "movement_patterns_zh": ["髋铰链"],
            "required_equipment_zh": ["带勾脚的下斜训练凳"],
            "instructions_zh": [
                "将45度罗马椅（山羊挺身凳）靠垫调至髋骨前侧下方，双脚踩稳踏板并将脚踝卡紧在后方滚轴下，双臂在胸前交叉抱紧。",
                "收紧核心与臀部使头、颈、躯干与双腿呈一条45度斜线作为起始位。",
                "吸气以髋关节为轴保持脊柱中立平直向前下方俯身屈髋，直至躯干与双腿约成90度并感受腘绳肌与臀部拉伸。",
                "呼气由臀大肌、腘绳肌与竖脊肌协同发力伸髋抬起躯干回到斜线位置，顶部避免腰椎过度反弓；每次俯身与抬起计一次。",
            ],
        },
        "0335": {
            "name_zh": "哑铃侧平举转前平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "pectorals", "serratus anterior"],
            "movement_patterns_zh": ["外展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立，收紧核心保持躯干挺直，双手各持一只哑铃自然垂于大腿外侧，掌心朝向身体。",
                "保持肘部微屈锁定、肩带下沉不耸肩，呼气由三角肌中束发力将双臂向两侧平举至与地面平行。",
                "维持手臂与地面平行的高度，控制双臂在水平面内向身前合拢至双肩正前方的前平举位置。",
                "再将双臂水平展开回到身体两侧并沿原路径缓慢下放回大腿外侧；每次完整完成侧平举、前移、回展与下放计一次。",
            ],
        },
        "0490": {
            "name_zh": "上斜窄距俯卧撑",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["pectorals", "delts", "abs"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "双手以略窄于肩宽的间距撑在稳固的平板训练凳边缘，双脚向后踩地，收紧核心与臀部使头、躯干与双腿呈一条斜线。",
                "吸气屈肘并让双肘全程贴近躯干两侧向后滑动，有控制地将胸部向凳面方向下放。",
                "下放至胸部接近凳面、上臂与前臂约成90度时短暂停顿，保持腰背平直不塌腰。",
                "呼气由肱三头肌与胸大肌发力推起身体直到双臂伸直回到起始支撑位；每次下放与推起计一次。",
            ],
        },
        "0337": {
            "name_zh": "哑铃仰卧横面臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头部、上背与臀部贴实凳面，双脚平踩地面，双手各持哑铃垂直举于肩部正上方。",
                "锁定上臂位置不变，吸气屈肘让前臂带动哑铃朝面部上方及对侧斜向缓慢下放。",
                "下放至前臂接近与地面平行、充分拉伸肱三头肌时短暂停顿，避免上臂前后晃动。",
                "呼气收缩肱三头肌伸肘将哑铃沿原弧线推回肩部正上方起始位；每次屈肘下放与伸肘推回计一次。",
            ],
        },
        "0491": {
            "name_zh": "上斜板仰卧直腿举腿提臀",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors", "obliques"],
            "movement_patterns_zh": ["抗伸展", "核心稳定"],
            "required_equipment_zh": ["上斜训练凳"],
            "instructions_zh": [
                "仰卧在上斜训练凳上，头颈与上背部贴稳凳面，双手抓住身体两侧的凳架或垫边固定上身，双腿并拢伸直。",
                "收紧腹直肌使下背部贴向凳面，呼气将伸直的双腿向上方抬起。",
                "抬至双腿接近垂直后继续由下腹发力带动骨盆微幅卷起离开凳面，在最高点短暂停顿。",
                "吸气有控制地先放回骨盆再缓慢下放双腿至起始角度，全程避免下背借力反弓；每次举腿提臀与回落计一次。",
            ],
        },
        "0338": {
            "name_zh": "哑铃仰卧臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、上背与臀部贴紧凳面，双脚踩实地面，双手各持一只哑铃掌心相对垂直举于胸部上方。",
                "保持上臂稳定并固定在垂直或微向头顶倾斜角度，吸气屈肘将哑铃沿头部两侧向后下方缓慢降落。",
                "下放至前臂越过水平位、哑铃位于头部两侧时短暂停顿，感受肱三头肌长头拉伸。",
                "呼气由肱三头肌发力伸展肘关节将哑铃沿原轨迹推回起始位；每次下放与伸肘推回计一次。",
            ],
        },
        "0492": {
            "name_zh": "上斜爆发推起俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "delts", "abs"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "双手与肩同宽撑在稳固的平板训练凳边缘，前脚掌踩实地面作为固定支点，收紧核心与臀部使身体呈一条斜线。",
                "吸气屈肘将胸部有控制地降向凳面，蓄力保持躯干刚性不塌腰。",
                "呼气由胸大肌与肱三头肌爆发性发力推离凳面，使双手短暂腾空离开凳垫，双脚全程踩稳地面不离地。",
                "双手落回凳面时顺势屈肘缓冲衔接下一次动作；每次完成下放、爆发推起与缓冲落稳计一次。",
            ],
        },
        "0339": {
            "name_zh": "哑铃仰卧负重臀桥",
            "category": "upper legs",
            "equipment": "dumbbell",
            "target": "hamstrings",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "lower back"],
            "movement_patterns_zh": ["髋伸展", "髋铰链"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在地面或训练垫上，双膝弯曲、双脚平踩地面且与肩同宽，双手扶稳一只哑铃横放在髋部折痕处。",
                "收紧核心使骨盆微后倾，避免腰椎反弓代偿。",
                "呼气由腘绳肌与臀大肌协同发力脚跟蹬地，将髋部与哑铃向上顶起至肩、髋、膝呈一条斜线。",
                "在顶端夹紧臀部短暂停顿后，吸气有控制地将臀部缓慢下放回地面；每次顶髋与下放计一次。",
            ],
        },
        "0493": {
            "name_zh": "上斜俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "delts", "abs"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": ["稳固踏台"],
            "instructions_zh": [
                "双手以略宽于肩的间距撑在稳固踏台或跳箱顶面，双脚向后踩地，收紧核心与臀部使头、背、臀、腿成一条直线。",
                "吸气有控制地屈肘下放身体，上臂与躯干约呈45度夹角，直至胸部接近踏台边缘。",
                "在最低点短暂停顿，保持肩带稳定与腰背平直。",
                "呼气由胸大肌、三角肌前束与肱三头肌协同发力推回起始支撑位；每次下放与推起计一次。",
            ],
        },
        "0340": {
            "name_zh": "哑铃仰卧对握卧推",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "delts"],
            "movement_patterns_zh": ["水平推"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，肩胛骨收紧下沉贴实凳面，双脚平踩地面，双手各持哑铃以掌心相对的对握（锤式握）举于胸部正上方。",
                "吸气屈肘将哑铃沿胸部两侧缓慢下放，保持前臂垂直地面、上臂贴近躯干约呈45度角。",
                "下放至哑铃位于胸部两侧、充分拉伸胸大肌时短暂停顿。",
                "呼气由胸大肌与肱三头肌发力将哑铃垂直推回肩部正上方起始位；每次下放与推起计一次。",
            ],
        },
    }

    sources = {
        "0335": "https://www.muscleandstrength.com/exercises/dumbbell-lateral-to-front-raise.html",
        "0490": "https://exrx.net/WeightExercises/Triceps/BWInclineCloseGripPushup",
        "0337": "https://exrx.net/WeightExercises/Triceps/DBLyingTriExt",
        "0491": "https://exrx.net/WeightExercises/RectusAbdominis/BWInclineLegHipRaise",
        "0338": "https://exrx.net/WeightExercises/Triceps/DBLyingTriExt",
    }

    review_notes = {
        "0335": "核对哑铃侧平举转前平举四阶段轨迹（体侧起始→侧平举→水平前移→回展下放）与三角肌、斜方肌、胸大肌、前锯肌目标；原四帧经整数平移与下肢固定配准后双脚及小腿支点残差 0.0 px。",
        "0490": "修正上斜窄距俯卧撑窄握说明并补齐平板训练凳与高位支撑肩腰负荷标签；原图仅两姿往复且凳面跳动，重制四帧后训练凳与前脚掌支点残差 0.0 px。",
        "0337": "将原机械直译误名“哑铃平躺面朝下伸展”纠正为“哑铃仰卧横面臂屈伸”，补齐平板训练凳与过顶伸展负荷标签；原四帧经整数平移（F1 +8,0；F2 0,+32）配准后凳架与双脚支点残差 0.0 px。",
        "0491": "修正上斜板仰卧直腿举腿提臀名称与步骤，补齐上斜训练凳支撑并清除底边残影；原四帧经整数平移与凳架配准后上斜凳与头肩支点残差 0.0 px。",
        "0338": "将原误名“哑铃平躺肘推”按实际过顶屈肘轨迹纠正为“哑铃仰卧臂屈伸”，补齐平板训练凳与过顶伸展负荷标签；原四帧经整数平移（F1 +4,0；F2 0,+48）配准后凳架与双脚支点残差 0.0 px。",
    }

    pending = {
        "0489": "待修图 · 已纠正为罗马椅抱胸背屈伸并补带勾脚的下斜训练凳；原图罗马椅底座与脚踏在不同帧存在约 3%–4% 独立缩放（底座偏移 -19,+4 px 而脚踏偏移 -13,+7 px），内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
        "0492": "待修图 · 已纠正为上斜爆发推起俯卧撑并补平板训练凳；原图第 3 帧出现双脚完全离地悬空的解剖与支点错误，内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
        "0339": "待修图 · 已将机械直译“哑铃平躺股骨”纠正为“哑铃仰卧负重臀桥”；原图第 1 帧为直腿平躺而第 2、3 帧跳变为屈膝臀桥且全身整体上移 46 px，内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
        "0493": "待修图 · 已补齐稳固踏台与上斜俯卧撑步骤；原图仅包含顶姿与底姿两帧重复（缺少中间过渡帧），首版重制草稿双脚相对踏台仍下移 51 px 未达标，内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂不替换现有图。",
        "0340": "待修图 · 已纠正为哑铃仰卧对握卧推并补平板训练凳；原图第 1 帧与第 3 帧同为顶部伸肘姿（缺少半程过渡姿）且平凳上移 28 px，内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
    }

    result = {
        "batch": "20260921_review13",
        "version": "1.2.18",
        "version_code": 2026092101,
        "apk_name": "时光屋-1.2.18-第十三批动作复核.apk",
        "output": "build/review13-20260921",
        "report": "docs/releases/2026-09-21-review-batch13.md",
        "inspected": inspected,
        "definition_updates": definition_updates,
        "sources": sources,
        "review_candidates": review_candidates,
        "pending": pending,
        "registered_media": review_candidates,
        "original_pose_repairs": ["0335", "0337", "0491", "0338"],
        "generated_images_imported": 1,
        "image_generation_calls": 7,
        "quota_exhausted_reset_at": "2026-11-11T19:37:36Z",
        "review_notes": review_notes,
    }
    (B / "review-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    code_files = sorted(R.glob("app/src/main/java/**/*.java"))
    baseline = {str(p.relative_to(R)): sha(p) for p in code_files}
    (B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

    qa_spec = {
        "batch": "20260921_review13",
        "expected_checks": 22,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260921_review13")


if __name__ == "__main__":
    main()
