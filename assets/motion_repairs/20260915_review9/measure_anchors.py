"""Measure unchanged support patches in existing frames; read-only media analysis."""
from pathlib import Path
import cv2,json,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BOXES={'0312': [[171, 412, 220, 466], [245, 411, 315, 463]], '0277': [[28, 388, 122, 442], [350, 292, 469, 348], [375, 143, 463, 215]], '0314': [[221, 425, 263, 464], [351, 385, 439, 442], [270, 394, 355, 441], [62, 344, 160, 385]], '0315': [[237, 405, 303, 473], [347, 400, 444, 461], [49, 351, 116, 386], [311, 411, 369, 456]], '0317': [[237, 408, 311, 477], [348, 410, 436, 470], [45, 350, 120, 387], [310, 410, 365, 465]], '0316': [[221, 409, 275, 477], [354, 389, 455, 461], [265, 414, 361, 457], [77, 379, 166, 424]], '0279': [[14, 350, 84, 412], [130, 382, 212, 446], [339, 272, 470, 359], [368, 246, 451, 279]], '0284': [[326, 49, 399, 230], [112, 382, 225, 472], [318, 87, 390, 145]], '0282': [[17, 371, 104, 437], [340, 357, 407, 429], [366, 326, 474, 386]]}
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
