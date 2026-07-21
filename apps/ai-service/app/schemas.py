from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, conint, confloat


class BoundingBox(BaseModel):
    left: conint(ge=0)
    top: conint(ge=0)
    width: conint(gt=0)
    height: conint(gt=0)


class SegmentationMask(BaseModel):
    """COCO-style run-length encoding, in row-major order."""

    encoding: Literal["rle"] = "rle"
    size: tuple[conint(gt=0), conint(gt=0)]
    counts: list[conint(gt=0)]


class ItemDebugVisuals(BaseModel):
    masked_crop_png_data_url: str


class ClothingItem(BaseModel):
    label: str
    confidence: confloat(ge=0, le=1)
    bounding_box: BoundingBox
    mask: SegmentationMask
    debug_visuals: ItemDebugVisuals | None = None


class PersonDebugVisuals(BaseModel):
    overlay_png_data_url: str


class PersonOutfit(BaseModel):
    id: str
    confidence: confloat(ge=0, le=1)
    bounding_box: BoundingBox
    items: list[ClothingItem]
    debug_visuals: PersonDebugVisuals | None = None
    debug_visuals_truncated: bool | None = None


class AnalysisThresholds(BaseModel):
    detection: confloat(ge=0, le=1)
    text: confloat(ge=0, le=1)


class AnalysisRequest(BaseModel):
    image_data_url: str = Field(..., max_length=8_000_000)
    source_url: HttpUrl
    detection_threshold: confloat(ge=0, le=1) | None = None
    text_threshold: confloat(ge=0, le=1) | None = None
    include_debug_visuals: bool = False


class AnalysisResponse(BaseModel):
    items: list[ClothingItem]
    people: list[PersonOutfit]
    thresholds: AnalysisThresholds
