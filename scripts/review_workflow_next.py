#!/usr/bin/env python3
"""Read-only, bounded continuation summary; never grants exercise approval."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/'assets/motion_repairs/review-workflow-state.json').read_text())
dataset=ROOT/'app/src/main/assets/exercises_1324.json'
ledger=json.loads((ROOT/'app/src/main/assets/exercise_reviews.json').read_text())
assert hashlib.sha256(dataset.read_bytes()).hexdigest()==ledger['dataset_sha256'],'Review dataset hash mismatch; resolve before continuing'
approved={r['id'] for r in ledger['reviewed']}
deferred=set(state.get('deferred_ids',[]))
pending={r['id']:r['note'] for r in ledger['pending']}
active=state.get('active_batch')
if active and active.get('phase')!='complete':
 print(json.dumps({'action':'resume','batch':active,'reviewed':len(approved)},ensure_ascii=False,indent=2))
else:
 rows=json.loads(dataset.read_text())['exercises']
 candidates=[e for e in rows if 'dataset_1324_'+e['id'] not in approved|deferred]
 priority={'body weight':0,'dumbbell':1,'suspension trainer':2}
 candidates.sort(key=lambda e:(e['id'] not in state.get('preferred_ids',[]),e['id']))
 pools={equipment:[e for e in candidates if e['equipment']==equipment] for equipment in priority}
 selected=[]
 while len(selected)<state.get('batch_size',10) and any(pools.values()):
  for equipment in priority:
   if pools[equipment] and len(selected)<state.get('batch_size',10):selected.append(pools[equipment].pop(0))
 if not selected:selected=candidates[:state.get('batch_size',10)]
 batch=[{'id':'dataset_1324_'+e['id'],'name':e['name_zh'],'equipment':e['equipment'],'note':pending.get('dataset_1324_'+e['id'],'')} for e in selected]
 seed_missing=[]
 if state.get('latest_audit'):
  audit=json.loads((ROOT/state['latest_audit']).read_text())
  seed_missing=[{'id':r['id'],'name':r['name']} for r in audit['exercises'] if r['id'].startswith('exercise_') and r['queue']=='待补图']
  for seed in seed_missing:
   attempt=state.get('generation_attempts',{}).get(seed['id'])
   if attempt:seed['previous_attempt']=attempt
 trx_repairs=[{'id':'dataset_1324_'+e['id'],'name':e['name_zh'],'note':pending.get('dataset_1324_'+e['id'],''),'requires_new_repair_strategy':True} for e in rows if e['equipment']=='suspension trainer' and 'dataset_1324_'+e['id'] in deferred]
 print(json.dumps({'action':'review_next' if batch else 'inspect_deferred_and_seed_queue','reviewed':len(approved),'remaining_dataset_candidates':len(candidates),'deferred':len(deferred),'next':batch,'seed_missing':seed_missing,'trx_repairs':trx_repairs},ensure_ascii=False,indent=2))
