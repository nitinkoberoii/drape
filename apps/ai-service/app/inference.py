from functools import lru_cache
import logging
from typing import Any

from fastapi import HTTPException
from PIL import Image

from app.config import settings
from app.fashion_taxonomy import canonicalize_detection_label, detector_prompts
from app.schemas import AnalysisThresholds, BoundingBox, ClothingItem, SegmentationMask

logger = logging.getLogger(__name__)


class FashionInference:
    """Lazily loaded, stateless Grounding DINO + SAM 2 inference pipeline."""

    def __init__(self) -> None:
        try:
            import torch
            from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor, Sam2Model, Sam2Processor
        except ImportError as error:
            raise RuntimeError("AI model dependencies are not installed.") from error

        self.torch = torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.detector_processor = AutoProcessor.from_pretrained(settings.detector_model_id)
        self.detector_model = AutoModelForZeroShotObjectDetection.from_pretrained(
            settings.detector_model_id
        ).to(self.device)
        self.segmenter_processor = Sam2Processor.from_pretrained(settings.segmenter_model_id)
        self.segmenter_model = Sam2Model.from_pretrained(settings.segmenter_model_id).to(self.device)

    def analyze(
        self, image: Image.Image, thresholds: AnalysisThresholds
    ) -> list[ClothingItem]:
        detections = self._detect(image, thresholds)
        return [self._segment(image, detection) for detection in detections]

    def _detect(
        self, image: Image.Image, thresholds: AnalysisThresholds
    ) -> list[dict[str, Any]]:
        labels = [detector_prompts()]
        inputs = self.detector_processor(images=image, text=labels, return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            outputs = self.detector_model(**inputs)
        results = self.detector_processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=thresholds.detection,
            text_threshold=thresholds.text,
            target_sizes=[image.size[::-1]],
        )[0]
        detections: list[dict[str, Any]] = []
        for label, score, box in zip(results["labels"], results["scores"], results["boxes"], strict=True):
            category = canonicalize_detection_label(label)
            if category is None:
                logger.warning("Discarding detection with an unmapped fashion label: %s", label)
                continue
            detections.append({"label": category, "score": float(score), "box": box})
        return suppress_duplicate_detections(detections, settings.duplicate_iou_threshold)

    def _segment(self, image: Image.Image, detection: dict[str, Any]) -> ClothingItem:
        box = detection["box"].tolist()
        inputs = self.segmenter_processor(images=image, input_boxes=[[box]], return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            outputs = self.segmenter_model(**inputs, multimask_output=False)
        mask = self.segmenter_processor.post_process_masks(
            outputs.pred_masks.cpu(), inputs["original_sizes"]
        )[0][0][0]
        left, top, right, bottom = (round(value) for value in box)
        return ClothingItem(
            label=detection["label"],
            confidence=detection["score"],
            bounding_box=BoundingBox(
                left=max(0, left), top=max(0, top), width=max(1, right - left), height=max(1, bottom - top)
            ),
            mask=SegmentationMask(size=(image.height, image.width), counts=_encode_mask(mask)),
        )


def _encode_mask(mask: Any) -> list[int]:
    """Encode a boolean mask in row-major RLE without adding a NumPy dependency."""
    values = (mask > 0).flatten().tolist()
    counts: list[int] = []
    current = 0
    length = 0
    for value in values:
        bit = 1 if value else 0
        if bit == current:
            length += 1
        else:
            counts.append(length)
            current = bit
            length = 1
    counts.append(length)
    return counts


def suppress_duplicate_detections(
    detections: list[dict[str, Any]], duplicate_iou_threshold: float
) -> list[dict[str, Any]]:
    """Keep the strongest overlapping box for each canonical fashion category."""
    kept: list[dict[str, Any]] = []
    for detection in sorted(detections, key=lambda item: item["score"], reverse=True):
        box = detection["box"].tolist()
        duplicate = any(
            detection["label"] == existing["label"]
            and _intersection_over_union(box, existing["box"].tolist()) >= duplicate_iou_threshold
            for existing in kept
        )
        if not duplicate:
            kept.append(detection)
    return kept


def _intersection_over_union(first: list[float], second: list[float]) -> float:
    first_left, first_top, first_right, first_bottom = first
    second_left, second_top, second_right, second_bottom = second
    intersection_width = max(0, min(first_right, second_right) - max(first_left, second_left))
    intersection_height = max(0, min(first_bottom, second_bottom) - max(first_top, second_top))
    intersection = intersection_width * intersection_height
    if intersection == 0:
        return 0
    first_area = (first_right - first_left) * (first_bottom - first_top)
    second_area = (second_right - second_left) * (second_bottom - second_top)
    return intersection / (first_area + second_area - intersection)


@lru_cache(maxsize=1)
def get_inference() -> FashionInference:
    try:
        return FashionInference()
    except (OSError, RuntimeError) as error:
        logger.exception("Unable to initialize AI inference models")
        raise HTTPException(status_code=503, detail="AI models are unavailable. Try again shortly.") from error
