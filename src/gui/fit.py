import os
import sys
from PySide6.QtCore import QStandardPaths, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
    QMainWindow, QSlider, QStyle, QToolBar, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QTableWidget, QTableWidgetItem)
from PySide6.QtMultimedia import (QAudio, QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
from PySide6.QtMultimediaWidgets import QVideoWidget
import fitdecode

from .color import Color
from state import GoProState
from fit import get_fit_dict

class FitLayout(QVBoxLayout):
    _state: GoProState

    def __init__(self, settings, state: GoProState):
        super().__init__()

        self._settings = settings
        self._state = state

        self._table = QTableWidget()
        self._table.setSortingEnabled(False)
        self.addWidget(self._table, stretch=10)

        tool_bar = QHBoxLayout()
        self.addLayout(tool_bar, stretch=1)

        self._open_button = QPushButton("Open Fit File")
        self._open_button.clicked.connect(self.open)
        tool_bar.addWidget(self._open_button, stretch=0)

    def open(self):
        file_dialog = QFileDialog(self.parentWidget(), filter="fit(*.fit)")

        fits_location = self._settings.value("fit_file_path", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation))
        file_dialog.setDirectory(fits_location)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            url = file_dialog.selectedUrls()[0]
            fit_path = url.toLocalFile()
            if url.isLocalFile():
                self._settings.setValue("fit_file_path", os.path.dirname(fit_path))
            self._state.fit_path = fit_path
            self._state.fit = get_fit_dict(fit_path)
            self._load_table()
    
    def _load_table(self):
        fit = self._state.fit
        self._table.setRowCount(min(len(fit), 100))
        self._table.setColumnCount(1)
        self._table.setHorizontalHeaderLabels(["Speed"])
        
        i = 0
        for k, v in self._state.fit.items():
            speed = v.get("speed")
            self._table.setItem(i, 0, QTableWidgetItem(f"{speed}"))
            if i > 100:
                break
            i += 1