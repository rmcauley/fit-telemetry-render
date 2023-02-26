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

1. Open a fit file
2. Open your video, or the first GoPro video in the chain (`GX01#####.mp4`)
3. Find a recognizable spot in the video using the seek bar that was along your route (intersections work well)
4. Align the semi-transparent mark on the map with the location your video is at, using the larger seek bar at the bottom
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
