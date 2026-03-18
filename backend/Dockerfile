FROM python:3.13-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir --progress-bar off -r requirements.txt

FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_MODE=production \
    PYTHONFAULTHANDLER=1 \
    PATH="/home/appuser/.local/bin:${PATH}"
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser -m appuser
USER appuser
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser ./src .
EXPOSE 8000
CMD ["gunicorn", \
     "--workers=4", \
     "--bind=0.0.0.0:8000", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "index:app"]