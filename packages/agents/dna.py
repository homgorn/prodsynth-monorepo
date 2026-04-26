"""
ProdSynth Product DNA — Genetic Code System (Phase 6)
Preserves and reuses patterns from previous syntheses.
Think of it as a "genetic library" of product patterns.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from datetime import datetime


class PatternGene(BaseModel):
    """A single gene — a reusable code pattern or architectural decision."""
    id: str
    name: str
    category: str  # auth, api, database, frontend, deployment, testing
    description: str
    tech_stack: List[str]
    code_snippet: Optional[str] = None  # SHA or reference, not full code
    created_at: int
    usage_count: int = 0
    success_rate: float = 1.0  # 0.0-1.0
    tags: List[str] = []
    parent_genes: List[str] = []  # inherited from
    metadata: Dict[str, Any] = {}


class ProductGenome(BaseModel):
    """The complete genetic profile of a synthesized product."""
    id: str
    project_id: str
    workspace_id: str
    name: str
    created_at: int
    genes: List[str]  # list of PatternGene IDs
    tech_stack: List[str]
    quality_score: float  # 0.0-1.0
    synthesis_cost: float
    synthesis_duration: int  # seconds
    parent_genomes: List[str] = []  # genomes that were mixed


class DNAResult(BaseModel):
    """Result of DNA analysis."""
    matched_genes: List[PatternGene]
    suggested_genes: List[PatternGene]
    crossbreed_recommendations: List[Dict[str, Any]]
    estimated_time_savings: float  # percentage
    estimated_cost_savings: float


class ProductDNA:
    """
    Product DNA system — genetic library of product patterns.
    
    Flow:
    1. After each synthesis, extract PatternGenes from the output
    2. Store genes in Neo4j graph
    3. When new synthesis starts, search for similar genes
    4. Suggest genes to CodeAgent for "natural selection"
    5. Genes with high success_rate get higher priority
    """

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.genes: Dict[str, PatternGene] = {}
        self.genomes: Dict[str, ProductGenome] = {}

    async def extract_genes(self, synthesis_result: Dict) -> List[PatternGene]:
        """
        Extract PatternGenes from synthesis output.
        Called after successful synthesis.
        """
        genes = []
        project_id = synthesis_result.get("project_id")
        tech_stack = synthesis_result.get("tech_stack", [])
        files = synthesis_result.get("files_generated", 0)

        # Extract auth patterns
        if "auth" in str(tech_stack).lower() or "jwt" in str(tech_stack).lower():
            genes.append(PatternGene(
                id=f"gene_auth_{project_id}",
                name="JWT Authentication Pattern",
                category="auth",
                description="JWT-based authentication with refresh tokens",
                tech_stack=["python", "fastapi"],
                usage_count=1,
                success_rate=0.95,
                tags=["auth", "jwt", "security"],
            ))

        # Extract API patterns
        if "api" in str(tech_stack).lower() or "fastapi" in str(tech_stack).lower():
            genes.append(PatternGene(
                id=f"gene_api_{project_id}",
                name="REST API CRUD Pattern",
                category="api",
                description="FastAPI with SQLAlchemy, Pydantic, async endpoints",
                tech_stack=["python", "fastapi", "sqlalchemy"],
                usage_count=1,
                success_rate=0.90,
                tags=["api", "rest", "crud"],
            ))

        # Extract database patterns
        if "postgres" in str(tech_stack).lower() or "database" in str(tech_stack).lower():
            genes.append(PatternGene(
                id=f"gene_db_{project_id}",
                name="PostgreSQL + SQLAlchemy Pattern",
                category="database",
                description="PostgreSQL with async SQLAlchemy, migrations, connection pooling",
                tech_stack=["python", "sqlalchemy", "postgresql"],
                usage_count=1,
                success_rate=0.92,
                tags=["database", "postgresql", "orm"],
            ))

        # Extract frontend patterns
        if "next" in str(tech_stack).lower() or "react" in str(tech_stack).lower():
            genes.append(PatternGene(
                id=f"gene_frontend_{project_id}",
                name="Next.js 14 App Router Pattern",
                category="frontend",
                description="Next.js 14 with App Router, Server Components, shadcn/ui",
                tech_stack=["typescript", "next", "react", "tailwind"],
                usage_count=1,
                success_rate=0.88,
                tags=["frontend", "next", "react"],
            ))

        # Extract testing patterns
        if synthesis_result.get("tests_generated", 0) > 0:
            genes.append(PatternGene(
                id=f"gene_test_{project_id}",
                name="pytest + Playwright Testing Pattern",
                category="testing",
                description=f"Generated {synthesis_result.get('tests_generated')} tests with {synthesis_result.get('coverage', 0)*100:.0f}% coverage",
                tech_stack=["python", "pytest", "playwright"],
                usage_count=1,
                success_rate=synthesis_result.get("coverage", 0.8),
                tags=["testing", "pytest", "e2e"],
            ))

        # Store genes
        for gene in genes:
            self.genes[gene.id] = gene

        return genes

    async def analyze_dna(self, tech_stack: List[str]) -> DNAResult:
        """
        Find matching genes for a new synthesis.
        Used to accelerate code generation.
        """
        matched = []
        suggested = []
        crossbreeds = []

        for gene in self.genes.values():
            # Check if tech stack overlaps
            overlap = set(gene.tech_stack) & set(tech_stack)
            if overlap:
                matched.append(gene)
            # Check if gene is complementary
            elif gene.category in self._get_complementary_categories(tech_stack):
                suggested.append(gene)

        # Crossbreed recommendations
        if len(matched) >= 2:
            crossbreeds.append({
                "type": "pattern_mix",
                "from": [g.id for g in matched[:2]],
                "recommendation": "Combine matched patterns for faster generation",
                "savings": len(matched) * 0.05,  # 5% savings per matched gene
            })

        total_savings = len(matched) * 0.10  # 10% per matched gene

        return DNAResult(
            matched_genes=matched,
            suggested_genes=suggested,
            crossbreed_recommendations=crossbreeds,
            estimated_time_savings=min(total_savings, 0.50),  # cap at 50%
            estimated_cost_savings=len(matched) * 0.05,  # $0.05 per gene
        )

    def _get_complementary_categories(self, tech_stack: List[str]) -> List[str]:
        """Get categories that complement the current tech stack."""
        categories = []
        stack_str = " ".join(tech_stack).lower()

        if "fastapi" in stack_str or "flask" in stack_str:
            categories.extend(["database", "auth", "testing"])
        if "react" in stack_str or "next" in stack_str:
            categories.extend(["api", "testing"])
        if "python" in stack_str:
            categories.extend(["api", "database", "testing", "deployment"])
        return categories

    async def update_gene_success(
        self,
        gene_id: str,
        success: bool,
        quality_score: float,
    ) -> None:
        """Update gene statistics after deployment."""
        gene = self.genes.get(gene_id)
        if not gene:
            return

        gene.usage_count += 1
        # Running average for success rate
        gene.success_rate = (
            (gene.success_rate * (gene.usage_count - 1) + (1.0 if success else 0.0))
            / gene.usage_count
        )
        if quality_score > 0:
            gene.metadata["avg_quality"] = (
                gene.metadata.get("avg_quality", gene.success_rate) * 0.7
                + quality_score * 0.3
            )

    async def crossbreed(
        self,
        genome_a: str,
        genome_b: str,
    ) -> List[str]:
        """
        "Crossbreed" two genomes to create a new product pattern.
        Takes best genes from both parents.
        """
        ga = self.genomes.get(genome_a)
        gb = self.genomes.get(genome_b)
        if not ga or not gb:
            return []

        # Combine genes, keeping highest success rate ones
        all_genes = {**{g.id: g for g in self.genes.values() if g.id in ga.genes},
                     **{g.id: g for g in self.genes.values() if g.id in gb.genes}}

        # Sort by success rate
        sorted_genes = sorted(all_genes.values(), key=lambda g: g.success_rate, reverse=True)

        # Take top genes (natural selection)
        best_genes = [g.id for g in sorted_genes[:10]]

        return best_genes

    async def get_top_genes(
        self,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> List[PatternGene]:
        """Get top-performing genes by category."""
        genes = list(self.genes.values())

        if category:
            genes = [g for g in genes if g.category == category]

        return sorted(genes, key=lambda g: (g.success_rate, g.usage_count), reverse=True)[:limit]


# Singleton per workspace
_dna_cache: Dict[str, ProductDNA] = {}


def get_product_dna(workspace_id: str) -> ProductDNA:
    """Get or create ProductDNA for a workspace."""
    if workspace_id not in _dna_cache:
        _dna_cache[workspace_id] = ProductDNA(workspace_id=workspace_id)
    return _dna_cache[workspace_id]