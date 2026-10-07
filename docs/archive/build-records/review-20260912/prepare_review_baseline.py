import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'app/src/main/assets/exercises_1324.json'
data=json.loads(p.read_text()); rows={r['id']:r for r in data['exercises']}
changes={
'0293':(['双脚站稳、膝盖微屈，双手各握哑铃，掌心相对。','从髋部向后折叠，保持背部中立、腹部收紧，手臂自然下垂。','保持躯干角度，肘部向后带动哑铃拉向腰侧；不耸肩、不转体。','控制下放回到起始位置。'],['拉','水平拉'],'upper back'),
'0294':(['站稳，双手持哑铃，掌心朝前，肘部靠近身体。','上臂保持稳定，屈肘将哑铃举至可控高度，手腕保持中立。','慢慢伸肘下放，不甩动身体或手臂。'],['肘屈'],'biceps'),
'1760':(['双脚约与肩同宽，双手托住一只哑铃，竖直放在胸前。','保持躯干稳定、全脚掌着地，屈髋屈膝下蹲，膝盖朝脚尖方向。','下蹲到能控制的深度，不强求最低点；哑铃始终贴近胸前。','脚掌均匀发力站起，保持膝盖稳定。'],['蹲','双腿蹲'],'glutes'),
'0662':(['双手略宽于肩，手掌和脚尖支撑，头到脚跟保持稳定直线。','屈肘下放身体，肘部斜向后方，避免向两侧过度张开。','胸部接近地面或降到可控深度后，推回起始位置；不塌腰、不耸肩。'],['推','水平推'],'triceps')}
refs={
'0293':'https://www.puregym.com/exercises/back/rows/dumbbell-bent-over-row/',
'0294':'https://www.mayoclinic.org/healthy-lifestyle/fitness/multimedia/biceps-curl/vid-20084675',
'1760':'https://www.nasm.org/resource-center/exercise-library/goblet-squat',
'0662':'https://www.nasm.org/resource-center/exercise-library/push-up'}
for xid,(steps,patterns,muscle) in changes.items():
 rows[xid]['instructions_zh']=steps
 rows[xid]['movement_patterns_zh']=patterns
 rows[xid]['muscle_group']=muscle
rows['1760']['name_zh']='哑铃杯式深蹲'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
baseline={'version':1,'dataset_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'reviewed':[],
 'pending':[{'id':'dataset_1324_0300','note':'待核逻辑 · 硬拉名称与髋铰链示范的变式需要进一步核对'},
 {'id':'dataset_1324_0289','note':'待核逻辑 · 卧推还需稳定卧推凳，当前器械筛选未单列支撑条件'}]}
for xid in changes:
 asset=root/'app/src/main/res/raw'/f'dataset_motion_{xid}.webp'
 baseline['reviewed'].append({'id':'dataset_1324_'+xid,'name':rows[xid]['name_zh'],
 'reviewed_at':'2026-09-13','reviewer':'AI逐项复核（本轮）','media_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),
 'note':'名称、器械、文字和四帧姿势已逐项核对；示范为分步阶段图，非连续实拍。', 'source':refs[xid]})
(root/'app/src/main/assets/exercise_reviews.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
print('reviewed',len(baseline['reviewed']),'other defaults remain unreviewed')
