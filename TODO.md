# ProdSynth — TODO List (BMAD v2.0)

_Статус: Active | Обновлено: 26.04.2026_

---

## ✅ Done (Завершено)

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
- [x] Реалізувати `apps/frontend/next.config.mjs` (Next.js config).
- [x] Реалізувати `apps/frontend/tailwind.config.ts`.
- [x] Створити `apps/frontend/src/app/layout.tsx` (JSON-LD, SEO, GitHub links).
- [x] Створити `apps/frontend/src/app/page.tsx` (Landing Page - hyper-detailed).
- [x] Створити `specs/openapi.yaml` (OpenAPI 3.1).
- [x] Реалізувати `apps/backend/Dockerfile`.
- [x] Реалізувати `apps/frontend/Dockerfile`.
- [x] Зробити коміт: "feat: Phase 0-1 infrastructure + Landing Page".
- [x] Створити UI компоненти: `button.tsx`, `card.tsx`, `input.tsx`, `badge.tsx`, `accordion.tsx`, `tabs.tsx`, `theme-provider.tsx`.
- [x] Створити `apps/frontend/src/app/dashboard/page.tsx` (Dashboard).
- [x] Створити `docs/api.md` (API Documentation).
- [x] Зробити коміт: "feat: Phase 2 - CodeAgent, TestAgent, Dashboard".

---

## 🏗️ Phase 3: Marketplace & Enterprise (Неделі 9–12) — НАЧИНАЕМ

### Marketplace & Billing
- [ ] Создать Marketplace API (CRUD для шаблонів).
- [ ] Реалізувати Stripe-біллінг (підписки, usage-based).
- [ ] Додати RBAC і SSO (SAML/OIDC) для Enterprise.
- [ ] Створити `docs/marketplace.md` (як створювати шаблони).
- [ ] Створити `packages/agents/deploy.py` (DeployAgent — Render/Fly.io API).

### Frontend (Full)
- [ ] Провести нагрузочне тестування (k6).
- [ ] Додати i18n (RU, EN, ZH-CN) у базові `next-intl`.
- [ ] Створити `src/app/marketplace/page.tsx` (Marketplace UI).

### NEW: Activation & Multi-tenancy
- [ ] **`WebhookNotifier`** (уведомлення в Slack/Telegram).
- [ ] **Multi-tenancy** (Schema-per-tenant у Neo4j, Data Residency для GDPR).
- [ ] **"Product DNA" система** (збереження "генетичного коду" продукту).
- [ ] **"First Product Challenge"** (місяць Pro бесплатно за деплой за 24 години).

### Documentation (Continuous)
- [ ] `docs/architecture.md` (C4 model: Context, Containers, Components).
- [ ] `docs/agents.md` (описання всіх агентів і їх ролей).
- [ ] `docs/security.md` (OWASP, секрети, аудит).
- [ ] **NEW:** `docs/licensing-and-ip.md` (IP, ліцензії, GPL-сумісність).
- [ ] **NEW:** `docs/cost-optimization.md` (економіка токенів).
- [ ] **NEW:** `docs/multi-tenancy.md` (ізоляція даних).
- [ ] **NEW:** `docs/activation-flow.md` (шлях користувача від реєстрації до "aha moment").

---

## ✅ Done (Заповнюється по ходу)

_(Пока пусто — починаємо Phase 3)_
