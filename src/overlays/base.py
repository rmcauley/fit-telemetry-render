from PIL import Image, ImageDraw

from state import GoProState


class BaseOverlay:
    _im: Image.Image
    _draw: ImageDraw.ImageDraw
    _state: GoProState

    def __init__(self, state: GoProState, w: int, h: int) -> None:
        self._state = state
        self._im = Image.new("RGBA", (w, h))
        self._draw = ImageDraw.Draw(self._im)

    def overlay(self, timestamp: int) -> Image.Image:
        return self._im
