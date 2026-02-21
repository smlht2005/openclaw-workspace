# OpenClaw 語音訊息設定手冊

## 📋 目錄
1. [TTS 語音服務設定](#1-tts-語音服務設定)
2. [如何發送語音訊息](#2-如何發送語音訊息)
3. [常見問題與解決方案](#3-常見問題與解決方案)

---

## 1. TTS 語音服務設定

### 1.1 設定檔位置
- 檔案：`/home/node/.openclaw/openclaw.json`
- 區塊：`messages.tts`

### 1.2 完整設定範例
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

### 1.3 設定說明

| 參數 | 可選值 | 說明 |
|------|--------|------|
| `auto` | `always` / `off` / `on` / `never` | 自動發送語音時機 |
| `provider` | `edge` / `openai` / `elevenlabs` | TTS 服務供應商 |
| `voice` | 見下方列表 | 語音選擇 |

### 1.4 可用的中文聲音

| 聲音代碼 | 說明 |
|----------|------|
| `zh-TW-HsiaoChenNeural` | 曉晨 (推薦) |
| `zh-TW-HsiaoYuNeural` | 曉雨 |
| `zh-CN-XiaoxiaoNeural` | 曉曉 (普通話) |

---

## 2. 如何發送語音訊息

### 2.1 使用指令控制

| 指令 | 說明 |
|------|------|
| `/tts on` | 開啟這次對話的語音回覆 |
| `/tts always` | 持續開啟語音回覆 |
| `/tts off` | 關閉語音回覆 |

### 2.2 使用對話要求

直接對機器人說：
- 「請用聲音回覆」
- 「用語音回答我」

### 2.3 手動發送語音

使用 `tts` 工具：
```python
tts(
    channel="telegram",
    text="要轉換的文字",
    voice="zh-TW-HsiaoChenNeural"  # 可選
)
```

然後使用 `message` 工具發送：
```python
message(
    action="send",
    filePath="/tmp/tts_output.mp3",
    asVoice="true"  # 關鍵參數！
)
```

---

## 3. 常見問題與解決方案

### 問題 1: 語音重疊播放

**現象：** 連續發送多個語音訊息時，音樂會重疊播放

**原因：** 發送時缺少 `asVoice="true"` 參數

**解決方案：**
```python
message(
    action="send",
    filePath="xxx.mp3",
    asVoice="true"  # 務必加入
)
```

---

### 問題 2: /tts 指令沒有聲音

**原因：** 缺少 FFmpeg

**解決方案：**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Mac
brew install ffmpeg
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

### 問題 4: 環境變數設定無效 (常見錯誤！)

**現象：** TTS 仍然使用英文，設定好像沒生效

**錯誤的設定方式：**
```json
// ❌ 錯誤！這樣設定不會生效
{
  "env": {
    "vars": {
      "TTS_VOICE": "zh-TW-YunJheNeural",
      "TTS_PROVIDER": "edge-tts",
      "TTS_ENABLED": "true"
    }
  }
}
```

**原因：** `env.vars` 是給外部程式用的環境變數，不是用來設定 OpenClaw 內建的 TTS 服務。

**正確的設定方式：**
```json
// ✅ 正確！
{
  "messages": {
    "tts": {
      "auto": "off",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-TW-YunJheNeural",
        "lang": "zh-TW"
      }
    }
  }
}
```

**⚠️ 注意：** 設定完成後需要重啟 Gateway 才會生效。

---

## 📂 相關檔案

| 檔案 | 說明 |
|------|------|
| `skills/tts-voice-reply/SKILL.md` | 語音回覆 Skill |
| `.env` | Gmail SMTP 設定 |
| `email_service.py` | 郵件發送服務 |
| `docs/voice_help.md` | 語音訊息指南 |

---

## 📅 更新日誌

- 2026-02-21: 初始版本
- 支援按需發送語音 (auto=off)
- 預設語音改為中文 (zh-TW-HsiaoChenNeural)
- 新增：環境變數設定無效的常見錯誤 (env.vars 不是正確方式)
