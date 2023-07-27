from tempfile import TemporaryDirectory

from state import AppState

from .get_movies import get_movies
from .overlay import write_overlay_images
from .final import encode_final
from .concat import concat


def start_encode(state: AppState) -> None:
    movie_files = get_movies(state.video_path)

    with TemporaryDirectory(prefix=".temp", dir=".") as tempdir:
        write_overlay_images(movie_files, state, tempdir)
        encode_final(state, movie_files, state.export_path, tempdir)
