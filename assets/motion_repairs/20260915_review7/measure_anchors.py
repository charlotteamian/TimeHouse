"""Measure unchanged support patches in existing frames; read-only media analysis."""
from pathlib import Path
import cv2,json,numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BOXES={'0138': [[20, 279, 96, 350], [273, 353, 350, 378]], '0287': [[181, 414, 225, 465], [335, 409, 405, 452], [230, 413, 309, 443], [76, 375, 192, 409]], '0288': [[20, 346, 83, 384], [78, 338, 123, 369], [108, 354, 188, 391], [371, 372, 440, 418], [310, 220, 391, 279]], '0290': [[188, 423, 227, 469], [339, 412, 411, 452], [229, 417, 310, 451], [99, 388, 177, 418]], '0291': [[215, 403, 259, 470], [284, 406, 353, 459], [43, 395, 122, 437]], '0305': [[10, 331, 77, 399], [68, 342, 179, 383], [356, 367, 456, 423]], '0139': [[73, 15, 106, 121], [375, 15, 405, 121], [192, 52, 226, 91], [275, 52, 309, 91]], '0140': [[83, 10, 117, 116], [402, 10, 440, 116], [210, 54, 245, 90], [292, 54, 329, 90]], '0251': [[70, 386, 128, 432], [324, 397, 409, 453], [200, 209, 241, 242]], '0253': [[86, 371, 142, 434], [312, 374, 393, 437], [194, 40, 219, 63], [263, 40, 287, 63]]}
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
