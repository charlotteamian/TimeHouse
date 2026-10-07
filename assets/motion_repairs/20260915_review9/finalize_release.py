"""Deliver batch nine only after evidence gates, then record the user's workflow pause."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil,tomllib
B=Path(__file__).resolve().parent;R=B.parents[2];O=R/'build/review9-20260915'
def load(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=load(B/'review-result.json');state=load(R/'assets/motion_repairs/review-workflow-state.json')
assert state['active_batch']['id']==B.name and state['active_batch']['phase']=='release_validation'
counts={n:len(load(O/n/'ui-checks.json')) for n in ['batch','review','edges','dynamic']}
assert counts=={'batch':30,'review':13,'edges':4,'dynamic':10},counts
assert result['initial_validation']=='passed' and len(result['newly_reviewed'])==4 and result['image_generation_calls']==0
package=load(O/'package-verification.json');apk=R/'build/timehouse-debug.apk'
assert package['version']=='1.2.13' and sha(apk)==package['sha256'] and package['signature_verified']
ledger=load(R/'app/src/main/assets/exercise_reviews.json');assert len(ledger['reviewed'])==34
names=[r['name'] for r in ledger['reviewed'] if r['id'] in result['newly_reviewed']]
options=load(O/'edges/reviewed-options.json');assert all(any(n in label for label in options) for n in names)
audit=load(O/'动作复核全量清单.json');assert audit['counts']=={'待核逻辑':1266,'待修图':52,'已完成':34,'待补图':3}
for name in ['review9-domain.log','review9-final-data.log']:
    assert 'ExerciseDataset: 1324 Chinese records and 1324 animations validated' in (R/'build'/name).read_text()
automation=tomllib.load(open('/Users/restartday/.codex/automations/automation/automation.toml','rb'));assert automation['status']=='PAUSED'
dest=R/'build'/result['apk_name'];assert not dest.exists();shutil.copy2(apk,dest);assert sha(dest)==package['sha256']
package['apk']=str(dest.relative_to(R));save(O/'package-verification.json',package)
now=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
summary={'status':'passed','completed_at':now,'version':'1.2.13','domain_tests':'passed','build':'passed','ui_checks':counts,'ui_checks_total':sum(counts.values()),'reviewed':34,'unreviewed':1321,'new_reviewed_picker_entries_verified':names,'package':package,'physical_device_tested':False,'image_generation_calls':0,'generated_images_imported':0,'workflow_status':'paused','pause_reason':'user_requested_stop_after_current_batch'}
save(O/'verification-summary.json',summary)
for src,name in [('review9-domain.log','domain-tests.log'),('review9-final-data.log','dataset-validation.log'),('review9-final-build.log','build.log'),('review9-initial-qa.log','initial-qa.log'),('review9-final-ui.log','final-ui.log')]:shutil.copy2(R/'build'/src,O/name)
result.update(validation='passed',completed_at=now,verification_summary=str((O/'verification-summary.json').relative_to(R)));save(B/'review-result.json',result)
report=R/result['report'];report.write_text(f'''# 时光屋 1.2.13 · 第九批动作复核

本批核查 10 条，新增 4 条已复核：下斜仰卧起坐（勾脚式）、哑铃双臂锤式弯举、哑铃上斜弯举、哑铃上斜弯举（另一示范）。累计 34 条已复核，1321 条未复核。

纠正下斜卷腹的变式名、锤式弯举的错误转掌步骤，补齐凳上动作所需的对应训练凳，以及扶墙提踵所需的墙面与踏台。修正主肌群和训练模式，使其与实际示范一致。保留原有可用姿势，仅对 0317 的四帧作整数平移；双脚、两处凳脚残差不超过 2 px，无前景截断。没有使用 imagegen 重制。

其余 6 条保持未复核：5 条仍有独立支点变化、姿势或图文对应问题，1 条来源变式与播放阶段仍待确认。0314 虽考虑重新排序，但近侧脚无法可靠对应，未导入该方案。逐项原因与来源见 [本批证据](../../assets/motion_repairs/20260915_review9/README.md)。

先在未复核状态完成 30 项候选检查并人工查看四个 Android 播放循环，再写入复核标签。最终版本通过 27 项复核筛选、动作组选择、动态封面和 TRX 回归，共 57 项模拟器检查。领域测试和全部动态图／资料检查通过；四个新动作均出现在仅已复核动作组选择器中。动态封面与正常训练可选保留。

与 1.2.12 相比，APK 内有 9 条动作资料修改、1 个动态图修改；全部 34 条复核媒体哈希和资料哈希通过校验，APK 完整性、同签名覆盖安装条件通过。已在模拟器覆盖安装，未在实体手机复测。

队列为 34 已完成、52 待修图、3 待补图、1266 待核逻辑。按用户“这一批核查完就先到此为止，打包好 apk”的要求，自动工作流已暂停，当前批次记录为完成；没有启动下一批。

安装包：`{dest.relative_to(R)}`，版本号 2026091503。SHA-256：`{package['sha256']}`。

验证摘要：`build/review9-20260915/verification-summary.json`；可续跑状态：`assets/motion_repairs/review-workflow-state.json`。
''')
with (B/'README.md').open('a') as f:f.write('\n## 最终结果\n\n4 条候选全部通过，累计 34 条已复核、1321 条未复核。57 项模拟器检查、领域和资源检查、APK 哈希及同签名校验通过。版本 1.2.13 已交付。按用户要求暂停自动唤醒；本批完成，没有启动下一批。实体手机未复测。\n')
state['active_batch'].update(phase='complete',next_step='Paused at user request after batch nine delivery; resume only upon a new user request')
state['last_delivered']={'version':'1.2.13','reviewed':34,'unreviewed':1321,'apk':str(dest.relative_to(R)),'sha256':package['sha256'],'report':str(report.relative_to(R))}
state['last_batch_summary']={'inspected':10,'newly_reviewed':4,'registered_media':1,'original_pose_repairs':1,'image_generation_calls':0,'generated_images_imported':0,'checks':57,'remaining_repair':52,'remaining_missing':3,'remaining_logic':1266}
state.update(status='paused',pause_reason='user_requested_stop_after_current_batch',paused_at=now,last_updated=now,latest_audit=str((O/'动作复核全量清单.json').relative_to(R)))
save(R/'assets/motion_repairs/review-workflow-state.json',state)
print(json.dumps({'apk':str(dest),'checks':57,'reviewed':34,'phase':'complete','workflow':'paused'},ensure_ascii=False))
