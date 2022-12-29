import sys
import logging

from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import QSettings, QPoint, QSize

from state import GoProState
from gui.export import ExportWidget
from gui.fit import FitLayout
from gui.video import VideoLayout

logging.getLogger('libav').setLevel(logging.ERROR)  # removes warning: deprecated pixel format used

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('rmcauley', 'GoPro Telemetry')
        self.state = GoProState()

        self.setWindowTitle("GoPro Telemetry")

        self.resize(self.settings.value("size", QSize(270, 225)))
        self.move(self.settings.value("pos", QPoint(50, 50)))

        layout = QVBoxLayout()
        fit_video_layout = QHBoxLayout()
        layout.addLayout(fit_video_layout, 9)
        export_layout = QHBoxLayout()
        layout.addLayout(export_layout, 1)

        fit_video_layout.addLayout(FitLayout(self.settings, self.state), 1)
        fit_video_layout.addLayout(VideoLayout(self.settings, self.state), 3)
        export_layout.addWidget(ExportWidget())

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