#!/usr/bin/env python3
"""Pack reviewed ImageGen 2x2 sheets as discrete keyframes, with fixed support registration.
No optical flow, morphing, invented poses, or per-frame auto-centering.
Run with the local Python containing Pillow, numpy and OpenCV.
"""
from pathlib import Path
import argparse, json, re, shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'assets/motion_repairs/20260909'
OUT=ROOT/'build/media-fix-20260909'
RAW=ROOT/'app/src/main/res/raw'
# Local cell fractions: stable support region for translation-only registration.
ANCHORS={
 '0025':(.04,.66,.98,.96),'0289':(.04,.70,.98,.97),
 '0201':(.70,.08,.92,.93),
 '0294':(.29,.68,.70,.96),'0310':(.33,.70,.62,.97),
 '0334':(.34,.70,.66,.97),'0406':(.35,.72,.65,.98),
 '0662':(.02,.58,.14,.85),'0293':(.32,.78,.73,.97),
 '0300':(.36,.86,.68,.98)}
DURATIONS=[800,380,800,380]
def cells(p,inset=0):
 im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,'white'); bg.alpha_composite(im); im=bg.convert('RGB'); w,h=im.size
 if abs(w-h)>2: raise ValueError('Expected square sheet: '+str(p))
 return [im.crop((c*w//2+inset,r*h//2+inset,(c+1)*w//2-inset,(r+1)*h//2-inset)).resize((480,480),Image.Resampling.LANCZOS) for r,c in [(0,0),(0,1),(1,0),(1,1)]]
def align(frames,rect,cycle=False,manual=None):
 if rect is None: return (frames if cycle else frames[:3]+[frames[1].copy()]), [[0,0]]*(4 if cycle else 3)
 x0,y0,x1,y1=[round(x*480) for x in rect]
 ref=np.asarray(frames[0]);mask=np.zeros((480,480),np.uint8);mask[y0:y1,x0:x1]=255
 gray=cv2.cvtColor(ref,cv2.COLOR_RGB2GRAY)
 def padded(a): return cv2.copyMakeBorder(a,32,32,32,32,cv2.BORDER_CONSTANT,value=(255,255,255))
 result=[Image.fromarray(padded(ref)).resize((480,480),Image.Resampling.LANCZOS)];offsets=[[0,0]]
 for frame_index,f in enumerate(frames[1:(4 if cycle else 3)],1):
  a=np.asarray(f);warp=np.eye(2,3,dtype=np.float32)
  try:
   if manual is not None: warp[:,2]=manual[frame_index]
   else: cc,warp=cv2.findTransformECC(gray,cv2.cvtColor(a,cv2.COLOR_RGB2GRAY),warp,cv2.MOTION_TRANSLATION,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,120,1e-5),mask,5)
   if max(abs(warp[0,2]),abs(warp[1,2]))>36: raise ValueError('Support drift exceeds 36px')
  except cv2.error as e: raise ValueError('Support registration failed') from e
  a=cv2.warpAffine(padded(a),warp,(544,544),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_CONSTANT,borderValue=(255,255,255))
  result.append(Image.fromarray(a).resize((480,480),Image.Resampling.LANCZOS));offsets.append([round(float(warp[0,2]),2),round(float(warp[1,2]),2)])
 # Return path retraces the exact same middle pose, not the separately redrawn fourth cell.
 return (result if cycle else result+[result[1].copy()]),offsets

def main():
 global SRC, OUT
 parser=argparse.ArgumentParser()
 parser.add_argument('--batch',default='20260909')
 parser.add_argument('--ids',nargs='*')
 args=parser.parse_args()
 if not re.fullmatch(r'[A-Za-z0-9_]+',args.batch): raise ValueError('Batch must be a safe identifier')
 SRC=ROOT/'assets/motion_repairs'/args.batch
 OUT=ROOT/('build/media-fix-'+args.batch)
 OUT.mkdir(exist_ok=True);(OUT/'before').mkdir(exist_ok=True)
 records=[]
 specs=json.loads((SRC/'prompts.json').read_text())
 if args.ids: specs=[s for s in specs if s['id'] in args.ids]
 for spec in specs:
  xid=spec['id']; frames,offsets=align(cells(SRC/(xid+'.png'),spec.get('cell_inset',0)),spec.get('anchor',ANCHORS.get(xid)),spec.get('cycle',False),spec.get('support_offsets'))
  for i,f in enumerate(frames):f.save(OUT/f'{xid}-frame-{i}.png')
  durations=[590]*4 if spec.get('cycle') else DURATIONS
  gif=OUT/(xid+'.gif')
  frames[0].save(gif,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
  target=RAW/f'dataset_motion_{xid}.webp'
  before=OUT/'before'/target.name
  if not before.exists():shutil.copy2(target,before)
  frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True,method=6)
  # Original material remains previewable, including animated backgrounds.
  old=Image.open(before); olds=[];ds=[]
  for i in range(old.n_frames):old.seek(i);olds.append(old.convert('RGB'));ds.append(1180 if old.n_frames==2 else 236)
  olds[0].save(OUT/(xid+'-before.gif'),save_all=True,append_images=olds[1:],duration=ds,loop=0,disposal=2)
  records.append({'id':xid,'name':spec['name'],'source':str((SRC/(xid+'.png')).relative_to(ROOT)),'asset':str(target.relative_to(ROOT)),'offsets':offsets,'frames':4,'duration':2360,'mode':'reviewed-keyframes-no-morph','prompt_sha256':spec.get('prompt_sha256','')})
 # The same exercise in the curated collection must not keep a different old demonstration.
 for xid,key in [('0289','dumbbell_bench_press'),('0294','dumbbell_curl'),('0027','bent_over_barbell_row'),('0405','seated_shoulder_press'),('1760','goblet_squat')]:
  if xid not in [r['id'] for r in records]: continue
  dst=RAW/f'motion_{key}.webp'; bak=OUT/'before'/dst.name
  if not bak.exists():shutil.copy2(dst,bak)
  shutil.copy2(RAW/f'dataset_motion_{xid}.webp',dst)
 # Identical exercise rows can share a reviewed result without another model call.
 reuse_path=SRC/'reuse.json'
 if reuse_path.exists() and not args.ids:
  names={str(spec['id']):spec['name'] for spec in specs}
  for xid,source_id in json.loads(reuse_path.read_text()).items():
   source_asset=RAW/f'dataset_motion_{source_id}.webp'
   target=RAW/f'dataset_motion_{xid}.webp'
   if not source_asset.exists() or not target.exists(): raise FileNotFoundError(f'Reuse asset missing: {xid} <- {source_id}')
   before=OUT/'before'/target.name
   if not before.exists():shutil.copy2(target,before)
   shutil.copy2(source_asset,target)
   source_preview=OUT/(source_id+'.gif')
   if source_preview.exists():shutil.copy2(source_preview,OUT/(xid+'.gif'))
   records.append({'id':xid,'name':names.get(source_id,xid),'source':str(source_asset.relative_to(ROOT)),'asset':str(target.relative_to(ROOT)),'offsets':[],'frames':4,'duration':2360,'mode':'reviewed-keyframe-reuse','reused_from':source_id})
 if args.ids and (SRC/'manifest.json').exists():
  prior=json.loads((SRC/'manifest.json').read_text())
  records=[r for r in prior if r['id'] not in args.ids]+records
 (SRC/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 cards=[]
 for r in records:
  x=r['id'];cards.append(f'<article><h2>{r["name"]}</h2><div class="pair"><figure><img src="{x}-before.gif"><figcaption>原示范</figcaption></figure><figure><img src="{x}.gif"><figcaption>本批新示范 · 三个动作阶段往返</figcaption></figure></div></article>')
 (OUT/'index.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>时光屋 · 首批10个动作图对照</title><style>body{font:16px system-ui;background:#edf3ef;color:#203b30;max-width:1080px;margin:32px auto;padding:0 20px}h1{font-size:28px}article{background:white;border-radius:20px;padding:20px;margin:20px 0}h2{margin:0 0 12px;font-size:20px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0;text-align:center}img{width:100%;max-width:480px}figcaption{padding:10px;color:#687b71}p{line-height:1.7}button{background:#2c7c62;color:white;border:0;padding:10px 18px;border-radius:12px}body.paused img{visibility:hidden}</style><h1>首批 10 个动作 · 新旧示范对照</h1><p>白底解剖示范，珊瑚红表示主要训练肌群。新示范使用实际生成的动作阶段往返播放；无整图扭曲和虚构中间姿势。此页方便逐项确认风格与动作，尚未扩展到剩余动作库。</p>'''+''.join(cards)+'</html>')
 page=OUT/'index.html'
 page.write_text(page.read_text().replace('首批10个', str(len(records))+'个').replace('首批 10 个',str(len(records))+' 个').replace('此页方便逐项确认风格与动作，尚未扩展到剩余动作库。','本页为本批修复的新旧示范对照。'))
 print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
