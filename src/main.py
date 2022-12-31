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
from gui.export import ExportWidget
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

        export_layout = QHBoxLayout()
        export_layout.addWidget(ExportWidget())
        layout.addLayout(export_layout, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def closeEvent(self, e):
        # Write window size and position to config file
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        e.accept()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
