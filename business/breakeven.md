## breakeven.md  

### 1. Cost per Active User (monthly)

| Cost component | Assumptions | Monthly cost per active user (USD) |
|----------------|-------------|------------------------------------|
| **Compute** (1 vCPU + 2 GB RAM, on‑demand cloud VM) | 730 h / mo × $0.04 / vCPU‑hr + $0.005 / GB‑ram‑hr | **$0.33** |
| **Storage** (10 GB per user for logs, configs, model artefacts) | $0.02 / GB‑mo (standard SSD) | **$0.20** |
| **Bandwidth** (outbound 5 GB/mo per active user) | $0.09 / GB (first 10 TB) | **$0.45** |
| **Third‑party AI API** (e.g., OpenAI embeddings, 100 K tokens) | $0.0004 / 1 K tokens → $0.04 | **$0.04** |
| **Support / Ops overhead** (shared tooling, monitoring) | $0.10 per user (amortised) | **$0.10** |
| **Total variable cost / active user** |  | **$1.12** |

> **Note:** Fixed infrastructure (load balancers, CI/CD runners, base VM pool) is accounted for in the “Fixed Monthly Overhead” section below.

### 2. Fixed Monthly Overhead (baseline)

| Item | Monthly cost (USD) |
|------|--------------------|
| Core VM pool (2 × c5.large) | $70 |
| Managed DB (PostgreSQL, 100 GB) | $45 |
| Object storage (S3, 1 TB) | $23 |
| CI/CD runners (GitHub Actions) | $30 |
| Monitoring & alerting (Datadog) | $25 |
| **Total Fixed Overhead** | **$193** |

These costs are incurred regardless of user count and are spread across the active‑user base.

### 3. Pricing Tiers (per active user, per month)

| Tier | Price (USD/mo) | Included Features |
|------|----------------|-------------------|
| **Starter** | **$9** | • Core Agent‑Reach API <br>• 5 K tokens / mo AI calls <br>• 10 GB storage <br>• Email support (24 h) |
| **Professional** | **$29** | • All Starter features <br>• 25 K tokens / mo <br>• 50 GB storage <br>• Webhook & custom‑hook SDK <br>• Priority email support (12 h) |
| **Enterprise** | **$79** | • All Professional features <br>• Unlimited tokens & storage (up to 200 GB) <br>• Dedicated Slack/Phone support (4 h) <br>• SLA 99.9 % <br>• On‑premise deployment option |

### 4. Customer Acquisition Cost (CAC)

| Source | Avg. spend to acquire 1 paying user | Reasoning |
|--------|--------------------------------------|-----------|
| Content & SEO (blog, tutorials) | $12–$18 | Low‑cost, long‑tail traffic; conversion ~2 % |
| Paid ads (LinkedIn, dev‑focused platforms) | $30–$45 | Higher intent, higher CPM |
| Partnerships / Marketplace listings | $8–$14 | Co‑sell with AI‑tool vendors |
| **Weighted CAC range** (overall) | **$15 – $35** | Blend of channels; assumes 40 % organic, 60 % paid |

### 5. Lifetime Value (LTV) Estimate

Assumptions  

* Average churn per month = 5 % (typical for dev‑tool SaaS) → average customer lifespan = 1 / 0.05 = **20 months**.  
* Mix of tier adoption (Starter 60 %, Professional 30 %, Enterprise 10 %).  

**Weighted average monthly revenue per user (ARPU):**  

\[
ARPU = 0.60 \times 9 + 0.30 \times 29 + 0.10 \times 79 = 5.4 + 8.7 + 7.9 = **\$21.99**\approx\$22
\]

**LTV:**  

\[
LTV = ARPU \times \text{lifespan} = 22 \times 20 = **\$440**
\]

Subtracting average CAC (mid‑point $25) gives a net contribution margin of **~$415** per customer over its life.

### 6. Break‑Even Users Count

Break‑even occurs when **Total Monthly Revenue ≥ Fixed Overhead + Variable Cost × Active Users**.

Let **U** = number of active paying users.

\[
Revenue = ARPU \times U
\]
\[
Cost = Fixed\_Overhead + Variable\_Cost \times U
\]

Set Revenue = Cost:

\[
22U = 193 + 1.12U \\
22U - 1.12U = 193 \\
20.88U = 193 \\
U = \frac{193}{20.88} \approx **9.2**
\]

**≈ 10 paying active users** are needed to cover all monthly expenses and reach breakeven.

### 7. Path to $10 K MRR

Target MRR = $10,000.

Using the tier mix above (60/30/10), compute required user counts.

| Tier | % of users | Price | Users needed (if only this tier) |
|------|------------|-------|----------------------------------|
| Starter | 60 % | $9 | 10,000 / 9 ≈ 1,112 users |
| Professional | 30 % | $29 | 10,000 / 29 ≈ 345 users |
| Enterprise | 10 % | $79 | 10,000 / 79 ≈ 127 users |

**Mixed‑tier strategy (maintaining 60/30/10 split):**

Let total users = **T**.  
Revenue = 0.60·9·T + 0.30·29·T + 0.10·79·T = 22·T (as above).  

\[
22T = 10,000 \;\Rightarrow\; T = \frac{10,000}{22} \approx 455\text{ users}
\]

Breakdown:

* Starter: 0.60 × 455 ≈ **273** users  
* Professional: 0.30 × 455 ≈ **137** users  
* Enterprise: 0.10 × 455 ≈ **45** users  

Thus, acquiring **≈ 455 paying active users** (with the assumed tier distribution) will push MRR to $10 K, comfortably above the 10‑user breakeven point.

---

### Quick Reference Summary

| Metric | Value |
|--------|-------|
| Variable cost / active user | $1.12/mo |
| Fixed overhead | $193/mo |
| Weighted ARPU | $22/mo |
| Break‑even users | **≈ 10** |
| CAC range | $15 – $35 |
| LTV (avg) | $440 |
| Users for $10 K MRR | **≈ 455** (273 Starter, 137 Pro, 45 Ent) |

These numbers give a concrete financial foundation for launching **agent‑enhance** and scaling toward sustainable profitability.