"""Verify final package against 1.2.14, registered review evidence and app source baseline."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,os,re
B=Path(__file__).resolve().parent;R=B.parents[2];O=R/'build/review10-20260916'
result=json.loads((B/'review-result.json').read_text());apk=R/'build/timehouse-debug.apk';prev=R/'build/时光屋-1.2.14-训练编辑与手表数据修复.apk'
sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(apk) as a,zipfile.ZipFile(prev) as b:
 assert a.testzip() is None
 for name in ['exercises_1324.json','exercise_reviews.json']:assert a.read('assets/'+name)==(R/'app/src/main/assets'/name).read_bytes()
 d=json.loads(a.read('assets/exercises_1324.json'));ld=json.loads(a.read('assets/exercise_reviews.json'));pd=json.loads(b.read('assets/exercises_1324.json'))
 assert ld['dataset_sha256']==sha(a.read('assets/exercises_1324.json'))
 old={e['id']:e for e in pd['exercises']};rows={e['id']:e for e in d['exercises']};changes=[x for x in rows if rows[x]!=old[x]]
 assert set(changes)==set(result['definition_updates'])
 rawnames={n for n in a.namelist() if n.startswith('res/raw/')};assert rawnames=={n for n in b.namelist() if n.startswith('res/raw/')}
 rawchanges=sorted(n for n in rawnames if a.getinfo(n).CRC!=b.getinfo(n).CRC or a.read(n)!=b.read(n))
 assert rawchanges==['res/raw/dataset_motion_0318.webp','res/raw/dataset_motion_0320.webp']
 for e in ld['reviewed']:
  media=rows[e['id'].removeprefix('dataset_1324_')]['media'].removeprefix('raw:')+'.webp';path='res/raw/'+media
  assert sha(a.read(path))==e['media_sha256'] and a.read(path)==(R/'app/src/main/res/raw'/media).read_bytes()
 assert len(ld['reviewed'])==37 and not ({r['id'] for r in ld['reviewed']} & {r['id'] for r in ld['pending']})
 changed_assets=sorted(n for n in a.namelist() if n.startswith('assets/') and (n not in b.namelist() or a.read(n)!=b.read(n)))
 assert changed_assets==['assets/exercise_reviews.json','assets/exercises_1324.json']
base=json.loads((B/'code-baseline.json').read_text());code_changes=[p for p,h in base.items() if sha((R/p).read_bytes())!=h]
assert code_changes==['app/src/main/java/com/restartday/fitness/app/WorkoutDoseEditor.java'],code_changes
BT=Path('/Users/restartday/Library/Android/sdk/build-tools/36.1.0');env=dict(os.environ,JAVA_HOME='/Applications/Android Studio.app/Contents/jbr/Contents/Home')
def cert(path):
 text=subprocess.check_output([str(BT/'apksigner'),'verify','--print-certs',str(path)],env=env,text=True)
 return re.search(r'certificate SHA-256 digest: (\w+)',text).group(1),text
signer,sign=cert(apk);previous_signer,_=cert(prev);assert signer==previous_signer;(O/'signature.txt').write_text(sign)
badging=subprocess.check_output([str(BT/'aapt2'),'dump','badging',str(apk)],text=True);(O/'apk-badging.txt').write_text(badging)
assert "versionCode='2026091602'" in badging and "versionName='1.2.15'" in badging
summary=dict(version='1.2.15',version_code=2026091602,sha256=sha(apk.read_bytes()),bytes=apk.stat().st_size,changed_dataset_ids=changes,changed_raw_assets=rawchanges,changed_app_code=code_changes,changed_bundled_assets=changed_assets,reviewed=37,unreviewed=1318,generated_images_imported=0,apk_integrity='passed',dataset_and_review_hashes='passed',signature_verified=True,same_signer_as_1_2_14=True,signer_sha256=signer)
(O/'package-verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
