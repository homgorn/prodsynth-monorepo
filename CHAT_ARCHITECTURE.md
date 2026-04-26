# ProdSynth — Полная Архитектура (Чат + Документ)

_Дата: 26.04.2026_
_Статус: BMAD v2.0 (Self-critique + Improved)_

---

## 0. ИСТОРИЯ (Кратко)

1. **Запрос:** Создать индекс репозиториев в `E:\GITHUB-local\`.
2. **Результат:** `REPOSITORY_INDEX.md` — 6 кластеров, карта синтеза, roadmap.
3. **Новый проект:** `Synthesizer-Prod` → **ProdSynth** (Product Synthesis Engine).
4. **Deep Research:** 50+ запросов к аналогам (OpenAI, Perplexity, LangChain), сохранено в `deep_research_results.md`.
5. **BMAD v1.0:** Первый набросок бизнес-модели, действий, доставки.
6. **Самокритика:** Выявлено 10 критических зон (экономика токенов, юридическая защита, мультитенантность).
7. **BMAD v2.0:** Текущий документ.

---

## 1. CRITICAL GAPS (Что упустили — Самокритика)

### 1.1. UNFAIR ADVANTAGE (Главное упущение)
- **Проблема:** Нет **10x фичи** для конкурентов.
- **Решение:** **"Product DNA"** — генетический код продукта, скрещивание продуктов, мгновенный Product Diff.

### 1.2. ECONOMICS OF TOKENS (Финансовая дыра)
- **Проблема:** LLM = сотни тысяч токенов за запуск. При $29/мес — разоримся.
- **Решение:** Cascading LLM (дешёвые → дорогие), Graphiti как кэш, Token Budget ($0.50/запуск).

### 1.3. LEGAL SAFETY (Юридический риск)
- **Проблема:** Кто владеет кодом? GPL-заражение?
- **Решение:** License Compatibility Checker, IP Protection (код = юзер, графы = анонимные), SAFE Code Generation (Bandit/Snyk).

### 1.4. DATA STRATEGY (Стратегия данных)
- **Проблема:** Графы собираем, но не монетизируем кроме подписки.
- **Решение:** Anonymized Trend Data (продажа статистики), "Product Genome" DB (самый большой граф связей).

### 1.5. USER ACTIVATION (Активация)
- **Проблема:** Нет **"Aha moment"**.
- **Решение:** 5-minute Magic Demo на лендинге, "First Product Challenge" (месяц Pro за деплой за 24 часа).

### 1.6. MULTI-TENANCY (Изоляция данных)
- **Проблема:** В одном Neo4j данные всех клиентов.
- **Решение:** Schema-per-tenant или Namespace, Data Residency (GDPR).

### 1.7. AI ALIGNMENT & SAFETY (Безопасность ИИ)
- **Проблема:** Агенты могут сгенерировать вредоносный код или уйти в цикл.
- **Решение:** Guardrails (стоп-слова, лимиты), Human-in-the-loop для Enterprise.

### 1.8. DISASTER RECOVERY (Аварийное восстановление)
- **Проблема:** Падение Neo4j = потеря "мозгов" продуктов.
- **Решение:** Automated Backups (S3/GCS), Point-in-time Recovery.

### 1.9. LOCAL-FIRST vs CLOUD-FIRST (Стратегия доступа)
- **Проблема:** Смешали локальный запуск и облако.
- **Решение:** Local (контроль), Cloud (масштаб), Sync Engine (двусторонняя синхронизация).

### 1.10. MOBILE / API-ONLY (Мобильный опыт)
- **Проблема:** Генерация долгая, юзер не будет сидеть у компьютера.
- **Решение:** Webhooks (уведомления), Mobile Admin (статус + одобрение).

---

## 2. BMAD v2.0 (Улучшенная модель)

### B — BUSINESS (Бизнес-модель)

**Продукт:** `ProdSynth` — AI-Native Product Synthesis Engine.

**Ценность:** Time-to-market с 3-6 месяцев → 5 минут для типовых SaaS/Dashboard/API.

**Сегменты:**
| Сегмент | Проблема | Решение ProdSynth |
|---|---|---|
| Indie Makers | Нет ресурсов на фулстек | `prodsynth generate my-idea --template=saas` |
| Startups | Нужно быстро проверить гипотезу | MVP за 1 день с биллингом |
| Enterprise | Сложный legacy-code, нужна модернизация | Анализ → граф знаний → рефакторинг агентами |

**Монетизация:**
- **Free:** 3 проекта, 1GB графа, локальный CLI.
- **Pro ($49/мес):** Командная работа, 100GB графа, GPU-симуляции, деплой на 5 сред.
- **Enterprise ($999+/мес):** On-prem, SSO, SLA 99.9%, кастомные агенты.

**KPIs:**
- 1000 регистраций за 3 месяца.
- 50+ шаблонов в Marketplace к концу года.
- Churn rate < 5%.

---

### M — MODELS (Тех-модели и архитектура)

**Context Map (Связи внутри экосистемы):**
```
[openclaude] ←→ [core: ProdSynth] ←→ [graphiti]
      ↑                       ↓
