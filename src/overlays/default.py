from PIL import Image

from .base import BaseOverlay


class DefaultOverlay(BaseOverlay):
    def overlay(self, timestamp: int) -> Image.Image:
        self._draw.rectangle((0, 0, self._im.width, self._im.height), fill=(0, 0, 0, 0))
        self._draw.line((0, 0) + self._im.size, fill=128)
        self._draw.line((0, self._im.size[1], self._im.size[0], 0), fill=128)

        return self._im
