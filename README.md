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
📋 Todo → 🔄 In Progress → 🔍 Review → ✅ Done → 📦 Archive
```

#### 優先級
| 等級 | 標記 | 意義 |
|------|------|------|
| P1 | 🔴 | 緊急重要 |
| P2 | 🟡 | 重要 |
| P3 | 🟢 | 普通 |
| P4 | ⚪ | 低優先級 |

#### 狀態標記
| 狀態 | 標記 | 說明 |
|------|------|------|
| 待處理 | 📋 Todo | 新建任務 |
| 進行中 | 🔄 In Progress | 開發中 |
| 待檢視 | 🔍 Review | 等待 Review |
| 已完成 | ✅ Done | Review 通過 |
| 歸檔 | 📦 Archive | 已歸檔 |
| 阻塞 | ⚠️ Blocked | 被阻塞 |

---

#### 📋 Kanban 完整流程

**Step 1: 建立任務 (Todo)**
```
1. 在 todos/{專案}.md 新增任務
2. 狀態標記為 📋 Todo
3. 指定優先級 (P1-P4)
4. 更新 kanban.md 的 Summary + Detail
```

**Step 2: 開始開發 (In Progress)**
```
1. 狀態改為 🔄 In Progress
2. 更新 kanban.md
3. 開始實作
```

**Step 3: 提交 Review**
```
1. 狀態改為 🔍 Review
2. 在 review/ 建立 T00X-任務名稱.md
3. 填寫 Review 檢查清單
4. 更新 kanban.md
```

**Step 4: Review 通過 (Done)**
```
1. 檢視通過 → 狀態改為 ✅ Done
2. 移動 review 檔案到 archive/
3. 更新 kanban.md
```

**Step 5: 歸檔 (Archive)**
```
1. 已完成的任務可移到 archive/
2. 維持 ✅ Done 標記
3. 檔案移到 archive/ 目錄
```

---

#### 📁 檔案位置

| 類型 | 路徑 |
|------|------|
| 看板 | `kanban.md` |
| 任務清單 | `todos/{專案}.md` |
| 待審查 | `review/T00X-任務名稱.md` |
| 已歸檔 | `archive/T00X-任務名稱.md` |

---

#### 📝 Review 範本

```markdown
# T00X 任務名稱 - Review

## 任務資訊
- **ID**: T00X
- **任務**: 任務名稱
- **優先級**: P2
- **狀態**: 🔍 Review
- **完成日期**: YYYY-MM-DD

## 實作摘要
- 完成功能 1
- 完成功能 2

## 檢視項目
- [ ] 功能正常運作
- [ ] 程式碼品質良好
- [ ] 已更新相關文件

## 檢視結果
- [ ] ✅ 通過
- [ ] ❌ 需修改

## 備註
```

---

#### ✅ 使用範例

```bash
# 1. 新建任務
# 編輯 todos/my-project.md，加入：
# - T010 - 新功能 [P2] 📋

# 2. 開始開發
# 狀態改為 🔄 In Progress

# 3. 提交 Review
# 狀態改為 🔍 Review
# 建立 review/T010-new-feature.md

# 4. Review 通過
# 狀態改為 ✅ Done
# 移動 T010-new-feature.md 到 archive/
```

---

#### 📊 Kanban 看板檢視

```bash
# 查看目前看板
cat kanban.md
```

看板範例：
```
| 狀態 | 數量 | 備註 |
|------|------|------|
| 🔴 P1 | 0 | 緊急 |
| 🟡 To Do | 2 | 待處理 |
| 🟢 In Progress | 1 | 進行中 |
| 🔵 Review | 1 | 待檢視 |
| ✅ Done | 3 | 已完成 |
```

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
[A-TAO] <類型>: <標題>

<說明>

類型: feat | fix | docs | refactor | test | qa
```

### PR 格式
```
[A-TAO] [類型] <標題>
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

## 📧 Email Service

### 設定
- 檔案: `.env`
- 格式:
```
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

### 使用方式
```bash
python3 email_service.py <收件人> <主旨> <內文> [附件路徑]
```

### 範例
```bash
python3 email_service.py "test@example.com" "Subject" "Body content"
```

---

## 🎙️ TTS 語音服務

### 設定位置
- 檔案: `/home/node/.openclaw/openclaw.json`
- 區塊: `messages.tts`

### 完整設定範例
```json
{
  "messages": {
    "tts": {
      "auto": "off",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-TW-HsiaoChenNeural",
        "lang": "zh-TW"
      }
    }
  }
}
```

### 可用的中文聲音
| 聲音代碼 | 說明 |
|----------|------|
| `zh-TW-HsiaoChenNeural` | 曉晨 (推薦) |
| `zh-TW-HsiaoYuNeural` | 曉雨 |
| `zh-CN-XiaoxiaoNeural` | 曉曉 (普通話) |

### 發送語音指令
```python
tts(channel="telegram", text="要轉換的文字")
message(action="send", filePath="/tmp/voice.mp3", asVoice="true")
```

---

## 📊 Cron Jobs

### 目前的定時任務
| 任務 | 時間 (台灣) | 頻率 |
|------|------------|------|
| 黃金價格 | 10:00, 12:00 | 每天 |
| 台股報價 (大同/長榮) | 10:00, 12:00 | 週一至週五 |
| Scrum Report | 14:00 | 每天 |

---

## 📂 相關文檔

| 檔案 | 說明 |
|------|------|
| `docs/tts_handbook.md` | TTS 完整設定手冊 |
| `docs/voice_help.md` | Telegram 語音訊息指南 |
| `email_service.py` | Email 發送服務 |

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

*最後更新: 2026-02-21*
