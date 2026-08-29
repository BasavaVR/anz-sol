import os
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(
    title="Build Info Service",
    description="Exposes build metadata and operational health endpoints",
    version=os.getenv("APP_VERSION", "1.0.0"),
)

class BuildInfoResponse(BaseModel):
    application: str
    version: str
    git_commit: str
    build_timestamp: str
    environment: str
    status: str

@app.get("/healthz", status_code=status.HTTP_200_OK, summary="Liveness & Readiness Probe")
def health_check():
    """Returns application health status for orchestrator probes."""
    return {"status": "ok"}

@app.get("/info", response_model=BuildInfoResponse, status_code=status.HTTP_200_OK, summary="Get Build Information")
def get_build_info():
    """Returns immutable build information baked during container build time."""
    return BuildInfoResponse(
        application=os.getenv("APP_NAME", "build-info-service"),
        version=os.getenv("APP_VERSION", "1.0.0"),
        git_commit=os.getenv("GIT_COMMIT", "local-development"),
        build_timestamp=os.getenv("BUILD_TIMESTAMP", "unknown"),
        environment=os.getenv("APP_ENV", "production"),
        status="healthy",
    )