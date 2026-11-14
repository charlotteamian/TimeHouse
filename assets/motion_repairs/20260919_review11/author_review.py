"""Persist batch 11 manually inspected decisions for all 10 exercises; does not approve the ledger."""
import json
import hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

B = Path(__file__).resolve().parent
R = B.parents[2]


def save(p: Path, d: dict) -> None:
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


updates = {
    "0467": dict(
        name_zh="反握悬挂举腿引体",
        target="abs",
        muscle_group="",
        secondary_muscles=["lats", "biceps", "hip flexors", "forearms"],
        movement_patterns_zh=["垂直拉", "核心屈曲"],
        required_equipment_zh=["单杠"],
        instructions_zh=[
            "双手反握单杠，握距与肩同宽，身体自然悬垂，双膝微屈并收紧核心。",
            "屈肘向上拉起身体的同时屈髋抬膝，使下巴接近或超过单杠、双膝抬向胸前。",
            "在最高点短暂停顿，感受腹直肌、背阔肌与肱二头肌协同收缩，避免身体前后晃动。",
            "有控制地同步伸臂并下放双腿回到起始悬垂姿态；每次完整上拉与还原计一次。",
        ],
    ),
    "0323": dict(
        name_zh="哑铃上斜单臂侧平举",
        target="delts",
        muscle_group="",
        secondary_muscles=["traps", "forearms"],
        movement_patterns_zh=["外展", "单侧", "辅助"],
        required_equipment_zh=["上斜训练凳"],
        instructions_zh=[
            "将上斜训练凳调节至约四十五度，侧身或斜靠在靠背上，双脚踩稳地面，非工作手扶稳大腿支撑躯干。",
            "工作手持一只哑铃自然垂于身体侧下方，掌心朝向身体，肘部保持微屈固定。",
            "保持躯干稳定不耸肩，三角肌中束发力将哑铃沿身体侧方向外抬起，直至手臂约与地面平行。",
            "在顶点稍作停顿后控制哑铃沿原路径缓慢下放；单侧按目标次数完成后换另一侧，每侧一次抬起与下放计一次。",
        ],
    ),
    "0469": dict(
        name_zh="仰卧分腿屈膝卷腹",
        target="abs",
        muscle_group="",
        secondary_muscles=["hip flexors", "inner thighs"],
        movement_patterns_zh=["躯干屈曲", "核心"],
        required_equipment_zh=[],
        instructions_zh=[
            "仰卧在地面或训练垫上，双膝弯曲并向两侧适度分开，双脚全脚掌稳踩地面，双手轻扶耳侧。",
            "呼气收紧腹直肌，带动头肩与上背向上卷起，使胸廓向骨盆方向靠近，下背部与双脚全程保持贴地稳定。",
            "在腹肌充分收缩处短暂停顿，避免双手抱头硬拉颈部或抬脚借力。",
            "吸气有控制地放回上背至起始位置；每次上卷并还原计一次。",
        ],
    ),
    "0324": dict(
        name_zh="哑铃上斜掌心相对推举",
        target="pectorals",
        muscle_group="",
        secondary_muscles=["shoulders", "triceps"],
        movement_patterns_zh=["推", "双臂推举", "辅助"],
        required_equipment_zh=["上斜训练凳"],
        instructions_zh=[
            "将上斜训练凳调节至约三十至四十五度，仰卧躺稳，上背与臀部贴紧凳面，双脚踩实地面。",
            "双手各持一只哑铃举于上胸两侧，全程保持掌心相对的中立对握，大臂与躯干呈约四十五度夹角。",
            "胸大肌上束与三角肌前束发力，将哑铃向胸骨上方垂直推起至双臂接近伸直，腕关节保持中立。",
            "在顶点稍作停顿后控制哑铃缓慢下放至上胸两侧；一次推起与下放计一次。",
        ],
    ),
    "0471": dict(
        name_zh="靠墙倒立俯卧撑",
        target="delts",
        muscle_group="",
        secondary_muscles=["triceps", "chest", "core"],
        movement_patterns_zh=["垂直推", "高位支撑", "核心抗伸展"],
        required_equipment_zh=["墙面"],
        instructions_zh=[
            "背对墙面双手撑地，双掌间距略宽于肩并全程固定在同一地面支撑点，双脚踩墙成倒立支撑，收紧腹臀避免塌腰。",
            "吸气有控制地屈肘下放身体，使头顶平稳向地面方向下降，双肘保持约四十五度轨迹且手掌不向外滑动。",
            "下放至头顶接近地面时短暂停顿，保持颈部中立，严禁以头顶砸地承重。",
            "呼气由三角肌与肱三头肌发力推地，将身体垂直推回肘关节伸直的倒立支撑位；每次下放并推起计一次。",
        ],
    ),
    "0325": dict(
        name_zh="哑铃上斜肩部推举",
        target="delts",
        muscle_group="",
        secondary_muscles=["chest", "triceps", "traps"],
        movement_patterns_zh=["垂直推", "辅助"],
        required_equipment_zh=["上斜训练凳"],
        instructions_zh=[
            "将上斜训练凳调至高位约六十至七十五度，坐稳后上背与臀部贴紧靠背，双脚踩实地面。",
            "双手各握一只哑铃举至肩部外侧准备位，掌心朝前，前臂近似垂直地面。",
            "核心收紧，三角肌与上胸协同发力将哑铃向头顶正上方推起，直至双臂接近伸直但不强行锁死肘部。",
            "控制哑铃沿原路径缓慢下放回肩部高度的起始位；一次推起与下放计一次。",
        ],
    ),
    "0472": dict(
        name_zh="悬挂直腿抬腿",
        target="abs",
        muscle_group="",
        secondary_muscles=["hip flexors", "forearms", "lats"],
        movement_patterns_zh=["核心屈曲", "悬挂稳定"],
        required_equipment_zh=["单杠"],
        instructions_zh=[
            "双手正握单杠，握距与肩同宽或略宽，双臂伸直自然悬垂，肩带下沉稳定，双腿伸直并拢。",
            "呼气收紧腹直肌与屈髋肌群，保持双膝伸直，将双腿向身体前方平稳抬起至与地面平行。",
            "在水平顶点短暂停顿并主动后倾骨盆挤压下腹，避免依靠身体前后摆动借力。",
            "吸气有控制地将双腿缓慢下放回垂直悬垂起点；一次抬起与下放计一次。",
        ],
    ),
    "0326": dict(
        name_zh="哑铃俯卧上斜后侧平举",
        target="delts",
        muscle_group="",
        secondary_muscles=["traps", "rhomboids"],
        movement_patterns_zh=["水平外展", "俯身稳定", "辅助"],
        required_equipment_zh=["上斜训练凳"],
        instructions_zh=[
            "将上斜训练凳调节至约四十五度，俯卧趴在凳面上，胸部贴紧靠背，双脚踩实地面。",
            "双手各持一只哑铃，自然垂于肩部下方，掌心相对或朝向后方，肘部保持微屈。",
            "保持躯干贴紧凳面，三角肌后束发力将双臂向身体两侧水平抬起，直至上臂与地面接近平行。",
            "在动作顶点稍作停顿并感受后束收缩，随后控制哑铃沿原路径缓慢降回起点；一次抬起与下放计一次。",
        ],
    ),
    "0473": dict(
        name_zh="悬挂直腿折刀举腿",
        target="abs",
        muscle_group="",
        secondary_muscles=["hip flexors", "lats", "forearms"],
        movement_patterns_zh=["核心屈曲", "悬挂稳定"],
        required_equipment_zh=["单杠"],
        instructions_zh=[
            "双手正握单杠，双臂伸直悬垂，收紧肩带与核心，双腿并拢伸直垂向地面。",
            "呼气先将伸直的双腿向上抬起经过水平位，同时继续卷动骨盆向上折体，使脚背朝单杠方向高抬。",
            "在双脚接近单杠的高折刀顶点短暂停顿，充分收缩腹直肌，避免大幅甩动借力。",
            "吸气控制核心张力，将双腿沿原轨迹经水平位缓慢下放回垂直悬垂起点；每次高抬并还原计一次。",
        ],
    ),
    "0327": dict(
        name_zh="哑铃俯卧上斜划船",
        target="upper back",
        muscle_group="",
        secondary_muscles=["lats", "biceps", "shoulders", "forearms"],
        movement_patterns_zh=["水平拉", "俯身稳定", "辅助"],
        required_equipment_zh=["上斜训练凳"],
        instructions_zh=[
            "将上斜训练凳调至约三十至四十五度，俯卧趴在凳面上，胸部贴稳靠背，前脚掌踩实地面支撑身体。",
            "双手各持一只哑铃自然垂于肩部正下方，掌心相对，肩胛骨自然前引伸展。",
            "保持胸部贴紧凳面不抬头挺腰，中上背与背阔肌发力带动双肘向后上方拉起哑铃，在顶点夹紧肩胛骨。",
            "在顶点稍作停顿后，控制哑铃沿原路径缓慢下放回起始伸展位；一次拉起与下放计一次。",
        ],
    ),
}

