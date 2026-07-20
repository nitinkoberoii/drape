from fastapi import FastAPI
from pydantic import BaseModel

from app.inference import get_inference
from app.preprocessing import decode_image_data_url
from app.config import settings
from app.schemas import AnalysisRequest, AnalysisResponse, AnalysisThresholds


class HealthResponse(BaseModel):
    status: str


app = FastAPI(title="Drape AI Service", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return service health without loading inference models."""
    return HealthResponse(status="ok")


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_frame(request: AnalysisRequest) -> AnalysisResponse:
    """Detect and segment every supported clothing item in one captured frame."""
    image = decode_image_data_url(request.image_data_url)
    thresholds = AnalysisThresholds(
        detection=(
            request.detection_threshold
            if request.detection_threshold is not None
            else settings.detection_confidence_threshold
        ),
        text=(
            request.text_threshold
            if request.text_threshold is not None
            else settings.text_confidence_threshold
        ),
    )
    return AnalysisResponse(items=get_inference().analyze(image, thresholds=thresholds), thresholds=thresholds)
