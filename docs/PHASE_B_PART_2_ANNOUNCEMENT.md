# FIFO Wealth OS — Advanced Assets update

**Phase B Part 2 is ready for review.** The Advanced Assets workspace now brings several research views together while keeping the Core portfolio ledger and existing risk engines intact.

### What’s new

- **Options Chain:** illustrative AAPL and SPY scenarios with five strikes across three expiries, call/put bid and ask, implied volatility, delta, ITM/ATM/OTM states, refresh controls, strike selection, and a long-option expiry payoff profile.
- **REIT Peer Comparison:** WHART, CPNREIT, FTREIT, SIRI and LHHOTEL sample profiles, yield chart, price/NAV, occupancy and market capitalization; add or remove up to five peers and export the selected set to CSV.
- **Private Equity Fund Screener:** five sample funds filterable by stage, vintage (2020–2026), IRR and TVPI; sort by either performance measure and open a fund detail view with a J-curve and dated cash-flow timeline.
- **Four-tab workspace:** Options, REITs, Private Equity and Futures remain in one Advanced Assets area, with existing options, income, PE and futures dashboards retained.

### Important data notice

This is an analytical and educational preview. The option chain, REIT figures, fund names, returns, cash flows and AUM are illustrative scenarios—not live quotes, verified issuer disclosures, fund records, investment recommendations or executable prices. Refresh recalculates the dated sample model; it does not connect to an exchange feed. The workspace does not submit orders or write advanced-asset trades to portfolio holdings. Validate market, issuer and fund information independently before making decisions.

The Compose deployment continues to use the repository’s SQLite Prisma schema and migration history. PostgreSQL is not enabled by this release. See `docs/DEPLOYMENT_SQLITE.md` for deployment and backup guidance.

**Status:** preview/review build. Public launch should wait until the checklist in `docs/LAUNCH_CHECKLIST.md` is completed, including Docker validation on a Docker-enabled host and the target test suite.