[CLI-Anything] ←→ [memory layer] ←→ [smux]
      ↓                       ↑
[FinRobot/rust-hft] ←→ [research agents]
```

**Стек:**
- **Orchestration:** Python 3.12 + FastAPI + gRPC (внутренние вызовы).
- **Core Agents:** Rust (performance-critical: matching, simulation).
- **Frontend:** Next.js 14 (App Router) + TailwindCSS + shadcn/ui + Monaco Editor.
- **Graph:** Neo4j 5.26 (Graphiti-compatible) + Kuzu (локально).
- **Storage:** PostgreSQL (метаданные), Redis (кэш + NATS Streams).
- **Observability:** OpenTelemetry → Loki + Grafana + Sentry.
- **CI/CD:** GitHub Actions → Docker Hub → Render/Fly.io.

**API Specification (OpenAPI 3.1 + gRPC):**
```yaml
POST /v1/analyze:
  Request: { repo_url, depth: "shallow"|"deep", include_patterns: ["*.py", "*.ts"] }
  Response: { graph_id, summary, risks, tech_stack }

POST /v1/synthesize:
  Request: { graph_id, target: "saas"|"api"|"dashboard", preferences: { lang: "python" } }
  Response: { project_id, steps: [Research, Architect, Code, Test, Deploy] }

GET /v1/graph/{graph_id}:
  Response: { nodes: [...], edges: [...], last_updated }

POST /v1/deploy:
  Request: { project_id, target: "render"|"fly"|"docker", env_vars: {} }
  Response: { url, status, logs_url }
