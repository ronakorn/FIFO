# FIFO Wealth OS — System-wide Health Check

**Date:** 28 October 2026 (Asia/Bangkok)  
**Scope:** Core/backend (`/home/user`) and Next.js frontend (`/home/user/fifo-wealth-os-web`)  
**Overall result:** **89/100 — Green, with maintainability follow-ups**  

> This is a heuristic engineering-health score for the audited scope, not a financial-model certification, security audit, or production-operations sign-off. No critical business formulas, database choices, or application architecture were changed.

## Executive summary

- Core and frontend typechecks, strict unused-symbol checks, frontend lint, all 28 backend Jest suites (**369 tests**), all 14 frontend Playwright tests, and the Next.js 15.5.28 production build passed.
- The browser smoke check loaded **23 routes with HTTP 200**, including English and Thai routes and a dynamic portfolio/tax route. The root path resolved to `/th`. No page exceptions, console errors, HTTP errors, or non-aborted failed requests occurred during navigation-only smoke checks.
- Static review confirmed **zero actionable dead buttons, zero broken static internal links, and zero unmatched frontend API calls**. A single no-handler heuristic candidate was a functioning Radix `DialogTrigger`.
- API failure, 30-second client timeout, empty and boundary inputs, invalid PE filter ranges, an empty result set, and rapid repeat submission were exercised. The UI recovered gracefully in each tested case.
- Main residual concern is maintainability: complexity/large-function scans flag existing UI and finance/import functions. No automatic refactoring was made because several findings touch business-critical calculations or integration flows.

## 1. Code health, unused code, formatting, and complexity

### Cleanup applied

- Removed unused imports, variables, and a redundant local computation from the previously identified frontend and core files.
- Deleted two unreferenced frontend barrels: `src/components/analytics/index.ts` and `src/components/fire/index.ts`.
- Renamed intentionally unused Express request parameters to `_req`.
- Kept all formula/precision behavior, including Decimal.js precision 40 with `ROUND_HALF_UP`, unchanged.
- Both code roots pass `tsc --noEmit --noUnusedLocals --noUnusedParameters`. Frontend lint reports no ESLint warnings or errors.

### Formatting review

- A whitespace scan over 119 source/config files found **0 trailing-whitespace lines, 0 indentation-tab lines, and 0 CRLF files**.
- The project has no Prettier configuration or format script. A read-only Prettier 3.5.3 check using its defaults flags **115 files**; because the default style is not an established repository standard, no repo-wide format rewrite was applied. Recommend agreeing a formatter/configuration before normalizing files.

### Complexity review

A review-only ESLint scan used `complexity > 15` and `max-lines-per-function > 120` thresholds; these rules are not currently enforced by the project's lint configuration.

- **Frontend:** 18 functions exceed the complexity threshold; 45 functions exceed 120 lines. Representative findings: `MultiAssetWorkspace` (complexity 70; 499 lines), `GoldSensitivityWorkspace` (complexity 33; 1,573 lines), and `BloombergUploader` (complexity 38; 422 lines).
- **Core:** 39 functions exceed the complexity threshold; 30 production functions exceed 120 lines (63 including tests). Representative findings: `extractRawIBKRDividendsSync` (complexity 46), `mapBloombergTradeToCDM` (43), `calculateFundPortfolio` (33), `runMonteCarloSimulation` (31), and `triggerManualSync` (30).
- These are maintainability signals, not lint failures. Refactoring finance, tax, FIFO, broker-sync, or import logic should be a separate developer-reviewed change with focused regression tests.

## 2. Buttons, links, routes, parameters, and API wiring

- Audited **144 literal `<button>` nodes**: **0 confirmed dead controls**. The one apparent missing-handler candidate is wrapped in Radix `DialogTrigger asChild` and works.
- Audited **50 `<Link>`/`<a>` elements with hrefs**. All **39 static internal references** match frontend route patterns; no actionable broken link was found.
- Audited **36 literal frontend API calls** against mounted backend routes and HTTP methods: **36/36 matched**.
- Browser smoke routes: **23/23 returned HTTP 200**. Root `/` resolved to `/th`; portfolio and tax dynamic paths loaded; upload paths with both valid-looking and unknown `portfolioId` query values loaded without client exceptions. This confirms route handling/no crash, not business-level validation of arbitrary IDs.
- Direct and frontend-proxied `GET /api/health` both returned **200**.

### Broken-link / dead-button findings

| Area | Finding | Fix |
|---|---|---|
| Buttons | 0 confirmed dead buttons; one heuristic false positive was a Radix dialog trigger | No product fix required |
| Internal links | 0 broken static internal links across the 39 checked references | No fix required |
| Frontend API calls | 0 unmatched methods/routes across 36 calls | No fix required |
| Redirect/route smoke | Root locale resolution and tested dynamic paths loaded successfully | No fix required |

