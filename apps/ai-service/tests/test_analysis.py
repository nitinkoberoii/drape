import base64
from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

import app.main as main_module
from app.schemas import AnalysisThresholds, BoundingBox, ClothingItem, PersonOutfit, SegmentationMask


def _image_data_url() -> str:
    image = Image.new("RGB", (8, 4), color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"


class FakeInference:
    def analyze(
        self, image: Image.Image, thresholds: AnalysisThresholds, include_debug_visuals: bool = False
    ) -> list[PersonOutfit]:
        assert image.size == (8, 4)
        assert thresholds == AnalysisThresholds(detection=0.3, text=0.25)
        assert not include_debug_visuals
        return [PersonOutfit(
            id="person_1",
            confidence=0.97,
            bounding_box=BoundingBox(left=0, top=0, width=8, height=4),
            items=[
            ClothingItem(
                label="jacket",
                confidence=0.91,
                bounding_box=BoundingBox(left=1, top=0, width=3, height=4),
                mask=SegmentationMask(size=(4, 8), counts=[1, 3, 28]),
            ),
            ClothingItem(
                label="bag",
                confidence=0.74,
                bounding_box=BoundingBox(left=5, top=1, width=2, height=2),
                mask=SegmentationMask(size=(4, 8), counts=[13, 2, 17]),
            ),
            ],
        )]


def test_analysis_returns_multiple_segmented_items(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "get_inference", lambda: FakeInference())
    client = TestClient(main_module.app)

    response = client.post(
        "/analyze",
        json={
            "image_data_url": _image_data_url(),
            "source_url": "https://www.youtube.com/watch?v=test",
            "detection_threshold": 0.3,
            "text_threshold": 0.25,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "label": "jacket",
                "confidence": 0.91,
                "bounding_box": {"left": 1, "top": 0, "width": 3, "height": 4},
                "mask": {"encoding": "rle", "size": [4, 8], "counts": [1, 3, 28]},
            },
            {
                "label": "bag",
                "confidence": 0.74,
                "bounding_box": {"left": 5, "top": 1, "width": 2, "height": 2},
                "mask": {"encoding": "rle", "size": [4, 8], "counts": [13, 2, 17]},
            },
        ],
        "people": [
            {
                "id": "person_1",
                "confidence": 0.97,
                "bounding_box": {"left": 0, "top": 0, "width": 8, "height": 4},
                "items": [
                    {
                        "label": "jacket",
                        "confidence": 0.91,
                        "bounding_box": {"left": 1, "top": 0, "width": 3, "height": 4},
                        "mask": {"encoding": "rle", "size": [4, 8], "counts": [1, 3, 28]},
                    },
                    {
                        "label": "bag",
                        "confidence": 0.74,
                        "bounding_box": {"left": 5, "top": 1, "width": 2, "height": 2},
                        "mask": {"encoding": "rle", "size": [4, 8], "counts": [13, 2, 17]},
                    },
                ],
            }
        ],
        "thresholds": {"detection": 0.3, "text": 0.25},
    }


def test_analysis_rejects_invalid_image_data() -> None:
    client = TestClient(main_module.app)

    response = client.post(
        "/analyze",
        json={"image_data_url": "data:image/png;base64,invalid", "source_url": "https://example.com"},
    )

    assert response.status_code == 422
