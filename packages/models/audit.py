"""
ProdSynth Models — Audit Events (Phase 3 Enterprise)
Tracks all significant actions for compliance and security.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class AuditEvent(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    action: str  # project.create, auth.login, billing.update, team.invite, ...
    resource_type: str  # project, auth, billing, team, sso, workspace
    resource_id: Optional[str] = None
    timestamp: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Dict[str, Any] = {}
    status: str = "success"  # success, failure, pending


# ─── Audit Event Types ───────────────────────────────────────
AUDIT_EVENT_TYPES = {
    "auth": [
        "auth.login",
        "auth.logout",
        "auth.register",
        "auth.sso_login",
        "auth.mfa_enable",
        "auth.mfa_disable",
        "auth.password_change",
    ],
    "project": [
        "project.create",
        "project.update",
        "project.delete",
        "project.share",
        "project.clone",
        "project.export",
    ],
    "billing": [
        "billing.subscribe",
        "billing.upgrade",
        "billing.downgrade",
        "billing.cancel",
        "billing.payment_failed",
        "billing.invoice_viewed",
    ],
    "team": [
        "team.invite",
        "team.join",
        "team.role_change",
        "team.remove",
        "team.sso_enforce",
    ],
    "sso": [
        "sso.config_change",
        "sso.provider_connected",
        "sso.provider_disconnected",
    ],
    "workspace": [
        "workspace.create",
        "workspace.update",
        "workspace.delete",
        "workspace.export",
    ],
    "product": [
        "product.run_start",
        "product.run_complete",
        "product.run_failed",
        "product.deploy",
        "product.webhook_triggered",
    ],
}


class AuditLogger:
    """Audit event logger. In production, writes to DB or external SIEM."""

    def __init__(self):
        self._buffer: List[AuditEvent] = []

    def log(
        self,
        workspace_id: str,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        status: str = "success",
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:
        event = AuditEvent(
            id=f"audit_{len(self._buffer) + 1}",
            workspace_id=workspace_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            timestamp=int(datetime.now().timestamp()),
            status=status,
            details=details or {},
        )
        self._buffer.append(event)
        return event

    def query(
        self,
        workspace_id: str,
        action: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[AuditEvent]:
        results = [e for e in self._buffer if e.workspace_id == workspace_id]
        if action:
            results = [e for e in results if e.action == action]
        if user_id:
            results = [e for e in results if e.user_id == user_id]
        return results[:limit]