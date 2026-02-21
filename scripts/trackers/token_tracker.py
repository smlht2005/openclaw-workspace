"""
LLM Token Usage Tracker
簡單的 Token 使用量追蹤函數
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

DATA_FILE = "/home/node/.openclaw/workspace/token_usage.json"

# 常見模型的定價 (USD per 1M tokens)
MODEL_PRICING = {
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "minimax-m2.5": {"input": 0.00, "output": 0.00},  # 免費或自訂價
    "minimax-m2.1": {"input": 0.00, "output": 0.00},
}


@dataclass
class TokenUsage:
    """Token 使用量記錄"""
    model: str
    input_tokens: int
    output_tokens: int
    timestamp: datetime
    is_test: bool = False  # 標記是否為測試資料
    
    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens
    
    def calculate_cost(self, pricing: Optional[dict] = None) -> float:
        """計算費用 (USD)"""
        if pricing is None:
            pricing = MODEL_PRICING.get(self.model, {"input": 0, "output": 0})
        
        input_cost = (self.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (self.output_tokens / 1_000_000) * pricing["output"]
        
        return round(input_cost + output_cost, 6)
    
    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "timestamp": self.timestamp.isoformat(),
            "is_test": self.is_test
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TokenUsage":
        return cls(
            model=data["model"],
            input_tokens=data["input_tokens"],
            output_tokens=data["output_tokens"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            is_test=data.get("is_test", False)
        )


class TokenTracker:
    """Token 使用量追蹤器"""
    
    def __init__(self):
        self.usage_history: list[TokenUsage] = []
        self._load()
    
    def _load(self):
        """從檔案載入歷史資料"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.usage_history = [
                        TokenUsage.from_dict(u) for u in data.get("history", [])
                    ]
                print(f"✅ 已載入 {len(self.usage_history)} 筆記錄")
            except Exception as e:
                print(f"⚠️ 載入失敗: {e}")
    
    def _save(self):
        """儲存到檔案"""
        data = {
            "history": [u.to_dict() for u in self.usage_history],
            "last_updated": datetime.now().isoformat()
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def record(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        is_test: bool = False,
        auto_save: bool = True
    ) -> TokenUsage:
        """記錄一次 API 調用"""
        usage = TokenUsage(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            timestamp=datetime.now(),
            is_test=is_test
        )
        self.usage_history.append(usage)
        
        if auto_save:
            self._save()
        
        return usage
    
    def get_total_usage(self) -> dict:
        """取得總使用量"""
        total_input = sum(u.input_tokens for u in self.usage_history)
        total_output = sum(u.output_tokens for u in self.usage_history)
        total_cost = sum(u.calculate_cost() for u in self.usage_history)
        
        return {
            "total_requests": len(self.usage_history),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_input + total_output,
            "total_cost_usd": round(total_cost, 6)
        }
    
    def get_usage_by_model(self) -> dict:
        """按模型分類統計"""
        stats = {}
        for usage in self.usage_history:
            if usage.model not in stats:
                stats[usage.model] = {
                    "requests": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0.0
                }
            
            stats[usage.model]["requests"] += 1
            stats[usage.model]["input_tokens"] += usage.input_tokens
            stats[usage.model]["output_tokens"] += usage.output_tokens
            stats[usage.model]["cost_usd"] += usage.calculate_cost()
        
        return stats
    
    def reset(self, confirm: bool = False):
        """重置記錄"""
        if not confirm:
            print("⚠️ 使用 reset(True) 確認清除所有資料")
            return
        
        self.usage_history.clear()
        self._save()
        print("✅ 已清除所有記錄")


# ============ 使用範例 ============

if __name__ == "__main__":
    tracker = TokenTracker()
    
    # 模擬記錄幾次 API 調用
    tracker.record("gpt-4o", input_tokens=1500, output_tokens=500)
    tracker.record("gpt-4o-mini", input_tokens=300, output_tokens=100)
    tracker.record("gpt-4o", input_tokens=2000, output_tokens=800)
    
    # 取得總使用量
    print("📊 總使用量:")
    print(tracker.get_total_usage())
    
    # 按模型分類
    print("\n📊 按模型分類:")
    for model, stats in tracker.get_usage_by_model().items():
        print(f"  {model}: {stats}")
