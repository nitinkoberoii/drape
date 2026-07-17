from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))


settings = Settings()
