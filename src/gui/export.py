import os

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QDialog,
)
from state import GoProState

from encode.start import start_encode


class ExportLayout(QHBoxLayout):
    _state: GoProState

    def __init__(self, settings, state: GoProState):
        super().__init__()

        self._settings = settings
        self._state = state

        self.button = QPushButton(text="Export")
        self.button.clicked.connect(self.start)
        self.addWidget(self.button)

    def start(self):
        file_dialog = QFileDialog(self.parentWidget(), filter="mp4(*.mp4)")

        out_location = self._settings.value(
            "export_file_location",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            ),
        )
        file_dialog.setDirectory(out_location)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            url = file_dialog.selectedUrls()[0]
            export_location = url.toLocalFile()
            start_encode(self.parentWidget(), self._state, export_location)
