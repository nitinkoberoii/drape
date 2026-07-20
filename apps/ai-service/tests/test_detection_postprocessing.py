from app.inference import suppress_duplicate_detections


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
