"""
每日 Session 使用量追蹤系統
每 6 小時自動記錄一次（4次/天）
"""

import json
import os
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 台北時區
TAIPEI_TZ = timezone(timedelta(hours=8))

# 可配置的路徑（支援環境變數）
MAX_CONTEXT = 200000
DATA_DIR = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace"))
DAILY_FILE = DATA_DIR / "daily_usage.json"
CURRENT_FILE = DATA_DIR / "current_session_usage.json"
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "/home/node/bin/openclaw")


def get_session_usage() -> dict:
    """從 openclaw sessions 獲取當前 session 使用量"""
    try:
        result = subprocess.run(
            [OPENCLAW_BIN, "sessions", "--json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return {"error": f"CLI error: {result.stderr}"}
        
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON response: {e}"}
        
        sessions = data.get("sessions", [])
        
        session_details = []
        total_tokens = 0
        total_input = 0
        total_output = 0
        
        for s in sessions:
            input_t = s.get("inputTokens", 0) or 0
            output_t = s.get("outputTokens", 0) or 0
            total = s.get("totalTokens", 0) or 0
            context_t = s.get("contextTokens", 0) or 0
            
            # 計算 Context 使用率（相對於最大 Context 200K）
            context_pct = round((context_t / MAX_CONTEXT * 100), 2) if context_t > 0 else 0
            
            session_details.append({
                "session_key": s.get("key"),
                "model": s.get("model"),
                "input_tokens": input_t,
                "output_tokens": output_t,
                "total_tokens": total,
                "context_tokens": context_t,
                "context_pct": context_pct
            })
            
            total_tokens += total
            total_input += input_t
            total_output += output_t
        
        return {
            "timestamp": datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "sessions": session_details,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_tokens,
            "active_sessions": len(sessions)
        }
        
    except Exception as e:
        return {"error": str(e)}


def load_daily_data() -> dict:
    """載入每日資料"""
    if DAILY_FILE.exists():
        with open(DAILY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_daily_data(data: dict):
    """儲存每日資料"""
    with open(DAILY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_usage():
    """記錄當前使用量"""
    usage = get_session_usage()
    
    if "error" in usage:
        print(f"⚠️ {usage['error']}")
        return usage
    
    today = datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d")
    
    # 載入現有資料
    data = load_daily_data()
    
    if today not in data:
        data[today] = {"records": [], "total_tokens": 0, "total_input": 0, "total_output": 0}
    
    # 新增記錄
    data[today]["records"].append(usage)
    data[today]["total_tokens"] = usage.get("total_tokens", 0)
    data[today]["total_input"] = usage.get("total_input_tokens", 0)
    data[today]["total_output"] = usage.get("total_output_tokens", 0)
    
    # 只保留最近 30 天
    dates = sorted(data.keys())
    if len(dates) > 30:
        for old_date in dates[:-30]:
            del data[old_date]
    
    save_daily_data(data)
    
    # 同時更新 current session
    with open(CURRENT_FILE, "w", encoding="utf-8") as f:
        json.dump(usage, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已記錄 {today} {usage['timestamp']}")
    print(f"   Session 數: {usage['active_sessions']}")
    print(f"   Total Tokens: {usage['total_tokens']:,}")
    
    return usage


def get_trend(days: int = 7) -> dict:
    """取得趨勢資料"""
    data = load_daily_data()
    
    dates = sorted(data.keys())[-days:]
    
    trend = []
    for date in dates:
        day_data = data[date]
        
        trend.append({
            "date": date,
            "total_tokens": day_data.get("total_tokens", 0),
            "total_input": day_data.get("total_input", 0),
            "total_output": day_data.get("total_output", 0),
            "records_count": len(day_data.get("records", []))
        })
    
    return {"trend": trend, "days": days}


def format_report() -> str:
    """產生報告訊息"""
    usage = record_usage()
    
    if not usage:
        return "⚠️ 無法獲取 session 資料"
    
    if "error" in usage:
        return f"⚠️ {usage['error']}"
    
    trend = get_trend(7)
    
    # 取得所有 sessions
    sessions = usage.get("sessions", [])
    model = sessions[0].get("model", "N/A") if sessions else "N/A"
    
    # 計算最高 Context
    max_context = max((s.get("context_pct", 0) for s in sessions), default=0)
    max_context_session = max(sessions, key=lambda s: s.get("context_pct", 0))
    
    lines = [
        "📊 Token 使用報告",
        f"⏰ {usage['timestamp']} (台北)",
        f"🤖 模型: {model}",
        f"📱 Sessions: {usage['active_sessions']}",
        f"🧮 Input: {usage.get('total_input_tokens', 0):,}",
        f"🧮 Output: {usage.get('total_output_tokens', 0):,}",
        f"🧮 Total: {usage['total_tokens']:,}",
        f"📊 Context: {max_context:.1f}%",
        "",
        "📈 趨勢（最近 7 天）"
    ]
    
    for t in trend["trend"]:
        tokens = t["total_tokens"]
        bar = "█" * min(int(tokens / 10000), 15)
        lines.append(f"{t['date'][-5:]} {bar} {tokens:,}")
    
    # Session 詳細列表
    lines.append("")
    lines.append("📱 Session 詳情")
    for s in sessions:
        key = s.get("session_key", "N/A")
        # 簡化 session key 顯示
        if "cron:" in key:
            display_key = "Cron"
        elif "telegram:" in key:
            display_key = "Telegram"
        else:
            display_key = "Main"
        ctx = s.get("context_pct", 0)
        total = s.get("total_tokens", 0)
        lines.append(f"  • {display_key}: {total:,} tokens, Context {ctx:.1f}%")
    
    # 如果有 Context > 80% 的 session，給出警告
    high_context_sessions = [s for s in sessions if s.get("context_pct", 0) > 80]
    if high_context_sessions:
        lines.append("")
        lines.append("⚠️ 注意：以下 Session Context 過高")
        for s in high_context_sessions:
            lines.append(f"  - {s.get('session_key', 'N/A')}: {s.get('context_pct', 0)}%")
        lines.append("💡 建議使用 /new 開新 session")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_report())
