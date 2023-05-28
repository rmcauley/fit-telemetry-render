import os
from tempfile import TemporaryDirectory

from state import AppState

from .get_movies import get_movies
from .overlay import write_overlay_images
from .final import encode_final
from .concat import concat


def start_encode(state: AppState) -> None:
    movie_files = get_movies(state.video_path)

    with TemporaryDirectory(prefix=".temp", dir=".") as tempdir:
        input_location = movie_files[0]
        if len(movie_files) > 1:
            input_location = concat(movie_files, os.path.dirname(input_location))

        write_overlay_images(input_location, state, tempdir)

        encode_final(state, input_location, state.export_path, tempdir)
