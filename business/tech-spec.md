# tech-spec.md

## 1. Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | **Node.js 20.x** + **Express 5** | Mature ecosystem, async/await, easy integration with GitHub APIs. |
| **Type System** | **TypeScript 5.3** | Compile‑time safety, better DX for a small team. |
| **Database** | **PostgreSQL 16** (managed via Supabase) | Relational schema for auditability, strong ACID guarantees. |
| **Auth** | **OAuth2 (GitHub)** + **JWT** | Native GitHub integration for repo access, stateless auth for API. |
| **Serverless Functions** | **Vercel Edge Functions** | Low‑latency, auto‑scaling for API endpoints. |
| **CI/CD** | **GitHub Actions** | Native repo, easy secrets management, free tier. |
| **Observability** | **OpenTelemetry** + **Prometheus** + **Grafana** (managed via Render) | Unified tracing, metrics, and dashboards. |
| **Logging** | **Logflare** (via Vercel) | Serverless‑friendly, free tier for 1M logs/month. |
| **Frontend** | **React 18** + **Next.js 14** (SSG/ISR) | SEO‑friendly, incremental static regeneration, easy API integration. |
| **State Management** | **React Query** | Declarative data fetching, caching, optimistic updates. |
| **Testing** | **Jest** + **Supertest** | Unit & integration tests for API. |
| **Linting/Formatting** | **ESLint + Prettier** | Consistent code style. |

> **Why this stack?**  
> - All components have generous free tiers (Supabase, Vercel, Render, Logflare).  
> - TypeScript + Express gives a quick, type‑safe API surface.  
> - PostgreSQL is the de‑facto standard for SaaS data models and works well with Supabase’s auth & storage.  
> - Vercel Edge Functions keep latency low for GitHub‑centric workflows.  

---

## 2. Hosting

| Component | Platform | Free‑Tier Details | Notes |
|-----------|----------|-------------------|-------|
| **API** | **Vercel** | 125 GB bandwidth, 125 GB storage, 125 k serverless invocations/month | Edge functions auto‑scale, no cold‑start for authenticated routes. |
| **Database** | **Supabase** | 1 GB storage, 50 k rows, 500 k requests/month | Built‑in Postgres, Row‑level security, Auth integration. |
| **Frontend** | **Vercel** | Same as API | SSR/ISR for product pages. |
| **Observability** | **Render** | 1 GB storage, 100 GB bandwidth, 1 k requests/month | Deploy Prometheus & Grafana containers. |
| **CI** | **GitHub Actions** | 2 k min/month, 500 MB storage | Native to repo, secrets stored in repo settings. |

> **Scaling path** – Once usage exceeds free limits, upgrade to Supabase Pro (10 GB DB, 1 M requests) and Render’s paid tier (10 GB storage, 1 TB bandwidth). Vercel’s paid plan adds 1 TB bandwidth and 1 M invocations.

---

## 3. Data Model

| Table | Key Fields | Description | Constraints |
|-------|------------|-------------|-------------|
| **users** | `id (PK)`, `github_id`, `name`, `email`, `created_at` | Authenticated GitHub users. | `github_id` unique. |
| **repos** | `id (PK)`, `user_id (FK)`, `github_repo_id`, `name`, `url`, `created_at` | Repositories the user owns or has granted access to. | `github_repo_id` unique per user. |
| **enhancements** | `id (PK)`, `repo_id (FK)`, `name`, `description`, `status`, `created_at`, `updated_at` | Feature enhancement requests. | `status` enum: `draft`, `submitted`, `approved`, `rejected`, `deployed`. |
| **enhancement_files** | `id (PK)`, `enhancement_id (FK)`, `path`, `content`, `created_at` | Files that will be added/modified. | `path` unique per enhancement. |
| **audit_logs** | `id (PK)`, `user_id (FK)`, `action`, `target_type`, `target_id`, `timestamp` | Immutable audit trail. | Index on `user_id`. |
| **subscriptions** | `id (PK)`, `user_id (FK)`, `plan`, `status`, `stripe_id`, `next_billing_date` | Billing info. | `plan` enum: `free`, `pro`. |

> **Row‑Level Security** – Supabase policies enforce that a user can only see their own repos and enhancements.

---

## 4. API Surface

