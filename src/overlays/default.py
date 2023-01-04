from .base import BaseOverlay

from PIL import ImageFont


class DefaultOverlay(BaseOverlay):
    def draw(self, fit_frame: dict, fit_units: dict) -> None:
        consolas48 = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 48)
        self._draw.text([256, 256], "hello", fill=(255, 255, 255, 128), font=consolas48)
