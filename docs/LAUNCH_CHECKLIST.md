# FIFO Wealth OS Launch Checklist

**Sandbox verification (2026-10-27):** `npm audit --audit-level=high` found 0 vulnerabilities in both root and web packages; backend Jest **369/369 passed**; frontend typecheck, lint, production build, and Playwright **9/9 passed**. Screenshots `72`–`74` and `76` are available. Screenshot `75-docker-compose-running.png` and runtime/persistence checks remain pending because Docker/Compose is not installed here.

**Database provider:** this release keeps the existing SQLite Prisma schema and migrations (Zero Core Rewrite). The PostgreSQL Compose example is intentionally not used; a provider conversion needs a separately authorized schema/migration/data-migration plan.

## ✅ Pre-Launch (Technical)

- [x] Security audit passed: 0 reported vulnerabilities at high severity or above (root + frontend).
- [x] All backend tests passing: 369/369 (350+ acceptance target met).
- [x] Production builds successful: backend TypeScript build and Next.js frontend build.
- [x] Frontend typecheck, lint, and Playwright smoke tests passed (9/9).
- [ ] SQLite migrations applied on the target Docker host and database volume verified.
- [ ] Production environment variables configured: unique `JWT_SECRET` and separate `ENCRYPTION_KEY` (32+ characters); no sample placeholders.
- [ ] Docker containers running and health checks passing on a Docker-enabled host.
- [ ] SQLite data persists across container recreation; backup and restore tested.
- [ ] SSL/TLS certificates installed for production.
- [ ] Rate limiting, CORS policy, and error logging reviewed for the production audience.
- [ ] Performance monitoring and alert routing configured.
- [x] Feature screenshots `72`–`74` captured and reviewed.
- [ ] `75-docker-compose-running.png` captured from a successfully running Compose stack.
- [x] `76-launch-checklist.png` captured from the current checklist.

## Pre-Launch (Content)

- [ ] Landing page reviewed and ready for public traffic.
- [ ] User guide/documentation complete.
- [x] API documentation (OpenAPI/Swagger) updated for the options-chain endpoint.
- [ ] Privacy policy published and reviewed for Thai PDPA requirements.
- [ ] Terms of service published.
- [ ] FAQ page created.
- [ ] Tutorial videos recorded (3–5 videos).

## Pre-Launch (Marketing)

- [ ] Social media accounts created.
- [x] Launch announcement draft prepared in `docs/PHASE_B_PART_2_ANNOUNCEMENT.md` (publish only after the technical release gate).
- [ ] Beta-user email list confirmed.
- [ ] Press release drafted.
- [ ] Partnership proposals sent (Bitkub, Dime, SET, Bloomberg). No partner/API connection is implied by this checklist.

## Launch Day

- [ ] Monitor server performance and disk space.
- [ ] Monitor application and container logs.
- [ ] Respond to user feedback and route incidents to the on-call owner.
- [ ] Track key metrics (signups, active users, retention).

## Post-Launch (Week 1)

- [ ] Collect user feedback.
- [ ] Fix critical bugs.
- [ ] Send weekly newsletter.
- [ ] Publish first blog post.
- [ ] Engage with the community.

## Post-Launch (Month 1)

- [ ] Analyze user behavior.
- [ ] Identify the most requested features.
- [ ] Plan Phase 3 development.
- [ ] Evaluate partnership opportunities.

## Operations / Release record

- [ ] Execute `scripts/deploy.sh` on the target host after configuring `.env`.
- [ ] Record the release commit, SQLite migration state, test totals, deployment operator, backup location, and rollback plan.
- [ ] Keep Stripe on the mock adapter until a separately approved integration and webhook verification plan is complete.
- [ ] Keep option-chain, REIT and PE sample data labeled illustrative/not live; do not imply advanced-asset order execution.
