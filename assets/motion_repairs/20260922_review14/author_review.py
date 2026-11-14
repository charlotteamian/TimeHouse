#!/usr/bin/env python3
"""Author Batch 14 (20260922_review14) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0494", "0341", "0495", "0342", "0496", "0343", "0497", "0344", "0498", "0345"]
    review_candidates = ["0341", "0342", "0496", "0343", "0497", "0344", "0498"]

    definition_updates = {
        "0494": {
            "name_zh": "上斜反握俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "biceps", "delts", "abs"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "双手以反握（手指朝向脚尖方向、掌根朝前）与肩同宽撑在稳固的平板训练凳边缘，双脚向后踩地，收紧核心与臀部使身体呈一条斜线。",
                "吸气屈肘并让双肘贴近躯干两侧向后滑动，有控制地将胸部向凳面方向下放。",
                "下放至胸部接近凳面边缘时短暂停顿，保持肩带下沉与腰背平直不塌腰。",
                "呼气由胸大肌、肱三头肌与三角肌前束协同发力推回起始支撑位；每次下放与推起计一次。",
            ],
        },
        "0341": {
            "name_zh": "哑铃俯卧平凳单臂后束提拉",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平拉", "俯身稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "俯卧在稳固的平板训练凳上，胸部、腹部与骨盆贴稳凳垫，双脚向后踩实地面，非训练手扶住凳面保持稳定，训练手持哑铃掌心朝内自然下垂。",
                "保持躯干与头部贴稳凳面不扭转，呼气由三角肌后束与中下斜方肌发力，带动训练手沿体侧向后上方提拉。",
                "提拉至上臂接近与躯干平齐并挤压肩胛骨时短暂停顿，避免耸肩或腰部反弓借力。",
                "吸气有控制地将哑铃沿原轨迹缓慢下放回肩部正下方；单侧完成规定次数后换另一侧。",
            ],
        },
        "0495": {
            "name_zh": "勾脚下斜板转体仰卧起坐",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "hip flexors"],
            "movement_patterns_zh": ["核心旋转", "核心稳定"],
            "required_equipment_zh": ["带勾脚的下斜训练凳"],
            "instructions_zh": [
                "坐在下斜训练凳上，将双脚脚背卡紧在滚轴垫下方，屈膝躺下，双手轻扶耳侧或抱于胸前。",
                "吸气准备，呼气由腹直肌与腹内外斜肌协同发力卷起上背部离开凳面。",
                "在起身同时将躯干向一侧旋转，使对侧手肘朝前上方膝盖方向靠近，在最高点短暂停顿。",
                "吸气有控制地还原躯干旋转并缓慢下放回下斜凳面，下一次起身转向另一侧；每次卷起转体与还原计一次。",
            ],
        },
        "0342": {
            "name_zh": "哑铃仰卧单臂对握卧推",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "delts", "core"],
            "movement_patterns_zh": ["水平推"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、上背与臀部贴实凳面，双脚分开踩稳地面，非训练手轻扶腹部或凳缘，训练手以对握（掌心朝向身体中线）持哑铃停在胸部外侧。",
                "收紧核心与肩胛骨对抗单侧偏载，呼气由胸大肌与肱三头肌发力将哑铃垂直向上推起。",
                "推至手臂在肩部正上方完全伸展锁定，保持上背与对侧臀部紧贴凳面不翻转。",
                "吸气有控制地屈肘让上臂贴近躯干约呈45度缓慢下放回胸侧起始位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0496": {
            "name_zh": "平凳俯卧屈膝腿弯举",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "hamstrings",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "calves"],
            "movement_patterns_zh": ["膝屈曲", "俯身稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "俯卧在稳固的平板训练凳上，髋部贴在凳面末端边缘，双腿向后水平伸直悬空，双手抓牢前方凳腿固定上身。",
                "收紧核心与臀部使骨盆贴稳凳垫，避免腰椎反弓代偿。",
                "呼气由腘绳肌发力屈膝，将小腿与脚跟朝臀部方向向上弯举至膝关节超过90度。",
                "在顶端夹紧大腿后侧短暂停顿后，吸气有控制地伸膝还原至双腿水平伸直位；每次弯举与伸展计一次。",
            ],
        },
        "0343": {
            "name_zh": "哑铃仰卧单臂卧推",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "delts", "core"],
            "movement_patterns_zh": ["水平推"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、上背与臀部紧贴凳面，双脚平踩地面，非训练手放于体侧辅助稳定，训练手以正握（掌心朝向脚侧）持哑铃置于肩胸外侧。",
                "收紧肩胛骨与核心肌群防止躯干向负重侧倾倒，呼气由胸大肌与肱三头肌协同发力将哑铃向上推起。",
                "推至肩部正上方肘部伸展但不过度锁死，在顶点短暂停顿。",
                "吸气有控制地屈肘将哑铃缓慢下放回胸部外侧起始位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0497": {
            "name_zh": "宽握低杠反向划船",
            "category": "back",
            "equipment": "body weight",
            "target": "upper back",
            "muscle_group": "",
            "secondary_muscles": ["lats", "biceps", "delts", "forearms"],
            "movement_patterns_zh": ["水平拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "将低位单杠或史密斯机横杆固定在齐腰高度，仰卧于横杆下方，双手以略宽于肩的正握抓牢横杆，双脚脚跟撑地。",
                "收紧核心与臀部，使头、肩、髋、膝与脚跟呈一条挺直斜线，双臂完全伸展作为起始位。",
                "呼气由上背斜方肌、菱形肌、三角肌后束与肱二头肌发力屈肘，将上胸部拉向横杆并夹紧肩胛骨。",
                "在胸口接近横杆处短暂停顿，吸气有控制地伸肘下放身体回到直臂悬垂斜线位；每次拉起与下放计一次。",
            ],
        },
        "0344": {
            "name_zh": "哑铃仰卧单臂正握臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、背、臀贴稳凳面，双脚踩实地面，训练手以正握（手背朝向头部方向）持一只哑铃垂直举于肩部正上方。",
                "锁定上臂垂直地面不前后晃动，吸气以肘关节为轴缓慢屈肘，让哑铃沿头部同侧向后下方降落。",
                "下放至前臂越过水平位、充分拉伸肱三头肌时短暂停顿。",
                "呼气由肱三头肌发力伸肘将哑铃沿原弧线推回肩部正上方起始位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0498": {
            "name_zh": "悬挂带反向划船",
            "category": "back",
            "equipment": "body weight",
            "target": "upper back",
            "muscle_group": "",
            "secondary_muscles": ["lats", "biceps", "delts", "forearms"],
            "movement_patterns_zh": ["水平拉"],
            "required_equipment_zh": ["TRX 悬挂带"],
            "instructions_zh": [
                "确认 TRX 悬挂带锚点稳固，面向锚点双手握紧把手，双脚向前迈出并以脚跟撑地，身体后倾使双臂伸直、头肩髋踝呈一条直线。",
                "下沉肩带并收紧核心与臀部，防止划船过程中耸肩或塌腰掉髋。",
                "呼气由上背肌群与肱二头肌发力屈肘向后拉动，将胸部拉向双手把手之间并收紧肩胛骨。",
                "在顶端短暂停顿后，吸气有控制地伸展双臂还原至起始后倾悬垂位；每次拉起与还原计一次。",
            ],
        },
        "0345": {
            "name_zh": "哑铃俯卧平凳单臂后束飞鸟",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平拉", "俯身稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "俯卧在稳固的平板训练凳上，胸腹部贴实凳垫，双脚踩地稳定下肢，非训练手扶稳凳腿，训练手持哑铃自然下垂于肩部正下方。",
                "保持肘部微屈固定角度，呼气由三角肌后束与菱形肌发力将手臂向身体外侧上方横向展开。",
                "外展至上臂与地面大致平行、感受肩后束充分收缩时短暂停顿，避免耸肩。",
                "吸气有控制地沿原弧线缓慢下放回肩部下方起始位；单侧完成规定次数后换另一侧。",
            ],
        },
    }

    sources = {
        "0341": "https://exrx.net/WeightExercises/DeltoidPosterior/DBLyingRearDeltRow",
        "0342": "https://exrx.net/WeightExercises/PectoralSternal/DBOneArmBenchPress",
        "0496": "https://exrx.net/WeightExercises/Hamstrings/BWLyingLegCurl",
        "0343": "https://exrx.net/WeightExercises/PectoralSternal/DBOneArmBenchPress",
        "0497": "https://exrx.net/WeightExercises/BackGeneral/BWSupineRow",
        "0344": "https://exrx.net/WeightExercises/Triceps/DBOneArmLyingTriExt",
        "0498": "https://exrx.net/WeightExercises/BackGeneral/STSupineRow",
    }

    review_notes = {
        "0341": "将原机械直译“哑铃平躺单臂后三角”纠正为“哑铃俯卧平凳单臂后束提拉”，补齐平板训练凳与俯身稳定负荷标签；原四帧经整数平移（F1 +2,0；F2 +1,+31）与凳腿下肢锁定配准后支点残差 0.0 px。",
        "0342": "将原“哑铃平躺单臂推举（第二式）”按实际对握轨迹纠正为“哑铃仰卧单臂对握卧推”，补齐平板训练凳并重排为胸侧底姿→半程→顶端锁定→半程连贯循环，双支点残差 0.0 px。",
        "0496": "将原“反向腿弯举（凳支撑）”规范为“平凳俯卧屈膝腿弯举”，补齐平板训练凳与俯身稳定负荷标签；原四帧经整数平移（F1 +12,0；F2 +18,+43）与凳架上身锁定配准后双支点残差 0.0 px。",
        "0343": "将原“哑铃平躺单臂推举”规范为“哑铃仰卧单臂卧推”，与 0342 对握变式区分并补齐平板训练凳；原四帧经整数平移（F1 +15,0；F2 0,+15）与平凳下肢配准后双支点残差 0.0 px。",
        "0497": "将原“反向划船（第二式）”按宽握固定低杠动作规范为“宽握低杠反向划船”，补齐单杠支撑器械；原四帧经整数平移（F1 +1,0；F2 0,+20）与立柱底座配准后双支点残差 0.0 px。",
        "0344": "纠正原英译中误译（pronated 应为正握而非反握）为“哑铃仰卧单臂正握臂屈伸”，补齐平板训练凳与过顶伸展负荷标签；原四帧经整数平移与平凳配准后双支点残差 0.0 px。",
        "0498": "将原错译“反向划船带带”纠正为“悬挂带反向划船”，补齐 TRX 悬挂带必需器械；原四帧经整数平移（F1 -2,0）与立柱锚点配准后双支点残差 0.0 px。",
    }

    pending = {
        "0494": "待修图 · 已规范上斜反握俯卧撑步骤并补平板训练凳与高位支撑标签；原图第 3 帧身体沉入凳面且脚尖与训练凳存在 13 px 非刚性相对漂移，内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
        "0495": "待修图 · 已纠正为勾脚下斜板转体仰卧起坐并补带勾脚的下斜训练凳；原图仅展示单侧转体且勾脚滚轴与下斜凳底脚存在非刚性相对漂移，内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
        "0345": "待修图 · 已规范为哑铃俯卧平凳单臂后束飞鸟并补平板训练凳；原图第 2 帧手臂向左后摆而第 3 帧突变为向右前伸至头下（方向矛盾约 120 度），内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
    }

    result = {
        "batch": "20260922_review14",
        "version": "1.2.19",
        "version_code": 2026092201,
        "apk_name": "时光屋-1.2.19-第十四批动作复核.apk",
        "output": "build/review14-20260922",
        "report": "docs/releases/2026-09-22-review-batch14.md",
        "inspected": inspected,
        "definition_updates": definition_updates,
        "sources": sources,
        "review_candidates": review_candidates,
        "pending": pending,
        "registered_media": review_candidates,
        "original_pose_repairs": review_candidates,
        "generated_images_imported": 0,
        "image_generation_calls": 0,
        "quota_exhausted_reset_at": "2026-11-11T19:37:36Z",
        "review_notes": review_notes,
    }
    (B / "review-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    code_files = sorted(R.glob("app/src/main/java/**/*.java"))
    baseline = {str(p.relative_to(R)): sha(p) for p in code_files}
    (B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

    qa_spec = {
        "batch": "20260922_review14",
        "expected_checks": 28,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260922_review14")


if __name__ == "__main__":
    main()
