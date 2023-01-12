from .base import BaseOverlay

from PIL import ImageFont

draw_keys = [
    "speed",
    "altitude",
    "grade",
    "cadence",
    "front_gear_num",
    "rear_gear_num",
    "heart_rate",
]

rear_gears = [
    "11",
    "12",
    "13",
    "14",
    "15",
    "17",
    "19",
    "21",
    "24",
    "27",
    "30",
    "34",
    "",
]
rear_gears.reverse()
front_gears = ["", "34", "50"]

hr_zones = [
    (-1, (0, 86, 147, 255)),
    (134, (0, 100, 0, 255)),
    (149, (100, 77, 0, 255)),
    (164, (100, 0, 0, 255)),
    (173, (100, 0, 100, 255)),
]
hr_zones.reverse()

grades = [
    (-100, (64, 64, 64, 255)),
    (3, (0, 100, 0, 255)),
    (5, (100, 77, 0, 255)),
    (7, (100, 0, 0, 255)),
    (9, (100, 0, 100, 255)),
    (12, (100, 0, 100, 255)),
]
grades.reverse()


class DefaultOverlay(BaseOverlay):
    font_l: ImageFont
    font_s: ImageFont

    sensor_block_w = 400
    sensor_block_h = 290
    sensor_block_pad = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font_l = ImageFont.truetype("./fonts/JetBrainsMono-ExtraBold.ttf", 200)
        self.font_m = ImageFont.truetype("./fonts/JetBrainsMono-ExtraBold.ttf", 148)
        self.font_s = ImageFont.truetype("./fonts/JetBrainsMono-ExtraBold.ttf", 60)

    def draw(self, fit_frame: dict, fit_units: dict) -> None:
        sensor_count = 0
        for key in draw_keys:
            if key in fit_frame:
                sensor_count += 1
        width = sensor_count * self.sensor_block_w + (
            (sensor_count - 1) * self.sensor_block_pad
        )
        x = (self.w / 2) - (width / 2)
        y = self.h - self.sensor_block_h

        if "speed" in fit_frame:
            self.sensor_block(
                x, y, fit_units["speed"].upper(), round(fit_frame["speed"])
            )
            x += self.sensor_block_w + self.sensor_block_pad
        if "heart_rate" in fit_frame:
            self.sensor_hr(x, y, fit_frame["heart_rate"])
            x += self.sensor_block_w + self.sensor_block_pad
        if "cadence" in fit_frame:
            self.sensor_block(x, y, fit_units["cadence"].upper(), fit_frame["cadence"])
            x += self.sensor_block_w + self.sensor_block_pad
        if "grade" in fit_frame:
            self.sensor_grade(x, y, fit_frame["grade"])
            x += self.sensor_block_w + self.sensor_block_pad
        if "front_gear_num" in fit_frame:
            self.sensor_block(
                x,
                y,
                "FRONT GEAR",
                front_gears[round(fit_frame["front_gear_num"])] + "T",
            )
            x += self.sensor_block_w + self.sensor_block_pad
        if "rear_gear_num" in fit_frame:
            self.sensor_block(
                x, y, "REAR GEAR", rear_gears[round(fit_frame["rear_gear_num"])] + "T"
            )
            x += self.sensor_block_w + self.sensor_block_pad
        if "altitude" in fit_frame:
            self.sensor_block(x, y, "ALTITUDE", round(fit_frame["altitude"]))
            x += self.sensor_block_w

    def sensor_rect(self, x, y, fill=(64, 64, 64, 255)):
        self._draw.rectangle(
            (x, y, x + self.sensor_block_w, y + self.sensor_block_h),
            fill=fill,
            outline=(0, 0, 0, 255),
            width=2,
        )

    def sensor_h(self, x, y, h):
        self._draw.text(
            [x + (self.sensor_block_w / 2), (y + 195)],
            h,
            fill=(255, 255, 255),
            font=self.font_s,
            anchor="ma",
        )

    def sensor_v(self, x, y, v):
        font = self.font_l
        if isinstance(v, int) and (v > 1000 or v < -99):
            font = self.font_m
        elif isinstance(v, str) and len(v) > 3:
            font = self.font_m

        self._draw.text(
            [x + (self.sensor_block_w / 2), y + 110],
            str(v),
            fill=(255, 255, 255),
            font=font,
            anchor="mm",
        )

    def sensor_block(self, x, y, h, v):
        self.sensor_rect(x, y)
        self.sensor_v(x, y, v)
        self.sensor_h(x, y, h)

    def sensor_hr(self, x, y, v):
        for hr in hr_zones:
            if v >= hr[0]:
                self.sensor_rect(x, y, hr[1])
                break
        self.sensor_v(x, y, v)
        self.sensor_h(x, y, "BPM")

    def sensor_grade(self, x, y, v):
        self.sensor_rect(x, y)
        if v > 0:
            for g in grades:
                if v >= g[0]:
                    self._draw.polygon(
                        (
                            (x, y + self.sensor_block_h),
                            (
                                x + self.sensor_block_w,
                                max(y, y + self.sensor_block_h - (v * 20)),
                            ),
                            (x + self.sensor_block_w, y + self.sensor_block_h),
                        ),
                        fill=g[1],
                    )
                    break

        self.sensor_h(x, y, "GRADE")
        self.sensor_v(x, y, str(round(v)) + "%")
