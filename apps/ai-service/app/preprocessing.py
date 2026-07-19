import base64
import binascii
from io import BytesIO

from fastapi import HTTPException
from PIL import Image, ImageOps

from app.config import settings

SUPPORTED_PREFIXES = ("data:image/jpeg;base64,", "data:image/png;base64,")


def decode_image_data_url(image_data_url: str) -> Image.Image:
    """Decode, normalize orientation, and bound the image dimensions for inference."""
    prefix = next((value for value in SUPPORTED_PREFIXES if image_data_url.startswith(value)), None)
    if prefix is None:
        raise HTTPException(status_code=422, detail="image_data_url must be a PNG or JPEG data URL.")

    try:
        image_bytes = base64.b64decode(image_data_url[len(prefix) :], validate=True)
        image = Image.open(BytesIO(image_bytes))
        image.load()
    except (binascii.Error, OSError) as error:
        raise HTTPException(status_code=422, detail="image_data_url contains an invalid image.") from error

    normalized = ImageOps.exif_transpose(image).convert("RGB")
    normalized.thumbnail((settings.max_image_dimension, settings.max_image_dimension))
    return normalized
