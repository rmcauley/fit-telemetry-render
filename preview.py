import sys
import importlib

from PySide6.QtCore import QSize, Qt
from PySide6.QtCore import QFileSystemWatcher
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout

from PIL import Image

import src.overlays.default as overlay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(QSize(1024, 768))

        watcher = QFileSystemWatcher(self)
        watcher.addPath("./src/overlays/default.py")
        watcher.addPath("./preview.png")
        watcher.fileChanged.connect(self.on_overlay_changed)

        self.central_widget = QLabel()
        self.setCentralWidget(self.central_widget)
        self.show()
        self.render_preview()

    def on_overlay_changed(self):
        importlib.reload(overlay)
        self.render_preview()

    def render_preview(self):
        fit_frame = {"speed": "20"}
        fit_units = {"speed": "km/h"}

        pil_im = Image.open("preview.png").convert("RGBA")
        o = overlay.DefaultOverlay(pil_im.width, pil_im.height).overlay(
            fit_frame, fit_units
        )
        pil_im.alpha_composite(o)
        pil_im = pil_im.resize(
            (self.central_widget.width(), self.central_widget.height()),
            resample=Image.Resampling.LANCZOS,
        )
        self.central_widget.setPixmap(pil_im.toqpixmap())


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
