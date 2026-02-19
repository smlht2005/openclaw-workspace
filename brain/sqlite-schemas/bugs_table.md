# SQLite Schema: bugs

## Table Definition
```sql
CREATE TABLE bugs (
    id VARCHAR(20) PRIMARY KEY,
    type VARCHAR(20) NOT NULL 
        CHECK(type IN ('bug', 'issue', 'improvement', 'security', 'performance')),
    title VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'open' 
        CHECK(status IN ('open', 'in-progress', 'review', 'fixed', 'closed', 'wontfix', 'duplicate')),
    priority VARCHAR(10) DEFAULT 'medium' 
        CHECK(priority IN ('critical', 'high', 'medium', 'low')),
    severity VARCHAR(20) 
        CHECK(severity IN ('critical', 'major', 'minor', 'trivial')),
    sprint_id VARCHAR(20) REFERENCES sprints(id),
    tags TEXT,
    description TEXT,
    solution TEXT,
    created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    resolved_at INTEGER
);
```

## Indexes
```sql
CREATE INDEX idx_bugs_type ON bugs(type);
CREATE INDEX idx_bugs_status ON bugs(status);
CREATE INDEX idx_bugs_priority ON bugs(priority);
CREATE INDEX idx_bugs_severity ON bugs(severity);
CREATE INDEX idx_bugs_sprint ON bugs(sprint_id);
```

## Field Reference

| Field | Type | Constraints | Values |
|-------|------|-------------|--------|
| id | VARCHAR(20) | PRIMARY KEY | e.g., BUG-001 |
| type | VARCHAR(20) | NOT NULL | bug, issue, improvement, security, performance |
| title | VARCHAR(255) | NOT NULL | Bug title |
| status | VARCHAR(20) | DEFAULT 'open' | open, in-progress, review, fixed, closed, wontfix, duplicate |
| priority | VARCHAR(10) | DEFAULT 'medium' | critical, high, medium, low |
| severity | VARCHAR(20) | - | critical, major, minor, trivial |
| sprint_id | VARCHAR(20) | REFERENCES sprints(id) | Foreign key |
| tags | TEXT | - | JSON array |
| description | TEXT | - | Description |
| solution | TEXT | - | Solution |
| created_at | INTEGER | NOT NULL, DEFAULT | Unix timestamp |
| updated_at | INTEGER | NOT NULL, DEFAULT | Unix timestamp |
| resolved_at | INTEGER | - | Unix timestamp |

## Relationships
- Many bugs belong to one sprint (sprint_id)
- One bug has one status
- One bug has one priority
- One bug has one severity
- One bug has one type
