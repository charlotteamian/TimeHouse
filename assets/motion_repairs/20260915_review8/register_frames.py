"""Repackage 0309 original poses and 0311 ImageGen v2 cells with measured offsets; no morphing."""
from pathlib import Path
import hashlib,json,shutil,sys
import cv2,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_exercise_gifs import webp_durations
SHIFTS={'0309':[(0,0),(26,0),(0,-1),(26,0)],'0311':[(0,0),(20,0),(0,0),(20,0)]}
measurements=json.loads((HERE/'anchor-measurements.json').read_text())
measurements['0311']=json.loads((HERE/'0311-generated-anchor-measurements.json').read_text())[:2]
result={}
for xid,shifts in SHIFTS.items():
 original=HERE/'before'/f'dataset_motion_{xid}.webp'
 if not original.exists():shutil.copy2(ROOT/'app/src/main/res/raw'/original.name,original)
 im=Image.open(original);frames=[]
 assert im.n_frames==4
 for i,(dx,dy) in enumerate(shifts):
  im.seek(i);a=np.array(Image.open(HERE/f'0311-v2-frame{i}.png').convert('RGB') if xid=='0311' else im.convert('RGB'))
  b=cv2.warpAffine(a,np.float32([[1,0,dx],[0,1,dy]]),(480,480),flags=cv2.INTER_NEAREST,borderValue=(255,255,255))
  assert (a.min(2)<200).sum()==(b.min(2)<200).sum(),(xid,i,'foreground cropped')
  frames.append(Image.fromarray(b));frames[-1].save(HERE/f'{xid}-fixed-{i}.png')
 checks=[]
 for record in measurements[xid]:
  residual=[[x+shifts[i][0]-shifts[0][0],y+shifts[i][1]-shifts[0][1],score] for i,(x,y,score) in enumerate(record['matches'])]
  assert all(abs(x)<=2 and abs(y)<=2 and score>=.83 for x,y,score in residual),(xid,residual)
  checks.append(dict(box=record['box'],residual=residual))
 durations=webp_durations(original)
 output=HERE/f'{xid}-fixed.webp'
 frames[0].save(output,save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True,method=6)
 frames[0].save(HERE/f'{xid}-fixed.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
 sheet=Image.new('RGB',(960,960),'white')
 for i,f in enumerate(frames):sheet.paste(f,((i%2)*480,(i//2)*480))
 sheet.save(HERE/f'{xid}-fixed-sheet.jpg')
 result[xid]=dict(source_sha256=hashlib.sha256((HERE/'0311-generated-v2.png' if xid=='0311' else original).read_bytes()).hexdigest(),output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),translations=shifts,frames=4,durations=durations,foreground_pixels_preserved=True,anchors=checks)
(HERE/'registration-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('Registered',len(result),'animations; all support residuals <= 2 px; original foreground retained')
