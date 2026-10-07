"""Apply this manually reviewed batch; evidence remains in this directory."""
from pathlib import Path
import hashlib,json,shutil
from datetime import datetime
from zoneinfo import ZoneInfo
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
UPDATES={
'1427':{'name_zh':'侧卧单腿髋外展','secondary_muscles':['core'],'movement_patterns_zh':['下肢','髋外展','单腿'],'instructions_zh':[
'侧躺，双腿伸直叠放，下侧手臂托住头，上侧手掌轻放在身前地面，肩和髋上下对齐。',
'腹部收紧，保持下侧腿贴地，上侧腿从髋部向上抬起，膝盖伸直，脚尖朝前。',
'只抬到骨盆仍能稳定的位置，不翻髋、后仰或追求抬得越高越好。',
'控制上侧腿落回，身体和下侧支点保持稳定；做完规定次数后换另一侧，左右各做。']},
'0298':{'name_zh':'哑铃单臂交叉锤式弯举','muscle_group':'brachialis','movement_patterns_zh':['拉','屈肘'],'instructions_zh':[
'双脚站稳，双手各持一只哑铃垂在身体两侧，掌心朝向身体。',
'保持躯干直立、肘部靠近身体，一侧屈肘，把哑铃斜向举到对侧胸肩前，手腕保持中立。',
'短暂停顿后控制降回原处，避免甩动身体或用肩部提拉借力，另一只手的哑铃保持下垂。',
'示范展示单侧动作；同侧完成规定次数后换臂，一组左右各做。']},
'0001':{'name_zh':'四分之三仰卧起坐','muscle_group':''},
'0292':{'muscle_group':'lats','movement_patterns_zh':['拉','水平拉','俯身稳定'],'instructions_zh':[
'一手持哑铃，另一手扶稳固的训练凳；双脚踩实地面，前后错开，屈髋俯身。',
'腹部收紧，背部保持自然平直，让持铃手臂向下伸展，肩部不要松垮。',
'将肘部向后拉向髋部，使哑铃靠近腰侧；躯干和骨盆不旋转借力。',
'控制手臂伸展回到起点，支撑手、训练凳和双脚保持稳定；完成规定次数后换侧。']},
'0295':{'name_zh':'哑铃翻举'},
'0296':{'name_zh':'哑铃窄握卧推','movement_patterns_zh':['推','水平推'],'instructions_zh':[
'双手各持一只哑铃，躺在稳定的平板训练凳上，双脚踩实地面，肩背和臀部贴稳凳面。',
'掌心相对，哑铃靠近胸部中央，肘部靠近躯干，手腕保持中立。',
'将两只哑铃向胸部正上方推起，控制伸肘，不用腰部过度拱起借力。',
'缓慢屈肘将哑铃降回胸前，保持窄握和稳定的肩部位置；全程为仰卧推举。']},
'0297':{'name_zh':'哑铃单臂集中弯举'},
}
PENDING={
'0001':'待核逻辑 · 已修复第三帧上浮 20 px、纠正仰卧起坐名称；四分之三变式的起止范围仍需匹配原始教练示范，图片修复不等于完整复核。',
'0292':'待核逻辑 · 图示双脚及训练凳基本稳定，已补充扶凳步骤并纠正主肌群；训练选材尚未完整表达额外训练凳条件，暂不授予复核。',
'1428':'待修图 · 头部、双脚固定，但四帧仅显示手腕往返位置，未展示完整画圈，着色在上臂而非手腕前臂，需修复动作方向及着色。',
'0295':'待修图 · 已将 clean 纠正为翻举；接铃屈髋屈膝阶段不清晰、腿部比例与脚位变化，现有阶段图不足以核对翻举的发力与接铃逻辑。',
'3016':'待修图 · 卷起帧脚部和臀部位移分别约 (-13,-79) 与 (-21,-77) px，不能整帧平移同时固定。',
'0296':'待修图 · 已纠正为哑铃窄握卧推并补齐仰卧步骤；现图误画成坐姿过顶推举，动作方向及变式不符，需重制；还需训练凳条件。',
'0297':'待修图 · 已明确单臂计次；中间帧左右脚水平漂移相差约 6 px，凳脚形态也变化，需同时修复人和凳；额外训练凳条件待核对。',
'0002':'待修图 · 最大侧弯时双脚水平漂移分别约 -2 与 +11 px，不能用整帧平移同时固定。',
}
SOURCES={
'1427':'https://www.acefitness.org/resources/everyone/exercise-library/38/side-lying-hip-abduction/',
'0298':'https://www.muscleandfitness.com/exercise/workouts/arm-exercises/cross-body-dumbbell-hammer-curl/',
'0292':'https://www.puregym.com/exercises/back/rows/single-arm-dumbbell-row/',
'0295':'https://www.crossfit.com/essentials/foundational-movement-clean-what-is-a-clean',
'0296':'https://www.muscleandstrength.com/exercises/close-grip-dumbbell-press.html',
'0002':'https://www.nhs.uk/live-well/exercise/flexibility-exercises/',
}
source=ROOT/'app/src/main/assets/exercises_1324.json';data=json.loads(source.read_text())
for e in data['exercises']:
 if e['id'] in UPDATES:e.update(UPDATES[e['id']])
