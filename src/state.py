from collections import OrderedDict

from PySide6.QtCore import QObject, Signal

from fit import FitDict, get_fit_dict

from overlays.base import BaseOverlay
from overlays.default import DefaultOverlay


class GoProState(QObject):
    _video_path: str
    _video_sec: int
    _fit_path: str
    _fit: FitDict
    _fit_offset: int

    overlay: BaseOverlay = DefaultOverlay

    videoPathChange = Signal()
    videoSecChange = Signal()
    fitChange = Signal()
    fitOffsetChange = Signal()
    fitPathChange = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._video_path = ""
        self._fit_path = ""
        self._fit = None
        self._fit_offset = 0
        self._video_sec = 0

    @property
    def video_path(self) -> str:
        return self._video_path

    @video_path.setter
    def video_path(self, v: str) -> None:
        self._video_path = v
        self.videoPathChange.emit()

    @property
    def video_sec(self) -> str:
        return self._video_sec

    @video_sec.setter
    def video_sec(self, v: str) -> None:
        self._video_sec = v
        self.videoSecChange.emit()

    @property
    def fit_path(self) -> str:
        return self._fit_offset

    @fit_path.setter
    def fit_path(self, v: str) -> None:
        fit = get_fit_dict(v)
        self._fit_path = v
        self.fit = fit
        # Match timestamp to video?
        self.fitPathChange.emit()

    @property
    def fit_offset(self) -> int:
        return self._fit_offset

    @fit_offset.setter
    def fit_offset(self, v: int) -> None:
        self._fit_offset = v
        self.fitOffsetChange.emit()

    def load_set_fit(self, fit_path: str) -> FitDict:
        fit = get_fit_dict(fit_path)
        self.fit_offset = 0
        self.fit = fit
        return fit

    @property
    def fit(self) -> FitDict:
        return self._fit

    @fit.setter
    def fit(self, v: FitDict):
        if self._fit:
            self._fit.close()
        self._fit = v
        self.fitChange.emit()
