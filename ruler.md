# 格式規範 (Ruler)

---

## 📊 Token 報告格式

**原則：** 不使用表格，適合手機螢幕閱讀

```
📊 Token 使用報告
⏰ YYYY-MM-DD HH:MM:SS (台北)
🤖 {model}
📱 Sessions: {N}
🧮 Input: {N}
🧮 Output: {N}
🧮 Total: {N}
📊 Context: {N}%

📈 趨勢
MM-DD ████████ {N}
```

### 範例
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

## 📋 Todo 任務格式

### Product Backlog
| ID | 任務 | 優先級 | 狀態 | 估點 | 備註 |
|----|------|--------|------|------|------|

### Sprint
- 📋 To Do
- 🔄 In Progress  
- 🔍 Review
- ✅ Done

### 優先級
- P1: 緊急重要
- P2: 重要
- P3: 普通
- P4: 低優先級

### 狀態標記
- 📋 Todo / To Do
- 🔄 In Progress
- 🔍 Review（待檢視）
- ✅ Done
- ⚠️ Blocked
- 🔴 P1

---

## 🔍 Review 流程

1. 任務完成 → 狀態改為 🔍 Review
2. 在 `review/` 建立 `.md` 檔
3. 檢視通過 → ✅ Done，移到 `archive/`
4. 需修改 → 改回 🔄 In Progress

### Review 格式
```markdown
# T00X 任務名稱 - Review

## 任務資訊
- **ID**: T00X
- **任務**: 名稱
- **完成日期**: YYYY-MM-DD

## 實作摘要
- 

## 檢視項目
- [ ] 功能正常
- [ ] 程式碼品質

## 檢視結果
- [ ] ✅ 通過
- [ ] ❌ 需修改

## 備註
```

---

## 🐛 Bug 追蹤格式

### Bug JSON
```json
{
  "bugs": [{
    "id": "BUG-001",
    "title": "標題",
    "description": "描述",
    "severity": "high|medium|low",
    "status": "open|fixed|pending",
    "created_at": "YYYY-MM-DD",
    "resolved_at": "YYYY-MM-DD",
    "root_cause": "原因",
    "solution": "解決方案",
    "affected_files": []
  }]
}
```

### 嚴重性
- high: 影響主要功能
- medium: 功能異常
- low: 小問題

---

## 📁 檔案位置

- 報告格式: `templates/token-report-format.md`
- Todo 模板: `templates/scrum-todos.md`
- Bug 模板: `templates/bug-template.md`
- Kanban: `kanban.md`
- Todos: `todos/*.md`
- Review: `review/*.md`
- Archive: `archive/`
- Bugs: `bugs/issues.json`

---

## 🔀 Git Workflow 規範

### 原則
1. **不直接修改** `main` 分支
2. **建立新分支** → 提交變更
3. **建立 PR** → 讓作者審查
4. **作者決定** 是否合併

### 分支命名規範
| 類型 | 範例 |
|------|------|
| 功能開發 | `feature/xxx` |
| Bug 修復 | `fix/xxx` |
| Code Review | `review/xxx` |
| QA 審查 | `qa/xxx` |

### Commit 訊息格式
```
<類型>: <標題>

<說明>
```

#### 類型
- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文件更新
- `refactor`: 重構
- `test`: 測試
- `qa`: QA 審查

### PR 標題格式
```
[類型] <標題>
```

#### 範例
```
[Feature] 新增用戶認證
[Fix] 修正登入問題
[QA] Code Review 建議
[Refactor] 重構資料庫模組
```

### 審查流程
1. 建立分支並提交變更
2. Push 到遠端
3. 建立 PR
4. 由作者或維護者審查
5. 通過 → 合併
6. 失敗 → 修改後重新提交

---

*最後更新：2026-02-16*
