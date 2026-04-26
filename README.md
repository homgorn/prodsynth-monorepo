# 🚀 ProdSynth — AI-Native Product Synthesis Engine

[![Build Status](https://img.shields.io/github/actions/workflows/ci.yml/homgorn/prodsynth-monorepo/main?label=build)](https://github.com/homgorn/prodsynth-monorepo/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Twitter Follow](https://img.shields.io/twitter/follow/prodsynth?label=Follow&style=flat)](https://twitter.com/prodsynth)

**ProdSynth** (Product Synthesis Engine) — платформа для автоматического создания рабочих продуктов из репозиториев. От идеи до деплоя за 5 минут.

---

## 📐 BMAD Summary (Кратко)

| Компонент | Описание |
|------------|-----------|
| **B**usiness | SaaS-платформа: Free ($0), Pro ($49/мес), Enterprise ($999+/мес). 1000+ регистраций за 3 месяца. |
| **M**odels | Tech Stack: Python/FastAPI, Next.js, Neo4j (Graphiti), Redis, NATS. gRPC для агентов. |
| **A**ctions | Phase 0–3: Инфраструктура → Синтез → Сборка → Marketplace. 12 недель до MVP. |
| **D**elivery | SEO-лэндинг (Next.js), Docs (Markdown), CI/CD (GitHub Actions), Monitoring (Grafana+Loki). |

**10x Feature:** **Product DNA** — система "генетического кода" продукта. Скрещивайте лучшие практики, сохраняйте историю решений.

---

## 📐 Phase 3: Marketplace & Enterprise

### Marketplace (`/marketplace`)
- Template grid with search, category tabs (SaaS, API, Dashboard, Favorites)
- 5 mock templates: SaaS Starter, API Service, Dashboard & Analytics, E-commerce, Data Pipeline
- Preview, download, ratings, favorites

### Billing (`/api/v1/billing`)
- **Plans:** Free ($0), Pro ($49/mo, $470/yr), Enterprise ($999/mo, $9990/yr)
- Subscription lifecycle: create, update, cancel
- Stripe webhooks for payment events
- Usage tracking: tokens, graph storage, API calls

### RBAC & SSO (`/api/v1/auth`)
- **Roles:** owner, admin, editor, viewer, billing_admin
- **SSO Providers:** Google Workspace, GitHub OAuth2, Okta SAML, Azure AD OIDC
- Team management: invite, role change, remove
- Audit log with full action taxonomy

### Multi-tenancy (`/api/v1/workspaces`)
- **Workspace isolation:** PostgreSQL RLS + workspace_id on all tables
- **TenantMiddleware:** X-Workspace-ID header enforcement
- **Plan-based limits:** projects, team members, storage, token budget
- Workspace settings: SSO enforcement, email domains, audit retention

### Enterprise Extras
- WebhookNotifier: Slack, Telegram, custom URLs
- AuditEvent model: auth, project, billing, team, sso, workspace actions
- SAML metadata endpoint, SSO callback with JWT

---

## 🚀 Quick Start (5 минут до продукта)

### 1. Install CLI
```bash
npm install -g @prodsynth/cli
# or
pip install prodsynth-cli
```

### 2. Login
```bash
prodsynth login
```

### 3. Generate Product
```bash
# From existing repo
prodsynth generate --from github.com/user/repo --template saas

# From idea
prodsynth generate --idea "AI-powered task manager" --target docker
```

### 4. Watch Progress
```bash
[Research Agent] Analyzing repo... ✅
[Architect Agent] Designing C4 model... ✅
[Code Agent] Generating Python/FastAPI code... ✅
[Test Agent] Running pytest + playwright... ✅
[Deploy Agent] Deploying to Render... ✅

✨ Product ready at: https://my-product.onrender.com
```

---

## 📂 Project Structure

```
prodsynth-monorepo/
├── apps/
│   ├── backend/     # FastAPI + gRPC (Python)
│   ├── frontend/    # Next.js Landing + Dashboard
│   └── cli/         # Node.js CLI package
├── packages/
│   ├── core/        # Synthesis engine (Python)
│   ├── agents/      # Research, Architect, Code, Test, Deploy
│   ├── graph/       # Graphiti adapter (Neo4j/Kuzu)
│   └── ui/          # Shared shadcn/ui components
├── docs/            # Architecture, API, Agents, Security docs
├── specs/           # OpenAPI 3.1, Protobuf specs
├── infra/           # Docker, K8s, Terraform
└── .github/         # CI/CD workflows
```

---

## 📚 Documentation

| Document | Description |
|-----------|-------------|
| [Architecture](CHAT_ARCHITECTURE.md) | Full BMAD v2.0, self-critique, improved plan |
| [Context Map](CONTEXT_MAP.md) | Visual connections between all components |
| [TODO List](TODO.md) | Phase-by-phase task list (12 weeks) |
| [API Spec](specs/openapi.yaml) | OpenAPI 3.1 specification |
| [Agents](docs/agents.md) | All 12+ agents and their roles (placeholder — see [CHAT_ARCHITECTURE.md](CHAT_ARCHITECTURE.md) for full agent list) |

---

## 🧠 Core Agents (Сердце системы)

1. **ResearchAgent** — AST-парсинг, анализ репозитория, формирование ТЗ.
2. **ArchitectAgent** — C4-модель, выбор tech stack, оценка рисков.
3. **LicenseChecker** — Проверка лицензий (GPL? MIT?), генерация совместимого кода.
4. **CodeAgent** — Генерация кода через OpenClaude API (cascading LLM).
5. **TestAgent** — Автогенерация pytest + playwright тестов.
6. **DeployAgent** — Деплой на Render/Fly.io/Docker.
7. **SafetyGuard** — Guardrails для агентов (стоп-слова, лимиты).
8. **TokenBudget** — Экономика токенов ($0.50/запуск).
9. **DebugAgent** — Анализ Sentry-ошибок → автофикс.
10. **BackupAgent** — Экспорт графов в S3/GCS.
11. **WebhookNotifier** — Slack/Telegram уведомления.
12. **ProductDNA** — Сохранение "генетического кода" продукта.

---

## 💰 Cost Optimization (Экономика токенов)

**Cascading LLM Usage:**
- **Layer 1 (Cheap):** Gemini Flash, DeepSeek — черновики ($0.05).
- **Layer 2 (Medium):** GPT-4o-mini, Claude Haiku — структура ($0.15).
- **Layer 3 (Expensive):** GPT-4o, Claude Sonnet — финализация ($0.30).
- **Total:** ~$0.50/synthesis (в рамках бюджета Pro-тарифа).

**Graphiti Cache:** Повторные запросы не тратят токены, если граф уже построен.

---

## 🔒 Security & Legal

- **License Compatibility Checker** — автоматическая проверка входных репозиториев.
- **IP Protection** — код принадлежит пользователю, графы анонимизированы.
- **SAFE Code Generation** — встроенный Bandit/Snyk в пайплайн.
- **OWASP Top 10** — защита от XSS, SQL injection, CSRF.
- **GDPR Compliance** — Multi-tenancy (Schema-per-tenant), Data Residency.

---

## 🌐 Deployment Targets

| Target | Setup Time | Best For |
|--------|------------|----------|
| **Docker** | 1 min | Local development, on-prem |
| **Render** | 2 min | Quick SaaS, prototypes |
| **Fly.io** | 2 min | Global edge, low latency |
| **Kubernetes** | 5 min | Enterprise, scale |
| **Vercel** | 1 min | Frontend-only apps |

---

## 📊 KPIs (Через 3 месяца)

- [ ] 1000+ регистраций (Free).
- [ ] 50+ шаблонов в Marketplace.
- [ ] Churn rate < 5%.
- [ ] Lighthouse Score > 95.
- [ ] Unit test coverage > 80%.

---

## 🤝 Contributing

```bash
git clone https://github.com/homgorn/prodsynth-monorepo.git
cd monorepo
npm install # or bun install
docker-compose up -d # Neo4j, Redis, NATS, Loki
npm run dev
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

_ProdSynth: Turn any repo into a product in 5 minutes._