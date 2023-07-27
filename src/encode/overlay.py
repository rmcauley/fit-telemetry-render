import os
import queue
from math import ceil
from typing import List
from math import floor
from multiprocessing import Queue, Process, cpu_count

import ffmpeg

from state import StateForOverlay, AppState


def write_png(state: StateForOverlay, tempdir: str, q: Queue, w: int, h: int):
    overlay = state.overlay_class(state, w, h)
    try:
        while frame := q.get(block=True, timeout=3):
            (second, fit_frame) = frame
            print(f"\r{second} of {state.duration}", end="")
            second_leading = "{:0>5}".format(second)
            overlay.overlay(fit_frame).save(
                os.path.join(tempdir, f"fit-{second_leading}.png"),
            )
    except queue.Empty as e:
        pass


def write_overlay_images(
    movie_files: List[str],
    state: AppState,
    tempdir: str,
):
    probe = ffmpeg.probe(movie_files[0])
    first_movie_ctime = os.path.getctime(movie_files[0])
    w = probe["streams"][0]["width"]
    h = probe["streams"][0]["height"]

    # Dividing by 2 produces ~60% utilization on a Ryzen 5900X
    # Dividing by 1.5 produces 85-95% utilization on a Ryzen 5900X
    num_processes = floor(cpu_count() / 1.5)
    queue = Queue()

    duration = 0
    for m in movie_files:
        probe = ffmpeg.probe(m)
        m_duration = float(probe["streams"][0]["duration"])
        start_time_offset = os.path.getctime(m) - first_movie_ctime
        for i in range(0, floor(m_duration)):
            queue.put(
                (
                    i + duration,
                    state.fit.get_point(i + state.fit_offset + start_time_offset),
                )
            )
        duration += floor(m_duration)

    overlay_state = state.get_state_for_overlay()
    overlay_state.duration = duration

    processes = []
    for i in range(0, num_processes):
        p = Process(
            target=write_png,
            args=(overlay_state, tempdir, queue, w, h),
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
