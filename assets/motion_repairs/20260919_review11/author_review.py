"""Persist batch 11 manually inspected decisions; does not approve the ledger."""
import json, hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

B = Path(__file__).resolve().parent
R = B.parents[2]

def save(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

rear_fly_instructions = [
    '将上斜训练凳调节至约四十五度，俯卧趴在凳面上，胸部贴紧靠背，双脚踩实地面。',
    '双手各持一只哑铃，自然垂于肩部下方，掌心相对或朝向后方，肘部保持微屈。',
    '保持躯干贴紧凳面，三角肌后束发力将双臂向身体两侧水平抬起，直至上臂与地面接近平行。',
    '在动作顶点稍作停顿并感受后束收缩，随后控制哑铃沿原路径缓慢降回起点；一次抬起与下放计一次。'
]

updates = {
    '0326': dict(
        name_zh='哑铃俯卧上斜后侧平举',
        movement_patterns_zh=['水平外展', '俯身稳定', '辅助'],
        required_equipment_zh=['上斜训练凳'],
        instructions_zh=rear_fly_instructions
    ),
    '0467': dict(
        name_zh='大猩猩引体向上',
        movement_patterns_zh=['垂直拉', '核心稳定'],
        required_equipment_zh=['单杠']
    ),
    '0323': dict(
        name_zh='哑铃上斜单臂侧平举',
        movement_patterns_zh=['外展', '单侧', '辅助'],
        required_equipment_zh=['上斜训练凳']
    ),
    '0469': dict(
        name_zh='仰卧开髋卷腹',
        movement_patterns_zh=['躯干屈曲', '核心']
    ),
    '0324': dict(
        name_zh='哑铃上斜掌心相对推举',
        movement_patterns_zh=['推', '双臂推举', '辅助'],
        required_equipment_zh=['上斜训练凳']
    ),
    '0471': dict(
        name_zh='靠墙倒立俯卧撑',
        movement_patterns_zh=['垂直推', '倒立稳定'],
        required_equipment_zh=['墙面']
    ),
    '0325': dict(
        name_zh='哑铃上斜肩部推举',
        movement_patterns_zh=['垂直推', '辅助'],
        required_equipment_zh=['上斜训练凳']
    ),
    '0472': dict(
        name_zh='悬挂直腿抬腿',
        movement_patterns_zh=['核心屈曲', '悬挂稳定'],
        required_equipment_zh=['单杠']
    ),
    '0473': dict(
        name_zh='悬挂直腿V字屈体',
        movement_patterns_zh=['核心屈曲', '悬挂稳定'],
        required_equipment_zh=['单杠']
    ),
    '0327': dict(
        name_zh='哑铃俯卧上斜划船',
        movement_patterns_zh=['水平拉', '俯身稳定'],
        required_equipment_zh=['上斜训练凳']
    ),
}

pending = {
    '0467': '待修图 · 引体架横梁高度与立柱形态随帧改变，双手握距在起始帧较窄、最高点变宽，腿部动作在顶点不够连贯。已纠正猩猩下巴误名，补齐单杠需求。',
    '0323': '待修图 · 初始准备帧与后续动作帧之间，训练凳前脚朝向与橡胶脚套透视发生大幅突变（由左侧突变到右侧），双脚与凳脚无法通过整体平移对齐；补齐上斜凳需求。',
    '0469': '待修图 · 起始帧头部与脚部紧贴甚至超出左侧边界（x=0截断）；第2/3帧下放时地面留有漂移残影黑斑；躯干与骨盆接地支点大幅漂移。纠正主肌群为腹部。',
    '0324': '待修图 · 最高点推举顶点哑铃冲至最顶部边界（y=0）；训练凳后脚在动作展开时向左延伸2px，而前脚向右漂移，支点呈非刚体形变；已补齐上斜凳需求。',
    '0471': '待修图 · 头部下落时双手手掌沿地面向两侧外滑漂移超过 20 px，双掌支撑距离跨帧变化，无法作为刚性固定支点；已补齐墙面需求与肩颈伤痛筛选。',
    '0325': '待修图 · 起始帧哑铃垂于大腿侧，中间帧突变至肩部推举准备位，最高点推举冲出顶部边界（y=0）；四处凳脚与足部存在不一致位移。补齐上斜凳条件。',
    '0472': '待修图 · 龙门架左侧斜撑在中间帧完全消失，左右立柱孔洞位置在帧间独立形变，立柱支点不稳；已补齐单杠需求与核心动作模式。',
    '0473': '待修图 · 引体架左上角斜撑在动作中间帧消失，立柱孔洞与底座形态改变，两处握点随身体摆动发生形变；纠正劈叉误名为悬挂直腿屈体，补齐单杠需求。',
    '0327': '待修图 · 训练凳后底座支撑架在动作进行时形状改变（由小三角连接延伸为覆盖脚底的长构件），无法以刚体平移消除漂移；已补齐上斜凳需求与水平拉动作模式。',
}

sources = {
    '0326': 'https://www.strengthlog.com/reverse-dumbbell-flyes/'
}

notes = {
    '0326': '纠正后侧平举为俯卧上斜后侧平举，补齐上斜训练凳条件与水平外展模式；原四帧通过整数平移校准，后凳脚、前凳脚与地面足部残差均为 0 px，匹配度 >= .963，胸部贴凳与双臂对称性核对通过。'
}

r = dict(
    batch=B.name,
    version='1.2.16',
    version_code=2026091901,
    apk_name='时光屋-1.2.16-第十一批动作复核.apk',
    output='build/review11-20260919',
    report='docs/releases/2026-09-19-review-batch11.md',
    inspected=[x['id'] for x in json.loads((B / 'selected.json').read_text())],
    definition_updates=updates,
    sources=sources,
    review_candidates=['0326'],
    newly_reviewed=[],
    pending=pending,
    registered_media=['0326'],
    original_pose_repairs=['0326'],
    generated_images_imported=0,
    image_generation_calls=0,
    initial_validation='pending',
    validation='pending',
    review_notes=notes
)

save(B / 'review-result.json', r)
save(B / 'qa-spec.json', dict(
    expected_checks=20,
    runner='scripts/qa_review_batch11.py',
    candidates=r['review_candidates'],
    visual_gate='Inspect saved Android loops before approving; unreviewed training remains blocked under 1.2.14 rules'
))

s = R / 'assets/motion_repairs/review-workflow-state.json'
state = json.loads(s.read_text())
state['status'] = 'manual_batch'
state['last_updated'] = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
state['active_batch']['next_step'] = 'Stage corrected definitions and media; validate candidates while unreviewed, then approve and package once'
save(s, state)

save(B / 'code-baseline.json', {
    str(p.relative_to(R)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in (R / 'app/src').rglob('*')
    if p.is_file() and (p.suffix == '.java' or '/res/layout/' in str(p))
})
print('Saved batch 11 review-result.json and qa-spec.json')
