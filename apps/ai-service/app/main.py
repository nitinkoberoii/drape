from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


app = FastAPI(title="Drape AI Service", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return service health without loading inference models."""
    return HealthResponse(status="ok")
