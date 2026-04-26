"""
ProdSynth Models — Workspace (Phase 3 Multi-tenancy)
Workspace = isolated tenant boundary with separate DB schema.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class Workspace(BaseModel):
    id: str
    name: str
    slug: str
    plan: str = "free"
    settings: Dict[str, Any] = {}
    features: List[str] = []
    created_at: int
    updated_at: int
    storage_used_bytes: int = 0
    storage_limit_bytes: int = 1_073_741_824  # 1GB default


class WorkspaceSettings(BaseModel):
    allow_signups: bool = True
    enforce_sso: bool = False
    sso_provider: Optional[str] = None
    require_mfa: bool = False
    allowed_email_domains: List[str] = []
    default_role: str = "editor"
    max_team_members: int = 5
    audit_retention_days: int = 90
    webhook_url: Optional[str] = None
    webhook_events: List[str] = ["product.ready"]