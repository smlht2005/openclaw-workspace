# Token Tracker 專案

## 📋 Product Backlog

| ID | 任務 | 優先級 | 狀態 | 估點 | 備註 |
|----|------|--------|------|------|------|
| T001 | JSON 持久化 | P2 | 🔍 Review | 2 | - |
| T002 | Telegram 報告發送 | P2 | 🔄 In Progress | 3 | Cron 4次/天 |
| T003 | 每日 Session 追蹤 | P2 | 🔍 Review | - | Cron 4次/天 |
| T004 | 網頁儀表板 | P3 | 📋 Todo | - | - |
| T005 | 更多模型支援 | P3 | 📋 Todo | - | - |
| T006 | Scrum Kanban Skill | P2 | 🔍 Review | 2 | skill + template |
| T007 | Bug Tracker | P3 | ✅ Done | 1 | bugs/issues.json |
| T008 | Bug Tracker Skill | P3 | ✅ Done | 1 | skill + template |

---

## 📝 Sprint 1 - 2026-02-15

### ✅ Done
- [x] T001: JSON 持久化 (2 pts)
- [x] T002: Telegram 報告發送 (3 pts)
- [x] T003: 每日 Session 追蹤

### 🔍 Review
- [ ] T002: Telegram 報告發送（→ 移動到 review/）

### 📋 To Do
- [ ] T004: 網頁儀表板
- [ ] T005: 更多模型支援

---

## ⚠️ 技術負債 / 注意事項
- Input tokens 過高 (336k)，context 100% → 建議使用 /new 開新 session

---

## 📊 點數統計
| Sprint | 預估 | 實際 | 完成率 |
|--------|------|------|--------|
| Sprint 1 | 5+ | 5+ | 100% |
