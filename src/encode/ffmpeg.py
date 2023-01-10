import os


def get_ffmpeg_bin(executable_name="ffmpeg"):
    # TODO: find executable
    return os.path.join(".", "ffmpeg", executable_name)
