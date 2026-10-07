"""Apply reviewed definitions and original-frame registration; approval is a separate gated step."""
from pathlib import Path
import json,hashlib,shutil,sys
from datetime import datetime
from zoneinfo import ZoneInfo
B=Path(__file__).resolve().parent;R=B.parents[2]
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=R/'app/src/main/assets/exercises_1324.json';l=R/'app/src/main/assets/exercise_reviews.json';s=R/'assets/motion_repairs/review-workflow-state.json'
d=json.loads(p.read_text());ledger=json.loads(l.read_text());state=json.loads(s.read_text())
assert state['active_batch']['id']==B.name
approved=['0287','0290','0253','0305']
sources={'0287':'https://www.puregym.com/exercises/arms-and-shoulders/shoulder-press/arnold-press/','0290':'https://www.muscleandstrength.com/exercises/seated-dumbbell-press.html','0253':'https://library.theprehabguys.com/vimeo-video/pull-up-neutral-grip/','0305':'https://www.muscleandfitness.com/exercise/workouts/shoulder-exercises/incline-dumbbell-shrug/'}
if '--approve' in sys.argv:
 result=json.loads((B/'review-result.json').read_text())
 assert result['initial_validation']=='passed' and set(result['android_playback_visually_reviewed'])==set(approved)
 assert len(json.loads((R/'build/review7-20260915/batch/ui-checks.json').read_text()))>=20
 assert hashlib.sha256(p.read_bytes()).hexdigest()==ledger['dataset_sha256']
 for xid in approved:
  assert 'dataset_1324_'+xid not in {r['id'] for r in ledger['reviewed']}
  e=next(e for e in d['exercises'] if e['id']==xid)
  note='已逐项核对名称、肌群、步骤、器械条件、计次及伤痛筛选；模拟器完整循环通过，保留动态封面和训练选择。'
  note+= ' 原有四帧仅作整数平移，双脚与两处凳脚同时对齐，残差不超过 2 px。' if xid in ['0287','0290'] else (' 原有四帧保持不变，架体与双手握点稳定；手腕随屈肘自然转动。' if xid=='0253' else ' 原有四帧保持不变，双脚和训练凳固定；图示为俯卧上斜耸肩，已纠正名称。')
  ledger['reviewed'].append(dict(id='dataset_1324_'+xid,name=e['name_zh'],reviewed_at='2026-09-15',reviewer='AI逐项复核',media_sha256=hashlib.sha256((R/f'app/src/main/res/raw/dataset_motion_{xid}.webp').read_bytes()).hexdigest(),source=sources[xid],note=note))
 ledger['pending']=[r for r in ledger['pending'] if r['id'] not in {'dataset_1324_'+x for x in approved}]
 save(l,ledger);result['newly_reviewed']=['dataset_1324_'+x for x in approved];save(B/'review-result.json',result)
 state['active_batch'].update(phase='release_validation',next_step='Build final ledger; verify reviewed-only training, dynamic covers, package and signature before release')