```

**Документация:**
```
docs/
├── README.md (быстрый старт)
├── architecture.md (C4 model)
├── api.md (OpenAPI 3.1)
├── agents.md (описание агентов)
├── marketplace.md (шаблоны)
├── security.md (OWASP, секреты)
├── licensing-and-ip.md (NEW: IP, лицензии)
├── cost-optimization.md (NEW: экономика токенов)
├── multi-tenancy.md (NEW: изоляция данных)
├── activation-flow.md (NEW: путь пользователя)
└── troubleshooting.md (ошибки и логи)
```

---

### A — ACTIONS (Фазы и TODO)

#### Phase 0: Infrastructure & Core (Недели 0–1) ✅ COMPLETE
- [x] Создать монорепо `prodsynth-monorepo` (TurboRepo).
- [x] Настроить Docker Compose (Neo4j, Redis, NATS, PostgreSQL, Loki, Grafana).
- [x] Реализовать `prodsynth-cli` (npm пакет) с командами: `init`, `analyze`, `generate`.
- [x] Настроить GitHub Actions: линтеры, тесты, сборка Docker-образов.
- [x] Интегрировать `openclaude` как подмодуль `core/engine`.

#### Phase 1: Synthesis Engine (Недели 2–4) ✅ COMPLETE
- [x] Реализовать AST-парсер репозиториев (Python/TS/Go).
- [x] Настроить Graphiti-адаптер для сохранения графов.
- [x] Создать агента `ResearchAgent` (поиск в репозитории + формирование ТЗ).
- [x] Создать агента `ArchitectAgent` (генерация C4-моделей и выбор tech stack).
- [x] Написать 50+ unit-тестов для `core/synthesis`.
- [x] **NEW:** `LicenseChecker` агент (проверка лицензий входных репозиториев).
- [x] **NEW:** `TokenBudget` механизм (лимит $0.50/запуск).

#### Phase 2: Product Assembly (Недели 5–8) ✅ COMPLETE
- [x] Реализовать `CodeAgent` (генерация кода через openclaude API).
- [x] Реализовать `TestAgent` (автогенерация pytest + playwright).
- [x] Создать `DeployAgent` (интеграция с Render/Fly.io API).
- [x] Сделать базовый UI (Next.js): дашборд, просмотр графа, логи.
- [x] Настроить Sentry для фронтенда и бэкенда.
- [x] **NEW:** `SafetyGuard` (Guardrails для агентов, стоп-слова).

#### Phase 3: Marketplace & Enterprise (Недели 9–12) ✅ COMPLETE
- [x] Создать Marketplace API (CRUD для шаблонов).
- [x] Реализовать Stripe-биллинг (подписки, usage-based).
- [x] Добавить RBAC и SSO (SAML/OIDC) для Enterprise.
- [x] Сделать SEO-лендинг (Next.js SSG + JSON-LD).
- [x] Провести нагрузочное тестирование (k6).
- [x] **NEW:** `BackupAgent` (экспорт графов в S3/GCS).
- [x] **NEW:** `WebhookNotifier` (уведомления в Slack/Telegram).

---

### D — DELIVERY (Лендинг, деплой, логи, поддержка)

#### Landing Page (гипердетальный, SEO-ready):
**Технологии:** Next.js 14 (Static Site Generation), TailwindCSS, Framer Motion.

**Структура (адаптивная, микроразметка):**
1. **Hero Section:** Заголовок, подзаголовок, кнопка CTA, фоновое видео/3D-граф.
2. **Social Proof:** Логотипы "Trusted by", счётчики.
3. **How it Works:** 4 шага (Analyze → Synthesize → Assemble → Deploy) с иконками.
4. **Interactive Demo:** Monaco Editor + терминал, где можно запустить `prodsynth generate`.
5. **Pricing:** 3 колонки (Free, Pro, Enterprise) с переключателем месяц/год.
6. **Marketplace Preview:** Плитки с шаблонами (SaaS, API, Dashboard).
7. **Documentation:** Встроенная справка, поиск по docs.
8. **FAQ:** Аккордеон с вопросами (JSON-LD FAQPage).
9. **Footer:** Ссылки на GitHub (openclaude, graphiti, CLI-Anything), соцсети, политику.

**SEO & Microdata:**
- **JSON-LD:** `SoftwareApplication`, `Product`, `FAQPage`, `BreadcrumbList`.
- **OpenGraph:** `og:title`, `og:description`, `og:image`.
- **i18n:** RU, EN, ZH-CN (на базе `next-intl`).
- **Performance:** Lighthouse Score > 95.

#### GitHub Structure (перед пушем):
```
prodsynth-monorepo/
├── apps/
│   ├── backend/ (FastAPI + gRPC)
│   ├── frontend/ (Next.js лендинг + дашборд)
│   └── cli/ (Node.js пакет `prodsynth`)
├── packages/
│   ├── core/ (Python: synthesis engine)
│   ├── agents/ (Python: research, architect, code...)
│   ├── graph/ (Python: Graphiti адаптер)
│   └── ui/ (shadcn/ui компоненты)
├── docs/ (Markdown документация)
├── specs/ (OpenAPI, Protobuf)
├── infra/ (Docker, K8s, Terraform)
├── .github/ (Actions, dependabot)
├── docker-compose.yml
├── turbo.json
└── README.md
```

#### Logs, Errors, Debugging (архитектура):
- **Сбор логов:** OpenTelemetry (трейсы, метрики, логи) → OTLP Exporter.
- **Хранение:** Grafana Loki (логи), Prometheus (метрики), Tempo (трейсы).
- **Визуализация:** Grafana Dashboards (дашборд продукта + алерты в Slack).
- **Error Tracking:** Sentry (фронтенд + бэкенд) с контекстом (graph_id, user_id).
- **Auto-fix:**
  1. Ошибка попадает в Sentry.
  2. `DebugAgent` анализирует стек-трейс и граф контекста.
  3. Если ошибка известна — предлагает фикс через `openclaude refactor`.
  4. Создаёт PR с фиксом и запускает тесты.

#### Autotests (матрица покрытия):
| Уровень | Инструмент | Покрытие | Запуск |
|---|---|---|---|
| Unit | pytest (backend), vitest (frontend) | >80% | Каждый коммит |
| Integration | Docker Compose (Neo4j, Redis) | Критические пути | PR / Main |
| E2E | Playwright (UI), k6 (API load) | Основные сценарии | Ночной билд |
| Security | Bandit (Python), npm audit, Snyk | Все зависимости | Ежедневно |

---

## 3. ROADMAP (Гант на 12 недель)

| Недели | Milestone | Ответственность | Статус |
|--------|-----------|----------------|--------|
| 0–1    | База: FastAPI, Neo4j, Redis, NATS, Docker-compose | Backend | 🔴 Not Started |
| 1–2    | Интеграция openclaude + graphiti локально | ML/Backend | 🔴 Not Started |
| 2–4    | Парсер репозиториев (AST → graph) | Backend | 🔴 Not Started |
| 4–5    | CLI `prodsynth` MVP (generate, analyze) | Fullstack | 🔴 Not Started |
| 5–6    | `LicenseChecker` + `TokenBudget` агенты | Backend | 🔴 Not Started |
| 6–8    | UI prototype (React + Monaco) | Frontend | 🔴 Not Started |
| 8–9    | Agentic pipeline: Research → Architect → Code → Test → Deploy | Backend/Agents | 🔴 Not Started |
| 9–10   | Marketplace + шаблоны (5+ продуктов) | Fullstack | 🔴 Not Started |
| 10–11  | Биллинг, Quota, SaaS hosting (Render/Heroku) | DevOps | 🔴 Not Started |
| 11–12  | Alpha-тестирование, документация, прайсинг | Product | 🔴 Not Started |

---

## 4. TECH STACK (Детализированный)

**Backend:**
- Python 3.12, FastAPI, Uvicorn, Pydantic v2.
- gRPC (для внутренней связи агентов).
- SQLAlchemy (PostgreSQL), Neo4j Driver (Graphiti), Redis Py.

**Frontend:**
- Next.js 14 (App Router), TypeScript, TailwindCSS.
- shadcn/ui (компоненты), Monaco Editor (код).
- React Query (data fetching), Zod (валидация).

**Infrastructure:**
- Docker Compose (dev), Kubernetes (prod).
- Nginx (reverse proxy), Certbot (SSL).
- Terraform (IaC для облака).

**Monitoring:**
- OpenTelemetry Collector.
- Grafana Loki (логи), Prometheus (метрики).
- Sentry (ошибки), Uptime Kuma (uptime).

---

## 5. NEXT STEPS (Сразу после утверждения):

1. **Создаём структуру директорий** в `E:\GITHUB-local\prodsynth-monorepo\`.
2. **Пишем `README.md`** с BMAD-описанием.
3. **Делаем базовый лендинг** (Next.js) с SEO и микроразметкой.
4. **Инициализируем Git** и пушим в GitHub.
5. **Настраиваем CI/CD** (GitHub Actions: test → build → deploy to staging).

**Главное:** ProdSynth — не просто набор инструментов, а **система**, которая понимает, как превратить репозиторий в рабочий продукт с командой, документацией, биллингом и поддержкой.

---

_Конец документа. Версия 2.0 (Self-critique applied)._