"""Read-only final APK verification against previous delivery and workspace evidence."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,os,re
B=Path(__file__).resolve().parent;R=B.parents[2];O=R/'build/review9-20260915'
apk=R/'build/timehouse-debug.apk';prev=R/'build/时光屋-1.2.12-第八批动作复核.apk'
sha=lambda b:hashlib.sha256(b).hexdigest()
a=zipfile.ZipFile(apk);b=zipfile.ZipFile(prev);assert a.testzip() is None
for name in ['exercises_1324.json','exercise_reviews.json']:assert a.read('assets/'+name)==(R/'app/src/main/assets'/name).read_bytes()
d=json.loads(a.read('assets/exercises_1324.json'));ld=json.loads(a.read('assets/exercise_reviews.json'));pd=json.loads(b.read('assets/exercises_1324.json'))
assert ld['dataset_sha256']==sha(a.read('assets/exercises_1324.json'))
old={e['id']:e for e in pd['exercises']};rows={e['id']:e for e in d['exercises']};changes=[x for x in rows if rows[x]!=old[x]]
expected=list(json.loads((B/'review-result.json').read_text())['definition_updates']);assert set(changes)==set(expected)
rawnames={n for n in a.namelist() if n.startswith('res/raw/')};assert rawnames=={n for n in b.namelist() if n.startswith('res/raw/')}
rawchanges=sorted(n for n in rawnames if a.getinfo(n).CRC!=b.getinfo(n).CRC or a.read(n)!=b.read(n))
assert rawchanges==['res/raw/dataset_motion_0317.webp']
for e in ld['reviewed']:
 media=rows[e['id'].removeprefix('dataset_1324_')]['media'].removeprefix('raw:')+'.webp';path='res/raw/'+media
 assert sha(a.read(path))==e['media_sha256'] and a.read(path)==(R/'app/src/main/res/raw'/media).read_bytes()
assert len(ld['reviewed'])==34 and not ({r['id'] for r in ld['reviewed']} & {r['id'] for r in ld['pending']})
BT=Path('/Users/restartday/Library/Android/sdk/build-tools/36.1.0');env=dict(os.environ,JAVA_HOME='/Applications/Android Studio.app/Contents/jbr/Contents/Home')
sign=subprocess.check_output([str(BT/'apksigner'),'verify','--print-certs',str(apk)],env=env,text=True);(O/'signature.txt').write_text(sign)
signer=re.search(r'certificate SHA-256 digest: (\w+)',sign).group(1);assert signer=='f97b8a406448cb301259189f833d7beb7985728929dd652d2c257e8d36a28997'
badging=subprocess.check_output([str(BT/'aapt2'),'dump','badging',str(apk)],text=True);(O/'apk-badging.txt').write_text(badging)
assert "versionCode='2026091503'" in badging and "versionName='1.2.13'" in badging
summary=dict(version='1.2.13',version_code=2026091503,sha256=sha(apk.read_bytes()),changed_dataset_ids=changes,changed_raw_assets=rawchanges,reviewed=34,unreviewed=1321,generated_images_imported=0,apk_integrity='passed',dataset_and_review_hashes='passed',signature_verified=True,signer_sha256=signer)
(O/'package-verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
