import os
import tempfile
import shlex
from typing import List

from .movie import Movie
from .ffmpeg import get_ffmpeg_bin


def concat(movie_files: List[Movie]) -> str:
    concat_path = os.path.join(".", "concat.txt")
    out_path = os.path.join(".", "merge.mp4")
    with open(concat_path, "w") as f:
        for movie in movie_files:
            ffmpeg_playlist_path = os.path.join(".", movie.path)
            f.write(f"file {shlex.quote(ffmpeg_playlist_path)}\n")

    ffmpeg_concat_opts = [
        "-f concat",
        "-safe 0",
        f"-i {concat_path}",
        "-c copy",
        out_path,
    ]

    os.system(get_ffmpeg_bin() + " " + " ".join(ffmpeg_concat_opts))

    return out_path
