import os
import re
from stat import ST_SIZE, S_ISREG, ST_MODE
from typing import List

import av

from .consts import GOPRO_FILENAME_REGEX


class Movie:
    size: int
    path: str
    frames: int
    length: int
    video_id: str
    chain_index: str

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.path

    def __init__(self, path: str, statinfo: os.stat_result) -> None:
        self.path = path
        self.size = statinfo[ST_SIZE]
        with av.open(path) as container:
            video = container.streams.video[0]
            self.frames = video.frames
            self.length = int(video.duration * video.time_base)
            self.width = video.width
            self.height = video.height
            self.pix_fmt = video.pix_fmt
        result = GOPRO_FILENAME_REGEX.match(path.split(os.path.sep)[-1])
        if result:
            self.video_id = result[2]
            self.chain_index = result[1]
        else:
            self.video_id = 0
            self.chain_index = 0

    def to_sortable(self):
        return f"{self.video_id}-{self.chain_index}"


def get_movies(video_path: str) -> List[Movie]:
    ingest_path = os.path.dirname(video_path)
    video_filename = video_path[len(ingest_path) + 1 :]
    gopro_match = re.match(GOPRO_FILENAME_REGEX, video_filename)
    movie_files = []
    if gopro_match and gopro_match[1] == "01":
        gopro_id = gopro_match[2]
        chain_index = 1
        while True:
            chain_index_str = str(chain_index).zfill(2)
            filename = f"GX{chain_index_str}{gopro_id}.mp4"
            filename_with_path = os.path.join(ingest_path, filename)
            if not os.path.exists(filename_with_path):
                break
            statinfo = os.stat(filename_with_path)
            if S_ISREG(statinfo[ST_MODE]):
                movie_files.append(Movie(filename_with_path, statinfo))
            chain_index += 1
        movie_files.sort(key=lambda m: m.to_sortable())
    else:
        statinfo = os.stat(video_path)
        if S_ISREG(statinfo[ST_MODE]):
            movie_files.append(Movie(video_path, statinfo))
    return movie_files
