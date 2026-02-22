# 使用量分析範例

## 數據來源

### daily_tracker.py 執行流程
1. 先寫入 `daily_usage.json`（JSON 持久化）
2. 再輸出 Markdown 報告

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

---

## 正常範例

```markdown
📊 Token 使用報告 - 2026-02-16

### 📈 數據摘要
| 項目 | 數值 |
|------|------|
| 模型 | MiniMax-M2.5 |
| 執行時間 | 09:00 (台北) |
| Input | 45,230 tokens |
| Output | 8,120 tokens |
| Total | 53,350 tokens |
| Context | 25.9% |
| 備註 | - |

### 💡 建議
- ✅ 使用量正常，維持現狀
- 下午可跑深度任務
```

## Context > 80% 範例

```markdown
⚠️ Token 使用報告 - 需要注意

### 📈 數據摘要
| 項目 | 數值 |
|------|------|
| 模型 | MiniMax-M2.5 |
| 執行時間 | 21:00 (台北) |
| Input | 285,000 tokens |
| Output | 12,500 tokens |
| Total | 297,500 tokens |
| Context | **100%** 🔴 |
| 備註 | 建議 /new |

### 🔥 關注重點
Context 滿載，Input 過高，任務執行效率差

### 💡 建議
- ⚠️ 建議馬上用 `/new` 開新 session
- 檢查是否有長對話導致 context 膨脹
- 考慮分段處理任務
```

## Cost 異常範例

```markdown
📊 Token 使用報告 - 本週累計

### 📈 數據摘要
| 項目 | 數值 |
|------|------|
| 模型 | MiniMax-M2.5 |
| 執行時間 | 09:00 (台北) |
| 本週總量 | 2,450,000 tokens |
| 上週總量 | 1,200,000 tokens |
| 漲幅 | +104% ⚠️ |
| 備註 | 需排查 |

### 🔥 關注重點
使用量翻倍成長，需排查原因

### 💡 建議
- 排查是否有自動化任務失控
- 考慮啟用較小模型處理簡單任務
- 檢查是否有測試資料未被標記
```
