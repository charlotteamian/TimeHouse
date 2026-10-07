"""Measure unchanged support patches in existing frames; read-only media analysis."""
from pathlib import Path
import cv2,json,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BOXES={
 '1427':[[12,312,70,347],[132,337,190,360],[334,335,391,348]],
 '0298':[[184,420,226,466],[267,418,326,460],[218,3,277,62]],
 '0002':[[174,426,218,477],[281,429,328,476]],
 '3016':[[390,349,474,381],[265,345,318,377]],
 '0001':[[29,341,116,372],[192,331,249,357]],
 '1428':[[180,420,221,460],[258,420,299,460],[214,5,269,80]],
 '0292':[[33,370,99,411],[115,349,183,380],[242,357,310,381],[394,389,457,413]],
 '0297':[[171,418,224,464],[335,389,449,438],[42,370,106,402],[258,383,303,414]],
 '0295':[[156,395,214,463],[257,380,323,453]],
 '0296':[[220,410,267,466],[302,402,389,451],[90,348,154,382]],
}
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
