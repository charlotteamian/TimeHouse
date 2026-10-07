"""Measure unchanged support patches in existing frames; read-only media analysis."""
from pathlib import Path
import cv2,json,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BOXES={'0309': [[164, 423, 208, 471], [242, 422, 307, 471]], '0311': [[178, 429, 218, 478], [251, 425, 328, 475]], '0306': [[40, 339, 121, 400], [386, 325, 470, 370], [367, 301, 440, 354], [333, 281, 376, 334]], '0308': [[75, 387, 156, 443], [342, 299, 431, 373], [79, 372, 160, 464], [23, 355, 85, 423]], '0307': [[15, 339, 78, 456], [321, 342, 424, 399]], '0267': [[380, 380, 478, 436], [278, 380, 343, 431]], '0262': [[356, 335, 470, 401], [228, 331, 292, 388]], '0257': [[201, 419, 265, 475], [267, 415, 324, 473]]}
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
