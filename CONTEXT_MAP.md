# ProdSynth — Context Map (Связи и Потоки данных)

_Версия: 2.0 (Self-critique applied) | Дата: 26.04.2026_

---

## 1. 🗺️ High-Level Context Map (Кто с кем говорит)

```
                          ┌─────────────────────────────────────────────────────────┐
                          │                   USER / CLIENT                        │
                          │  (Browser, Mobile App, CLI `prodsynth`)        │
                          └──────────────────────┬───────────────────────┘
                                         │ HTTPS / gRPC
                          ┌──────────────────────▼───────────────────────┐
                          │              PRODSYNTH CORE (FastAPI)              │
                          │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
                          │  │ Research │  │Architect │  │  Code    │ │
                          │  │ Agent    │  │ Agent    │  │ Agent    │ │
                          │  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
                          │       │              │              │          │
                          │  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐ │
                          │  │  Test    │  │  Deploy  │  │  Debug   │ │
                          │  │  Agent   │  │  Agent   │  │  Agent   │ │
                          │  └──────────┘  └──────────┘  └──────────┘ │
                          └──────────────────────┬───────────────────────┘
                     ┌───────┘              │              └───────┐
                     │                      │                      │
            ┌────────▼────────┐  ┌────────▼────────┐  ┌────────▼────────┐
            │   OPENCLAUDE    │  │    GRAPHITI      │  │  CLI-ANYTHING  │
            │ (Engine/Local)  │  │ (Neo4j/Kuzu)   │  │ (Adapters)      │
            └────────────────┘  └────────────────┘  └────────────────┘
                     │                      │                      │
                     └──────────┬───────────────┬──────────────┘
                                │               │
                        ┌───────▼───────┐   │
                        │  PRODUCT DNA  │   │
                        │ (Graph of     │   │
                        │  decisions)  │   │
                        └───────┬───────┘   │
                                │               │
            ┌───────────────────────▼───┐   │
            │     TOKEN BUDGET        │   │
            │ (Cost Control: $0.50)  │   │
            └───────────────────────┬───┘   │
                                    │               │
            ┌───────────────────────▼───┐
            │     LICENSE CHECKER     │
            │ (IP, GPL, MIT check) │
            └──────────────────────────┘

```

---

## 2. 💰 Data Flow (Поток данных при генерации)

```
[User: `prodsynth generate my-repo`]
    │
    ▼
[1. Research Agent] ──▶ [AST Parser] ──▶ [Graphiti: Create Graph]
    │                                        │
    │ (repo_url, tech_stack, risks)              │ (nodes: files, functions, deps)
    ▼                                        ▼
[2. Architect Agent] ◀────────────────── [Graphiti: Query Graph]
    │                                        │
    │ (C4 model, tech stack choice)             │ (context-aware decisions)
    ▼                                        ▼
[3. Code Agent] ──▶ [OpenClaude API] ──▶ [Generated Code]
    │                                        │
    │ (files: .py, .ts, Dockerfile)            │ (Product DNA: why this code?)
    ▼                                        ▼
[4. Test Agent] ──▶ [pytest/Playwright] ──▶ [Test Results]
    │                                        │
    │ (unit + e2e pass?)                       │ (auto-fix via DebugAgent)
    ▼                                        ▼
[5. Deploy Agent] ──▶ [Render/Fly API] ──▶ [Live URL]
    │
    ▼
[WebhookNotifier] ──▶ [User: Slack/Telegram "Product ready!"]
```

---

## 3. 🔐 Security & Safety Context (Новое из самокритики)

```
┌─────────────────────────────────────────────────────────────┐
│                   SAFETY LAYER                       │
│                                                     │
│  [LicenseChecker]                                   │
│    │                                              │
│    ├─▶ Checks input repo licenses (GPL? MIT?)        │
│    └─▶ Generates compatible output code             │
│                                                     │
│  [SafetyGuard]                                      │
│    │                                              │
│    ├─▶ Stop-words filter (no dangerous commands)    │
│    ├─▶ Recursion depth limit (prevent loops)        │
│    └─▶ Human-in-the-loop (Enterprise approval)      │
│                                                     │
│  [TokenBudget]                                     │
│    │                                              │
│    ├─▶ $0.50 limit per synthesize run             │
│    ├─▶ Cascade: Cheap models → Expensive models   │
│    └─▶ Graphiti as cache (reuse previous results)   │
│                                                     │
│  [BackupAgent]                                     │
│    │                                              │
│    └─▶ Daily export to S3/GCS (JSON format)       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 4. 🏗️ Multi-tenancy Context (Изоляция данных)

```
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│   TENANT A       │  │   TENANT B       │  │   TENANT C       │
│                   │  │                   │  │                   │
│  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │
│  │ Graphiti   │  │  │  │ Graphiti   │  │  │  │ Graphiti   │  │
│  │ (namespace │  │  │  │ (namespace │  │  │  │ (namespace │  │
│  │  a_123)   │  │  │  │  b_456)   │  │  │  │  c_789)   │  │
│  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │
│                   │  │                   │  │                   │
│  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │
│  │ PostgreSQL │  │  │  │ PostgreSQL │  │  │  │ PostgreSQL │  │
│  │ (user_a)  │  │  │  │ (user_b)  │  │  │  │ (user_c)  │  │
│  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │
└───────────────────┘  └───────────────────┘  └───────────────────┘
          │                       │                       │
          └───────────┬───────────┬───────────┘
                      │           │
              ┌───────▼───┐   │
              │  RBAC      │   │
              │  (SSO,     │   │
              │  SAML/OIDC)│   │
              └───────┬───┘   │
                      │           │
              ┌───────▼───┐
              │  Core API  │
              │  (Shared)  │
              └────────────┘
