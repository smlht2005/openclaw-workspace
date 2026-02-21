# Telegram 語音訊息設定指南

## 📋 目錄
1. [如何發送語音訊息到 Telegram](#1-如何發送語音訊息到-telegram)
2. [Telegram 問題與解決方案](#2-telegram-問題與解決方案)
3. [前置要求](#3-前置要求)

---

## 1. 如何發送語音訊息到 Telegram

### 前置要求
- OpenClaw 已安裝並正常運作
- 已設定 Telegram Bot Token
- ✅ 已安裝 FFmpeg (用於轉換音訊格式)

### 安裝 FFmpeg

Telegram 語音訊息需要 .ogg (Opus) 格式，FFmpeg 負責轉換：

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Mac
brew install ffmpeg
```

#### Step 1: 產生語音 (使用 TTS)
```python
# 使用內建 tts 工具 (預設英文)
tts(
    channel="telegram",
    text="要轉換的文字"
)

# ✅ 設定中文聲音
tts(
    channel="telegram",
    text="要轉換的文字",
    voice="zh-TW-HsiaoChenNeural"  # 曉晨 (中文)
)
```

### 可用的中文聲音

| 聲音代碼 | 說明 |
|----------|------|
| `zh-TW-HsiaoChenNeural` | 曉晨 (推薦) |
| `zh-TW-HsiaoYuNeural` | 曉雨 |
| `zh-CN-XiaoxiaoNeural` | 曉曉 (普通話) |

#### Step 2: 發送語音訊息 (關鍵！)
```python
message(
    action="send",
    filePath="/tmp/tts_voice/output.mp3",
    message="選填的描述",
    asVoice="true"  # ← 必加參數！
)
```

### ⚠️ 重要提醒

| 參數 | 必要性 | 說明 |
|------|--------|------|
| `asVoice` | **必加** | 設為 `true` 才會以語音訊息傳送 |

**若忘記加 `asVoice="true"`，Telegram 會以一般音檔播放，無法連續播放多個語音（會覆蓋）。**

---

## 2. Telegram 問題與解決方案

### 問題 1: 語音重疊播放 (T011)

**現象：** 連續發送多個語音訊息時，音樂會重疊播放

**原因：** 發送時缺少 `asVoice="true"` 參數

**解決方案：**
- 發送語音時**務必加入 `asVoice="true"`**
- 這樣 Telegram 會以 Voice Message 處理，避免重疊

---

### 問題 2: Cron Delivery 發送到 Telegram 失敗 (T009, BUG-001~003)

**現象：** Cron Job 設定 delivery 到 Telegram 失敗

**錯誤訊息：**
```
Unknown target "telegram" for Telegram. Hint: <chatId>
```

**原因：** delivery 設定缺少 `to` 參數（chatId）

**解決方案：**
```json
{
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "你的chatId"  // ← 必填！
  }
}
```

**修正指令：**
```bash
openclaw cron update <jobId> --patch '{"delivery": {"channel": "telegram", "to": "你的chatId"}}'
```

---

## 📂 相關檔案

| 檔案 | 說明 |
|------|------|
| `skills/tts-voice-reply/SKILL.md` | 語音回覆 Skill 完整說明 |
| `skills/scrum-kanban/SKILL.md` | Scrum 看板管理 |
| `.env` | Gmail SMTP 設定 |

---

## 📅 更新日誌

- 2026-02-21: 初始版本
