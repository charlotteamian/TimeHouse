"""Measure unchanged support patches in existing frames; read-only media analysis."""
from pathlib import Path
import cv2,json,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BOXES={'0003': [[262, 348, 318, 378], [83, 352, 135, 379]], '0299': [[171, 413, 211, 458], [255, 402, 316, 450]], '0020': [[166, 389, 267, 444], [200, 389, 244, 419]], '0301': [[30, 305, 129, 364], [332, 337, 413, 408]], '0129': [[10, 398, 110, 430], [345, 385, 454, 429]], '0130': [[18, 412, 139, 460], [368, 403, 460, 455]], '0302': [[82, 381, 171, 443], [332, 333, 448, 386], [402, 304, 467, 347]], '0303': [[45, 383, 140, 439], [307, 354, 426, 404], [389, 315, 455, 352]], '0137': [[314, 407, 470, 460], [26, 379, 104, 445]], '0304': [[10, 331, 77, 399], [68, 342, 179, 383], [356, 367, 456, 423]], '0292': [[33, 370, 99, 411], [115, 349, 183, 380], [242, 357, 310, 381], [394, 389, 457, 413]]}
result={}
for xid,boxes in BOXES.items():
 im=Image.open(HERE/'before'/f'dataset_motion_{xid}.webp');frames=[]
 for i in range(im.n_frames):im.seek(i);frames.append(cv2.cvtColor(np.array(im.convert('RGB')),cv2.COLOR_RGB2GRAY))
 records=[]
 for box in boxes:
  x0,y0,x1,y1=box;t=frames[0][y0:y1,x0:x1];matches=[]
  for a in frames:
   # Search locally, including up to 100 px of known packaging drift.
   sx=max(0,x0-55);sy=max(0,y0-100);ex=min(480,x1+55);ey=min(480,y1+100)
   _,score,_,loc=cv2.minMaxLoc(cv2.matchTemplate(a[sy:ey,sx:ex],t,cv2.TM_CCOEFF_NORMED))
   matches.append([int(loc[0]+sx-x0),int(loc[1]+sy-y0),round(score,3)])
  records.append({'box':box,'matches':matches})
 result[xid]=records
(HERE/'anchor-measurements.json').write_text(json.dumps(result,indent=2)+'\n')
for xid,records in result.items():print(xid,[r['matches'] for r in records])
