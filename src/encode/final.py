import os
from typing import List

import ffmpeg

from .movie import Movie
from .consts import NVIDIA_MAX_BITRATE


def encode_final_png(input_file: str, movie_files: List[Movie], out: str):
    total_length = int(sum(m.length for m in movie_files))
    total_size_mb = int(sum(m.size for m in movie_files) / 1024 / 1024)
    total_size_gb = int(total_size_mb / 1024)

    max_rate = NVIDIA_MAX_BITRATE
    if total_size_gb > 125:
        max_rate = min(NVIDIA_MAX_BITRATE, int(((125000 * 8192) / total_length) - 128))

    avg_rate = int(max_rate * 0.9)
    buf_size = avg_rate * 2

    input_stream = ffmpeg.input(input_file)
    overlay_stream = ffmpeg.input(
        os.path.join(".", "png", r"fit-%05d.png"), framerate="1", thread_queue_size="32"
    )
    overlaid_stream = ffmpeg.overlay(input_stream, overlay_stream, eof_action="pass")
    overlaid_stream = overlaid_stream.output(
        out,
        **{
            "c:v": "hevc_nvenc",
            "preset": "medium",
            "rc-lookahead:v": "32",
            "b_ref_mode:v": "middle",
            "temporal-aq:v": "1",
            "b:v": f"{avg_rate}K",
            "maxrate:v": f"{max_rate}K",
            "bufsize:v": f"{buf_size}K",
            "c:a": "copy",
            "movflags": "+faststart",
            "f": "mp4",
            "y": None,
        },
    )
    print(ffmpeg.get_args(overlaid_stream))
    overlaid_stream.run()
