#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. Install Docker Engine and the Compose v2 plugin." >&2
  exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required (docker compose)." >&2
  exit 1
fi
if [[ ! -f .env ]]; then
  echo "Missing .env. Copy .env.example to .env and set unique JWT_SECRET and ENCRYPTION_KEY values first." >&2
  exit 1
fi

jwt_secret="$(sed -n 's/^JWT_SECRET[[:space:]]*=[[:space:]]*//p' .env | head -n 1 | tr -d '\"' | tr -d "'")"
if [[ -z "$jwt_secret" || "$jwt_secret" == *replace-with-strong* || "$jwt_secret" == *change-this* ]]; then
  echo "JWT_SECRET is empty or still the sample placeholder. Set a unique secret (for example: openssl rand -base64 48)." >&2
  exit 1
fi

encryption_key="$(sed -n 's/^ENCRYPTION_KEY[[:space:]]*=[[:space:]]*//p' .env | head -n 1 | tr -d '\"' | tr -d "'")"
if [[ ${#encryption_key} -lt 32 || "$encryption_key" == *replace-with-* ]]; then
  echo "ENCRYPTION_KEY is missing, shorter than 32 characters, or still a placeholder. Generate a separate key (for example: openssl rand -hex 32)." >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to run the backend and frontend security audits." >&2
  exit 1
fi

echo "Running backend security audit..."
npm audit --audit-level=high
echo "Running frontend security audit..."
npm --prefix fifo-wealth-os-web audit --audit-level=high

# Compose configuration validation catches interpolation and YAML errors before a build.
docker compose config --quiet
docker compose build --pull
docker compose up --detach --remove-orphans
"$ROOT_DIR/scripts/healthcheck.sh"
docker compose ps
