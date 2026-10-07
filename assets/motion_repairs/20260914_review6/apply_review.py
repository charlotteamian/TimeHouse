from pathlib import Path
import json,hashlib,shutil
from datetime import datetime
from zoneinfo import ZoneInfo
B=Path(__file__).resolve().parent;R=B.parents[2]
updates={
'0003':{'name_zh':'自行车卷腹','muscle_group':'obliques'},
'0299':{'muscle_group':'','movement_patterns_zh':['推','肩外旋','过顶伸展'],'instructions_zh':['双脚站稳，双手各持轻哑铃，腹部收紧，上臂抬至肩部附近，肘部弯曲约九十度。','保持肘部位置，带动上臂做肩外旋，使前臂从朝前转向竖直向上；不是单独转动手腕。','在肩部可控制的范围内将哑铃推向头顶，不用后仰或耸肩借力。','先降回肩部，再反向旋转回起始姿势；使用轻重量，控制整个过程。']},
'0129':{'name_zh':'屈膝凳上臂屈伸','muscle_group':'','movement_patterns_zh':['推','伸肘'],'instructions_zh':['坐在稳固平板训练凳的边缘，双手扶在臀部两侧，双脚踩实地面，膝盖保持弯曲。','臀部移到凳子前方，背部靠近凳边，手掌和双脚的位置保持稳定。','控制屈肘使身体下降，肘部朝后；下到肩部舒适、上臂接近平行地面的位置即可，不追求更深幅度。','用手臂推起回到起点，避免耸肩或弹起；双腿全程屈膝，出现肩部疼痛时停止。']},
'0304':{'name_zh':'哑铃俯卧上斜凳耸肩','muscle_group':'','movement_patterns_zh':['拉','肩胛上提'],'instructions_zh':['将可调训练凳设为稳固的上斜角度，俯卧使胸腹贴住凳面，双脚在地面站稳。','双手各持一只哑铃自然下垂，手臂伸直，颈部保持自然，不抬头借力。','胸部继续贴凳，通过肩胛和肩部向上提起带动哑铃，不屈肘划船或移动训练凳。','短暂停顿后控制放低肩部，回到手臂自然下垂的位置，双脚和凳脚全程稳定。']}}
required={'0020':'平衡板','0301':'下斜训练凳','0129':'平板训练凳','0302':'下斜训练凳','0130':'平板训练凳','0303':'下斜训练凳','0304':'上斜训练凳','0292':'平板训练凳'}
for xid,name in required.items():updates.setdefault(xid,{})['required_equipment_zh']=[name]
sources={'0129':'https://www.nasm.org/resource-center/exercise-library/bench-dips','0304':'https://www.muscleandfitness.com/exercise/workouts/shoulder-exercises/incline-dumbbell-shrug/','0292':'https://www.puregym.com/exercises/back/rows/single-arm-dumbbell-row/','0299':'https://www.muscleandstrength.com/exercises/seated-cuban-press'}
pending={'0003':'待修图 · 自行车卷腹左右交替时骨盆与上背贴地区域不能稳定对应，侧向卷转和腿部交替仍需复核。','0299':'待修图 · 古巴推举原图底部残留其他帧内容，过顶帧人体比例与双脚位置变化；已纠正肩外旋步骤、模式和肩腰负荷。','0020':'待修图 · 已补平衡板为必需器械；板面随人体平移、站立脚与板支点关系仍需复核，不能当作普通无器械动作。','0301':'待修图 · 图示头高脚低，与下斜卧推头低脚高相反，凳脚与腿部漂移也不一致；需重制，已补下斜凳条件。','0302':'待修图 · 飞鸟图的远侧凳脚形态跨帧不同，虽然近侧凳脚与脚部平移接近，仍不能确认整个凳子固定；已补下斜凳条件。','0130':'待修图 · 凳上髋伸展的凳脚与脚部水平漂移相反，且图文变式仍需核对；已补平板训练凳条件。','0303':'待修图 · 下斜锤式推举中间帧近侧凳脚移 -22 px、远侧凳脚与脚部仅 -1 px，不能整体平移同时固定；已补下斜凳条件。','0137':'待修图 · 当前示范为凳上直腿臂屈伸，与 body-up 条目的具体变式尚未匹配；凳脚和脚部位移也不一致。'}
p=R/'app/src/main/assets/exercises_1324.json';d=json.loads(p.read_text())
for e in d['exercises']:
 if e['id'] in updates:e.update(updates[e['id']])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for xid in ['0129','0304']:shutil.copy2(B/f'{xid}-fixed.webp',R/f'app/src/main/res/raw/dataset_motion_{xid}.webp')
l=R/'app/src/main/assets/exercise_reviews.json';ledger=json.loads(l.read_text());approved=['0129','0304','0292'];ledger['pending']=[r for r in ledger['pending'] if r['id']!='dataset_1324_0292']
for xid in approved:
 assert 'dataset_1324_'+xid not in {r['id'] for r in ledger['reviewed']}
 e=next(e for e in d['exercises'] if e['id']==xid)
 ledger['reviewed'].append({'id':'dataset_1324_'+xid,'name':e['name_zh'],'reviewed_at':'2026-09-14','reviewer':'AI逐项复核','media_sha256':hashlib.sha256((R/f'app/src/main/res/raw/dataset_motion_{xid}.webp').read_bytes()).hexdigest(),'source':sources[xid],'note':'已核对动作变式、肌群、步骤、计次和完整四帧；多个支撑点残差不超过 2 px，必需训练凳作为额外条件参与训练筛选，保留动态循环。'})
for xid,note in pending.items():ledger['pending'].append({'id':'dataset_1324_'+xid,'note':note})
ledger['dataset_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();l.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
m=R/'app/src/main/AndroidManifest.xml';s=m.read_text();assert '1.2.9' in s;s=s.replace('android:versionName="1.2.9"','android:versionName="1.2.10"').replace('android:versionCode="2026091403"','android:versionCode="2026091404"');m.write_text(s)
r={'batch':B.name,'inspected':[r['id'] for r in json.loads((B/'selected.json').read_text())],'definition_updates':updates,'sources':sources,'newly_reviewed':['dataset_1324_'+x for x in approved],'pending':pending,'registered_media':['0129','0304'],'image_generation_calls':0,'validation':'pending'};(B/'review-result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
s=R/'assets/motion_repairs/review-workflow-state.json';state=json.loads(s.read_text());state['active_batch'].update(phase='validation',inspected_ids=r['inspected'],next_step='Validate required supports, review fingerprints, dynamic playback and training selection in 1.2.10');state['deferred_ids']=[x for x in state['deferred_ids'] if x!='dataset_1324_0292']+['dataset_1324_'+x for x in pending];state['last_updated']=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat();s.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print('Applied',len(updates),'definitions, 2 media repairs and 3 review candidates')
