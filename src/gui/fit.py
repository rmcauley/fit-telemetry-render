import sys
from PyQt6.QtCore import QStandardPaths, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QScreen
from PyQt6.QtWidgets import (QApplication, QDialog, QFileDialog,
    QMainWindow, QSlider, QStyle, QToolBar, QWidget, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt6.QtMultimedia import (QAudio, QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
from PyQt6.QtMultimediaWidgets import QVideoWidget

from .color import Color

class FitLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        w = Color("red")
        self.addWidget(w)