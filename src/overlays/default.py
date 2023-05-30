from .base import BaseOverlay

from PIL import ImageFont

draw_keys = [
    "speed",
    "altitude",
    "grade",
    "front_gear_num",
    "rear_gear_num",
    "heart_rate",
]

hr_emoji = ["💜", "❤️", "💛", "💚", "💙"]

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

        self.font_xl = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 400)
        self.font_l = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 200)
        self.font_m = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 148)
        self.font_s = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 60)

    def draw(self, fit_frame: dict) -> None:
        fit_units = self.state.fit_units
        remainder = []

        if "speed" in fit_units:
            self.speed(
                fit_frame.get("speed", "-"),
                fit_units["speed"].upper(),
                None,  # fit_file.max.get("speed"),
            )
        if (
            "front_gear_num" in fit_units
            and "rear_gear_num" in fit_units
            and "front_gear_num" in fit_frame
            and "rear_gear_num" in fit_frame
        ):
            try:
                front_gear = int(
                    self.state.front_gears[round(fit_frame["front_gear_num"])]
                )
                rear_gear = int(
                    self.state.rear_gears[round(fit_frame["rear_gear_num"])]
                )
                remainder.append(f"{rear_gear}/{front_gear}")
            except ValueError:
                remainder.append("-.--" + "x")
        if (
            "altitude" in fit_units
            and "altitude" in fit_frame
            and self.state.show_alt == 1
        ):
            altitude = round(fit_frame["altitude"]) if "altitude" in fit_frame else "-"
            remainder.append(f"{altitude}{fit_units['altitude']}")
        if "grade" in fit_units and "grade" in fit_frame and self.state.show_grade == 1:
            remainder.append(str(round(fit_frame["grade"])) + "%")
        if "heart_rate" in fit_units:
            hr = fit_frame.get("heart_rate", "-")
            self.sensor_hr(hr)
            remainder.append(str(hr))

        self._draw.text(
            [self.w - 700, self.h - 120],
            "  ".join(remainder),
            fill=(255, 255, 255),
            font=self.font_m,
            anchor="rb",
        )

    def speed(self, speed, units, max_speed):
        # An arc for a speedometer that would need frame-by-frame rendering
        # self._draw.arc(
        #     [(self.w - 800, self.h - 900), (self.w - 50, self.h - 50)],
        #     start=90,
        #     end=270 * (speed / max_speed) + 90,
        #     fill=(255, 255, 255, 255),
        #     width=70,
        # )
        self._draw.text(
            [self.w - 120, self.h - 120],
            str(speed),
            fill=(255, 255, 255),
            font=self.font_xl,
            anchor="rb",
        )
        self._draw.text(
            [self.w - 140, self.h - 450],
            units,
            fill=(255, 255, 255),
            font=self.font_s,
            anchor="rb",
        )

    def sensor_hr(self, v):
        heart = hr_emoji[-1]
        if isinstance(v, str):
            return
        for i, hr in enumerate(self.state.hr_zones):
            if v >= hr[0]:
                heart = hr_emoji[i]
                break
        self._pilmoji.text(
            [self.w - 680, self.h - 230],
            text="🤍",
            anchor="tl",
            font=self.font_m,
            emoji_scale_factor=0.8,
        )
        self._pilmoji.text(
            [self.w - 680 + 8, self.h - 222],
            text=heart,
            anchor="tl",
            font=self.font_m,
            emoji_scale_factor=0.69,
        )
