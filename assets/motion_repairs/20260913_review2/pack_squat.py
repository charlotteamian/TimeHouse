"""Package reviewed regenerated squat poses, with support-point registration only."""
from pathlib import Path
import json,hashlib
import cv2,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
im=Image.open(HERE/'1685.png').convert('RGB');w,h=im.size
cells=[np.array(im.crop((x*w//2,y*h//2,(x+1)*w//2,(y+1)*h//2)).resize((480,480),Image.Resampling.LANCZOS)) for y,x in [(0,0),(0,1),(1,0)]]
shifts=[(0,0),(18,0),(-6,42)];raw=[];frames=[]
for a,(dx,dy) in zip(cells,shifts):
 b=cv2.warpAffine(a,np.float32([[1,0,dx],[0,1,dy]]),(480,480),flags=cv2.INTER_NEAREST,borderValue=(255,255,255));raw.append(b)
 b=cv2.copyMakeBorder(b,24,24,24,24,cv2.BORDER_CONSTANT,value=(255,255,255))
 frames.append(Image.fromarray(b).resize((480,480),Image.Resampling.LANCZOS))
frames.append(frames[1].copy())
checks=[]
for x,y,xx,yy in [(188,447,216,475),(269,440,316,468)]:
 ref=cv2.cvtColor(raw[0],cv2.COLOR_RGB2GRAY)[y:yy,x:xx];values=[]
 for a in raw:
  match=cv2.matchTemplate(cv2.cvtColor(a,cv2.COLOR_RGB2GRAY)[y-7:min(480,yy+7),x-7:xx+7],ref,cv2.TM_CCOEFF_NORMED)
  _,score,_,loc=cv2.minMaxLoc(match);values.append([loc[0]-7,loc[1]-7,round(score,3)])
 checks.append(values)
assert all(abs(x)<=2 and abs(y)<=1 for foot in checks for x,y,_ in foot),checks
for i,frame in enumerate(frames):frame.save(HERE/f'1685-fixed-{i}.png')
frames[0].save(HERE/'1685-fixed.webp',save_all=True,append_images=frames[1:],duration=[800,380,800,380],loop=0,lossless=True,method=6)
frames[0].save(HERE/'1685-fixed.gif',save_all=True,append_images=frames[1:],duration=[800,380,800,380],loop=0,disposal=2)
sheet=Image.new('RGB',(960,960),'white')
for i,f in enumerate(frames):sheet.paste(f,((i%2)*480,(i//2)*480))
sheet.save(HERE/'1685-fixed-sheet.jpg')
(HERE/'1685-validation.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256((HERE/'1685.png').read_bytes()).hexdigest(),output_sha256=hashlib.sha256((HERE/'1685-fixed.webp').read_bytes()).hexdigest(),translations=shifts,uniform_padding=24,feet_residual_before_uniform_resize=checks,frames=4,durations=[800,380,800,380]),indent=2)+'\n')
print(checks)
