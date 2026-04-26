"""
ProdSynth Backend — FastAPI + gRPC
Phase 0: Infrastructure & Core
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Telemetry (OpenTelemetry)
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Sentry
# import sentry_sdk
# from sentry_sdk.integrations.fastapi import FastApiIntegration

# Local modules (will be created in Phase 1-2)
# from core.synthesis import Synthesizer
# from agents.research import ResearchAgent
# from graph.adapter import GraphitiAdapter

# ─── Logging ───────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("prodsynth.backend")

# ─── Sentry (optional, Phase 2) ────────────────────────────────────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    # sentry_sdk.init(
    #     dsn=SENTRY_DSN,
    #     integrations=[FastApiIntegration()],
    #     traces_sample_rate=1.0,
    #     environment=os.getenv("ENV", "development"),
    # )
    logger.info("Sentry initialized")

# ─── Telemetry (OpenTelemetry, Phase 2) ─────────────────────────────────────
# if os.getenv("OTEL_ENABLED", "false").lower() == "true":
#     FastAPIInstrumentor().instrument()
#     RequestsInstrumentor().instrument()
#     logger.info("OpenTelemetry instrumentation enabled")

# ─── Lifespan (startup/shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup and shutdown events."""
    # Startup
    logger.info("🚀 ProdSynth Backend starting...")
    logger.info(f"Neo4j URI: {os.getenv('NEO4J_URI', 'not set')}")
    logger.info(f"Redis URL: {os.getenv('REDIS_URL', 'not set')}")
    logger.info(f"Postgres DB: {os.getenv('DATABASE_URL', 'not set')}")
    yield
    # Shutdown
    logger.info("🛑 ProdSynth Backend shutting down...")

# ─── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="ProdSynth API",
    description="AI-Native Product Synthesis Engine — API & gRPC",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "prodsynth-backend",
            "version": "0.1.0",
            "environment": os.getenv("ENV", "development"),
        },
        status_code=200,
    )

# ─── API v1 Routers (Phase 1-2) ─────────────────────────────────────────
# @app.get("/api/v1/analyze", tags=["Analysis"])
# async def analyze_repo(repo_url: str, depth: str = "shallow"):
#     """Analyze repository and build graph."""
#     return {"graph_id": "temp_123", "status": "pending"}

# @app.post("/api/v1/synthesize", tags=["Synthesis"])
# async def synthesize_product(graph_id: str, target: str = "saas"):
#     """Start product synthesis pipeline."""
#     return {"project_id": "proj_456", "status": "running"}

# @app.get("/api/v1/graph/{graph_id}", tags=["Graph"])
# async def get_graph(graph_id: str):
#     """Retrieve product graph (Graphiti)."""
#     return {"nodes": [], "edges": []}

# @app.post("/api/v1/deploy", tags=["Deploy"])
# async def deploy_product(project_id: str, target: str = "docker"):
#     """Deploy synthesized product."""
#     return {"url": "https://example.com", "status": "deployed"}

# ─── WebSocket (gRPC-like, Phase 1) ────────────────────────────────────
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message received: {data}")

# ─── Root ───────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "ProdSynth API — AI-Native Product Synthesis Engine",
        "docs": "/docs",
        "health": "/health",
        "version": "0.1.0",
    }

# ─── Error Handlers ─────────────────────────────────────────────────────────
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "code": exc.status_code},
    )

# ─── Main (for uvicorn) ──────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("ENV", "development") == "development",
        log_level="info",
    )
