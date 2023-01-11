import os
import shlex
from typing import List


def concat(movie_files: List[str], tempdir: str) -> str:
    concat_path = os.path.join(".", "concat.txt")
    with open(concat_path, "w") as f:
        for movie in movie_files:
            ffmpeg_playlist_path = os.path.join(".", movie)
            f.write(f"file {shlex.quote(ffmpeg_playlist_path)}\n")

    outpath = os.path.join(tempdir, "merge.mp4")
    ffmpeg_concat_opts = [
        "-f concat",
        "-safe 0",
        f"-i {concat_path}",
        "-c copy",
        "-y",
        outpath,
    ]
    os.system("ffmpeg " + " ".join(ffmpeg_concat_opts))

    return outpath
