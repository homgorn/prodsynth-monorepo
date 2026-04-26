# ProdSynth — TODO List (BMAD v2.0)

_Статус: Active | Обновлено: 26.04.2026_

---

## ✅ Done (Повний список)

### Phase 0: Infrastructure & Core (Completed 26.04.2026)
- [x] Создати монорепо `prodsynth-monorepo` (TurboRepo).
- [x] Создати структуру директорій: `apps/`, `packages/`, `docs/`, `specs/`, `infra/`.
- [x] Настроїти `docker-compose.yml` (Neo4j, Redis, NATS, PostgreSQL, Loki, Grafana).
- [x] Реалізувати `apps/backend/main.py` (FastAPI + gRPC).
- [x] Реалізувати `apps/backend/requirements.txt`.
- [x] Реалізувати `apps/frontend/package.json` (Next.js).
- [x] Реалізувати `apps/cli/package.json` (Node.js CLI).
- [x] Настроїти `.github/workflows/ci.yml` (CI/CD).
- [x] Ініціалізувати Git і зробити перший коміт.
- [x] Створити `CHAT_ARCHITECTURE.md` (BMAD v2.0 + Self-critique).
- [x] Створити `CONTEXT_MAP.md` (Visual connections).
- [x] Створити `README.md` (Project overview).
- [x] Створити `turbo.json` (Monorepo config).
- [x] Створити `.gitignore`.

### Phase 1: Synthesis Engine (Completed 26.04.2026)
- [x] Створити `packages/core/synthesis.py` (Engine).
- [x] Створити `packages/agents/research.py` (ResearchAgent + LicenseChecker).
- [x] Створити `packages/graph/adapter.py` (GraphitiAdapter).
- [x] Настроїти AST-парсинг репозиторіїв.
- [x] Настроїти Graphiti-адаптер для збереження графів.
- [x] Написати 50+ unit-тестів для `packages/core/synthesis`.
- [x] **NEW:** `LicenseChecker` агент (перевірка ліцензій).
- [x] **NEW:** `TokenBudget` механізм (ліміт $0.50/запуск).

### Phase 2: Product Assembly (Completed 26.04.2026)
- [x] Створити `packages/agents/code.py` (CodeAgent з cascading LLM).
- [x] Створити `packages/agents/test.py` (TestAgent з pytest/Playwright).
- [x] Створити `packages/agents/deploy.py` (DeployAgent).
- [x] Реалізувати `apps/frontend/next.config.mjs` (Next.js config).
- [x] Реалізувати `apps/frontend/tailwind.config.ts`.
- [x] Створити `apps/frontend/src/app/layout.tsx` (JSON-LD, SEO, GitHub links).
- [x] Створити `apps/frontend/src/app/page.tsx` (Landing Page - hyper-detailed).
- [x] Створити `specs/openapi.yaml` (OpenAPI 3.1).
- [x] Реалізувати `apps/backend/Dockerfile`.
- [x] Реалізувати `apps/frontend/Dockerfile`.
- [x] Створити UI компоненти: button, card, input, badge, accordion, tabs, theme-provider.
- [x] Створити `apps/frontend/src/app/dashboard/page.tsx` (Dashboard).
- [x] Створити `docs/api.md` (API Documentation).
- [x] Створити `docs/agents.md` (All 12 agents described).

### Phase 3: Marketplace & Enterprise (Completed 26.04.2026)
- [x] Створити Marketplace API endpoints (`apps/backend/routes/marketplace.py`).
- [x] Marketplace UI: search, category tabs, template cards, favorites (`apps/frontend/src/app/marketplace/page.tsx`).
- [x] Stripe Billing: plans (Free/Pro $49/Enterprise $999), subscriptions, webhooks (`apps/backend/routes/billing.py`).
- [x] RBAC & SSO: owner/admin/editor/viewer/billing_admin roles, Google/GitHub/Okta/Azure SSO (`apps/backend/routes/rbac.py`).
- [x] WebhookNotifier: Slack, Telegram, custom URLs (`packages/agents/webhook.py`).
- [x] Multi-tenancy models: Workspace, Tenant, plan-based limits (`packages/models/workspace.py`, `packages/models/tenant.py`).
- [x] TenantMiddleware: workspace isolation via X-Workspace-ID header (`apps/backend/middleware/tenant.py`).
- [x] AuditEvent model: full action taxonomy (auth, project, billing, team, sso) (`packages/models/audit.py`).
- [x] Push to GitHub: https://github.com/homgorn/prodsynth-monorepo.

---

### Phase 4: Polish & Launch (Completed 26.04.2026)
- [x] k6 load test config: 10→50→100→200 RPS stages (`tests/load/api-load-test.js`).
- [x] i18n setup: EN/RU/ZH-CN with locale detection middleware (`apps/frontend/src/i18n/`).
- [x] `docs/architecture.md` (C4 model: Context, Containers, Components, APIs).
- [x] `docs/security.md` (OWASP Top 10, GDPR, audit logging, incident response).
- [x] `docs/multi-tenancy.md` (RLS, Neo4j isolation, plan limits, GDPR).
- [x] `docs/activation-flow.md` (signup → dashboard → synthesis → deploy → upgrade funnel).
- [x] `docs/cost-optimization.md` (cascading LLM, token budgets, Graphiti cache, ROI).
- [x] `docs/licensing-and-ip.md` (LicenseChecker, GPL contamination, user ownership, DMCA).
- [x] `docs/marketplace.md` (template structure, publishing, search, revenue 70/30 split).
- [x] Push to GitHub: 19 commits total.
