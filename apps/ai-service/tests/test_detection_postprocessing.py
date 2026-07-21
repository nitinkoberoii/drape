from PIL import Image

from app.inference import crop_person, suppress_duplicate_detections, translate_detection


class FakeBox:
    def __init__(self, coordinates: list[float]) -> None:
        self.coordinates = coordinates

    def tolist(self) -> list[float]:
        return self.coordinates


def test_suppresses_overlapping_duplicates_in_the_same_category() -> None:
    detections = [
        {"label": "pants", "score": 0.8, "box": FakeBox([0, 0, 100, 100])},
        {"label": "pants", "score": 0.6, "box": FakeBox([5, 5, 95, 95])},
        {"label": "bag", "score": 0.7, "box": FakeBox([5, 5, 95, 95])},
    ]

    result = suppress_duplicate_detections(detections, duplicate_iou_threshold=0.6)

    assert [(item["label"], item["score"]) for item in result] == [
        ("pants", 0.8),
        ("bag", 0.7),
    ]


def test_preserves_separate_items_in_the_same_category() -> None:
    detections = [
        {"label": "shoe", "score": 0.8, "box": FakeBox([0, 0, 20, 20])},
        {"label": "shoe", "score": 0.7, "box": FakeBox([80, 80, 100, 100])},
    ]

    result = suppress_duplicate_detections(detections, duplicate_iou_threshold=0.6)

    assert len(result) == 2


def test_person_crop_translation_restores_full_image_coordinates() -> None:
    image = Image.new("RGB", (100, 100))
    crop, offset = crop_person(image, [20, 20, 60, 80], padding=0.1)

    result = translate_detection({"label": "pants", "score": 0.8, "box": [4, 6, 24, 50]}, offset)

    assert crop.size == (48, 72)
    assert result["box"] == [20, 20, 40, 64]
