import os
import queue
from time import sleep
from multiprocessing import Queue, Process, connection

from PySide6.QtWidgets import QProgressDialog

from state import GoProState
from overlays.default import DefaultOverlay


def write_png(q, w, h, fit_units):
    overlay = DefaultOverlay(w, h)
    try:
        while frame := q.get(block=True, timeout=3):
            (second, fit_frame) = frame
            print(second)
            second_leading = "{:0>5}".format(second)
            overlay.overlay(fit_frame, fit_units).save(
                os.path.join(".", "png", f"fit-{second_leading}.png"),
            )
    except queue.Empty as e:
        pass
    print("process done")


def write_overlay_images(
    w: int,
    h: int,
    state: GoProState,
    progress: QProgressDialog,
    duration: int,
):
    fit = state.fit
    num_processes = 12
    queue = Queue()

    for i in range(0, duration + 1):
        queue.put((i, fit.get_point(i + state.fit_offset)))

    processes = []
    for i in range(0, num_processes):
        p = Process(target=write_png, args=(queue, w, h, state.fit.units))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("ok bye")
