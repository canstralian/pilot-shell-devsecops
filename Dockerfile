# Dockerfile optimised for Hugging Face Spaces
#
# Hugging Face Spaces requirements:
#   - The application must listen on $PORT (injected at runtime; default 7860).
#   - The image must run as a non-root user.
#   - HTTPS termination is handled by the Spaces edge proxy; do NOT expose 443.

FROM python:3.9-slim

# ── System hardening ──────────────────────────────────────────────────────── #
# Disable pip version check noise and bytecode generation in the image.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ── Install dependencies ──────────────────────────────────────────────────── #
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application source ───────────────────────────────────────────────── #
COPY app.py .

# ── Non-root user (required by Hugging Face Spaces) ──────────────────────── #
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# ── Runtime ──────────────────────────────────────────────────────────────── #
# $PORT is injected by Hugging Face Spaces at runtime (default: 7860).
EXPOSE 7860

# Use Gunicorn as the production WSGI server.
# Workers = (2 × CPU cores) + 1 is a common heuristic; keep it conservative
# for the shared Spaces environment.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-7860} --workers 2 --threads 4 --timeout 60 app:app"]
