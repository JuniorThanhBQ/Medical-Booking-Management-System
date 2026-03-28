FROM python:3.13-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/home/appuser/.local/bin:${PATH}" \
    PYTHONPATH=/app
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
RUN groupadd -r appuser && useradd -r -g appuser -m appuser
RUN mkdir -p /app/instance && chown -R appuser:appuser /app/instance
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chmod=555 ./src ./src
USER appuser
EXPOSE 8000
CMD ["bash", "-c", " \
    while ! flask --app src.index:app db upgrade; do \
        echo 'Services is unhealthy. Retrying in 5 seconds'; \
        sleep 5; \
    done && \
    echo 'Migrations applied!' && \
    python src/fixtures/fixtures.py && \
    exec gunicorn --workers=4 --bind=0.0.0.0:8000 --access-logfile=- --error-logfile=- src.index:app \
"]
