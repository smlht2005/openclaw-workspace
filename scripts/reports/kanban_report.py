#!/usr/bin/env python3
"""
Kanban 看板生成器
從 todos/todos.json 和 bugs/issues.json 自動生成 kanban.md

用法:
    python3 kanban_report.py           # 產生 kanban.md
    python3 kanban_report.py --dry-run  # 預覽不儲存
    python3 kanban_report.py --show    # 顯示但不儲存
"""

import json
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# 設定
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace"))
TODOS_FILE = WORKSPACE / "todos" / "todos.json"
BUGS_FILE = WORKSPACE / "bugs" / "issues.json"
KANBAN_FILE = WORKSPACE / "kanban.md"

# 台北時區
TAIPEI_TZ = "+08:00"


def load_todos():
    """載入 todos"""
    if not TODOS_FILE.exists():
        return {"todos": [], "summary": {}}
    with open(TODOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_bugs():
    """載入 bugs"""
    if not BUGS_FILE.exists():
        return {"bugs": []}
    with open(BUGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_date():
    """取得台北時間"""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def generate_kanban(todos: dict, bugs: dict) -> str:
    """生成 kanban.md 內容"""
    
    # 分類 tasks
    task_list = todos.get("todos", [])
    
    todo_tasks = [t for t in task_list if t.get("status") == "todo"]
    in_progress = [t for t in task_list if t.get("status") == "in_progress"]
    review_tasks = [t for t in task_list if t.get("status") == "review"]
    done_tasks = [t for t in task_list if t.get("status") == "done"]
    
    # 分類 bugs
    bug_list = bugs.get("bugs", [])
    open_bugs = [b for b in bug_list if b.get("status") == "open"]
    p1_bugs = [b for b in open_bugs if b.get("severity") == "high"]
    
    # Summary
    summary = todos.get("summary", {})
    todo_count = len(todo_tasks)
    in_progress_count = len(in_progress)
    review_count = len(review_tasks)
    done_count = len(done_tasks)
    p1_count = len(p1_bugs)
    
    lines = [
        "# 📋 Project Kanban 看板",
        "",
        "---",
        "",
        "## 📊 Summary 摘要",
        "",
        "| 狀態 | 數量 | 備註 |",
        "|------|------|------|",
        f"| 🔴 P1 | {p1_count} | 緊急 |",
        f"| 🟡 To Do | {todo_count} | 待處理 |",
        f"| 🟢 In Progress | {in_progress_count} | 進行中 |",
        f"| 🔵 Review | {review_count} | 待檢視 |",
        f"| ✅ Done | {done_count} | 已完成 |",
        "",
        "---",
        "",
        "## 📝 Detail 詳情",
        "",
        "### 🟡 To Do 待處理",
    ]
    
    # To Do
    if todo_tasks:
        for t in todo_tasks:
            priority = t.get("priority", "P3")
            task = t.get("task", "")
            task_id = t.get("id", "")
            lines.append(f"- **{task_id}** - {task} [{priority}]")
    else:
        lines.append("- （無）")
    
    lines.extend([
        "",
        "### 🟢 In Progress 進行中",
    ])
    
    # In Progress
    if in_progress:
        for t in in_progress:
            priority = t.get("priority", "P3")
            task = t.get("task", "")
            task_id = t.get("id", "")
            notes = t.get("notes", "")
            note_str = f"（{notes}）" if notes else ""
            lines.append(f"- **{task_id}** - {task} [{priority}] {note_str}")
    else:
        lines.append("- （無）")
    
    lines.extend([
        "",
        "### 🔵 Review 待檢視",
    ])
    
    # Review
    if review_tasks:
        for t in review_tasks:
            priority = t.get("priority", "P3")
            task = t.get("task", "")
            task_id = t.get("id", "")
            lines.append(f"- **{task_id}** - {task} → [檢視](./review/{task_id}-*.md)")
    else:
        lines.append("- （無）")
    
    lines.extend([
        "",
        "### ✅ Done 已完成",
    ])
    
    # Done
    if done_tasks:
        for t in done_tasks:
            task = t.get("task", "")
            task_id = t.get("id", "")
            completed = t.get("completed_date", "")
            date_str = f"({completed})" if completed else ""
            lines.append(f"- **{task_id}** - {task} {date_str}")
    else:
        lines.append("- （無）")
    
    # Open Bugs (如果有)
    if open_bugs:
        lines.extend([
            "",
            "---",
            "",
            "## 🐛 Open Bugs",
            "",
        ])
        for b in open_bugs:
            severity = b.get("severity", "low")
            bug_id = b.get("id", "")
            title = b.get("title", "")
            sev_icon = "🔴" if severity == "high" else "🟡" if severity == "medium" else "🟢"
            lines.append(f"- **{bug_id}** {sev_icon} {title}")
    
    # Footer
    lines.extend([
        "",
        "---",
        "",
        "## 📌 圖例",
        "",
        "| 標記 | 意義 |",
        "|------|------|",
        "| 🔴 P1 | 緊急重要 |",
        "| 🟡 To Do | 待處理 |",
        "| 🟢 In Progress | 進行中 |",
        "| 🔵 Review | 待審查 |",
        "| ✅ Done | 已完成 |",
        "",
        f"*最後更新: {format_date()} (台北)*",
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Kanban 看板生成器")
    parser.add_argument("--dry-run", action="store_true", help="預覽不儲存")
    parser.add_argument("--show", action="store_true", help="顯示但不儲存")
    parser.add_argument("--telegram", action="store_true", help="發送到 Telegram")
    
    args = parser.parse_args()
    
    # 載入資料
    todos = load_todos()
    bugs = load_bugs()
    
    # 生成內容
    content = generate_kanban(todos, bugs)
    
    if args.dry_run or args.show:
        # 預覽模式
        print(content)
        if args.dry_run:
            print("\n⚠️ --dry-run: 未儲存檔案")
    else:
        # 儲存模式
        with open(KANBAN_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已更新 kanban.md")
        print(f"📁 路徑: {KANBAN_FILE}")
    
    # Telegram 發送 (預留)
    if args.telegram:
        print("📱 發送到 Telegram... (TODO)")
        # 這裡可以加入 Telegram 發送邏輯


if __name__ == "__main__":
    main()
