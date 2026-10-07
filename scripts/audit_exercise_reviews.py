#!/usr/bin/env python3
"""Create an evidence-based review queue. Technical validity never grants review status."""
import argparse,hashlib,json,os,subprocess
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='build/review-current')
args=parser.parse_args()
OUT=ROOT/args.output
JDK=Path(os.environ.get('JAVA_HOME','/Applications/Android Studio.app/Contents/jbr/Contents/Home'))/'bin'
OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/'app/src/main/assets/exercises_1324.json'
ledger=json.loads((ROOT/'app/src/main/assets/exercise_reviews.json').read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==ledger['dataset_sha256'],'Review dataset changed; re-review required'
reviewed={r['id']:r for r in ledger['reviewed']}
assert len(reviewed)==len(ledger['reviewed'])
pending={r['id']:r['note'] for r in ledger['pending']}
subprocess.run([str(JDK/'javac'),'-cp',str(ROOT/'build/test-classes'),'-d',str(OUT),str(ROOT/'scripts/review_catalog/ExportSeedCatalog.java')],check=True)
seeds=json.loads(subprocess.check_output([str(JDK/'java'),'-cp',str(OUT)+':'+str(ROOT/'build/test-classes'),'ExportSeedCatalog']))
rows=[dict(id='dataset_1324_'+r['id'],name=r['name_zh'],equipment=r['equipment'],region=r['category'],media=r['media']) for r in json.loads(source.read_text())['exercises']]+seeds
for row in rows:
 media=row['media']; asset=ROOT/'app/src/main/res/raw'/(media[4:]+'.webp') if media.startswith('raw:') else None
 row['status']='已复核' if row['id'] in reviewed else '未复核'
 row['queue']='已完成' if row['id'] in reviewed else ('待补图' if not media or (asset and not asset.exists()) else '待核逻辑')
 row['note']=pending.get(row['id'],'')
 if row['status']=='未复核' and row['queue']!='待补图' and row['note'].startswith('待修图'):
  row['queue']='待修图'
 row['asset']=str(asset.relative_to(ROOT)) if asset else ''
 if row['id'] in reviewed:
  approval=reviewed[row['id']]
  assert asset and asset.exists() and hashlib.sha256(asset.read_bytes()).hexdigest()==approval['media_sha256']
  assert approval['reviewer'] and approval['reviewed_at'] and approval['source'].startswith('https://')
  row['note']=approval['note']; row['source']=approval['source']
assert set(reviewed)<=set(r['id'] for r in rows)
counts=dict(Counter(r['queue'] for r in rows))
rows.sort(key=lambda r:({'待补图':0,'待修图':1,'待核逻辑':2,'已完成':3}[r['queue']],r['equipment'],r['name']))
(OUT/'动作复核全量清单.json').write_text(json.dumps({'total':len(rows),'counts':counts,'exercises':rows},ensure_ascii=False,indent=2)+'\n')
lines=['# 动作库复核清单','',f'默认动作 {len(rows)} 条；已复核 {len(reviewed)} 条；其余 {len(rows)-len(reviewed)} 条均为未复核。','',
'复核标签独立于资料来源、旧版已验证标签和图片技术检查。只有逐项核对名称、器械、文字、动作模式和实际四帧且留下有效记录的条目进入已复核；不是实拍连续动画或个体适用性保证。','',
'## 先补齐缺失示范','',
'以下条目本身仍没有可用示范；同名或近似名称的其他条目不能自动算作已补图。','']
for r in rows:
 if r['queue']=='待补图': lines.append(f'- {r["name"]} · {r["equipment"]} · `{r["id"]}`')
lines+=['','## 本轮已复核','']
for r in rows:
 if r['status']=='已复核': lines.append(f'- {r["name"]} · `{r["id"]}` · [参考资料]({r["source"]})')
lines+=['','## 已知待办','']
for xid,note in pending.items(): lines.append(f'- `{xid}`：{note}')
lines+=['','## 后续顺序','',
'1. 先处理日常动作组会用到、已标心和常用器械的未复核动作，每批 5–10 个。',
'2. 核对名称、实际所需器械、肌群和文字步骤；再对照每个姿势与完整播放。',
'3. 缺图标待补图，重影/错姿势标待修图；生成或修图后仍保持未复核。',
'4. 四项全部核对完成才标已复核。修改资料或示范后自动退回未复核。',
'5. 手机内复核使用动作详情的“复核这个动作”；可记录问题和撤销。',
'',f'队列数量：{json.dumps(counts,ensure_ascii=False)}。全量逐条清单见同目录 JSON。']
(OUT/'动作库梳理.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'total':len(rows),'reviewed':len(reviewed),'counts':counts},ensure_ascii=False))
