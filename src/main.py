import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QToolBar,
)
from PySide6.QtGui import QAction

from state import AppState
from gui.export import ExportLayout
from gui.fit import FitLayout
from gui.video import VideoLayout
from gui.offset import OffsetLayout
from gui.preferences import PreferencesModal
from encode.start import start_encode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FIT Telemetry Overlay")

        state = AppState(self)
        self.state = state

        self.resize(state.size)
        self.move(state.pos)

        # Layout

        layout = QVBoxLayout()

        fit_video_layout = QHBoxLayout()
        fit_video_layout.addLayout(FitLayout(self.state))
        fit_video_layout.addLayout(VideoLayout(self.state))
        layout.addLayout(fit_video_layout, stretch=9)

        offset_layout = OffsetLayout(self.state)
        layout.addLayout(offset_layout, stretch=1)

        export_layout = ExportLayout(self.state, self)
        layout.addLayout(export_layout, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.show()

    def closeEvent(self, e):
        self.state.size = self.size()
        self.state.pos = self.pos()

        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    state = w.state
    app.exec()

    if state.export_path:
        start_encode(state)
