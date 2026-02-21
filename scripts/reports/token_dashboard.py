"""
Token Usage Dashboard - Canvas UI
"""

from token_tracker import TokenTracker

# 獲取數據
tracker = TokenTracker()
total = tracker.get_total_usage()
by_model = tracker.get_usage_by_model()

# 計算百分比
total_tokens = total['total_tokens'] or 1

# 生成 HTML
html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      min-height: 100vh;
      padding: 24px;
      color: #fff;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
    }}
    h1 {{
      text-align: center;
      margin-bottom: 24px;
      font-size: 28px;
    }}
    .card {{
      background: rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      backdrop-filter: blur(10px);
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }}
    .stat-item {{
      background: rgba(0,0,0,0.2);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
    }}
    .stat-value {{
      font-size: 32px;
      font-weight: bold;
      color: #4ade80;
    }}
    .stat-label {{
      font-size: 14px;
      color: #94a3b8;
      margin-top: 4px;
    }}
    .progress-bar {{
      height: 24px;
      background: rgba(0,0,0,0.3);
      border-radius: 12px;
      overflow: hidden;
      margin: 16px 0;
    }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, #4ade80, #22d3ee);
      border-radius: 12px;
      transition: width 0.5s ease;
    }}
    .model-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .model-item {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      background: rgba(0,0,0,0.2);
      border-radius: 8px;
    }}
    .model-name {{
      flex: 1;
      font-weight: 600;
    }}
    .model-stats {{
      text-align: right;
      font-size: 13px;
      color: #94a3b8;
    }}
    .model-cost {{
      color: #fbbf24;
      font-weight: bold;
    }}
    .emoji {{ font-size: 24px; }}
    .footer {{
      text-align: center;
      margin-top: 20px;
      color: #64748b;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>📊 Token 使用量儀表板</h1>
    
    <!-- 總覽卡片 -->
    <div class="card">
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{total['total_requests']}</div>
          <div class="stat-label">總請求次數</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{total['total_tokens']:,}</div>
          <div class="stat-label">總 Tokens</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{total['total_input_tokens']:,}</div>
          <div class="stat-label">Input Tokens</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">${total['total_cost_usd']:.4f}</div>
          <div class="stat-label">總費用 (USD)</div>
        </div>
      </div>
    </div>
    
    <!-- 按模型分布 -->
    <div class="card">
      <h2 style="margin-bottom: 16px;">🏭 按模型分布</h2>
      <div class="model-list">
"""

# 添加每個模型的數據
for model, stats in by_model.items():
    pct = (stats['input_tokens'] + stats['output_tokens']) / total_tokens * 100
    emoji = "🤖" if "gpt" in model else ("🧠" if "claude" in model else ("⚡" if "minimax" in model else "📦"))
    html += f"""
        <div class="model-item">
          <span class="emoji">{emoji}</span>
          <div class="model-name">{model}</div>
          <div class="model-stats">
            {stats['input_tokens']:,} in / {stats['output_tokens']:,} out<br>
            <span class="model-cost">${stats['cost_usd']:.4f}</span>
          </div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: {pct}%"></div>
        </div>
"""

html += """
      </div>
    </div>
    
    <div class="footer">
      更新時間: """ + tracker.usage_history[-1].timestamp.strftime('%Y-%m-%d %H:%M:%S') if tracker.usage_history else "N/A" + """
    </div>
  </div>
</body>
</html>
"""

print(html)
