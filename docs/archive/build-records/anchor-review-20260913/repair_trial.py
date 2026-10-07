from pathlib import Path
import cv2,numpy as np,json,sys
from PIL import Image
sys.path.insert(0,str(Path.cwd()/'scripts'))
from validate_exercise_gifs import webp_durations
out=Path(__file__).resolve().parent
for xid in ['0426','0808']:
 path=Path(f'app/src/main/res/raw/dataset_motion_{xid}.webp')
 fs=[np.array(Image.open(out/f'{xid}-{i}.png').convert('RGB')) for i in range(4)]
 fixed=[]
 for i,a in enumerate(fs):
  if xid=='0426':
   # Both feet drift downward together by six pixels in the top position.
   b=cv2.warpAffine(a,np.float32([[1,0,0],[0,1,-6 if i==2 else 0]]),(480,480),flags=cv2.INTER_NEAREST,borderValue=(255,255,255))
  elif i in [1,2,3]:
   # Isolate only the strap and wall mount above the grip. Body and ground contact are untouched.
   old=np.float64([400,42]) if i in [1,3] else np.float64([404,39])
   new=np.float64([419,45]); grip=np.float64([247,125])
   direction=old-grip
   linear=np.eye(2)+np.outer(new-old,direction)/np.dot(direction,direction)
   affine=np.column_stack([linear,grip-linear@grip]).astype('float32')
   mask=np.zeros((480,480),np.uint8)
   cv2.fillPoly(mask,[np.array([[244,112],[389,21],[412,21],[414,57],[253,142],[239,135]],np.int32)],255)
   # White background only; the mask deliberately stops above hands/handles.
   layer=np.full_like(a,255);layer[mask>0]=a[mask>0]
   b=a.copy();b[mask>0]=255
   moved=cv2.warpAffine(layer,affine,(480,480),flags=cv2.INTER_LINEAR,borderValue=(255,255,255))
   movedmask=cv2.warpAffine(mask,affine,(480,480),flags=cv2.INTER_NEAREST)
   b[movedmask>0]=moved[movedmask>0]
   # Exact original wall mount at the original attachment point, after cleaning its old position.
   b[26:67,393:431]=fs[0][26:67,393:431]
  else:b=a.copy()
  Image.fromarray(b).save(out/f'{xid}-fixed-{i}.png');fixed.append(Image.fromarray(b))
 fixed[0].save(out/f'{xid}-fixed.webp',save_all=True,append_images=fixed[1:],duration=webp_durations(path),loop=0,lossless=True,method=6)
 fixed[0].save(out/f'{xid}-fixed.gif',save_all=True,append_images=fixed[1:],duration=webp_durations(path),loop=0,disposal=2)
 sheet=Image.new('RGB',(960,960),'white')
 for i,f in enumerate(fixed):sheet.paste(f,((i%2)*480,(i//2)*480))
 sheet.save(out/f'{xid}-fixed-sheet.jpg')
