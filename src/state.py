import os

from PySide6.QtCore import QObject, Signal, QSize, QPoint, QSettings, QStandardPaths
from PySide6.QtWidgets import QFileDialog, QDialog
from PySide6.QtMultimedia import QMediaFormat

from fit import FitFile, get_fit_dict
from gears import KNOWN_REAR_MECHS, KNOWN_FRONT_MECHS
from overlays.default import DefaultOverlay

MP4 = "video/mp4"


def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.ConversionMode.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class StateForOverlay:
    overlay_class = DefaultOverlay
    fit_units: dict
    front_gears: list
    rear_gears: list
    hr_zones: list
    show_alt: bool
    show_grade: bool

    def __init__(
        self,
        fit_units: dict,
        front_gears: list,
        rear_gears: list,
        hr_zones: list,
        show_alt: bool,
        show_grade: bool,
    ):
        self.fit_units = fit_units
        self.front_gears = front_gears
        self.rear_gears = rear_gears
        self.hr_zones = hr_zones
        self.show_alt = show_alt
        self.show_grade = show_grade


class AppState(QObject):
    fit: FitFile
    _export_path: str

    _mime_types: list

    videoPathChange = Signal(str)
    videoSecChange = Signal(int)
    fitChange = Signal(FitFile)
    fitOffsetChange = Signal(int)
    fitPathChange = Signal(str)
    exportPathChange = Signal(str)

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._settings = QSettings("rmcauley", "fitrender")
        self._parent = parent

        self.fit = None
        self.export_path = None

        self._mime_types = []

        self.fitPathChange.connect(self._on_fit_path_change)

        try:
            self._on_fit_path_change(self.fit_path)
        except Exception:
            self.fit_path = ""

    def __delete__(self) -> None:
        self._settings.sync()

    def get_state_for_overlay(self):
        return StateForOverlay(
            self.fit.units,
            self.front_gears,
            self.rear_gears,
            self.hr_zones,
            self.show_alt,
            self.show_grade,
        )

    @property
    def video_path(self) -> str:
        return self._settings.value("video_path", "")

    @video_path.setter
    def video_path(self, v: str) -> None:
        self._settings.setValue("video_path", v)
        self.videoPathChange.emit(v)

    @property
    def video_sec(self) -> int:
        return self._settings.value("video_sec", 0)

    @video_sec.setter
    def video_sec(self, v: str) -> None:
        self._settings.setValue("video_sec", v)
        self.videoSecChange.emit(v)

    @property
    def fit_path(self) -> str:
        return self._settings.value("fit_path", "")

    @fit_path.setter
    def fit_path(self, v: str) -> None:
        self._settings.setValue("fit_path", v)
        self.fitPathChange.emit(v)

    def _on_fit_path_change(self, v: str) -> None:
        if self.fit:
            self.fit.close()
        if v:
            self.fit = get_fit_dict(v)
            self.fitChange.emit(self.fit)

    @property
    def fit_offset(self) -> int:
        return self._settings.value("fit_offset", 0)

    @fit_offset.setter
    def fit_offset(self, v: int) -> None:
        self._settings.setValue("fit_offset", v)
        self.fitOffsetChange.emit(v)

    @property
    def size(self) -> QSize:
        return self._settings.value("size", QSize(270, 225))

    @size.setter
    def size(self, v: QSize) -> None:
        self._settings.setValue("size", v)

    @property
    def pos(self) -> QPoint:
        return self._settings.value("pos", QPoint(50, 50))

    @pos.setter
    def pos(self, v: QPoint) -> None:
        self._settings.setValue("pos", v)

    @property
    def fit_dialog_path(self) -> str:
        return self._settings.value(
            "fit_dialog_path",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            ),
        )

    @fit_dialog_path.setter
    def fit_dialog_path(self, v: str) -> None:
        self._settings.setValue("fit_dialog_path", v)

    @property
    def video_import_dialog_path(self) -> str:
        return self._settings.value(
            "video_import_dialog_path",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            ),
        )

    @video_import_dialog_path.setter
    def video_import_dialog_path(self, v: str) -> None:
        self._settings.setValue("video_import_dialog_path", v)

    @property
    def video_export_dialog_path(self) -> str:
        return self._settings.value(
            "video_export_dialog_path",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            ),
        )

    @video_export_dialog_path.setter
    def video_export_dialog_path(self, v: str) -> None:
        self._settings.setValue("video_export_dialog_path", v)

    @property
    def encoder(self) -> str:
        return self._settings.value("encoder", "libx265")

    @encoder.setter
    def encoder(self, v: str) -> None:
        self._settings.setValue("encoder", v)

    @property
    def hr_zones(self) -> list:
        return self._settings.value(
            "hr_zones",
            [
                [173, (100, 0, 100, 255)],
                [164, (100, 0, 0, 255)],
                [149, (100, 77, 0, 255)],
                [134, (0, 100, 0, 255)],
                [-1, (0, 86, 147, 255)],
            ],
        )

    @hr_zones.setter
    def hr_zones(self, v: list) -> None:
        self._settings.setValue("hr_zones", v)

    @property
    def front_gears(self) -> list:
        # Default is 2-ring Shimano road
        return self._settings.value(
            "front_gears", KNOWN_FRONT_MECHS["Shimano Road 34,50"]
        )

    @front_gears.setter
    def front_gears(self, v: list) -> None:
        self._settings.setValue("front_gears", v)

    @property
    def rear_gears(self) -> list:
        return self._settings.value(
            "rear_gears", KNOWN_REAR_MECHS["Shimano Road 12spd 11-34"]
        )

    @rear_gears.setter
    def rear_gears(self, v: list) -> None:
        self._settings.setValue("rear_gears", v)

    @property
    def export_path(self) -> int:
        return self._export_path

    @export_path.setter
    def export_path(self, v: str) -> None:
        self._export_path = v
        self.exportPathChange.emit(v)

    @property
    def show_alt(self) -> list:
        return self._settings.value("show_alt", True)

    @show_alt.setter
    def show_alt(self, v: bool) -> None:
        self._settings.setValue("show_alt", v)

    @property
    def show_grade(self) -> list:
        return self._settings.value("show_grade", True)

    @show_grade.setter
    def show_grade(self, v: bool) -> None:
        self._settings.setValue("show_grade", v)

    def open_fit_dialog(self):
        file_dialog = QFileDialog(self._parent, filter="fit(*.fit)")
        file_dialog.setDirectory(self.fit_dialog_path)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            url = file_dialog.selectedUrls()[0]
            fit_path = url.toLocalFile()
            if url.isLocalFile():
                self.fit_dialog_path = os.path.dirname(fit_path)
            self.fit_path = fit_path

    def open_export_dialog(self):
        file_dialog = QFileDialog(self._parent, filter="mp4(*.mp4)")
        file_dialog.setDirectory(self.video_export_dialog_path)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            self.export_path = file_dialog.selectedUrls()[0].toLocalFile()
            self.exportPathChange.emit(self.export_path)
        else:
            self.export_path = None

    def open_video_dialog(self):
        file_dialog = QFileDialog(self._parent)

        if not self._mime_types:
            self._mime_types = get_supported_mime_types()
            if MP4 not in self._mime_types:
                self._mime_types.append(MP4)

        file_dialog.setMimeTypeFilters(self._mime_types)

        default_mimetype = MP4
        if default_mimetype in self._mime_types:
            file_dialog.selectMimeTypeFilter(default_mimetype)

        file_dialog.setDirectory(self.video_import_dialog_path)
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            url = file_dialog.selectedUrls()[0]
            if url.isLocalFile():
                self.video_path = url.toLocalFile()
