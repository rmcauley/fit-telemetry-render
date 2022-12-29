from PIL import Image, ImageDraw

class DefaultOverlay:
    _im: Image
    _draw: ImageDraw

    def __init__(self, w: int, h: int):
        self._im = Image.new("RGBA", (w, h))
        self._draw = ImageDraw.Draw(self._im)

    def overlay(self, timestamp: int) -> Image.Image:
        self._draw.rectangle((0, 0, self._im.width, self._im.height), fill=(0, 0, 0, 0))
        self._draw.line((0, 0) + self._im.size, fill=128)
        self._draw.line((0, self._im.size[1], self._im.size[0], 0), fill=128)

        return self._im