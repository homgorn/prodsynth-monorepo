# ProdSynth Marketplace Guide (BMAD v2.0 — Phase 4)

## Overview

The **ProdSynth Marketplace** is where users publish, discover, and purchase product templates. Templates are pre-built product patterns (SaaS apps, APIs, dashboards) that can be customized in minutes.

---

## Creating a Template

### What Makes a Great Template

A template is a **product skeleton** — not just code, but:
- Complete project structure
- Working auth flow
- Real database schema
- Deployment configuration
- README with setup instructions
- At least 3 example screens/routes

### Template Structure

```
templates/saas-starter/
├── template.json          ← Template manifest
├── README.md             ← Setup instructions
├── .prodsynth/          ← ProdSynth metadata
│   ├── preview/         ← Screenshots, demo video
│   ├── demo/            ← Live demo URL
│   └── config.yaml      ← Template configuration
├── src/                 ← Source code
│   ├── backend/
│   └── frontend/
├── docker-compose.yml   ← Local dev setup
├── Dockerfile
└── .env.example
```

### template.json Manifest

```json
{
  "id": "saas_starter",
  "name": "SaaS Starter",
  "version": "1.2.0",
  "description": "Complete SaaS with auth, billing, and dashboard. FastAPI + Next.js + Stripe.",
  "category": "saas",
  "tags": ["auth", "billing", "dashboard", "fastapi", "nextjs"],
  "tech_stack": ["FastAPI", "Next.js 14", "PostgreSQL", "Stripe", "Tailwind"],
  "difficulty": "beginner",
  "price": 0,
  "rating": 4.8,
  "downloads": 1234,
  "requirements": {
    "node_version": ">=18.0.0",
    "python_version": ">=3.11",
    "docker": true
  },
  "features": [
    "User authentication (email + OAuth)",
    "Stripe billing integration",
    "Admin dashboard",
    "API documentation (OpenAPI)",
    "Playwright E2E tests",
    "Docker deployment"
  ],
  "author": {
    "id": "user_123",
    "name": "ProdSynth Team",
    "verified": true
  },
  "preview": {
    "images": ["/templates/saas-starter/preview/1.png"],
    "video_url": "https://demo.prodsynth.com/saas-starter",
    "live_url": "https://saas-starter.onrender.com"
  },
  "compatibility": {
    "license": "MIT",
    "no_gpl_contamination": true
  }
}
```

---

## Publishing Flow

```
┌──────────────────────────────────────────────────────┐
│  1. Create Template                                  │
│     └── User runs synthesis → clicks "Publish to Marketplace"  │
│                                                        │
│  2. Review (Automated)                                │
│     └── License check, code quality, security scan    │
│                                                        │
│  3. Review (Manual — if flagged)                     │
│     └── ProdSynth team reviews within 48h            │
│                                                        │
│  4. Publish                                         │
│     └── Template appears in marketplace               │
│                                                        │
│  5. Earning                                         │
│     └── User gets 70% of template revenue            │
└──────────────────────────────────────────────────────┘
```

### Automated Checks

```python
class TemplateValidator:
    async def validate(self, template_dir: str) -> ValidationResult:
        issues = []

        # 1. Manifest exists and is valid
        manifest = self._load_manifest(template_dir)
        if not manifest:
            issues.append("Missing template.json")

        # 2. License is compatible
        license_ok = self._check_license(template_dir)
        if not license_ok:
            issues.append("Incompatible license (GPL/contaminated)")

        # 3. Required files present
        required = ["README.md", "docker-compose.yml", "Dockerfile"]
        for f in required:
            if not (template_dir / f).exists():
                issues.append(f"Missing required file: {f}")

        # 4. Code quality (no obvious issues)
        quality = await self._check_quality(template_dir)
        if quality.score < 0.7:
            issues.append(f"Code quality score too low: {quality.score}")

        # 5. No prohibited patterns
        prohibited = self._scan_prohibited(template_dir)
        if prohibited:
            issues.append(f"Prohibited content: {prohibited}")

        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            quality_score=quality.score,
            license_risk=license_ok.risk
        )
```

