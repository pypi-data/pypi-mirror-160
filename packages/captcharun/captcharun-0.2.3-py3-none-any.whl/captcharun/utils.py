import base64
from typing import Union


def to_base64(image: Union[bytes, str]) -> str:
    if isinstance(image, bytes):
        image = base64.b64encode(image).decode()
    return image
