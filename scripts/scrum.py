"""
Scrum Agile Task Tracker
簡單的 Scrum 追蹤系統
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import json
import os

SCRUM_FILE = "/home/node/.openclaw/workspace/scrum.json"


class TaskStatus(Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.BACKLOG
    priority: Priority = Priority.MEDIUM
    story_points: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    sprint: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "story_points": self.story_points,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "sprint": self.sprint,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data.get("status", "backlog")),
            priority=Priority(data.get("priority", "medium")),
            story_points=data.get("story_points", 1),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.now(),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            sprint=data.get("sprint"),
            tags=data.get("tags", [])
        )


@dataclass
class Sprint:
    name: str
    goal: str = ""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    task_ids: list[str] = field(default_factory=list)
    velocity: int = 0  # 完成的 story points
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "goal": self.goal,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "task_ids": self.task_ids,
            "velocity": self.velocity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Sprint":
        return cls(
            name=data["name"],
            goal=data.get("goal", ""),
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None,
            task_ids=data.get("task_ids", []),
            velocity=data.get("velocity", 0)
        )


class ScrumBoard:
    """Scrum 看板"""
    
    def __init__(self):
        self.tasks: dict[str, Task] = {}
        self.sprints: dict[str, Sprint] = {}
        self.current_sprint: Optional[str] = None
        self._load()
    
    def _load(self):
        """從檔案載入"""
        if os.path.exists(SCRUM_FILE):
            try:
                with open(SCRUM_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = {k: Task.from_dict(v) for k, v in data.get("tasks", {}).items()}
                    self.sprints = {k: Sprint.from_dict(v) for k, v in data.get("sprints", {}).items()}
                    self.current_sprint = data.get("current_sprint")
            except Exception as e:
                print(f"載入失敗: {e}")
    
    def _save(self):
        """儲存到檔案"""
        data = {
            "tasks": {k: v.to_dict() for k, v in self.tasks.items()},
            "sprints": {k: v.to_dict() for k, v in self.sprints.items()},
            "current_sprint": self.current_sprint
        }
        with open(SCRUM_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ============ Task 操作 ============
    
    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        story_points: int = 1,
        tags: list[str] = None
    ) -> Task:
        """新增任務"""
        task_id = f"T{len(self.tasks) + 1:03d}"
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            story_points=story_points,
            tags=tags or []
        )
        self.tasks[task_id] = task
        self._save()
        return task
    
    def update_status(self, task_id: str, status: TaskStatus) -> bool:
        """更新任務狀態"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = status
        task.updated_at = datetime.now()
        
        if status == TaskStatus.DONE:
            task.completed_at = datetime.now()
        
        self._save()
        return True
    
    def assign_to_sprint(self, task_id: str, sprint_name: str) -> bool:
        """指派任務到 Sprint"""
        if task_id not in self.tasks or sprint_name not in self.sprints:
            return False
        
        self.tasks[task_id].sprint = sprint_name
        self.sprints[sprint_name].task_ids.append(task_id)
        self._save()
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """刪除任務"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._save()
            return True
        return False
    
    # ============ Sprint 操作 ============
    
    def create_sprint(
        self,
        name: str,
        goal: str = "",
        duration_weeks: int = 2
    ) -> Sprint:
        """建立 Sprint"""
        start = datetime.now()
        end = start + timedelta(weeks=duration_weeks)
        
        sprint = Sprint(
            name=name,
            goal=goal,
            start_date=start,
            end_date=end
        )
        self.sprints[name] = sprint
        
        if not self.current_sprint:
            self.current_sprint = name
        
        self._save()
        return sprint
    
    def set_current_sprint(self, sprint_name: str) -> bool:
        """設定當前 Sprint"""
        if sprint_name in self.sprints:
            self.current_sprint = sprint_name
            self._save()
            return True
        return False
    
    def complete_sprint(self, sprint_name: str) -> dict:
        """完成 Sprint，計算 velocity"""
        if sprint_name not in self.sprints:
            return {}
        
        sprint = self.sprints[sprint_name]
        completed_points = sum(
            self.tasks[tid].story_points 
            for tid in sprint.task_ids 
            if tid in self.tasks and self.tasks[tid].status == TaskStatus.DONE
        )
        sprint.velocity = completed_points
        self._save()
        
        return {
            "sprint": sprint_name,
            "total_tasks": len(sprint.task_ids),
            "completed_points": completed_points,
            "velocity": completed_points
        }
    
    # ============ 檢視 ============
    
    def get_backlog(self) -> list[Task]:
        """取得 Product Backlog"""
        return [t for t in self.tasks.values() if t.status == TaskStatus.BACKLOG]
    
    def get_sprint_backlog(self, sprint_name: str = None) -> list[Task]:
        """取得 Sprint Backlog"""
        sprint_name = sprint_name or self.current_sprint
        if not sprint_name or sprint_name not in self.sprints:
            return []
        
        return [
            self.tasks[tid] 
            for tid in self.sprints[sprint_name].task_ids 
            if tid in self.tasks
        ]
    
    def get_board(self, sprint_name: str = None) -> dict:
        """取得 Kanban Board 視圖"""
        sprint_name = sprint_name or self.current_sprint
        tasks = self.get_sprint_backlog(sprint_name) or list(self.tasks.values())
        
        board = {
            "todo": [],
            "in_progress": [],
            "review": [],
            "done": []
        }
        
        for task in tasks:
            if task.status.value in board:
                board[task.status.value].append(task)
        
        return board
    
    def get_stats(self) -> dict:
        """取得統計資料"""
        total = len(self.tasks)
        done = sum(1 for t in self.tasks.values() if t.status == TaskStatus.DONE)
        in_progress = sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS)
        
        total_points = sum(t.story_points for t in self.tasks.values())
        done_points = sum(t.story_points for t in self.tasks.values() if t.status == TaskStatus.DONE)
        
        return {
            "total_tasks": total,
            "done_tasks": done,
            "in_progress_tasks": in_progress,
            "backlog_tasks": total - done - in_progress,
            "total_story_points": total_points,
            "done_story_points": done_points,
            "completion_rate": round(done / total * 100, 1) if total > 0 else 0
        }
    
    def print_board(self):
        """在終端機顯示看板"""
        stats = self.get_stats()
        print("\n" + "="*60)
        print(f"📊 Scrum Board - {self.current_sprint or 'No Sprint'}")
        print("="*60)
        print(f"總任務: {stats['total_tasks']} | 完成: {stats['done_tasks']} | 進行中: {stats['in_progress_tasks']}")
        print(f"Story Points: {stats['done_story_points']}/{stats['total_story_points']} ({stats['completion_rate']}%)")
        print("-"*60)
        
        board = self.get_board()
        
        for status, tasks in [
            ("📋 TODO", board["todo"]),
            ("🔄 IN PROGRESS", board["in_progress"]),
            ("👀 REVIEW", board["review"]),
            ("✅ DONE", board["done"])
        ]:
            print(f"\n{status} ({len(tasks)})")
            for task in tasks:
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[task.priority.value]
                print(f"  {task.id} {priority_icon} {task.title} ({task.story_points} pts)")
        
        print("\n" + "="*60)


# ============ 快捷命令 ============

def cmd(args: list[str] = None):
    """命令列介面"""
    board = ScrumBoard()
    args = args or []
    
    if not args:
        board.print_board()
        return
    
    cmd = args[0]
    
    if cmd == "board":
        board.print_board()
    
    elif cmd == "add" and len(args) > 1:
        title = " ".join(args[1:])
        task = board.add_task(title)
        print(f"✅ 已新增: {task.id} - {task.title}")
    
    elif cmd == "sprint" and len(args) > 1:
        if args[1] == "create" and len(args) > 2:
            name = args[2]
            goal = " ".join(args[3:]) if len(args) > 3 else ""
            sprint = board.create_sprint(name, goal)
            print(f"✅ Sprint 建立: {sprint.name} (目標: {sprint.goal})")
        elif args[1] == "current":
            print(f"目前 Sprint: {board.current_sprint}")
        elif args[1] == "list":
            for name, sprint in board.sprints.items():
                print(f"  {name}: {sprint.goal}")
    
    elif cmd == "move" and len(args) > 2:
        task_id = args[1]
        status = args[2]
        if board.update_status(task_id, TaskStatus(status)):
            print(f"✅ {task_id} → {status}")
        else:
            print(f"❌ 找不到任務: {task_id}")
    
    elif cmd == "stats":
        stats = board.get_stats()
        print(f"""
📊 統計:
  總任務: {stats['total_tasks']}
  完成: {stats['done_tasks']} ({stats['completion_rate']}%)
  進行中: {stats['in_progress_tasks']}
  Backlog: {stats['backlog_tasks']}
  Story Points: {stats['done_story_points']}/{stats['total_story_points']}
        """)
    
    else:
        print("""
📖 Commands:
  board              - 顯示看板
  add <title>       - 新增任務
  sprint create <name> [goal] - 建立 Sprint
  sprint current    - 顯示當前 Sprint
  sprint list       - 列出所有 Sprint
  move <id> <status>- 移動任務 (todo/in_progress/review/done)
  stats              - 顯示統計
        """)


if __name__ == "__main__":
    import sys
    cmd(sys.argv[1:])
