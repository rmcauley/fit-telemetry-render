import os
import queue
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
    input_location: str,
    state: AppState,
    tempdir: str,
):
    probe = ffmpeg.probe(input_location)
    w = probe["streams"][0]["width"]
    h = probe["streams"][0]["height"]
    duration = round(float(probe["streams"][0]["duration"]))

    # Dividing by 2 produces ~60% utilization on a Ryzen 5900X
    # Dividing by 1.5 produces 85-95% utilization on a Ryzen 5900X
    num_processes = floor(cpu_count() / 1.5)
    queue = Queue()

    for i in range(0, duration):
        queue.put((i, state.fit.get_point(i + state.fit_offset)))

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