| Method | Path | Purpose | Auth | Notes |
|--------|------|---------|------|-------|
| **GET** | `/api/v1/repos` | List user’s repos | OAuth | Paginated, 50 per page |
| **POST** | `/api/v1/repos` | Register a new repo (GitHub webhook) | OAuth | Validates GitHub webhook signature |
| **GET** | `/api/v1/enhancements` | List enhancements for a repo | OAuth | Query params: `repo_id`, `status` |
| **POST** | `/api/v1/enhancements` | Create new enhancement | OAuth | Body: `repo_id`, `name`, `description` |
| **GET** | `/api/v1/enhancements/:id` | Retrieve enhancement details | OAuth | Includes files |
| **PATCH** | `/api/v1/enhancements/:id` | Update enhancement (name/description/files) | OAuth | Partial updates |
| **DELETE** | `/api/v1/enhancements/:id` | Delete an enhancement | OAuth | Only if status is `draft` |
| **POST** | `/api/v1/enhancements/:id/submit` | Submit enhancement for review | OAuth | Triggers CI pipeline |
| **POST** | `/api/v1/enhancements/:id/deploy` | Deploy approved enhancement | OAuth | Calls GitHub API to push changes |
| **GET** | `/api/v1/health` | Health check | Public | Returns 200 OK |
| **GET** | `/api/v1/metrics` | Prometheus metrics endpoint | Public | Exposes `/metrics` |

> **Rate limits** – 1000 requests per minute per user (enforced via middleware).  

---

## 5. Security Model

| Layer | Mechanism | Details |
|-------|-----------|---------|
| **Auth** | OAuth2 (GitHub) + JWT | Users authenticate via GitHub; backend issues short‑lived JWTs (15 min) signed with HS256. |
| **Secrets** | GitHub Secrets + Vercel Environment Variables | `GITHUB_TOKEN`, `STRIPE_SECRET`, `SUPABASE_URL`, `SUPABASE_KEY`. |
| **IAM** | Supabase RLS + PostgREST | Policies: `users` can only access rows where `user_id = current_user.id`. |
| **Transport** | HTTPS only | Vercel enforces TLS. |
| **Input Validation** | `zod` schemas | All request bodies validated server‑side. |
| **CSRF** | Same‑site cookies + double submit token | For any state‑changing endpoints. |
| **Rate Limiting** | Express middleware | 1000 req/min per IP/user. |
| **Audit** | `audit_logs` table | Immutable logs of all actions. |

---

## 6. Observability

| Category | Tool | Implementation |
|----------|------|----------------|
| **Logging** | Logflare (via Vercel) | Structured JSON logs, filter by `user_id`, `repo_id`. |
| **Metrics** | Prometheus + Grafana (Render) | Exported via `/metrics` endpoint: `api_requests_total`, `api_request_duration_seconds`, `enhancement_submissions_total`. |
| **Tracing** | OpenTelemetry (Node) | Export to Jaeger (Render) for distributed tracing of GitHub API calls. |
| **Error Tracking** | Sentry (Node) | Capture unhandled exceptions, attach user context. |
| **Health** | `/api/v1/health` | Simple liveness/readiness probe. |

> **Alerting** – Grafana alerts on `api_request_duration_seconds > 2s` and `enhancement_submissions_total` spike.

---

## 7. Build & CI

| Stage | Tool | Steps |
|-------|------|-------|
| **Lint** | ESLint + Prettier | `npm run lint` |
| **Test** | Jest + Supertest | `npm run test` |
| **Build** | Vercel Edge | `npm run build` (Next.js) |
| **Deploy** | GitHub Actions | `vercel --prod` |
| **Database Migration** | Supabase CLI | `supabase db push` |
| **Secrets** | GitHub Actions secrets | `SUPABASE_KEY`, `GITHUB_TOKEN`, etc. |
| **Versioning** | Semantic Versioning via `npm version` | Tag on merge to `main`. |
| **Rollback** | Vercel rollback | Manual via dashboard or CLI. |

> **Pipeline** – On every push to `main`, the workflow runs lint → test → build → deploy. On PR merge, a preview deployment is created.  
> **Security Checks** – `npm audit` and `trivy` run before deployment.

---

### Quick Reference

```bash
# Local dev
npm install
npm run dev

# Run tests
npm run test

# Deploy
vercel --prod
```

---