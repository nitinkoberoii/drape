from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    max_image_dimension: int = int(os.getenv("MAX_IMAGE_DIMENSION", "1536"))
    detector_model_id: str = os.getenv("DETECTOR_MODEL_ID", "IDEA-Research/grounding-dino-base")
    segmenter_model_id: str = os.getenv("SEGMENTER_MODEL_ID", "facebook/sam2-hiera-small")
    clothing_labels: tuple[str, ...] = (
        "top", "shirt", "t-shirt", "blouse", "jacket", "coat", "dress", "skirt",
        "pants", "jeans", "shorts", "shoe", "boot", "sneaker", "bag", "handbag",
        "belt", "hat", "scarf", "glasses", "watch", "jewelry",
    )


settings = Settings()
