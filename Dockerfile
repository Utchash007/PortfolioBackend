FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /wheels \
        --index-url https://download.pytorch.org/whl/cpu \
        --extra-index-url https://pypi.org/simple \
        -r requirements.txt

# ── runtime ──────────────────────────────────────────────
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HAYSTACK_TELEMETRY_ENABLED=false

WORKDIR /app

COPY --from=builder /wheels /tmp/wheels
RUN pip install --no-cache-dir --no-deps /tmp/wheels/* && \
    rm -rf /tmp/wheels /root/.cache && \
    pip list | grep -iE "nvidia|cuda|triton|nccl" && echo "ERROR: CUDA packages found!" && exit 1 || true

COPY Files/ Files/
COPY Configs/ Configs/
COPY DBQuery/ DBQuery/
COPY RAGPipeline/ RAGPipeline/
COPY App/ App/
COPY main.py .

# Create user WITH a real home directory
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --home /home/appuser appuser && \
    chown -R appuser:appgroup /app
USER appuser

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]