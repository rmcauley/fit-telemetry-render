from PIL import Image, ImageDraw


class BaseOverlay:
    _im: Image.Image
    _draw: ImageDraw.ImageDraw
    w: int
    h: int

    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self._im = Image.new("RGBA", (w, h))
        self._draw = ImageDraw.Draw(self._im)

    def overlay(self, fit_frame: dict, fit_units: dict) -> Image.Image:
        self._draw.rectangle((0, 0, self._im.width, self._im.height), fill=(0, 0, 0, 0))
        self.draw(fit_frame, fit_units)
        return self._im

    def draw(self, fit_frame: dict, fit_units: dict) -> None:
        pass
