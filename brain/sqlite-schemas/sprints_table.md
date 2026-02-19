# SQLite Schema: sprints

## Table Definition
```sql
CREATE TABLE sprints (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) DEFAULT 'development' 
        CHECK(type IN ('development', 'bugfix', 'research', 'release', 'maintenance')),
    goal TEXT,
    status VARCHAR(20) DEFAULT 'planning' 
        CHECK(status IN ('planning', 'active', 'completed', 'cancelled')),
    start_date INTEGER,
    end_date INTEGER,
    velocity INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);
```

## Indexes
```sql
CREATE INDEX idx_sprints_status ON sprints(status);
CREATE INDEX idx_sprints_type ON sprints(type);
```

## Field Reference

| Field | Type | Constraints | Values |
|-------|------|-------------|--------|
| id | VARCHAR(20) | PRIMARY KEY | e.g., Sprint 1 |
| name | VARCHAR(50) | NOT NULL | Sprint name |
| type | VARCHAR(20) | DEFAULT 'development' | development, bugfix, research, release, maintenance |
| goal | TEXT | - | Sprint goal |
| status | VARCHAR(20) | DEFAULT 'planning' | planning, active, completed, cancelled |
| start_date | INTEGER | - | Unix timestamp |
| end_date | INTEGER | - | Unix timestamp |
| velocity | INTEGER | DEFAULT 0 | Completed story points |
| created_at | INTEGER | NOT NULL, DEFAULT | Unix timestamp |
| updated_at | INTEGER | NOT NULL, DEFAULT | Unix timestamp |

## Relationships
- One sprint has many todos
- One sprint has many bugs
