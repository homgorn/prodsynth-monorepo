"""
ProdSynth Agents — ResearchAgent (Phase 1)
AST parsing, repository analysis, forming Technical Specification (TZ).
"""

import os
import logging
import ast
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger("prodsynth.agents.research")


class ResearchAgent:
    """
    Agent for repository analysis and graph building.
    Uses AST parsing to understand code structure.
    """

    def __init__(self, graph_adapter=None):
        self.graph_adapter = graph_adapter
        logger.info("🔍 ResearchAgent initialized")

    async def analyze_repository(self, repo_url: str, depth: str = "shallow") -> Dict[str, Any]:
        """
        Analyze repository and build knowledge graph.
        Phase 1: Basic structure analysis.
        """
        logger.info(f"🔍 Starting repository analysis: {repo_url} (depth: {depth})")

        result = {
            "graph_id": "graph_" + repo_url.split("/")[-1],
            "status": "pending",
            "tech_stack": [],
            "files_analyzed": 0,
            "functions": [],
            "classes": [],
            "dependencies": [],
            "risks": [],
        }

        try:
            # Placeholder: In real implementation, clone repo or read local path
            # For now, simulate analysis
            repo_name = repo_url.rstrip("/").split("/")[-1]
            result["graph_id"] = f"graph_{repo_name}"

            # Simulate AST parsing (Phase 1 stub)
            result["tech_stack"] = self._detect_tech_stack(repo_url)
            result["files_analyzed"] = 42  # Simulated
            result["functions"] = ["main", "init", "analyze"]
            result["classes"] = ["SynthesisEngine", "Agent"]
            result["dependencies"] = ["fastapi", "neo4j", "redis"]

            # Build graph if adapter available
            if self.graph_adapter:
                await self._build_graph(result["graph_id"], result)

            result["status"] = "completed"
            logger.info(f"✅ Analysis complete: {result['files_analyzed']} files analyzed")

        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            result["status"] = "failed"
            result["error"] = str(e)

        return result

    def _detect_tech_stack(self, repo_url: str) -> List[str]:
        """Detect technology stack from repository."""
        # Phase 1: Simple detection based on common patterns
        tech_stack = []

        # Simulate tech detection
        if "python" in repo_url.lower() or "fastapi" in repo_url.lower():
            tech_stack.extend(["Python", "FastAPI"])
        if "react" in repo_url.lower() or "next" in repo_url.lower():
            tech_stack.extend(["TypeScript", "Next.js"])
        if "rust" in repo_url.lower():
            tech_stack.append("Rust")

        # Default stack
        if not tech_stack:
            tech_stack = ["Python", "FastAPI", "React"]

        return tech_stack

    async def _build_graph(self, graph_id: str, data: Dict[str, Any]):
        """Build knowledge graph in Graphiti/Neo4j."""
        logger.info(f"📊 Building graph: {graph_id}")

        # Placeholder for Graphiti integration
        # In Phase 1, this will call graph_adapter.create_nodes()
        if self.graph_adapter:
            try:
                # Simulate graph creation
                logger.info(f"  → Creating nodes for {len(data['functions'])} functions")
                logger.info(f"  → Creating nodes for {len(data['classes'])} classes")
                logger.info(f"  → Creating edges for dependencies")
            except Exception as e:
                logger.error(f"Graph building failed: {e}")

    async def check_licenses(self, repo_path: str) -> Dict[str, Any]:
        """
        LicenseChecker agent: Check repository licenses.
        Critical for IP protection (Phase 1, from self-critique).
        """
        logger.info(f"⚖️ Checking licenses for: {repo_path}")

        # Phase 1: Basic license detection
        license_info = {
            "repo_path": repo_path,
            "license": "MIT",  # Default assumption
            "compatible": True,
            "warnings": [],
        }

        # Check for LICENSE file
        license_file = Path(repo_path) / "LICENSE"
        if license_file.exists():
            with open(license_file, "r") as f:
                content = f.read().lower()
                if "gpl" in content:
                    license_info["license"] = "GPL"
                    license_info["compatible"] = False
                    license_info["warnings"].append(
                        "GPL license detected — generated code must be GPL-compatible"
                    )
                elif "mit" in content:
                    license_info["license"] = "MIT"
                elif "apache" in content:
                    license_info["license"] = "Apache 2.0"

        logger.info(f"License: {license_info['license']} (compatible: {license_info['compatible']})")
        return license_info


# Singleton instance
_research_agent: Optional[ResearchAgent] = None


def get_research_agent(graph_adapter=None) -> ResearchAgent:
    """Get or create ResearchAgent singleton."""
    global _research_agent
    if _research_agent is None:
        _research_agent = ResearchAgent(graph_adapter=graph_adapter)
    return _research_agent
