# SQLite Schema: todos

## Table Definition
```sql
CREATE TABLE todos (
    id VARCHAR(20) PRIMARY KEY,
    type VARCHAR(20) NOT NULL 
        CHECK(type IN ('feature', 'bug', 'research', 'task', 'improvement', 'documentation')),
    title VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'todo' 
        CHECK(status IN ('todo', 'in-progress', 'review', 'done', 'cancelled')),
    priority VARCHAR(10) DEFAULT 'medium' 
        CHECK(priority IN ('critical', 'high', 'medium', 'low')),
    points INTEGER DEFAULT 0 CHECK(points >= 0),
    sprint_id VARCHAR(20) REFERENCES sprints(id),
    tags TEXT,
    description TEXT,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    completed_at INTEGER
);
```

## Indexes
```sql
CREATE INDEX idx_todos_type ON todos(type);
CREATE INDEX idx_todos_status ON todos(status);
CREATE INDEX idx_todos_priority ON todos(priority);
CREATE INDEX idx_todos_sprint ON todos(sprint_id);
```

## Field Reference

| Field | Type | Constraints | Values |
|-------|------|-------------|--------|
| id | VARCHAR(20) | PRIMARY KEY | e.g., T001 |
| type | VARCHAR(20) | NOT NULL | feature, bug, research, task, improvement, documentation |
| title | VARCHAR(255) | NOT NULL | Task title |
| status | VARCHAR(20) | DEFAULT 'todo' | todo, in-progress, review, done, cancelled |
| priority | VARCHAR(10) | DEFAULT 'medium' | critical, high, medium, low |
| points | INTEGER | DEFAULT 0, >= 0 | Story points |
| sprint_id | VARCHAR(20) | REFERENCES sprints(id) | Foreign key |
| tags | TEXT | - | JSON array |
| description | TEXT | - | Description |
| created_at | INTEGER | NOT NULL, DEFAULT | Unix timestamp |
| updated_at | INTEGER | NOT NULL, DEFAULT | Unix timestamp |
| completed_at | INTEGER | - | Unix timestamp |

## Relationships
- Many todos belong to one sprint (sprint_id)
- One todo has one status
- One todo has one priority
- One todo has one type
