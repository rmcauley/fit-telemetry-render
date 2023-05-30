from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QFormLayout,
    QCheckBox,
)

from state import AppState
from gears import KNOWN_REAR_MECHS, KNOWN_FRONT_MECHS


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

        layout = QVBoxLayout()

        front_gear_label = QLabel()
        front_gear_label.setText("Di2 Front Gearing")
        layout.addWidget(front_gear_label)
        front_gear = QComboBox()
        for name in KNOWN_FRONT_MECHS.keys():
            front_gear.addItem(name)
        self._front_gear = front_gear
        layout.addWidget(front_gear)

        layout.addWidget(Spacer())

        rear_gear_label = QLabel()
        rear_gear_label.setText("Di2 Rear Gearing")
        layout.addWidget(rear_gear_label)
        rear_gear = QComboBox()
        for name in KNOWN_REAR_MECHS.keys():
            rear_gear.addItem(name)
        self._rear_gear = rear_gear
        layout.addWidget(rear_gear)

        layout.addWidget(Spacer())

        settings_layout = QFormLayout()

        encoder_label = QLabel()
        encoder_label.setText("Video Encoder")
        layout.addWidget(encoder_label)
        encoder = QComboBox()
        encoder.addItem("nvidia")
        encoder.addItem("libx264")
        self._encoder = encoder
        layout.addWidget(encoder)

        layout.addLayout(settings_layout)

        layout.addWidget(Spacer())

        zone_layout = QFormLayout()

        self._show_alt = QCheckBox()
        zone_layout.addRow("Show Altitude", self._show_alt)

        self._show_grade = QCheckBox()
        zone_layout.addRow("Show Grade", self._show_grade)

        zone1 = QLineEdit()
        zone1.setValidator(QIntValidator())
        self._hr_zone_1 = zone1
        zone_layout.addRow("Zone 1 Min HR", zone1)

        zone2 = QLineEdit()
        zone2.setValidator(QIntValidator())
        self._hr_zone_2 = zone2
        zone_layout.addRow("Zone 2 Min HR", zone2)

        zone3 = QLineEdit()
        zone3.setValidator(QIntValidator())
        self._hr_zone_3 = zone3
        zone_layout.addRow("Zone 3 Min HR", zone3)

        zone4 = QLineEdit()
        zone4.setValidator(QIntValidator())
        self._hr_zone_4 = zone4
        zone_layout.addRow("Zone 4 Min HR", zone4)

        layout.addLayout(zone_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

        self.reset_values()

    def reset_values(self):
        self._front_gear.setCurrentText(
            next(
                (
                    k
                    for k, v in KNOWN_FRONT_MECHS.items()
                    if v == self._state.front_gears
                ),
                "Unknown",
            )
        )
        self._rear_gear.setCurrentText(
            next(
                (k for k, v in KNOWN_REAR_MECHS.items() if v == self._state.rear_gears),
                "Unknown",
            )
        )
        self._encoder.setCurrentText(self._state.encoder)
        self._hr_zone_4.setText(str(self._state.hr_zones[0][0]))
        self._hr_zone_3.setText(str(self._state.hr_zones[1][0]))
        self._hr_zone_2.setText(str(self._state.hr_zones[2][0]))
        self._hr_zone_1.setText(str(self._state.hr_zones[3][0]))
        self._show_alt.setCheckState(
            Qt.CheckState.Checked if self._state.show_alt else Qt.CheckState.Unchecked
        )
        self._show_grade.setCheckState(
            Qt.CheckState.Checked if self._state.show_grade else Qt.CheckState.Unchecked
        )

    def accept(self):
        self._state.front_gears = next(
            (
                v
                for k, v in KNOWN_FRONT_MECHS.items()
                if k == self._front_gear.currentText()
            ),
            [],
        )
        self._state.rear_gears = next(
            (
                v
                for k, v in KNOWN_REAR_MECHS.items()
                if k == self._rear_gear.currentText()
            ),
            [],
        )
        self._state.encoder = self._encoder.currentText()
        self._state.hr_zones = [
            [int(self._hr_zone_4.text()), (100, 0, 100, 255)],
            [int(self._hr_zone_3.text()), (100, 0, 0, 255)],
            [int(self._hr_zone_2.text()), (100, 77, 0, 255)],
            [int(self._hr_zone_1.text()), (0, 100, 0, 255)],
            [-1, (0, 86, 147, 255)],
        ]
        self._state.show_alt = (
            True if self._show_alt.checkState() == Qt.CheckState.Checked else False
        )
        self._state.show_grade = (
            True if self._show_grade.checkState() == Qt.CheckState.Checked else False
        )
        self.hide()

    def reject(self):
        self.hide()
        self.reset_values()
