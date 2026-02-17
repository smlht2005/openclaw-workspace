# 🐧 OpenClaw Assistant - 濤哥的 AI 助手

> 專為濤哥打造的 OpenClaw 工作環境，內建 SOP、格式規範與自動化流程

---

## 📁 專案結構

```
/home/node/.openclaw/workspace/
├── AGENTS.md          # AI 行為準則
├── SOUL.md            # AI 人格設定
├── USER.md            # 使用者資訊
├── IDENTITY.md        # AI 身份設定
├── MEMORY.md          # 長期記憶
├── ruler.md           # 格式規範 (非常重要！)
├── kanban.md          # 任務看板
├── HEARTBEAT.md       # 心跳檢查清單
│
├── skills/            # 技能模組
│   ├── session-sop/       # Session 結束 SOP
│   ├── session-restart/  # Session 啟動流程
│   ├── scrum-kanban/      # Scrum 看板管理
│   ├── bug-tracker/      # Bug 追蹤
│   ├── ruler-enforcer/   # 格式規範檢查
│   └── usage-advisor/     # Token 使用分析
│
├── memory/            # 每日工作日誌
├── todos/             # 任務清單
├── bugs/              # Bug 追蹤
├── review/            # 待審查項目
├── archive/          # 已完成任務
└── reports/           # 報告輸出
```

---

## 🕐 時區規範 (重要！)

**所有報告和輸出必須使用台北時間 (UTC+8)**

```
時間格式: YYYY-MM-DD HH:MM (台北)
例如: 2026-02-17 10:05 (台北)
```

---

## 📋 SOP 標準作業流程

### 1. Session 結束 SOP (`session-sop`)

每次重要 session 結束時執行：

1. **記錄 Session** - 建立 `memory/YYYY-MM-DD.md`
2. **更新 Todo/Bug** - 狀態同步
3. **Git 提交** - `git add -A && git commit -m "..." && git push`
4. **建立技能** - 如有需要，建立新 skill
5. **總結給用戶** - 簡述完成事項

```bash
# 常用指令
git add -A && git commit -m "feat: 完成項目" && git push
```

### 2. Session 啟動流程 (`session-restart`)

Session 重新啟動時：

1. 讀取 `MEMORY.md` + 當天/昨天的 memory
2. 檢查 cron jobs 狀態 (`cron action=list/status`)
3. 查看 session 狀態 (`session_status`)
4. 產生 Startup Report (台北時間)
5. 輸出歡迎訊息

### 3. Scrum Kanban (`scrum-kanban`)

任務狀態流程：

```
📋 Todo → 🔄 In Progress → 🔍 Review → ✅ Done
```

**優先級**: P1 (緊急) > P2 (重要) > P3 (普通) > P4 (低)

**狀態標記**:
- 📋 Todo / To Do
- 🔄 In Progress
- 🔍 Review (待檢視)
- ✅ Done
- ⚠️ Blocked
- 🔴 P1

### 4. Bug 追蹤 (`bug-tracker`)

**Bug JSON 位置**: `bugs/issues.json`

```json
{
  "id": "BUG-001",
  "title": "標題",
  "severity": "high|medium|low",
  "status": "open|fixed|pending",
  "created_at": "YYYY-MM-DD",
  "resolved_at": "YYYY-MM-DD"
}
```

---

## 📊 報告格式 (Ruler)

### Token 報告

```
📊 Token 使用報告
⏰ 2026-02-17 10:05 (台北)
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

**原則**: 不使用表格，適合手機閱讀

### Bug 列表

```
🐛 Bug 列表

🔴 High (1)
- BUG-001: 標題 [open]

🟡 Medium (1)
- BUG-002: 標題 [fixed]
```

---

## 🔀 Git Workflow

### 分支命名
| 類型 | 範例 |
|------|------|
| 功能開發 | `feature/xxx` |
| Bug 修復 | `fix/xxx` |
| Code Review | `review/xxx` |
| QA 審查 | `qa/xxx` |

### Commit 格式
```
<類型>: <標題>

<說明>

類型: feat | fix | docs | refactor | test | qa
```

### PR 格式
```
[類型] <標題>
```

---

## ⚡ 常用指令速查

```bash
# Session
openclaw gateway status
openclaw gateway restart

# Cron
cron action=list
cron action=status

# Git
git add -A && git commit -m "..." && git push

# 讀取檔案
cat kanban.md
cat bugs/issues.json
cat memory/2026-02-17.md

# 狀態
session_status
```

---

## 🤖 AI 模型

- **Default**: minimax-portal/MiniMax-M2.5
- **Available**: minimax-m2.1, minimax-m2.5

---

## 📝 格式規範摘要

| 項目 | 規範 |
|------|------|
| 時區 | 台北時間 (UTC+8) |
| 時間格式 | `YYYY-MM-DD HH:MM (台北)` |
| 報告 | 不用表格，用 emoji |
| 數字 | 千分位 (例: 53,350) |
| Commit | feat/fix/docs/refactor/test/qa |

---

*最後更新: 2026-02-17*
