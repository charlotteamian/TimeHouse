#!/usr/bin/env python3
"""Prepare bounded review evidence from the current queue; never grants approval."""
import argparse,json,shutil,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('batch');a=p.parse_args()
ROOT=Path(__file__).resolve().parents[1]
if not a.batch.replace('_','').isalnum():raise SystemExit('Invalid batch id')
q=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/review_workflow_next.py')]))
if q['action']!='review_next':raise SystemExit('Resume current batch or inspect deferred queue first')
b=ROOT/'assets/motion_repairs'/a.batch
if b.exists():raise SystemExit('Existing batch must be resumed, not overwritten')
(b/'before').mkdir(parents=True)
ids=[e['id'].split('_')[-1] for e in q['next']]
dataset=json.loads((ROOT/'app/src/main/assets/exercises_1324.json').read_text())
rows=[e for xid in ids for e in dataset['exercises'] if e['id']==xid]
(b/'selected.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
for name in ['exercises_1324.json','exercise_reviews.json']:shutil.copy2(ROOT/'app/src/main/assets'/name,b/'before'/name)
shutil.copy2(ROOT/'app/src/main/AndroidManifest.xml',b/'before/AndroidManifest.xml')
for e in rows:shutil.copy2(ROOT/'app/src/main/res/raw'/f'dataset_motion_{e["id"]}.webp',b/'before')
for page in range((len(rows)+4)//5):
 sheet=Image.new('RGB',(1200,1625),'#eee');d=ImageDraw.Draw(sheet)
 for j,e in enumerate(rows[page*5:page*5+5]):
  d.text((8,j*325+6),e['id']+' '+e['name'],fill='black')
  im=Image.open(b/'before'/f'dataset_motion_{e["id"]}.webp')
  for f in range(im.n_frames):im.seek(f);sheet.paste(im.convert('RGB').resize((300,300)),(f*300,j*325+25))
 sheet.save(b/f'contact-{page+1}.jpg')
statep=ROOT/'assets/motion_repairs/review-workflow-state.json';state=json.loads(statep.read_text())
state['active_batch']={'id':a.batch,'path':str(b.relative_to(ROOT)),'phase':'inspection','inspected_ids':ids,'next_step':'Inspect all frames, supports and definitions; save manual evidence before approval'}
statep.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'batch':str(b),'ids':ids},ensure_ascii=False))
