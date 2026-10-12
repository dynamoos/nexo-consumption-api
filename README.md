# nexo-consumption-api

Internal API that exposes how much Nexo's chatbot was used, so the billing
server (Cata) can build the monthly pre-invoice. It returns **quantities only**:
Cata applies the prices and the monthly fixed fee.

## Quick path

1. `uv sync`
2. `cp .env.example .env` and fill in the values (see [Configuration](#configuration)).
3. `uv run python manage.py runserver`
4. Ask for a month:

```bash
curl -H "Authorization: Bearer $SERVICE_TOKEN" \
  "http://localhost:8000/api/consumption/monthly?start=2026-09-01&end=2026-09-30"
```

## Endpoints

Both endpoints are `GET`, need `Authorization: Bearer <SERVICE_TOKEN>`, and take
the same query parameters.

| Parameter | Format | Meaning |
|-----------|--------|---------|
| `start` | `YYYY-MM-DD` | First day, included |
| `end` | `YYYY-MM-DD` | Last day, included |

| Endpoint | Returns |
|----------|---------|
| `/api/consumption/monthly` | One line per month and stage, with its quantity |
| `/api/consumption/leads` | One line per lead, with its conversation |

```json
{"items": [{"month": "2026-09", "stage": "lead", "conversation_type": "completa", "quantity": 160}]}
```

```json
{"items": [{"day": "2026-09-30", "conversation_id": "…", "lead_id": "…", "stage": "inicial", "conversation_type": "iniciada"}]}
```

| Status | When |
|--------|------|
| 200 | Always has `items`, which may be empty |
| 400 | A date is missing or malformed, or `end` is before `start` |
| 401 | The token is missing or wrong |
| 500 | Something failed on our side; the cause is only in the log |

## Configuration

| Variable | Required | Meaning |
|----------|----------|---------|
| `DJANGO_SECRET_KEY` | yes | Signs what Django signs |
| `DATABASE_URL` | yes | Nexo's database, e.g. `postgresql://user:pass@host:5432/nexo?sslmode=require` |
| `SERVICE_TOKEN` | yes | The token Cata presents |
| `DEBUG` | no | `True` only for local work |
| `ALLOWED_HOSTS` | when `DEBUG` is off | Comma-separated hosts the service answers to |
| `FORCE_HTTPS` | no | Redirect to HTTPS; defaults to `not DEBUG` |
| `CONN_MAX_AGE` | no | Seconds a database connection is kept |
| `LOG_LEVEL` | no | Defaults to `INFO` |
| `WEB_CONCURRENCY` | no | Number of `gunicorn` workers in the container; defaults to 1 |
| `CORS_ALLOW_ALL_ORIGINS` | no | `True` lets any web page read the service; defaults to `False` |
| `CORS_ALLOWED_ORIGINS` | no | Comma-separated pages allowed to read it, e.g. `https://cata.mibot.cl`; used when the switch above is off |

## Deployment

The service runs as one container behind Traefik, on the same domain as
`inmobilia-agent`, under the `/nexo` path.

| Where | What |
|-------|------|
| `docker-compose.yml` | Builds the image and joins `traefik_proxy` and `prod_backend` |
| `.env` on the server | `DATABASE_URL`, `SERVICE_TOKEN`, `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, `WEB_CONCURRENCY`, `CORS_ALLOW_ALL_ORIGINS` |
| Traefik `dynamic/` folder | A file that routes `Host(...) && PathPrefix(/nexo)` to the container |

`DEBUG` and `FORCE_HTTPS` are fixed in the compose file: Traefik ends TLS, and
a copied development `.env` must never turn on `DEBUG`.

`ALLOWED_HOSTS` must name the public domain and `localhost`, which the
container's own healthcheck uses.

```bash
docker compose up -d --build
docker compose ps    # the service should become healthy
```

Public URL: `https://<domain>/nexo/api/consumption/monthly?start=…&end=…`

## How consumption is counted

- A **lead** is one row of `public.leads`. A conversation can have several.
- Each lead is billed by its stage:

| Stage | Billed as |
|-------|-----------|
| `inicial` | `iniciada` |
| `prelead` | `parcial` |
| `lead`, `lead enriquecido` | `completa` |

- A status that names no stage is not counted.
- Days are **UTC days**, which is how the July–September pre-invoices were cut.
- The database is only read, never written.

## Open questions

- Is billing per lead row, or per conversation and the stage it reached?
- Do repeated rows for the same property in one conversation count more than once?

## Layout

```
config/                     settings, urls, error handling
contexts/consumption/
  domain/                   rules: stages, date range, repository port
  application/queries/      one query, handler and response per use case
  infrastructure/           Django model, mapper, repository, API, wiring
tests/
```

## Development

```bash
uv run pytest            # tests
uv run ruff check .      # lint
uv run ruff format .     # format
uv run mypy config contexts tests manage.py   # types
```
