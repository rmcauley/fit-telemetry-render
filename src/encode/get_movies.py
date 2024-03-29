import os
import re
from typing import List
import datetime

GOPRO_FILENAME_REGEX = re.compile(r"GX(\d\d)(\d+)\.MP4", flags=re.IGNORECASE)


def get_gopro_id(f):
    match = re.match(GOPRO_FILENAME_REGEX, f)
    if match:
        return match[2]
    return None


def gopro_sort(f):
    match = re.match(GOPRO_FILENAME_REGEX, f)
    id = match[2]
    chain = match[1]
    return f"{id}{chain}"


def get_movies(video_path: str) -> List[str]:
    ingest_path = os.path.dirname(video_path)
    video_filename = video_path[len(ingest_path) + 1 :]
    start_day = datetime.datetime.fromtimestamp(os.path.getctime(video_path)).strftime(
        r"%Y-%m-%d"
    )
    movie_files = []

    if get_gopro_id(video_filename) is not None:
        gopro_files = [
            f
            for f in os.listdir(ingest_path)
            if os.path.isfile(os.path.join(ingest_path, f))
            and datetime.datetime.fromtimestamp(
                os.path.getctime(os.path.join(ingest_path, f))
            ).strftime(r"%Y-%m-%d")
            == start_day
        ]
        movie_files = sorted(
            gopro_files,
            key=gopro_sort,
        )
        movie_files = [os.path.join(ingest_path, f) for f in movie_files]
    else:
        movie_files.append(video_path)

    return movie_files
