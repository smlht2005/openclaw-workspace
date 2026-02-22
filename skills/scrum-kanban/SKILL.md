---
name: scrum-kanban
description: Scrum Kanban 看板管理。當需要建立、更新、管理任務看板時觸發。使用於追蹤專案任務進度、管理 Sprint、產品待辦清單。
---

# Scrum Kanban 看板管理

管理專案任務看板，包含 Summary 和 Detail 兩個區塊。

## 檔案位置

- **Kanban 看板**: `/home/node/.openclaw/workspace/kanban.md`
- **專案任務**: `/home/node/.openclaw/workspace/todos/{專案名稱}.md`
- **待審查**: `/home/node/.openclaw/workspace/review/{TaskID}-{任務名稱}.md`
- **已完成**: `/home/node/.openclaw/workspace/archive/`

## 格式範本

### Summary 摘要
```markdown
| 狀態 | 數量 | 備註 |
|------|------|------|
| 🔴 P1 | 0 | 緊急 |
| 🟡 To Do | 0 | 待處理 |
| 🟢 In Progress | 0 | 進行中 |
| 🔵 Review | 0 | 待檢視 |
| ✅ Done | 0 | 已完成 |
```

### Detail 詳情
```markdown
### 🟡 To Do 待處理
- （無）

### 🟢 In Progress 進行中
- （無）

### 🔵 Review 待檢視
- （無）

### ✅ Done 已完成
- （無）
```

## 工作流程

### 1. 建立新任務
1. 在 `todos/{專案}.md` 新增任務（狀態 📋 Todo）
2. 更新 `kanban.md` 的 Summary 和 Detail

### 2. 開始任務
1. 狀態改為 🔄 In Progress
2. 更新 kanban

### 3. 任務完成 → Review
1. 狀態改為 🔍 Review
2. 在 `review/` 建立檢視檔案
3. 更新 kanban

### 4. Review 通過 → Done
1. 狀態改為 ✅ Done
2. 移動檢視檔案到 `archive/`
3. 更新 kanban

## 常用操作

### 查詢看板
```bash
cat /home/node/.openclaw/workspace/kanban.md
```

### 更新範例
```markdown
## 📊 Summary 摘要

| 狀態 | 數量 | 備註 |
|------|------|------|
| 🔴 P1 | 0 | 緊急 |
| 🟡 To Do | 2 | - |
| 🟢 In Progress | 0 | - |
| 🔵 Review | 1 | - |
| ✅ Done | 2 | - |

## 📝 Detail 詳情

### 🟡 To Do 待處理
- **T004** - 網頁儀表板 [P2]
- **T005** - 更多模型支援 [P2]

### 🔵 Review 待檢視
- **T002** - Telegram 報告發送

### ✅ Done 已完成
- **T001** - JSON 持久化
- **T003** - 每日 Session 追蹤
```

## 優先級
- P1: 緊急重要
- P2: 重要
- P3: 普通
- P4: 低優先級

## 狀態標記
- 📋 Todo / To Do
- 🔄 In Progress
- 🔍 Review
- ✅ Done
- ⚠️ Blocked
