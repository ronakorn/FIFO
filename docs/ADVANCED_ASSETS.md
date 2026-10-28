# Advanced Assets — Phase 2

Advanced assets are implemented as an additive extension layer. The original base transaction and existing extension interfaces remain unchanged. The only added Core asset class is `FUTURES`; the existing exhaustive asset-class registry has the corresponding additive display/config entry so the TypeScript mapping stays complete. Advanced-only fields are declared in `src/types/advancedAssets.ts` and are not added to `MultiAssetTransaction`.

## Scope and data handling

The dashboard presents clearly marked illustrative scenarios. These calculators do not create or persist advanced holdings in the Core ledger. APIs require a valid JWT but do not require portfolio IDs because they calculate from the request payload only. No market-data feed is implied; callers must supply market and fund inputs.

## Numerical conventions

- Financial calculations use isolated `decimal.js` clones configured to precision 40 and `ROUND_HALF_UP`.
- Monetary/rate inputs are decimal strings. Count and contract-size inputs may be numbers or decimal strings where shown in the API schema; they are converted to Decimal before financial arithmetic.
- Results are returned as strings with documented display precision.
- UI chart coordinates are converted to JavaScript numbers only after Decimal calculations, for SVG/chart rendering.

## Options

`src/services/optionsEngine.ts` implements European Black–Scholes price and annualized Greeks using the Abramowitz–Stegun 26.2.17 normal-CDF approximation.

- Time to expiry is in years; rates and volatility are annualized decimals (`0.05` = 5%).
- `theta` is per year. `vega` is the price derivative per `1.00` volatility change and `rho` per `1.00` rate change; divide by 100 for a one-percentage-point move.
- Implied volatility uses Newton–Raphson with a safeguarded volatility bracket/bisection fallback and no-arbitrage input checks.
- Expiry payoff is long-option net payoff: `(intrinsic value − premium) × contractSize`.
- Verified reference: S=K=100, T=0.25, r=0.05, σ=0.20 gives a call near **4.6150**. The earlier 3.99 illustrative value is not Black–Scholes-consistent and is intentionally not copied.

Authenticated endpoints:

- `POST /api/advanced-assets/options/pricing`
- `POST /api/advanced-assets/options/implied-volatility`
- `POST /api/advanced-assets/options/payoff`

## REITs

`src/services/reitsEngine.ts` calculates premium/discount to NAV, annual distribution yield, FFO/AFFO and an estimated schedule.

- Premium/discount = `(market price − NAV) / NAV`.
- Distribution yield = annual distribution per unit / market price.
- The requested `capRate` field is labeled and documented as **distribution / NAV proxy** only; it is not a property-level capitalization rate.
- If maintenance capex is omitted, AFFO uses a disclosed 10% of FFO proxy. Supply fund-reported capex when available.
- Schedule amounts are annualized estimates; actual payment dates are returned empty until supplied by an authoritative fund notice.

Authenticated endpoints:

- `POST /api/advanced-assets/reits/valuation`
- `POST /api/advanced-assets/reits/distribution-schedule`

## Private Equity

`src/services/privateEquityEngine.ts` uses dated XIRR cash flows with an actual/365 day count, Newton–Raphson and a bracketed fallback. XIRR requires at least one negative and one positive cash flow; multiple/ill-conditioned roots are reported instead of silently guessing.

- TVPI = `(distributions + residual value) / invested capital`.
- DPI = distributions / invested capital.
- RVPI = residual value / invested capital.
- MOIC = total value / invested capital.
- J-curve points are chronologically sorted cumulative net cash flows. IRR is `0.000000` while a prefix lacks both cash-flow signs.

Authenticated endpoints:

- `POST /api/advanced-assets/private-equity/irr`
- `POST /api/advanced-assets/private-equity/metrics`
- `POST /api/advanced-assets/private-equity/j-curve`

## Futures

`src/services/futuresRiskEngine.ts` supports linear-contract mark-to-market, account margin health and a simplified liquidation level.

- `qty` is the number of contracts; initial and maintenance margin inputs are **per contract**.
- MTM = side × qty × contract size × multiplier × (mark − entry).
- Account equity = balance + aggregate unrealized P/L; margins are multiplied by contract count.
- Margin bands: below 100% = `MARGIN_CALL`; 100–120% = `DANGER`; 120–200% = `WARNING`; at least 200% = `HEALTHY`.
- Liquidation price assumes per-contract margin cushion, no fees/funding/slippage, and a linear contract: `entry ± (initial − maintenance) / (contractSize × multiplier)`. Quantity cancels because both position P/L and per-position margin scale with contract count. This is an estimate, not a broker liquidation price.

Authenticated endpoints:

- `POST /api/advanced-assets/futures/margin-health`
- `POST /api/advanced-assets/futures/mark-to-market`
- `POST /api/advanced-assets/futures/liquidation-price`

## Dashboards and screenshots

The localized route is `/[locale]/advanced-assets`, reachable from the sidebar. The four tabs are Options, REITs, Private Equity and Futures. Sample holdings are labeled illustrative and no values are represented as live prices.

- `screenshots/68-options-dashboard-with-greeks.png`
- `screenshots/69-reits-distribution-yield.png`
- `screenshots/70-private-equity-j-curve.png`
- `screenshots/71-futures-margin-health-gauge.png`

## Phase B Part 2 views

The existing four top-level tabs now retain their dashboards and expose a second view where applicable:

- **Options Chain:** AAPL and SPY use a dated, explicitly illustrative model chain with five strikes per expiry and three expiries. The authenticated `POST /api/advanced-assets/options/chain` endpoint validates the symbol/date and recalculates the sample using the options engine; it is not a market-data feed. The UI displays call/put bid and ask, IV, delta and moneyness, and supports a selected-strike payoff chart.
- **REIT Peer Comparison:** WHART, CPNREIT, FTREIT, SIRI and LHHOTEL are sample profiles with property type, distribution yield, price/NAV, occupancy and market-cap assumptions. The view charts selected yields, enforces a five-peer limit and exports CSV. SIRI is labeled an illustrative residential peer, not asserted to be a REIT.
- **PE Fund Screener:** five illustrative funds can be filtered by stage, inclusive vintage range (2020–2026), IRR and TVPI, sorted by IRR or TVPI, and opened in a detail modal showing the dated cash-flow J-curve and timeline.

The UI converts Decimal results to native numbers only at chart-rendering boundaries. Sample prices, fund returns, cash flows and REIT statistics are not live or verified, are not investment advice and are not persisted as holdings.

Screenshots for the current launch checklist:

- `screenshots/72-options-chain-visualization.png` — captured from the built app at 1920px desktop width.
- `screenshots/73-reits-peer-comparison.png` — captured from the built app at 1920px desktop width.
- `screenshots/74-pe-fund-screener.png` — captured from the built app at 1920px desktop width.
- `screenshots/75-docker-compose-running.png` — pending; Docker/Compose is unavailable in this sandbox, so no running-container screenshot is claimed.
- `screenshots/76-launch-checklist.png` — browser rendering of the current checklist.

The earlier visual details and Futures shots remain available as `screenshots/75-pe-fund-details.png` and `screenshots/76-futures-risk-monitor.png` for design review.