else:
 assert state['active_batch']['phase']=='inspection'
 updates={
 '0138':{'name_zh':'仰卧举髋卷腹','muscle_group':''},
 '0139':{'name_zh':'窄握引体向上'},
 '0140':{'name_zh':'引体向上'},
 '0287':{'muscle_group':'','movement_patterns_zh':['推','垂直推','过顶伸展'],'instructions_zh':['坐在稳固的直立靠背训练凳上，背部贴近靠背，双脚踩实地面；双手持哑铃在肩前，掌心朝向自己。','将肘部向两侧打开，随手臂展开把掌心转向前方，再将哑铃推向头顶；不要只拧动手腕。','推至可控制的高度，肘部不强行锁死，腹部收紧，不后仰借力。','控制降回肩部并反向转回掌心朝向自己的姿势，双脚和训练凳全程稳定。']},
 '0288':{'muscle_group':'','instructions_zh':['仰卧在稳固平板训练凳上，头背贴凳，双脚踩实地面。','双手稳握一只哑铃，举至胸部上方，肘部保持轻微弯曲。','保持肘角，在肩部可控制的范围内将哑铃沿弧线降向头后，不塌腰或弹震。','控制将哑铃带回胸部上方，重复动作。']},
 '0290':{'muscle_group':'','secondary_muscles':['triceps','traps'],'movement_patterns_zh':['推','垂直推','过顶伸展']},
 '0251':{'name_zh':'双杠臂屈伸（偏胸）','instructions_zh':['双手握住稳固双杠，手臂伸展使双脚离地，身体略微前倾。','控制屈肘下降至上臂约平行地面或肩部舒适的范围，不追求更深幅度。','保持握点稳定，用胸部和手臂发力推回起点，不弹起或耸肩借力。','重复动作；肩部出现疼痛时停止。']},
 '0253':{'target':'lats','muscle_group':'upper back','movement_patterns_zh':['拉','垂直拉'],'instructions_zh':['握住稳固引体架的窄距平行握把，掌心相对；双脚离地，腹部收紧。','先稳定肩胛，再屈肘将身体拉起，肘部向下靠近身体，双手始终握在原位。','上拉至下巴接近或超过握把所在横杆的高度，不伸颈或摆腿借力。','控制下降回到手臂伸展的位置，不塌腰；双臂同步完成一次上拉和下放计一次。']}}
 old=next(e for e in d['exercises'] if e['id']=='0304')
 updates['0305']={key:old[key] for key in ['muscle_group','movement_patterns_zh','instructions_zh']}
 updates['0305']['name_zh']='哑铃俯卧上斜凳耸肩（另一示范）'
 required={'0287':'直立靠背训练凳','0288':'平板训练凳','0290':'直立靠背训练凳','0291':'平板训练凳','0305':'上斜训练凳','0139':'单杠','0140':'单杠','0251':'双杠','0253':'中立握引体架'}
 for xid,name in required.items():updates.setdefault(xid,{})['required_equipment_zh']=[name]
 pending={'0138':'待修图 · 实际是仰卧举髋卷腹，已纠正倒立撑误名；头部与贴地手掌不能同时对齐，仍保持未复核。','0139':'待修图 · 单杠固定但双手握距跨帧改变，起始脚部贴近画面下边缘；握法与图示仍需统一，已补必需单杠。','0140':'待修图 · 单杠立柱和横杆跨帧改变位置、握距也变化，无法整体平移修复；已补必需单杠。','0288':'待修图 · 近侧凳脚与脚部横向位移接近零，远侧凳脚却移动约 22 px，不能同时固定；已补平板训练凳并纠正屈肘步骤。','0251':'待修图 · 双杠固定但双手沿杠移动，需固定握点；已纠正胸推误名、下降幅度和必需双杠。','0291':'待修图 · 训练凳与双脚独立移动，不能同时对齐；已补平板训练凳，保持触凳深蹲图文待修。'}
 for e in d['exercises']:
  if e['id'] in updates:e.update(updates[e['id']])
 save(p,d)
 for xid in ['0287','0290']:shutil.copy2(B/f'{xid}-fixed.webp',R/f'app/src/main/res/raw/dataset_motion_{xid}.webp')
 ledger['pending']=[r for r in ledger['pending'] if r['id'] not in {'dataset_1324_'+x for x in pending}]
 for xid,note in pending.items():ledger['pending'].append({'id':'dataset_1324_'+xid,'note':note})
 ledger['dataset_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();save(l,ledger)
 m=R/'app/src/main/AndroidManifest.xml';text=m.read_text();assert 'android:versionName="1.2.10"' in text;text=text.replace('android:versionName="1.2.10"','android:versionName="1.2.11"').replace('android:versionCode="2026091404"','android:versionCode="2026091501"');m.write_text(text)
 result={'batch':B.name,'inspected':[e['id'] for e in json.loads((B/'selected.json').read_text())],'definition_updates':updates,'sources':sources,'review_candidates':approved,'newly_reviewed':[],'pending':pending,'registered_media':['0287','0290'],'image_generation_calls':0,'initial_validation':'pending','validation':'pending'};save(B/'review-result.json',result)
 state['active_batch'].update(phase='initial_validation',next_step='Verify loaded definitions, required supports, training selection and full Android playback before approval')
 state['deferred_ids']=list(dict.fromkeys(state['deferred_ids']+['dataset_1324_'+x for x in pending]))
state['last_updated']=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat();save(s,state)
print('Saved phase:',state['active_batch']['phase'],'; reviewed:',len(ledger['reviewed']))
