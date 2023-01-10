from PIL import Image, ImageDraw


class BaseOverlay:
    _im: Image.Image
    _draw: ImageDraw.ImageDraw
    w: int
    h: int
    fill: tuple

    def __init__(self, w: int, h: int, fill=(255, 0, 255, 0)) -> None:
        self.w = w
        self.h = h
        self.fill = fill
        self._im = Image.new("RGB", (w, h))
        self._draw = ImageDraw.Draw(self._im)

    def overlay(self, fit_frame: dict, fit_units: dict) -> Image.Image:
        self._draw.rectangle((0, 0, self._im.width, self._im.height), fill=self.fill)
        self.draw(fit_frame, fit_units)
        return self._im

    def draw(self, fit_frame: dict, fit_units: dict) -> None:
        pass
