# OpenClaw Assistant

個人 AI 助手，包含 Token 追蹤、技能系統、任務管理。

---

## 📊 Token 使用追蹤

### 功能
- 每日 4 次自動記錄（09:00、12:00、18:00、21:00 台北時間）
- JSON 持久化 + Markdown 報告輸出

### 使用
```bash
python3 daily_tracker.py
```

### 輸出範例
```
📊 Token 使用報告
⏰ 2026-02-16 09:00 (台北)
🤖 MiniMax-M2.5
📱 Sessions: 2
🧮 Input: 45,230
🧮 Output: 8,120
🧮 Total: 53,350
📊 Context: 25.9%

📈 趨勢
02-15 █████████ 280,000
02-16 ██████ 180,000
```

---

## 📋 任務管理

### 檔案
- `kanban.md` - 任務看板
- `todos/` - 專案待辦

### 狀態
- 📋 Todo - 待處理
- 🔄 In Progress - 進行中
- 🔍 Review - 待審查
- ✅ Done - 已完成

---

## 🐛 Bug 追蹤

### 檔案
- `bugs/issues.json` - Bug 清單

### 格式
```json
{
  "bugs": [{
    "id": "BUG-001",
    "title": "標題",
    "severity": "high|medium|low",
    "status": "open|fixed|pending"
  }]
}
```

---

## 🔧 Skills

### 可用技能
| Skill | 功能 |
|-------|------|
| `usage-advisor` | Token 使用分析 |
| `scrum-kanban` | 任務看板管理 |
| `bug-tracker` | Bug 追蹤 |
| `ruler-enforcer` | 格式規範檢查 |

### 位置
- `/app/skills/`

---

## 📁 專案結構

```
.
├── daily_tracker.py      # Token 追蹤腳本
├── kanban.md             # 任務看板
├── ruler.md              # 格式規範
├── bugs/
│   └── issues.json       # Bug 追蹤
├── todos/
│   └── token-tracker.md  # 專案待辦
├── templates/
│   ├── bug-template.md
│   ├── scrum-todos.md
│   └── token-report-format.md
├── review/               # 任務審查
├── memory/               # 工作日誌
└── skills/               # 技能系統
```

---

## 📝 格式規範

參考 `ruler.md`

---

## 🔗 相關連結

- [GitHub Repo](https://github.com/smlht2005/openclaw-assistant)
- [OpenClaw Docs](https://docs.openclaw.ai)
