#!/usr/bin/env python3
"""Stage a manually authored batch; approve only after matching Android and visual evidence."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse,json,hashlib,shutil,re
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('batch');p.add_argument('action',choices=['stage','approve']);a=p.parse_args()
B=R/'assets/motion_repairs'/a.batch
if B.parent != R/'assets/motion_repairs':raise SystemExit('Invalid batch path')
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=load(B/'review-result.json');sp=R/'assets/motion_repairs/review-workflow-state.json';s=load(sp);assert s['active_batch']['id']==a.batch==r['batch']
dp=R/'app/src/main/assets/exercises_1324.json';lp=R/'app/src/main/assets/exercise_reviews.json';d=load(dp);l=load(lp);rows={e['id']:e for e in d['exercises']};new=r['review_candidates'];out=R/r['output']
assert set(new).isdisjoint(r['pending']) and set(new)|set(r['pending'])==set(r['inspected'])
assert len(new)==len(set(new)) and all(x in rows and r['sources'][x].startswith('https://') for x in new)
assert sha(dp)==l['dataset_sha256'] and r['image_generation_calls']<=2 and r['generated_images_imported']<=1
if a.action=='stage':
 assert s['active_batch']['phase']=='inspection' and sha(dp)==sha(B/'before/exercises_1324.json') and sha(lp)==sha(B/'before/exercise_reviews.json')
 assert set(r['definition_updates'])<=set(r['inspected']) and not any('dataset_1324_'+x in {e['id'] for e in l['reviewed']} for x in r['inspected'])
 for x in r['registered_media']:
  assert x in r['inspected'] and (B/f'{x}-fixed.webp').is_file()
 for x,patch in r['definition_updates'].items():rows[x].update(patch)
 save(dp,d)
 for x in r['registered_media']:shutil.copy2(B/f'{x}-fixed.webp',R/f'app/src/main/res/raw/dataset_motion_{x}.webp')
 l['pending']=[e for e in l['pending'] if e['id'] not in {'dataset_1324_'+x for x in r['pending']}]+[{'id':'dataset_1324_'+x,'note':note} for x,note in r['pending'].items()]
 l['dataset_sha256']=sha(dp);save(lp,l)
 m=R/'app/src/main/AndroidManifest.xml';text=m.read_text();text,n=re.subn(r'android:versionName="[^"]+"',f'android:versionName="{r["version"]}"',text);assert n==1;text,n=re.subn(r'android:versionCode="[^"]+"',f'android:versionCode="{r["version_code"]}"',text);assert n==1;m.write_text(text)
 s['deferred_ids']=list(dict.fromkeys(s['deferred_ids']+['dataset_1324_'+x for x in r['pending']]))
 s['active_batch'].update(phase='initial_validation',next_step='Run batch Android checks and visually inspect full loops before writing approval evidence')
else:
 assert s['active_batch']['phase']=='initial_validation'
 proof=load(B/'initial-validation.json');assert proof['status']=='passed' and set(proof['visually_reviewed'])==set(new)
 assert proof['dataset_sha256']==sha(dp) and proof['media_sha256']=={x:sha(R/f'app/src/main/res/raw/dataset_motion_{x}.webp') for x in new}
 checks=load(out/'batch/ui-checks.json');assert len(checks)==proof['checks']==load(B/'qa-spec.json')['expected_checks']
 for x in new:
  assert (out/f'batch/{x}-playback-contact.jpg').is_file() and 'dataset_1324_'+x not in {e['id'] for e in l['reviewed']}
  l['reviewed'].append({'id':'dataset_1324_'+x,'name':rows[x]['name_zh'],'reviewed_at':datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat(),'reviewer':'AI逐项复核','media_sha256':proof['media_sha256'][x],'source':r['sources'][x],'note':r['review_notes'][x]+' 已核对实际加载、器械筛选、关节负荷、计次及 Android 完整循环，保留动态封面和训练选择。'})
 l['pending']=[e for e in l['pending'] if e['id'] not in {'dataset_1324_'+x for x in new}];save(lp,l)
 r.update(initial_validation='passed',newly_reviewed=['dataset_1324_'+x for x in new],android_playback_visually_reviewed=new);save(B/'review-result.json',r)
 s['deferred_ids']=[x for x in s['deferred_ids'] if x not in r['newly_reviewed']]
 s['active_batch'].update(phase='release_validation',next_step='Build final ledger; verify reviewed-only choices, dynamic covers and package before delivery')
s['last_updated']=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat();save(sp,s);print(json.dumps({'phase':s['active_batch']['phase'],'reviewed':len(l['reviewed'])},ensure_ascii=False))
