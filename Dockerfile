# ── Stage 1: Build ─────────────────────────────────────────────────────
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ── Stage 2: Production ───────────────────────────────────────────────
FROM python:3.12-slim as production

# Create non-root user
RUN groupadd -r storeboost && \
    useradd -r -g storeboost -d /app -s /sbin/nologin storeboost

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/storeboost/.local

# Copy application code
COPY ai-service/ ./ai-service/
COPY pyproject.toml .

# Set ownership
RUN chown -R storeboost:storeboost /app

# Switch to non-root user
USER storeboost

# Set Python path to find modules
ENV PYTHONPATH=/app/ai-service
ENV PATH=/home/storeboost/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; r = httpx.get('http://localhost:8000/health'); r.raise_for_status()"

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app/ai-service"]
