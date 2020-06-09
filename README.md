# GoPro Joiner
Joins GoPro videos together for Youtube uploading.

I often take long bike rides and record them to share with friends via YouTube.  This tool has saved me a lot of time in putting them together.

## Usage

- Have Python (3.6+) installed and ready to use
- Place `ffmpeg` and `ffprobe` into a `bin` directory underneath gopro.py
- Place your movie files into an `in` directory underneath gopro.py
- Run the script
- Your file ready for Youtube will be available in `merge.mp4`

## What it Does

- Re-encodes to fit under Youtube's 128GB file size limit if necessary
- Re-encodes to flip any sections of upside-down video from e.g. handlebar mounts if multiple rotations are detected
- If not necessary, merges all files together without re-encoding

## Known Issues

- Only encodes using nVidia HEVC and decodes using nVidia HW
- Not tested on Linux
- Does not support ffmpeg existing on the path
- All input files must be from the same GoPro size, framerate, and encoder settings
- Undiagnosed, but certain combinations of files will not concatenate and must be re-encoded manually