import os
import sys

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
    QVideoSink,
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

        self._audio_output = QAudioOutput()

        self._input_video_sink = QVideoSink()
        self._input_video_sink.videoFrameChanged.connect(self._handle_overlay)

        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._player.errorOccurred.connect(self._player_error)
        self._player.playbackStateChanged.connect(self.update_buttons)
        self._player.setVideoSink(self._input_video_sink)

        self._video_widget = QVideoWidget()
        self._output_video_sink = self._video_widget.videoSink()
        self.addWidget(self._video_widget, stretch=10)

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

        self._volume_slider = QSlider()
        self._volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(100)
        self._volume_slider.setValue(self._audio_output.volume())
        self._volume_slider.setTickInterval(10)
        self._volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._volume_slider.setToolTip("Volume")
        self._volume_slider.valueChanged.connect(self._audio_output.setVolume)
        tool_bar.addWidget(self._volume_slider, stretch=1)

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
            self._player.play()

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

    def _handle_overlay(self, video_frame: QVideoFrame):
        if self._state.fit:
            k = round(video_frame.startTime() / 1000000)
            fit_frame = self._state.fit.get(k, {})
            self._speed_at.setText(str(fit_frame.get("speed", "--")))
        self._video_widget.videoSink().setVideoFrame(video_frame)
