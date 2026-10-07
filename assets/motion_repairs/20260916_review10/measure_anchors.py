"""Read-only support-patch measurements; no image modification or approval."""
from pathlib import Path
import cv2,json,numpy as np
from PIL import Image
B=Path(__file__).resolve().parent
BOXES={
'0318':[[238,414,302,470],[358,405,436,450],[51,356,164,394],[279,407,363,442]],
'0320':[[207,419,268,469],[336,410,415,450],[65,369,177,400],[190,415,296,445]],
'0322':[[218,412,278,460],[348,401,430,440],[59,371,184,400],[262,402,361,437]],
'0321':[[194,421,248,466],[60,385,136,431],[284,329,416,380],[136,379,275,435]],
'0319':[[171,411,220,475],[33,378,109,430],[281,317,402,367]],
'0459':[[201,356,297,408],[385,287,473,330]],
'0466':[[80,8,138,90],[259,8,321,90],[48,362,174,457],[332,370,433,440]],
'0464':[[403,380,470,427],[19,353,92,401]],
}
result={}
for xid,boxes in BOXES.items():
 im=Image.open(B/'before'/f'dataset_motion_{xid}.webp');frames=[]
 for i in range(im.n_frames):
  im.seek(i);frames.append(cv2.cvtColor(np.array(im.convert('RGB')),cv2.COLOR_RGB2GRAY))
 records=[]
 for box in boxes:
  x0,y0,x1,y1=box;t=frames[0][y0:y1,x0:x1];matches=[]
  for f in frames:
   sx=max(0,x0-50);sy=max(0,y0-70);ex=min(480,x1+50);ey=min(480,y1+70)
   _,score,_,loc=cv2.minMaxLoc(cv2.matchTemplate(f[sy:ey,sx:ex],t,cv2.TM_CCOEFF_NORMED))
   matches.append([int(loc[0]+sx-x0),int(loc[1]+sy-y0),round(score,3)])
  records.append({'box':box,'matches':matches})
 result[xid]=records
(B/'anchor-measurements.json').write_text(json.dumps(result,indent=2)+'\n')
for xid,records in result.items():print(xid,[r['matches'] for r in records])
