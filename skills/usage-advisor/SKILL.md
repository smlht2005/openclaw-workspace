---
name: usage-advisor
description: 分析 cron 排程結果（如 Token 使用報告）並給出建議和評論。當需要解讀定時任務輸出、分析使用量趨勢、提供優化建議時觸發。
---

# 使用量顧問

分析 cron 排程的輸出數據，提供有價值的建議和評論。

## 數據來源

### daily_tracker.py
- **執行流程**：
  1. 先寫入 `daily_usage.json`（JSON 持久化）
  2. 再輸出 Markdown 報告
- **JSON 位置**：`/home/node/.openclaw/workspace/daily_usage.json`
- **即時資料**：`/home/node/.openclaw/workspace/current_session_usage.json`

### JSON 結構
```json
{
  "timestamp": "2026-02-16 09:00:00",
  "sessions": [{
    "session_key": "agent:main:main",
    "model": "MiniMax-M2.5",
    "input_tokens": 45000,
    "output_tokens": 8000,
    "total_tokens": 53000,
    "context_tokens": 204800,
    "context_pct": 25.9
  }],
  "total_input_tokens": 45000,
  "total_output_tokens": 8000,
  "total_tokens": 53000,
  "active_sessions": 1
}
```

## 分析維度

### 1. Token 使用量
- **Input tokens**: 是否過高？（>100k 建議開新 session）
- **Output tokens**: 產出是否合理
- **Context 使用率**: >80% 時建議重置
- **與前次比較**: 是否有異常波動

### 2. コスト意識
- 單日/單週總量是否合理
- 是否有不必要的浪費（如重複請求）

### 3. 建議格式

#### 正常情況
```markdown
📊 [報告類型]

### 📈 數據摘要
| 項目 | 數值 |
|------|------|
| 模型 | MiniMax-M2.5 |
| 執行時間 | HH:MM (台北) |
| Input | X tokens |
| Output | X tokens |
| Total | X tokens |
| Context | X% |
| 備註 | - |

### 💡 建議
- [建議 1-2 點]
```

#### Context > 80% 情況（高優先級）
```markdown
⚠️ [報告類型] - 需要注意

### 📈 數據摘要
| 項目 | 數值 |
|------|------|
| 模型 | MiniMax-M2.5 |
| 執行時間 | HH:MM (台北) |
| Input | X tokens |
| Output | X tokens |
| Total | X tokens |
| Context | **X%** 🔴 |
| 備註 | 建議 /new |

### 🔥 關注重點
- [1 句精簡摘要]

### 💡 建議
- 建議使用 `/new` 開新 session 重置 Context
- [其他建議]
```

## 觸發條件
- Context 使用率 > 80% → 需要特別關注
- Input tokens 異常高時

## 輸出原則
- 保持簡短，最多 3-5 點建議
- 用繁體中文
- 語氣像個資深工程師哥們
- Markdown 格式
