from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSlider,
    QHBoxLayout,
)
from state import AppState


class OffsetLayout(QHBoxLayout):
    _state: AppState

    def __init__(self, state: AppState):
        super().__init__()

        self._state = state

        self._slider = QSlider()
        self._slider.setOrientation(Qt.Orientation.Horizontal)
        self._slider.setMinimum(0)
        self._slider.setMaximum(30000)
        self._slider.setValue(self._state.fit_offset)
        self._slider.setSingleStep(1)
        self._slider.valueChanged.connect(self.seek)
        self.addWidget(self._slider)

        self._state.fitChange.connect(self.on_fit)

    def seek(self, v):
        self._state.fit_offset = v

    def on_fit(self):
        keys = self._state.fit.keys()
        self._slider.setMinimum(min(keys) - round(len(keys) * 0.1))
        self._slider.setMaximum(max(keys))
        self._slider.setValue(self._state.fit_offset)
