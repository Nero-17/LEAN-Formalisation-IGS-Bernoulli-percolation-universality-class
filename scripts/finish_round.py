"""Finalize the single R071 report after its six-hour wall-clock budget."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json

root = Path(__file__).resolve().parents[1]
state_path = root / "ROUND_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8-sig"))
started = datetime.fromisoformat(state["start_utc"].replace("Z", "+00:00"))
finished = datetime.now(timezone.utc)
elapsed = (finished - started).total_seconds()
if elapsed < 21600:
    raise SystemExit("The requested six-hour wall-clock interval has not finished.")
audit = json.loads((root / "docs/source-audit.json").read_text(encoding="utf-8-sig"))
if not audit["ok"]:
    raise SystemExit("Refusing to finalize without a passed source audit.")
state.update(status="completed", finished_utc=finished.isoformat(),
             wall_clock_seconds=round(elapsed, 3),
             verified_modules=audit["module_count"],
             proof_source_commit="347766e")
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
report_path = root / "docs/R071_完整研究记录.md"
report = report_path.read_text(encoding="utf-8-sig")
report = report.replace("**状态：持续工作中，非最终报告。**",
    "**状态：本轮六小时工作完成；全文形式化尚未完成。**")
local_finish = finished.astimezone(timezone(timedelta(hours=8)))
hours, remainder = divmod(int(elapsed), 3600)
minutes, seconds = divmod(remainder, 60)
report = report.replace("- 计划结束：2026-10-06 07:14:33，中国标准时间。",
    f"- 结束：{local_finish:%Y-%m-%d %H:%M:%S}，中国标准时间。\n"
    f"- 实际连续墙钟：{hours}小时{minutes}分{seconds}秒（包括构建、核查与归档收尾）。")
report = report.replace("Git提交`b53e5f9`（之前为`a01154b`与`4a9ebdb`）",
    "Git提交`347766e`（之前为`b53e5f9`、`a01154b`与`4a9ebdb`）")
report_path.write_text(report, encoding="utf-8")
print(json.dumps({"status": state["status"], "finished_utc": state["finished_utc"],
                  "wall_clock_seconds": state["wall_clock_seconds"]}, ensure_ascii=False))
