---
name: session-restart
description: |
  Session 重新啟動時的初始化流程。當使用 /new、/reset 或 session 意外中斷後重新連線時觸發。
  用於載入上下文、建立狀態、提供歡迎訊息。
  觸發時機：(1) 使用 /new 或 /reset 命令 (2) 長時間斷線後重新連線 (3) 任何 session 初始化場景
---

# Session Restart Skill

當 session 重新啟動時，按照以下順序執行：

## 0. 讀取上一次的 Startup Report (如有)

```bash
# 讀取上一次的 report (如有)
read reports/session-startup-YYYYMMDD.md
```

如有上一次的 report，先輸出到 Telegram 告知用戶：「這是上次 session 的結尾報告」

## 1. 讀取 Memory + Ruler

依序讀取以下檔案以恢復上下文：

```bash
# 讀取格式規範 (重要！)
read ruler.md

# 讀取長期記憶
read MEMORY.md

# 讀取今天的 daily memory (如果存在)
read memory/YYYY-MM-DD.md

# 讀取昨天的 daily memory (獲取最近上下文)
read memory/YYYY-MM-DD.md (昨天的日期)
```

## 2. 檢查 Cron Jobs 狀態

執行以下命令檢查排程任務：

```bash
cron action=list
cron action=status
```

檢查的重點：
- 是否有失敗的 jobs
- 是否有即將執行的重要任務
- 是否有 pending 的 wake events

## 3. 檢查 Session 狀態

```bash
session_status
```

查看：
- 目前的 model
- 使用量統計
- 對話時間

## 4. 產生 Startup Report

整合以上資訊，產出一份簡潔的 report 給使用者，包含：

- 📅 日期/時間 **(台北時間 UTC+8)**
- 📊 Session 狀態 (model, 使用量)
- ⏰ 待處理的 cron jobs
- 📝 最近的心得/筆記 (從 memory)
- 🎯 提醒事項 (如果有)

**務必遵守 ruler.md 的格式規範，特別是：**
- 時間使用台北時間格式: `YYYY-MM-DD HH:MM (台北)`
- 報告不使用表格
- 使用 emoji 標記

## 5. 輸出歡迎訊息

根據上下文產生個人化的歡迎訊息：
- 如果有重要事項 → 直接告知
- 如果沒什麼特別的 → 簡單問候 + "有什麼需要幫忙的？"

## 6. 儲存 Report 到檔案

將步驟 4 產生的 report 儲存到：

```bash
reports/session-startup-YYYYMMDD.md
```

這樣下次啟動時可以讀取上一次的 report。

---

## 注意事項

- 如果是 fresh session (無 memory 檔案)，跳過 memory 讀取步驟
- 只報告重要的事項，避免資訊過載
- 保持輸出簡潔有力
