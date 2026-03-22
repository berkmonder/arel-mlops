FROM python:3.11-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_NO_DEV=1

WORKDIR /app

COPY pyproject.toml uv.lock .
RUN uv sync --locked

COPY . .
