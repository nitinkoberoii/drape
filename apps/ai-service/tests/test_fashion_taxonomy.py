from app.fashion_taxonomy import canonicalize_detection_label, detector_prompts


def test_detector_prompts_are_specific_fashion_terms() -> None:
    prompts = detector_prompts()

    assert "a crop top" in prompts
    assert "a cargo pants" in prompts
    assert "a shoulder bag" in prompts


def test_canonicalizes_specific_and_merged_detector_labels() -> None:
    assert canonicalize_detection_label("a cargo pants") == "pants"
    assert canonicalize_detection_label("a shoe boot a sneaker") == "shoe"
    assert canonicalize_detection_label("a pants a jeans") == "pants"
    assert canonicalize_detection_label("a tote bag") == "bag"


def test_rejects_labels_outside_the_fashion_taxonomy() -> None:
    assert canonicalize_detection_label("a lamp") is None
