from PIL import Image

from .base import BaseOverlay

from fit import FitDict


class DefaultOverlay(BaseOverlay):
    def draw(self, fit_frame: dict, fit: FitDict) -> None:
        self._draw.text([20, 20], "hello", fill="white")
