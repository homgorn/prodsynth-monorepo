# ProdSynth Multi-tenancy Architecture (BMAD v2.0 — Phase 4)

## Overview

ProdSynth uses **workspace** as the primary isolation boundary. Every tenant gets:
- A `workspace_id` (UUID)
- Isolated data in PostgreSQL (row-level security)
- Isolated graphs in Neo4j (workspace-tagged nodes)
- Isolated cache in Redis (key prefixed with `ws:{id}:`)
- Isolated audit log (filtered by workspace_id)

---

## Data Isolation Strategy

### PostgreSQL: Row-Level Security (RLS)

All multi-tenant tables include `workspace_id`. RLS policies enforce isolation:

```sql
-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Policy: users can only see their workspace's projects
CREATE POLICY workspace_isolation ON projects
  USING (workspace_id = current_setting('app.current_workspace_id')::UUID);

-- Set workspace context per connection
SET app.current_workspace_id = 'ws_abc123';
SELECT * FROM projects;  -- Only returns ws_abc123's projects
```

### Neo4j: Workspace-Tagged Nodes

```cypher
// Every node has workspace_id property
CREATE (p:Project {
  id: "proj_123",
  workspace_id: "ws_abc123",  // required
  name: "My SaaS App",
  created_at: 1714041600
})

// Query only within workspace
MATCH (p:Project {workspace_id: $workspace_id})
RETURN p
```

### Redis: Key Prefixing

```
ws:{workspace_id}:projects          → Hash of project list
ws:{workspace_id}:token_budget     → Remaining budget
ws:{workspace_id}:rate_limit      → Request counter
ws:{workspace_id}:session:{id}    → User session
```

---

## Middleware Enforcement

```python
# apps/backend/middleware/tenant.py
class TenantMiddleware:
    EXEMPT_PATHS = {"/", "/health", "/docs", "/auth/login", "/billing/plans"}

    async def dispatch(self, request, call_next):
        # 1. Check exempt paths
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        # 2. Extract workspace_id
        workspace_id = (
            request.headers.get("X-Workspace-ID")
            or request.state.workspace_id  # from JWT
        )

        if not workspace_id:
            raise HTTPException(401, "workspace_id required")

        # 3. Validate exists and user has access
        workspace = await db.workspaces.find_one({"id": workspace_id})
        if not workspace:
            raise HTTPException(404, "workspace not found")

        # 4. Attach to request state for downstream use
        request.state.workspace_id = workspace_id

        return await call_next(request)
```

---

## Plan-Based Limits

| Limit | Free | Pro | Enterprise |
|--------|------|-----|-----------|
| Projects | 3 | ∞ | ∞ |
| Team members | 1 | 10 | ∞ |
| Graph storage | 1 GB | 100 GB | ∞ |
| Token budget/run | $0.50 | $0.50 | $1.00 |
| API rate limit | 60/min | 300/min | 1000/min |
| Concurrent builds | 1 | 2 | 10 |
| SSO providers | — | — | 4 |
| SLA | — | — | 99.9% |
| Support | Community | Email | Dedicated |
| Schema isolation | Shared | Shared | Dedicated |

### Limit Enforcement

```python
# Enforced at API layer
async def enforce_limits(workspace_id: str, action: str) -> bool:
    workspace = await db.workspaces.find_one({"id": workspace_id})
    limits = TENANT_LIMITS[workspace.plan]

    if action == "project.create":
        if limits.max_projects != -1:
            count = await db.projects.count({"workspace_id": workspace_id})
            if count >= limits.max_projects:
                raise HTTPException(402, "Project limit reached. Upgrade to Pro.")

    elif action == "synthesis.run":
        concurrent = await db.runs.count({
            "workspace_id": workspace_id,
            "status": "running"
        })
        if concurrent >= limits.max_concurrent_builds:
            raise HTTPException(429, "Concurrent build limit reached.")

    return True
```

---

## Schema-Per-Tenant (Enterprise Only)

For Enterprise, we can provision a dedicated PostgreSQL schema:

```python
async def get_enterprise_schema(workspace_id: str) -> str:
    workspace = await db.workspaces.find_one({"id": workspace_id})
    if workspace.plan != "enterprise":
        return "public"  # shared schema

    # Create schema if not exists
    schema_name = f"tenant_{workspace_id.replace('-', '_')}"
    await db.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    await db.execute(f"SET search_path TO {schema_name}, public")
    return schema_name
```

---

## Cross-Workspace Sharing

Projects can be shared between workspaces:

```python
# sharing.py
class ShareRequest(BaseModel):
    project_id: str
    target_workspace_id: str
    permission: str  # "view" | "edit" | "admin"

# Creates a reference in the target workspace
share = {
    "project_id": "proj_123",
    "source_workspace_id": "ws_abc",
    "target_workspace_id": "ws_xyz",
    "permission": "edit",
    "shared_at": now(),
}
```

---

## Data Residency & GDPR

### Region Selection
- Free/Pro: EU (Frankfurt) or US (Virginia) — user choice
- Enterprise: Any region (AWS/GCP/Azure)

### Data Export
```python
# Export all workspace data as JSON
GET /api/v1/workspaces/{id}/export
→ Returns: projects, graphs, audit_log, team_members
```

### Data Deletion
```python
# Soft delete → anonymize after 30 days
DELETE /api/v1/workspaces/{id}
→ Sets deleted_at timestamp
→ Removes PII (email, name → "deleted_user")
→ Retains aggregates for billing
```

---

## Connection Pooling

Each workspace gets a logical connection pool:

```python
# pgBouncer configuration (per-tenant pools)
[databases]
; Each tenant gets 5 connections max
prod_synth_db = host=pg port=5432 dbname=prodsynth

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
```

---

## Backup Strategy

| Scope | Frequency | Retention | Storage |
|--------|-----------|-----------|---------|
| Full DB | Daily | 30 days | S3 |
| Incremental | Every 6h | 7 days | S3 |
| Neo4j graphs | Every 6h | 30 days | S3 |
| Audit log | Real-time | 90 days | Loki |
| Files/artifacts | Per deploy | 7 days | R2 |