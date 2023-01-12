import os

import ffmpeg

NVIDIA_MAX_BITRATE = 60000


def encode_final(input_file: str, out: str, tempdir: str):
    duration = round(float(ffmpeg.probe(input_file)["streams"][0]["duration"]))
    max_rate = min(NVIDIA_MAX_BITRATE, int(((125000 * 8192) / duration) - 128))
    avg_rate = int(max_rate * 0.9)
    buf_size = avg_rate * 2

    input_audio_stream = ffmpeg.input(input_file).audio
    input_video_stream = ffmpeg.input(input_file).video
    overlay_stream = ffmpeg.input(
        os.path.join(tempdir, r"fit-%05d.png"),
        framerate="1",
        thread_queue_size="32",
    )
    overlaid_stream = ffmpeg.overlay(
        input_video_stream, overlay_stream, eof_action="pass"
    )
    runner = ffmpeg.output(
        input_audio_stream,
        overlaid_stream,
        out,
        **{
            "c:v": "hevc_nvenc",
            "preset": "medium",
            "rc-lookahead:v": "16",
            "b_ref_mode:v": "middle",
            "temporal-aq:v": "1",
            "spatial-aq:v": "1",
            "b:v": f"{avg_rate}K",
            "maxrate:v": f"{max_rate}K",
            "bufsize:v": f"{buf_size}K",
            "c:a": "copy",
            "movflags": "+faststart",
            "f": "mp4",
            "y": None,
            "hide_banner": None,
        },
    )
    runner.run()
