# syntax=docker/dockerfile:1


# --- What the service needs to run ---------------------------------------------

# Dependencies are gathered in a stage of their own: only the result is
# delivered, not the tools used to gather it.
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.30 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# The lock decides what is installed, so nothing else is read. Test and
# formatting tools stay out.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project


# --- The service as it is delivered --------------------------------------------

# Only what runs: the dependencies already installed, and the service itself.
FROM python:3.14-slim AS runtime

# Nobody with more power than the service needs.
RUN groupadd --system app && useradd --system --gid app --home-dir /app app

WORKDIR /app

# What it is made of. The service's own code comes last, because it is what
# changes most.
COPY --from=builder /app/.venv /app/.venv
COPY --chown=app:app manage.py ./
COPY --chown=app:app config ./config
COPY --chown=app:app contexts ./contexts

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

# How it starts: answering on one port, with every access written to the output.
EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--no-control-socket"]
