# ProdSynth Architecture (BMAD v2.0 — Phase 4)

> C4 Model: Context → Containers → Components → Code

---

## 1. System Context (Level 1)

```
┌──────────────────────────────────────────────────────────────┐
│                        ProdSynth Platform                      │
│              AI-Native Product Synthesis Engine               │
│                                                              │
│  ┌────────────┐    ┌────────────┐    ┌─────────────────────┐  │
│  │  Developer  │───▶│   Web UI   │    │     CLI Tool        │  │
│  │  (Human)   │    │ (Next.js)  │    │  (Node.js CLI)     │  │
│  └────────────┘    └─────┬──────┘    └─────────┬─────────┘  │
│                           │                     │             │
│                           ▼                     ▼             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Backend                     │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │              12 Synthesis Agents                 │  │  │
│  │  │  ResearchAgent → ArchitectAgent → CodeAgent     │  │  │
│  │  │  TestAgent → DeployAgent → SafetyGuard          │  │  │
│  │  │  TokenBudget → DebugAgent → BackupAgent          │  │  │
│  │  │  WebhookNotifier → ProductDNA                   │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
│                           │                                   │
│         ┌─────────────────┼─────────────────┐                 │
│         ▼                 ▼                 ▼                 │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐           │
│  │   Neo4j   │    │   Redis    │    │ PostgreSQL │           │
│  │ (Graphiti)│    │  (Cache)   │    │ (RLS/Auth) │           │
│  └────────────┘    └────────────┘    └────────────┘           │
│                                                              │
│  ┌────────────┐    ┌────────────┐    ┌─────────────────────┐  │
│  │   Slack/   │    │  Deploy    │    │  LLM Providers     │  │
│  │ Telegram   │    │  Targets   │    │ (OpenClaude/GPT)  │  │
│  └────────────┘    └────────────┘    └─────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**External Actors:**
- **Developer** — initiates synthesis, manages projects
- **LLM Providers** — OpenClaude, OpenAI, Anthropic, Google
- **Deploy Targets** — Render, Fly.io, Docker, Kubernetes
- **Payment Provider** — Stripe (subscriptions, billing)
- **Notification Services** — Slack, Telegram
- **SSO Providers** — Google Workspace, GitHub, Okta, Azure AD

---

## 2. Container Architecture (Level 2)

### Backend (`apps/backend/`)

```
FastAPI (Python 3.11+)
    │
    ├── REST API (Port 8000)
    │   ├── /api/v1/auth/*      → Auth, SSO, RBAC
    │   ├── /api/v1/projects/*  → CRUD, synthesis runs
    │   ├── /api/v1/synthesis/* → Run agents, streaming
    │   ├── /api/v1/marketplace/* → Templates, purchase
    │   ├── /api/v1/billing/*   → Plans, subscriptions
    │   └── /api/v1/workspaces/* → Multi-tenancy
    │
    ├── gRPC Services (Port 50051)
    │   └── agent.proto          → Internal agent communication
    │
    ├── Middleware
    │   ├── TenantMiddleware     → workspace_id enforcement
    │   ├── AuthMiddleware      → JWT validation
    │   ├── RateLimitMiddleware → Per-tenant rate limits
    │   └── LoggingMiddleware   → Structured logging (Loki)
    │
    ├── Agents (packages/agents/)
    │   ├── research.py         → Repository analysis
    │   ├── architect.py        → C4 model generation
    │   ├── code.py            → Code generation (cascading LLM)
    │   ├── test.py            → Test generation (pytest + Playwright)
    │   ├── deploy.py          → Target deployment
    │   ├── debug.py           → Error analysis → auto-fix
    │   ├── webhook.py         → Notification dispatcher
    │   └── safety.py          → Guardrails, content filtering
    │
    └── Core (packages/core/)
        ├── synthesis.py       → Orchestration engine
        ├── graph.py           → Graphiti integration
        └── cost.py           → Token budget management
```

### Frontend (`apps/frontend/`)

```
Next.js 14 (App Router)
    │
    ├── Landing Page (/)
    │   ├── Hero + Demo video
    │   ├── Feature sections (6 pillars)
    │   ├── Pricing table (3 tiers)
    │   ├── Testimonials carousel
    │   ├── FAQ accordion
    │   └── CTA + Footer
    │
    ├── Dashboard (/dashboard)
    │   ├── Project list with status
    │   ├── Create new project
    │   ├── Real-time synthesis progress
    │   └── Token usage meter
    │
    ├── Marketplace (/marketplace)
    │   ├── Template grid with filters
    │   ├── Search by tech stack
    │   ├── Favorites system
    │   └── Template detail → use template
    │
    └── Settings (/settings)
        ├── Team management
        ├── Billing portal
        └── SSO configuration
```

---

## 3. Component Details (Level 3)

### Synthesis Engine Flow

```
1. User submits repo URL or idea
   │
2. ResearchAgent
   ├── Clone repo (if GitHub URL)
   ├── AST parse: extract functions, imports, exports
   ├── Analyze tech stack (package.json, requirements.txt)
   ├── Check licenses (LicenseChecker)
   └── Output: TechSpec (JSON graph)
       │
3. ArchitectAgent
   ├── Generate C4 context diagram
   ├── Select tech stack alternatives
   ├── Estimate cost/risk
   └── Output: ArchitecturePlan
       │
4. [TokenBudget] Check budget ($0.50/limit)
   │
5. CodeAgent (cascading LLM)
   ├── Layer 1: Gemini Flash → draft code
   ├── Layer 2: GPT-4o-mini → structure/refine
   ├── Layer 3: GPT-4o → final code
   └── Output: Generated code files
       │
6. TestAgent
   ├── pytest unit tests (Python)
   ├── Playwright E2E tests (frontend)
   └── Coverage target: 80%
       │
7. SafetyGuard
   ├── Bandit scan (security)
   ├── License compatibility check
   └── Output: SafetyReport
       │
8. DeployAgent
   ├── Build Docker image
   ├── Push to registry
   └── Deploy to target (Render/Fly.io)
       │
9. WebhookNotifier
   └── Send Slack/Telegram notification
```

### Graphiti Memory Layer

```
Every synthesis run → adds to Neo4j graph:

(n:Node) ──[r:RELATES_TO]──▶ (n2:Node)
     │
     ├── type: "component" | "endpoint" | "function" | "test"
     ├── name: "UserService"
     ├── file_path: "src/services/user.py"
     ├── line: 42
     ├── tech_stack: ["python", "fastapi"]
     └── created_at: timestamp

Query patterns:
- "Show all endpoints in the project"
- "Find similar auth logic from other projects"
- "Trace dependencies of function X"
- "Get all tests for component Y"
```

### Multi-tenancy Data Model

```
┌─────────────────┐
��    Workspace    │  ← isolated tenant boundary
│ (workspace_id)  │
└───────┬─────────┘
        │
        ├── users (RLS by workspace_id)
        ├── projects (RLS by workspace_id)
        ├── graphs (RLS by workspace_id)
        └── audit_events (RLS by workspace_id)

Plan limits enforced at API layer:
├─ Free:  3 projects, 1GB storage, 1 user
├─ Pro:   unlimited projects, 100GB, 10 users
└─ Enterprise: unlimited + SSO + SLA + Custom schema
```

---

## 4. Technology Choices

| Layer | Technology | Justification |
|-------|-----------|---------------|
| **API** | FastAPI 0.109+ | Type safety, auto-docs, async, gRPC |
| **Agents** | Python + asyncio | Rich LLM ecosystem, gRPC support |
| **Memory** | Neo4j (Graphiti) | Graph queries, temporal reasoning |
| **Cache** | Redis | Token cache, rate limiting, pub/sub |
| **DB** | PostgreSQL 16 | RLS multi-tenancy, JSONB, full-text |
| **Frontend** | Next.js 14 | App Router, Server Components, SEO |
| **UI** | shadcn/ui + Tailwind | Accessible, customizable |
| **State** | Zustand | Lightweight, React-native compatible |
| **Auth** | JWT + OAuth2 | Stateless, SSO ready |
| **Queue** | NATS JetStream | Lightweight pub/sub, streaming |
| **Observability** | Loki + Grafana + Prometheus | Structured logs, metrics, dashboards |
| **LLM Routing** | Custom cascading | Cost optimization ($0.50/run) |

---

## 5. Deployment Topology

### Development
```
Local machine
├── docker-compose up -d (Neo4j, Redis, PG, Loki, Grafana)
├── pip install -r requirements.txt
├── npm install && npm run dev
└── http://localhost:3000
```

### Production (Render/Railway)
```
┌─────────────────────────────────────────┐
│          Load Balancer (Cloudflare)       │
│            https://prodsynth.com          │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
Frontend (Vercel)         Backend (Render)
- Next.js SSR              - FastAPI + gRPC
- Edge caching             - Auto-scaling
- CDN global               - $0 compute/idle
```

### Enterprise (Kubernetes)
```
┌────────────────────────────────────────────┐
│           EKS / GKE Cluster                 │
│  ┌──────────────────────────────────────┐  │
│  │         ingress-nginx (TLS)           │  │
│  └───────────────┬──────────────────────┘  │
│                  │                          │
│   ┌──────────────┼──────────────┐          │
│   ▼              ▼              ▼          │
│ API Pod     Frontend Pod    Worker Pod      │
│ (3 replicas) (3 replicas)  (NATS sub)      │
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │  Neo4j  │  │  Redis  │  │Postgres │    │
│  │ Cluster │  │ Cluster │  │ (RLS)   │    │
│  └─────────┘  └─────────┘  └─────────┘    │
│                                          │
│  ┌──────────────────────────────────────┐ │
│  │         Grafana + Loki + Prometheus   │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

---

## 6. API Contract

### Core Endpoints

```
POST   /api/v1/auth/login              → JWT token
POST   /api/v1/auth/sso/{provider}    → SSO redirect
GET    /api/v1/auth/sso/callback      → JWT after SSO

GET    /api/v1/projects               → List projects
POST   /api/v1/projects               → Create project
GET    /api/v1/projects/{id}          → Get project
DELETE /api/v1/projects/{id}          → Delete project

POST   /api/v1/synthesis/run          → Start synthesis
GET    /api/v1/synthesis/{run_id}     → Get run status
GET    /api/v1/synthesis/{run_id}/stream → SSE progress

GET    /api/v1/marketplace/templates  → List templates
GET    /api/v1/marketplace/templates/{id} → Template detail
POST   /api/v1/marketplace/purchase   → Purchase template

GET    /api/v1/billing/plans          → Available plans
POST   /api/v1/billing/subscribe      → Create subscription
GET    /api/v1/billing/usage          → Token/storage usage
POST   /api/v1/billing/webhook        → Stripe webhook

GET    /api/v1/team                  → List team members
POST   /api/v1/team/invite           → Invite member
PUT    /api/v1/team/{user_id}        → Update roles
DELETE /api/v1/team/{user_id}        → Remove member

GET    /api/v1/audit                 → Audit log
```

### Streaming (Server-Sent Events)

```
GET /api/v1/synthesis/{run_id}/stream
Events:
  {"agent": "ResearchAgent", "status": "running", "progress": 25}
  {"agent": "ArchitectAgent", "status": "running", "progress": 50}
  {"agent": "CodeAgent", "status": "running", "progress": 75}
  {"agent": "TestAgent", "status": "running", "progress": 90}
  {"agent": "DeployAgent", "status": "running", "progress": 100}
  {"status": "complete", "url": "https://my-app.onrender.com"}
```