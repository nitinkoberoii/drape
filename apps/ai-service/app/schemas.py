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


class ClothingItem(BaseModel):
    label: str
    confidence: confloat(ge=0, le=1)
    bounding_box: BoundingBox
    mask: SegmentationMask


class AnalysisRequest(BaseModel):
    image_data_url: str = Field(..., max_length=8_000_000)
    source_url: HttpUrl


class AnalysisResponse(BaseModel):
    items: list[ClothingItem]

