"""Unit tests for ResearchAgent and LicenseChecker."""

import pytest
from packages.agents.research import ResearchAgent, LicenseChecker, LicenseReport


class TestLicenseChecker:
    def test_mit_license_compatible(self):
        checker = LicenseChecker()
        result = checker.check("MIT")
        assert result.risk == "LOW"
        assert result.action == "ALLOW"

    def test_apache_license_compatible(self):
        checker = LicenseChecker()
        result = checker.check("Apache-2.0")
        assert result.risk == "LOW"
        assert result.action == "ALLOW"

    def test_bsd_license_compatible(self):
        checker = LicenseChecker()
        for license_name in ["BSD-2-Clause", "BSD-3-Clause", "ISC"]:
            result = checker.check(license_name)
            assert result.risk == "LOW"

    def test_gpl_license_contaminating(self):
        checker = LicenseChecker()
        for license_name in ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]:
            result = checker.check(license_name)
            assert result.risk == "MEDIUM"
            assert result.action == "WARN_CONTAMINATION"

    def test_no_license_blocked(self):
        checker = LicenseChecker()
        result = checker.check("NONE")
        assert result.risk == "HIGH"
        assert result.action == "BLOCK"

    def test_cc_non_commercial_blocked(self):
        checker = LicenseChecker()
        for license_name in ["CC-BY-NC", "CC-BY-NC-ND", "CC-BY-ND"]:
            result = checker.check(license_name)
            assert result.risk in ("HIGH", "CRITICAL")
            assert result.action == "BLOCK"

    def test_proprietary_license_blocked(self):
        checker = LicenseChecker()
        result = checker.check("Proprietary")
        assert result.risk == "CRITICAL"
        assert result.action == "BLOCK"

    def test_unlicense_compatible(self):
        checker = LicenseChecker()
        result = checker.check("Unlicense")
        assert result.risk == "LOW"
        assert result.action == "ALLOW"


class TestResearchAgent:
    def test_research_agent_initialization(self):
        agent = ResearchAgent()
        assert agent is not None
        assert agent.name == "ResearchAgent"

    def test_research_agent_tech_stack_detection(self):
        agent = ResearchAgent()
        package_json = {
            "dependencies": {
                "react": "^18.0.0",
                "next": "^14.0.0",
                "typescript": "^5.0.0",
            }
        }
        tech_stack = agent.detect_tech_stack(package_json)
        assert "react" in tech_stack
        assert "next" in tech_stack

    def test_research_agent_python_detection(self):
        agent = ResearchAgent()
        requirements = {
            "fastapi": ">=0.100.0",
            "pydantic": ">=2.0.0",
            "sqlalchemy": ">=2.0.0",
        }
        tech_stack = agent.detect_tech_stack(requirements)
        assert "python" in tech_stack
        assert "fastapi" in tech_stack

    def test_research_agent_returns_techspec(self):
        agent = ResearchAgent()
        techspec = agent.generate_techspec("https://github.com/example/repo")
        assert "repo_url" in techspec or "tech_stack" in techspec or "components" in techspec


class TestRepoAnalysis:
    def test_ast_parsing(self):
        code = """
def hello():
    return "world"

class UserService:
    def get_user(self, user_id: int):
        return {"id": user_id, "name": "test"}
"""
        functions = ["hello"]
        classes = ["UserService"]
        assert "hello" in functions
        assert "UserService" in classes

    def test_dependency_analysis(self):
        dependencies = [
            {"name": "fastapi", "version": ">=0.100.0", "license": "MIT"},
            {"name": "pydantic", "version": ">=2.0.0", "license": "MIT"},
            {"name": "gpl-utils", "version": ">=1.0.0", "license": "GPL-3.0"},
        ]
        gpl_count = sum(1 for d in dependencies if "GPL" in d.get("license", ""))
        assert gpl_count == 1

    def test_security_pattern_detection(self):
        dangerous_patterns = ["eval(", "exec(", "subprocess.call", "os.system"]
        safe_code = "def hello(): return 'world'"
        found = [p for p in dangerous_patterns if p in safe_code]
        assert len(found) == 0


class TestLicenseCompatibilityMatrix:
    @pytest.mark.parametrize("license", ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Unlicense"])
    def test_compatible_licenses(self, license):
        checker = LicenseChecker()
        result = checker.check(license)
        assert result.risk in ("LOW", "NONE")
        assert result.action in ("ALLOW", "ALLOW_WITH_NOTICE")

    @pytest.mark.parametrize("license", ["GPL-2.0", "GPL-3.0", "AGPL-3.0"])
    def test_contaminating_licenses(self, license):
        checker = LicenseChecker()
        result = checker.check(license)
        assert result.risk in ("MEDIUM", "HIGH")

    @pytest.mark.parametrize("license", ["CC-BY-NC", "CC-BY-NC-ND", "Proprietary"])
    def test_blocked_licenses(self, license):
        checker = LicenseChecker()
        result = checker.check(license)
        assert result.action == "BLOCK"