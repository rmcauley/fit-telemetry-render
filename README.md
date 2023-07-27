# FIT Render

Renders .FIT data on top of video files, with special care for GoPro videos meant for uploading to YouTube.

## What it Does

- Renders speed, cadence, heartrate, Di2, and altitude on top of videos
- Automatically merges GoPro segmented files together
- Ensures videos fit within YouTube's 128GB file size limit

## Prerequisites

- Install `ffmpeg` on PATH
- Install Python modules in `requirements.txt`

## How To

The app needs to be run in a terminal, as the export process has no GUI.

Run `src/main.py`:

1. Open a fit file.
2. Open a video file. Depending on the file name, the app will behave differently:

   - If the file matches a GoPro naming scheme (e.g. `GX010456.mp4`) it will assume all videos in the same directory were recorded on the same day, and will merge all GoPro files.
   - Otherwise, only the selected video is used.

3. Playback the video, and pause the video when you find a recognizable spot along your route. You can use the movie seek bar.
4. Move the bottom seek bar until the transparent marker on the map represents the location in the paused video. The opaque blue marker will represent the start location of your video.
5. Export

## Known Issues

- If you use h265 encoding on GoPro and are on Windows, you will need to purchase the HEVC Media Extensions on the Microsoft store
- No manual timer input for video if you want to avoid HEVC Media Extension by using an external app
- No loading indicator when loading FIT files (app will appear frozen)
- No status bar for video / video errors
- Video does not render preview immediately after opening
- FIT+Video offset bar does not return to previously saved position on app reload

## TODO

- Ability to select/deselect which gauges to display on export
