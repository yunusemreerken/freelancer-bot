# ── Build stage ─────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Runtime stage ────────────────────────────────────
FROM python:3.11-slim AS runtime

# Remove unnecessary tools from the runtime image.
RUN apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/lib/python3/dist-packages

# Create a non-root user for the application process.
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

WORKDIR /app

# Copy only the installed Python packages from the builder stage.
COPY --from=builder /install/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /install/bin/uvicorn /usr/local/bin/uvicorn

COPY app/ ./app/
COPY static/ ./static/

# Switch from root to the dedicated application user.
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
