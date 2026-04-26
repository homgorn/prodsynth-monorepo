"""
ProdSynth Debug Utilities — Phase 5
Error handlers, logging helpers, debug endpoints.
"""

import logging
import traceback
import sys
import time
import json
from typing import Dict, Any, Optional
from functools import wraps
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger("prodsynth.debug")


# ─── Error Classes ─────────────────────────────────────────
class SynthesisError(Exception):
    def __init__(self, message: str, agent: Optional[str] = None, cost: float = 0.0):
        self.message = message
        self.agent = agent
        self.cost = cost
        super().__init__(self.message)


class TokenBudgetExceeded(SynthesisError):
    def __init__(self, budget: float, used: float):
        self.budget = budget
        self.used = used
        super().__init__(
            f"Token budget exceeded: ${used:.2f} used of ${budget:.2f} limit",
            agent="TokenBudget",
            cost=used,
        )


class LicenseError(SynthesisError):
    def __init__(self, license_name: str, action: str):
        self.license_name = license_name
        self.action = action
        super().__init__(
            f"License '{license_name}' blocked: {action}",
            agent="LicenseChecker",
        )


class WorkspaceNotFoundError(SynthesisError):
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        super().__init__(
            f"Workspace '{workspace_id}' not found or access denied",
            agent="TenantMiddleware",
        )


# ─── Error Response Model ──────────────────────────────────
class ErrorResponse(BaseModel):
    error: str
    code: str
    message: str
    agent: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: int
    trace_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# ─── Request ID Middleware ─────────────────────────────────
def generate_request_id() -> str:
    import uuid
    return str(uuid.uuid4())[:8]


class RequestContext:
    def __init__(self):
        self.request_id = generate_request_id()
        self.start_time = time.time()
        self.agent_times: Dict[str, float] = {}

    def mark_agent(self, name: str):
        self.agent_times[name] = time.time()
        logger.info(f"  [{name}] at {self.agent_times[name] - self.start_time:.2f}s")

    def duration(self) -> float:
        return time.time() - self.start_time


# ─── Error Handlers ───────────────────────────────────────
def handle_synthesis_error(e: SynthesisError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error": e.__class__.__name__,
            "code": e.agent or "UNKNOWN",
            "message": e.message,
            "agent": e.agent,
            "cost": e.cost,
            "timestamp": int(time.time()),
        },
    )


def handle_validation_error(e: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "code": "VALIDATION",
            "message": str(e),
            "timestamp": int(time.time()),
        },
    )


def handle_generic_error(e: Exception) -> JSONResponse:
    exc_type = type(e).__name__
    exc_trace = traceback.format_exception(*sys.exc_info())
    logger.error(f"Unhandled error: {exc_type}: {e}\n{''.join(exc_trace)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "code": "INTERNAL",
            "message": "An unexpected error occurred. Please try again.",
            "timestamp": int(time.time()),
        },
    )


# ─── Debug Endpoints ────────────────────────────────────────
def register_debug_routes(app):
    from fastapi import APIRouter

    router = APIRouter(prefix="/debug", tags=["Debug"])

    @router.get("/ping")
    async def ping():
        return {"pong": True, "timestamp": int(time.time())}

    @router.get("/status")
    async def status(request: Request):
        return {
            "status": "healthy",
            "version": "0.1.0",
            "python_version": sys.version.split()[0],
            "timestamp": int(time.time()),
        }

    @router.get("/memory")
    async def memory_stats():
        import psutil
        process = psutil.Process()
        mem = process.memory_info()
        return {
            "rss_mb": mem.rss / 1024 / 1024,
            "vms_mb": mem.vms / 1024 / 1024,
            "timestamp": int(time.time()),
        }

    @router.get("/config")
    async def debug_config(request: Request):
        ws_id = getattr(request.state, "workspace_id", None)
        return {
            "workspace_id": ws_id,
            "env_vars": {
                "STRIPE_API_KEY": "SET" if __import__("os")..getenv("STRIPE_API_KEY") else "NOT_SET",
                "NEO4J_URI": "SET" if __import__("os").getenv("NEO4J_URI") else "NOT_SET",
                "REDIS_URL": "SET" if __import__("os").getenv("REDIS_URL") else "NOT_SET",
            },
        }

    @router.post("/synthesis/dry-run")
    async def synthesis_dry_run(request: Request, data: Dict[str, Any]):
        logger.info(f"🔬 Dry run synthesis: {data}")
        return {
            "status": "dry_run",
            "would_run": [
                "ResearchAgent",
                "ArchitectAgent",
                "CodeAgent",
                "TestAgent",
            ],
            "estimated_cost": 0.50,
            "timestamp": int(time.time()),
        }

    @router.get("/graph/{workspace_id}")
    async def debug_graph(workspace_id: str):
        return {
            "workspace_id": workspace_id,
            "nodes": 0,
            "edges": 0,
            "last_updated": int(time.time()),
        }

    @router.get("/rate-limits/{workspace_id}")
    async def debug_rate_limits(workspace_id: str):
        return {
            "workspace_id": workspace_id,
            "requests_this_minute": 0,
            "limit": 60,
            "remaining": 60,
            "resets_at": int(time.time()) + 60,
        }

    app.include_router(router)


# ─── Retry Decorator ───────────────────────────────────────
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt} failed: {e}. Retrying in {delay}s..."
                        )
                        import asyncio
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed: {e}")
            raise last_error

        return wrapper

    return decorator


# ─── Logging Helpers ───────────────────────────────────────
def log_agent_start(agent_name: str, context: RequestContext):
    context.mark_agent(f"[START] {agent_name}")
    logger.info(f"🚀 {agent_name} starting...")


def log_agent_end(agent_name: str, context: RequestContext, result: Any = None):
    elapsed = context.duration()
    logger.info(f"✅ {agent_name} completed in {elapsed:.2f}s")
    if result:
        logger.debug(f"   Result: {str(result)[:200]}")


def log_agent_error(agent_name: str, context: RequestContext, error: Exception):
    elapsed = context.duration()
    logger.error(f"❌ {agent_name} failed after {elapsed:.2f}s: {error}")
    logger.debug(traceback.format_exc())


# ─── Structured Log Format ───────────────────────────────────
class StructuredLogger:
    def __init__(self, component: str):
        self.component = component

    def log(self, level: str, event: str, **kwargs):
        record = {
            "timestamp": int(time.time()),
            "component": self.component,
            "event": event,
            **kwargs,
        }
        getattr(logger, level)(json.dumps(record))


def get_logger(component: str) -> StructuredLogger:
    return StructuredLogger(component)