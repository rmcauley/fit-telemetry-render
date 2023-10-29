# This file is for developing overlays.
# Place a "preview.png" file in the same directory as this, adjust
# the overlay import to your overlay if necessary, and run this file.

import sys
import os
import importlib
import datetime

from PySide6.QtCore import QSize
from PySide6.QtCore import QFileSystemWatcher
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel

from PIL import Image

import overlays.default as overlay
from state import AppState
from fit import FitFile

fit_frame = {
    "timestamp": datetime.datetime(
        2022, 12, 18, 15, 31, 39, tzinfo=datetime.timezone.utc
    ),
    "position_lat": 28.36728979130319,
    "position_long": -16.71821173776546,
    "gps_accuracy": 10,
    "distance": 51768.25,
    "speed": 22,
    "battery_soc": 73.0,
    "temperature": 22,
    "altitude": 1232.79999999999995,
    "grade": 5,
    "ascent": 1601,
    "descent": 1417,
    "cadence": 75,
    "front_gear_num": 1,
    "rear_gear_num": 5,
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
    "front_gear_num": "T",
    "rear_gear_num": "T",
}
fit_max = {
    "speed": 35,
}
fit_min = {
    "speed": 0,
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        pil_im = Image.open(
            os.path.join(os.path.dirname(__file__), "preview.png")
        ).convert("RGBA")

        self.resize(QSize(pil_im.width / 3, pil_im.height / 3))

        watcher = QFileSystemWatcher(self)
        watcher.addPath("./src/overlays/default.py")
        watcher.addPath("./preview.png")
        watcher.fileChanged.connect(self.on_overlay_changed)

        self.state = AppState(self)
        self.fit = FitFile()
        self.fit.units = fit_units
        self.fit.max = fit_max
        self.fit.min = fit_min
        self.central_widget = QLabel()
        self.setCentralWidget(self.central_widget)
        self.show()
        self.render_preview()

    def on_overlay_changed(self):
        importlib.reload(overlay)
        self.render_preview()

    def render_preview(self):
        pil_im = Image.open(
            os.path.join(os.path.dirname(__file__), "preview.png")
        ).convert("RGBA")

        o = overlay.DefaultOverlay(
            self.state.get_state_for_overlay(), pil_im.width, pil_im.height
        ).overlay(fit_frame)
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
