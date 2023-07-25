import os
import ffmpeg

from state import AppState

from .final import get_merged_stream
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
        audio_encode_args = ["-c:a aac", "-b:a 128k"]
        concat_in_arg = "".join(
            f"[{index}:v:0][{index}:a:0]" for index, _ in enumerate(movie_files)
        )
        concat_out_arg = f"concat=n={len(movie_files)}:v=1:a=1[outv][outa]"
        input_args.append(f'-filter_complex "{concat_in_arg}{concat_out_arg}"')
        input_args.append('-map "[outv]" -map "[outa]"')

        final_args = []
        for k, v in input_video_kwargs.items():
            final_args.append(f"-{k} {v}")
        final_args += input_args
        final_args += audio_encode_args
        for k, v in ffmpeg_options.items():
            if k != "c:a":
                if v is None:
                    final_args.append(f"-{k}")
                else:
                    final_args.append(f"-{k} {v}")
        final_args.append("-f mp4")
        final_args.append(state.youtube_path)
        os.system("ffmpeg " + " ".join(final_args))

    else:
        concat(movie_files, os.path.dirname(state.youtube_path))
