import os
import queue
from math import floor
from multiprocessing import Queue, Process, cpu_count

import ffmpeg

from state import AppState
from overlays.default import DefaultOverlay


def write_png(tempdir: str, q: Queue, w: int, h: int, fit_units: dict):
    overlay = DefaultOverlay(w, h)
    try:
        while frame := q.get(block=True, timeout=3):
            (second, fit_frame) = frame
            print(f"\r{second}", end="")
            second_leading = "{:0>5}".format(second)
            overlay.overlay(fit_frame, fit_units).save(
                os.path.join(tempdir, f"fit-{second_leading}.png"),
            )
    except queue.Empty as e:
        pass


def write_overlay_images(
    input_location: str,
    state: AppState,
    tempdir: str,
):
    probe = ffmpeg.probe(input_location)
    w = probe["streams"][0]["width"]
    h = probe["streams"][0]["height"]
    duration = round(float(probe["streams"][0]["duration"]))

    num_processes = floor(cpu_count() / 2)
    queue = Queue()

    for i in range(0, duration):
        queue.put((i, state.fit.get_point(i + state.fit_offset)))

    processes = []
    for i in range(0, num_processes):
        p = Process(target=write_png, args=(tempdir, queue, w, h, state.fit.units))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
