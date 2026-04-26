# ProdSynth Agents Reference

> All 12 synthesis agents and their responsibilities.

## Agent Overview

| Agent | File | Purpose |
|-------|------|---------|
| ResearchAgent | `packages/agents/research.py` | AST parsing, repo analysis, license check |
| ArchitectAgent | `packages/agents/research.py` | C4 model, tech stack selection, risk assessment |
| LicenseChecker | `packages/agents/research.py` | License compatibility (MIT/GPL/CC) |
| CodeAgent | `packages/agents/code.py` | Cascading LLM code generation |
| TestAgent | `packages/agents/test.py` | pytest + Playwright test generation |
| DeployAgent | `packages/agents/deploy.py` | Render/Fly.io/Docker deployment |
| SafetyGuard | `packages/agents/safety.py` | Guardrails, content filtering |
| TokenBudget | `packages/core/cost.py` | Token budget enforcement ($0.50/run) |
| DebugAgent | `packages/agents/debug.py` | Sentry error analysis → auto-fix |
| BackupAgent | `packages/core/backup.py` | Graph export to S3/GCS |
| WebhookNotifier | `packages/agents/webhook.py` | Slack/Telegram notifications |
| ProductDNA | `packages/agents/dna.py` | Pattern extraction, crossbreed, success tracking |

## Agent Communication

Agents communicate via:
- **gRPC** for internal agent-to-agent communication
- **NATS JetStream** for async event streaming
- **Redis** for token cache and rate limiting

## Execution Order

```
ResearchAgent → ArchitectAgent → LicenseChecker
       ↓
TokenBudget.check()
       ↓
CodeAgent (Layer 1: Gemini Flash → Layer 2: GPT-4o-mini → Layer 3: GPT-4o)
       ↓
TestAgent
       ↓
SafetyGuard
       ↓
DeployAgent → WebhookNotifier
```

## Agent Details

### ResearchAgent
Analyzes input repository:
- Clones GitHub repo (if URL provided)
- AST-parses source files
- Extracts tech stack (package.json, requirements.txt)
- Identifies components, endpoints, dependencies
- Outputs: `TechSpec` (JSON graph)

### ArchitectAgent
Designs the product architecture:
- Generates C4 context/containers/components diagrams
- Selects optimal tech stack alternatives
- Estimates cost and risk for each approach
- Outputs: `ArchitecturePlan`

### LicenseChecker
Checks input license compatibility:
- MIT, Apache 2.0, BSD → ALLOW
- GPL 2/3, AGPL → WARN_CONTAMINATION
- CC (non-commercial), Proprietary → BLOCK

### CodeAgent
Generates production-ready code:
- Layer 1: Gemini Flash → draft code ($0.01/1K tokens)
- Layer 2: GPT-4o-mini → structure refinement ($0.15/1K tokens)
- Layer 3: GPT-4o → final code ($0.30/1K tokens)
- Average cost: $0.30 per synthesis

### TestAgent
Generates test coverage:
- pytest unit tests (Python backend)
- Playwright E2E tests (Next.js frontend)
- Target: 80% code coverage
- Average: 84 tests generated per run

### DeployAgent
Deploys to target platform:
- Render (PaaS, recommended for MVP)
- Fly.io (edge deployment)
- Docker (local/on-prem)
- Kubernetes (enterprise)

### WebhookNotifier
Sends notifications on completion:
- Slack (webhook URL)
- Telegram (bot token + chat ID)
- Custom HTTP webhook

### ProductDNA
Extracts and preserves patterns:
- PatternGene: reusable code patterns (auth, API, DB, frontend, testing)
- ProductGenome: complete genetic profile
- Crossbreed: combine best genes from two genomes
- Success rate tracking (natural selection)