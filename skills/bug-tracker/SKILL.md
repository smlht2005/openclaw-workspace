---
name: bug-tracker
description: Bug 追蹤管理。當需要記錄、查詢、更新 bug 狀態時觸發。使用於問題追蹤、技術債管理。
---

# Bug Tracker 技能

管理專案 Bug，儲存於 `bugs/issues.json`

## 檔案位置

- **Bug 清單**: `/home/node/.openclaw/workspace/bugs/issues.json`
- **模板**: `/home/node/.openclaw/workspace/templates/bug-template.md`

## Bug JSON 格式

```json
{
  "bugs": [
    {
      "id": "BUG-001",
      "title": "標題",
      "description": "描述",
      "severity": "high|medium|low",
      "status": "open|fixed|pending",
      "created_at": "YYYY-MM-DD",
      "resolved_at": "YYYY-MM-DD",
      "root_cause": "原因分析",
      "solution": "解決方案",
      "affected_files": ["檔案1"]
    }
  ]
}
```

## 嚴重性分類

- **high**: 影響主要功能運作
- **medium**: 功能異常但不影響核心
- **low**: 小問題或外觀問題

## 狀態

- **open**: 待處理
- **fixed**: 已修復
- **pending**: 等待中

## 常用操作

### 新增 Bug
```bash
# 讀取現有 bug
# 加入新 bug 到 JSON
# 存回 issues.json
```

### 查詢 Bug
```bash
# 讀取 issues.json
# 顯示所有 bug 或依 severity/status 篩選
```

### 更新狀態
```bash
# 找到 bug ID
# 更新 status
# 填入 resolved_at
```

## 輸出格式（參考 ruler.md）

不使用表格，簡潔呈現：

```
🐛 Bug 列表

🔴 High (N)
- BUG-001: 標題 [open]

🟡 Medium (N)
- BUG-002: 標題 [fixed]

🟢 Low (N)
- (無)
```

## 觸發時機
- 回報新 bug
- 查詢 bug 狀態
- 更新 bug 狀態
- Sprint Review 時檢視
