import os
import json

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtWebEngineWidgets import QWebEngineView

from state import AppState


class FitLayout(QVBoxLayout):
    _state: AppState

    def __init__(self, settings, state: AppState):
        super().__init__()

        self._settings = settings
        self._state = state

        self._web = QWebEngineView()
        self._web.setHtml("")
        self._web.loadFinished.connect(self.show_offset)
        self._web.loadFinished.connect(self.show_current)
        self.addWidget(self._web, stretch=11)

        tool_bar = QHBoxLayout()
        self.addLayout(tool_bar, stretch=1)

        self._open_button = QPushButton("Open Fit File")
        self._open_button.clicked.connect(self.open)
        tool_bar.addWidget(self._open_button)

        self._state.fitOffsetChange.connect(self.show_offset)
        self._state.fitOffsetChange.connect(self.show_current)
        self._state.videoSecChange.connect(self.show_current)
        self._state.fitChange.connect(self._on_fit_change)

        if self._state.fit:
            self._on_fit_change()

    def open(self):
        file_dialog = QFileDialog(self.parentWidget(), filter="fit(*.fit)")

        fits_location = self._settings.value(
            "fit_file_path",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            ),
        )
        file_dialog.setDirectory(fits_location)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            url = file_dialog.selectedUrls()[0]
            fit_path = url.toLocalFile()
            if url.isLocalFile():
                self._settings.setValue("fit_file_path", os.path.dirname(fit_path))
            self._state.fit_path = fit_path

    def _on_fit_change(self):
        fit = self._state.fit

        polyline = [
            (fit[key]["position_lat"], fit[key]["position_long"])
            for key in sorted(fit.keys())
            if "position_long" in fit[key]
        ]

        html = ""
        with open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "fit.html"),
            "r",
        ) as file:
            html = file.read()

        html = html.replace("$minLat", str(fit.min_lat))
        html = html.replace("$minLong", str(fit.min_long))
        html = html.replace("$maxLat", str(fit.max_lat))
        html = html.replace("$maxLong", str(fit.max_long))
        html = html.replace("$polyline", json.dumps(polyline))

        self._web.setHtml(html)

    def show_offset(self):
        if self._state.fit:
            offset = self._state.fit_offset or 0
            point = self._state.fit.get_point(offset)
            if point:
                lat = point["position_lat"]
                long = point["position_long"]
                self._web.page().runJavaScript(f"setOffsetPoint({lat}, {long})")

    def show_current(self):
        if self._state.fit:
            offset = (self._state.video_sec or 0) + self._state.fit_offset
            point = self._state.fit.get_point(offset)
            if point:
                lat = point["position_lat"]
                long = point["position_long"]
                self._web.page().runJavaScript(f"setCurrentPoint({lat}, {long})")

    def generate_folium_html(self):
        # Used to generate a new fit.html.  foliumn is not part of the requirements.
        import folium

        fit = self._state.fit
        fol = folium.Map()
        fol.fit_bounds(
            ((fit.min_lat, fit.min_long), (fit.max_lat, fit.max_long)), padding=(10, 10)
        )
        path = folium.PolyLine(locations=[])
        path.add_to(fol)
        fol.save("folium.html")
