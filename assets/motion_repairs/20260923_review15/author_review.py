#!/usr/bin/env python3
"""Author Batch 15 (20260923_review15) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0499", "0346", "0500", "0347", "0501", "0348", "0507", "0349", "0508", "0350"]
    review_candidates = ["0499", "0346", "0347", "0348", "0349", "0508", "0350"]

    definition_updates = {
        "0499": {
            "name_zh": "低杠反向划船",
            "category": "back",
            "equipment": "body weight",
            "target": "upper back",
            "muscle_group": "",
            "secondary_muscles": ["lats", "biceps", "delts", "forearms"],
            "movement_patterns_zh": ["水平拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "将低位单杠或力量架横杆设置在齐腰高度，仰卧于横杆正下方，双手以与肩同宽的正握抓牢横杆，双脚脚跟撑稳地面。",
                "收紧核心与臀部使头、肩、髋、膝与脚跟呈一条挺直斜线，双臂完全伸直悬垂作为起始位。",
                "呼气由上背斜方肌、菱形肌、背阔肌与肱二头肌协同发力屈肘，将胸部拉向横杆并向内收紧肩胛骨。",
                "在胸口接近横杆处短暂停顿，吸气有控制地伸肘下放身体回到直臂悬垂位；每次拉起与下放计一次。",
            ],
        },
        "0346": {
            "name_zh": "哑铃仰卧单臂反握臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "delts"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、背、臀贴实凳面，双脚平踩地面，训练手以反握（掌心朝向面部方向）持一只哑铃垂直举于肩部正上方。",
                "锁定上臂垂直地面不前后摆动，吸气以肘关节为轴缓慢屈肘，将哑铃沿头部同侧向后下方降落。",
                "下放至前臂越过水平位、充分拉伸肱三头肌时短暂停顿。",
                "呼气由肱三头肌发力伸肘将哑铃沿原弧线推回肩部正上方起始位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0500": {
            "name_zh": "左右移动俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["delts", "triceps", "core"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双手以明显宽于肩的间距撑稳地面，前脚掌踩实地面，收紧核心与臀部使头、躯干与双腿保持一条直线。",
                "吸气屈肘将胸部降至接近地面高度，先将上身重心水平移向一侧手掌上方，对侧手臂随之伸展。",
                "保持双掌与双脚支点原位不动、胸部维持低位高度，发力控制身体经过正中水平平移至另一侧手掌上方。",
                "再将重心平滑移回对侧或正中完成往复移动，全程避免塌腰或摆臀；每次完整左右平移往复计一次。",
            ],
        },
        "0347": {
            "name_zh": "哑铃俯卧平凳前臂旋前弯举",
            "category": "lower arms",
            "equipment": "dumbbell",
            "target": "forearms",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "brachialis"],
            "movement_patterns_zh": ["腕屈伸", "俯身稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "俯卧在稳固的平板训练凳上，胸腹部贴稳凳面，双脚向后踩地固定下身，双手各持一只哑铃自然垂于肩部下方，起始掌心朝后。",
                "保持上臂与躯干稳定不动，呼气屈肘向前上方抬起前臂，同时前臂内旋使掌心转为朝下。",
                "抬至前臂约呈45度、充分收紧旋前圆肌与前臂伸屈肌群时短暂停顿。",
                "吸气有控制地边还原前臂旋转边缓慢下放哑铃回到垂直悬垂位；每次屈肘旋前与还原计一次。",
            ],
        },
        "0501": {
            "name_zh": "开合波比跳",
            "category": "cardio",
            "equipment": "body weight",
            "target": "cardiovascular system",
            "muscle_group": "",
            "secondary_muscles": ["quadriceps", "hamstrings", "calves", "delts", "triceps", "core"],
            "movement_patterns_zh": ["全身多关节", "爆发力"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然站立，屈髋屈膝下蹲并将双手撑在身前地面上。",
                "双脚向后跳出落成直臂支撑位并顺势完成一次俯卧撑（可结合双脚开合跳一次），保持核心收紧不塌腰。",
                "双脚迅速向前跳回双手外侧成深蹲预备姿。",
                "紧接着由下肢爆发蹬地垂直向上跳起，同时双臂向头顶上方伸展，落地时屈膝缓冲回到起始位；每次完整循环计一次。",
            ],
        },
        "0348": {
            "name_zh": "哑铃俯卧平凳后束飞鸟",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平拉", "俯身稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "俯卧在稳固的平板训练凳上，胸部贴实凳垫前端，双腿分开向两侧踩稳地面，双手对握各持一只哑铃自然垂于肩部正下方。",
                "保持肘关节微屈固定角度、肩带下沉不耸肩，呼气由三角肌后束与中下斜方肌发力带动双臂向两侧上方横向展开。",
                "外展至上臂与地面平行、肩胛骨适度内收时短暂停顿。",
                "吸气有控制地将哑铃沿原弧线缓慢下放回肩部下方起始位；每次展开与下放计一次。",
            ],
        },
        "0507": {
            "name_zh": "折刀仰卧起坐",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors", "obliques"],
            "movement_patterns_zh": ["抗伸展", "核心稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双腿并拢伸直，双臂向头顶后方伸直贴近耳侧，收紧核心使下背部贴稳垫面。",
                "呼气由腹直肌与髋屈肌协同发力，以臀部为固定支点同时向上抬起伸直的双腿与上身。",
                "在最高点让身体折成 V 字形、双手向前触碰或接近脚尖，短暂停顿。",
                "吸气有控制地同步缓慢下放上身与双腿回到仰卧伸展起始位；每次折叠起身与还原计一次。",
            ],
        },
        "0349": {
            "name_zh": "哑铃仰卧平凳前臂旋后弯举",
            "category": "lower arms",
            "equipment": "dumbbell",
            "target": "forearms",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "brachialis"],
            "movement_patterns_zh": ["腕屈伸"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、背、臀贴实凳面，双脚分开踩稳地面，双手各持一只哑铃垂于体侧下方。",
                "保持上臂贴近躯干两侧稳定不动，呼气屈肘向上弯举前臂，同时前臂积极外旋（旋后）使小指侧向上翻转。",
                "继续弯举至哑铃接近肩部前方、肱二头肌与旋后肌群充分收缩时短暂停顿。",
                "吸气有控制地边还原前臂旋后角度边缓慢下放哑铃回到体侧下垂位；每次弯举旋后与下放计一次。",
            ],
        },
        "0508": {
            "name_zh": "扬达仰卧起坐",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "hamstrings"],
            "movement_patterns_zh": ["核心稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在地面或训练垫上，双膝弯曲约90度，双脚脚掌平踩地面，双手轻扶耳侧且手肘朝外。",
                "全程主动用脚跟向后下方蹬地发力收紧腘绳肌与臀部，通过交互抑制减少髂腰肌代偿。",
                "呼气单纯依靠腹直肌收缩将头、肩与上背部逐节卷离地面至躯干约成45度，骨盆与双脚保持稳固不移动。",
                "在顶端短暂停顿后，吸气有控制地将上身逐节放回垫面；每次卷起与放回计一次。",
            ],
        },
        "0350": {
            "name_zh": "哑铃仰卧平凳弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、上背与臀部紧贴凳面，双脚平踩地面，双手掌心朝前各持一只哑铃自然垂于体侧。",
                "收紧肩胛骨并锁定上臂在体侧位置不向前摆动，呼气由肱二头肌发力屈肘将哑铃向上弯举。",
                "弯举至哑铃到达肩部上方、肱二头肌完全收缩时短暂停顿。",
                "吸气有控制地缓慢伸肘将哑铃沿原弧线下放回体侧悬垂起始位，感受肱二头肌长头拉伸；每次弯举与下放计一次。",
            ],
        },
    }

    sources = {
        "0499": "https://exrx.net/WeightExercises/BackGeneral/BWSupineRow",
        "0346": "https://exrx.net/WeightExercises/Triceps/DBOneArmLyingTriExt",
        "0347": "https://exrx.net/WeightExercises/Pronators/DBLyingPronation",
        "0348": "https://exrx.net/WeightExercises/DeltoidPosterior/DBLyingRearLateralRaise",
        "0349": "https://exrx.net/WeightExercises/Supinators/DBLyingSupination",
        "0508": "https://www.muscleandstrength.com/exercises/janda-sit-up.html",
        "0350": "https://exrx.net/WeightExercises/Biceps/DBSupineCurl",
    }

    review_notes = {
        "0499": "规范低杠反向划船名称与四步动作说明，补齐单杠支撑器械；原四帧经整数平移（F1 -12,-1；F2 -3,-1）与深蹲架立柱底座配准后双支点残差 0.0 px。",
        "0346": "纠正原英译中误译（supinated 应为反握而非正握）为“哑铃仰卧单臂反握臂屈伸”，补齐平板训练凳与过顶伸展标签；原四帧经整数平移（F1 +2,0；F2 0,+28）与平凳下肢配准后双支点残差 0.0 px。",
        "0347": "将原机械直译“哑铃平躺旋前”规范为“哑铃俯卧平凳前臂旋前弯举”，补齐平板训练凳与俯身稳定标签；原四帧经整数平移（F1 -18,0；F2 0,+1）与凳腿下肢配准后双支点残差 0.0 px。",
        "0348": "将原“哑铃平躺后侧平举”规范为“哑铃俯卧平凳后束飞鸟”，补齐平板训练凳与俯身稳定标签；原四帧经整数平移（F1 +1,0）与中央凳柱底座配准后双支点残差 0.0 px。",
        "0349": "将原“哑铃平躺旋后”规范为“哑铃仰卧平凳前臂旋后弯举”，补齐平板训练凳支撑器械；原四帧经整数平移（F2 0,+20）与平凳下肢配准后双支点残差 0.0 px。",
        "0508": "将原音译“贾达仰卧起坐”规范为标准康复训练名“扬达仰卧起坐”，补齐脚跟蹬地抑制屈髋代偿要点；原四帧经整数平移（F1 +21,0；F2 +16,+6）与下肢支点配准后双支点残差 0.0 px。",
        "0350": "将原重复译名“哑铃平躺仰卧弯举”规范为“哑铃仰卧平凳弯举”，补齐平板训练凳支撑器械；原四帧经整数平移（F2 0,+20）与平凳下肢配准后双支点残差 0.0 px。",
    }

    pending = {
        "0500": "待修图 · 已规范左右移动俯卧撑说明并补高位支撑标签；原图双手间距在不同帧缩放 30 px 且双脚相对手掌反向漂移 83 px（非刚性剪切变形），内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
        "0501": "待修图 · 已规范为开合波比跳并补齐动作步骤；原图仅包含蹲撑→俯卧撑→腾空跳 3 帧（返回时从空中直接跳变至地面俯卧撑且人物比例缩放约 40%），内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
        "0507": "待修图 · 已规范折刀仰卧起坐说明并补抗伸展与核心稳定标签；原图臀部支点在折叠起身时存在非刚性形态与尺度跳变（匹配分 0.8126 < 0.96），内置生图模型配额将于 2026-11-11T19:37:36Z 恢复，暂存待重制。",
    }

    result = {
        "batch": "20260923_review15",
        "version": "1.2.20",
        "version_code": 2026092301,
        "apk_name": "时光屋-1.2.20-第十五批动作复核.apk",
        "output": "build/review15-20260923",
        "report": "docs/releases/2026-09-23-review-batch15.md",
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
        "batch": "20260923_review15",
        "expected_checks": 28,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260923_review15")


if __name__ == "__main__":
    main()