---

## Template Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **saas** | Full SaaS applications | SaaS Starter, SaaS + AI, Multi-tenant CRM |
| **api** | Backend APIs | REST API, GraphQL API, gRPC Service |
| **dashboard** | Admin & analytics dashboards | Analytics Dashboard, CRM Dashboard |
| **ecommerce** | Online stores | Shopify-style store, Digital goods store |
| **ai** | AI-powered apps | AI Chatbot, AI Writing Assistant |
| **mobile** | Mobile-first apps | React Native + Expo, Flutter app |
| **blockchain** | Web3 apps | NFT Marketplace, DAO dashboard |
| **infra** | Infrastructure templates | Kubernetes cluster, Terraform modules |

---

## Pricing & Revenue

### Pricing Tiers

| Price | Typical Use |
|-------|------------|
| **Free ($0)** | Starter templates, community contributions |
| **Paid ($29–$299)** | Premium templates, complex products |
| **Custom** | Enterprise templates, white-label solutions |

### Revenue Split

| Party | Share | Notes |
|-------|-------|-------|
| **Template Author** | 70% | Deposited to Stripe Connect account |
| **ProdSynth** | 30% | Platform fee, payment processing, support |

### Payout Schedule
- Minimum payout: $50
- Frequency: Monthly (after the 1st of the month)
- Method: Stripe Connect (direct bank transfer)

---

## Discovery & Search

### Search Algorithm

```python
def search_templates(
    query: str,
    filters: SearchFilters,
    user_id: str
) -> SearchResults:
    # 1. Full-text search on name, description, tags
    text_results = elasticsearch.search(query, fields=["name^3", "description", "tags^2"])

    # 2. Category filter
    if filters.category:
        text_results = text_results.filter(category=filters.category)

    # 3. Tech stack filter
    if filters.tech_stack:
        text_results = text_results.filter(tech_stack__contains_any=filters.tech_stack)

    # 4. Price filter
    if filters.max_price:
        text_results = text_results.filter(price__lte=filters.max_price)

    # 5. Sort by relevance or popularity
    if filters.sort == "popular":
        text_results = text_results.order_by(downloads=-1, rating=-1)
    elif filters.sort == "newest":
        text_results = text_results.order_by(created_at=-1)
    elif filters.sort == "price_asc":
        text_results = text_results.order_by(price=1)

    # 6. Personalization (if logged in)
    if user_id:
        # Boost templates similar to user's previous downloads
        personalized = boost_similar(text_results, user_id)

    return text_results.limit(20)
```

### Filters Available
- Category (saas, api, dashboard, etc.)
- Tech stack (FastAPI, Next.js, React, etc.)
- Price range ($0–$299+)
- Rating (4+, 4.5+, 4.8+)
- Difficulty (beginner, intermediate, advanced)
- Free / Paid / Any

---

## Ratings & Reviews

### Rating System
- 1–5 stars (0.5 increments)
- Weighted average: more downloads = higher weight
- Minimum 3 reviews before showing rating
- Spam/fake review detection

### Review Criteria
```json
{
  "rating": 4.5,
  "pros": ["Great structure", "Easy to customize", "Works out of the box"],
  "cons": ["Missing email templates", "Stripe webhook needs fixes"],
  "comment": "Exactly what I needed for my MVP. Spent 20 mins customizing.",
  "use_case": "SaaS product for my consulting business"
}
```

---

## Updates & Versioning

### Template Updates

Templates can be updated (v1.0 → v1.1):
- Author pushes update → automated tests run
- If tests pass → new version published
- Users who downloaded can upgrade (diff shown)
- Old versions remain available

### Breaking Changes
- Major version bump (v1 → v2) requires explicit user action
- Changelog shown before upgrade
- Rollback available for 30 days