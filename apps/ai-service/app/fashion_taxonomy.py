"""Fashion-specific detector prompts and stable categories for downstream services."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class FashionCategory:
    label: str
    prompts: tuple[str, ...]


FASHION_TAXONOMY: tuple[FashionCategory, ...] = (
    FashionCategory("top", ("crop top", "tank top", "sleeveless top", "t shirt", "sweater")),
    FashionCategory("shirt", ("button down shirt", "shirt", "blouse")),
    FashionCategory("outerwear", ("leather jacket", "jacket", "cardigan", "hoodie", "blazer", "coat")),
    FashionCategory("dress", ("evening gown", "gown", "dress", "jumpsuit")),
    FashionCategory("skirt", ("skirt",)),
    FashionCategory("pants", ("cargo pants", "wide leg trousers", "trousers", "jeans", "pants", "leggings", "shorts")),
    FashionCategory("shoe", ("sneakers", "sneaker", "boots", "boot", "heels", "sandals", "shoes", "shoe")),
    FashionCategory("bag", ("shoulder bag", "tote bag", "handbag", "backpack", "clutch", "bag")),
    FashionCategory("hat", ("baseball cap", "beanie", "hat")),
    FashionCategory("belt", ("belt",)),
    FashionCategory("scarf", ("scarf",)),
    FashionCategory("glasses", ("sunglasses", "glasses")),
    FashionCategory("watch", ("watch",)),
    FashionCategory("jewelry", ("necklace", "earrings", "earring", "bracelet", "ring", "jewelry")),
)

_PROMPT_TO_CATEGORY = {
    prompt: category.label for category in FASHION_TAXONOMY for prompt in category.prompts
}
_SORTED_PROMPTS = tuple(sorted(_PROMPT_TO_CATEGORY, key=len, reverse=True))


def detector_prompts() -> list[str]:
    """Return the precise prompts sent to the open-vocabulary detector."""
    return [f"a {prompt}" for prompt in _PROMPT_TO_CATEGORY]


def canonicalize_detection_label(raw_label: str) -> str | None:
    """Map a detector phrase, including merged synonym spans, to one Drape category."""
    normalized = re.sub(r"[^a-z0-9]+", " ", raw_label.lower()).strip()
    matches: list[tuple[int, int, str]] = []
    for prompt in _SORTED_PROMPTS:
        match = re.search(rf"(?<!\w){re.escape(prompt)}(?!\w)", normalized)
        if match:
            matches.append((match.start(), -len(prompt), _PROMPT_TO_CATEGORY[prompt]))

    if not matches:
        return None
    # Grounding DINO can return neighbouring text spans together. Prefer the first,
    # most-specific matching phrase; synonyms in one span map to the same category.
    return min(matches)[2]
