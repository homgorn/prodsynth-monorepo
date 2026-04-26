# ProdSynth Cost Optimization (BMAD v2.0 — Phase 4)

## Token Budget Architecture

Every synthesis run has a budget. When exhausted, synthesis pauses — not the user.

```
$0.50 per run (Free/Pro)    $1.00 per run (Enterprise)
         │                            │
         ▼                            ▼
┌────────────────────────────────────────────────────────┐
│                  TokenBudget Agent                     │
│                                                         │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐     │
│  │ Gemini    │   │ GPT-4o    │   │ Claude     │     │
│  │ Flash    │   │ mini       │   │ Sonnet     │     │
│  │ $0.05   │   │ $0.15     │   │ $0.30    │     │
│  └────────────┘   └────────────┘   └────────────┘     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Cascading LLM Strategy               │  │
│  │                                                   │  │
│  │  1. DeepSeek/Gemini Flash → Draft (fast, cheap)  │  │
│  │  2. GPT-4o-mini/Claude Haiku → Refine          │  │
│  │  3. GPT-4o/Claude Sonnet → Finalize            │  │
│  │                                                   │  │
│  │  Average: $0.50 per complete synthesis           │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## LLM Provider Routing

### Tier 1: Cheap & Fast (Drafts, Research)
| Provider | Model | Cost/1K tokens | Use Case |
|----------|-------|---------------|----------|
| Google | Gemini Flash 2.0 | $0.01 | Initial code drafts, file structure |
| DeepSeek | DeepSeek V2 | $0.05 | Code drafts, test generation |
| Mistral | Mistral Small | $0.04 | Simple refactoring |

### Tier 2: Medium (Refinement)
| Provider | Model | Cost/1K tokens | Use Case |
|----------|-------|---------------|----------|
| OpenAI | GPT-4o-mini | $0.15 | Code refinement, complexity analysis |
| Anthropic | Claude Haiku | $0.10 | Architecture review, test improvement |
| Google | Gemini Pro | $0.15 | Multi-file coherence |

### Tier 3: Expensive (Finalization)
| Provider | Model | Cost/1K tokens | Use Case |
|----------|-------|---------------|----------|
| OpenAI | GPT-4o | $0.30 | Final code generation, safety checks |
| Anthropic | Claude Sonnet | $0.30 | Complex logic, architecture decisions |
| OpenAI | o3-mini | $0.20 | Reasoning-heavy tasks |

---

## Cascading Strategy by Agent

### ResearchAgent
```
1. Gemini Flash ($0.01/1K) → Parse repo structure, extract imports
2. DeepSeek ($0.05/1K) → Analyze dependencies, identify patterns
3. GPT-4o-mini ($0.15/1K) → Generate TechSpec (JSON)

Total ResearchAgent: ~$0.08 per run
```

### ArchitectAgent
```
1. Gemini Flash ($0.01/1K) → List C4 components
2. GPT-4o-mini ($0.15/1K) → Generate C4 diagrams (Mermaid)

Total ArchitectAgent: ~$0.06 per run
```

### CodeAgent (Biggest Spender)
```
Layer 1: Gemini Flash ($0.01/1K) → Generate 5 alternative drafts
  ↓
Layer 2: GPT-4o-mini ($0.15/1K) → Select best draft, expand to full files
  ↓
Layer 3: GPT-4o ($0.30/1K) → Finalize critical files (auth, payments, core logic)

Total CodeAgent: ~$0.30 per run
```

### TestAgent
```
1. GPT-4o-mini ($0.15/1K) → Generate pytest unit tests
2. Claude Haiku ($0.10/1K) → Generate Playwright E2E tests

Total TestAgent: ~$0.05 per run
```

---

## Graphiti Cache Strategy

### Cache Hit = No Tokens

When a graph is already built for a similar repo pattern:

```
Repo: "expressjs/rest-api-starter" (cached: 2026-04-20)
  → Graph: 847 nodes, 234 edges
  → "Express.js REST API" pattern recognized

New Repo: "expressjs/todo-app"
  ↓
ResearchAgent checks graph cache first
  ↓
"Found similar pattern in 0.3 seconds"
  ↓
Only new/changed files → token budget used: $0.02
  vs. full analysis → would cost: $0.08

Savings: 75%
```

### Cache Invalidation
- Pattern TTL: 7 days
- Major version bump (e.g., Express 4→5): invalidate
- Security vulnerability detected: invalidate relevant patterns

---

## Cost Monitoring & Alerts

### Per-User Budget
```python
# Enforce daily/monthly limits at middleware level
async def check_token_budget(user_id: str) -> bool:
    today = get_today_usage(user_id)
    monthly = get_monthly_usage(user_id)

    if today > 5.00:  # Daily cap
        raise HTTPException(429, "Daily token budget exceeded. Try again tomorrow.")

    if monthly > 20.00:  # Monthly cap (Free tier)
        raise HTTPException(402, "Monthly budget exhausted. Upgrade to Pro.")

    return True
```

### Alerts
| Threshold | Action |
|-----------|--------|
| 70% daily budget used | In-app banner: "You're using your daily budget quickly" |
| 90% daily budget | Email: "Upgrade to Pro for $0.50/run" |
| Budget exceeded | Slack notification to ops team (aggregated) |
| > 10 users hitting limit | Alert: potential abuse or pricing issue |

### Cost Attribution
```python
# Every synthesis run tagged with cost center
{
    "run_id": "run_123",
    "workspace_id": "ws_456",
    "user_id": "user_789",
    "llm_costs": {
        "research": 0.08,
        "architect": 0.06,
        "code": 0.30,
        "test": 0.05,
        "deploy": 0.00,
    },
    "total": 0.49,
    "cached_tokens": 2340,  # from graphiti cache
    "cache_savings": 0.12,
    "actual_cost": 0.37,
}
```

---

## Infrastructure Cost Optimization

### Compute
| Component | Strategy | Savings |
|-----------|----------|---------|
| Backend API | Render hobby → auto-scale Pro | Pay per request |
| Frontend | Vercel (free tier) → Edge | Global CDN |
| Workers | NATS + stateless | Scale to 0 when idle |
| Database | Neon PostgreSQL (serverless) | Per-query billing |

### Storage
| Type | Strategy | Savings |
|------|----------|--------|
| User code | S3/R2 → auto-delete after 30 days (Free) | 80% storage cost |
| Graphs | Neo4j Aura (Free tier) | $0 for < 1GB |
| Logs | Loki (self-hosted) | vs. Datadog: 90% cheaper |
| Backups | S3 Intelligent Tiering | 60% cheaper than Standard |

### Networking
| Strategy | Savings |
|----------|--------|
| Cloudflare caching (static assets) | 70% bandwidth cost |
| gRPC for internal agent communication | 40% less traffic vs HTTP |
| Compression (brotli) | 30% smaller responses |

---

## ROI Model

```
Revenue per Pro user:     $49/month
Avg LLM cost per user:    $3/month  (50 runs × $0.06)
Infrastructure cost:       $1/month
Gross margin:            $45/month (92%)

Break-even: 1 user covers 1.09 Pro subscriptions
LTV at 12 months:       $588 - $48 = $540
```

### Cost per Feature
| Feature | Token Cost | Infra Cost | Total |
|---------|-----------|-----------|-------|
| Basic synthesis | $0.49 | $0.01 | $0.50 |
| + E2E tests | $0.05 | $0.02 | $0.07 |
| + Deploy | $0.00 | $0.10 | $0.10 |
| + Team (5 users) | $0.00 | $0.05 | $0.05 |
| **Total per run** | **$0.54** | **$0.18** | **$0.72** |