sources = {
    "0467": "https://www.muscleandstrength.com/exercises/gorilla-chin.html",
    "0323": "https://www.muscleandstrength.com/exercises/incline-one-arm-dumbbell-lateral-raise.html",
    "0469": "https://www.muscleandstrength.com/exercises/crunch.html",
    "0324": "https://www.muscleandstrength.com/exercises/neutral-grip-incline-dumbbell-bench-press.html",
    "0471": "https://www.muscleandstrength.com/exercises/handstand-push-up.html",
    "0325": "https://www.muscleandstrength.com/exercises/seated-dumbbell-press.html",
    "0472": "https://www.muscleandstrength.com/exercises/hanging-leg-raise.html",
    "0326": "https://www.strengthlog.com/reverse-dumbbell-flyes/",
    "0473": "https://www.crossfit.com/essentials/the-toes-to-bar",
    "0327": "https://www.muscleandstrength.com/exercises/chest-supported-dumbbell-row.html",
}

notes = {
    "0467": "纠正猩猩下巴机翻误名为反握悬垂举腿引体，补齐单杠需求；重绘同画风反握引体配合屈膝抬腿四帧闭环，左右立柱底座与双手握点残差 0.0 px，匹配度 1.0。",
    "0323": "核对哑铃上斜单臂侧平举，补齐上斜训练凳条件与单侧计次说明；原四帧前后凳脚与双脚四处固定支撑残差 0.0 px，匹配度 >= 0.9978。",
    "0469": "纠正腹股沟卷腹误名为仰卧分腿屈膝卷腹；重绘并固定骨盆、分腿屈膝与双脚踩地支撑，消除脚尖越界与地面黑斑，骨盆与足部残差 0.0 px，匹配度 >= 0.9995。",
    "0324": "核对哑铃上斜掌心相对推举，补齐上斜训练凳条件；下移最高点帧恢复顶部白边并固定下肢与底座，四处支撑残差 0.0 px，匹配度 1.0。",
    "0471": "核对靠墙倒立俯卧撑，补齐墙面需求与高位支撑筛选；修复双手随屈肘向外滑移问题，墙面与双掌撑地点残差 0.0 px，匹配度 1.0。",
    "0325": "纠正哑铃上斜推举为哑铃上斜肩部推举，补齐上斜训练凳条件；重绘肩高起始→半程推起→过顶锁定→半程回落四帧闭环，四处底座与足部残差 0.0 px，匹配度 1.0。",
    "0472": "核对悬挂直腿抬腿，补齐单杠需求与核心屈曲模式；原四帧左右立柱底座与双手握点残差 0.0 px，匹配度 >= 0.9899。",
    "0326": "纠正后侧平举为哑铃俯卧上斜后侧平举，补齐上斜训练凳条件与水平外展模式；原四帧经整数平移校准后前后凳脚与足部残差 0.0 px，匹配度 >= 0.9643。",
    "0473": "纠正悬挂劈叉机翻误名为悬挂直腿折刀举腿，补齐单杠需求；重绘赤足垂直悬垂→水平举腿→高折刀举腿触杠→水平回落四帧闭环，立柱底座与握点残差 0.0 px，匹配度 >= 0.998。",
    "0327": "纠正上斜划船为哑铃俯卧上斜划船，补齐上斜训练凳条件与水平拉模式；原四帧经整数平移校准后双脚与前后凳脚残差 <= 1.0 px，匹配度 >= 0.9613。",
}

