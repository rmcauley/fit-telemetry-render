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
blank_hr = "🖤"

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
    def __init__(self, state, w: int, h: int):
        super().__init__(state, w, h)

        if w < 3000:
            self.remainer_right_pad = 420
            self.remainer_bottom_pad = 60

            self.speed_right_pad = 80
            self.speed_bottom_pad = 60
            self.speed_label_right_pad = 90
            self.speed_label_bottom_pad = 250

            self.heart_right_pad = self.w - 400
            self.heart_bottom_pad = self.h - 112
            self.heart_scale = 0.8
            self.heart_colour_right_pad = self.heart_right_pad + 4
            self.heart_colour_bottom_pad = self.heart_bottom_pad + 4
            self.heart_colour_scale = 0.69

            self.font_xl = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 220)
            self.font_l = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 100)
            self.font_m = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 70)
            self.font_s = ImageFont.truetype("./fonts/RobotoCondensed-Bold.ttf", 40)
        else:
            self.remainer_right_pad = 700
            self.remainer_bottom_pad = 120

            self.speed_right_pad = 120
            self.speed_bottom_pad = 120
            self.speed_label_right_pad = 140
            self.speed_label_bottom_pad = 450

            self.heart_right_pad = self.w - 680
            self.heart_bottom_pad = self.h - 230
            self.heart_scale = 0.8
            self.heart_colour_right_pad = self.heart_right_pad + 8
            self.heart_colour_bottom_pad = self.heart_bottom_pad + 8
            self.heart_colour_scale = 0.69

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
            self.state.show_gears == 1
            and "front_gear_num" in fit_units
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
        if "grade" in fit_units and self.state.show_grade == 1:
            if "grade" in fit_frame:
                remainder.append(str(round(fit_frame["grade"])) + "%")
            else:
                remainder.append("-%")
        if "heart_rate" in fit_units:
            hr = fit_frame.get("heart_rate", "-")
            self.sensor_hr(hr)
            remainder.append(str(hr))

        self._draw.text(
            [self.w - self.remainer_right_pad, self.h - self.remainer_bottom_pad],
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
            [self.w - self.speed_right_pad, self.h - self.speed_bottom_pad],
            str(speed),
            fill=(255, 255, 255),
            font=self.font_xl,
            anchor="rb",
        )
        self._draw.text(
            [self.w - self.speed_label_right_pad, self.h - self.speed_label_bottom_pad],
            units,
            fill=(255, 255, 255),
            font=self.font_s,
            anchor="rb",
        )

    def sensor_hr(self, v):
        heart = hr_emoji[-1]
        if isinstance(v, str):
            heart = blank_hr
        else:
            for i, hr in enumerate(self.state.hr_zones):
                if v >= hr[0]:
                    heart = hr_emoji[i]
                    break

        self._pilmoji.text(
            [self.heart_right_pad, self.heart_bottom_pad],
            text="🤍",
            anchor="tl",
            font=self.font_m,
            emoji_scale_factor=self.heart_scale,
        )
        self._pilmoji.text(
            [self.heart_colour_right_pad, self.heart_colour_bottom_pad],
            text=heart,
            anchor="tl",
            font=self.font_m,
            emoji_scale_factor=self.heart_colour_scale,
        )
