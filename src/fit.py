from collections import OrderedDict

import fitdecode


class FitDict(OrderedDict):
    units: dict
    min_lat: int
    min_long: int
    max_lat: int
    max_long: int
    mid_lat: int
    mid_long: int

    def __init__(self, *args, **kwargs) -> None:
        self.units = {}
        self.min_lat = 255
        self.min_long = 255
        self.max_lat = -255
        self.max_long = -255
        self.mid_lat = 0
        self.mid_long = 0
        super().__init__(*args, **kwargs)

    def set_unit(self, key: str, unit: str) -> None:
        self.units[key] = unit

    def get_point(self, second: int) -> dict:
        d = None
        attempts = 0
        while d is None:
            d = self.get(second - attempts, None)
            attempts += 1
            if attempts > 5:
                break
        return d


def get_fit_dict(path: str) -> FitDict:
    fitted = FitDict()

    with fitdecode.FitReader(path) as fit:
        time_created = 0
        frame_values = {}
        for frame in fit:
            if frame.frame_type == 4:
                if not time_created and frame.has_field("time_created"):
                    time_created = frame.get_value("time_created")

            if frame.frame_type == 4 and frame.name == "event":
                event = frame.get_value("event")
                if isinstance(event, str) and event.endswith("gear_change"):
                    frame_values.update(
                        {
                            "front_gear_num": frame.get_value("front_gear_num"),
                            "rear_gear_num": frame.get_value("rear_gear_num"),
                        }
                    )
                    fitted[
                        round(
                            (
                                frame_values.get("timestamp", time_created)
                                - time_created
                            ).total_seconds()
                        )
                    ] = frame_values.copy()
            elif frame.frame_type == 4 and frame.name == "record":
                for f in frame.fields:
                    if f.field_def and f.value is not None:
                        if f.units:
                            if f.field_def.name == "speed" and f.units == "m/s":
                                f.units = "km/h"
                                f.value = round(f.value * 3.6, 2)
                            fitted.set_unit(f.field_def.name, f.units)

                        if f.field_def.name == "position_long":
                            f.value = f.value / 11930465
                            if f.value < fitted.min_long:
                                fitted.min_long = f.value
                            if f.value > fitted.max_long:
                                fitted.max_long = f.value
                        elif f.field_def.name == "position_lat":
                            f.value = f.value / 11930465
                            if f.value < fitted.min_lat:
                                fitted.min_lat = f.value
                            if f.value > fitted.max_lat:
                                fitted.max_lat = f.value
                        frame_values[f.field_def.name] = f.value
                fitted[
                    round(
                        (
                            frame_values.get("timestamp", time_created) - time_created
                        ).total_seconds()
                    )
                ] = frame_values.copy()

    fitted.min_lat = (fitted.max_lat + fitted.min_lat) / 2
    fitted.mid_long = (fitted.max_long + fitted.min_long) / 2

    return fitted
