# SQLite deployment (Docker Compose)

## Provider compatibility and scope

The Core Prisma schema (`prisma/schema.prisma`) and checked-in migration history currently target **SQLite**. The Compose stack deliberately mounts a persistent SQLite database at `/app/data/fifo_wealth_os.db`; it does not run PostgreSQL. Do not point `DATABASE_URL` at PostgreSQL or adopt the incomplete `schema.postgresql.prisma` as a deployment schema. A provider change requires explicit authorization, a complete schema, reviewed provider-specific migrations, and a rehearsed data migration/rollback plan.

This is a single-host deployment suitable for a small beta. SQLite is not a multi-writer database service; plan an approved database migration before scaling to multiple API replicas or write-heavy workloads.

## Prerequisites

- Docker Engine with the Docker Compose v2 plugin (`docker compose`).
- A host with persistent storage and a TLS reverse proxy for public access.
- A unique, high-entropy JWT secret. Generate one with `openssl rand -base64 48`.

## First deployment

1. Copy `.env.example` to `.env`; set a unique `JWT_SECRET` (`openssl rand -base64 48`) and a separate `ENCRYPTION_KEY` of at least 32 characters (`openssl rand -hex 32`). Keep `.env` out of source control.
2. Review `OPEN_BETA_MODE` and the host/port values. The example binds ports `3000` and `3001` to loopback (`127.0.0.1`) so a reverse proxy can provide HTTPS. Set the bind addresses intentionally if direct access is required.
3. Run `./scripts/deploy.sh`. The script validates Compose interpolation, builds the API and web images, starts services, and waits for the API and localized web route health checks.
4. Put a TLS-terminating reverse proxy in front of the web app. Restrict direct access to the API port unless it is needed by trusted clients.

The backend runs `prisma migrate deploy` before starting. Its health endpoint is `GET /api/health`; the UI is served at `/en/advanced-assets` (and other localized routes). The frontend rewrites `/api/*` requests through the Compose network to `http://backend:3000`; browser code does not call a container hostname directly.

## Persistence and backup

- `fifo-wealth-os_fifo_sqlite_data` holds the SQLite database.
- `fifo-wealth-os_fifo_uploads_data` holds uploaded files and generated report storage.
- Back up both volumes before releases and before migration changes. Use a consistent, stopped-service copy or a SQLite-aware online backup; do not copy a live database file without a consistency strategy.
- Test restore into a separate stack before relying on a backup. Never use `docker compose down -v` for routine deploys; it deletes persistent volumes.

Example quiesced backup (run during a maintenance window from the repository root):

```bash
docker compose stop backend
mkdir -p backups
# Resolve actual Compose volume names with `docker volume ls`; these names include the project prefix.
docker run --rm -v fifo-wealth-os_fifo_sqlite_data:/source:ro -v "$PWD/backups:/backup" alpine:3.20 \
  sh -c 'tar -czf /backup/sqlite-data-$(date -u +%Y%m%dT%H%M%SZ).tgz -C /source .'
docker compose start backend
```

Back up `/app/storage` separately. Adjust volume names if Compose is invoked with a custom project name.

## Environment notes

- `.env.example` is a template only. `scripts/deploy.sh` rejects the included JWT placeholder.
- Compose sets the production SQLite URL to `file:/app/data/fifo_wealth_os.db`; the local development URL remains schema-relative (`file:./dev.db`).
- Stripe stays on the mock adapter. Do not provide live payment keys or announce payment processing as enabled.
- Options-chain, REIT and PE sample data are illustrative. No live market-data feed or order execution is configured.
- The Bloomberg Port adapter remains an empty mock until its API contract and approved authentication flow are verified.

## GitHub Actions

- `.github/workflows/ci.yml` runs backend typecheck/tests/build, web typecheck/lint/Playwright/build, and a Docker Compose config plus image build on GitHub-hosted runners.
- `.github/workflows/deploy.yml` is manual-only and is gated by the `production` GitHub Environment. Configure `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_DIR`, and preferably `DEPLOY_KNOWN_HOSTS`. The target must already have the repository checked out, Docker Compose v2, a persistent `.env`, and a working Git remote. Type `deploy` in the workflow confirmation input to update the selected workflow commit and run the deployment script.
- Protect the production environment with required reviewers and restrict which refs can deploy. Do not put the production `.env` or JWT secret in GitHub source files.

## Deployment verification

The repository's GitHub Actions CI runs typechecks, tests, frontend checks, Playwright smoke tests, and a Compose configuration/image build on GitHub-hosted runners. Local Docker validation must still be performed in the target environment before production; an unavailable Docker daemon in a development sandbox is not evidence that Compose started successfully.
