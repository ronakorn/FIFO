# FIFO Wealth OS API — SQLite/Prisma compatible production image
FROM node:20-bookworm-slim AS builder

WORKDIR /app
RUN apt-get update -y && apt-get install -y --no-install-recommends openssl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json ./
COPY prisma ./prisma/
RUN npm ci
RUN npx prisma generate

COPY tsconfig.json ./
COPY assets ./assets/
COPY src ./src/
RUN npm run build

FROM node:20-bookworm-slim AS runner
WORKDIR /app
ENV NODE_ENV=production \
    PORT=3000 \
    DATABASE_URL=file:/app/data/fifo_wealth_os.db \
    STORAGE_DIR=/app/storage/uploads \
    REPORTS_STORAGE_DIR=/app/storage/reports

RUN apt-get update -y && apt-get install -y --no-install-recommends openssl ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/package.json /app/package-lock.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/assets ./assets
COPY --from=builder /app/dist ./dist
RUN mkdir -p /app/data /app/docs /app/storage/uploads /app/storage/reports \
    && chown -R node:node /app/data /app/docs /app/storage

USER node
EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=5 \
  CMD curl -fsS http://127.0.0.1:3000/api/health || exit 1

# The Prisma schema and checked-in migrations both target SQLite. The named data volume
# is the durable database store; do not change providers without a migration project.
CMD ["sh", "-c", "./node_modules/.bin/prisma migrate deploy && node dist/api/server.js"]