source.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
for xid in ['1427','0298','0001']:shutil.copy2(HERE/f'{xid}-fixed.webp',ROOT/f'app/src/main/res/raw/dataset_motion_{xid}.webp')
ledgerp=ROOT/'app/src/main/assets/exercise_reviews.json';ledger=json.loads(ledgerp.read_text())
for xid in ['1427','0298']:
 full='dataset_1324_'+xid
 assert full not in {r['id'] for r in ledger['reviewed']}
 name=UPDATES[xid]['name_zh'];media=ROOT/f'app/src/main/res/raw/dataset_motion_{xid}.webp'
 ledger['reviewed'].append({'id':full,'name':name,'reviewed_at':'2026-09-14','reviewer':'AI逐项复核','media_sha256':hashlib.sha256(media.read_bytes()).hexdigest(),'note':'逐项核对名称、器械、肌群、步骤、动作模式及左右各做计次；用整帧偏移修正固定点漂移，多个支撑点残差不超过 2 px，保留原四帧及 2.36 秒动态循环。','source':SOURCES[xid]})
for xid,note in PENDING.items():
 assert 'dataset_1324_'+xid not in {r['id'] for r in ledger['pending']}
 ledger['pending'].append({'id':'dataset_1324_'+xid,'note':note})
ledger['dataset_sha256']=hashlib.sha256(source.read_bytes()).hexdigest();ledgerp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
manifest=ROOT/'app/src/main/AndroidManifest.xml';s=manifest.read_text();assert 'android:versionName="1.2.8"' in s;s=s.replace('android:versionName="1.2.8"','android:versionName="1.2.9"').replace('android:versionCode="2026091402"','android:versionCode="2026091403"');manifest.write_text(s)
result={'batch':HERE.name,'inspected':[e['id'] for e in json.loads((HERE/'selected.json').read_text())],'definition_updates':UPDATES,'sources':SOURCES,'source_gaps':{'0001':'Original Bodybuilding.com 3/4 sit-up source was unavailable; variant range remains unapproved.'},'newly_reviewed':['dataset_1324_1427','dataset_1324_0298'],'pending':PENDING,'registered_media':['1427','0298','0001'],'validation':'pending','image_generation_calls':0,'deferred_generation_reason':'Prior squat/TRX failures have no new repair strategy in this batch; existing frame registration provided useful repairs.'}
(HERE/'review-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
statep=ROOT/'assets/motion_repairs/review-workflow-state.json';state=json.loads(statep.read_text());state['active_batch'].update(phase='validation',next_step='Build and validate 1.2.9, especially per-side timing, reviewed filters and three repaired animations');state['deferred_ids']+=['dataset_1324_'+x for x in PENDING];state['last_updated']=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat();statep.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
print('Applied 7 definition updates, 3 registered animations, 2 review candidates and 8 pending reasons')
