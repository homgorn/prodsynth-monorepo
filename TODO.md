# ProdSynth — TODO List (BMAD v2.0)

_Статус: Active | Обновлено: 26.04.2026_

---

## 🏗️ Phase 0: Infrastructure & Core (Недели 0–1)

### Repository & Structure
- [ ] Создать монорепо `prodsynth-monorepo` (TurboRepo).
- [ ] Создать структуру директорий: `apps/`, `packages/`, `docs/`, `specs/`, `infra/`.

### Docker & Local Environment
- [ ] Настроить `docker-compose.yml` (Neo4j, Redis, NATS, PostgreSQL, Loki, Grafana).
- [ ] Создать `infra/docker/` с Dockerfile для backend/frontend/cli.

### Core Engine
- [ ] Интегрировать `openclaude` как подмодуль `packages/core/engine`.
- [ ] Настроить Graphiti-адаптер для сохранения графов (`packages/graph/`).
- [ ] Реализовать `prodsynth-cli` (npm пакет) с командами: `init`, `analyze`, `generate`.

### CI/CD
- [ ] Настроить GitHub Actions: линтеры, тесты, сборка Docker-образов.
- [ ] Добавить Dependabot для обновления зависимостей.

---

## 🧠 Phase 1: Synthesis Engine (Недели 2–4)

### Parsing & Analysis
- [ ] Реализовать AST-парсер репозиториев (Python/TS/Go).
- [ ] Настроить Graphiti-адаптер для сохранения графов.
- [ ] Написать 50+ unit-тестов для `packages/core/synthesis`.

### Agents (Base)
- [ ] Создать агента `ResearchAgent` (поиск в репозитории + формирование ТЗ).
- [ ] Создать агента `ArchitectAgent` (генерация C4-моделей и выбор tech stack).

### NEW: Critical Additions (Self-Critique)
- [ ] **`LicenseChecker` агент** (проверка лицензий входных репозиториев и генерация совместимого кода).
- [ ] **`TokenBudget` механизм** (лимит $0.50/запуск, каскадные модели: дешёвые → дорогие).
- [ ] **`CostOptimization` модуль** (учёт токенов, Graphiti как кэш для повторных запросов).

---

## 🏭 Phase 2: Product Assembly (Недели 5–8)

### Agents (Assembly)
- [ ] Реализовать `CodeAgent` (генерация кода через openclaude API).
- [ ] Реализовать `TestAgent` (автогенерация pytest + playwright).
- [ ] Создать `DeployAgent` (интеграция с Render/Fly.io API).

### Frontend (MVP)
- [ ] Сделать базовый UI (Next.js): дашборд, просмотр графа, логи.
- [ ] Настроить Sentry для фронтенда и бэкенда.
- [ ] Интегрировать Monaco Editor для редактирования кода.

### NEW: Safety & Recovery
- [ ] **`SafetyGuard` модуль** (Guardrails для агентов: стоп-слова, лимиты глубины рекурсии).
- [ ] **`DebugAgent`** (анализ Sentry-ошибок + граф контекста → автофикс через `openclaude refactor`).
- [ ] **`BackupAgent`** (экспорт графов в S3/GCS, ежедневные бэкапы).

---

## 🏪 Phase 3: Marketplace & Enterprise (Недели 9–12)

### Marketplace & Billing
- [ ] Создать Marketplace API (CRUD для шаблонов).
- [ ] Реализовать Stripe-биллинг (подписки, usage-based).
- [ ] Добавить RBAC и SSO (SAML/OIDC) для Enterprise.

### Frontend (Full)
- [ ] Написать SEO-лэндинг (Next.js SSG + JSON-LD).
- [ ] Провести нагрузочное тестирование (k6).
- [ ] Добавить i18n (RU, EN, ZH-CN) на базе `next-intl`.

### NEW: Activation & Multi-tenancy
- [ ] **`WebhookNotifier`** (уведомления в Slack/Telegram о готовности продукта).
- [ ] **Multi-tenancy** (Schema-per-tenant в Neo4j или Namespace, Data Residency для GDPR).
- [ ] **"Product DNA" система** (сохранение "генетического кода" продукта, скрещивание продуктов).
- [ ] **"First Product Challenge"** (месяц Pro бесплатно за деплой за 24 часа).

---

## 📂 Documentation (Continuous)

- [ ] `docs/README.md` (быстрый старт).
- [ ] `docs/architecture.md` (C4 model: Context, Containers, Components).
- [ ] `docs/api.md` (OpenAPI 3.1 спецификация).
- [ ] `docs/agents.md` (описание всех агентов и их ролей).
- [ ] `docs/marketplace.md` (как создавать шаблоны).
- [ ] `docs/security.md` (OWASP, секреты, аудит).
- [ ] **NEW:** `docs/licensing-and-ip.md` (IP, лицензии, GPL-совместимость).
- [ ] **NEW:** `docs/cost-optimization.md` (экономика токенов).
- [ ] **NEW:** `docs/multi-tenancy.md` (изоляция данных).
- [ ] **NEW:** `docs/activation-flow.md` (путь пользователя от регистрации до "aha moment").

---

## ✅ Done (Заполняется по ходу)

_(Пока пусто — начинаем Phase 0)_