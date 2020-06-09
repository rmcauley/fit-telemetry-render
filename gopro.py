import os
import time
import sys
import json
import subprocess
import shutil
import shlex
from typing import List, Union
from stat import S_ISREG, ST_CTIME, ST_MODE, ST_SIZE

from moviepy.video.io.VideoFileClip import VideoFileClip

INGEST_PATH = "in"
FFMPEG_PLAYLIST_PATH = "in.txt"
OUTPUT_PATH = "merge.mp4"
NVIDIA_MAX_BITRATE = 50000


def get_ffmpeg_bin(executable_name="ffmpeg"):
    # TODO: find executable
    return os.path.join(".", "bin", executable_name)


def get_ffmpeg_args(
    input_filenames: List[str],
    output_filename: str,
    bitrate_encode_args: List[str] = None,
    other_args=[],
    debug=False,
):
    # TODO: support x264 if nvidia hardware not available
    log_args = []
    if debug:
        log_args.append("-loglevel debug")
    video_decode_args = [
        "-hwaccel cuda",
    ]
    video_encode_args = [
        "-c:v hevc_nvenc",
        "-preset medium",
        "-rc-lookahead:v 32",
        "-b_ref_mode:v middle",
        "-temporal-aq:v 1",
    ]
    audio_encode_args = []
    if not bitrate_encode_args:
        bitrate_encode_args = [
            f"-b:v {NVIDIA_MAX_BITRATE}K",
        ]
    input_args = [f"-i {input_filename}" for input_filename in input_filenames]
    if len(input_filenames) > 1:
        audio_encode_args = ["-c:a aac", "-b:a 128k"]
        concat_in_arg = "".join(
            f"[{index}:v:0][{index}:a:0]" for index, _ in enumerate(input_filenames)
        )
        concat_out_arg = f"concat=n={len(input_filenames)}:v=1:a=1[outv][outa]"
        input_args.append(f'-filter_complex "{concat_in_arg}{concat_out_arg}"')
        input_args.append('-map "[outv]" -map "[outa]"')
    else:
        audio_encode_args.append("-c:a copy")

    return " ".join(
        log_args
        + video_decode_args
        + input_args
        + video_encode_args
        + other_args
        + audio_encode_args
        + bitrate_encode_args
        + ["-movflags +faststart", "-f mp4", output_filename]
    )


class GoProMovie:
    ctime: int
    size: int
    path: str
    filename: str
    rotation: Union[str, None] = None

    def __init__(self, filename: str, path: str, statinfo: os.stat_result) -> None:
        self.filename = filename
        self.path = path
        self.ctime = statinfo[ST_CTIME]
        self.size = statinfo[ST_SIZE]


movie_files: List[GoProMovie] = []
for filename in os.listdir(INGEST_PATH):
    filename_with_path = os.path.join(INGEST_PATH, filename)
    statinfo = os.stat(filename_with_path)
    if S_ISREG(statinfo[ST_MODE]):
        movie_files.append(GoProMovie(filename, filename_with_path, statinfo))
movie_files = sorted(movie_files, key=lambda m: m.ctime)
movie_files.reverse()

total_length = 0
total_size = 0
rotations = []

for movie in movie_files:
    print(f"Inspecting: {movie.path}")
    total_size += movie.size
    with VideoFileClip(movie.path) as clip:
        total_length += int(clip.duration)

    ffprobe_opts = [
        "-loglevel error",
        "-select_streams v:0",
        "-show_entries stream_tags=rotate",
        "-print_format json",
        f"-i {movie.path}",
    ]
    result = json.loads(
        subprocess.run(
            get_ffmpeg_bin("ffprobe") + " " + " ".join(ffprobe_opts),
            capture_output=True,
        ).stdout
    )
    movie.rotation = result["streams"][0]["tags"].get("rotate")
    rotations.append(movie.rotation)

total_size_mb = int(total_size / 1024 / 1024)
total_size_gb = int(total_size_mb / 1024)

print(
    "Movie total: %02d:%02d:%02d %sGB"
    % (
        total_length // 60 // 60,
        total_length // 60 % 60,
        total_length % 60,
        total_size_gb,
    )
)


if total_size_gb > 125 or len(rotations) > 1:
    # https://trac.ffmpeg.org/wiki/Encode/H.265
    current_bitrate = int(((total_size_mb * 8192) / total_length) - 128)
    max_rate = min(NVIDIA_MAX_BITRATE, int(((125000 * 8192) / total_length) - 128))
    avg_rate = int(max_rate * 0.9)
    buf_size = avg_rate * 2
    print(
        f" Current average: {current_bitrate}kbps.  Target max: {max_rate}kbps.  Target average: {avg_rate}kbps."
    )
    other_args = []
    if len(rotations) > 1:
        other_args.append("-map_metadata -1")
    os.system(
        get_ffmpeg_bin()
        + " "
        + get_ffmpeg_args(
            input_filenames=[os.path.join(".", movie.path) for movie in movie_files],
            output_filename=OUTPUT_PATH,
            bitrate_encode_args=[
                f"-b:v {avg_rate}K",
                f"-maxrate:v {max_rate}K",
                f"-bufsize:v {buf_size}K",
            ],
            other_args=other_args,
        )
    )
else:
    with open(FFMPEG_PLAYLIST_PATH, "w") as f:
        for movie in movie_files:
            ffmpeg_playlist_path = os.path.join(".", movie.path)
            f.write(f"file {shlex.quote(ffmpeg_playlist_path)}\n")

    ffmpeg_concat_opts = [
        "-f concat",
        "-safe 0",
        f"-i {FFMPEG_PLAYLIST_PATH}",
        "-c copy",
        OUTPUT_PATH,
    ]

    os.system(get_ffmpeg_bin() + " " + " ".join(ffmpeg_concat_opts))
