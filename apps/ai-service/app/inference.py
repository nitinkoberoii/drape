from functools import lru_cache
import base64
from dataclasses import dataclass
from io import BytesIO
import logging
from typing import Any

from fastapi import HTTPException
from PIL import Image

from app.config import settings
from app.fashion_taxonomy import canonicalize_detection_label, detector_prompts
from app.schemas import (
    AnalysisThresholds,
    BoundingBox,
    ClothingItem,
    ItemDebugVisuals,
    PersonDebugVisuals,
    PersonOutfit,
    SegmentationMask,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SegmentedDetection:
    item: ClothingItem
    mask: Any


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
        self, image: Image.Image, thresholds: AnalysisThresholds, include_debug_visuals: bool = False
    ) -> list[PersonOutfit]:
        people = self._detect_people(image, thresholds)
        outfits: list[PersonOutfit] = []
        for index, person in enumerate(sorted(people, key=lambda item: item["box"][0]), start=1):
            crop, offset = crop_person(image, person["box"], settings.person_crop_padding)
            detections = self._detect_fashion(crop, thresholds)
            translated = [translate_detection(detection, offset) for detection in detections]
            segmented = [self._segment(image, detection) for detection in translated]
            item_limit = settings.debug_visual_max_items_per_person
            visible_segmented = segmented[:item_limit] if include_debug_visuals else []
            items = [
                self._with_debug_crop(result, image)
                if include_debug_visuals and item_index < item_limit
                else result.item
                for item_index, result in enumerate(segmented)
            ]
            outfits.append(
                PersonOutfit(
                    id=f"person_{index}",
                    confidence=person["score"],
                    bounding_box=to_bounding_box(person["box"]),
                    items=items,
                    debug_visuals=(
                        PersonDebugVisuals(
                            overlay_png_data_url=create_person_overlay(
                                image, [result.mask for result in visible_segmented]
                            )
                        )
                        if include_debug_visuals
                        else None
                    ),
                    debug_visuals_truncated=(
                        len(segmented) > item_limit if include_debug_visuals else None
                    ),
                )
            )
        return outfits

    def _detect_people(self, image: Image.Image, thresholds: AnalysisThresholds) -> list[dict[str, Any]]:
        return suppress_duplicate_detections(
            self._run_detector(image, ["a person"], thresholds, text_threshold=thresholds.text),
            settings.duplicate_iou_threshold,
        )

    def _detect_fashion(self, image: Image.Image, thresholds: AnalysisThresholds) -> list[dict[str, Any]]:
        raw_detections = self._run_detector(image, detector_prompts(), thresholds)
        detections: list[dict[str, Any]] = []
        for detection in raw_detections:
            category = canonicalize_detection_label(detection["label"])
            if category is None:
                logger.warning("Discarding detection with an unmapped fashion label: %s", detection["label"])
                continue
            detections.append({**detection, "label": category})
        return suppress_duplicate_detections(detections, settings.duplicate_iou_threshold)

    def _run_detector(
        self,
        image: Image.Image,
        prompts: list[str],
        thresholds: AnalysisThresholds,
        text_threshold: float | None = None,
    ) -> list[dict[str, Any]]:
        labels = [prompts]
        inputs = self.detector_processor(images=image, text=labels, return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            outputs = self.detector_model(**inputs)
        results = self.detector_processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=thresholds.detection,
            text_threshold=text_threshold if text_threshold is not None else thresholds.text,
            target_sizes=[image.size[::-1]],
        )[0]
        detections: list[dict[str, Any]] = []
        for label, score, box in zip(results["labels"], results["scores"], results["boxes"], strict=True):
            detections.append(
                {"label": label.removeprefix("a "), "score": float(score), "box": box.tolist()}
            )
        return detections

    def _segment(self, image: Image.Image, detection: dict[str, Any]) -> SegmentedDetection:
        box = detection["box"]
        inputs = self.segmenter_processor(images=image, input_boxes=[[box]], return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            outputs = self.segmenter_model(**inputs, multimask_output=False)
        mask = self.segmenter_processor.post_process_masks(
            outputs.pred_masks.cpu(), inputs["original_sizes"]
        )[0][0][0]
        left, top, right, bottom = (round(value) for value in box)
        return SegmentedDetection(
            item=ClothingItem(
                label=detection["label"],
                confidence=detection["score"],
                bounding_box=BoundingBox(
                    left=max(0, left),
                    top=max(0, top),
                    width=max(1, right - left),
                    height=max(1, bottom - top),
                ),
                mask=SegmentationMask(size=(image.height, image.width), counts=_encode_mask(mask)),
            ),
            mask=mask,
        )

    def _with_debug_crop(self, segmented: SegmentedDetection, image: Image.Image) -> ClothingItem:
        return segmented.item.copy(
            update={
                "debug_visuals": ItemDebugVisuals(
                    masked_crop_png_data_url=create_masked_crop(
                        image, segmented.mask, segmented.item.bounding_box
                    )
                )
            }
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


def _mask_alpha(mask: Any) -> Image.Image:
    height, width = mask.shape[-2:]
    alpha = bytes(255 if value else 0 for value in (mask > 0).flatten().tolist())
    return Image.frombytes("L", (width, height), alpha)


def _png_data_url(image: Image.Image) -> str:
    rendered = image.copy()
    rendered.thumbnail(
        (settings.debug_visual_max_dimension, settings.debug_visual_max_dimension), Image.Resampling.LANCZOS
    )
    buffer = BytesIO()
    rendered.save(buffer, format="PNG", optimize=True)
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"


def create_masked_crop(image: Image.Image, mask: Any, box: BoundingBox) -> str:
    source = image.convert("RGBA")
    source.putalpha(_mask_alpha(mask))
    crop = source.crop((box.left, box.top, box.left + box.width, box.top + box.height))
    return _png_data_url(crop)


def create_person_overlay(image: Image.Image, masks: list[Any]) -> str:
    overlay = image.convert("RGBA")
    colors = ((79, 70, 229), (14, 165, 233), (34, 197, 94), (245, 158, 11), (239, 68, 68))
    for index, mask in enumerate(masks):
        highlight = Image.new("RGBA", image.size, colors[index % len(colors)] + (0,))
        highlight.putalpha(_mask_alpha(mask).point(lambda value: value // 2))
        overlay = Image.alpha_composite(overlay, highlight)
    return _png_data_url(overlay)


def suppress_duplicate_detections(
    detections: list[dict[str, Any]], duplicate_iou_threshold: float
) -> list[dict[str, Any]]:
    """Keep the strongest overlapping box for each canonical fashion category."""
    kept: list[dict[str, Any]] = []
    for detection in sorted(detections, key=lambda item: item["score"], reverse=True):
        box = _box_values(detection["box"])
        duplicate = any(
            detection["label"] == existing["label"]
            and _intersection_over_union(box, _box_values(existing["box"])) >= duplicate_iou_threshold
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


def _box_values(box: Any) -> list[float]:
    values = box.tolist() if hasattr(box, "tolist") else box
    return [float(value) for value in values]


def to_bounding_box(box: list[float]) -> BoundingBox:
    left, top, right, bottom = (round(value) for value in box)
    return BoundingBox(
        left=max(0, left),
        top=max(0, top),
        width=max(1, right - left),
        height=max(1, bottom - top),
    )


def crop_person(image: Image.Image, box: list[float], padding: float) -> tuple[Image.Image, tuple[int, int]]:
    """Create a padded person crop and return the crop's full-image offset."""
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    crop_left = max(0, round(left - width * padding))
    crop_top = max(0, round(top - height * padding))
    crop_right = min(image.width, round(right + width * padding))
    crop_bottom = min(image.height, round(bottom + height * padding))
    return image.crop((crop_left, crop_top, crop_right, crop_bottom)), (crop_left, crop_top)


def translate_detection(detection: dict[str, Any], offset: tuple[int, int]) -> dict[str, Any]:
    """Translate a person-crop detection into full-image coordinates for SAM 2."""
    left, top, right, bottom = detection["box"]
    offset_left, offset_top = offset
    return {
        **detection,
        "box": [left + offset_left, top + offset_top, right + offset_left, bottom + offset_top],
    }


@lru_cache(maxsize=1)
def get_inference() -> FashionInference:
    try:
        return FashionInference()
    except (OSError, RuntimeError) as error:
        logger.exception("Unable to initialize AI inference models")
        raise HTTPException(status_code=503, detail="AI models are unavailable. Try again shortly.") from error
