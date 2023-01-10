import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog, QWidget

from state import GoProState

from .movie import get_movies
from .overlay import encode_overlay
from .final import encode_final
from .concat import concat


def start_encode(parent: QWidget, state: GoProState, out: str) -> None:
    progress = QProgressDialog("Encoding Overlay", "Cancel", 0, 100, parent)
    progress.setWindowModality(Qt.WindowModal)

    movie_files = get_movies(state.video_path)
    duration = sum(m.length for m in movie_files)
    progress.setMaximum(duration)

    overlay_location = os.path.join(".", "overlay.mp4")

    encode_overlay(
        overlay_location,
        movie_files[0].pix_fmt,
        movie_files[0].width,
        movie_files[0].height,
        state,
        progress,
        duration,
    )

    progress.close()

    input_location = state.video_path
    if len(movie_files) > 1:
        input_location = concat(movie_files)

    encode_final(input_location, movie_files, out, overlay_location)
