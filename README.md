# PortfolioLens

PortfolioLens is a Streamlit micro-SaaS for portfolio analytics. It supports:
- Asset/index comparison using Yahoo Finance tickers.
- Portfolio upload via CSV (`ticker,weight`) with validation.
- Performance analytics (CAGR, Vol, Sharpe, Sortino, Max Drawdown, Calmar, Beta/Alpha).
- Rules-based recommendation engine with triggered rules and what-if estimates.
- SaaS scaffolding for authentication (Supabase), persistence (Postgres), and billing (Stripe).

## Architecture

```text
app/                # Streamlit multipage app
core/               # Pure-python analytics + recommendation engine
db/                 # SQLAlchemy models + Alembic migrations
services/           # FastAPI webhook service (Stripe events)
tests/              # Unit tests for core analytics
```

## Pages

1. **Home** (demo mode, no login required)
2. **Compare Assets** (tickers/date/frequency, metrics + charts)
3. **Upload Portfolio** (CSV weights, benchmark analytics)
4. **Recommendations** (rules-based recommendation engine + what-if)
5. **Saved Reports** (requires login)
6. **Billing** (Stripe billing portal link)

## Quickstart (local)

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

### 2) Run Postgres

Option A (Docker):
```bash
docker compose up -d postgres
```

Option B (local Postgres):
- Create DB `portfoliolens`
- Update `DATABASE_URL` in `.env`

### 3) Run migrations

```bash
./scripts/init_db.sh
```

### 4) Run app + webhook service

```bash
./scripts/run_streamlit.sh
./scripts/run_webhook.sh
```

- App: http://localhost:8501
- Webhook service: http://localhost:8000

## Docker deployment

```bash
cp .env.example .env
docker compose up --build
```

Services:
- `app` (Streamlit): port 8501
- `webhook` (FastAPI): port 8000
- `postgres`: port 5432

## SaaS integration notes

### Supabase Auth
- Current UI contains a demo sign-in widget in `app/auth.py`.
- Replace with real Supabase flows (magic link/OAuth), then persist Supabase user IDs in `users.supabase_user_id`.

### Stripe Subscriptions
- Use Stripe Checkout on sign-up and store customer/subscription metadata in Postgres.
- Configure webhook secret and endpoint (`/webhooks/stripe`) in Stripe dashboard.
- Implement tier updates in `services/webhook_service.py` TODO blocks.

## Core analytics API

Main data structure: `core.models.Report`.

Analytics modules:
- `core/metrics.py`: returns, risk/performance metrics, beta/alpha, rolling correlation.
- `core/portfolio.py`: CSV weight validation and weighted return aggregation.
- `core/reporting.py`: orchestrates analytics and recommendations into a `Report` dataclass.
- `core/recommendations.py`: v1 rules engine.
- `core/regimes.py`: placeholder scaffold for regime classification.
- `core/factors.py`: placeholder scaffold for factor analysis.

## Quality checks

```bash
ruff check .
mypy core app services db
pytest -q
```

## GitHub Actions

A CI workflow runs Ruff, MyPy, and pytest on pushes and pull requests.

## Security

- No secrets are committed.
- `.env.example` includes placeholders only.
- Use least-privilege keys for Supabase and Stripe.
