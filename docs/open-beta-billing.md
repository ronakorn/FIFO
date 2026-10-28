# Open Beta Billing, Pricing & Support

## Current launch behavior

- `OPEN_BETA_MODE=true` bypasses every feature and usage-limit gate before a database lookup. An unset value is also the safe Open Beta default; set it explicitly to `false` only when subscription gating is approved.
- `GET /api/billing/status` is public during beta and returns `BETA_ALL_ACCESS` / `ALL_FEATURES`, the entitlement map, published pricing, Early-Bird terms, and `chargesEnabled: false`.
- `GET /api/billing/pricing` is public, read-only, and returns the approved catalog. If a JWT is supplied, the response also reflects that account's saved Early-Bird claim and cancellation state.
- Subscription Checkout is intentionally not exposed. No subscription charges are collected during Open Beta; the Billing UI disables upgrades and the Pro trial button only records a deferred reservation.
- Donations require an authenticated account so a contribution is associated with `Donation.userId`. The current adapter creates mock Checkout/Payment Intent identifiers only and never charges a card.
- Mock webhook signatures use a local HMAC format. They are not Stripe signatures and must not be used as a live Stripe verifier.

## Approved subscription catalog

`src/config/pricing.ts` is the source of truth. Amounts are THB per month/per year, and billing calculations use Decimal.js precision 40.

| Tier | Monthly | Yearly | Entitlements |
|---|---:|---:|---|
| FREE | ฿0 | ฿0 | 1 portfolio, 50 transactions per year, CSV upload, basic net-worth view |
| PRO | ฿290 | ฿2,784 | Unlimited portfolios/transactions, PDF tax report, advanced analytics, FIRE planner, AI assistant, audit trail, priority support |
| FAMILY | ฿590 | ฿5,664 | Pro features, family wealth, up to 3 family members |
| ADVISOR | ฿1,990 | ฿19,104 | Pro features, family wealth (up to 3 members), white label, client management, up to 30 clients |

Annual prices are 20% below twelve monthly payments. Stripe Price IDs are placeholders (`price_pro_monthly`, etc.) and must be replaced before a real provider adapter is enabled.

## Early-Bird and donor rewards

- Beta Users may claim a 30% Early-Bird discount through **June 30, 2027** (inclusive, Bangkok calendar date). Exact Pro monthly math is `฿290 × 0.7 = ฿203.00`.
- Claim state is stored on `User`. The discount lasts for the active subscription and is permanently marked ended when that subscription is canceled; a used claim cannot be reclaimed. A claim does not start checkout or create a charge.
- A separate donor reward is granted automatically once a user's `SUCCEEDED` donations total at least **฿2,784**. The one-year Pro reward is queued and starts only when subscriptions open; it is not an Early-Bird claim and does not require a manual claim.
- Community fundraising displays the fixed **฿127,450** baseline plus only `Donation` records whose status is `SUCCEEDED`, against the **฿500,000** goal. All amounts remain precision-40 Decimal.js calculations and are persisted/read as decimal strings.
- Free→Pro trial requests reserve a **14-day** trial. It begins when subscriptions open. During Open Beta the request is stored only; there is no subscription Checkout or charge.

## Feature gates

The boolean feature-to-tier map and plan limits are declared in `src/config/pricing.ts`. `src/middleware/subscriptionGuard.ts` resolves feature requirements from this mapping. The app applies it to advanced analytics, FIRE, AI, family wealth, audit trail, and PDF tax reports. Free portfolio and annual transaction quotas are checked on portfolio creation and transaction intake/sync; the three-member family cap is checked when joining a family group. The 30-client Advisor limit is defined in the catalog and should be enforced when an Advisor client-management endpoint is introduced. Open Beta bypasses every feature and quota gate; the annual tax-summary JSON remains available as a core feature.

- `-1` represents an unlimited numeric limit.
- `OPEN_BETA_MODE=true` (or unset) bypasses gates to preserve current all-access behavior.
- `User.isBetaAllAccess` and `Subscription.isBetaAllAccess` remain independent account-level beta overrides.

## API contract

- `POST /api/donate/create` — JWT-protected; accepts `amountTHB` as a decimal string and an optional message (maximum 280 characters). Amount bounds are ฿10–฿1,000,000 with at most two decimal places.
- `GET /api/billing/community` — public fundraising summary: baseline + succeeded donation strings, target, remaining amount, and progress.
- `GET /api/billing/pricing` — public read-only pricing; optional JWT adds personalized Early-Bird claim state. `chargesEnabled` is always false.
- `GET /api/billing/status` — public `BETA_ALL_ACCESS` response while Open Beta is enabled; JWT-protected account status after beta is disabled.
- `GET /api/billing/early-bird/status` — JWT-protected Early-Bird, donor reward, and trial reservation status.
- `POST /api/billing/early-bird/claim` — JWT-protected, Beta User-only one-time claim; no checkout.
- `POST /api/billing/trial/reserve` — JWT-protected idempotent reservation for a 14-day trial at subscription launch; no checkout.
- `POST /api/billing/portal` — JWT-protected mock Customer Portal session.
- `POST /api/webhooks/stripe` — signed mock webhook endpoint; successful donation events update the reward qualification and subscription lifecycle events end an active Early-Bird discount when canceled.

## Post-beta activation checklist

1. Replace every placeholder Stripe Price ID with approved provider IDs and configure the real sales contact used by the Advisor CTA.
2. Replace `MockStripeService` with a real Stripe SDK adapter; use a secret manager, exact raw-body signature verification, and provider idempotency keys.
3. Implement the approved launch operation that starts queued donor Pro-year rewards and 14-day trial reservations only after subscriptions are officially open.
4. Add real subscription Checkout/lifecycle flows and update status persistence only after provider integration, entitlements, and authenticated end-to-end tests are deployed.
5. Keep `chargesEnabled` false until that release is complete. Do not use local mock webhook signatures in production.

The SQLite migration is additive. Both the SQLite Prisma schema and production PostgreSQL schema contain the account-level claim, cancellation, deferred trial, and donor qualification fields.
