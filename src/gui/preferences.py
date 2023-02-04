from PySide6.QtCore import QObject
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QFormLayout,
)

from state import AppState

known_rear_mechs = {"11,12,13,14,15,17,19,21,24,27,30,34": "Shimano Road 12spd"}

known_front_mechs = {
    "34,50": "Shimano Road",
}


class Spacer(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(" ")


class PreferencesModal(QDialog):
    def __init__(self, state: AppState, parent: QObject, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._state = state

        self.setModal(True)

        self.setWindowTitle("Preferences")

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self._prefs = {
            "front_gears": ",".join(state.front_gears),
            "rear_gears": ",".join(state.rear_gears),
            "encoder": state.encoder,
            "hr_zone_1": str(state.hr_zones[3][0]),
            "hr_zone_2": str(state.hr_zones[2][0]),
            "hr_zone_3": str(state.hr_zones[1][0]),
            "hr_zone_4": str(state.hr_zones[0][0]),
        }

        layout = QVBoxLayout()

        front_gear_label = QLabel()
        front_gear_label.setText("Di2 Front Gearing")
        layout.addWidget(front_gear_label)
        front_gear = QComboBox()
        for gears, name in known_front_mechs.items():
            front_gear.addItem(f"{name}: {gears}")
        front_gear.currentIndexChanged.connect(self._front_gear_change)
        layout.addWidget(front_gear)

        layout.addWidget(Spacer())

        rear_gear_label = QLabel()
        rear_gear_label.setText("Di2 Rear Gearing")
        layout.addWidget(rear_gear_label)
        rear_gear = QComboBox()
        for gears, name in known_rear_mechs.items():
            show_gears = gears.split(",")
            rear_gear.addItem(f"{name}: {show_gears[0]}-{show_gears[-1]}")
        rear_gear.currentIndexChanged.connect(self._rear_gear_change)
        layout.addWidget(rear_gear)

        layout.addWidget(Spacer())

        settings_layout = QFormLayout()

        encoder_label = QLabel()
        encoder_label.setText("Video Encoder")
        layout.addWidget(encoder_label)
        encoder = QComboBox()
        encoder.addItem("nvidia")
        encoder.addItem("libx264")
        encoder.currentTextChanged.connect(self._encoder_change)
        layout.addWidget(encoder)

        layout.addLayout(settings_layout)

        layout.addWidget(Spacer())

        zone_layout = QFormLayout()

        zone1 = QLineEdit(self._prefs["hr_zone_1"])
        zone1.setValidator(QIntValidator())
        zone1.textChanged.connect(self._hr_zone_1_change)
        zone_layout.addRow("Zone 1 Min HR", zone1)

        zone2 = QLineEdit(self._prefs["hr_zone_2"])
        zone2.setValidator(QIntValidator())
        zone2.textChanged.connect(self._hr_zone_2_change)
        zone_layout.addRow("Zone 2 Min HR", zone2)

        zone3 = QLineEdit(self._prefs["hr_zone_3"])
        zone3.setValidator(QIntValidator())
        zone3.textChanged.connect(self._hr_zone_3_change)
        zone_layout.addRow("Zone 3 Min HR", zone3)

        zone4 = QLineEdit(self._prefs["hr_zone_4"])
        zone4.setValidator(QIntValidator())
        zone4.textChanged.connect(self._hr_zone_4_change)
        zone_layout.addRow("Zone 4 Min HR", zone4)

        layout.addLayout(zone_layout)

        self.setLayout(layout)

    def accept(self):
        self._state.front_gears = self._prefs["front_gears"]
        self._state.rear_gears = self._prefs["rear_gears"]
        self._state.encoder = self._prefs["encoder"]
        self._state.hr_zones[0] = self._prefs["hr_zone_4"]
        self._state.hr_zones[1] = self._prefs["hr_zone_3"]
        self._state.hr_zones[2] = self._prefs["hr_zone_2"]
        self._state.hr_zones[3] = self._prefs["hr_zone_1"]

    def reject(self):
        pass

    def _front_gear_change(self, index):
        pass

    def _rear_gear_change(self, index):
        pass

    def _encoder_change(self, value):
        pass

    def _hr_zone_1_change(self, value):
        pass

    def _hr_zone_2_change(self, value):
        pass

    def _hr_zone_3_change(self, value):
        pass

    def _hr_zone_4_change(self, value):
        pass
