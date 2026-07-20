from dataclasses import dataclass
import os


def _confidence_from_environment(name: str, default: str) -> float:
    value = float(os.getenv(name, default))
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1.")
    return value


@dataclass(frozen=True)
class Settings:
    # CONFIDENCE_THRESHOLD remains a backwards-compatible default for both values.
    detection_confidence_threshold: float = _confidence_from_environment(
        "DETECTION_CONFIDENCE_THRESHOLD", os.getenv("CONFIDENCE_THRESHOLD", "0.5")
    )
    text_confidence_threshold: float = _confidence_from_environment(
        "TEXT_CONFIDENCE_THRESHOLD", os.getenv("CONFIDENCE_THRESHOLD", "0.5")
    )
    duplicate_iou_threshold: float = _confidence_from_environment(
        "DUPLICATE_IOU_THRESHOLD", "0.6"
    )
    max_image_dimension: int = int(os.getenv("MAX_IMAGE_DIMENSION", "1536"))
    detector_model_id: str = os.getenv("DETECTOR_MODEL_ID", "IDEA-Research/grounding-dino-base")
    segmenter_model_id: str = os.getenv("SEGMENTER_MODEL_ID", "facebook/sam2-hiera-small")
settings = Settings()
