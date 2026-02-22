#!/usr/bin/env python3
"""
Scrum 報告生成器
輸出到 reports 目錄並顯示
"""

import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace"))
REPORTS_DIR = WORKSPACE / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def load_todos():
    """載入 todos"""
    with open(WORKSPACE / "todos" / "todos.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_bugs():
    """載入 bugs"""
    with open(WORKSPACE / "bugs" / "issues.json", "r", encoding="utf-8") as f:
        return json.load(f)

def format_scrum_report():
    """產生 Scrum 報告"""
    todos = load_todos()
    bugs = load_bugs()
    
    summary = todos.get("summary", {})
    todo_list = [t for t in todos.get("todos", []) if t["status"] == "todo"]
    in_progress = [t for t in todos.get("todos", []) if t["status"] == "in_progress"]
    review = [t for t in todos.get("todos", []) if t["status"] == "review"]
    done = [t for t in todos.get("todos", []) if t["status"] == "done"]
    
    open_bugs = [b for b in bugs.get("bugs", []) if b["status"] == "open"]
    high_bugs = [b for b in open_bugs if b["severity"] == "high"]
    medium_bugs = [b for b in open_bugs if b["severity"] == "medium"]
    
    lines = [
        "📋 **Sprint 進度摘要**",
        f"📅 日期: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"📊 統計: 📋{summary.get('todo', 0)} | 🔄{summary.get('in_progress', 0)} | 🔍{summary.get('review', 0)} | ✅{summary.get('done', 0)}",
        f"總估點: {summary.get('total_points', 0)} pts",
        "",
        "---",
    ]
    
    if in_progress:
        lines.append("🔄 進行中")
        for t in in_progress:
            lines.append(f"  • {t['id']}: {t['task']} [{t['priority']}]")
        lines.append("")
    
    if review:
        lines.append("🔍 Review")
        for t in review:
            lines.append(f"  • {t['id']}: {t['task']} [{t['priority']}]")
        lines.append("")
    
    if done:
        lines.append("✅ 已完成")
        for t in done:
            lines.append(f"  • {t['id']}: {t['task']}")
        lines.append("")
    
    if open_bugs:
        lines.append("🐛 Open Bugs")
        for b in open_bugs:
            sev = "🔴" if b["severity"] == "high" else "🟡"
            lines.append(f"  {sev} {b['id']}: {b['title']}")
        lines.append("")
    
    report = "\n".join(lines)
    
    # 寫入檔案
    filename = REPORTS_DIR / f"scrum_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    # latest
    latest = REPORTS_DIR / "scrum_latest.md"
    with open(latest, "w", encoding="utf-8") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    print(format_scrum_report())
