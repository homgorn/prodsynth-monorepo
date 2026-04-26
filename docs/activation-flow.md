# ProdSynth Activation Flow (BMAD v2.0 — Phase 4)

## User Journey: From Signup to "Aha Moment"

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          USER ACTIVATION FLOW                                  │
│                                                                              │
│  ┌──────────┐   ┌──────────────┐   ┌────────────┐   ┌──────────────┐     │
│  │  Landing │──▶│  Sign Up    │──▶│  Dashboard │──▶│  First      │     │
│  │  Page    │   │  (2 mins)  │   │  (30 sec) │   │  Synthesis │     │
│  └──────────┘   └──────────────┘   └────────────┘   └──────────────┘     │
│                                                              │               │
│                    ┌───────────────────────────────────────────┘               │
│                    ▼                                                           │
│          ┌──────────────┐   ┌────────────┐   ┌────────────┐   ┌───────────┐ │
│          │  Product     │──▶│  Share    │──▶│  Upgrade  │──▶│  Pro User │ │
│          │  Deployed   │   │  (CTA)   │   │  (Trial)  │   │  (Churn↓) │ │
│          └──────────────┘   └────────────┘   └────────────┘   └───────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Landing Page → Sign Up (2 minutes)

### What the user sees:
1. **Hero section** — "Turn any repo into a product in 5 minutes"
2. **Live demo** — 30-second video showing full synthesis
3. **Social proof** — "500+ products generated", testimonials
4. **How it works** — 3-step visual (paste repo → AI analyzes → product ready)
5. **Pricing table** — Clear Free/Pro/Enterprise tiers
6. **FAQ** — Top 10 questions
7. **CTA** — "Start Free" or "Sign up with GitHub"

### Sign Up Friction Reduction:
- [x] OAuth sign-up (GitHub, Google) — no password creation
- [x] Magic link option — email only
- [x] Single form field (email) → instant account creation
- [x] No credit card required for Free tier
- [x] Clear value prop on signup page

### Analytics Events:
```
landing_view         → page, referrer
cta_click           → "Start Free" button
signup_page_view    → source (landing / direct)
oauth_start         → provider
oauth_complete      → provider, success
email_signup_start  →
email_signup_complete →
```

---

## Step 2: Dashboard Onboarding (30 seconds)

### First Login Experience:
1. **Welcome modal** — "You're in! Let's build your first product."
2. **2-step wizard:**
   - Step 1: "Paste your GitHub repo URL" OR "Describe your idea"
   - Step 2: "Choose your target" (Docker / Next.js / API / Custom)
3. **Quick-start templates** — 3 popular starting points shown

### Empty State Design:
```
┌──────────────────────────────────────────────────────┐
│                                                       │
│   🚀 Your First Product Awaits                       │
│                                                       │
│   Paste a GitHub URL to turn any repo into           │
│   a working, deployable product.                      │
│                                                       │
│   ┌─────────────────────────────────────────────┐    │
│   │  https://github.com/user/repo              │    │
│   └─────────────────────────────────────────────┘    │
│                                                       │
│   [Generate Product →]                               │
│                                                       │
│   ─── Or start from an idea ───                      │
│   ┌─────────────────────────────────────────────┐    │
│   │  "AI-powered task manager with Slack..."   │    │
│   └─────────────────────────────────────────────┘    │
│                                                       │
└──────────────────────────────────────────────────────┘
```

### Analytics Events:
```
dashboard_view           → workspace_id, plan
onboarding_modal_view   →
repo_url_submit         → url (domain only, not full)
idea_submit            → idea_text (truncated)
template_select        → template_id
```

---

## Step 3: First Synthesis (THE AHA MOMENT)

### The Critical 5-Minute Experience:

#### 0:00 — "Starting synthesis..."
```
┌──────────────────────────────────────────────────────┐
│  🎯 Building: my-saas-app                            │
│                                                       │
│  [ResearchAgent]      Analyzing repo...  ✅           │
│  [ArchitectAgent]     Designing C4 model... ✅         │
│  [CodeAgent]          Generating code...    ▶ 60%    │
│  [TestAgent]          Writing tests...     ○           │
│  [DeployAgent]        Deploying...       ○           │
│                                                       │
│  ⚡ Token budget: $0.23 / $0.50                    │
└──────────────────────────────────────────────────────┘
```

#### 1:30 — First code appears
- User sees live file tree updating
- "CodeAgent wrote 127 files in 1.2 seconds"
- Streaming output in terminal-style panel

