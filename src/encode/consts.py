import re

GOPRO_FILENAME_REGEX = re.compile(r"GX(\d\d)(\d+)\.MP4", flags=re.IGNORECASE)
NVIDIA_MAX_BITRATE = 50000
