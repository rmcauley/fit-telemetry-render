from collections import OrderedDict

from overlays.default import DefaultOverlay

class GoProState:
    _video_path: str
    _fit_path: str
    _fit_offset: int
    _overlay: DefaultOverlay
    _fit: OrderedDict

    def __init__(self) -> None:
        self._video_path = None
        self._fit_path = None
        self._fit_offset = 0
        self._overlay = DefaultOverlay
        self._fit = None

    @property
    def video_path(self) -> str:
        return self._video_path

    @video_path.setter
    def video_path(self, v: str) -> None:
        self._video_path = v

    @property
    def fit_path(self) -> str:
        return self._fit_path

    @fit_path.setter
    def fit_path(self, v: str) -> None:
        self._fit_path = v

    @property
    def fit_offset(self) -> int:
        return self._fit_offset

    @fit_offset.setter
    def fit_offset(self, v: int) -> None:
        self._fit_offset = v

    @property
    def fit(self) -> OrderedDict:
        return self._fit

    @fit.setter
    def fit(self, v: OrderedDict):
        if self._fit:
            self._fit.close()
        self._fit = v

    @property
    def overlay(self) -> DefaultOverlay:
        return self._overlay

    @overlay.setter
    def overlay(self, v: DefaultOverlay):
        self._overlay = v