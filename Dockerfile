# ============================================================
# GridPortfolio
# Python Application Container
# ============================================================

FROM python:3.11-slim

# ------------------------------------------------------------
# Runtime configuration
# ------------------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ------------------------------------------------------------
# System dependencies
# ------------------------------------------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Application directory
# ------------------------------------------------------------

WORKDIR /app

# ------------------------------------------------------------
# Install Python dependencies
# ------------------------------------------------------------

COPY pyproject.toml README.md ./

RUN pip install --upgrade pip setuptools wheel && \
    pip install -e ".[dev]"

# ------------------------------------------------------------
# Copy application source
# ------------------------------------------------------------

COPY src ./src
COPY scripts ./scripts
COPY tests ./tests
COPY examples ./examples
COPY docs ./docs

# ------------------------------------------------------------
# Create runtime data directories
# ------------------------------------------------------------

RUN mkdir -p \
    /app/data/raw \
    /app/data/processed \
    /app/data/scenarios

# ------------------------------------------------------------
# Non-root application user
# ------------------------------------------------------------

RUN useradd \
    --create-home \
    --shell /bin/bash \
    appuser

RUN chown -R appuser:appuser /app

USER appuser

# ------------------------------------------------------------
# API configuration
# ------------------------------------------------------------

EXPOSE 8000

# ------------------------------------------------------------
# Health check
# ------------------------------------------------------------

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=20s \
    --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# ------------------------------------------------------------
# Default command
# ------------------------------------------------------------

CMD [
    "uvicorn",
    "gridportfolio.api.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]