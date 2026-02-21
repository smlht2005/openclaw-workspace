"""
初始化 Scrum Backlog
"""

from scrum import ScrumBoard, Priority, TaskStatus

board = ScrumBoard()

# 建立第一個 Sprint
sprint1 = board.create_sprint("Sprint 1", "Token Tracker MVP", duration_weeks=1)
print(f"✅ 建立 Sprint: {sprint1.name}")

# 加入任務到 Product Backlog
tasks_data = [
    ("Phase 1: JSON 檔案持久化", "將使用量資料寫入檔案，重啟後不消失", Priority.HIGH, 2, ["token-tracker"]),
    ("Phase 2: 整合 OpenClaw 追蹤", "自動追蹤每個 session 的 token 使用量", Priority.HIGH, 3, ["openclaw"]),
    ("Phase 3: 網頁儀表板", "用 Canvas 做視覺化儀表板", Priority.MEDIUM, 3, ["ui"]),
    ("Phase 4: 更多模型支援", "支援常見 LLM 模型的定價", Priority.MEDIUM, 1, ["token-tracker"]),
    ("Phase 5: 自動 report", "每日/每週自動生成使用報告", Priority.LOW, 2, ["automation"]),
]

for title, desc, priority, points, tags in tasks_data:
    task = board.add_task(title, desc, priority, points, tags)
    print(f"✅ 加入: {task.id} - {task.title}")

# 移動 T001 到 Sprint Backlog
board.assign_to_sprint("T001", "Sprint 1")
board.update_status("T001", TaskStatus.TODO)

# 顯示看板
board.print_board()
