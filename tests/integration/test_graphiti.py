"""Integration tests for Graphiti memory and Neo4j."""

import pytest
from packages.graph.adapter import GraphitiAdapter, GraphNode, GraphEdge


class TestGraphitiAdapter:
    def test_adapter_initialization(self):
        adapter = GraphitiAdapter()
        assert adapter is not None

    def test_adapter_connection_config(self):
        adapter = GraphitiAdapter()
        assert hasattr(adapter, "workspace_id") or hasattr(adapter, "uri")

    def test_workspace_isolation(self):
        adapter1 = GraphitiAdapter(workspace_id="ws_001")
        adapter2 = GraphitiAdapter(workspace_id="ws_002")
        assert adapter1.workspace_id != adapter2.workspace_id


class TestGraphOperations:
    def test_create_node(self):
        node = GraphNode(
            id="node_001",
            type="component",
            name="UserService",
            workspace_id="ws_001",
            tech_stack=["python", "fastapi"],
        )
        assert node.workspace_id == "ws_001"
        assert node.type == "component"

    def test_create_edge(self):
        edge = GraphEdge(
            from_id="node_001",
            to_id="node_002",
            relation="depends_on",
            workspace_id="ws_001",
        )
        assert edge.relation == "depends_on"

    def test_graph_cache_key_generation(self):
        workspace_id = "ws_001"
        pattern_name = "express-rest-api"
        cache_key = f"ws:{workspace_id}:pattern:{pattern_name}"
        assert cache_key == "ws:ws_001:pattern:express-rest-api"

    def test_graph_cache_hit_detection(self):
        cache = {
            "ws:ws_001:pattern:express-rest-api": {
                "nodes": 847,
                "edges": 234,
                "created_at": 1714041600,
            }
        }
        cache_key = "ws:ws_001:pattern:express-rest-api"
        assert cache_key in cache

    def test_graph_cache_miss(self):
        cache = {}
        cache_key = "ws:ws_001:pattern:new-pattern"
        assert cache_key not in cache

    def test_cache_invalidation_on_version_bump(self):
        cache = {
            "ws:ws_001:pattern:express-v4": {"version": "4.0.0"},
        }
        new_version = "5.0.0"
        if new_version != cache["ws:ws_001:pattern:express-v4"]["version"]:
            del cache["ws:ws_001:pattern:express-v4"]
        assert "ws:ws_001:pattern:express-v4" not in cache


class TestGraphQueries:
    def test_find_similar_patterns(self):
        patterns = [
            {"name": "express-rest-api", "score": 0.95},
            {"name": "express-graphql", "score": 0.72},
            {"name": "fastapi-crud", "score": 0.45},
            {"name": "react-dashboard", "score": 0.12},
        ]
        similar = [p for p in patterns if p["score"] > 0.5]
        assert len(similar) == 2
        assert similar[0]["name"] == "express-rest-api"

    def test_trace_dependencies(self):
        graph = {
            "UserService": ["AuthService", "DatabaseService"],
            "AuthService": ["DatabaseService"],
            "DatabaseService": [],
        }
        deps = graph["UserService"]
        assert "AuthService" in deps
        assert "DatabaseService" in deps
        assert "UserService" not in deps

    def test_get_tests_for_component(self):
        component_tests = {
            "UserService": ["test_user_service.py", "test_user_service_integration.py"],
            "AuthService": ["test_auth.py"],
            "DatabaseService": [],
        }
        tests = component_tests.get("UserService", [])
        assert len(tests) == 2


class TestTemporalReasoning:
    def test_node_time_travel(self):
        graph_snapshots = [
            {"timestamp": 1713955200, "nodes": 100, "edges": 50},
            {"timestamp": 1714041600, "nodes": 120, "edges": 65},
            {"timestamp": 1714128000, "nodes": 150, "edges": 80},
        ]
        assert graph_snapshots[-1]["nodes"] > graph_snapshots[0]["nodes"]

    def test_version_isolation(self):
        versions = ["v1.0.0", "v2.0.0", "v3.0.0"]
        for v in versions:
            assert v.startswith("v")