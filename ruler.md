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
