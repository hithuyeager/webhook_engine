FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.4.30 /uv /bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml ./
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python -r pyproject.toml

FROM python:3.12-slim AS runtime

RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --chown=appuser:appgroup alembic.ini ./
COPY --chown=appuser:appgroup alembic ./alembic
COPY --chown=appuser:appgroup app ./app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]