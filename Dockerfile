# Stage 1: Build stage
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.12-slim AS runtime

WORKDIR /app

# Injected at build time via CI/CD
ARG APP_NAME="build-info-service"
ARG APP_VERSION="1.0.0"
ARG GIT_COMMIT="unknown"
ARG BUILD_TIMESTAMP="unknown"
ARG APP_ENV="production"

# Persist build metadata into runtime environment
ENV APP_NAME=$APP_NAME \
    APP_VERSION=$APP_VERSION \
    GIT_COMMIT=$GIT_COMMIT \
    BUILD_TIMESTAMP=$BUILD_TIMESTAMP \
    APP_ENV=$APP_ENV \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PATH=/home/appuser/.local/bin:$PATH

# Create non-root user for security compliance
RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -s /bin/sh -m appuser

# Copy installed dependencies and source code
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ /app/app/

RUN chown -R appuser:appgroup /app /home/appuser

USER appuser

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]