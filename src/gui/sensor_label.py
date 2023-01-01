from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
)


class SensorLabel(QVBoxLayout):
    def __init__(self, header: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._header = QLabel()
        self._header.setText(header)
        self.addWidget(self._header)

        self._value = QLabel()
        self._value.setText("--")
        self.addWidget(self._value)

        self._unit = ""

    def set_unit(self, v):
        self._unit = v

    def set_value(self, v):
        if v is None:
            self._value.setText("--")
        elif isinstance(v, str):
            self._value.setText(v + " " + self._unit)
        else:
            self._value.setText(str(v) + " " + self._unit)
