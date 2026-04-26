"""Pytest configuration and fixtures for ProdSynth."""

import pytest
import asyncio
from typing import Generator


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_workspace_id() -> str:
    return "test_ws_001"


@pytest.fixture
def mock_user_id() -> str:
    return "test_user_001"


@pytest.fixture
def mock_project_data() -> dict:
    return {
        "id": "proj_test_123",
        "name": "test-project",
        "description": "A test project for unit testing",
        "workspace_id": "test_ws_001",
        "tech_stack": ["python", "fastapi", "react"],
        "status": "draft",
    }


@pytest.fixture
def mock_synthesis_result() -> dict:
    return {
        "run_id": "run_test_123",
        "project_id": "proj_test_123",
        "status": "completed",
        "agents_completed": [
            "ResearchAgent",
            "ArchitectAgent",
            "CodeAgent",
            "TestAgent",
            "DeployAgent",
        ],
        "files_generated": 127,
        "tests_generated": 84,
        "coverage": 0.81,
        "deployed_url": "https://test-app.onrender.com",
        "cost_usd": 0.47,
        "duration_seconds": 312,
    }


@pytest.fixture
def mock_token_budget() -> dict:
    return {
        "workspace_id": "test_ws_001",
        "budget_per_run": 0.50,
        "budget_used": 0.23,
        "budget_remaining": 0.27,
        "daily_limit": 5.00,
        "daily_used": 1.23,
        "monthly_limit": 20.00,
        "monthly_used": 5.47,
    }


@pytest.fixture
def mock_license_report() -> dict:
    return {
        "license": "MIT",
        "risk": "LOW",
        "message": "MIT License is compatible with MIT distribution.",
        "action": "ALLOW",
    }


@pytest.fixture
def mock_audit_event() -> dict:
    return {
        "id": "audit_test_001",
        "workspace_id": "test_ws_001",
        "user_id": "test_user_001",
        "action": "project.create",
        "resource_type": "project",
        "resource_id": "proj_test_123",
        "timestamp": 1714041600,
        "ip_address": "127.0.0.1",
        "status": "success",
        "details": {},
    }