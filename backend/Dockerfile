FROM python:3.13-slim AS builder
WORKDIR /app
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY backend/requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/venv/bin:$PATH" \
    PYTHONPATH=/app
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser -m appuser
COPY --from=builder --chown=appuser:appuser /venv /venv
COPY --chown=appuser:appuser backend/src ./src
COPY --chown=appuser:appuser database/migrations ./migrations
RUN mkdir -p /app/instance && chown -R appuser:appuser /app/instance
COPY --chown=appuser:appuser backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
RUN mkdir -p /app/shared_tmp && chmod 777 /app/shared_tmp
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --retries=5 --start-period=30s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=5", "--worker-tmp-dir", "/tmp", "--access-logfile=-", "--error-logfile=-", "src.index:app"]
