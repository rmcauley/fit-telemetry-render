from collections import OrderedDict

from PySide6.QtCore import QObject, Signal


class GoProState(QObject):
    _video_path: str
    _video_sec: int
    _fit: OrderedDict
    _fit_offset: int

    videoPathChange = Signal()
    videoSecChange = Signal()
    fitChange = Signal()
    fitOffsetChange = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._video_path = None
        self._fit = None
        self._fit_offset = 0

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
    def fit_offset(self) -> int:
        return self._fit_offset

    @fit_offset.setter
    def fit_offset(self, v: int) -> None:
        self._fit_offset = v
        self.fitOffsetChange.emit()

    @property
    def fit(self) -> OrderedDict:
        return self._fit

    @fit.setter
    def fit(self, v: OrderedDict):
        if self._fit:
            self._fit.close()
        self._fit = v
        self.fitChange.emit()
