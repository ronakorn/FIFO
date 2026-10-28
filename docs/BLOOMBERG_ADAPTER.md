# Bloomberg export adapter

## Scope and truthful integration status

This adapter imports **user-exported Bloomberg files**; it is not a direct Bloomberg Terminal or Port connection and does not claim an official Bloomberg partnership. The Port class is an explicit sandbox stub that returns empty arrays. Live Port calls fail closed unless a separately reviewed transport is injected. No Bloomberg credentials are accepted or stored by this implementation.

Trade uploads are authenticated, portfolio-owned, idempotent imports into the existing Multi-Asset CDM. The original upload file is held in memory only and is not retained. Corporate actions are parsed for review only; they are not persisted or applied to lots.

## File formats

- CSV, TSV, and Excel `.xlsx`, up to 10 MB.
- Legacy binary `.xls` is not supported; save it as `.xlsx` or CSV first.
- For `.xlsx`, the first worksheet is read. Excel date serials in columns with a `date` header are normalized to ISO dates.
- CSV headers may include introductory rows above the actual header. The importer searches for the header row.

### Trade columns

Required for all trades: `Ticker` (or `Bloomberg Ticker`/`Security`), `Trade Date`, `Side`, `Quantity`, `Price`, and `Currency` (currency pairs may be inferred from a valid `Curncy` ticker). `Gross Amount`, `Commission`, `Taxes`, `Net Amount`, `Settlement Date`, `Exchange`, and security identifiers are optional where a documented mapping exists.

For foreign-currency trades, include `FX Rate to THB` (or `FX Rate To Base`). The importer deliberately does not apply synthetic fallback FX rates. Portfolio valuation engines currently require a THB-base portfolio.

Asset-specific fields:

- **Fixed income** (`Corp`, `Govt`, `Mortgage`, `Muni`): `Coupon Rate`, `Payment Frequency`, `Maturity Date`, `Face Value`; optional `Accrued Interest`, `YTM`, `Credit Rating`, `Issuer`. The adapter maps face value and accrued interest into the CDM's THB fields using the provided FX rate when required.
- **Commodities** (`Comdty`): `Weight Per Unit` (or `Weight`), `Weight Unit`, and optionally `Purity`, `Spot Price Per Unit`, `Storage Fee THB`, and `Premium THB`.
- **Options and warrants** (`Option`, `Warrant`): `Option Type`, `Strike Price`, `Expiration Date`, `Underlying Asset`; optional `Contract Size` and `Option Premium`.
- **FX pairs** (`Curncy`): use a six-letter pair such as `EURUSD Curncy` (or explicit `Base Currency` and `Quote Currency`). `Quantity` is units of the pair's base currency, and `Price` is quote currency per base unit. Pair buys are normalized into the CDM's source-to-target `CONVERT` convention.

## Bloomberg yellow-key mapping

| Bloomberg suffix | Existing CDM class | Import status |
| --- | --- | --- |
| `Equity`, `Pfd`, `Index` | `EQUITY` | Supported; `Index` is an equity-like record and is not independently valued by the current CDM |
| `Corp`, `Govt`, `Mortgage`, `Muni` | `BOND` | Supported when required bond terms are present |
| `Curncy` | `FOREX` | Supported as a currency conversion |
| `Comdty` | `COMMODITY` | Supported when weight and unit are present |
| `Option`, `Warrant` | `OPTION` | Supported when option terms are present |
| `Future` | nearest family shown as `OPTION` for classification | **Rejected**: the protected Core CDM has no Futures contract type; it is not stored as an option |

All financial arithmetic uses a Decimal.js clone configured at precision 40. Financial values are serialized as decimal strings as required by the current CDM. Quantity remains a number because the protected CDM defines `qty` as a JavaScript number.

## Authenticated endpoints

- `POST /api/upload/bloomberg-trades` — multipart `file` plus `portfolioId`, or JSON `portfolioId` and `csvContent`. Persists CDM trades after ownership, FX, duplicate, and supported-engine ledger checks.
- `POST /api/upload/bloomberg-corporate-actions` — multipart `file` or JSON `csvContent`. Returns a preview only.
- `POST /api/bloomberg/tickers/parse` — parses one yellow-key ticker.
- `POST /api/connect/bloomberg-port` — authenticated `SANDBOX` empty mock; `LIVE` responds with `501 BLOOMBERG_PORT_LIVE_NOT_CONFIGURED`.

Trade IDs are converted into deterministic SHA-256-derived IDs for repeat-import deduplication. Account numbers and broker credentials are not written into CDM transaction payloads.
