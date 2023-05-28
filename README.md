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
2. Open your video, or the first GoPro video in the chain. (`GX01#####.mp4`)
3. Playback the video, and pause the video when you find a recognizable spot along your route. You can use the movie seek bar.
4. Move the bottom seek bar until the transparent marker on the map represents the location in the paused video. The opaque blue marker will represent the start location of your video.
5. Export

Currently, video export will happen in 3 stages:

1. A concatenated version of your GoPro file(s) in proper order will be produced if necessary and placed in the same directory as your GoPro files, if you wish to re-export. This can be deleted afterwards.
2. Overlay images will be generated.
3. The final video will be made.

## Known Issues

- If you use h265 encoding on GoPro and are on Windows, you will need to purchase the HEVC Media Extensions on the Microsoft store
- No manual timer input for video if you want to avoid HEVC Media Extension by using an external app
- No loading indicator when loading FIT files (app will appear frozen)
- No status bar for video / video errors
- Video does not render preview immediately after opening
- FIT+Video offset bar does not return to previously saved position on app reload

## TODO

- Ability to select/deselect which gauges to display on export
