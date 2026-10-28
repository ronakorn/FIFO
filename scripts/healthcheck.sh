#!/usr/bin/env bash
set -Eeuo pipefail

API_HEALTH_URL="${API_HEALTH_URL:-http://127.0.0.1:${API_HOST_PORT:-3000}/api/health}"
WEB_HEALTH_URL="${WEB_HEALTH_URL:-http://127.0.0.1:${WEB_HOST_PORT:-3001}/en/advanced-assets}"
ATTEMPTS="${HEALTHCHECK_ATTEMPTS:-60}"
INTERVAL="${HEALTHCHECK_INTERVAL_SECONDS:-2}"

wait_for_url() {
  local url="$1"
  local label="$2"
  local attempt
  for ((attempt = 1; attempt <= ATTEMPTS; attempt++)); do
    if curl --fail --silent --show-error --max-time 5 "$url" >/dev/null 2>&1; then
      printf '%s is healthy: %s\n' "$label" "$url"
      return 0
    fi
    sleep "$INTERVAL"
  done
  printf 'Timed out waiting for %s: %s\n' "$label" "$url" >&2
  return 1
}

wait_for_url "$API_HEALTH_URL" "Backend API"
wait_for_url "$WEB_HEALTH_URL" "Web app"
