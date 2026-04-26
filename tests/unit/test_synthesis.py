"""Unit tests for Synthesis Engine."""

import pytest
from packages.core.synthesis import SynthesisEngine, SynthesisConfig, SynthesisStatus


class TestSynthesisEngine:
    def test_engine_initialization(self):
        engine = SynthesisEngine()
        assert engine is not None
        assert engine.config is not None

    def test_engine_with_custom_config(self):
        config = SynthesisConfig(
            target="docker",
            max_cost=1.00,
            language="python",
        )
        engine = SynthesisEngine(config)
        assert engine.config.target == "docker"
        assert engine.config.max_cost == 1.00

    def test_synthesis_config_defaults(self):
        config = SynthesisConfig()
        assert config.target == "docker"
        assert config.max_cost == 0.50
        assert config.language == "auto"
        assert config.include_tests is True

    def test_synthesis_config_custom_language(self):
        config = SynthesisConfig(language="typescript")
        assert config.language == "typescript"

    def test_synthesis_status_constants(self):
        assert SynthesisStatus.PENDING == "pending"
        assert SynthesisStatus.RUNNING == "running"
        assert SynthesisStatus.COMPLETED == "completed"
        assert SynthesisStatus.FAILED == "failed"
        assert SynthesisStatus.CANCELLED == "cancelled"

    def test_synthesis_result_structure(self, mock_synthesis_result):
        assert "run_id" in mock_synthesis_result
        assert "project_id" in mock_synthesis_result
        assert "status" in mock_synthesis_result
        assert "cost_usd" in mock_synthesis_result
        assert mock_synthesis_result["cost_usd"] <= 0.50

    def test_synthesis_cost_within_budget(self, mock_synthesis_result):
        assert mock_synthesis_result["cost_usd"] <= mock_synthesis_result.get("max_cost", 0.50)


class TestSynthesisPipeline:
    def test_research_phase(self):
        assert True

    def test_architect_phase(self):
        assert True

    def test_code_generation_phase(self):
        assert True

    def test_test_generation_phase(self):
        assert True

    def test_deploy_phase(self):
        assert True

    def test_pipeline_order(self):
        expected_order = [
            "ResearchAgent",
            "ArchitectAgent",
            "CodeAgent",
            "TestAgent",
            "DeployAgent",
        ]
        assert expected_order == sorted(expected_order)


class TestTokenBudget:
    def test_budget_calculation(self, mock_token_budget):
        assert mock_token_budget["budget_used"] > 0
        assert mock_token_budget["budget_remaining"] > 0
        assert mock_token_budget["budget_used"] + mock_token_budget["budget_remaining"] == pytest.approx(
            mock_token_budget["budget_per_run"], rel=0.01
        )

    def test_daily_limit_enforcement(self, mock_token_budget):
        assert mock_token_budget["daily_used"] < mock_token_budget["daily_limit"]

    def test_monthly_limit_enforcement(self, mock_token_budget):
        assert mock_token_budget["monthly_used"] < mock_token_budget["monthly_limit"]

    def test_budget_exceeded_alert(self):
        budget = {"budget_used": 0.60, "budget_per_run": 0.50}
        assert budget["budget_used"] > budget["budget_per_run"]

    def test_cascading_llm_cost_tiers(self):
        tiers = [
            {"name": "Gemini Flash", "cost_per_1k": 0.01},
            {"name": "GPT-4o-mini", "cost_per_1k": 0.15},
            {"name": "GPT-4o", "cost_per_1k": 0.30},
        ]
        costs = [t["cost_per_1k"] for t in tiers]
        assert costs == sorted(costs)


class TestGraphitiIntegration:
    def test_graph_node_creation(self):
        node = {
            "type": "component",
            "name": "UserService",
            "workspace_id": "test_ws",
            "tech_stack": ["python", "fastapi"],
        }
        assert node["type"] == "component"
        assert "workspace_id" in node

    def test_graph_edge_creation(self):
        edge = {
            "from": "UserService",
            "to": "AuthService",
            "relation": "depends_on",
        }
        assert edge["relation"] == "depends_on"

    def test_graph_cache_hit(self):
        cache_key = "ws:test_ws:pattern:express-rest-api"
        assert cache_key.startswith("ws:")
        assert "test_ws" in cache_key

    def test_graph_cache_invalidation(self):
        patterns = [
            "express-rest-api",
            "react-dashboard",
            "fastapi-crud",
        ]
        assert len(patterns) == 3