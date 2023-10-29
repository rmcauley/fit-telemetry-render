from PIL import Image, ImageDraw
from pilmoji import Pilmoji


class BaseOverlay:
    _im: Image.Image
    _draw: ImageDraw.ImageDraw
    w: int
    h: int
    fill: tuple

    def __init__(self, state, w: int, h: int) -> None:
        self.state = state
        self.w = w
        self.h = h
        self.fill = (0, 0, 0, 0)
        self._im = Image.new("RGBA", (self.w, self.h))
        self._draw = ImageDraw.Draw(self._im)
        self._pilmoji = Pilmoji(self._im)

    def overlay(self, fit_frame: dict) -> Image.Image:
        self._draw.rectangle((0, 0, self._im.width, self._im.height), fill=self.fill)
        self.draw(fit_frame)
        return self._im

    def draw(self, fit_frame: dict) -> None:
        pass
