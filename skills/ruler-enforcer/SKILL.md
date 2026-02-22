---
name: ruler-enforcer
description: 格式規範檢查。當需要產生報告、Todo、Review 等格式化輸出時，必須先讀取 ruler.md 確認格式規範。使用於所有需要格式化輸出的場景。
---

# Ruler - 格式規範檢查

**重要：** 產生任何格式化輸出前，必須先讀取 `/home/node/.openclaw/workspace/ruler.md`

## 速查

### 📊 Token 報告
- 不使用表格
- 每行一個項目
- 使用 emoji 圖示

### 📋 Todo 格式
- 圖示標記狀態
- 不使用複雜表格

### 🔍 Review
- 簡潔格式
- 檢查清單

---

## 檔案位置
- 規範文件: `/home/node/.openclaw/workspace/ruler.md`
- 模板: `/home/node/.openclaw/workspace/templates/`

## 觸發時機
- 產生 Token 報告
- 更新 Todo
- 建立 Review
- 建立 Bug 記錄
- 任何格式化輸出

## 輸出前檢查清單
- [ ] 已讀取 ruler.md
- [ ] 報告不使用表格
- [ ] 使用正確的 emoji 標記
- [ ] 數字使用千分位（,）
- [ ] 時間使用台北時區
