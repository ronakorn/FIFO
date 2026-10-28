CREATE TABLE "multi_asset_transactions" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "portfolioId" TEXT NOT NULL,
    "date" TEXT NOT NULL,
    "assetClass" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "symbol" TEXT NOT NULL,
    "payload" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "multi_asset_transactions_portfolioId_fkey"
      FOREIGN KEY ("portfolioId") REFERENCES "Portfolio" ("id")
      ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX "multi_asset_transactions_portfolioId_date_idx"
  ON "multi_asset_transactions"("portfolioId", "date");
CREATE INDEX "multi_asset_transactions_portfolioId_assetClass_idx"
  ON "multi_asset_transactions"("portfolioId", "assetClass");
CREATE INDEX "multi_asset_transactions_portfolioId_symbol_idx"
  ON "multi_asset_transactions"("portfolioId", "symbol");
