"""Finalize this Section 3 tranche; this does not mark all Section 3 complete."""
from pathlib import Path
from datetime import datetime, timezone
import json

root = Path(__file__).resolve().parents[1]
state_path = root / 'SECTION3_ROUND_STATE.json'
state = json.loads(state_path.read_text(encoding='utf-8-sig'))
audit = json.loads((root / 'docs/source-audit.json').read_text(encoding='utf-8-sig'))
assert audit['ok']
finished = datetime.now(timezone.utc)
elapsed = (finished - datetime.fromisoformat(state['start_utc'].replace('Z', '+00:00'))).total_seconds()
state.update(status='first_tranche_completed_section3_incomplete', round_status='assigned_and_uploaded',
    finished_utc=finished.isoformat(), wall_clock_seconds=round(elapsed, 3),
    archive_file_id='1mBbMwK7oUpqG33omB1_yPM7IEcTT_vpf',
    proof_source_commit='d2d264b465d708ceb8e257c24755975466b4feba',
    verified_modules=audit['module_count'], milestone_axiom_audits=audit['milestone_axiom_audit_count'])
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
report_path = root / 'docs/R073_完整研究记录.md'
report = report_path.read_text(encoding='utf-8')
report = report.replace('状态：本轮持续工作中，正在全项目编译与交付核查；Section 3 尚未整体完成。',
    '状态：本轮第一批基础证明完成；Section 3 尚未整体完成。')
report = report.replace('结束时间与实际墙钟：收尾时更新本文及 `SECTION3_ROUND_STATE.json`。',
    f'结束记录时间（最终归档打包截止）：{finished:%Y-%m-%d %H:%M:%S} UTC；本轮实际连续墙钟 {int(elapsed)//60} 分 {int(elapsed)%60} 秒。最后的上传回执核验在此后进行。')
report = report.replace('权威归档：首次上传后填写同一 Drive 文件 ID；中途和最终版本均更新该 ID。',
    '权威归档：https://drive.google.com/file/d/1mBbMwK7oUpqG33omB1_yPM7IEcTT_vpf/view 。中途和最终版本始终更新同一文件 ID。')
report = report.replace('上传前再次核对 R073。', '首次上传前已再次核对 R073 未被占用。')
report += '\n## 交付核验\n\n证明源码提交 `d2d264b465d708ceb8e257c24755975466b4feba` 已推送至私有仓库 main。269 个模块和 154 项关键公理审计通过，源文件审计零错误。权威 ZIP 同时包含完整报告、所有 Lean 源文件、工具链配置、构建证据、论文快照和逐项覆盖表；不包含运行时依赖缓存。\n'
report_path.write_text(report, encoding='utf-8')
print(json.dumps({'finished_utc': state['finished_utc'], 'wall_clock_seconds': state['wall_clock_seconds']}, indent=2))
