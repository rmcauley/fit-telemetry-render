import os
import re
from typing import List

GOPRO_FILENAME_REGEX = re.compile(r"GX(\d\d)(\d+)\.MP4", flags=re.IGNORECASE)


def get_movies(video_path: str) -> List[str]:
    ingest_path = os.path.dirname(video_path)
    video_filename = video_path[len(ingest_path) + 1 :]
    movie_files = []

    gopro_match = re.match(GOPRO_FILENAME_REGEX, video_filename)
    if gopro_match and gopro_match[1] == "01":
        gopro_id = gopro_match[2]
        chain_index = 1
        while True:
            filename_with_path = os.path.join(
                ingest_path, f"GX{str(chain_index).zfill(2)}{gopro_id}.mp4"
            )
            if not os.path.exists(filename_with_path):
                break
            movie_files.append(filename_with_path)
            chain_index += 1
    else:
        movie_files.append(video_path)

    return movie_files
