"""
ProdSynth Middleware — Tenant Isolation (Phase 3 Enterprise)
Ensures all requests are scoped to a workspace_id.
Uses X-Workspace-ID header or JWT claim.
"""

import logging
from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("prodsynth.middleware.tenant")


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces workspace isolation.
    Extracts workspace_id from JWT or X-Workspace-ID header,
    attaches it to request.state.workspace_id.
    """

    # Endpoints exempt from workspace scoping
    EXEMPT_PATHS = {
        "/",
        "/health",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/sso",
        "/api/v1/billing/plans",
        "/api/v1/marketplace/templates",
        "/docs",
        "/openapi.json",
        "/redoc",
    }

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow exempt paths
        if path in self.EXEMPT_PATHS or path.startswith("/docs") or path.startswith("/openapi"):
            return await call_next(request)

        # Extract workspace_id
        workspace_id: Optional[str] = None

        # 1. From X-Workspace-ID header
        header_ws = request.headers.get("X-Workspace-ID")
        if header_ws:
            workspace_id = header_ws
            logger.debug(f"  Tenant: workspace_id from header = {workspace_id}")

        # 2. From JWT (request.state set by auth middleware)
        if not workspace_id and hasattr(request.state, "workspace_id"):
            workspace_id = request.state.workspace_id
            logger.debug(f"  Tenant: workspace_id from JWT = {workspace_id}")

        if not workspace_id:
            logger.warning(f"  Tenant: No workspace_id for {path}")
            raise HTTPException(
                status_code=401,
                detail="workspace_id required (X-Workspace-ID header or JWT claim)",
            )

        # Attach to request state for downstream handlers
        request.state.workspace_id = workspace_id

        logger.debug(f"  Tenant: request scoped to workspace={workspace_id}")
        response = await call_next(request)
        return response


def get_workspace_id(request: Request) -> str:
    """Get workspace_id from request state."""
    ws = getattr(request.state, "workspace_id", None)
    if not ws:
        raise HTTPException(status_code=401, detail="workspace_id not set")
    return ws