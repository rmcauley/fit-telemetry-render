from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QDialog,
    QApplication,
)
from state import AppState


class ExportLayout(QHBoxLayout):
    _state: AppState

    def __init__(self, settings, state: AppState):
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
            self._state.export_path = url.toLocalFile()
            for window in QApplication.topLevelWidgets():
                window.close()
        else:
            self._state.export_path = None
