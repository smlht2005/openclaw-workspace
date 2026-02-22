# OpenClaw 知識庫 - 系統整合手冊

> 本文件整合了 Email Service、TTS 語音服務與 Telegram 整合的完整設定指南

---

## 📋 目錄

1. [Email Service (Gmail SMTP)](#1-email-service-gmail-smtp)
2. [TTS 語音服務](#2-tts-語音服務)
3. [Telegram 整合](#3-telegram-整合)
4. [Cron Jobs 排程](#4-cron-jobs-排程)
5. [常見問題與解決方案](#5-常見問題與解決方案)

---

## 1. Email Service (Gmail SMTP)

### 1.1 設定 .env
```bash
# .env 檔案
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

### 1.2 使用方式
```bash
# 基本發送
python3 scripts/email_service.py <收件人> <主旨> <內文>

# 夾帶附件
python3 scripts/email_service.py <收件人> <主旨> <內文> <附件路徑>
```

### 1.3 Gmail App Password 取得
1. 前往 https://myaccount.google.com/signinoptions/two-step-verification 啟用 2FA
2. 前往 https://myaccount.google.com/apppasswords 產生 App Password

---

## 2. TTS 語音服務

### 2.1 設定位置
- 檔案: `/home/node/.openclaw/openclaw.json`
- 區塊: `messages.tts`

### 2.2 完整設定範例
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

### 2.3 可用的中文聲音

| 聲音代碼 | 說明 |
|----------|------|
| `zh-TW-HsiaoChenNeural` | 曉晨 (推薦) |
| `zh-TW-HsiaoYuNeural` | 曉雨 |
| `zh-CN-XiaoxiaoNeural` | 曉曉 (普通話) |

### 2.4 發送語音指令
```python
# 產生語音
tts(channel="telegram", text="要轉換的文字")

# 發送語音訊息
message(action="send", filePath="/tmp/voice.mp3", asVoice="true")
```

### 2.5 前置要求 - FFmpeg 安裝
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Mac
brew install ffmpeg
```

---

## 3. Telegram 整合

### 3.1 Cron Delivery 設定
```json
{
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "你的chatId"
  }
}
```

### 3.2 指令控制

| 指令 | 說明 |
|------|------|
| `/tts on` | 開啟這次對話的語音回覆 |
| `/tts always` | 持續開啟語音回覆 |
| `/tts off` | 關閉語音回覆 |

---

## 4. Cron Jobs 排程

### 4.1 目前的定時任務

| 任務 | 時間 (台灣) | 頻率 |
|------|------------|------|
| 黃金價格 | 10:00, 12:00 | 每天 |
| 台股報價 (大同/長榮) | 10:00, 12:00 | 週一至週五 |
| Scrum Report | 14:00 | 每天 |

### 4.2 新增 Cron Job
```bash
cron action=add --job '{
  "name": "任務名稱",
  "schedule": {"kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Taipei"},
  "payload": {"kind": "agentTurn", "message": "任務描述"},
  "delivery": {"channel": "telegram", "to": "你的chatId"},
  "sessionTarget": "isolated"
}'
```

---

## 5. 常見問題與解決方案

### 問題 1: 語音重疊播放

**現象：** 連續發送多個語音訊息時，音樂會重疊播放

**原因：** 發送時缺少 `asVoice="true"` 參數

**解決方案：**
```python
message(action="send", filePath="xxx.mp3", asVoice="true")
```

---

### 問題 2: /tts 指令沒有聲音

**原因：** 缺少 FFmpeg

**解決方案：**
```bash
sudo apt install ffmpeg
```

---

### 問題 3: 語音是英文

**原因：** 預設語音是英文

**解決方案：**
在設定中加入中文語音：
```json
"edge": {
  "voice": "zh-TW-HsiaoChenNeural",
  "lang": "zh-TW"
}
```

---

### 問題 4: 環境變數設定無效

**錯誤的設定方式：**
```json
// ❌ 錯誤！
{
  "env": {
    "vars": {
      "TTS_VOICE": "zh-TW-YunJheNeural"
    }
  }
}
```

**正確的設定方式：**
```json
// ✅ 正確！
{
  "messages": {
    "tts": {
      "edge": {
        "voice": "zh-TW-HsiaoChenNeural"
      }
    }
  }
}
```

---

### 問題 5: Cron Delivery 到 Telegram 失敗

**錯誤訊息：**
```
Unknown target "telegram" for Telegram. Hint: <chatId>
```

**原因：** delivery 設定缺少 `to` 參數

**解決方案：**
```json
{
  "delivery": {
    "channel": "telegram",
    "to": "你的chatId"
  }
}
```

---

## 📂 相關檔案

| 檔案 | 說明 |
|------|------|
| `scripts/email_service.py` | Email 發送服務 |
| `.env` | 敏感資訊設定 |
| `skills/tts-voice-reply/SKILL.md` | 語音回覆 Skill |
| `skills/scrum-kanban/SKILL.md` | Scrum 看板管理 |
| `ruler.md` | 格式規範 |

---

## 📅 更新日誌

- 2026-02-21: 初始版本 - 整合 Email Service、TTS 語音服務與 Telegram 整合
