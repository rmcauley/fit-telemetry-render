import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressDialog, QWidget

from state import GoProState

from .movie import get_movies
from .overlay import write_overlay_images
from .final import encode_final_png
from .concat import concat


def start_encode(parent: QWidget, state: GoProState, out: str) -> None:
    progress = QProgressDialog("Encoding Overlay", "Cancel", 0, 100, parent)
    progress.setWindowModality(Qt.WindowModal)

    movie_files = get_movies(state.video_path)

    duration = sum(m.length for m in movie_files)
    progress.setMaximum(duration)

    write_overlay_images(
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

    encode_final_png(input_location, movie_files, out)
