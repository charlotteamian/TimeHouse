"""Publish one local reviewed APK after the recorded verification gates pass."""
from pathlib import Path
import json,hashlib,shutil
from datetime import datetime
from zoneinfo import ZoneInfo
B=Path(__file__).resolve().parent;R=B.parents[2];O=R/'build/review7-20260915'
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
expected={'batch':25,'review':13,'edges':4,'dynamic':10}
checks={name:len(json.loads((O/name/'ui-checks.json').read_text())) for name in expected};assert checks==expected,checks
package=json.loads((O/'package-verification.json').read_text());assert package['version']=='1.2.11'
apk=R/'build/timehouse-debug.apk';assert hashlib.sha256(apk.read_bytes()).hexdigest()==package['sha256']
dest=R/'build/时光屋-1.2.11-第七批动作复核.apk';assert not dest.exists()
for log in ['review7-domain.log','review7-final-data.log']:
 text=(R/'build'/log).read_text();assert 'ExerciseDataset: 1324 Chinese records and 1324 animations validated' in text
result=json.loads((B/'review-result.json').read_text());assert result['initial_validation']=='passed' and len(result['newly_reviewed'])==4
ledger=json.loads((R/'app/src/main/assets/exercise_reviews.json').read_text());assert len(ledger['reviewed'])==28
newnames=[r['name'] for r in ledger['reviewed'] if r['id'] in result['newly_reviewed']];options=json.loads((O/'edges/reviewed-options.json').read_text());assert all(any(name in label for label in options) for name in newnames)
shutil.copy2(apk,dest);assert hashlib.sha256(dest.read_bytes()).hexdigest()==package['sha256'];package['apk']=str(dest.relative_to(R));save(O/'package-verification.json',package)
now=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
summary={'status':'passed','completed_at':now,'version':'1.2.11','domain_tests':'passed','build':'passed','ui_checks':checks,'ui_checks_total':sum(checks.values()),'reviewed':28,'unreviewed':1327,'new_reviewed_picker_entries_verified':newnames,'package':package,'physical_device_tested':False,'generated_images_imported':0}
save(O/'verification-summary.json',summary)
for src,name in [('review7-domain.log','domain-tests.log'),('review7-final-data.log','dataset-validation.log'),('review7-final-build.log','build.log')]:shutil.copy2(R/'build'/src,O/name)
result.update(validation='passed',completed_at=now,verification_summary=str((O/'verification-summary.json').relative_to(R)));save(B/'review-result.json',result)
report=R/'docs/releases/2026-09-15-review-batch7.md'
report.write_text(f'''# 时光屋 1.2.11 · 第七批动作复核

本批核查 10 条，新增 4 条已复核：哑铃坐姿阿诺德推举、哑铃坐姿肩上推举、窄距平行握引体向上、哑铃俯卧上斜凳耸肩（另一示范）。累计 28 条已复核，1327 条未复核。

两条坐姿推举保留原有四帧，仅修正位置偏移，双脚及训练凳脚同时固定。另两条通过的原图保持不变。纠正倒立撑、胸推、下斜耸肩等误名，以及握法、主肌群和步骤；本批 9 条补齐直立靠背凳、单杠、双杠、中立握引体架或其他凳面配置的必需条件。本轮没有调用 imagegen。

六条仍存在握点或器械独立漂移，保留未复核并记录原因，没有用局部对齐代替通过。动态封面、训练时示范及“仅已复核”选材均保留。在设置中勾选实际具备的器械及凳面配置后，已复核动作可正常选入动作组和训练。

先以未复核状态完成 25 项候选检查，观察全部四条 Android 实际循环，再写已复核标签。最终版本通过 27 项复核筛选、动作组、动态封面和 TRX 回归，共 52 项模拟器检查。领域测试、全部动态图与资料检查通过；安装包内资料、28 条复核媒体哈希及与上一版相同的签名均已核对。实体手机未复测。

当前队列：28 已完成、40 待修图、3 待补图、1284 待核逻辑。工作流继续按小批续跑；已因器械条件重新检查的四条完成处置，仍有独立漂移的条目重新暂缓。

安装包：`{dest.relative_to(R)}`，版本号 2026091501。SHA-256：`{package['sha256']}`。

逐项证据：`assets/motion_repairs/20260915_review7/README.md`；验证明细：`build/review7-20260915/verification-summary.json`。
''')
with (B/'README.md').open('a') as f:f.write('\n## 最终结果\n\n四条候选全部通过；累计 28 条已复核、1327 条未复核。52 项模拟器检查、领域检查、资源验证及安装包验签通过。实体手机未复测。无 imagegen 调用，动态封面与训练可选保持。版本 1.2.11 已生成，完整结果见上述验证明细。\n')
statep=R/'assets/motion_repairs/review-workflow-state.json';state=json.loads(statep.read_text());assert state['active_batch']['id']==B.name
state['active_batch'].update(phase='complete',next_step='Run review_workflow_next.py for the next bounded batch; do not repeat deferred repairs without a new strategy')
state['last_delivered']={'version':'1.2.11','reviewed':28,'unreviewed':1327,'apk':str(dest.relative_to(R)),'sha256':package['sha256'],'report':str(report.relative_to(R))}
state['last_batch_summary']={'inspected':10,'newly_reviewed':4,'registered_media':2,'image_generation_calls':0,'generated_images_imported':0,'checks':52,'remaining_repair':40,'remaining_missing':3,'remaining_logic':1284}
state['preferred_ids']=[x for x in state['preferred_ids'] if x not in result['inspected']]
state['deferred_ids']=[x for x in state['deferred_ids'] if x not in result['newly_reviewed']]
state['new_repair_strategy'].update(status='evaluated',completed_batch=B.name,passed=['0287','0290'],still_deferred=['0288','0291'],note='Required supports now work; the two remaining assets have independent bench/foot drift and require a different repair method.')
state.update(last_updated=now,latest_audit=str((O/'动作复核全量清单.json').relative_to(R)));save(statep,state)
print(json.dumps({'apk':str(dest),'checks':sum(checks.values()),'reviewed':28,'state':'complete'},ensure_ascii=False))
