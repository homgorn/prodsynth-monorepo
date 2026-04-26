"""
ProdSynth Models — Tenant / Multi-tenancy (Phase 3 Enterprise)
Tenant isolation strategy: PostgreSQL row-level security (RLS)
with workspace_id foreign key on all tables.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class TenantConfig(BaseModel):
    workspace_id: str
    plan: str = "free"
    row_level_security: bool = True
    separate_schema: bool = False  # true only for Enterprise
    rate_limit_per_minute: int = 60
    max_concurrent_builds: int = 2


class TenantLimits(BaseModel):
    workspace_id: str
    max_projects: int = 3
    max_team_members: int = 1
    max_graph_storage_gb: int = 1
    max_token_budget: float = 1.00
    features: List[str] = []


TENANT_LIMITS = {
    "free": TenantLimits(
        workspace_id="*",
        max_projects=3,
        max_team_members=1,
        max_graph_storage_gb=1,
        max_token_budget=1.00,
        features=["core", "graphiti", "marketplace"],
    ),
    "pro": TenantLimits(
        workspace_id="*",
        max_projects=-1,
        max_team_members=10,
        max_graph_storage_gb=100,
        max_token_budget=0.50,
        features=["core", "graphiti", "marketplace", "api", "webhooks"],
    ),
    "enterprise": TenantLimits(
        workspace_id="*",
        max_projects=-1,
        max_team_members=-1,
        max_graph_storage_gb=-1,
        max_token_budget=1.00,
        features=["core", "graphiti", "marketplace", "api", "webhooks", "sso", "audit", "sla"],
    ),
}


def get_tenant_limits(plan: str) -> TenantLimits:
    return TENANT_LIMITS.get(plan, TENANT_LIMITS["free"])