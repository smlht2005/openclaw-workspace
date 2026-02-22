# Bug Tracker 範本

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
      "affected_files": ["檔案1", "檔案2"]
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

## Bug 位置
- `/home/node/.openclaw/workspace/bugs/issues.json`
