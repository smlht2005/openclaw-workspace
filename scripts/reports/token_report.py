"""
Token Usage Reporter - Telegram 版本
直接從 token_usage.json 讀取並透過 Telegram 發送報告
"""

from token_tracker import TokenTracker

from datetime import datetime, timezone, timedelta

def get_report() -> str:
    """產生 Token 使用報告"""
    
    # 台北時區 UTC+8
    taipei_tz = timezone(timedelta(hours=8))
    
    tracker = TokenTracker()
    total = tracker.get_total_usage()
    by_model = tracker.get_usage_by_model()
    
    # 建立訊息
    lines = [
        "📊 *Token 使用量報告*",
        "=" * 30,
        "",
        "📈 *總覽*",
        f"• 總請求次數: `{total['total_requests']}`",
        f"• 總 Tokens: `{total['total_tokens']:,}`",
        f"  - Input: `{total['total_input_tokens']:,}`",
        f"  - Output: `{total['total_output_tokens']:,}`",
        f"• 總費用: `${total['total_cost_usd']:.4f}` USD",
        "",
        "🏭 *按模型分布*",
    ]
    
    # 按費用排序
    sorted_models = sorted(
        by_model.items(),
        key=lambda x: x[1]['cost_usd'],
        reverse=True
    )
    
    for model, stats in sorted_models:
        emoji = "🤖" if "gpt" in model else ("🧠" if "claude" in model else ("⚡" if "minimax" in model else "📦"))
        lines.append(f"{emoji} `{model}`")
        lines.append(f"   Requests: {stats['requests']}")
        lines.append(f"   Tokens: {stats['input_tokens']:,} in / {stats['output_tokens']:,} out")
        lines.append(f"   Cost: `${stats['cost_usd']:.4f}`")
        lines.append("")
    
    # 檢查是否為測試資料
    is_test_data = any(u.is_test for u in tracker.usage_history)
    
    if is_test_data:
        lines.insert(2, "⚠️ *⚠️ 測試資料，請忽略*")
    
    # 加入時間戳（台北時區）
    if tracker.usage_history:
        last = tracker.usage_history[-1]
        # 轉換為台北時區
        taipei_time = last.timestamp.astimezone(timezone(timedelta(hours=8)))
        lines.append(f"⏰ 最後更新: {taipei_time.strftime('%Y-%m-%d %H:%M:%S')} (台北)")
    
    return "\n".join(lines)


def send_report_via_telegram(target: str = None):
    """產生報告並發送到 Telegram"""
    from message import message
    
    report = get_report()
    
    # 發送到當前對話
    result = message(
        action="send",
        message=report,
        target=target  # 如果不指定則發送到當前對話
    )
    
    return result


if __name__ == "__main__":
    print(get_report())
