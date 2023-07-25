from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
)
from state import AppState
from .preferences import PreferencesModal


class ExportLayout(QHBoxLayout):
    _state: AppState

    def __init__(self, state: AppState, parent):
        super().__init__()

        self._state = state

        hbox = QHBoxLayout()

        preferences_modal = PreferencesModal(state, parent)
        preferences = QPushButton(text="Preferences")
        preferences.clicked.connect(preferences_modal.show)
        hbox.addWidget(preferences)

        self.youtube_button = QPushButton(text="Youtube Merge")
        self.youtube_button.clicked.connect(state.open_youtube_dialog)
        hbox.addWidget(self.youtube_button)

        self.button = QPushButton(text="Export")
        self.button.clicked.connect(state.open_export_dialog)
        hbox.addWidget(self.button)

        self.addLayout(hbox)
