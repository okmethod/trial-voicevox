# syntax=docker/dockerfile:1
# check=error=true

ARG PYTHON_VERSION=x

FROM python:${PYTHON_VERSION}-slim AS base
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# linux向け voicevox_core のダウンロード
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget -O /app/download-linux-x64 https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.0/download-linux-x64 && \
    chmod +x /app/download-linux-x64 && \
    echo "y" | ./download-linux-x64 --exclude c-api

FROM base AS requirements-exporter
RUN pip install --no-cache-dir uv
COPY ./pyproject.toml ./uv.lock ./
RUN uv export --frozen --no-dev --format requirements-txt > requirements.txt
RUN uv export --frozen --format requirements-txt > requirements_dev.txt

FROM base AS development
COPY --from=requirements-exporter /app/requirements_dev.txt ./
RUN pip install --no-cache-dir -r requirements_dev.txt
COPY ./voicevox_core voicevox_core

FROM base AS production
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
COPY --from=requirements-exporter /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER appuser
COPY ./src src
COPY ./voicevox_core voicevox_core
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--log-config", "src/logging.ini"]
