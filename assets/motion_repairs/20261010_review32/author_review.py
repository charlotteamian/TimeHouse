#!/usr/bin/env python3
"""Author Batch 32 (20261010_review32) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["1366", "0438", "1367", "0439", "1374", "0660", "1377", "0727", "1386", "0777"]
    review_candidates = ["1367"]

    definition_updates = {
        "1366": {
            "name_zh": "上犬式",
            "category": "back",
            "equipment": "body weight",
            "target": "spine",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "chest", "abs"],
            "movement_patterns_zh": ["脊柱伸展"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "俯卧在训练垫上，双腿在身后自然伸直、脚背平贴垫面。",
                "双手掌心向下置于下肋骨两侧垫面，手指朝正前方。",
                "呼气掌根用力压地推直双臂，将胸廓、躯干与大腿一并温和抬离垫面仅以双手和脚背着地。",
                "主动沉肩向后展胸看向前上方，保持均匀呼吸片刻后再有控制地缓慢放回垫面；按次重复。",
            ],
        },
        "0438": {
            "name_zh": "坐姿哑铃外旋折臂推举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "chest", "core"],
            "movement_patterns_zh": ["推", "垂直推", "过顶伸展"],
            "required_equipment_zh": ["直立靠背训练凳"],
            "instructions_zh": [
                "稳坐在直立靠背训练凳上，背部贴实靠背、双脚平踩地面，双手正握各持一只哑铃举至肩高、大臂略外展呈双折臂姿态，掌心朝前。",
                "收紧腹部肋骨下压避免借腰过度反弓。",
                "呼气由三角肌发力沿斜上方弧线将两只哑铃一并向上推举至双臂接近伸直。",
                "在顶点短暂停顿后，吸气沿原外展轨道缓慢下放回到肩侧起始位；每次推回计一次。",
            ],
        },
        "1367": {
            "name_zh": "宽握颈后引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "forearms", "upper back"],
            "movement_patterns_zh": ["拉", "垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "面对单杠站立，采用明显宽于肩距的正手抓法握稳单杠横杆。",
                "双臂充分伸直自然下垂准备，下沉肩胛并收紧核心与双腿减少身体晃动。",
                "呼气由背阔肌与上背肌群协同发力下压手肘，有控制地将身体向上拉起至单杠横杆贴近颈后斜方上缘。",
                "在顶点短暂停顿保持背部收缩感，随后吸气控制速率缓慢放回双臂伸直位；每次完整拉放计一次。",
            ],
        },
        "0439": {
            "name_zh": "哑铃佐特曼弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然站直，双手各持一只哑铃自然垂于体侧、掌心向前方。",
                "锁定上臂稳定贴近躯干两侧不前后甩摆，挺胸收紧核心。",
                "呼气保持掌心向上由肱二头肌集中屈肘将哑铃弯举至肩前顶点，随后在最高位将前臂向内旋前转为掌心朝下。",
                "吸气保持反握掌心向下姿势缓慢有控制地放落哑铃回大腿前侧，到底部再旋回掌心朝前准备下一次；每次弯举下放计一次。",
            ],
        },
        "1374": {
            "name_zh": "单腿箱上落地稳定",
            "category": "lower legs",
            "equipment": "body weight",
            "target": "calves",
            "muscle_group": "",
            "secondary_muscles": ["quadriceps", "hamstrings", "glutes"],
            "movement_patterns_zh": ["下肢", "单侧稳定"],
            "required_equipment_zh": ["稳固踏台"],
            "instructions_zh": [
                "站在稳固踏台一侧，一脚稳踏地面或准备跨踩至踏台面上。",
                "收紧核心与髋膝稳定肌群，发力轻量跃起并以单脚稳稳踩落至稳固踏台中心（另一脚自然屈膝离地维持平衡）。",
                "落地瞬间保持膝关节微屈对齐脚尖方向不内扣，利用小腿与大腿力量稳定停住身体1至2秒。",
                "控制脚步放回地面完成单次稳定落箱；每侧完成规定次数后换另一腿。",
            ],
        },
        "0660": {
            "name_zh": "哑铃窄距俯卧撑",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["chest", "shoulders", "core"],
            "movement_patterns_zh": ["推", "水平推"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "将两只防滚哑铃近距离平行放置于肩前下方地面，双手紧握哑铃手柄、身体呈俯卧撑直线姿势。",
                "收紧腹臀避免塌腰或撅臀，肘窝微朝内维持手腕中立。",
                "吸气紧贴体侧缓慢向后下方屈肘放落胸口接近哑铃上缘。",
                "呼气由肱三头肌与胸肌集中发力推直双肘回到高位起始位；每次下放与推起计一次。",
            ],
        },
        "1377": {
            "name_zh": "扶墙弓步小腿拉伸",
            "category": "lower legs",
            "equipment": "body weight",
            "target": "calves",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "ankles"],
            "movement_patterns_zh": ["拉伸", "下肢"],
            "required_equipment_zh": ["墙面"],
            "instructions_zh": [
                "面对墙面站立，双手抬至与肩同高掌心扶实墙面。",
                "一脚向后迈开约一大步，保持后侧膝关节充分伸直且后脚脚跟全程踩实地面不翘起。",
                "吸气稳步屈曲前侧膝盖并顺势将重心轻轻前倾压向墙面，感受后侧小腿腓肠肌与跟腱清晰舒展。",
                "平稳呼吸维持拉伸20至30秒后回正起身并换另一条腿重复。",
            ],
        },
        "0727": {
            "name_zh": "单腿持哑铃站台提踵",
            "category": "lower legs",
            "equipment": "dumbbell",
            "target": "calves",
            "muscle_group": "",
            "secondary_muscles": ["ankles", "feet"],
            "movement_patterns_zh": ["下肢", "单侧提踵"],
            "required_equipment_zh": ["稳固踏台"],
            "instructions_zh": [
                "同侧手单手持一只哑铃自然垂于体侧，另一脚轻踏上稳固踏台前沿使前脚掌踩实台面、脚跟自然悬出外缘，对侧腿略屈膝离地。",
                "挺直躯干收紧核心维持侧面身体稳定不前后大幅晃动。",
                "吸气充分下放支撑侧脚跟至低于踏台水平感受小腿后侧充分牵伸，随后呼气由小腿肌发力推前脚掌垂直向上顶起脚跟至最高点。",
                "在顶峰收缩停顿片刻后有控制地缓缓下放还原；每侧完成规定次数后换另一腿。",
            ],
        },
        "1386": {
            "name_zh": "单腿扶墙提踵",
            "category": "lower legs",
            "equipment": "body weight",
            "target": "calves",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "glutes", "ankles"],
            "movement_patterns_zh": ["下肢", "单侧提踵"],
            "required_equipment_zh": ["墙面"],
            "instructions_zh": [
                "面对墙面或稳固横杆保持适当站距，双手平扶墙面与胸肩等高保持躯干前倾稳定。",
                "将非训练侧腿向后略微屈膝抬离地面，由工作腿全脚掌直立踩稳地面。",
                "呼气保持工作膝近乎伸直，由小腿肌群集中发力踩稳前脚掌尽力将脚跟垂直顶高。",
                "在最高点略作停顿后缓慢有控制地放落脚跟轻触地面；每侧完成规定次数后换另一腿。",
            ],
        },
        "0777": {
            "name_zh": "哑铃巫师式斜向摆举",
            "category": "waist",
            "equipment": "dumbbell",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "lower back", "shoulders"],
            "movement_patterns_zh": ["髋铰链", "核心旋转"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚略宽于髋站稳并保持膝盖微屈，双手上下叠握共同抓稳同一只哑铃手柄悬于身前一侧大腿外下前方。",
                "收紧核心与下背，保持脊柱中立随轻度屈髋转体动作发力。",
                "呼气由腹部、腹斜肌与肩臂协同带动哑铃沿对角斜线自一侧小腿外侧向上摆举至对侧肩上方高位。",
                "随后沿斜线有控制地回落至对侧外下方并交替向另一侧斜上方完成摆举；按左右交替规定次数执行。",
            ],
        },
    }

    sources = {
        "1367": "https://exrx.net/WeightExercises/LatissimusDorsi/BWRearPullup",
    }

    review_notes = {
        "1367": "纠正原上游错译“宽握反向引体向上”（易与水平俯身划船或反握混淆）为宽握颈后引体向上，明确 `单杠` 必需支撑器械并重写单杠横杆标准要点；原图第 0 帧经 `(0, +3)`、第 1 帧经 `(+16, +3)` 纯整数平移与第 2 帧对齐后门架上下左右四角全部精确重合（残差 `0.0 px`，匹配分 `≥ 0.9887`），无顶底边缘截断（前景留存 100%）。",
    }

    pending = {
        "1366": "待修图 · 已规范上犬式呼吸伸展与核心控制要点；原图第 2 帧右下边缘 `x=479` 残留黑点杂影，且第 1、2 帧躯干与手撑位置横跳、无固定支点对齐，暂存待重制。",
        "0438": "待修图 · 已补充 `直立靠背训练凳` 必需器械与过顶推举肩负核查，更名为坐姿哑铃外旋折臂推举；原图第 1、2 帧座椅支腿静止但上半身头胸相对于凳背垂向整体下沉达 `12–13 px`（`head sc=0.7268`），暂存待重制。",
        "0439": "待修图 · 已纠正Literal错译“哑铃佐特曼卷”为哑铃佐特曼弯举并规范上下交替旋前步骤；原图第 1 帧在 `(+22, 0)` 下肢重合时头部 `head_face` 错位达 `1 px`（`sc=0.9392`），调至 `(+23, 0)` 则 `calves_knees sc=0.9463`，未同时满足多支点 `≥ 0.96` 门槛，暂存待重制。",
        "1374": "待修图 · 已补充 `稳固踏台` 并规范单腿箱上落地稳定四步要点（自动激活单腿计次）；原图三帧中箱体与人像左右大幅跃迁、尺寸变化且出现 `y=0/479` 裁断，暂存待重制。",
        "0660": "待修图 · 已调整手握地面哑铃顺序并规范为哑铃窄距俯卧撑；原图哑铃锚点与双脚位置存在不同步横移与纵跳（`feet dy=+38` 对 `dumbbells dy=+34, dx=-6`），暂存待重制。",
        "1377": "待修图 · 已补充 `墙面` 必需支持并明确弓步后脚伸直跟落地要点；原图三帧头部顶部贴顶边 `y=0` 持续被裁断且扶墙深度与步距横移，暂存待重制。",
        "0727": "待修图 · 已纠正“on a dumbbell”歧义名称为单腿持哑铃站台提踵并补充 `稳固踏台`（保留单腿计次）；原图第 1 帧在踏台仅差 `1 px` 时上身整体前滑 `3.16 px`（`head res=3.16 px, sc=0.8569`）且第 2 帧头发顶贴 `y=0`，暂存待重制。",
        "1386": "待修图 · 已纠正上游将“bar”误译为“酒吧”并规范为单腿扶墙提踵与 `墙面` 支持；原图第 1 帧头发触顶 `y=0` 裁断、前脚掌相对墙面发生 `3–4 px` 异步滑动，暂存待重制。",
        "0777": "待修图 · 已纠正原步骤错写“单手握持伸向另侧手”为双手共持同一只哑铃斜向摆举并命名哑铃巫师式斜向摆举；原图第 2 帧顶边 `y=0` 残留游离哑铃碎块且画面放大导致双脚于 `y=479` 裁切，暂存待重制。",
    }

    result = {
        "batch": "20261010_review32",
        "version": "1.2.37",
        "version_code": 2026101001,
        "apk_name": "时光屋-1.2.37-第三十二批动作复核.apk",
        "output": "build/review32-20261010",
        "report": "docs/releases/2026-10-10-review-batch32.md",
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
        "batch": "20261010_review32",
        "expected_checks": 10,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261010_review32")


if __name__ == "__main__":
    main()
