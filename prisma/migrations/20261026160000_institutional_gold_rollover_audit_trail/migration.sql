-- CreateTable
CREATE TABLE "BrokerConnection" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "portfolioId" TEXT,
    "brokerName" TEXT NOT NULL DEFAULT 'IBKR',
    "flexQueryTokenEncrypted" TEXT NOT NULL,
    "flexQueryId" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'CONNECTED',
    "lastSyncedAt" DATETIME,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "BrokerConnection_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "gold_transactions" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "portfolioId" TEXT NOT NULL,
    "date" TEXT NOT NULL,
    "symbol" TEXT NOT NULL,
    "assetSubclass" TEXT NOT NULL,
    "weight" TEXT NOT NULL,
    "weightUnit" TEXT NOT NULL,
    "purity" TEXT NOT NULL,
    "spotPricePerUnit" TEXT NOT NULL,
    "premiumPerUnit" TEXT NOT NULL,
    "commission" TEXT NOT NULL,
    "totalCost" TEXT NOT NULL,
    "fxRateAtPurchase" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "gold_transactions_portfolioId_fkey" FOREIGN KEY ("portfolioId") REFERENCES "Portfolio" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "derivatives_contract_extensions" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "transactionId" TEXT NOT NULL,
    "contractMonth" TEXT NOT NULL,
    "expirationDate" TEXT NOT NULL,
    "legAction" TEXT NOT NULL DEFAULT 'OPEN_LONG',
    "isRollover" BOOLEAN NOT NULL DEFAULT false,
    "rolloverGroupId" TEXT,
    "rolloverSpread" TEXT,
    "rolloverFee" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "derivatives_contract_extensions_transactionId_fkey" FOREIGN KEY ("transactionId") REFERENCES "gold_transactions" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "audit_logs" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "action" TEXT NOT NULL,
    "entityType" TEXT NOT NULL,
    "entityId" TEXT NOT NULL,
    "beforeState" TEXT,
    "afterState" TEXT,
    "ipAddress" TEXT,
    "timestamp" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_ChatSession" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "messages" TEXT NOT NULL DEFAULT '[]',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "ChatSession_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "new_ChatSession" ("createdAt", "id", "messages", "updatedAt", "userId") SELECT "createdAt", "id", "messages", "updatedAt", "userId" FROM "ChatSession";
DROP TABLE "ChatSession";
ALTER TABLE "new_ChatSession" RENAME TO "ChatSession";
CREATE INDEX "ChatSession_userId_idx" ON "ChatSession"("userId");
CREATE TABLE "new_FireGoal" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "targetAmount" TEXT NOT NULL,
    "currentAmount" TEXT NOT NULL,
    "monthlyContribution" TEXT NOT NULL,
    "expectedReturn" TEXT NOT NULL,
    "inflationRate" TEXT NOT NULL,
    "targetYear" INTEGER NOT NULL,
    "currentAge" INTEGER NOT NULL,
    "retirementAge" INTEGER NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "FireGoal_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "new_FireGoal" ("createdAt", "currentAge", "currentAmount", "expectedReturn", "id", "inflationRate", "monthlyContribution", "name", "retirementAge", "targetAmount", "targetYear", "updatedAt", "userId") SELECT "createdAt", "currentAge", "currentAmount", "expectedReturn", "id", "inflationRate", "monthlyContribution", "name", "retirementAge", "targetAmount", "targetYear", "updatedAt", "userId" FROM "FireGoal";
DROP TABLE "FireGoal";
ALTER TABLE "new_FireGoal" RENAME TO "FireGoal";
CREATE INDEX "FireGoal_userId_idx" ON "FireGoal"("userId");
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;

-- CreateIndex
CREATE INDEX "BrokerConnection_userId_idx" ON "BrokerConnection"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "BrokerConnection_userId_brokerName_key" ON "BrokerConnection"("userId", "brokerName");

-- CreateIndex
CREATE INDEX "gold_transactions_portfolioId_date_idx" ON "gold_transactions"("portfolioId", "date");

-- CreateIndex
CREATE INDEX "gold_transactions_portfolioId_symbol_idx" ON "gold_transactions"("portfolioId", "symbol");

-- CreateIndex
CREATE UNIQUE INDEX "derivatives_contract_extensions_transactionId_key" ON "derivatives_contract_extensions"("transactionId");

-- CreateIndex
CREATE INDEX "derivatives_contract_extensions_rolloverGroupId_idx" ON "derivatives_contract_extensions"("rolloverGroupId");

-- CreateIndex
CREATE INDEX "derivatives_contract_extensions_expirationDate_idx" ON "derivatives_contract_extensions"("expirationDate");

-- CreateIndex
CREATE INDEX "audit_logs_userId_timestamp_idx" ON "audit_logs"("userId", "timestamp");

-- CreateIndex
CREATE INDEX "audit_logs_entityType_entityId_idx" ON "audit_logs"("entityType", "entityId");