## 3. Runtime, API failures, empty states, timeouts, and boundaries

- **Browser route smoke:** 23 routes; 0 page errors, 0 navigation console errors, 0 HTTP responses ≥400, and 0 non-aborted failed requests. Next.js link-prefetch requests canceled by subsequent navigations were excluded as expected `ERR_ABORTED` events.
- **Playwright:** **14/14 passed**. The 9 existing advanced-asset checks pass; 5 runtime-health checks were added for failure/timeout/fallback behavior, duplicate refreshes, filter boundaries/empty results, and required login fields.
- **503 API failure:** the options panel shows an accessible error, retains its five sample rows, and re-enables Refresh.
- **30-second API timeout:** Axios timeout was exercised with a deliberately stalled request; the fallback alert appeared, sample rows remained visible, and Refresh recovered.
- **Rapid submission:** a double-click during a delayed refresh produced **one request**.
- **Input boundaries:** blank PE range fields remain optional; IRR 0–100 and TVPI 0–5 boundaries retain results; 100–100 yields the designed empty-results state; minimum IRR above maximum produces an inline validation alert.
- **Empty login:** required email/password prevent submission; the test observed **zero API calls**.
- **Real unauthenticated endpoint:** `POST /api/advanced-assets/options/chain` returns **401** without a Bearer token, as required by the API tests. The preview UI catches it, preserves five sample rows, and tells the user to sign in. Chromium emits one generic “Failed to load resource” 401 console message for that expected HTTP rejection; there was no unhandled page exception.
- Backend API validation/authentication and edge cases are also covered by the passing 369-test Jest suite.

## Error and fix log

| Issue observed | Resolution / disposition | Final status |
|---|---|---|
| Two pre-existing E2E selectors did not match the actual accessible names (`Select strike`; `Min/Max IRR %` and `Min/Max TVPI`) | Corrected selectors in `e2e/tests/advancedAssets.spec.ts`; application UI was not changed | All 9 original browser tests pass |
| New failure-state assertions initially matched both the app alert and Next.js route-announcer alert | Scoped assertions to the application's `p[role="alert"]` | All 5 new runtime-health tests pass |
| Playwright browser binary was initially absent; the sandbox also lacked Chromium shared libraries | Installed the browser and temporary user-space libraries for this run only; no project dependency or lockfile changes | Playwright suite runs successfully |
| One production-build attempt was killed while the API/frontend servers were running | Stopped both servers, cleared generated `.next` output, and reran the production build | Final build passed |
| Unauthenticated model refresh returned 401 | Expected protected-endpoint behavior; UI displays the sign-in fallback and retains sample data | No product change; note the generic browser network console message |
| Next.js workspace-root warning and `next-intl` dynamic-import webpack cache warnings | Nonfatal; recorded for deployment/configuration review | Build still succeeds |

## Cleanup log

- Removed unused imports/locals and redundant computation in `error.tsx`, `FuturesRiskDashboard.tsx`, `OptionsDashboard.tsx`, `PEScreener.tsx`, `MultiAssetWorkspace.tsx`, `multiAsset.ts`, `forexEngine.ts`, and `advancedAssets.test.ts`.
- Deleted the two unused analytics/fire barrel files.
- Renamed unused Express request parameters in `advancedAssets.ts` and the Bloomberg ticker-parse handler.
- Updated the two incorrect test selectors and added `e2e/tests/runtimeHealth.spec.ts` with five targeted regressions.
- No pricing, tax, FIFO, investment, accounting, or data-persistence logic was altered.

## Manual recommendations / developer review

1. Review the high-complexity functions above in a dedicated change. Preserve current accounting and Decimal behavior; use smaller pure helpers plus domain regression tests rather than broad rewrites.
2. Decide and document a formatter configuration, then normalize files in a controlled formatting-only change. Do not use the current default Prettier style as an implicit project policy.
3. Resolve the multi-lockfile workspace-root warning deliberately (for example, set `outputFileTracingRoot` after deployment review); do not remove either lockfile without confirming the shared-source dependency setup.
4. Plan migration from deprecated `next lint` before upgrading past the current Next.js 15.5.28 baseline.
5. Run manual, credential-safe checks for real login/session expiry, CSV/XLSX import fixtures (empty, malformed, and large files), and broker/vendor sandbox integrations. Those external live integrations were not activated during this audit.
6. Add cross-browser/device, keyboard/accessibility, and production-like load/performance checks; this run used headless Chromium and route smoke tests, not a full accessibility or load audit.
