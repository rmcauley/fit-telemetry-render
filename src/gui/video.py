import os
import sys
from math import floor

from PySide6.QtCore import QStandardPaths, Qt, QSettings
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QSlider,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtMultimedia import (
    QAudioOutput,
    QMediaFormat,
    QMediaPlayer,
    QVideoFrame,
)
from PySide6.QtMultimediaWidgets import QVideoWidget

from state import GoProState

MP4 = "video/mp4"


def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.ConversionMode.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class VideoLayout(QVBoxLayout):
    def __init__(self, settings: QSettings, state: GoProState):
        super().__init__()

        self._settings = settings
        self._state = state
        self._last_updated_pos = None

        self._audio_output = QAudioOutput()
        self._audio_output.setMuted(True)

        self._video_widget = QVideoWidget()
        self.addWidget(self._video_widget, stretch=10)

        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._player.errorOccurred.connect(self._player_error)
        self._player.playbackStateChanged.connect(self.update_buttons)
        self._player.durationChanged.connect(self._duration_changed)
        self._player.positionChanged.connect(self._position_changed)
        self._player.setVideoOutput(self._video_widget)

        sensors_at = QHBoxLayout()
        self._speed_at = QLabel()
        self._speed_at.setText("hello")
        sensors_at.addWidget(self._speed_at)
        self.addLayout(sensors_at, stretch=1)

        tool_bar = QHBoxLayout()
        self.addLayout(tool_bar, stretch=1)

        self._open_button = QPushButton("Open Video")
        self._open_button.clicked.connect(self.open)
        tool_bar.addWidget(self._open_button, stretch=0)

        self._play_action = QPushButton("Play")
        self._play_action.clicked.connect(self._player.play)
        tool_bar.addWidget(self._play_action, stretch=0)

        self._pause_action = QPushButton("Pause")
        self._pause_action.clicked.connect(self._player.pause)
        tool_bar.addWidget(self._pause_action, stretch=0)

        self._seeker = QSlider()
        self._seeker.setOrientation(Qt.Orientation.Horizontal)
        self._seeker.setMinimum(0)
        self._seeker.setMaximum(100)
        self._seeker.setValue(0)
        self._seeker.setDisabled(True)
        self._seeker.sliderMoved.connect(self._seek)
        tool_bar.addWidget(self._seeker, stretch=1)

        self.update_buttons(self._player.playbackState())
        self._mime_types = []

    def closeEvent(self, event):
        self._ensure_stopped()
        event.accept()

    def open(self):
        self._ensure_stopped()
        file_dialog = QFileDialog(self.parentWidget())

        if not self._mime_types:
            self._mime_types = get_supported_mime_types()
            if MP4 not in self._mime_types:
                self._mime_types.append(MP4)

        file_dialog.setMimeTypeFilters(self._mime_types)

        default_mimetype = MP4
        if default_mimetype in self._mime_types:
            file_dialog.selectMimeTypeFilter(default_mimetype)

        movies_location = self._settings.value(
            "movie_file_path",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.MoviesLocation
            ),
        )
        file_dialog.setDirectory(movies_location)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._overlay = None
            if url.isLocalFile():
                self._settings.setValue(
                    "movie_file_path", os.path.dirname(url.toLocalFile())
                )
            self._player.setSource(url)
            self._player.setPosition(0)

    def _ensure_stopped(self):
        if self._player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
            self._player.stop()

    def update_buttons(self, state):
        self._play_action.setEnabled(state != QMediaPlayer.PlaybackState.PlayingState)
        self._pause_action.setEnabled(state == QMediaPlayer.PlaybackState.PlayingState)

    def show_status_message(self, message):
        pass
        # self.statusBar().showMessage(message, 5000)

    def _player_error(self, error, error_string):
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)

    def _position_changed(self, pos_ms):
        pos_s = floor(pos_ms / 1000)

        if self._last_updated_pos != pos_s:
            self._last_updated_pos = pos_s
            if self._state.fit:
                fit_frame = self._state.fit.get(pos_s, {})
                self._speed_at.setText(str(fit_frame.get("speed", "--")))
            self._seeker.setValue(pos_ms)
            self._state.video_sec = pos_s

    def _duration_changed(self, v):
        self._seeker.setDisabled(False)
        self._seeker.setValue(0)
        self._seeker.setMaximum(v)

    def _seek(self, v):
        self._player.setPosition(v)
