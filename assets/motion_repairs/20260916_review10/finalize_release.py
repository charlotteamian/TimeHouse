"""Publish this single batch only after all package and targeted regression gates pass."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
B=Path(__file__).resolve().parent;R=B.parents[2];O=R/'build/review10-20260916'
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=load(B/'review-result.json');s=load(R/'assets/motion_repairs/review-workflow-state.json')
assert s['active_batch']['id']==B.name and s['active_batch']['phase']=='release_validation'
expected={'batch':21,'new-training':12,'review':13,'edges':4,'dynamic':10,'save-bug':15,'user-fixes':20,'routines':4}
counts={key:len(load(O/key/'ui-checks.json')) for key in expected};assert counts==expected,counts
assert len(load(O/'save-bug-before/ui-checks.json'))==3
assert r['initial_validation']=='passed' and len(r['newly_reviewed'])==3
package=load(O/'package-verification.json');apk=R/'build/timehouse-debug.apk'
assert package['version']=='1.2.15' and package['sha256']==sha(apk) and package['signature_verified']
ledger=load(R/'app/src/main/assets/exercise_reviews.json');assert len(ledger['reviewed'])==37
names=[x['name'] for x in ledger['reviewed'] if x['id'] in r['newly_reviewed']]
options=load(O/'edges/reviewed-options.json');assert all(any(n in label for label in options) for n in names)
audit=load(O/'动作复核全量清单.json');assert audit['counts']=={'待核逻辑':1257,'待修图':58,'已完成':37,'待补图':3}
assert 'ExerciseDataset: 1324 Chinese records and 1324 animations validated' in (R/'build/review10-domain.log').read_text()
assert 'Success' in (R/'build/review10-final-install.log').read_text()
assert 'ALL USER FIX CHECKS PASSED' in (R/'build/review10-final-ui.log').read_text()
dest=R/'build'/r['apk_name'];assert not dest.exists();shutil.copy2(apk,dest);assert sha(dest)==package['sha256']
package['apk']=str(dest.relative_to(R));save(O/'package-verification.json',package)
now=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
summary=dict(status='passed',completed_at=now,version='1.2.15',domain_tests='passed',build='passed',ui_checks=counts,ui_checks_total=sum(counts.values()),bug_reproduction_checks=3,reviewed=37,unreviewed=1318,new_reviewed_picker_entries_verified=names,package=package,physical_device_tested=False,image_generation_calls=0,generated_images_imported=0,workflow_status='paused',pause_reason='requested_single_batch_complete')
save(O/'verification-summary.json',summary)
for source,name in [('review10-domain.log','domain-tests.log'),('review10-final-build.log','build.log'),('review10-initial-qa.log','initial-qa.log'),('review10-final-ui.log','final-ui.log'),('review10-save-qa.log','save-bug.log')]:shutil.copy2(R/'build'/source,O/name)
r.update(validation='passed',completed_at=now,verification_summary=str((O/'verification-summary.json').relative_to(R)));save(B/'review-result.json',r)
report=R/r['report'];report.write_text(f'''# 时光屋 1.2.15 · 第十批复核与旧记录保存修复

本批检查 10 条，新增 3 条已复核：哑铃上斜弯举（双臂同步）、哑铃上斜锤式弯举、哑铃上斜锤式弯举（另一示范）。累计 37 条已复核，1318 条未复核。其余 7 条分别记录支点、残图、动作阶段或变式问题，保持未复核。

9 条资料修正：纠正图文名称与步骤、主肌群，补齐上斜凳、平板凳及单杠要求。2 个素材仅用整数平移修正，保留原四帧姿势和 2.36 秒循环；固定点残差不超过 1 px。生成调用 0 次。复核来源、逐项判定、原件和测量见[本批证据](../../assets/motion_repairs/20260916_review10/README.md)。

修复用户截图中的旧记录保存失败：旧记录缺少处方时计划组数为空，被整数解析拒绝，错误又误标在次数框。现在按已记录完成组数预填可修改的计划组数并明确提示，未知次数与重量仍留空；校验错误定位对应字段并滚动显示。在模拟器复现原问题后，验证 3 组旧记录只补 15 次即可保存，重启后保留，原文、心得、热量及心率数据不丢失。

候选在未复核状态先完成 21 项检查并逐项查看 Android 循环；通过后验证 3 个动作均能在器械齐全时进入正常训练、缺凳时拦截、严重肩痛时被推荐筛选排除，并验证双臂同步计次。最终包含复核筛选、动态封面、旧记录保存边界以及共享编辑器的预览／训练中／历史记录回归，共 {sum(counts.values())} 项最终与候选检查通过；另有 3 项原问题复现检查。

领域测试、1324 条资料和动态图校验、全量复核哈希、APK 完整性及与 1.2.14 同签名检查通过。应用 Java 代码仅共享训练安排编辑器改变，保留 1.2.14 其他功能。已模拟器覆盖安装；未在实体手机复测。

队列：37 已完成、58 待修图、3 待补图、1257 待核逻辑。本次仅完成一批，自动工作流保持暂停。

安装包：`{dest.relative_to(R)}`；版本号 2026091602；大小 {package['bytes'] / 1024 / 1024:.1f} MiB。

SHA-256：`{package['sha256']}`。

验证摘要：`build/review10-20260916/verification-summary.json`。
''')
p=B/'README.md';p.write_text(p.read_text().replace('- [ ]','- [x]')+f'\n## 最终结果\n\n候选 3 条全部通过，累计 37 条已复核、1318 条未复核。{sum(counts.values())} 项检查通过，另 3 项旧问题复现通过。APK、数据与素材哈希、签名及覆盖安装验证通过。仅完成本批，持续自动复核保持暂停；未进行实体手机测试。\n')
s['active_batch'].update(phase='complete',next_step='Single requested batch and legacy-save fix delivered; wait for another user request')
s['last_delivered']=dict(version='1.2.15',reviewed=37,unreviewed=1318,apk=str(dest.relative_to(R)),sha256=package['sha256'],report=str(report.relative_to(R)))
s['last_batch_summary']=dict(inspected=10,newly_reviewed=3,registered_media=2,original_pose_repairs=2,image_generation_calls=0,generated_images_imported=0,checks=sum(counts.values()),remaining_repair=58,remaining_missing=3,remaining_logic=1257)
s.update(status='paused',pause_reason='requested_single_batch_complete',paused_at=now,last_updated=now,latest_audit=str((O/'动作复核全量清单.json').relative_to(R)))
save(R/'assets/motion_repairs/review-workflow-state.json',s)
(dest.parent/(dest.name+'.sha256')).write_text(package['sha256']+'  '+dest.name+'\n')
print(json.dumps(dict(apk=str(dest),checks=sum(counts.values()),reviewed=37,status='complete'),ensure_ascii=False))
