"""Unit tests for Product DNA system."""

import pytest
from packages.agents.dna import ProductDNA, PatternGene, ProductGenome, DNAResult


class TestPatternGene:
    def test_gene_creation(self):
        gene = PatternGene(
            id="gene_auth_001",
            name="JWT Auth Pattern",
            category="auth",
            description="JWT authentication",
            tech_stack=["python", "fastapi"],
            usage_count=1,
            success_rate=0.95,
            tags=["auth", "jwt"],
        )
        assert gene.id == "gene_auth_001"
        assert gene.category == "auth"
        assert gene.success_rate == 0.95
        assert "jwt" in gene.tags

    def test_gene_defaults(self):
        gene = PatternGene(
            id="gene_test",
            name="Test",
            category="testing",
            description="Test pattern",
            tech_stack=["python"],
        )
        assert gene.usage_count == 1
        assert gene.success_rate == 1.0
        assert gene.tags == []
        assert gene.metadata == {}


class TestProductDNA:
    def test_dna_initialization(self):
        dna = ProductDNA(workspace_id="ws_001")
        assert dna.workspace_id == "ws_001"
        assert dna.genes == {}
        assert dna.genomes == {}

    def test_extract_auth_genes(self):
        dna = ProductDNA(workspace_id="ws_001")
        result = {
            "project_id": "proj_001",
            "tech_stack": ["python", "fastapi", "jwt"],
            "files_generated": 50,
        }
        genes = dna.extract_genes(result)
        auth_genes = [g for g in genes if g.category == "auth"]
        assert len(auth_genes) >= 1

    def test_extract_api_genes(self):
        dna = ProductDNA(workspace_id="ws_001")
        result = {
            "project_id": "proj_002",
            "tech_stack": ["python", "fastapi", "sqlalchemy"],
            "files_generated": 100,
        }
        genes = dna.extract_genes(result)
        api_genes = [g for g in genes if g.category == "api"]
        assert len(api_genes) >= 1

    def test_extract_multiple_patterns(self):
        dna = ProductDNA(workspace_id="ws_001")
        result = {
            "project_id": "proj_003",
            "tech_stack": ["python", "fastapi", "react", "postgresql", "pytest"],
            "files_generated": 200,
            "tests_generated": 84,
        }
        genes = dna.extract_genes(result)
        categories = {g.category for g in genes}
        assert "auth" in categories
        assert "api" in categories
        assert "database" in categories
        assert "frontend" in categories
        assert "testing" in categories

    def test_analyze_dna_matched_genes(self):
        dna = ProductDNA(workspace_id="ws_001")
        gene = PatternGene(
            id="gene_auth_001",
            name="JWT Auth",
            category="auth",
            description="JWT",
            tech_stack=["python", "fastapi"],
        )
        dna.genes["gene_auth_001"] = gene

        result = dna.analyze_dna(["python", "fastapi"])
        assert len(result.matched_genes) >= 1

    def test_analyze_dna_time_savings(self):
        dna = ProductDNA(workspace_id="ws_001")
        for i in range(3):
            gene = PatternGene(
                id=f"gene_{i}",
                name=f"Gene {i}",
                category="auth",
                description="Test",
                tech_stack=["python", "fastapi"],
            )
            dna.genes[f"gene_{i}"] = gene

        result = dna.analyze_dna(["python", "fastapi"])
        assert result.estimated_time_savings >= 0.10
        assert result.estimated_time_savings <= 0.50

    def test_update_gene_success(self):
        dna = ProductDNA(workspace_id="ws_001")
        gene = PatternGene(
            id="gene_001",
            name="Test Gene",
            category="auth",
            description="Test",
            tech_stack=["python"],
            usage_count=1,
            success_rate=1.0,
        )
        dna.genes["gene_001"] = gene

        dna.update_gene_success("gene_001", success=True, quality_score=0.9)
        assert dna.genes["gene_001"].usage_count == 2
        assert dna.genes["gene_001"].success_rate == 1.0  # still 1.0 (100%)

    def test_update_gene_failure(self):
        dna = ProductDNA(workspace_id="ws_001")
        gene = PatternGene(
            id="gene_002",
            name="Test Gene",
            category="auth",
            description="Test",
            tech_stack=["python"],
            usage_count=1,
            success_rate=1.0,
        )
        dna.genes["gene_002"] = gene

        dna.update_gene_success("gene_002", success=False, quality_score=0.5)
        assert dna.genes["gene_002"].usage_count == 2
        assert dna.genes["gene_002"].success_rate == 0.5  # 50%

    def test_get_top_genes(self):
        dna = ProductDNA(workspace_id="ws_001")
        for i, rate in enumerate([0.8, 0.95, 0.7, 0.9]):
            gene = PatternGene(
                id=f"gene_{i}",
                name=f"Gene {i}",
                category="auth",
                description="Test",
                tech_stack=["python"],
                usage_count=i + 1,
                success_rate=rate,
            )
            dna.genes[f"gene_{i}"] = gene

        top = dna.get_top_genes(category="auth", limit=3)
        assert len(top) == 3
        assert top[0].success_rate >= top[1].success_rate

    def test_crossbreed(self):
        dna = ProductDNA(workspace_id="ws_001")
        gene1 = PatternGene(
            id="gene_auth",
            name="Auth",
            category="auth",
            description="Auth",
            tech_stack=["python"],
            success_rate=0.95,
        )
        gene2 = PatternGene(
            id="gene_api",
            name="API",
            category="api",
            description="API",
            tech_stack=["fastapi"],
            success_rate=0.90,
        )
        dna.genes["gene_auth"] = gene1
        dna.genes["gene_api"] = gene2

        genome_a = ProductGenome(
            id="genome_a",
            project_id="proj_a",
            workspace_id="ws_001",
            name="Genome A",
            created_at=1714041600,
            genes=["gene_auth"],
            tech_stack=["python"],
            quality_score=0.9,
            synthesis_cost=0.45,
            synthesis_duration=300,
        )
        genome_b = ProductGenome(
            id="genome_b",
            project_id="proj_b",
            workspace_id="ws_001",
            name="Genome B",
            created_at=1714041600,
            genes=["gene_api"],
            tech_stack=["fastapi"],
            quality_score=0.85,
            synthesis_cost=0.40,
            synthesis_duration=280,
        )
        dna.genomes["genome_a"] = genome_a
        dna.genomes["genome_b"] = genome_b

        crossed = dna.crossbreed("genome_a", "genome_b")
        assert isinstance(crossed, list)


class TestComplementaryCategories:
    def test_fastapi_gets_complementary(self):
        dna = ProductDNA(workspace_id="ws_001")
        cats = dna._get_complementary_categories(["python", "fastapi"])
        assert "database" in cats
        assert "auth" in cats
        assert "testing" in cats

    def test_react_gets_complementary(self):
        dna = ProductDNA(workspace_id="ws_001")
        cats = dna._get_complementary_categories(["react", "next"])
        assert "api" in cats
        assert "testing" in cats

    def test_python_gets_all_complementary(self):
        dna = ProductDNA(workspace_id="ws_001")
        cats = dna._get_complementary_categories(["python"])
        assert "api" in cats
        assert "database" in cats
        assert "testing" in cats
        assert "deployment" in cats