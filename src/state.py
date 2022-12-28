from overlays.default import DefaultOverlay

class GoProState:
    def __init__(self):
        self._video_path = None
        self._fit_path = None
        self._fit_offset = 0
        self._overlay = DefaultOverlay(self)

    @property
    def video_path(self):
        return self._video_path

    @video_path.setter
    def video_path(self, v):
        self._video_path = v

    @property
    def fit_path(self):
        return self._fit_path

    @fit_path.setter
    def fit_path(self, v):
        self._fit_path = v

    @property
    def fit_offset(self):
        return self._fit_offset

    @fit_offset.setter
    def fit_offset(self, v):
        self._fit_offset = v

    @property
    def overlay(self):
        return self._overlay

    @overlay.setter
    def overlay(self, v):
        self._overlay = v