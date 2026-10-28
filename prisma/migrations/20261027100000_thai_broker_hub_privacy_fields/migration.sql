-- Thai Local Broker Hub, PDPA metadata, precise source-level purge provenance
-- and the previously db-pushed read-only CryptoWallet schema.

-- Alter broker connections to persist explicit connection/data-source mode and consent receipts.
ALTER TABLE "BrokerConnection" ADD COLUMN "connectionMode" TEXT NOT NULL DEFAULT 'READ_ONLY_API';
ALTER TABLE "BrokerConnection" ADD COLUMN "dataSource" TEXT;
ALTER TABLE "BrokerConnection" ADD COLUMN "pdpaConsentedAt" DATETIME;
ALTER TABLE "BrokerConnection" ADD COLUMN "pdpaConsentVersion" TEXT;

-- Preserve connector provenance so Right-to-be-Forgotten only purges records imported by that connector.
ALTER TABLE "Transaction" ADD COLUMN "sourceConnector" TEXT;
ALTER TABLE "Dividend" ADD COLUMN "sourceConnector" TEXT;

-- Cross-chain public-address wallet metadata. Address ciphertext is AES-256-GCM encrypted.
-- addressHash enables private uniqueness lookup and addressMasked is the display field.
CREATE TABLE "crypto_wallets" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "portfolioId" TEXT,
    "chain" TEXT NOT NULL,
    "address" TEXT NOT NULL,
    "addressHash" TEXT NOT NULL,
    "addressMasked" TEXT NOT NULL,
    "label" TEXT,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "lastSyncedAt" DATETIME,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "crypto_wallets_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "crypto_wallets_portfolioId_fkey" FOREIGN KEY ("portfolioId") REFERENCES "Portfolio" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE UNIQUE INDEX "crypto_wallets_userId_chain_addressHash_key"
    ON "crypto_wallets"("userId", "chain", "addressHash");
CREATE INDEX "crypto_wallets_userId_idx" ON "crypto_wallets"("userId");
CREATE INDEX "crypto_wallets_portfolioId_idx" ON "crypto_wallets"("portfolioId");
