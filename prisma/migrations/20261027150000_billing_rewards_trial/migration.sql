-- Billing-only entitlements. Money remains a Decimal.js precision-40 string in Donation.amountTHB.
ALTER TABLE "User" ADD COLUMN "earlyBirdClaimedAt" DATETIME;
ALTER TABLE "User" ADD COLUMN "earlyBirdDiscountPercent" INTEGER;
ALTER TABLE "User" ADD COLUMN "earlyBirdCanceledAt" DATETIME;
ALTER TABLE "User" ADD COLUMN "proTrialRequestedAt" DATETIME;
ALTER TABLE "User" ADD COLUMN "proTrialDurationDays" INTEGER;
ALTER TABLE "User" ADD COLUMN "proYearRewardQualifiedAt" DATETIME;
