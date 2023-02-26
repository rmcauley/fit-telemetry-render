import fitdecode


class FitFile(dict):
    units: dict
    min_lat: int
    min_long: int
    max_lat: int
    max_long: int
    mid_lat: int
    mid_long: int
    max: dict
    min: dict

    def __init__(self, *args, **kwargs) -> None:
        self.units = {}
        self.min_lat = 255
        self.min_long = 255
        self.max_lat = -255
        self.max_long = -255
        self.mid_lat = 0
        self.mid_long = 0
        self.max = {}
        self.min = {}
        super().__init__(*args, **kwargs)

    def get_point(self, second: int) -> dict:
        d = None
        while d is None and second >= 0:
            d = self.get(second, None)
            second -= 1
        return d or {}


def get_fit_dict(path: str) -> FitFile:
    fitted = FitFile()
    duration = 0

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
                    fitted.units["front_gear_num"] = "T"
                    fitted.unuts["rear_gear_num"] = "T"
                    second = round(
                        (
                            frame_values.get("timestamp", time_created) - time_created
                        ).total_seconds()
                    )
                    fitted[second] = frame_values.copy()
                    duration = max(duration, second)
            elif frame.frame_type == 4 and frame.name == "record":
                for f in frame.fields:
                    if f.field_def and f.value is not None:
                        if f.units:
                            if f.field_def.name == "speed" and f.units == "m/s":
                                f.units = "km/h"
                                f.value = round(f.value * 3.6)
                            fitted.units[f.field_def.name] = f.units

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

                        if (
                            not fitted.max.get(f.field_def.name)
                            or f.value > fitted.max[f.field_def.name]
                        ):
                            fitted.max[f.field_def.name] = f.value
                        if f.value > 0 and (
                            not fitted.min.get(f.field_def.name)
                            or f.value < fitted.min[f.field_def.name]
                        ):
                            fitted.min[f.field_def.name] = f.value

                second = round(
                    (
                        frame_values.get("timestamp", time_created) - time_created
                    ).total_seconds()
                )
                fitted[second] = frame_values.copy()
                duration = max(duration, second)

    # fill gaps in keys
    for i in range(duration):
        if not fitted.get(i, None):
            fitted[i] = fitted.get_point(i)

    fitted.min_lat = (fitted.max_lat + fitted.min_lat) / 2
    fitted.mid_long = (fitted.max_long + fitted.min_long) / 2

    return fitted
