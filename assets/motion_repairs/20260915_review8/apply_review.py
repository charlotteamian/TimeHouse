"""Stage reviewed edits first; approve only after recorded Android checks and visual review."""
from pathlib import Path
import json,hashlib,shutil,sys
from datetime import datetime
from zoneinfo import ZoneInfo
B=Path(__file__).resolve().parent;R=B.parents[2]
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=R/'app/src/main/assets/exercises_1324.json';l=R/'app/src/main/assets/exercise_reviews.json';sp=R/'assets/motion_repairs/review-workflow-state.json'
d=json.loads(p.read_text());ledger=json.loads(l.read_text());state=json.loads(sp.read_text());assert state['active_batch']['id']==B.name
sources={'0309':'https://www.strengthlog.com/dumbbell-front-raise/','0311':'https://library.theprehabguys.com/vimeo-video/scaption-raise-dumbbell-2-2/'}
new=['0309','0311']
if '--approve' in sys.argv:
 result=json.loads((B/'review-result.json').read_text());assert result['initial_validation']=='passed' and set(result['android_playback_visually_reviewed'])==set(new)
 assert len(json.loads((R/'build/review8-20260915/batch/ui-checks.json').read_text()))==15
 for xid in new:
  assert 'dataset_1324_'+xid not in {r['id'] for r in ledger['reviewed']}
  row=next(e for e in d['exercises'] if e['id']==xid)
  ledger['reviewed'].append({'id':'dataset_1324_'+xid,'name':row['name_zh'],'reviewed_at':'2026-09-15','reviewer':'AI逐项复核','media_sha256':hashlib.sha256((R/f'app/src/main/res/raw/dataset_motion_{xid}.webp').read_bytes()).hexdigest(),'source':sources[xid],'note':'已核对图文、肩部肌群、双侧计次、器械和肩部伤痛筛选；双脚跨帧固定，完整 Android 动态循环与训练选择通过。'+('原姿势仅修正整数平移。' if xid=='0309' else '内置 imagegen 一次生成加一次定向精修纠正肩胛平面和拇指朝上握法，按固定脚点封装；未使用插帧或混合帧。')})
 save(l,ledger);result['newly_reviewed']=['dataset_1324_'+x for x in new];save(B/'review-result.json',result);state['active_batch'].update(phase='release_validation',next_step='Verify final reviewed-only selection, covers, package and signature')
else:
 assert state['active_batch']['phase']=='inspection'
 updates={'0257':{'name_zh':'站姿膝部绕环'},'0258':{'name_zh':'时钟式俯卧撑'},'0260':{'muscle_group':''},'0267':{'muscle_group':''},'0306':{'muscle_group':'','required_equipment_zh':['下斜训练凳']},'0307':{'required_equipment_zh':['下斜训练凳']},'0308':{'muscle_group':'','required_equipment_zh':['平板训练凳']},'0309':{'name_zh':'哑铃双臂前平举','muscle_group':'','movement_patterns_zh':['肩屈曲','站姿稳定','辅助'],'instructions_zh':['双脚站稳，双手各持一只轻哑铃放在大腿前方，掌心朝向大腿。','保持腹部收紧、背部自然，肘部微屈并保持角度。','双臂同时向前举起至肩部高度，不耸肩或后仰甩起重量。','控制降回起点，一次举起和下放计一次，双脚全程保持原位。']},'0311':{'name_zh':'哑铃肩胛平面上举（拇指朝上）','muscle_group':'','movement_patterns_zh':['肩胛平面上举','站姿稳定','辅助'],'instructions_zh':['双脚站稳，双手各持轻哑铃在身体两侧，掌心朝向身体，肘部微屈。','双臂沿身体侧方略向前约三十至四十五度的方向同步举起，拇指带动向上，保持中立握法。','举至肩部高度即可，不耸肩、后仰或摆动身体。','控制沿原路径下放，一次举起和下放计一次，双脚保持固定。']}}
 pending={'0257':'待修图 · 脚掌支点与膝部绕环顺序尚未匹配，现有四帧主要表现向一侧摆动，未完整表现顺逆时针绕环。','0258':'待修图 · 示范混入单臂侧移姿势，身体朝向与手脚支点跨帧改变，尚不能匹配时钟式俯卧撑的绕行逻辑。','0260':'待核逻辑 · 已将髋屈肌从主肌群移至辅助；收拢时骨盆接触区域及躯干卷起幅度仍待确认，暂不按仅一个贴地区域授予通过。','0262':'待修图 · 原文要求双脚放地交替卷转，示范仅一侧屈膝抬腿且脚部、骨盆跨帧位置不同，变式与固定点仍需匹配。','0267':'待修图 · 抬起阶段从头后长臂变成向前伸手，脚位和骨盆关系变化，另有画面边缘残留，不能确认为同一长臂卷腹。','0306':'待修图 · 虽然凳脚与双脚可同时平移对齐，上臂仍大幅向头后摆动，尚不能确认肘伸展动作逻辑；已补必需下斜凳。','0307':'待修图 · 原图头高脚低，与下斜飞鸟定义相反，凳面和脚部也有位移；已补下斜训练凳条件。','0308':'待修图 · 部分脚点可对齐，但远侧凳脚被遮挡且形态不能可靠匹配，飞鸟最低点与支撑稳定仍需复核；已补平板训练凳。'}
 for row in d['exercises']:
  if row['id'] in updates:row.update(updates[row['id']])
 save(p,d)
 for xid in new:shutil.copy2(B/f'{xid}-fixed.webp',R/f'app/src/main/res/raw/dataset_motion_{xid}.webp')
 assert not ({'dataset_1324_'+x for x in pending}&{r['id'] for r in ledger['pending']})
 ledger['pending'] += [{'id':'dataset_1324_'+x,'note':note} for x,note in pending.items()];ledger['dataset_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();save(l,ledger)
 m=R/'app/src/main/AndroidManifest.xml';text=m.read_text();assert 'android:versionName="1.2.11"' in text;m.write_text(text.replace('android:versionName="1.2.11"','android:versionName="1.2.12"').replace('android:versionCode="2026091501"','android:versionCode="2026091502"'))
 result={'batch':B.name,'inspected':[e['id'] for e in json.loads((B/'selected.json').read_text())],'definition_updates':updates,'sources':sources,'additional_sources':{'0311':'https://www.acefitness.org/certifiednewsarticle/2660/a-commonsense-approach-to-addressing-shoulder-instability/'},'review_candidates':new,'newly_reviewed':[],'pending':pending,'registered_media':new,'original_pose_repairs':['0309'],'generated_images_imported':1,'image_generation_calls':2,'initial_validation':'pending','validation':'pending'};save(B/'review-result.json',result)
 state['active_batch'].update(phase='initial_validation',next_step='Verify both candidate animations, selected equipment, shoulder screening, counting and playback before approval')
 state['deferred_ids']+=['dataset_1324_'+x for x in pending]
 state['generation_attempts']['dataset_1324_0311'].update(result='candidate_under_validation',reason='Refinement corrected peak scaption plane; both feet align within 1 px after uniform frame translation')
state['last_updated']=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat();save(sp,state);print(state['active_batch']['phase'],len(ledger['reviewed']))
