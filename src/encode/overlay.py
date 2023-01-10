import av

from PySide6.QtWidgets import QProgressDialog

from state import GoProState


def encode_overlay(
    out: str,
    pix_fmt: str,
    w: int,
    h: int,
    state: GoProState,
    progress: QProgressDialog,
    duration: int,
):
    output = av.open(out, "w")
    output_stream_v = output.add_stream(av.Codec("libx264", mode="w"), 1.0)
    output_stream_v.options = {"crf": "0"}
    output_stream_v.pix_fmt = "yuv444p"
    output_stream_v.width = w
    output_stream_v.height = h

    pts = 0
    fit = state.fit
    fit_units = state.fit.units
    overlay = state.overlay(w, h)
    while pts <= duration and (fit_frame := fit.get_point(pts + state.fit_offset)):
        pts += 1

        packet = output_stream_v.encode(
            av.VideoFrame.from_image(overlay.overlay(fit_frame, fit_units))
        )
        output.mux(packet)
        progress.setValue(pts)

    output.close()
