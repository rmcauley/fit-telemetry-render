class DefaultOverlay:
    def __init__(self, state):
        self._state = state

    def frame_to_image(self, frame, timestamp):
        return frame.to_image()