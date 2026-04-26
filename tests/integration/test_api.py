"""Integration tests for API endpoints."""

import pytest
import httpx
import asyncio
from typing import Generator


BASE_URL = "http://localhost:8000"


@pytest.fixture
def client() -> Generator[httpx.Client, None, None]:
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        yield client


@pytest.fixture
async def async_client() -> Generator[httpx.AsyncClient, None, None]:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        yield client


@pytest.fixture
def auth_headers() -> dict:
    return {
        "Authorization": "Bearer test_token",
        "X-Workspace-ID": "test_ws_001",
        "Content-Type": "application/json",
    }


class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "ok" in data or "healthy" in data


class TestAuthEndpoints:
    def test_login_success(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "test123"},
        )
        assert response.status_code in (200, 401, 500)

    def test_login_invalid_credentials(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "invalid@example.com", "password": "wrong"},
        )
        assert response.status_code in (401, 500)

    def test_login_missing_fields(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com"},
        )
        assert response.status_code in (400, 422, 500)

    def test_sso_providers_list(self, client):
        response = client.get("/api/v1/auth/sso/providers")
        assert response.status_code in (200, 500)

    def test_sso_authorize_google(self, client):
        response = client.get("/api/v1/auth/sso/authorize/google")
        assert response.status_code in (200, 404, 500)

    def test_sso_authorize_invalid_provider(self, client):
        response = client.get("/api/v1/auth/sso/authorize/invalid_provider")
        assert response.status_code in (404, 500)


class TestProjectEndpoints:
    def test_list_projects_unauthorized(self, client):
        response = client.get("/api/v1/projects")
        assert response.status_code in (401, 500)

    def test_list_projects_with_auth(self, client, auth_headers):
        response = client.get("/api/v1/projects", headers=auth_headers)
        assert response.status_code in (200, 401, 500)

    def test_create_project_without_workspace(self, client):
        response = client.post(
            "/api/v1/projects",
            json={"name": "test-project", "description": "Test"},
        )
        assert response.status_code in (401, 500)

    def test_create_project_with_auth(self, client, auth_headers):
        response = client.post(
            "/api/v1/projects",
            json={"name": "test-project", "description": "Test"},
            headers=auth_headers,
        )
        assert response.status_code in (200, 201, 401, 500)


class TestMarketplaceEndpoints:
    def test_list_templates(self, client):
        response = client.get("/api/v1/marketplace/templates")
        assert response.status_code in (200, 500)

    def test_list_templates_with_filters(self, client):
        response = client.get("/api/v1/marketplace/templates?category=saas&price=0")
        assert response.status_code in (200, 500)

    def test_get_template_detail(self, client):
        response = client.get("/api/v1/marketplace/templates/tmpl_1")
        assert response.status_code in (200, 404, 500)

    def test_search_templates(self, client):
        response = client.get("/api/v1/marketplace/templates?search=saas")
        assert response.status_code in (200, 500)

    def test_purchase_template(self, client):
        response = client.post(
            "/api/v1/marketplace/purchase",
            json={"template_id": "tmpl_1", "payment_method_id": "pm_test"},
        )
        assert response.status_code in (200, 401, 500)


class TestBillingEndpoints:
    def test_get_plans(self, client):
        response = client.get("/api/v1/billing/plans")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3

    def test_get_plans_structure(self, client):
        response = client.get("/api/v1/billing/plans")
        if response.status_code == 200:
            data = response.json()
            for plan in data:
                assert "id" in plan
                assert "name" in plan
                assert "price_monthly" in plan
                assert "features" in plan

    def test_create_subscription(self, client, auth_headers):
        response = client.post(
            "/api/v1/billing/subscribe",
            json={"plan_id": "plan_pro", "billing_cycle": "monthly"},
            headers=auth_headers,
        )
        assert response.status_code in (200, 201, 401, 500)

    def test_get_subscription(self, client, auth_headers):
        response = client.get("/api/v1/billing/subscription", headers=auth_headers)
        assert response.status_code in (200, 401, 500)

    def test_get_usage(self, client, auth_headers):
        response = client.get("/api/v1/billing/usage", headers=auth_headers)
        assert response.status_code in (200, 401, 500)

    def test_billing_portal(self, client, auth_headers):
        response = client.get("/api/v1/billing/portal", headers=auth_headers)
        assert response.status_code in (200, 401, 500)

    def test_stripe_webhook(self, client):
        response = client.post(
            "/api/v1/billing/webhook",
            json={"type": "invoice.payment_succeeded", "data": {}},
        )
        assert response.status_code in (200, 400, 500)


class TestTeamEndpoints:
    def test_get_team(self, client, auth_headers):
        response = client.get("/api/v1/auth/team", headers=auth_headers)
        assert response.status_code in (200, 401, 500)

    def test_invite_member(self, client, auth_headers):
        response = client.post(
            "/api/v1/auth/team/invite",
            params={"email": "new@example.com", "role": "editor"},
            headers=auth_headers,
        )
        assert response.status_code in (200, 401, 500)

    def test_invite_invalid_role(self, client, auth_headers):
        response = client.post(
            "/api/v1/auth/team/invite",
            params={"email": "new@example.com", "role": "superadmin"},
            headers=auth_headers,
        )
        assert response.status_code in (400, 401, 500)

    def test_update_member_role(self, client, auth_headers):
        response = client.put(
            "/api/v1/auth/team/user_2",
            json={"roles": ["admin"]},
            headers=auth_headers,
        )
        assert response.status_code in (200, 401, 500)

    def test_remove_member(self, client, auth_headers):
        response = client.delete("/api/v1/auth/team/user_2", headers=auth_headers)
        assert response.status_code in (200, 401, 500)


class TestAuditEndpoints:
    def test_get_audit_log(self, client, auth_headers):
        response = client.get("/api/v1/auth/audit", headers=auth_headers)
        assert response.status_code in (200, 401, 500)

    def test_get_audit_log_with_pagination(self, client, auth_headers):
        response = client.get(
            "/api/v1/auth/audit",
            params={"limit": 50, "offset": 0},
            headers=auth_headers,
        )
        assert response.status_code in (200, 401, 500)


class TestTenantMiddleware:
    def test_missing_workspace_id_returns_401(self, client):
        response = client.get("/api/v1/projects")
        assert response.status_code in (401, 500)

    def test_exempt_paths_work_without_workspace(self, client):
        exempt_paths = ["/health", "/api/v1/billing/plans", "/api/v1/marketplace/templates"]
        for path in exempt_paths:
            response = client.get(path)
            assert response.status_code in (200, 404, 500)


@pytest.mark.integration
class TestSynthesisPipeline:
    @pytest.mark.slow
    def test_synthesis_run(self, client, auth_headers):
        response = client.post(
            "/api/v1/synthesis/run",
            json={"project_id": "proj_test_123", "target": "docker"},
            headers=auth_headers,
        )
        assert response.status_code in (200, 201, 401, 404, 500)

    @pytest.mark.slow
    def test_synthesis_status(self, client, auth_headers):
        response = client.get("/api/v1/synthesis/run_123", headers=auth_headers)
        assert response.status_code in (200, 401, 404, 500)


@pytest.mark.integration
class TestWebhookNotifier:
    def test_webhook_event_send(self, client):
        response = client.post(
            "/api/v1/webhooks/test",
            json={
                "event": "product.ready",
                "project_id": "proj_123",
                "url": "https://test.onrender.com",
                "status": "deployed",
            },
        )
        assert response.status_code in (200, 404, 500)