```

---

## 5. 🚀 Activation Flow (Путь пользователя / "Aha Moment")

```
[1. Landing Page] ──▶ [2. Sign Up (Free)]
    │                          │
    │                          ▼
    │                  [3. "5-min Magic Demo"]
    │                          │ (paste repo URL)
    │                          ▼
    │                  [4. See Architecture]
    │                          │ (interactive graph view)
    │                          ▼
    │                  [5. Click "Generate"]
    │                          │ (token budget: $0.50)
    │                          ▼
    │                  [6. Watch Progress]
    │                          │ (Research → Architect → Code)
    │                          ▼
    │                  [7. Deployed URL]
    │                          │ (live SaaS in 5 min)
    │                          ▼
    │                  [8. "Aha Moment!"]
    │                          │
    ▼                          ▼
[9. Upgrade to Pro] ◀───────┘
    │
    ▼
[10. Invite Team] ──▶ [11. Marketplace] ──▶ [12. Custom Agents]
```

---

## 6. 📊 Storage Context (Где что лежит)

| Component           | Storage            | Purpose                        | Retention  |
|---------------------|--------------------|--------------------------------|------------|
| **Graphiti**         | Neo4j               | Product DNA, decisions, graph      | Permanent |
| **Metadata**         | PostgreSQL         | User accounts, project settings    | Permanent |
| **Cache**            | Redis              | Session data, token budgets       | 24 hours  |
| **Message Queue**    | NATS Streams       | Agent task queue                 | Until ack   |
| **Backups**          | S3 / GCS           | Daily graph exports (JSON)        | 30 days   |
| **Logs**             | Grafana Loki       | Application logs, errors          | 7 days    |
| **Traces**           | Tempo              | OpenTelemetry traces             | 7 days    |
| **Metrics**          | Prometheus         | Performance metrics               | 30 days   |
| **Errors**           | Sentry             | Exception tracking                | 90 days   |

---

## 7. 💸 Cost Optimization Context (Экономика токенов)

```
[Request: Synthesize]
    │
    ├─▶ [Graphiti: Check Cache]
    │       │
    │       ├─▶ HIT  ──▶ Return cached result (Cost: $0.00)  ✅
    │       │
    │       └─▶ MISS ──▶ Continue
    │
    ▼
[TokenBudget: $0.50 available]
    │
    ▼
[Start Cascade]
    │
    ├─▶ [Layer 1: Cheap Model] (Gemini Flash, DeepSeek)
    │       │ (analyze repo, basic structure)
    │       │ Cost: ~$0.05
    │       ▼
    │   [Graphiti: Save intermediate results]
    │
    ├─▶ [Layer 2: Medium Model] (GPT-4o-mini, Claude Haiku)
    │       │ (architect decisions, code skeleton)
    │       │ Cost: ~$0.15
    │       ▼
    │   [Graphiti: Save decisions]
    │
    └─▶ [Layer 3: Expensive Model] (GPT-4o, Claude Sonnet)
            │ (final code, complex logic)
            │ Cost: ~$0.30
            ▼
        [Total: ~$0.50] ✅ Within budget
```

---

## 8. 🔗 Integration Points (Связи с нашими репозиториями)

| Our Repo               | Role in ProdSynth           | Integration Method           |
|------------------------|----------------------------|-----------------------------|
| **openclaude**          | Core engine / executor      | Submodule: `packages/core/engine` |
| **graphiti**            | Memory layer / graph store  | Adapter: `packages/graph/`     |
| **CLI-Anything**        | Universal adapter for tools | Plugin: `packages/adapters/`   |
| **smux**               | Terminal automation        | CLI tool: `infra/smux/`       |
| **FinRobot**            | Finance-specific agents    | Templates: `marketplace/finance/` |
| **rust-hft**            | Low-latency simulations    | Rust module: `packages/sim/`    |
| **MiroFish**            | Social simulation         | Agent: `packages/agents/social/` |

---

_Конец Context Map v2.0_