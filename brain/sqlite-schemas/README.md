# SQLite Schema Index - Todos & Bugs Management

## Database Location
```
/home/node/.openclaw/workspace/data/todos.db
```

---

## Tables Overview

| Table | File | Fields | Primary Key |
|-------|------|--------|--------------|
| sprints | `sprints_table.md` | 10 | id |
| todos | `todos_table.md` | 13 | id |
| bugs | `bugs_table.md` | 14 | id |

---

## Relationships

```
┌─────────────┐       ┌─────────────┐
│   sprints   │       │   sprints   │
└──────┬──────┘       └──────┬──────┘
       │ (1)                  │ (1)
       │<───────            │<───────
       │        │            │        │
       │ (N)    │            │ (N)    │
       ▼        ▼            ▼        ▼
┌─────────────┐       ┌─────────────┐
│    todos    │       │    bugs     │
└─────────────┘       └─────────────┘
```

---

## Constraint Values Summary

### sprints
| Field | Values |
|-------|--------|
| type | development, bugfix, research, release, maintenance |
| status | planning, active, completed, cancelled |

### todos
| Field | Values |
|-------|--------|
| type | feature, bug, research, task, improvement, documentation |
| status | todo, in-progress, review, done, cancelled |
| priority | critical, high, medium, low |

### bugs
| Field | Values |
|-------|--------|
| type | bug, issue, improvement, security, performance |
| status | open, in-progress, review, fixed, closed, wontfix, duplicate |
| priority | critical, high, medium, low |
| severity | critical, major, minor, trivial |

---

## Indexes Summary

| Table | Indexes |
|-------|---------|
| sprints | status, type |
| todos | type, status, priority, sprint_id |
| bugs | type, status, priority, severity, sprint_id |

---

## Migration Notes

### From JSON to SQLite
1. Backup existing JSON files
2. Create SQLite database
3. Run CREATE TABLE statements
4. Run CREATE INDEX statements
5. Import data with timestamp conversion
6. Verify data integrity
7. Switch application to use SQLite

### Date Handling
- All timestamps: Unix epoch (seconds)
- Query example: `SELECT date('unixepoch', created_at) FROM todos`
