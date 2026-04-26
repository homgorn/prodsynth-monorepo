# ProdSynth Security & Compliance (BMAD v2.0 — Phase 4)

## 1. Authentication & Authorization

### JWT Structure
```json
{
  "sub": "user_123",
  "workspace_id": "ws_456",
  "roles": ["editor"],
  "plan": "pro",
  "mfa": true,
  "exp": 1714128000,
  "iss": "https://app.prodsynth.com"
}
```

### RBAC Permissions Matrix

| Role | Projects | Team | Billing | SSO | Audit |
|------|----------|------|---------|-----|-------|
| **owner** | * | * | * | * | * |
| **admin** | * | * | read | — | read |
| **editor** | read/write | — | — | — | — |
| **viewer** | read | — | — | — | — |
| **billing_admin** | — | read | * | — | — |

### SSO Providers
- **Google Workspace** — OAuth2, domain verification
- **GitHub** — OAuth2, org membership enforcement
- **Okta** — SAML 2.0, MFA enforcement
- **Azure AD** — OIDC, group-to-role mapping

---

## 2. OWASP Top 10 Mitigations

### A01: Broken Access Control
- [x] TenantMiddleware: workspace_id enforced on every request
- [x] RLS policies: PostgreSQL row-level security
- [x] Role checks: `has_permission(roles, resource, action)` decorator
- [x] Resource ownership: users can only access their own projects

### A02: Cryptographic Failures
- [x] JWT with RS256 (asymmetric) — tokens signed, not encrypted
- [x] Secrets via environment variables — never in code
- [x] bcrypt password hashing (cost factor 12)
- [x] HTTPS everywhere (Cloudflare, Render)

### A03: Injection
- [x] SQLAlchemy ORM — parameterized queries only
- [x] Pydantic validation — all inputs validated before processing
- [x] AST parsing for repo analysis — sandboxed execution
- [x] SafetyGuard — blocks dangerous code patterns (exec, eval, subprocess)

### A04: Insecure Design
- [x] Rate limiting per tenant (60 req/min Free, 1000 req/min Enterprise)
- [x] Token budget enforcement — synthesis stops at $0.50
- [x] Subscription limits — projects, storage, team size

### A05: Security Misconfiguration
- [x] CORS: explicit origins only
- [x] Helmet.js — security headers (CSP, HSTS, X-Frame-Options)
- [x] No debug mode in production
- [x] Minimal container images (distroless)

### A06: Vulnerable Components
- [x] Dependabot automated updates
- [x] `pip-audit` / `npm audit` in CI
- [x] Pinned versions in requirements.txt

### A07: Identification & Authentication Failures
- [x] MFA support (TOTP)
- [x] SSO enforcement option per workspace
- [x] Session timeout: 24h inactivity → re-auth
- [x] Failed login lockout: 5 attempts → 15 min lock

### A08: Software Integrity Failures
- [x] Signed container images (Cosign)
- [x] SBOM generation (Syft)
- [x] No auto-updates from untrusted sources

### A09: Security Logging Failures
- [x] AuditEvent model: all significant actions logged
- [x] Structured logging → Loki (JSON format)
- [x] Retention: 90 days default, 1 year Enterprise

### A10: SSRF Protection
- [x] URL validation before fetching repos
- [x] Allowlist: only github.com, gitlab.com, bitbucket.org by default
- [x] Private repos require explicit token addition

---

## 3. GDPR & Data Residency

### Data Minimization
- Users provide: email, name, password (hashed)
- Optional: avatar URL, SSO identifiers
- We NEVER store: credit card numbers (Stripe), passwords in plain text

### Right to Erasure
- `DELETE /api/v1/account` → anonymizes data, deletes graphs
- Scheduled job: anonymizes deleted users after 30 days

### Data Residency
| Plan | Region | Strategy |
|------|--------|---------|
| Free/Pro | Single region (EU or US) | Schema-per-tenant in shared DB |
| Enterprise | Configurable (AWS/GCP/Azure) | Dedicated schema per workspace |

### Consent Management
- Cookie banner on first visit
- Analytics: anonymized (no PII)
- Marketing emails: opt-in only

---

## 4. Secrets Management

### Production
```
AWS Secrets Manager / GCP Secret Manager
  ├── STRIPE_API_KEY
  ├── DATABASE_URL
  ├── REDIS_URL
  ├── JWT_SECRET (RS256 private key)
  ├── LLM_API_KEYS (OpenClaude, OpenAI)
  └── SSO_CLIENT_SECRETS (Google, GitHub, Okta, Azure)
```

### Development
- `.env.local` (never committed)
- `.env.example` template in repo
- `.gitignore` excludes all `.env` files

### Rotation Policy
- JWT signing keys: rotate every 90 days
- SSO secrets: rotate every 180 days
- LLM API keys: rotate every 30 days (unused key deletion)

---

## 5. Audit Logging

### Event Schema
```json
{
  "id": "audit_123",
  "workspace_id": "ws_456",
  "user_id": "user_789",
  "action": "project.delete",
  "resource_type": "project",
  "resource_id": "proj_abc",
  "timestamp": 1714041600,
  "ip_address": "203.0.113.42",
  "user_agent": "Mozilla/5.0...",
  "status": "success",
  "details": {}
}
```

### Actions Tracked
- Auth: login, logout, sso_login, mfa_enable, password_change
- Projects: create, update, delete, share, clone, export
- Billing: subscribe, upgrade, downgrade, cancel, payment_failed
- Team: invite, join, role_change, remove, sso_enforce
- SSO: config_change, provider_connected, provider_disconnected
- Workspace: create, update, delete, export
- Product: run_start, run_complete, run_failed, deploy, webhook_triggered

### Retention
- Free/Pro: 90 days (hot storage)
- Enterprise: 1 year (hot) + 3 years (cold archive)

### SIEM Integration
- Export to: Splunk, Datadog, Elastic SIEM
- Format: CEF (Common Event Format)
- Transport: syslog over TLS

---

## 6. Container & Runtime Security

### Image Hardening
```dockerfile
FROM python:3.11-slim-bookworm
# No root user
USER app
# Read-only filesystem
# No shell access in production
# Distroless base image for final stage
```

### Runtime Policies
- No `privileged` containers
- Pod security: restricted policy
- Network policies: default deny, explicit allow
- AppArmor/SELinux profiles

---

## 7. Incident Response

### Severity Levels
| Level | Response Time | Example |
|-------|-------------|---------|
| P0 (Critical) | 15 min | Data breach, complete outage |
| P1 (High) | 1 hour | Partial data exposure, major feature broken |
| P2 (Medium) | 4 hours | Non-critical vulnerability, degraded performance |
| P3 (Low) | 24 hours | Minor bug, cosmetic issue |

### Response Steps
1. **Detect** → Grafana alerts + automated PagerDuty
2. **Contain** → Isolate affected workspace, revoke compromised sessions
3. **Eradicate** → Patch vulnerability, rotate compromised secrets
4. **Recover** → Restore from backup, verify data integrity
5. **Post-mortem** → blameless review within 48h, action items tracked

### Backup & Recovery
- **Frequency:** Every 6 hours (incremental), daily (full)
- **Retention:** 30 days
- **RTO:** < 1 hour
- **RPO:** < 6 hours
- **Test restore:** Monthly dry run