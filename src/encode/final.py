import os
from typing import List

import ffmpeg
from state import AppState

NVIDIA_MAX_BITRATE = 60000


def get_merged_stream(state: AppState, input_files: List[str]):
    duration = 0
    for f in input_files:
        duration += round(float(ffmpeg.probe(f)["streams"][0]["duration"]))
    max_rate = min(NVIDIA_MAX_BITRATE, int(((125000 * 8192) / duration) - 128))
    avg_rate = int(max_rate * 0.9)
    buf_size = avg_rate * 2

    input_video_kwargs = {}
    if state.encoder.startswith("nvidia"):
        input_video_kwargs.update({"hwaccel": "nvdec"})

    ffmpeg_options = {
        "c:a": "aac",
        "b:a": "128k",
        "movflags": "+faststart",
        "f": "mp4",
        "y": None,
        "hide_banner": None,
        "b:v": f"{avg_rate}K",
        "maxrate:v": f"{max_rate}K",
        "bufsize:v": f"{buf_size}K",
    }
    if state.encoder == "nvidia":
        ffmpeg_options.update(
            {
                "c:v": "hevc_nvenc",
                "preset": "fast",
                "rc-lookahead:v": 16,
                "b_ref_mode:v": "middle",
                "temporal-aq:v": 1,
                "spatial-aq:v": 1,
            }
        )
    else:
        ffmpeg_options.update({"c:v": "libx264", "preset": "fast"})
    return (input_video_kwargs, ffmpeg_options)


def get_ffmpeg_args(input_video_kwargs, input_args, ffmpeg_options, out):
    final_args = []
    for k, v in input_video_kwargs.items():
        final_args.append(f"-{k} {v}")
    final_args += input_args
    for k, v in ffmpeg_options.items():
        if v is None:
            final_args.append(f"-{k}")
        else:
            final_args.append(f"-{k} {v}")
    final_args.append("-f mp4")
    final_args.append(out)
    return " ".join(final_args)


def encode_final(state: AppState, input_files: List[str], out: str, tempdir: str):
    (input_video_kwargs, ffmpeg_options) = get_merged_stream(state, input_files)

    input_args = [f'-i "{input_filename}"' for input_filename in input_files]

    png_input = os.path.join(tempdir, r"fit-%05d.png")
    input_args.append(f'-framerate 1 -thread_queue_size 4096 -i "{png_input}"')

    concat_in_filter = "".join(
        f"[{index}:v:0][{index}:a:0]" for index, _ in enumerate(input_files)
    )
    concat_out_filter = f"concat=n={len(input_files)}:v=1:a=1[mergev][finala];"
    overlay_filter = f"[mergev][{len(input_args) - 1}:v]overlay=eof_action=pass[finalv]"
    input_args.append(
        f'-filter_complex "{concat_in_filter}{concat_out_filter}{overlay_filter}"'
    )
    input_args.append('-map "[finalv]" -map "[finala]"')

    os.system(
        "ffmpeg " + get_ffmpeg_args(input_video_kwargs, input_args, ffmpeg_options, out)
    )
