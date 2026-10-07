"""Register the existing dumbbell RDL frame; no generated/interpolated poses."""
from pathlib import Path
import hashlib,json,shutil,sys
import cv2,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from validate_exercise_gifs import webp_durations
original=HERE/'before/dataset_motion_0300.webp'
if not original.exists():shutil.copy2(ROOT/'app/src/main/res/raw/dataset_motion_0300.webp',original)
im=Image.open(original); frames=[]
for i in range(im.n_frames):
 im.seek(i);a=np.array(im.convert('RGB'))
 if i==2:a=cv2.warpAffine(a,np.float32([[1,0,-4],[0,1,18]]),(480,480),flags=cv2.INTER_NEAREST,borderValue=(255,255,255))
 frames.append(Image.fromarray(a))
assert len(frames)==4
for i,f in enumerate(frames):f.save(HERE/f'0300-fixed-{i}.png')
frames[0].save(HERE/'0300-fixed.webp',save_all=True,append_images=frames[1:],duration=webp_durations(original),loop=0,lossless=True,method=6)
frames[0].save(HERE/'0300-fixed.gif',save_all=True,append_images=frames[1:],duration=webp_durations(original),loop=0,disposal=2)
sheet=Image.new('RGB',(960,960),'white')
for i,f in enumerate(frames):sheet.paste(f,((i%2)*480,(i//2)*480))
sheet.save(HERE/'0300-fixed-sheet.jpg')
checks=[]
ref=cv2.cvtColor(np.array(frames[0]),cv2.COLOR_RGB2GRAY)
fixed=cv2.cvtColor(np.array(frames[2]),cv2.COLOR_RGB2GRAY)
for x,y,xx,yy in [(199,433,272,462),(253,418,288,444)]:
 score=cv2.matchTemplate(fixed[y-10:min(480,yy+10),x-10:xx+10],ref[y:yy,x:xx],cv2.TM_CCOEFF_NORMED)
 _,s,_,p=cv2.minMaxLoc(score);checks.append([p[0]-10,p[1]-10,round(s,3)])
assert all(x==0 and y==0 for x,y,_ in checks)
(HERE/'0300-validation.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),output_sha256=hashlib.sha256((HERE/'0300-fixed.webp').read_bytes()).hexdigest(),shift_frame_2=[-4,18],feet_displacements_after=checks,frames=4,durations=webp_durations(original)),indent=2)+'\n')
print('Both foot anchors aligned: '+str(checks))
