# This file is for developing overlays.
# Place a "preview.png" file in the same directory as this, adjust
# the overlay import to your overlay if necessary, and run this file.

import sys
import importlib
import datetime

from PySide6.QtCore import QSize
from PySide6.QtCore import QFileSystemWatcher
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel

from PIL import Image

import src.overlays.default as overlay

fit_frame = {
    "timestamp": datetime.datetime(
        2022, 12, 18, 15, 31, 39, tzinfo=datetime.timezone.utc
    ),
    "position_lat": 28.36728979130319,
    "position_long": -16.71821173776546,
    "gps_accuracy": 10,
    "distance": 51768.25,
    "speed": 20,
    "battery_soc": 73.0,
    "temperature": 22,
    "altitude": 1232.79999999999995,
    "grade": 5,
    "ascent": 1601,
    "descent": 1417,
    "cadence": 75,
    "front_gear_num": 1,
    "rear_gear_num": 1,
    "heart_rate": 142,
    "calories": 3487,
}
fit_units = {
    "position_lat": "semicircles",
    "position_long": "semicircles",
    "gps_accuracy": "m",
    "distance": "m",
    "speed": "km/h",
    "battery_soc": "percent",
    "temperature": "C",
    "altitude": "m",
    "grade": "%",
    "ascent": "m",
    "descent": "m",
    "cadence": "rpm",
    "heart_rate": "bpm",
    "calories": "kcal",
}


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
        pil_im = Image.open("preview.png").convert("RGBA")
        o = overlay.DefaultOverlay(pil_im.width, pil_im.height, (0, 0, 0, 0)).overlay(
            fit_frame, fit_units
        )
        pil_im.alpha_composite(o)
        pil_im = pil_im.resize(
            (self.central_widget.width(), self.central_widget.height()),
            resample=Image.Resampling.LANCZOS,
        )
        self.central_widget.setPixmap(pil_im.toqpixmap())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
