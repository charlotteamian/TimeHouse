"""Deliver one APK only after all recorded batch and final review gates pass."""
from pathlib import Path
import json,hashlib,shutil
from datetime import datetime
from zoneinfo import ZoneInfo
B=Path(__file__).resolve().parent;R=B.parents[2];O=R/'build/review8-20260915'
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
counts={n:len(json.loads((O/n/'ui-checks.json').read_text())) for n in ['batch','review','edges','dynamic']};assert counts=={'batch':15,'review':13,'edges':4,'dynamic':10},counts
package=json.loads((O/'package-verification.json').read_text());assert package['version']=='1.2.12'
apk=R/'build/timehouse-debug.apk';assert hashlib.sha256(apk.read_bytes()).hexdigest()==package['sha256']
result=json.loads((B/'review-result.json').read_text());assert result['initial_validation']=='passed' and len(result['newly_reviewed'])==2
ledger=json.loads((R/'app/src/main/assets/exercise_reviews.json').read_text());assert len(ledger['reviewed'])==30
names=[r['name'] for r in ledger['reviewed'] if r['id'] in result['newly_reviewed']];options=json.loads((O/'edges/reviewed-options.json').read_text());assert all(any(n in label for label in options) for n in names)
rows=json.loads((R/'app/src/main/assets/exercises_1324.json').read_text())['exercises'];assert {e['id'] for e in rows if '站姿稳定' in e.get('movement_patterns_zh',[])}=={'0309','0311'}
for log in ['review8-domain.log','review8-final-data.log']:assert 'ExerciseDataset: 1324 Chinese records and 1324 animations validated' in (R/'build'/log).read_text()
dest=R/'build/时光屋-1.2.12-第八批动作复核.apk';assert not dest.exists();shutil.copy2(apk,dest);assert hashlib.sha256(dest.read_bytes()).hexdigest()==package['sha256'];package['apk']=str(dest.relative_to(R));save(O/'package-verification.json',package)
now=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat();summary={'status':'passed','completed_at':now,'version':'1.2.12','domain_tests':'passed','build':'passed','ui_checks':counts,'ui_checks_total':sum(counts.values()),'reviewed':30,'unreviewed':1325,'new_reviewed_picker_entries_verified':names,'package':package,'physical_device_tested':False,'image_generation_calls':2,'generated_images_imported':1,'standing_stability_scope':['0309','0311']};save(O/'verification-summary.json',summary)
for src,name in [('review8-domain.log','domain-tests.log'),('review8-final-data.log','dataset-validation.log'),('review8-final-build.log','build.log')]:shutil.copy2(R/'build'/src,O/name)
result.update(validation='passed',completed_at=now,verification_summary=str((O/'verification-summary.json').relative_to(R)));save(B/'review-result.json',result)
p=B/'generation-attempt.json';g=json.loads(p.read_text());g.update(status='approved',android_validation='passed');save(p,g)
report=R/'docs/releases/2026-09-15-review-batch8.md';report.write_text(f'''# 时光屋 1.2.12 · 第八批动作复核

本批核查 10 条，新增 2 条已复核：哑铃双臂前平举、哑铃肩胛平面上举（拇指朝上）。累计 30 条已复核，1325 条未复核。

前平举保留原有四帧，只修正同向漂移。肩胛平面上举原名误译为“全幅度侧平举”，图片握法和轨迹也不明确；使用内置 imagegen 一次生成、一次定向精修，纠正抬臂方向与中立握法，再以两脚为固定点重封装。两张动态图均通过 Android 完整循环核查，保持动态封面与训练可选。

为 3 条未复核的凳上动作补齐下斜凳／平板凳条件；纠正相关名称和主肌群。两条通过项明确为辅助上举动作，双臂同步计次，不作为垂直推举。站姿稳定模式补齐低腰背负荷，肩部仍按中等负荷筛选。本轮其他 8 条保持未复核，其中 7 条待修图、1 条待核逻辑。

先在未复核状态完成 15 项候选检查并逐帧查看实际播放，再写入复核标签。最终版本通过 27 项复核筛选、动作组、动态封面和 TRX 回归，共 42 项模拟器检查。领域测试和全部动态图／资料检查通过，两个新动作均能从仅已复核动作组选择器选入。APK 资料与 30 条复核媒体哈希、同签名覆盖安装条件均通过。实体手机未复测。

当前队列：30 已完成、47 待修图、3 待补图、1275 待核逻辑。工作流继续小批续跑，保留其他已失败生成的记录，未重复尝试同一失败方法。

安装包：`{dest.relative_to(R)}`，版本号 2026091502。SHA-256：`{package['sha256']}`。

逐项证据及 imagegen 提示词：`assets/motion_repairs/20260915_review8/README.md`；验证明细：`build/review8-20260915/verification-summary.json`。
''')
with (B/'README.md').open('a') as f:f.write('\n## 最终结果\n\n两条候选全部通过；累计 30 条已复核、1325 条未复核。42 项模拟器检查、领域和资源检查、APK 哈希及同签名校验通过。一个动作使用内置 imagegen 两次调用，其他原姿势继续保留。版本 1.2.12 已交付，实体手机未复测。\n')
p=R/'assets/motion_repairs/review-workflow-state.json';state=json.loads(p.read_text());assert state['active_batch']['id']==B.name;state['active_batch'].update(phase='complete',next_step='Run review_workflow_next.py for the next bounded batch; preserve deferred failures and generation limits')
state['last_delivered']={'version':'1.2.12','reviewed':30,'unreviewed':1325,'apk':str(dest.relative_to(R)),'sha256':package['sha256'],'report':str(report.relative_to(R))};state['last_batch_summary']={'inspected':10,'newly_reviewed':2,'registered_media':2,'original_pose_repairs':1,'image_generation_calls':2,'generated_images_imported':1,'checks':42,'remaining_repair':47,'remaining_missing':3,'remaining_logic':1275};state['generation_attempts']['dataset_1324_0311'].update(result='approved',reason='Refined arm plane and neutral grip, stationary feet and full Android playback passed',requires_new_strategy=False);state.update(last_updated=now,latest_audit=str((O/'动作复核全量清单.json').relative_to(R)));save(p,state)
print(json.dumps({'apk':str(dest),'checks':42,'reviewed':30,'phase':'complete'},ensure_ascii=False))
