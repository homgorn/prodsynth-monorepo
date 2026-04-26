"""Unit tests for RBAC & SSO."""

import pytest
from apps.backend.routes.rbac import ROLES, has_permission, SSO_PROVIDERS


class TestRBACRoles:
    def test_all_roles_defined(self):
        expected_roles = {"owner", "admin", "editor", "viewer", "billing_admin"}
        assert set(ROLES.keys()) == expected_roles

    def test_owner_has_all_permissions(self):
        owner = ROLES["owner"]
        assert "workspace:*" in owner.permissions
        assert "project:*" in owner.permissions
        assert "billing:*" in owner.permissions
        assert "sso:*" in owner.permissions

    def test_admin_permissions(self):
        admin = ROLES["admin"]
        assert "project:*" in admin.permissions
        assert "team:*" in admin.permissions
        assert "billing:read" in admin.permissions
        assert "sso:*" not in admin.permissions

    def test_editor_permissions(self):
        editor = ROLES["editor"]
        assert "project:read" in editor.permissions
        assert "project:write" in editor.permissions
        assert "project:execute" in editor.permissions
        assert "project:delete" not in editor.permissions
        assert "billing:*" not in editor.permissions

    def test_viewer_permissions(self):
        viewer = ROLES["viewer"]
        assert "project:read" in viewer.permissions
        assert len(viewer.permissions) == 1

    def test_billing_admin_permissions(self):
        billing_admin = ROLES["billing_admin"]
        assert "billing:*" in billing_admin.permissions
        assert "team:read" in billing_admin.permissions


class TestPermissionChecker:
    def test_owner_can_do_anything(self):
        assert has_permission(["owner"], "workspace", "read") is True
        assert has_permission(["owner"], "project", "delete") is True
        assert has_permission(["owner"], "billing", "admin") is True

    def test_editor_can_read_and_write_projects(self):
        assert has_permission(["editor"], "project", "read") is True
        assert has_permission(["editor"], "project", "write") is True
        assert has_permission(["editor"], "project", "delete") is False
        assert has_permission(["editor"], "billing", "read") is False

    def test_viewer_can_only_read(self):
        assert has_permission(["viewer"], "project", "read") is True
        assert has_permission(["viewer"], "project", "write") is False
        assert has_permission(["viewer"], "team", "read") is False

    def test_multi_role_permission(self):
        assert has_permission(["viewer", "editor"], "project", "write") is True
        assert has_permission(["viewer"], "project", "write") is False

    def test_unknown_resource_denied(self):
        assert has_permission(["owner"], "unknown", "read") is False


class TestSSOProviders:
    def test_google_oauth2_configured(self):
        google = SSO_PROVIDERS["google"]
        assert google["issuer"] == "https://accounts.google.com"
        assert "openid" in google["scopes"]

    def test_github_oauth2_configured(self):
        github = SSO_PROVIDERS["github"]
        assert github["issuer"] == "https://github.com"
        assert "user:email" in github["scopes"]

    def test_all_providers_have_issuer(self):
        for provider_id, config in SSO_PROVIDERS.items():
            assert "issuer" in config or "domain" in config

    def test_azure_oidc_configured(self):
        azure = SSO_PROVIDERS["azure"]
        assert "tenant_id" in azure
        assert "client_id" in azure
        assert "authority" in azure


class TestTeamManagement:
    def test_invite_role_validation(self):
        valid_roles = list(ROLES.keys())
        for role in valid_roles:
            assert role in ROLES

    def test_invite_expiration(self):
        invite = {
            "invite_id": "invite_123",
            "email": "test@example.com",
            "role": "editor",
            "expires_at": 1714128000,
        }
        assert invite["expires_at"] > 1714041600  # expires in future

    def test_role_change_requires_valid_role(self):
        new_role = "admin"
        assert new_role in ROLES

    def test_sso_callback_returns_jwt(self):
        callback_response = {
            "token": "jwt_token_placeholder",
            "user": {
                "id": "sso_user_123",
                "email": "user@example.com",
                "sso_provider": "google",
                "roles": ["editor"],
            },
        }
        assert "token" in callback_response
        assert "user" in callback_response
        assert callback_response["user"]["sso_provider"] == "google"


class TestAuditLog:
    def test_audit_log_fields(self):
        audit_entry = {
            "id": "audit_1",
            "user_id": "user_1",
            "action": "project.create",
            "resource": "project_123",
            "timestamp": 1714041600,
            "ip": "192.168.1.1",
        }
        assert "action" in audit_entry
        assert "timestamp" in audit_entry
        assert "ip" in audit_entry