import sys
import logging

from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from PySide6.QtCore import QSettings, QPoint, QSize

from state import GoProState
from gui.export import ExportLayout
from gui.fit import FitLayout
from gui.video import VideoLayout
from gui.offset import OffsetLayout

# removes warning: deprecated pixel format used
logging.getLogger("libav").setLevel(logging.ERROR)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GoPro Telemetry")

        self.settings = QSettings("rmcauley", "GoPro Telemetry")
        self.state = GoProState()

        self.resize(self.settings.value("size", QSize(270, 225)))
        self.move(self.settings.value("pos", QPoint(50, 50)))

        layout = QVBoxLayout()

        fit_video_layout = QHBoxLayout()
        fit_video_layout.addLayout(FitLayout(self.settings, self.state))
        fit_video_layout.addLayout(VideoLayout(self.settings, self.state))
        layout.addLayout(fit_video_layout, stretch=9)

        offset_layout = OffsetLayout(self.settings, self.state)
        layout.addLayout(offset_layout, stretch=1)

        export_layout = ExportLayout(self.settings, self.state)
        layout.addLayout(export_layout, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.show()

        fit_path = self.settings.value("fit_path", "", str)
        video_path = self.settings.value("video_path", "", str)
        video_sec = self.settings.value("video_sec", 0, int)
        fit_offset = self.settings.value("fit_offset", 0, int)
        if fit_path and fit_path != "-1":
            try:
                self.state.fit_path = fit_path
                if fit_offset and fit_offset != -1:
                    self.state.fit_offset = fit_offset
            except Exception as e:
                print(e)
                pass
        if video_path and video_path != "-1":
            self.state.video_path = video_path
        if video_sec and video_sec != -1:
            self.state.video_sec = video_sec

    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        if self.state.fit_path:
            self.settings.setValue("fit_path", self.state.fit_path)
        if self.state.video_path:
            self.settings.setValue("video_path", self.state.video_path)
        if self.state.fit_offset:
            self.settings.setValue("fit_offset", self.state.fit_offset)
        if self.state.video_sec:
            self.settings.setValue("video_sec", self.state.video_sec)

        self.settings.sync()

        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
