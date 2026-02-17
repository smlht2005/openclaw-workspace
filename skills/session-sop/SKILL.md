---
name: session-sop
description: Session 結束 SOP - 記錄、總結、提交並建立技能
---

# Session 結束 SOP

每次重要 session 結束時，執行以下步驟：

## 1. 記錄 Session

建立 `memory/YYYY-MM-DD.md` 檔案，記錄：
- 完成的事項
- 新增的檔案/功能
- 待處理問題
- Git commit 相關資訊

## 2. 更新相關檔案

### Todo 狀態
- 更新 `todos/todos.json` 的 `last_updated`
- 新增任務狀態變更

### Bug 狀態
- 修復的 bug 標記為 `fixed`
- 填入 `resolved_at` 日期

## 3. Git 提交

```bash
cd /home/node/.openclaw/workspace
git add -A
git commit -m "feat/fix: <標題>

- 完成事項 1
- 完成事項 2"
git push
```

Commit 訊息格式：
- `feat:` 新功能
- `fix:` Bug 修復
- `refactor:` 重構
- `docs:` 文件

## 4. 建立技能 (如有需要)

如果完成的事項值得建立技能：
1. 在 `skills/` 建立新資料夾
2. 撰寫 `SKILL.md`
3. 記錄到 `TOOLS.md` (如有必要)

## 5. 總結給用戶

用戶離開前，提供：
- 本次完成事項
- 待處理項目
- 下次可以繼續的方向

---

## 常用指令速查

```bash
# 記錄 memory
vim memory/2026-02-17.md

# 更新 todos
vim todos/todos.json

# 更新 bugs
vim bugs/issues.json

# Git
git add -A && git commit -m "..." && git push
```
