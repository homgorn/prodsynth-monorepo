# ProdSynth Documentation

Welcome to the ProdSynth documentation! This directory contains detailed guides for all platform components.

## Quick Navigation

| Document | Description |
|----------|-------------|
| [Architecture](architecture.md) | C4 model: Context → Containers → Components → Code |
| [API Reference](api.md) | OpenAPI 3.1 spec with all endpoints |
| [Agents](agents.md) | All 12+ agents and their roles |
| [Security](security.md) | OWASP Top 10, GDPR, audit logging |
| [Multi-tenancy](multi-tenancy.md) | RLS, Neo4j workspace isolation, plan limits |
| [Activation Flow](activation-flow.md) | User journey from signup to "aha moment" |
| [Cost Optimization](cost-optimization.md) | Cascading LLM routing, token budgets |
| [Licensing & IP](licensing-and-ip.md) | GPL contamination, user ownership, DMCA |
| [Marketplace](marketplace.md) | Template structure, publishing, revenue |

## Getting Started

```bash
# Clone the repository
git clone https://github.com/homgorn/prodsynth-monorepo.git
cd prodsynth-monorepo

# Run with Docker Compose
docker-compose -f infra/docker/docker-compose.dev.yml up -d

# Or run individually
cd apps/backend && pip install -r requirements.txt && uvicorn main:app --reload
cd apps/frontend && npm install && npm run dev
```

## Architecture Overview

ProdSynth uses a 3-tier architecture:

```
User (CLI / Web UI)
    ↓
FastAPI Backend (12 agents)
    ↓
Graphiti (Neo4j) + Redis + PostgreSQL
```

See [architecture.md](architecture.md) for the full C4 model.

## Key Concepts

- **BMAD Methodology** — Business → Models → Actions → Delivery
- **Product DNA** — Genetic patterns preserved across syntheses
- **Cascading LLM** — Gemini Flash → GPT-4o-mini → GPT-4o for cost optimization
- **Graphiti Memory** — Persistent graph memory with temporal reasoning

## Support

- Issues: https://github.com/homgorn/prodsynth-monorepo/issues
- Email: support@prodsynth.com