#### 3:00 — Tests start
- "TestAgent generated 84 tests (73 passing, 11 skipped)"
- Coverage meter fills: "81% coverage"

#### 5:00 — Deploy complete
- 🎉 Confetti animation
- "Your product is live at: https://my-saas-app.onrender.com"
- "Share this product" Twitter/LinkedIn buttons
- "View on GitHub" link

### AHA MOMENT Metrics:
- **Target:** < 5 minutes from submit to deployed URL
- **Success rate:** > 90% (no failures on Free tier)
- **Token budget:** Never exceed $0.50 per run

### Analytics Events:
```
synthesis_start         → project_id, target, has_repo_url
synthesis_agent_start   → project_id, agent_name
synthesis_agent_done    → project_id, agent_name, duration_ms, tokens_used
synthesis_complete      → project_id, duration_ms, total_tokens, status
synthesis_failed       → project_id, agent_name, error
deploy_complete        → project_id, url, target
share_cta_click        → platform (twitter/linkedin/whatsapp)
```

---

## Step 4: Post-Deploy Engagement

### Share / Invite Flow:
1. **Share modal** — "Your product is live! Share the news:"
   - Twitter: "I just built a SaaS app in 5 minutes with @prodsynth!"
   - LinkedIn: "Built with ProdSynth"
   - Copy link button
2. **Invite teammates** — "Collaborate with your team" (Pro+)
3. **GitHub repo** — Auto-created repo with full code

### Upgrade Nudges (Contextual):
| Trigger | Message | CTA |
|---------|---------|-----|
| 3 projects created | "You've created 3 projects. Upgrade to Pro for unlimited." | "Start Pro — Free for 14 days" |
| 10+ synthesis runs | "You've used 10 runs this month. Pro gives you unlimited." | "Upgrade to Pro" |
| Team member invited | "Add unlimited team members. Upgrade to Pro." | "Start Pro Trial" |
| Marketplace visited | "Publish your product in the Marketplace. Pro required." | "Start Pro" |

---

## Step 5: First Product Challenge (Growth Hack)

### Campaign: "Build in 24 Hours, Get 1 Month Pro Free"

```
┌────────────────────────────────────────────────────────┐
│  🏆 First Product Challenge                            │
│                                                        │
│  Build and deploy a real product in 24 hours.          │
│  If you ship — get 1 month of Pro for FREE.            │
│                                                        │
│  ┌──────────────────────────────────────────────┐     │
│  │  Starts in: 2 days, 14:32:07                │     │
│  │                                              │     │
│  │  [Register for Challenge →]                   │     │
│  └──────────────────────────────────────────────┘     │
│                                                        │
│  How it works:                                        │
│  ✓ Sign up → ✓ Build → ✓ Deploy → ✓ Get Pro free       │
└────────────────────────────────────────────────────────┘
```

### Requirements:
1. Must be a real product (not a placeholder)
2. Must be deployed and publicly accessible
3. Must be created within 24 hours of challenge start
4. Submit via form with deployed URL + GitHub repo

### Analytics Events:
```
challenge_page_view    → referrer
challenge_register     → user_id
challenge_submit       → project_url, deploy_target, created_at
challenge_eligible     → verified (boolean)
challenge_reward_sent  → pro_months_granted
```

---

## Step 6: Retention Loops

### Weekly Digest Email (Free users):
- "You have 2 unused synthesis runs this week"
- "Top templates from the marketplace"
- "New features" changelog

### Monthly Re-engagement (Dormant users):
- "Your last synthesis was 30 days ago"
- "Check out what's new" with screenshot
- "Reactivate — your projects are still there"

### Pro User Benefits:
- Usage dashboard with cost savings
- Team activity feed
- Marketplace earnings notifications

---

## Activation Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Landing → Sign Up | > 5% | — |
| Sign Up → First Synthesis | > 70% | — |
| First Synthesis → Deploy | > 90% | — |
| First Deploy → Share | > 40% | — |
| Share → Upgrade to Pro | > 15% | — |
| **Aha Moment Time** | **< 5 min** | — |
| Churn (month 1) | < 10% | — |
| Churn (month 3) | < 25% | — |

### Funnel Visualization (Grafana):
```
Landing Views:     ████████████████████████████████████ 10,000
Sign Ups:          ████████████                          1,200  (12%)
First Project:     ██████████                           1,000  (10%)
First Synthesis:   ████████                             800   (8%)
Deploy:            ███████                              700   (7%)
Upgrade:           ██                                   200   (2%)
```