inspected = [x["id"] for x in json.loads((B / "selected.json").read_text(encoding="utf-8"))]

r = dict(
    batch=B.name,
    version="1.2.16",
    version_code=2026091901,
    apk_name="时光屋-1.2.16-第十一批动作复核.apk",
    output="build/review11-20260919",
    report="docs/releases/2026-09-19-review-batch11.md",
    inspected=inspected,
    definition_updates=updates,
    sources=sources,
    review_candidates=inspected,
    newly_reviewed=[],
    pending={},
    registered_media=inspected,
    original_pose_repairs=["0323", "0324", "0326", "0327", "0472"],
    remade_media=["0325", "0467", "0469", "0471", "0473"],
    generated_images_imported=5,
    image_generation_calls=14,
    initial_validation="pending",
    validation="pending",
    review_notes=notes,
)

save(B / "review-result.json", r)
save(
    B / "qa-spec.json",
    dict(
        expected_checks=37,
        runner="scripts/qa_review_batch11.py",
        candidates=r["review_candidates"],
        visual_gate="Inspect saved Android loops before approving; unreviewed training remains blocked under 1.2.14 rules",
    ),
)

s = R / "assets/motion_repairs/review-workflow-state.json"
state = json.loads(s.read_text(encoding="utf-8"))
state["status"] = "manual_batch"
state["last_updated"] = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat()
state["active_batch"]["next_step"] = "Stage corrected definitions and media; validate candidates while unreviewed, then approve and package once"
save(s, state)

save(
    B / "code-baseline.json",
    {
        str(p.relative_to(R)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (R / "app/src").rglob("*")
        if p.is_file() and (p.suffix == ".java" or "/res/layout/" in str(p))
    },
)
print("Saved batch 11 review-result.json and qa-spec.json for all 10 exercises")
