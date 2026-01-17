# Multi-stage Dockerfile for Quantum Tech Trader
# Suitable for Docker Cloud Builder and portable across platforms

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 trader && \
    mkdir -p /app/data && \
    chown -R trader:trader /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/trader/.local

# Copy application code
COPY src/ /app/src/

# Set ownership
RUN chown -R trader:trader /app

# Switch to non-root user
USER trader

# Add local Python packages to PATH
ENV PATH=/home/trader/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Expose API port
EXPOSE 8000

# Volume for persistent trade history
VOLUME ["/app/data"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz').read()"

# Default: Run API server (can be overridden)
CMD ["python", "-m", "uvicorn", "src.quantum_trader.service:app", "--host", "0.0.0.0", "--port", "8000"]

# Alternative commands (override CMD):
# CLI mode: docker run ... python -m src.quantum_trader.cli --help
# Scheduler: docker run ... python -m src.quantum_trader.scheduler --help
