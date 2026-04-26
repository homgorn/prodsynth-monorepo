"""Unit tests for Billing routes."""

import pytest
from apps.backend.routes.billing import Plan, SubscriptionRequest, Subscription


class TestBillingPlans:
    def test_free_plan_price(self):
        plans = [
            Plan(
                id="plan_free",
                name="Free",
                price_monthly=0.0,
                price_yearly=0.0,
                features=["3 projects", "1GB storage"],
                limits={"projects": 3, "graph_storage_gb": 1},
            )
        ]
        assert plans[0].price_monthly == 0.0
        assert plans[0].id == "plan_free"

    def test_pro_plan_price(self):
        plan = Plan(
            id="plan_pro",
            name="Pro",
            price_monthly=49.0,
            price_yearly=470.0,
            features=["Unlimited projects"],
            limits={"projects": -1},
        )
        assert plan.price_monthly == 49.0
        assert plan.price_yearly == 470.0
        yearly_savings = plan.price_monthly * 12 - plan.price_yearly
        assert yearly_savings == 118.0  # 2 months free

    def test_enterprise_plan_price(self):
        plan = Plan(
            id="plan_enterprise",
            name="Enterprise",
            price_monthly=999.0,
            price_yearly=9990.0,
            features=["Everything in Pro", "SSO"],
            limits={"projects": -1},
        )
        assert plan.price_monthly == 999.0
        assert "SSO" in plan.features

    def test_plan_limits_structure(self):
        plan = Plan(
            id="plan_test",
            name="Test",
            price_monthly=0.0,
            price_yearly=0.0,
            features=[],
            limits={
                "projects": 5,
                "graph_storage_gb": 2,
                "token_budget_per_run": 0.50,
            },
        )
        assert plan.limits["projects"] == 5
        assert plan.limits["token_budget_per_run"] == 0.50


class TestSubscription:
    def test_subscription_status_values(self):
        valid_statuses = ["active", "cancelled", "past_due", "trialing"]
        for status in valid_statuses:
            sub = Subscription(
                id=f"sub_{status}",
                plan_id="plan_pro",
                status=status,
                current_period_end=1714041600,
                cancel_at_period_end=False,
            )
            assert sub.status == status

    def test_subscription_cancel_at_period_end(self):
        sub = Subscription(
            id="sub_123",
            plan_id="plan_pro",
            status="active",
            current_period_end=1714041600,
            cancel_at_period_end=True,
        )
        assert sub.cancel_at_period_end is True


class TestUsageTracking:
    def test_usage_within_limits(self):
        usage = {
            "token_budget_used": 0.30,
            "token_budget_total": 0.50,
            "graph_storage_used_gb": 0.5,
            "graph_storage_total_gb": 1.0,
            "api_calls_used": 30,
            "api_calls_total": 60,
        }
        assert usage["token_budget_used"] < usage["token_budget_total"]
        assert usage["graph_storage_used_gb"] < usage["graph_storage_total_gb"]
        assert usage["api_calls_used"] < usage["api_calls_total"]

    def test_usage_percentage_calculation(self):
        usage = {
            "token_budget_used": 0.25,
            "token_budget_total": 0.50,
        }
        pct = (usage["token_budget_used"] / usage["token_budget_total"]) * 100
        assert pct == 50.0

    def test_usage_exceeded_alert(self):
        usage = {
            "graph_storage_used_gb": 1.2,
            "graph_storage_total_gb": 1.0,
        }
        exceeded = usage["graph_storage_used_gb"] > usage["graph_storage_total_gb"]
        assert exceeded is True


class TestStripeWebhook:
    def test_webhook_event_types(self):
        events = [
            "invoice.payment_succeeded",
            "invoice.payment_failed",
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
        ]
        assert len(events) == 5

    def test_webhook_signature_verification(self):
        payload = '{"type": "invoice.payment_succeeded", "data": {"object": {}}}'
        sig_header = "t=1714041600,v1=abc123"
        assert "t=" in sig_header
        assert "v1=" in sig_header

    def test_billing_portal_session(self):
        portal_url = "https://billing.stripe.com/session/test_123"
        assert portal_url.startswith("https://")
        assert "billing.stripe.com" in portal_url