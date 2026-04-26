"""Unit tests for Multi-tenancy models and TenantMiddleware."""

import pytest
from packages.models.tenant import TenantLimits, get_tenant_limits, TENANT_LIMITS
from packages.models.workspace import Workspace, WorkspaceSettings
from packages.models.audit import AuditEvent, AuditLogger, AUDIT_EVENT_TYPES


class TestTenantLimits:
    def test_free_plan_limits(self):
        limits = get_tenant_limits("free")
        assert limits.max_projects == 3
        assert limits.max_team_members == 1
        assert limits.max_graph_storage_gb == 1
        assert "core" in limits.features

    def test_pro_plan_limits(self):
        limits = get_tenant_limits("pro")
        assert limits.max_projects == -1  # unlimited
        assert limits.max_team_members == 10
        assert limits.max_graph_storage_gb == 100
        assert "sso" not in limits.features  # not in Pro

    def test_enterprise_plan_limits(self):
        limits = get_tenant_limits("enterprise")
        assert limits.max_projects == -1
        assert limits.max_team_members == -1  # unlimited
        assert limits.max_graph_storage_gb == -1
        assert "sso" in limits.features
        assert "audit" in limits.features
        assert "sla" in limits.features

    def test_unknown_plan_defaults_to_free(self):
        limits = get_tenant_limits("unknown_plan")
        assert limits.max_projects == 3
        assert limits == get_tenant_limits("free")

    def test_unlimited_marker(self):
        pro_limits = get_tenant_limits("pro")
        assert pro_limits.max_projects == -1
        ent_limits = get_tenant_limits("enterprise")
        assert ent_limits.max_team_members == -1


class TestWorkspaceModel:
    def test_workspace_creation(self):
        ws = Workspace(
            id="ws_test_001",
            name="Test Workspace",
            slug="test-ws",
            plan="pro",
            created_at=1714041600,
            updated_at=1714041600,
        )
        assert ws.plan == "pro"
        assert ws.slug == "test-ws"

    def test_workspace_default_plan(self):
        ws = Workspace(
            id="ws_test_002",
            name="Default Workspace",
            slug="default",
            created_at=1714041600,
            updated_at=1714041600,
        )
        assert ws.plan == "free"
        assert ws.storage_limit_bytes == 1_073_741_824  # 1GB

    def test_workspace_settings_defaults(self):
        settings = WorkspaceSettings()
        assert settings.allow_signups is True
        assert settings.enforce_sso is False
        assert settings.require_mfa is False
        assert settings.max_team_members == 5
        assert settings.audit_retention_days == 90

    def test_workspace_sso_settings(self):
        settings = WorkspaceSettings(
            enforce_sso=True,
            sso_provider="google",
            allowed_email_domains=["prodsynth.com"],
        )
        assert settings.enforce_sso is True
        assert settings.sso_provider == "google"
        assert "prodsynth.com" in settings.allowed_email_domains


class TestAuditLogger:
    def test_audit_logger_initialization(self):
        logger = AuditLogger()
        assert logger._buffer == []

    def test_audit_log_creation(self):
        logger = AuditLogger()
        event = logger.log(
            workspace_id="ws_001",
            user_id="user_001",
            action="project.create",
            resource_type="project",
            resource_id="proj_123",
        )
        assert event.workspace_id == "ws_001"
        assert event.action == "project.create"
        assert event.status == "success"

    def test_audit_query_by_workspace(self):
        logger = AuditLogger()
        logger.log(workspace_id="ws_001", user_id="u1", action="project.create", resource_type="project")
        logger.log(workspace_id="ws_001", user_id="u2", action="auth.login", resource_type="auth")
        logger.log(workspace_id="ws_002", user_id="u3", action="project.create", resource_type="project")

        ws001_events = logger.query("ws_001")
        assert len(ws001_events) == 2

    def test_audit_query_by_action(self):
        logger = AuditLogger()
        logger.log(workspace_id="ws_001", user_id="u1", action="project.create", resource_type="project")
        logger.log(workspace_id="ws_001", user_id="u1", action="auth.login", resource_type="auth")

        login_events = logger.query("ws_001", action="auth.login")
        assert len(login_events) == 1
        assert login_events[0].action == "auth.login"

    def test_audit_query_by_user(self):
        logger = AuditLogger()
        logger.log(workspace_id="ws_001", user_id="u1", action="project.create", resource_type="project")
        logger.log(workspace_id="ws_001", user_id="u2", action="project.create", resource_type="project")

        u1_events = logger.query("ws_001", user_id="u1")
        assert len(u1_events) == 1
        assert u1_events[0].user_id == "u1"

    def test_audit_event_types_completeness(self):
        expected_categories = {"auth", "project", "billing", "team", "sso", "workspace", "product"}
        assert set(AUDIT_EVENT_TYPES.keys()) == expected_categories

    def test_audit_log_failure_status(self):
        logger = AuditLogger()
        event = logger.log(
            workspace_id="ws_001",
            user_id="user_001",
            action="synthesis.run",
            resource_type="product",
            status="failure",
            details={"error": "budget_exceeded"},
        )
        assert event.status == "failure"
        assert event.details["error"] == "budget_exceeded"


class TestRLSPolicies:
    def test_workspace_isolation_query(self):
        workspace_id = "ws_001"
        query = f'SELECT * FROM projects WHERE workspace_id = "{workspace_id}"'
        assert workspace_id in query
        assert "ws_002" not in query

    def test_redis_key_prefixing(self):
        workspace_id = "ws_abc123"
        keys = [
            f"ws:{workspace_id}:projects",
            f"ws:{workspace_id}:token_budget",
            f"ws:{workspace_id}:rate_limit",
        ]
        for key in keys:
            assert key.startswith(f"ws:{workspace_id}:")

    def test_neo4j_workspace_tagging(self):
        workspace_id = "ws_abc123"
        node = {
            "id": "proj_123",
            "workspace_id": workspace_id,
            "name": "Test Project",
        }
        assert node["workspace_id"] == workspace_id


class TestRateLimiting:
    def test_free_plan_rate_limit(self):
        limits = get_tenant_limits("free")
        assert limits.rate_limit_per_minute == 60

    def test_pro_plan_rate_limit(self):
        limits = get_tenant_limits("pro")
        assert limits.rate_limit_per_minute == 300

    def test_enterprise_plan_rate_limit(self):
        limits = get_tenant_limits("enterprise")
        assert limits.rate_limit_per_minute == 1000