import sys
from math import floor

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QSlider,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtMultimedia import (
    QAudioOutput,
    QMediaFormat,
    QMediaPlayer,
)
from PySide6.QtMultimediaWidgets import QVideoWidget

from state import AppState
from overlays.base import BaseOverlay

from .sensor_label import SensorLabel

MP4 = "video/mp4"


def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.ConversionMode.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class VideoLayout(QVBoxLayout):
    _overlay: BaseOverlay

    def __init__(self, state: AppState):
        super().__init__()

        self._state = state
        self._overlay = None
        self._last_updated_pos = 0

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

        sensors = QHBoxLayout()
        self._sensor_speed = SensorLabel("Speed")
        sensors.addLayout(self._sensor_speed)
        self._sensor_bpm = SensorLabel("BPM")
        sensors.addLayout(self._sensor_bpm)
        self._sensor_rpm = SensorLabel("RPM")
        sensors.addLayout(self._sensor_rpm)
        self._sensor_elev = SensorLabel("Alt")
        sensors.addLayout(self._sensor_elev)
        self.addLayout(sensors, stretch=1)

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
        self._seeker.setMaximum(1000)
        self._seeker.setSingleStep(1000)
        self._seeker.setValue(0)
        self._seeker.setDisabled(True)
        self._seeker.sliderMoved.connect(self._seek)
        tool_bar.addWidget(self._seeker, stretch=1)

        self.update_buttons(self._player.playbackState())
        self._mime_types = []

        self._state.videoPathChange.connect(self._open_video)
        self._state.fitOffsetChange.connect(self._update_sensors)
        self._state.fitChange.connect(self._update_sensors_units)

    def closeEvent(self, event):
        self._ensure_stopped()
        event.accept()

    def open(self):
        self._ensure_stopped()
        self._state.open_video_dialog()

    def _open_video(self):
        self._player.setSource(self._state.video_path)
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
            self._update_sensors()
            self._seeker.setValue(pos_ms)
            self._state.video_sec = pos_s

    def _update_sensors(self):
        if self._state.fit and self._last_updated_pos:
            fit_frame = self._state.fit.get(
                self._state.fit_offset + self._last_updated_pos, {}
            )
            self._sensor_speed.set_value(fit_frame.get("speed"))
            self._sensor_bpm.set_value(fit_frame.get("heart_rate"))
            self._sensor_rpm.set_value(fit_frame.get("cadence"))
            self._sensor_elev.set_value(fit_frame.get("altitude"))

    def _update_sensors_units(self):
        self._sensor_speed.set_unit(self._state.fit.units.get("speed", ""))
        self._sensor_bpm.set_unit(self._state.fit.units.get("heart_rate", ""))
        self._sensor_rpm.set_unit(self._state.fit.units.get("cadence", ""))
        self._sensor_elev.set_unit(self._state.fit.units.get("altitude", ""))

    def _duration_changed(self, v):
        self._seeker.setDisabled(False)
        self._seeker.setValue(0)
        self._seeker.setMaximum(v)

    def _seek(self, v):
        self._player.setPosition(v)
