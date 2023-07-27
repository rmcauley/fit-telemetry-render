import os

from state import AppState

from .final import get_merged_stream, get_ffmpeg_args
from .get_movies import get_movies
from .concat import concat


def youtube_encode(state: AppState):
    movie_files = get_movies(state.video_path)

    total_size_gb = 0
    for f in movie_files:
        total_size_gb += os.stat(f).st_size / (1024 * 1024 * 1024)

    if total_size_gb >= 126:
        (input_video_kwargs, ffmpeg_options) = get_merged_stream(state, movie_files)
        input_args = [f'-i "{input_filename}"' for input_filename in movie_files]
        concat_in_arg = "".join(
            f"[{index}:v:0][{index}:a:0]" for index, _ in enumerate(movie_files)
        )
        concat_out_arg = f"concat=n={len(movie_files)}:v=1:a=1[outv][outa]"
        input_args.append(f'-filter_complex "{concat_in_arg}{concat_out_arg}"')
        input_args.append('-map "[outv]" -map "[outa]"')

        os.system(
            "ffmpeg "
            + get_ffmpeg_args(
                input_video_kwargs, input_args, ffmpeg_options, state.youtube_path
            )
        )

    else:
        concat(movie_files, os.path.dirname(state.youtube_path))
