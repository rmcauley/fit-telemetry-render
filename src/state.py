from PySide6.QtCore import QObject, Signal

from fit import FitFile, get_fit_dict

from overlays.base import BaseOverlay
from overlays.default import DefaultOverlay


class AppState(QObject):
    _video_path: str
    _video_sec: int
    _fit_path: str
    _fit: FitFile
    _fit_offset: int
    export_path: str

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
        self.export_path = None

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
        return self._fit_path

    @fit_path.setter
    def fit_path(self, v: str) -> None:
        fit = get_fit_dict(v)
        self._fit_path = v
        self.fit = fit
        self.fitPathChange.emit()

    @property
    def fit_offset(self) -> int:
        return self._fit_offset

    @fit_offset.setter
    def fit_offset(self, v: int) -> None:
        self._fit_offset = v
        self.fitOffsetChange.emit()

    @property
    def fit(self) -> FitFile:
        return self._fit

    @fit.setter
    def fit(self, v: FitFile):
        if self._fit:
            self._fit.close()
        self._fit = v
        self.fitChange.emit()
