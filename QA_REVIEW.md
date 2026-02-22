# QA Review Notes

## PR Review: [A-TAO] feat: 新增 Email Service、TTS 語音服務與腳本重整

### 🔐 Security Issues Fixed

1. **`scripts/email_service.py`** — Hardcoded email address as default fallback (`"smlhtliu@gmail.com"`).
   - Violates ruler.md: "嚴禁 hardcode - 所有密碼、API Token、私鑰不可寫死在程式碼中"
   - **Fix**: Changed default to `""` — caller must set `GMAIL_USER` env var.

### 🛠️ Code Quality Issues Fixed

2. **`scripts/reports/scrum_report.py`** — Hardcoded workspace path `/home/node/.openclaw/workspace`.
   - Inconsistent with `daily_tracker.py` which already uses `os.environ.get("OPENCLAW_WORKSPACE", ...)`.
   - **Fix**: Use `OPENCLAW_WORKSPACE` env var with same fallback pattern.

3. **`scripts/reports/kanban_report.py`** — Same hardcoded path issue.
   - **Fix**: Use `OPENCLAW_WORKSPACE` env var.

4. **`scripts/trackers/token_tracker.py`** — Same hardcoded path issue.
   - **Fix**: Use `OPENCLAW_WORKSPACE` env var.

### ✅ Items Verified OK

- `daily_tracker.py`: Already correctly uses `OPENCLAW_WORKSPACE` and `OPENCLAW_BIN` env vars.
- `email_service.py`: Correctly reads `.env` file and uses `GMAIL_APP_PASSWORD` without hardcoding.
- Error handling in place for JSON parse errors, subprocess failures.
- 30-day data retention in `daily_tracker.py` is appropriate.

### 📋 Review Result: ✅ Approved (after fixes)

