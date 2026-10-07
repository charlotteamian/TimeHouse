import cv2,json,numpy as np
from PIL import Image
from pathlib import Path
out=Path(__file__).resolve().parent
specs={'0276':[[22,300,105,375],[265,340,315,368]],'3013':[[24,269,92,335],[405,321,470,350]],'1685':[[165,410,220,447],[270,410,326,447]],'0334':[[166,414,220,448],[264,414,305,448]],'0406':[[170,414,209,450],[264,414,305,450]],'0426':[[170,410,225,455],[270,410,328,455]],'0805':[[386,45,455,438],[62,390,116,446]],'0808':[[394,29,425,65],[333,573 if False else 384,407,420]],'0809':[[223,630 if False else 405,337 if False else 338,448],[386,60,410,135]]}
# Correct front shoe extent for 0809.
specs['0809'][0]=[224 if False else 147,407,229,448]
results={}
for xid,rois in specs.items():
 fs=[cv2.imread(str(out/f'{xid}-{i}.png'),0) for i in range(4)]
 anchors=[]
 for roi in rois:
  x0,y0,x1,y1=roi;t=fs[0][y0:y1,x0:x1]; per=[]
  for f in fs:
   sx=max(0,x0-70);sy=max(0,y0-70);ex=min(480,x1+70);ey=min(480,y1+70)
   score=cv2.matchTemplate(f[sy:ey,sx:ex],t,cv2.TM_CCOEFF_NORMED)
   _,conf,_,loc=cv2.minMaxLoc(score)
   per.append([loc[0]+sx-x0,loc[1]+sy-y0,round(conf,3)])
  anchors.append({'roi':roi,'matches':per})
 results[xid]=anchors
(out/'anchor-measurements.json').write_text(json.dumps(results,indent=2))
for k,v in results.items():print(k,[x['matches'] for x in v])
